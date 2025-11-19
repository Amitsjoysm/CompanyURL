from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from core.database import get_db
from core.auth import get_current_user
from models.api_token import APIToken, APITokenCreate, APITokenResponse, APITokenListItem
from typing import List
from datetime import datetime, timedelta, timezone

router = APIRouter(prefix="/api-tokens", tags=["API Tokens"])

@router.post("/", response_model=APITokenResponse)
async def create_api_token(
    token_data: APITokenCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Create a new API token for programmatic access"""
    user_id = current_user['sub']
    
    # Calculate expiration
    expires_at = None
    if token_data.expires_in_days:
        expires_at = datetime.now(timezone.utc) + timedelta(days=token_data.expires_in_days)
    
    # Create token
    api_token = APIToken(
        user_id=user_id,
        name=token_data.name,
        scopes=token_data.scopes,
        expires_at=expires_at
    )
    
    await db.api_tokens.insert_one(api_token.dict())
    
    # Return full token (only time it's shown)
    return APITokenResponse(**api_token.dict())

@router.get("/", response_model=List[APITokenListItem])
async def list_api_tokens(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """List all API tokens for current user"""
    user_id = current_user['sub']
    
    tokens = await db.api_tokens.find({"user_id": user_id}).to_list(100)
    
    # Return without full token value
    result = []
    for token in tokens:
        token_preview = f"...{token['token'][-4:]}"
        result.append(APITokenListItem(
            **{**token, "token_preview": token_preview}
        ))
    
    return result

@router.delete("/{token_id}")
async def revoke_api_token(
    token_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Revoke an API token"""
    user_id = current_user['sub']
    
    # Verify ownership
    token = await db.api_tokens.find_one({"id": token_id, "user_id": user_id})
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
    
    # Delete token
    await db.api_tokens.delete_one({"id": token_id})
    
    return {"message": "Token revoked successfully"}

@router.put("/{token_id}/toggle")
async def toggle_api_token(
    token_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Enable/disable an API token"""
    user_id = current_user['sub']
    
    # Verify ownership
    token = await db.api_tokens.find_one({"id": token_id, "user_id": user_id})
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
    
    # Toggle active status
    new_status = not token['is_active']
    await db.api_tokens.update_one(
        {"id": token_id},
        {"$set": {"is_active": new_status}}
    )
    
    return {"message": f"Token {'enabled' if new_status else 'disabled'}", "is_active": new_status}
