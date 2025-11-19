from pydantic import BaseModel, Field, ConfigDict, HttpUrl
from typing import Optional, List
from datetime import datetime, timezone
import uuid

class CompanyData(BaseModel):
    """Company information model"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Core identifiers
    company_name: Optional[str] = None
    domain: Optional[str] = None
    linkedin_url: Optional[str] = None
    
    # Company details
    industry: Optional[str] = None
    employee_size: Optional[str] = None
    founded_on: Optional[str] = None
    founders: Optional[List[str]] = None
    description: Optional[str] = None
    
    # Contact information
    address: Optional[str] = None
    phone_numbers: Optional[List[str]] = None
    emails: Optional[List[str]] = None
    country: Optional[str] = None
    location: Optional[str] = None
    
    # Social media
    twitter_url: Optional[str] = None
    facebook_url: Optional[str] = None
    
    # Additional data
    latest_news: Optional[List[dict]] = None
    website_urls: Optional[List[str]] = None
    
    # Confidence and metadata
    confidence_score: float = 0.0
    data_sources: List[str] = []
    last_crawled: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    crawled_by_user: Optional[str] = None

class CrawlRequest(BaseModel):
    """Single crawl request"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    
    # Input
    input_type: str  # 'company_name', 'domain', 'linkedin_url'
    input_value: str
    
    # Status
    status: str = "pending"  # pending, processing, completed, failed
    result: Optional[CompanyData] = None
    error: Optional[str] = None
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None

class BulkCrawlJob(BaseModel):
    """Bulk crawl job"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    
    total_requests: int
    completed_requests: int = 0
    failed_requests: int = 0
    
    status: str = "pending"  # pending, processing, completed, failed
    
    # File tracking
    input_filename: str
    output_filename: Optional[str] = None
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None

class CrawlRequestCreate(BaseModel):
    input_type: str
    input_value: str

class BulkCrawlRequest(BaseModel):
    requests: List[CrawlRequestCreate]
