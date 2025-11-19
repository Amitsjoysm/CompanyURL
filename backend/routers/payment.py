from fastapi import APIRouter, Depends, HTTPException
from models.payment import Plan, OrderCreate, Transaction, PaymentVerification
from services.payment_service import PaymentService
from services.user_service import UserService
from core.database import get_db
from core.auth import get_current_user
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List

router = APIRouter(prefix="/payment", tags=["Payment"])

@router.get("/plans", response_model=List[Plan])
async def get_plans(db: AsyncIOMotorDatabase = Depends(get_db)):
    """Get all available pricing plans"""
    payment_service = PaymentService(db)
    return await payment_service.get_plans()

@router.post("/create-order", response_model=Transaction)
async def create_order(
    order_data: OrderCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Create a payment order"""
    payment_service = PaymentService(db)
    return await payment_service.create_order(current_user['sub'], order_data)

@router.post("/verify")
async def verify_payment(
    verification: PaymentVerification,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Verify payment and credit user account"""
    payment_service = PaymentService(db)
    user_service = UserService(db)
    
    # Verify payment
    success = await payment_service.verify_payment(verification)
    
    if not success:
        raise HTTPException(status_code=400, detail="Payment verification failed")
    
    # Get transaction details
    transaction = await payment_service.get_transaction(verification.transaction_id)
    
    if transaction:
        # Credit user account
        await user_service.update_credits(current_user['sub'], transaction.credits_purchased)
    
    return {"message": "Payment verified and credits added", "success": True}

@router.get("/razorpay-key")
async def get_razorpay_key():
    """Get Razorpay public key for frontend"""
    from core.config import get_settings
    settings = get_settings()
    return {"key": settings.RAZORPAY_KEY_ID}
