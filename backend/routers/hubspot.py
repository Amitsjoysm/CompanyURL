from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from motor.motor_asyncio import AsyncIOMotorDatabase
from core.database import get_db
from core.auth import get_current_user
from core.config import get_settings
from models.hubspot import (
    HubSpotAuth, HubSpotSettings, HubSpotCompanySync,
    HubSpotContactSync, SyncResult
)
from typing import List
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode
import httpx
import jwt as pyjwt
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter(prefix="/hubspot", tags=["HubSpot CRM"])

# Helper function to check if user has access to HubSpot features
async def check_hubspot_access(current_user: dict, db: AsyncIOMotorDatabase):
    """Check if user has Enterprise plan or is superadmin"""
    user = await db.users.find_one({"id": current_user["sub"]})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    is_superadmin = user.get("role") == "superadmin"
    is_enterprise = user.get("current_plan", "").lower() == "enterprise"
    
    if not (is_superadmin or is_enterprise):
        raise HTTPException(
            status_code=403,
            detail="HubSpot CRM sync is only available for Enterprise users and Superadmins"
        )
    
    return user

@router.get("/auth/url")
async def get_auth_url(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Generate HubSpot OAuth authorization URL"""
    # Check access
    await check_hubspot_access(current_user, db)
    
    scopes = [
        "crm.objects.companies.read",
        "crm.objects.companies.write",
        "crm.objects.contacts.read",
        "crm.objects.contacts.write",
    ]
    
    # Create state token with user ID
    state_data = {
        "user_id": current_user["sub"],
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }
    state_token = pyjwt.encode(state_data, settings.SECRET_KEY, algorithm="HS256")
    
    params = {
        "client_id": settings.HUBSPOT_CLIENT_ID,
        "redirect_uri": settings.HUBSPOT_REDIRECT_URI,
        "scope": " ".join(scopes),
        "state": state_token,
    }
    
    auth_url = f"https://app.hubspot.com/oauth/authorize?{urlencode(params)}"
    return {"auth_url": auth_url}

@router.get("/callback")
async def oauth_callback(
    code: str,
    state: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Handle OAuth callback from HubSpot"""
    # Verify and decode state token
    try:
        state_data = pyjwt.decode(state, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = state_data["user_id"]
    except pyjwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="State token expired")
    except pyjwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid state token")
    
    # Exchange code for tokens
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            f"{settings.HUBSPOT_API_BASE_URL}/oauth/v1/token",
            data={
                "grant_type": "authorization_code",
                "client_id": settings.HUBSPOT_CLIENT_ID,
                "client_secret": settings.HUBSPOT_CLIENT_SECRET,
                "redirect_uri": settings.HUBSPOT_REDIRECT_URI,
                "code": code,
            },
        )
    
    if token_response.status_code != 200:
        logger.error(f"Failed to obtain tokens: {token_response.text}")
        raise HTTPException(status_code=400, detail="Failed to obtain access tokens")
    
    token_data = token_response.json()
    
    # Store tokens
    hubspot_auth = HubSpotAuth(
        user_id=user_id,
        access_token=token_data["access_token"],
        refresh_token=token_data["refresh_token"],
        expires_at=datetime.now(timezone.utc) + timedelta(seconds=token_data["expires_in"]),
    )
    
    # Delete existing auth for this user
    await db.hubspot_auth.delete_many({"user_id": user_id})
    
    # Insert new auth
    await db.hubspot_auth.insert_one(hubspot_auth.model_dump())
    
    # Create or update settings with defaults
    existing_settings = await db.hubspot_settings.find_one({"user_id": user_id})
    if not existing_settings:
        settings_doc = HubSpotSettings(user_id=user_id)
        await db.hubspot_settings.insert_one(settings_doc.model_dump())
    
    # Redirect to frontend success page
    return RedirectResponse(url=f"{settings.CORS_ORIGINS.split(',')[0]}/dashboard?hubspot=connected")

