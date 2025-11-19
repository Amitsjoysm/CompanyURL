from fastapi import APIRouter, Depends, HTTPException, Request
from models.payment import Plan, OrderCreate, Transaction, PaymentVerification, WebhookEvent
from services.payment_service import PaymentService
from services.user_service import UserService
from core.database import get_db
from core.auth import get_current_user
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
import json
import uuid

router = APIRouter(prefix="/payment", tags=["Payment"])

@router.get("/plans", response_model=List[Plan])
async def get_plans(db: AsyncIOMotorDatabase = Depends(get_db)):
    """Get all available pricing plans"""
    payment_service = PaymentService(db)
    return await payment_service.get_plans()

@router.post("/create-order", response_model=Transaction)
async def create_order(
    order_data: OrderCreate,
    request: Request,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Create a payment order with security checks"""
    payment_service = PaymentService(db)
    
    # Get client info for security
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get('user-agent')
    
    return await payment_service.create_order(
        current_user['sub'], 
        order_data,
        ip_address=ip_address,
        user_agent=user_agent
    )

@router.post("/verify")
async def verify_payment(
    verification: PaymentVerification,
    request: Request,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Verify payment and credit user account with fraud prevention"""
    payment_service = PaymentService(db)
    user_service = UserService(db)
    
    # Get client IP for audit
    ip_address = request.client.host if request.client else None
    
    # Generate idempotency key if not provided
    if not verification.idempotency_key:
        verification.idempotency_key = str(uuid.uuid4())
    
    # Verify payment (includes all security checks)
    success = await payment_service.verify_payment(
        verification, 
        current_user['sub'],
        ip_address=ip_address
    )
    
    if not success:
        raise HTTPException(status_code=400, detail="Payment verification failed")
    
    # Get transaction details
    transaction = await payment_service.get_transaction(verification.transaction_id)
    
    if transaction and transaction.is_verified:
        # Credit user account (only if verified)
        await user_service.update_credits(current_user['sub'], transaction.credits_purchased)
    
    return {"message": "Payment verified and credits added", "success": True}

@router.get("/razorpay-key")
async def get_razorpay_key():
    """Get Razorpay public key for frontend"""
    from core.config import get_settings
    settings = get_settings()
    return {"key": settings.RAZORPAY_KEY_ID}
