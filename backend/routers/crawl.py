from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from models.company import CrawlRequestCreate, CrawlRequest, CompanyData
from services.crawl_service import CrawlService
from core.database import get_db
from core.auth import get_current_user
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
import pandas as pd
import io

router = APIRouter(prefix="/crawl", tags=["Crawl"])

@router.post("/single", response_model=CrawlRequest)
async def create_single_crawl(
    request_data: CrawlRequestCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Create a single crawl request"""
    crawl_service = CrawlService(db)
    return await crawl_service.create_crawl_request(current_user['sub'], request_data)

@router.get("/request/{request_id}", response_model=CrawlRequest)
async def get_crawl_request(
    request_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get crawl request by ID"""
    crawl_service = CrawlService(db)
    request = await crawl_service.get_crawl_request(request_id, current_user['sub'])
    
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    return request

@router.get("/history", response_model=List[CrawlRequest])
async def get_crawl_history(
    limit: int = 50,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get user's crawl history"""
    crawl_service = CrawlService(db)
    return await crawl_service.get_user_requests(current_user['sub'], limit)

@router.get("/search", response_model=List[CompanyData])
async def search_companies(
    query: str,
    limit: int = 10,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Search companies in central ledger"""
    crawl_service = CrawlService(db)
    return await crawl_service.search_central_ledger(query, limit)

@router.post("/bulk-upload")
async def bulk_upload(
    file: UploadFile = File(...),
    input_type: str = "domain",
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Upload CSV/Excel file for bulk crawling"""
    try:
        contents = await file.read()
        
        # Read file based on type
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(io.BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="Invalid file format. Use CSV or Excel")
        
        # Process rows
        crawl_service = CrawlService(db)
        requests = []
        
        for _, row in df.iterrows():
            # Assume first column contains the input values
            input_value = str(row.iloc[0])
            request_data = CrawlRequestCreate(input_type=input_type, input_value=input_value)
            req = await crawl_service.create_crawl_request(current_user['sub'], request_data)
            requests.append(req.id)
        
        return {
            "message": f"Created {len(requests)} crawl requests",
            "request_ids": requests
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