async def get_valid_access_token(user_id: str, db: AsyncIOMotorDatabase) -> str:
    """Get valid access token, refreshing if necessary"""
    auth_doc = await db.hubspot_auth.find_one({"user_id": user_id})
    
    if not auth_doc:
        raise HTTPException(
            status_code=401,
            detail="HubSpot not connected. Please authorize the app first."
        )
    
    expires_at = auth_doc["expires_at"]
    
    # Refresh if token expires within 5 minutes
    if datetime.now(timezone.utc) > expires_at - timedelta(minutes=5):
        async with httpx.AsyncClient() as client:
            refresh_response = await client.post(
                f"{settings.HUBSPOT_API_BASE_URL}/oauth/v1/token",
                data={
                    "grant_type": "refresh_token",
                    "client_id": settings.HUBSPOT_CLIENT_ID,
                    "client_secret": settings.HUBSPOT_CLIENT_SECRET,
                    "refresh_token": auth_doc["refresh_token"],
                },
            )
        
        if refresh_response.status_code == 200:
            new_token_data = refresh_response.json()
            await db.hubspot_auth.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "access_token": new_token_data["access_token"],
                        "expires_at": datetime.now(timezone.utc) + timedelta(seconds=new_token_data["expires_in"]),
                        "updated_at": datetime.now(timezone.utc)
                    }
                }
            )
            return new_token_data["access_token"]
        else:
            logger.error(f"Failed to refresh token: {refresh_response.text}")
            raise HTTPException(status_code=401, detail="Failed to refresh access token")
    
    return auth_doc["access_token"]

