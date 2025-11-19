"""
Database indexing for scalability and performance
"""
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging

logger = logging.getLogger(__name__)


async def create_indexes(db: AsyncIOMotorDatabase):
    """Create all necessary indexes for optimal performance with 10000+ users"""
    try:
        logger.info("Creating database indexes...")
        
        # Users collection
        await db.users.create_index("email", unique=True)
        await db.users.create_index("id", unique=True)
        await db.users.create_index("role")
        await db.users.create_index("current_plan")
        await db.users.create_index("is_active")
        await db.users.create_index([("created_at", -1)])
        logger.info("✓ Users indexes created")
        
        # Companies collection
        await db.companies.create_index("domain", unique=True)
        await db.companies.create_index("id", unique=True)
        await db.companies.create_index("linkedin_url")
        await db.companies.create_index("user_id")
        await db.companies.create_index([("last_crawled", -1)])
        await db.companies.create_index("confidence_score")
        await db.companies.create_index([("user_id", 1), ("last_crawled", -1)])
        logger.info("✓ Companies indexes created")
        
        # Transactions collection
        await db.transactions.create_index("id", unique=True)
        await db.transactions.create_index("user_id")
        await db.transactions.create_index("razorpay_order_id", unique=True)
        await db.transactions.create_index("razorpay_payment_id", unique=True, sparse=True)
        await db.transactions.create_index("status")
        await db.transactions.create_index([("created_at", -1)])
        await db.transactions.create_index([("user_id", 1), ("created_at", -1)])
        await db.transactions.create_index([("user_id", 1), ("status", 1), ("created_at", -1)])
        logger.info("✓ Transactions indexes created")
        
        # API Tokens collection
        await db.api_tokens.create_index("id", unique=True)
        await db.api_tokens.create_index("token", unique=True)
        await db.api_tokens.create_index("user_id")
        await db.api_tokens.create_index("is_active")
        await db.api_tokens.create_index([("created_at", -1)])
        await db.api_tokens.create_index([("user_id", 1), ("is_active", 1)])
        logger.info("✓ API Tokens indexes created")
        
        # Plans collection
        await db.plans.create_index("id", unique=True)
        await db.plans.create_index("name", unique=True)
        await db.plans.create_index("is_active")
        logger.info("✓ Plans indexes created")
        
        # Crawl Requests collection
        await db.crawl_requests.create_index("id", unique=True)
        await db.crawl_requests.create_index("user_id")
        await db.crawl_requests.create_index("status")
        await db.crawl_requests.create_index([("created_at", -1)])
        await db.crawl_requests.create_index([("user_id", 1), ("created_at", -1)])
        logger.info("✓ Crawl Requests indexes created")
        
        # Audit Logs collection
        await db.audit_logs.create_index("transaction_id")
        await db.audit_logs.create_index("user_id")
        await db.audit_logs.create_index("event_type")
        await db.audit_logs.create_index([("timestamp", -1)])
        await db.audit_logs.create_index([("user_id", 1), ("timestamp", -1)])
        await db.audit_logs.create_index("timestamp", expireAfterSeconds=7776000)
        logger.info("✓ Audit Logs indexes created")
        
        # Blogs collection
        await db.blogs.create_index("id", unique=True)
        await db.blogs.create_index("slug", unique=True)
        await db.blogs.create_index("is_published")
        await db.blogs.create_index([("created_at", -1)])
        await db.blogs.create_index([("title", "text"), ("content", "text")])
        logger.info("✓ Blogs indexes created")
        
        # FAQs collection
        await db.faqs.create_index("id", unique=True)
        await db.faqs.create_index("is_published")
        await db.faqs.create_index("order")
        await db.faqs.create_index([("question", "text"), ("answer", "text")])
        logger.info("✓ FAQs indexes created")
        
        # HubSpot Auth collection
        await db.hubspot_auth.create_index("user_id", unique=True)
        await db.hubspot_auth.create_index("expires_at")
        logger.info("✓ HubSpot Auth indexes created")
        
        # HubSpot Settings collection
        await db.hubspot_settings.create_index("user_id", unique=True)
        logger.info("✓ HubSpot Settings indexes created")
        
        logger.info("✅ All database indexes created successfully!")
        
    except Exception as e:
        logger.error(f"Error creating indexes: {str(e)}")
        raise
