from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal
from datetime import datetime, timezone
import uuid

class Plan(BaseModel):
    """Pricing plan model"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    price: float
    credits: int
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Transaction(BaseModel):
    """Payment transaction model"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    
    # Payment details
    plan_name: str
    amount: float
    credits_purchased: int
    
    # Razorpay details
    razorpay_order_id: Optional[str] = None
    razorpay_payment_id: Optional[str] = None
    razorpay_signature: Optional[str] = None
    
    status: Literal["pending", "completed", "failed", "expired"] = "pending"
    
    # Security and fraud prevention
    idempotency_key: Optional[str] = None  # Prevent duplicate verifications
    ip_address: Optional[str] = None  # Track payment source
    user_agent: Optional[str] = None  # Track device info
    is_verified: bool = False  # Additional verification flag
    verification_attempts: int = 0  # Track verification attempts
    expires_at: Optional[datetime] = None  # Order expiry time
    
    # Audit trail
    notes: Optional[str] = None
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None

class OrderCreate(BaseModel):
    plan_name: str
    amount: float
    credits: int

class PaymentVerification(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
    transaction_id: str
