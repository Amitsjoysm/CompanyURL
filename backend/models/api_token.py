from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime, timezone
import uuid
import secrets

class APIToken(BaseModel):
    """API Token for programmatic access"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    name: str  # User-friendly name for the token
    token: str = Field(default_factory=lambda: f"corp_{secrets.token_urlsafe(32)}")
    
    # Permissions
    scopes: list[str] = ["crawl:read", "crawl:write"]  # Default scopes
    
    # Status
    is_active: bool = True
    last_used: Optional[datetime] = None
    
    # Metadata
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: Optional[datetime] = None

class APITokenCreate(BaseModel):
    name: str
    scopes: list[str] = ["crawl:read", "crawl:write"]
    expires_in_days: Optional[int] = None  # None = no expiration

class APITokenResponse(BaseModel):
    id: str
    name: str
    token: str  # Only shown once during creation
    scopes: list[str]
    is_active: bool
    created_at: datetime
    expires_at: Optional[datetime]

class APITokenListItem(BaseModel):
    """Token info without the actual token value"""
    id: str
    name: str
    token_preview: str  # Last 4 chars only
    scopes: list[str]
    is_active: bool
    last_used: Optional[datetime]
    created_at: datetime
    expires_at: Optional[datetime]
