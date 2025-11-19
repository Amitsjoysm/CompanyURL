from fastapi import APIRouter, Depends, HTTPException
from models.content import Blog, BlogCreate, BlogUpdate, FAQ, FAQCreate, FAQUpdate
from services.content_service import ContentService
from core.database import get_db
from core.auth import get_current_superadmin
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List

router = APIRouter(prefix="/content", tags=["Content"])

# Public endpoints
@router.get("/blogs", response_model=List[Blog])
async def get_all_blogs(db: AsyncIOMotorDatabase = Depends(get_db)):
    """Get all published blogs"""
    content_service = ContentService(db)
    return await content_service.get_all_blogs(published_only=True)

@router.get("/blogs/{slug}", response_model=Blog)
async def get_blog(slug: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    """Get blog by slug"""
    content_service = ContentService(db)
    blog = await content_service.get_blog(slug)
    
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    return blog

@router.get("/faqs", response_model=List[FAQ])
async def get_all_faqs(db: AsyncIOMotorDatabase = Depends(get_db)):
    """Get all published FAQs"""
    content_service = ContentService(db)
    return await content_service.get_all_faqs(published_only=True)

# Admin endpoints
@router.post("/blogs", response_model=Blog)
async def create_blog(
    blog_data: BlogCreate,
    current_user: dict = Depends(get_current_superadmin),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Create a new blog (Admin only)"""
    content_service = ContentService(db)
    return await content_service.create_blog(blog_data)

@router.put("/blogs/{slug}", response_model=Blog)
async def update_blog(
    slug: str,
    blog_data: BlogUpdate,
    current_user: dict = Depends(get_current_superadmin),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Update blog (Admin only)"""
    content_service = ContentService(db)
    blog = await content_service.update_blog(slug, blog_data)
    
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    return blog

@router.delete("/blogs/{slug}")
async def delete_blog(
    slug: str,
    current_user: dict = Depends(get_current_superadmin),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Delete blog (Admin only)"""
    content_service = ContentService(db)
    success = await content_service.delete_blog(slug)
    
    if not success:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    return {"message": "Blog deleted successfully"}

@router.post("/faqs", response_model=FAQ)
async def create_faq(
    faq_data: FAQCreate,
    current_user: dict = Depends(get_current_superadmin),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Create a new FAQ (Admin only)"""
    content_service = ContentService(db)
    return await content_service.create_faq(faq_data)

@router.put("/faqs/{faq_id}", response_model=FAQ)
async def update_faq(
    faq_id: str,
    faq_data: FAQUpdate,
    current_user: dict = Depends(get_current_superadmin),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Update FAQ (Admin only)"""
    content_service = ContentService(db)
    faq = await content_service.update_faq(faq_id, faq_data)
    
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")
    
    return faq

@router.delete("/faqs/{faq_id}")
async def delete_faq(
    faq_id: str,
    current_user: dict = Depends(get_current_superadmin),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Delete FAQ (Admin only)"""
    content_service = ContentService(db)
    success = await content_service.delete_faq(faq_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="FAQ not found")
    
    return {"message": "FAQ deleted successfully"}
