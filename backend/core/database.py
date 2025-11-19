from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from core.config import get_settings
import logging

logger = logging.getLogger(__name__)

class Database:
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    @classmethod
    def connect(cls):
        """Connect to MongoDB with connection pooling for scalability"""
        settings = get_settings()
        
        # Configure connection pool for handling 10000+ users
        cls.client = AsyncIOMotorClient(
            settings.MONGO_URL,
            maxPoolSize=100,  # Maximum connections in pool
            minPoolSize=10,   # Minimum connections to maintain
            maxIdleTimeMS=50000,  # Close idle connections after 50s
            serverSelectionTimeoutMS=5000,  # Timeout for server selection
            connectTimeoutMS=10000,  # Timeout for initial connection
            socketTimeoutMS=20000,  # Timeout for socket operations
        )
        cls.db = cls.client[settings.DB_NAME]
        logger.info(f"Connected to MongoDB: {settings.DB_NAME} with connection pooling")

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