@router.get("/status")
async def get_connection_status(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get HubSpot connection status"""
    user = await check_hubspot_access(current_user, db)
    
    auth_doc = await db.hubspot_auth.find_one({"user_id": current_user["sub"]})
    settings_doc = await db.hubspot_settings.find_one({"user_id": current_user["sub"]})
    
    return {
        "connected": auth_doc is not None,
        "auto_sync_enabled": settings_doc.get("auto_sync_enabled", False) if settings_doc else False,
        "last_sync_at": settings_doc.get("last_sync_at") if settings_doc else None,
    }

@router.post("/settings")
async def update_settings(
    auto_sync_enabled: bool = Query(False),
    sync_companies: bool = Query(True),
    sync_contacts: bool = Query(True),
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Update HubSpot sync settings"""
    await check_hubspot_access(current_user, db)
    
    await db.hubspot_settings.update_one(
        {"user_id": current_user["sub"]},
        {
            "$set": {
                "auto_sync_enabled": auto_sync_enabled,
                "sync_companies": sync_companies,
                "sync_contacts": sync_contacts,
                "updated_at": datetime.now(timezone.utc)
            }
        },
        upsert=True
    )
    
    return {"message": "Settings updated successfully"}

@router.get("/settings")
async def get_settings_endpoint(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get HubSpot sync settings"""
    await check_hubspot_access(current_user, db)
    
    settings_doc = await db.hubspot_settings.find_one({"user_id": current_user["sub"]})
    
    if not settings_doc:
        return {
            "auto_sync_enabled": False,
            "sync_companies": True,
            "sync_contacts": True,
        }
    
    return {
        "auto_sync_enabled": settings_doc.get("auto_sync_enabled", False),
        "sync_companies": settings_doc.get("sync_companies", True),
        "sync_contacts": settings_doc.get("sync_contacts", True),
        "last_sync_at": settings_doc.get("last_sync_at"),
    }

@router.post("/sync/companies", response_model=SyncResult)
async def sync_companies(
    companies: List[HubSpotCompanySync],
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Manually sync companies to HubSpot"""
    await check_hubspot_access(current_user, db)
    
    try:
        access_token = await get_valid_access_token(current_user["sub"], db)
    except HTTPException as e:
        raise e
    
    synced_count = 0
    failed = []
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for company in companies:
            try:
                # Check if company exists by domain
                search_response = await client.post(
                    f"{settings.HUBSPOT_API_BASE_URL}/crm/v3/objects/companies/search",
                    headers={"Authorization": f"Bearer {access_token}"},
                    json={
                        "filterGroups": [
                            {
                                "filters": [
                                    {
                                        "propertyName": "domain",
                                        "operator": "EQ",
                                        "value": company.domain
                                    }
                                ]
                            }
                        ]
                    }
                )
                
                # Prepare properties
                properties = {
                    "name": company.name,
                    "domain": company.domain,
                }
                
                if company.city:
                    properties["city"] = company.city
                if company.state:
                    properties["state"] = company.state
                if company.country:
                    properties["country"] = company.country
                if company.industry:
                    properties["industry"] = company.industry
                if company.phone:
                    properties["phone"] = company.phone
                if company.website:
                    properties["website"] = company.website
                if company.description:
                    properties["description"] = company.description
                
                if search_response.status_code == 200:
                    search_data = search_response.json()
                    
                    if search_data.get("total", 0) > 0:
                        # Update existing company
                        company_id = search_data["results"][0]["id"]
                        update_response = await client.patch(
                            f"{settings.HUBSPOT_API_BASE_URL}/crm/v3/objects/companies/{company_id}",
                            headers={"Authorization": f"Bearer {access_token}"},
                            json={"properties": properties}
                        )
                        
                        if update_response.status_code == 200:
                            synced_count += 1
                        else:
                            failed.append({"domain": company.domain, "error": update_response.text})
                    else:
                        # Create new company
                        create_response = await client.post(
                            f"{settings.HUBSPOT_API_BASE_URL}/crm/v3/objects/companies",
                            headers={"Authorization": f"Bearer {access_token}"},
                            json={"properties": properties}
                        )
                        
                        if create_response.status_code == 201:
                            synced_count += 1
                        else:
                            failed.append({"domain": company.domain, "error": create_response.text})
                            
            except Exception as e:
                logger.error(f"Error syncing company {company.domain}: {str(e)}")
                failed.append({"domain": company.domain, "error": str(e)})
    
    # Update last sync time
    await db.hubspot_settings.update_one(
        {"user_id": current_user["sub"]},
        {"$set": {"last_sync_at": datetime.now(timezone.utc)}}
    )
    
    return SyncResult(
        success=len(failed) == 0,
        synced_companies=synced_count,
        failed_companies=failed,
        message=f"Synced {synced_count} companies, {len(failed)} failed"
    )

@router.post("/sync/contacts", response_model=SyncResult)
async def sync_contacts(
    contacts: List[HubSpotContactSync],
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Manually sync contacts to HubSpot"""
    await check_hubspot_access(current_user, db)
    
    try:
        access_token = await get_valid_access_token(current_user["sub"], db)
    except HTTPException as e:
        raise e
    
    synced_count = 0
    failed = []
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Use batch upsert for contacts (more efficient)
        inputs = []
        for contact in contacts:
            properties = {"email": contact.email}
            
            if contact.firstname:
                properties["firstname"] = contact.firstname
            if contact.lastname:
                properties["lastname"] = contact.lastname
            if contact.phone:
                properties["phone"] = contact.phone
            if contact.company:
                properties["company"] = contact.company
            if contact.jobtitle:
                properties["jobtitle"] = contact.jobtitle
            if contact.lifecyclestage:
                properties["lifecyclestage"] = contact.lifecyclestage
            
            inputs.append({
                "id": contact.email,
                "idProperty": "email",
                "properties": properties
            })
        
        try:
            response = await client.post(
                f"{settings.HUBSPOT_API_BASE_URL}/crm/v3/objects/contacts/batch/upsert",
                headers={"Authorization": f"Bearer {access_token}"},
                json={"inputs": inputs}
            )
            
            if response.status_code == 200 or response.status_code == 201:
                response_data = response.json()
                synced_count = len(response_data.get("results", []))
            else:
                for contact in contacts:
                    failed.append({"email": contact.email, "error": response.text})
                
        except Exception as e:
            logger.error(f"Error syncing contacts: {str(e)}")
            for contact in contacts:
                failed.append({"email": contact.email, "error": str(e)})
    
    # Update last sync time
    await db.hubspot_settings.update_one(
        {"user_id": current_user["sub"]},
        {"$set": {"last_sync_at": datetime.now(timezone.utc)}}
    )
    
    return SyncResult(
        success=len(failed) == 0,
        synced_contacts=synced_count,
        failed_contacts=failed,
        message=f"Synced {synced_count} contacts, {len(failed)} failed"
    )

@router.delete("/disconnect")
async def disconnect_hubspot(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Disconnect HubSpot integration"""
    await check_hubspot_access(current_user, db)
    
    # Delete auth tokens
    await db.hubspot_auth.delete_many({"user_id": current_user["sub"]})
    
    # Delete settings
    await db.hubspot_settings.delete_many({"user_id": current_user["sub"]})
    
    return {"message": "HubSpot disconnected successfully"}
