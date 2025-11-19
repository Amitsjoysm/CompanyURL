from fastapi import APIRouter, Depends, HTTPException, Request
from models.user import UserCreate, UserLogin, TokenResponse, UserResponse
from services.user_service import UserService
from core.database import get_db
from core.auth import get_current_user
from core.security import (
    validate_password_strength,
    check_login_attempts,
    record_failed_login,
    clear_login_attempts,
    audit_log_action
)
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=TokenResponse)
async def register(
    user_data: UserCreate,
    request: Request,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Register a new user with password strength validation"""
    # Validate password strength
    is_strong, message = validate_password_strength(user_data.password)
    if not is_strong:
        raise HTTPException(status_code=400, detail=message)
    
    # Get client IP for audit logging
    client_ip = request.client.host if request.client else "unknown"
    
    try:
        user_service = UserService(db)
        user = await user_service.create_user(user_data)
        user, token = await user_service.authenticate_user(
            UserLogin(email=user.email, password=user_data.password)
        )
        
        # Audit log
        audit_log_action(
            action="register",
            user_id=user.id,
            resource="user",
            details={"email": user.email},
            ip_address=client_ip,
            success=True
        )
        
        return TokenResponse(
            access_token=token,
            user=UserResponse(**user.model_dump())
        )
    except Exception as e:
        audit_log_action(
            action="register",
            user_id="unknown",
            resource="user",
            details={"email": user_data.email, "error": str(e)},
            ip_address=client_ip,
            success=False
        )
        raise

@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: UserLogin,
    request: Request,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Login user with account lockout protection"""
    # Get client IP
    client_ip = request.client.host if request.client else "unknown"
    
    # Check if account is locked due to too many failed attempts
    if check_login_attempts(credentials.email):
        logger.warning(f"Login blocked for {credentials.email} - too many failed attempts from {client_ip}")
        raise HTTPException(
            status_code=429,
            detail="Too many failed login attempts. Please try again in 15 minutes."
        )
    
    try:
        user_service = UserService(db)
        user, token = await user_service.authenticate_user(credentials)
        
        # Clear failed login attempts on successful login
        clear_login_attempts(credentials.email)
        
        # Audit log
        audit_log_action(
            action="login",
            user_id=user.id,
            resource="user",
            details={"email": user.email},
            ip_address=client_ip,
            success=True
        )
        
        return TokenResponse(
            access_token=token,
            user=UserResponse(**user.model_dump())
        )
    except HTTPException as e:
        # Record failed login attempt
        record_failed_login(credentials.email)
        
        # Audit log
        audit_log_action(
            action="login",
            user_id="unknown",
            resource="user",
            details={"email": credentials.email, "error": str(e.detail)},
            ip_address=client_ip,
            success=False
        )
        raise

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get current user information"""
    user_service = UserService(db)
    user = await user_service.get_user(current_user['sub'])
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(**user.model_dump())
