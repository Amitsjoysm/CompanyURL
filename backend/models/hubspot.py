from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime, timezone
import uuid

class HubSpotAuth(BaseModel):
    """HubSpot OAuth credentials storage"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    access_token: str
    refresh_token: str
    expires_at: datetime
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class HubSpotSettings(BaseModel):
    """User's HubSpot sync settings"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    auto_sync_enabled: bool = False
    sync_companies: bool = True
    sync_contacts: bool = True
    last_sync_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class HubSpotCompanySync(BaseModel):
    """Company data for HubSpot sync"""
    name: str
    domain: str
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    industry: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    employee_size: Optional[str] = None
    founded_date: Optional[str] = None
    description: Optional[str] = None

class HubSpotContactSync(BaseModel):
    """Contact data for HubSpot sync"""
    email: str
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    jobtitle: Optional[str] = None
    lifecyclestage: Optional[str] = "lead"

class SyncResult(BaseModel):
    """Result of a sync operation"""
    success: bool
    synced_companies: int = 0
    synced_contacts: int = 0
    failed_companies: List[dict] = []
    failed_contacts: List[dict] = []
    message: str

class UserPlanInfo(BaseModel):
    """User plan information"""
    user_id: str
    plan_name: str  # Free, Starter, Pro, Enterprise
    is_enterprise: bool
    is_paid: bool
