from motor.motor_asyncio import AsyncIOMotorDatabase
from models.payment import Transaction, Plan, OrderCreate, PaymentVerification
from core.config import get_settings
import razorpay
import logging
from datetime import datetime, timezone
from typing import List, Optional

logger = logging.getLogger(__name__)
settings = get_settings()

class PaymentService:
    """Payment service for handling Razorpay transactions"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.transactions = db.transactions
        self.plans = db.plans
        
        # Initialize Razorpay client
        if settings.RAZORPAY_KEY_ID and settings.RAZORPAY_KEY_SECRET:
            self.razorpay_client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
            )
        else:
            self.razorpay_client = None
            logger.warning("Razorpay credentials not configured")
    
    async def initialize_plans(self):
        """Initialize default pricing plans"""
        plans = [
            Plan(name="Free", price=0.0, credits=settings.FREE_PLAN_CREDITS),
            Plan(name="Starter", price=settings.STARTER_PLAN_PRICE, credits=settings.STARTER_PLAN_CREDITS),
            Plan(name="Pro", price=settings.PRO_PLAN_PRICE, credits=settings.PRO_PLAN_CREDITS)
        ]
        
        for plan in plans:
            existing = await self.plans.find_one({"name": plan.name})
            if not existing:
                plan_dict = plan.model_dump()
                plan_dict['created_at'] = plan_dict['created_at'].isoformat()
                await self.plans.insert_one(plan_dict)
    
    async def get_plans(self) -> List[Plan]:
        """Get all active plans"""
        plans_list = await self.plans.find({"is_active": True}, {"_id": 0}).to_list(100)
        return [Plan(**{**p, 'created_at': datetime.fromisoformat(p['created_at']) if isinstance(p['created_at'], str) else p['created_at']}) for p in plans_list]
    
    async def create_order(self, user_id: str, order_data: OrderCreate) -> Transaction:
        """
        Create a Razorpay order and transaction record
        """
        if not self.razorpay_client:
            raise Exception("Payment system not configured")
        
        # Create Razorpay order
        try:
            razorpay_order = self.razorpay_client.order.create({
                "amount": int(order_data.amount * 100),  # Amount in paise
                "currency": "INR",
                "payment_capture": 1
            })
            
            # Create transaction record
            transaction = Transaction(
                user_id=user_id,
                plan_name=order_data.plan_name,
                amount=order_data.amount,
                credits_purchased=order_data.credits,
                razorpay_order_id=razorpay_order['id'],
                status="pending"
            )
            
            transaction_dict = transaction.model_dump()
            transaction_dict['created_at'] = transaction_dict['created_at'].isoformat()
            
            await self.transactions.insert_one(transaction_dict)
            
            logger.info(f"Created order for user {user_id}: {transaction.id}")
            return transaction
        
        except Exception as e:
            logger.error(f"Error creating Razorpay order: {str(e)}")
            raise
    
    async def verify_payment(self, verification: PaymentVerification) -> bool:
        """
        Verify Razorpay payment and update transaction
        """
        if not self.razorpay_client:
            raise Exception("Payment system not configured")
        
        try:
            # Verify signature
            params_dict = {
                'razorpay_order_id': verification.razorpay_order_id,
                'razorpay_payment_id': verification.razorpay_payment_id,
                'razorpay_signature': verification.razorpay_signature
            }
            
            self.razorpay_client.utility.verify_payment_signature(params_dict)
            
            # Update transaction
            await self.transactions.update_one(
                {"id": verification.transaction_id},
                {
                    "$set": {
                        "razorpay_payment_id": verification.razorpay_payment_id,
                        "razorpay_signature": verification.razorpay_signature,
                        "status": "completed",
                        "completed_at": datetime.now(timezone.utc).isoformat()
                    }
                }
            )
            
            logger.info(f"Payment verified for transaction {verification.transaction_id}")
            return True
        
        except Exception as e:
            logger.error(f"Payment verification failed: {str(e)}")
            await self.transactions.update_one(
                {"id": verification.transaction_id},
                {"$set": {"status": "failed"}}
            )
            return False
    
    async def get_transaction(self, transaction_id: str) -> Optional[Transaction]:
        """Get transaction by ID"""
        trans_dict = await self.transactions.find_one({"id": transaction_id}, {"_id": 0})
        if not trans_dict:
            return None
        
        # Convert timestamps
        for field in ['created_at', 'completed_at']:
            if trans_dict.get(field) and isinstance(trans_dict[field], str):
                trans_dict[field] = datetime.fromisoformat(trans_dict[field])
        
        return Transaction(**trans_dict)
