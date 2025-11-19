from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from core.config import get_settings
import logging

logger = logging.getLogger(__name__)

class Database:
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    @classmethod
    def connect(cls):
        """Connect to MongoDB"""
        settings = get_settings()
        cls.client = AsyncIOMotorClient(settings.MONGO_URL)
        cls.db = cls.client[settings.DB_NAME]
        logger.info(f"Connected to MongoDB: {settings.DB_NAME}")

    @classmethod
    def close(cls):
        """Close MongoDB connection"""
        if cls.client:
            cls.client.close()
            logger.info("Closed MongoDB connection")

    @classmethod
    def get_db(cls) -> AsyncIOMotorDatabase:
        """Get database instance"""
        if cls.db is None:
            cls.connect()
        return cls.db

db_instance = Database()

def get_db() -> AsyncIOMotorDatabase:
    """Dependency for getting database"""
    return db_instance.get_db()
