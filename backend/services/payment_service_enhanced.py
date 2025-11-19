from motor.motor_asyncio import AsyncIOMotorDatabase
from models.payment import Transaction, Plan, OrderCreate, PaymentVerification, AuditLog
from core.config import get_settings
import razorpay
import logging
import hmac
import hashlib
from datetime import datetime, timezone, timedelta
from typing import List, Optional
from fastapi import HTTPException

logger = logging.getLogger(__name__)
settings = get_settings()

class PaymentService:
    """Enhanced payment service with fraud prevention and security"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.transactions = db.transactions
        self.plans = db.plans
        self.audit_logs = db.payment_audit_logs
        
        # Initialize Razorpay client
        if settings.RAZORPAY_KEY_ID and settings.RAZORPAY_KEY_SECRET:
            self.razorpay_client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
            )
        else:
            self.razorpay_client = None
            logger.warning("Razorpay credentials not configured")
    
    async def _log_audit_event(self, transaction_id: str, user_id: str, event_type: str, details: dict, ip_address: Optional[str] = None):
        """Log audit event for payment activities"""
        audit_log = AuditLog(
            transaction_id=transaction_id,
            user_id=user_id,
            event_type=event_type,
            details=details,
            ip_address=ip_address
        )
        audit_dict = audit_log.model_dump()
        audit_dict['timestamp'] = audit_dict['timestamp'].isoformat()
        await self.audit_logs.insert_one(audit_dict)
        logger.info(f"Audit: {event_type} for transaction {transaction_id}")
    
    async def _check_payment_rate_limit(self, user_id: str) -> bool:
        """Check if user has exceeded payment rate limit"""
        one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
        count = await self.transactions.count_documents({
            "user_id": user_id,
            "created_at": {"$gte": one_hour_ago.isoformat()}
        })
        return count < settings.PAYMENT_RATE_LIMIT_PER_HOUR
    
    async def _expire_old_transactions(self):
        """Expire transactions older than timeout"""
        expiry_time = datetime.now(timezone.utc) - timedelta(minutes=settings.TRANSACTION_TIMEOUT_MINUTES)
        
        result = await self.transactions.update_many(
            {
                "status": "pending",
                "created_at": {"$lt": expiry_time.isoformat()}
            },
            {"$set": {"status": "expired"}}
        )
        
        if result.modified_count > 0:
            logger.info(f"Expired {result.modified_count} old transactions")
    
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
    
    async def create_order(self, user_id: str, order_data: OrderCreate, ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> Transaction:
        """
        Create a Razorpay order with security checks
        """
        if not self.razorpay_client:
            raise HTTPException(status_code=503, detail="Payment system not configured")
        
        # Expire old transactions
        await self._expire_old_transactions()
        
        # Check rate limit
        if not await self._check_payment_rate_limit(user_id):
            await self._log_audit_event("rate_limit_exceeded", user_id, "rate_limit_exceeded", 
                                        {"amount": order_data.amount, "plan": order_data.plan_name}, ip_address)
            raise HTTPException(status_code=429, detail="Payment rate limit exceeded. Please try again later.")
        
        # Validate amount
        if order_data.amount <= 0:
            raise HTTPException(status_code=400, detail="Invalid payment amount")
        
        if order_data.amount > settings.MAX_PAYMENT_AMOUNT:
            raise HTTPException(status_code=400, detail=f"Payment amount exceeds maximum limit of ₹{settings.MAX_PAYMENT_AMOUNT}")
        
        # Validate credits
        if order_data.credits <= 0:
            raise HTTPException(status_code=400, detail="Invalid credits amount")
        
        try:
            # Create Razorpay order
            razorpay_order = self.razorpay_client.order.create({
                "amount": int(order_data.amount * 100),  # Amount in paise
                "currency": "INR",
                "payment_capture": 1,
                "notes": {
                    "user_id": user_id,
                    "plan_name": order_data.plan_name
                }
            })
            
            # Calculate expiry time
            expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.TRANSACTION_TIMEOUT_MINUTES)
            
            # Create transaction record
            transaction = Transaction(
                user_id=user_id,
                plan_name=order_data.plan_name,
                amount=order_data.amount,
                credits_purchased=order_data.credits,
                razorpay_order_id=razorpay_order['id'],
                status="pending",
                ip_address=ip_address,
                user_agent=user_agent,
                expires_at=expires_at
            )
            
            transaction_dict = transaction.model_dump()
            transaction_dict['created_at'] = transaction_dict['created_at'].isoformat()
            if transaction_dict.get('expires_at'):
                transaction_dict['expires_at'] = transaction_dict['expires_at'].isoformat()
            
            await self.transactions.insert_one(transaction_dict)
            
            # Log audit event
            await self._log_audit_event(
                transaction.id, user_id, "order_created",
                {
                    "amount": order_data.amount,
                    "credits": order_data.credits,
                    "plan": order_data.plan_name,
                    "razorpay_order_id": razorpay_order['id']
                },
                ip_address
            )
            
            logger.info(f"Created order for user {user_id}: {transaction.id}")
            return transaction
        
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error creating Razorpay order: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to create payment order")
    
    async def verify_payment(self, verification: PaymentVerification, user_id: str, ip_address: Optional[str] = None) -> bool:
        """
        Verify Razorpay payment with idempotency and fraud checks
        """
        if not self.razorpay_client:
            raise HTTPException(status_code=503, detail="Payment system not configured")
        
        # Get transaction
        transaction = await self.get_transaction(verification.transaction_id)
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        # Check if transaction belongs to user
        if transaction.user_id != user_id:
            await self._log_audit_event(
                verification.transaction_id, user_id, "unauthorized_verification_attempt",
                {"actual_user": transaction.user_id}, ip_address
            )
            raise HTTPException(status_code=403, detail="Unauthorized transaction access")
        
        # Check if already verified (idempotency)
        if transaction.status == "completed":
            if verification.idempotency_key and transaction.idempotency_key == verification.idempotency_key:
                logger.info(f"Idempotent verification request for {verification.transaction_id}")
                return True
            else:
                raise HTTPException(status_code=400, detail="Payment already verified")
        
        # Check if transaction expired
        if transaction.status == "expired":
            raise HTTPException(status_code=400, detail="Transaction has expired")
        
        # Check if transaction failed
        if transaction.status == "failed":
            raise HTTPException(status_code=400, detail="Transaction already failed")
        
        # Check expiry
        if transaction.expires_at and datetime.now(timezone.utc) > transaction.expires_at:
            await self.transactions.update_one(
                {"id": verification.transaction_id},
                {"$set": {"status": "expired"}}
            )
            raise HTTPException(status_code=400, detail="Transaction has expired")
        
        # Check verification attempts
        if transaction.verification_attempts >= settings.MAX_VERIFICATION_ATTEMPTS:
            await self._log_audit_event(
                verification.transaction_id, user_id, "max_verification_attempts",
                {"attempts": transaction.verification_attempts}, ip_address
            )
            raise HTTPException(status_code=400, detail="Maximum verification attempts exceeded")
        
        # Increment verification attempts
        await self.transactions.update_one(
            {"id": verification.transaction_id},
            {"$inc": {"verification_attempts": 1}}
        )
        
        try:
            # Verify signature
            params_dict = {
                'razorpay_order_id': verification.razorpay_order_id,
                'razorpay_payment_id': verification.razorpay_payment_id,
                'razorpay_signature': verification.razorpay_signature
            }
            
            self.razorpay_client.utility.verify_payment_signature(params_dict)
            
            # Fetch payment details from Razorpay for additional validation
            try:
                payment_details = self.razorpay_client.payment.fetch(verification.razorpay_payment_id)
                
                # Validate amount matches
                if payment_details.get('amount') != int(transaction.amount * 100):
                    await self._log_audit_event(
                        verification.transaction_id, user_id, "amount_mismatch",
                        {
                            "expected": transaction.amount,
                            "received": payment_details.get('amount', 0) / 100
                        },
                        ip_address
                    )
                    raise HTTPException(status_code=400, detail="Payment amount mismatch")
                
                # Validate payment status
                if payment_details.get('status') != 'captured' and payment_details.get('status') != 'authorized':
                    raise HTTPException(status_code=400, detail=f"Payment not successful: {payment_details.get('status')}")
                
            except Exception as e:
                logger.error(f"Error fetching payment details: {str(e)}")
                # Continue with verification if fetch fails (don't block valid payments)
            
            # Update transaction
            update_data = {
                "razorpay_payment_id": verification.razorpay_payment_id,
                "razorpay_signature": verification.razorpay_signature,
                "status": "completed",
                "is_verified": True,
                "completed_at": datetime.now(timezone.utc).isoformat()
            }
            
            if verification.idempotency_key:
                update_data["idempotency_key"] = verification.idempotency_key
            
            await self.transactions.update_one(
                {"id": verification.transaction_id},
                {"$set": update_data}
            )
            
            # Log success
            await self._log_audit_event(
                verification.transaction_id, user_id, "payment_verified",
                {
                    "amount": transaction.amount,
                    "credits": transaction.credits_purchased,
                    "razorpay_payment_id": verification.razorpay_payment_id
                },
                ip_address
            )
            
            logger.info(f"Payment verified for transaction {verification.transaction_id}")
            return True
        
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Payment verification failed: {str(e)}")
            
            # Update transaction status
            await self.transactions.update_one(
                {"id": verification.transaction_id},
                {"$set": {"status": "failed"}}
            )
            
            # Log failure
            await self._log_audit_event(
                verification.transaction_id, user_id, "payment_verification_failed",
                {"error": str(e)}, ip_address
            )
            
            raise HTTPException(status_code=400, detail="Payment verification failed")
    
    async def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        """Verify Razorpay webhook signature"""
        if not settings.RAZORPAY_WEBHOOK_SECRET:
            logger.warning("Webhook secret not configured")
            return False
        
        expected_signature = hmac.new(
            settings.RAZORPAY_WEBHOOK_SECRET.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(expected_signature, signature)
    
    async def handle_webhook(self, event_data: dict, ip_address: Optional[str] = None):
        """Handle Razorpay webhook events"""
        event = event_data.get('event')
        payload = event_data.get('payload', {})
        
        logger.info(f"Received webhook event: {event}")
        
        if event == "payment.captured":
            payment = payload.get('payment', {}).get('entity', {})
            order_id = payment.get('order_id')
            payment_id = payment.get('id')
            
            # Find transaction by order_id
            transaction = await self.transactions.find_one({"razorpay_order_id": order_id}, {"_id": 0})
            
            if transaction:
                # Update if not already completed
                if transaction.get('status') != 'completed':
                    await self.transactions.update_one(
                        {"id": transaction['id']},
                        {
                            "$set": {
                                "razorpay_payment_id": payment_id,
                                "status": "completed",
                                "completed_at": datetime.now(timezone.utc).isoformat()
                            }
                        }
                    )
                    
                    await self._log_audit_event(
                        transaction['id'], transaction['user_id'], "webhook_payment_captured",
                        {"payment_id": payment_id, "order_id": order_id}, ip_address
                    )
                    
                    logger.info(f"Payment captured via webhook: {payment_id}")
        
        elif event == "payment.failed":
            payment = payload.get('payment', {}).get('entity', {})
            order_id = payment.get('order_id')
            
            transaction = await self.transactions.find_one({"razorpay_order_id": order_id}, {"_id": 0})
            
            if transaction:
                await self.transactions.update_one(
                    {"id": transaction['id']},
                    {"$set": {"status": "failed"}}
                )
                
                await self._log_audit_event(
                    transaction['id'], transaction['user_id'], "webhook_payment_failed",
                    {"order_id": order_id, "error": payment.get('error_description')}, ip_address
                )
    
    async def get_transaction(self, transaction_id: str) -> Optional[Transaction]:
        """Get transaction by ID"""
        trans_dict = await self.transactions.find_one({"id": transaction_id}, {"_id": 0})
        if not trans_dict:
            return None
        
        # Convert timestamps
        for field in ['created_at', 'completed_at', 'expires_at']:
            if trans_dict.get(field) and isinstance(trans_dict[field], str):
                trans_dict[field] = datetime.fromisoformat(trans_dict[field])
        
        return Transaction(**trans_dict)
    
    async def get_user_transactions(self, user_id: str, limit: int = 50) -> List[Transaction]:
        """Get user's transaction history"""
        trans_list = await self.transactions.find(
            {"user_id": user_id},
            {"_id": 0}
        ).sort("created_at", -1).limit(limit).to_list(limit)
        
        transactions = []
        for trans_dict in trans_list:
            for field in ['created_at', 'completed_at', 'expires_at']:
                if trans_dict.get(field) and isinstance(trans_dict[field], str):
                    trans_dict[field] = datetime.fromisoformat(trans_dict[field])
            transactions.append(Transaction(**trans_dict))
        
        return transactions
    
    async def get_audit_logs(self, transaction_id: str) -> List[dict]:
        """Get audit logs for a transaction"""
        logs = await self.audit_logs.find(
            {"transaction_id": transaction_id},
            {"_id": 0}
        ).sort("timestamp", 1).to_list(100)
        
        return logs
