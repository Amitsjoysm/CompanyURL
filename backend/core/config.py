from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

class Settings(BaseSettings):
    # Database
    MONGO_URL: str = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    DB_NAME: str = os.environ.get('DB_NAME', 'corpinfo_db')
    
    # Security
    SECRET_KEY: str = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Groq API
    GROQ_API_KEY: str = os.environ.get('GROQ_API_KEY', '')
    
    # Razorpay
    RAZORPAY_KEY_ID: str = os.environ.get('RAZORPAY_KEY_ID', '')
    RAZORPAY_KEY_SECRET: str = os.environ.get('RAZORPAY_KEY_SECRET', '')
    RAZORPAY_WEBHOOK_SECRET: str = os.environ.get('RAZORPAY_WEBHOOK_SECRET', '')
    
    # CORS
    CORS_ORIGINS: str = os.environ.get('CORS_ORIGINS', '*')
    
    # Credits Config
    FREE_PLAN_CREDITS: int = 10
    STARTER_PLAN_PRICE: float = 25.0
    STARTER_PLAN_CREDITS: int = 1000
    PRO_PLAN_PRICE: float = 49.0
    PRO_PLAN_CREDITS: int = 2500
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Payment Security
    TRANSACTION_TIMEOUT_MINUTES: int = 30  # Order expires after 30 minutes
    MAX_VERIFICATION_ATTEMPTS: int = 3  # Max attempts to verify a payment
    MAX_PAYMENT_AMOUNT: float = 100000.0  # Maximum single payment amount
    PAYMENT_RATE_LIMIT_PER_HOUR: int = 10  # Max payment attempts per user per hour
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
