from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from core.database import get_db
from core.auth import get_current_user, require_superadmin
from models.user import User, UserResponse
from models.payment import Plan
from typing import List
from pydantic import BaseModel

router = APIRouter(prefix="/admin", tags=["Admin"])

# User management models
class UserCreditsUpdate(BaseModel):
    credits: int

class UserStatusUpdate(BaseModel):
    is_active: bool

class UserPlanUpdate(BaseModel):
    current_plan: str  # Free, Starter, Pro, Enterprise

# Plan management models
class PlanCreate(BaseModel):
    name: str
    price: float
    credits: int
    is_active: bool = True

class PlanUpdate(BaseModel):
    name: str = None
    price: float = None
    credits: int = None
    is_active: bool = None

@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    current_user: dict = Depends(require_superadmin),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get all users (superadmin only)"""
    users = await db.users.find({}).to_list(1000)
    return users

@router.put("/users/{user_id}/credits")
async def update_user_credits(
    user_id: str,
    update_data: UserCreditsUpdate,
    current_user: dict = Depends(require_superadmin),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Update user credits (superadmin only)"""
    result = await db.users.update_one(
        {"id": user_id},
        {"$set": {"credits": update_data.credits}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "Credits updated successfully"}

@router.put("/users/{user_id}/status")
async def update_user_status(
    user_id: str,
    update_data: UserStatusUpdate,
    current_user: dict = Depends(require_superadmin),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Activate/deactivate user (superadmin only)"""
    result = await db.users.update_one(
        {"id": user_id},
        {"$set": {"is_active": update_data.is_active}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User status updated successfully"}

@router.put("/users/{user_id}/plan")
async def update_user_plan(
    user_id: str,
    update_data: UserPlanUpdate,
    current_user: dict = Depends(require_superadmin),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Update user plan (superadmin only)"""
    if update_data.current_plan not in ["Free", "Starter", "Pro", "Enterprise"]:
        raise HTTPException(status_code=400, detail="Invalid plan name")
    
    result = await db.users.update_one(
        {"id": user_id},
        {"$set": {"current_plan": update_data.current_plan}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User plan updated successfully"}

@router.post("/plans", response_model=Plan)
async def create_plan(
    plan_data: PlanCreate,
    current_user: dict = Depends(require_superadmin),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Create a new pricing plan (superadmin only)"""
    plan = Plan(**plan_data.dict())
    await db.plans.insert_one(plan.dict())
    return plan

@router.put("/plans/{plan_id}", response_model=Plan)
async def update_plan(
    plan_id: str,
    plan_data: PlanUpdate,
    current_user: dict = Depends(require_superadmin),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Update a pricing plan (superadmin only)"""
    update_dict = {k: v for k, v in plan_data.dict().items() if v is not None}
    
    if not update_dict:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    result = await db.plans.update_one(
        {"id": plan_id},
        {"$set": update_dict}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    plan = await db.plans.find_one({"id": plan_id})
    return plan

@router.delete("/plans/{plan_id}")
async def delete_plan(
    plan_id: str,
    current_user: dict = Depends(require_superadmin),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Delete a pricing plan (superadmin only)"""
    result = await db.plans.delete_one({"id": plan_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    return {"message": "Plan deleted successfully"}

@router.get("/central-ledger")
async def get_central_ledger(
    limit: int = 100,
    current_user: dict = Depends(require_superadmin),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get all companies from central ledger (superadmin only)"""
    companies = await db.companies.find({}).sort("last_crawled", -1).limit(limit).to_list(limit)
    return companies
