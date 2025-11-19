"""
HubSpot service for auto-sync functionality
"""
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.hubspot import HubSpotCompanySync, HubSpotContactSync
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class HubSpotService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def should_auto_sync(self, user_id: str) -> bool:
        """Check if user has auto-sync enabled"""
        settings = await self.db.hubspot_settings.find_one({"user_id": user_id})
        if not settings:
            return False
        
        return settings.get("auto_sync_enabled", False)
    
    async def prepare_company_for_sync(self, company_data: Dict) -> HubSpotCompanySync:
        """Convert crawled company data to HubSpot format"""
        return HubSpotCompanySync(
            name=company_data.get("name", ""),
            domain=company_data.get("domain", ""),
            city=company_data.get("location", {}).get("city"),
            state=company_data.get("location", {}).get("state"),
            country=company_data.get("location", {}).get("country"),
            industry=company_data.get("industry"),
            phone=company_data.get("contact", {}).get("phone"),
            website=company_data.get("website", company_data.get("domain")),
            employee_size=str(company_data.get("employee_size", "")),
            description=company_data.get("description")
        )
    
    async def prepare_contacts_from_company(self, company_data: Dict) -> List[HubSpotContactSync]:
        """Extract contacts from company data if available"""
        contacts = []
        
        # Extract from founders if available
        founders = company_data.get("founders", [])
        for founder in founders:
            if founder.get("email"):
                contacts.append(HubSpotContactSync(
                    email=founder["email"],
                    firstname=founder.get("first_name"),
                    lastname=founder.get("last_name"),
                    company=company_data.get("name"),
                    jobtitle="Founder",
                    lifecyclestage="customer"
                ))
        
        # Extract from contact info if available
        contact_info = company_data.get("contact", {})
        if contact_info.get("email"):
            contacts.append(HubSpotContactSync(
                email=contact_info["email"],
                company=company_data.get("name"),
                phone=contact_info.get("phone"),
                lifecyclestage="lead"
            ))
        
        return contacts
