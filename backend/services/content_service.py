from motor.motor_asyncio import AsyncIOMotorDatabase
from models.content import Blog, BlogCreate, BlogUpdate, FAQ, FAQCreate, FAQUpdate
from typing import List, Optional
import logging
from datetime import datetime, timezone
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)

class ContentService:
    """Service for managing blogs and FAQs"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.blogs = db.blogs
        self.faqs = db.faqs
    
    # Blog methods
    async def create_blog(self, blog_data: BlogCreate) -> Blog:
        """
        Create a new blog post
        """
        # Check if slug exists
        existing = await self.blogs.find_one({"slug": blog_data.slug})
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Blog with this slug already exists"
            )
        
        blog = Blog(**blog_data.model_dump())
        blog_dict = blog.model_dump()
        blog_dict['created_at'] = blog_dict['created_at'].isoformat()
        blog_dict['updated_at'] = blog_dict['updated_at'].isoformat()
        
        await self.blogs.insert_one(blog_dict)
        
        logger.info(f"Created blog: {blog.slug}")
        return blog
    
    async def get_blog(self, slug: str) -> Optional[Blog]:
        """
        Get blog by slug
        """
        blog_dict = await self.blogs.find_one({"slug": slug}, {"_id": 0})
        if not blog_dict:
            return None
        
        for field in ['created_at', 'updated_at']:
            if isinstance(blog_dict[field], str):
                blog_dict[field] = datetime.fromisoformat(blog_dict[field])
        
        return Blog(**blog_dict)
    
    async def get_all_blogs(self, published_only: bool = True) -> List[Blog]:
        """
        Get all blogs
        """
        query = {"is_published": True} if published_only else {}
        blogs_list = await self.blogs.find(query, {"_id": 0}).sort("created_at", -1).to_list(100)
        
        result = []
        for blog in blogs_list:
            for field in ['created_at', 'updated_at']:
                if isinstance(blog[field], str):
                    blog[field] = datetime.fromisoformat(blog[field])
            result.append(Blog(**blog))
        
        return result
    
    async def update_blog(self, slug: str, blog_data: BlogUpdate) -> Optional[Blog]:
        """
        Update blog
        """
        update_data = {k: v for k, v in blog_data.model_dump().items() if v is not None}
        if not update_data:
            return await self.get_blog(slug)
        
        update_data['updated_at'] = datetime.now(timezone.utc).isoformat()
        
        result = await self.blogs.update_one(
            {"slug": slug},
            {"$set": update_data}
        )
        
        if result.modified_count > 0:
            return await self.get_blog(slug)
        return None
    
    async def delete_blog(self, slug: str) -> bool:
        """
        Delete blog
        """
        result = await self.blogs.delete_one({"slug": slug})
        return result.deleted_count > 0
    
    # FAQ methods
    async def create_faq(self, faq_data: FAQCreate) -> FAQ:
        """
        Create a new FAQ
        """
        faq = FAQ(**faq_data.model_dump())
        faq_dict = faq.model_dump()
        faq_dict['created_at'] = faq_dict['created_at'].isoformat()
        faq_dict['updated_at'] = faq_dict['updated_at'].isoformat()
        
        await self.faqs.insert_one(faq_dict)
        
        logger.info(f"Created FAQ: {faq.id}")
        return faq
    
    async def get_faq(self, faq_id: str) -> Optional[FAQ]:
        """
        Get FAQ by ID
        """
        faq_dict = await self.faqs.find_one({"id": faq_id}, {"_id": 0})
        if not faq_dict:
            return None
        
        for field in ['created_at', 'updated_at']:
            if isinstance(faq_dict[field], str):
                faq_dict[field] = datetime.fromisoformat(faq_dict[field])
        
        return FAQ(**faq_dict)
    
    async def get_all_faqs(self, published_only: bool = True) -> List[FAQ]:
        """
        Get all FAQs
        """
        query = {"is_published": True} if published_only else {}
        faqs_list = await self.faqs.find(query, {"_id": 0}).sort("order", 1).to_list(100)
        
        result = []
        for faq in faqs_list:
            for field in ['created_at', 'updated_at']:
                if isinstance(faq[field], str):
                    faq[field] = datetime.fromisoformat(faq[field])
            result.append(FAQ(**faq))
        
        return result
    
    async def update_faq(self, faq_id: str, faq_data: FAQUpdate) -> Optional[FAQ]:
        """
        Update FAQ
        """
        update_data = {k: v for k, v in faq_data.model_dump().items() if v is not None}
        if not update_data:
            return await self.get_faq(faq_id)
        
        update_data['updated_at'] = datetime.now(timezone.utc).isoformat()
        
        result = await self.faqs.update_one(
            {"id": faq_id},
            {"$set": update_data}
        )
        
        if result.modified_count > 0:
            return await self.get_faq(faq_id)
        return None
    
    async def delete_faq(self, faq_id: str) -> bool:
        """
        Delete FAQ
        """
        result = await self.faqs.delete_one({"id": faq_id})
        return result.deleted_count > 0
