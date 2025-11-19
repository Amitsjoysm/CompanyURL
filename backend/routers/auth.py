from fastapi import APIRouter, Depends, HTTPException
from models.user import UserCreate, UserLogin, TokenResponse, UserResponse
from services.user_service import UserService
from core.database import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    """Register a new user"""
    user_service = UserService(db)
    user = await user_service.create_user(user_data)
    user, token = await user_service.authenticate_user(UserLogin(email=user.email, password=user_data.password))
    
    return TokenResponse(
        access_token=token,
        user=UserResponse(**user.model_dump())
    )

@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: AsyncIOMotorDatabase = Depends(get_db)):
    """Login user"""
    user_service = UserService(db)
    user, token = await user_service.authenticate_user(credentials)
    
    return TokenResponse(
        access_token=token,
        user=UserResponse(**user.model_dump())
    )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: dict = Depends(lambda: {}),  # Will be replaced with actual auth
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get current user information"""
    if not current_user.get('sub'):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    user_service = UserService(db)
    user = await user_service.get_user(current_user['sub'])
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(**user.model_dump())
