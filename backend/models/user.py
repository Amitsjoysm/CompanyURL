from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime, timezone
import uuid

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    full_name: str
    hashed_password: str
    role: str = "user"  # user or superadmin
    is_active: bool = True
    credits: int = 10  # Free tier starts with 10 credits
    current_plan: str = "Free"  # Free, Starter, Pro, Enterprise
    preferred_currency: str = "USD"  # USD or INR
    country_code: Optional[str] = None  # Detected country code
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_login: Optional[datetime] = None

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    role: str
    is_active: bool
    credits: int
    current_plan: str
    preferred_currency: str = "USD"
    country_code: Optional[str] = None
    created_at: datetime
    last_login: Optional[datetime] = None

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    preferred_currency: Optional[str] = None

class PasswordChange(BaseModel):
    current_password: str
    new_password: str
