from motor.motor_asyncio import AsyncIOMotorDatabase
from models.user import User, UserCreate, UserLogin
from core.auth import get_password_hash, verify_password, create_access_token
from typing import Optional
import logging
from fastapi import HTTPException, status
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class UserService:
    """User service for authentication and user management"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.users
    
    async def create_user(self, user_data: UserCreate) -> User:
        """
        Create a new user
        """
        # Check if user exists
        existing_user = await self.collection.find_one({"email": user_data.email})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create user with default role
        hashed_password = get_password_hash(user_data.password)
        user = User(
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hashed_password,
            role="user"  # Default role for new registrations
        )
        
        # Store user
        user_dict = user.model_dump()
        user_dict['created_at'] = user_dict['created_at'].isoformat()
        
        await self.collection.insert_one(user_dict)
        
        logger.info(f"Created user: {user.email}")
        return user
    
    async def authenticate_user(self, credentials: UserLogin) -> tuple[User, str]:
        """
        Authenticate user and return user + token
        """
        # Find user
        user_dict = await self.collection.find_one({"email": credentials.email})
        if not user_dict:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Verify password
        if not verify_password(credentials.password, user_dict['hashed_password']):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Check if active
        if not user_dict.get('is_active', True):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive"
            )
        
        # Convert to User model
        if isinstance(user_dict['created_at'], str):
            user_dict['created_at'] = datetime.fromisoformat(user_dict['created_at'])
        
        user = User(**{k: v for k, v in user_dict.items() if k != '_id'})
        
        # Create token
        token = create_access_token(
            data={"sub": user.id, "email": user.email, "role": user.role}
        )
        
        logger.info(f"User authenticated: {user.email}")
        return user, token
    
    async def get_user(self, user_id: str) -> Optional[User]:
        """
        Get user by ID
        """
        user_dict = await self.collection.find_one({"id": user_id}, {"_id": 0, "hashed_password": 0})
        if not user_dict:
            return None
        
        if isinstance(user_dict['created_at'], str):
            user_dict['created_at'] = datetime.fromisoformat(user_dict['created_at'])
        
        return User(**user_dict)
    
    async def update_credits(self, user_id: str, credits_delta: int) -> bool:
        """
        Update user credits (positive or negative delta)
        """
        result = await self.collection.update_one(
            {"id": user_id},
            {"$inc": {"credits": credits_delta}}
        )
        return result.modified_count > 0
    
    async def get_user_credits(self, user_id: str) -> int:
        """
        Get user's current credits
        """
        user = await self.get_user(user_id)
        return user.credits if user else 0
