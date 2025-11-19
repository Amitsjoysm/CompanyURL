"""
Security middleware and utilities for enhanced application security
"""
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from typing import Callable
import time
import logging
from collections import defaultdict
from datetime import datetime, timedelta, timezone
import re

logger = logging.getLogger(__name__)

# In-memory store for rate limiting (use Redis in production)
rate_limit_store = defaultdict(list)
login_attempts = defaultdict(list)

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        # Content Security Policy
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self' https://api.razorpay.com https://api.hubapi.com; "
            "frame-ancestors 'none';"
        )
        response.headers["Content-Security-Policy"] = csp
        
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware"""
    
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.window_seconds = 60
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip rate limiting for health checks
        if request.url.path in ["/api/health", "/api/"]:
            return await call_next(request)
        
        # Get client identifier (IP or user ID from token)
        client_id = self._get_client_id(request)
        
        # Check rate limit
        now = time.time()
        window_start = now - self.window_seconds
        
        # Clean old requests
        rate_limit_store[client_id] = [
            req_time for req_time in rate_limit_store[client_id] 
            if req_time > window_start
        ]
        
        # Check if limit exceeded
        if len(rate_limit_store[client_id]) >= self.requests_per_minute:
            logger.warning(f"Rate limit exceeded for client: {client_id}")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please try again later."
            )
        
        # Add current request
        rate_limit_store[client_id].append(now)
        
        response = await call_next(request)
        
        # Add rate limit headers
        remaining = self.requests_per_minute - len(rate_limit_store[client_id])
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(max(0, remaining))
        response.headers["X-RateLimit-Reset"] = str(int(window_start + self.window_seconds))
        
        return response
    
    def _get_client_id(self, request: Request) -> str:
        """Get client identifier from request"""
        # Try to get user ID from authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            try:
                from core.auth import decode_token
                token = auth_header.split(" ")[1]
                payload = decode_token(token)
                return f"user:{payload.get('sub')}"
            except:
                pass
        
        # Fall back to IP address
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return f"ip:{forwarded_for.split(',')[0].strip()}"
        
        client_host = request.client.host if request.client else "unknown"
        return f"ip:{client_host}"


class RequestSizeLimitMiddleware(BaseHTTPMiddleware):
    """Limit request body size to prevent memory exhaustion"""
    
    def __init__(self, app, max_size: int = 10 * 1024 * 1024):  # 10MB default
        super().__init__(app)
        self.max_size = max_size
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Check Content-Length header
        content_length = request.headers.get("Content-Length")
        
        if content_length:
            if int(content_length) > self.max_size:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"Request body too large. Maximum size: {self.max_size} bytes"
                )
        
        return await call_next(request)


def validate_password_strength(password: str) -> tuple[bool, str]:
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit"
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"
    
    return True, "Password is strong"


def check_login_attempts(email: str, max_attempts: int = 5, window_minutes: int = 15) -> bool:
    """Check if user has exceeded login attempts"""
    now = datetime.now(timezone.utc)
    window_start = now - timedelta(minutes=window_minutes)
    
    # Clean old attempts
    login_attempts[email] = [
        attempt_time for attempt_time in login_attempts[email]
        if attempt_time > window_start
    ]
    
    # Check if locked out
    if len(login_attempts[email]) >= max_attempts:
        logger.warning(f"Account locked due to too many failed login attempts: {email}")
        return True
    
    return False


def record_failed_login(email: str):
    """Record a failed login attempt"""
    login_attempts[email].append(datetime.now(timezone.utc))
    logger.info(f"Failed login attempt recorded for: {email}")


def clear_login_attempts(email: str):
    """Clear login attempts after successful login"""
    if email in login_attempts:
        login_attempts[email] = []


def sanitize_user_input(input_str: str) -> str:
    """Sanitize user input to prevent NoSQL injection and XSS"""
    if not input_str:
        return input_str
    
    # Remove potential MongoDB operators
    dangerous_patterns = [
        r'\$where', r'\$regex', r'\$gt', r'\$lt', r'\$gte', r'\$lte',
        r'\$ne', r'\$in', r'\$nin', r'\$exists', r'\$type', r'\$expr'
    ]
    
    sanitized = input_str
    for pattern in dangerous_patterns:
        sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
    
    # Remove script tags and other XSS vectors
    sanitized = re.sub(r'<script[^>]*>.*?</script>', '', sanitized, flags=re.IGNORECASE | re.DOTALL)
    sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r'on\w+\s*=', '', sanitized, flags=re.IGNORECASE)
    
    return sanitized.strip()


def audit_log_action(
    action: str,
    user_id: str,
    resource: str,
    details: dict,
    ip_address: str = None,
    success: bool = True
):
    """Log security-relevant actions for audit trail"""
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "user_id": user_id,
        "resource": resource,
        "details": details,
        "ip_address": ip_address,
        "success": success
    }
    
    if success:
        logger.info(f"AUDIT: {action} by {user_id} on {resource}", extra=log_entry)
    else:
        logger.warning(f"AUDIT FAILED: {action} by {user_id} on {resource}", extra=log_entry)
