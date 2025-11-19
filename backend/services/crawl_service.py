from motor.motor_asyncio import AsyncIOMotorDatabase
from models.company import CrawlRequest, BulkCrawlJob, CompanyData, CrawlRequestCreate
from services.crawler_orchestrator import CrawlerOrchestrator
from services.user_service import UserService
from typing import List, Optional
import logging
from datetime import datetime, timezone
import asyncio
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)

class CrawlService:
    """Service for managing crawl requests and jobs"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.crawl_requests = db.crawl_requests
        self.bulk_jobs = db.bulk_jobs
        self.central_ledger = db.central_ledger
        
        self.orchestrator = CrawlerOrchestrator()
        self.user_service = UserService(db)
    
    async def create_crawl_request(self, user_id: str, request_data: CrawlRequestCreate) -> CrawlRequest:
        """
        Create a single crawl request
        """
        # Check user credits
        credits = await self.user_service.get_user_credits(user_id)
        if credits < 1:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail="Insufficient credits"
            )
        
        # Create request
        crawl_request = CrawlRequest(
            user_id=user_id,
            input_type=request_data.input_type,
            input_value=request_data.input_value,
            status="pending"
        )
        
        request_dict = crawl_request.model_dump()
        request_dict['created_at'] = request_dict['created_at'].isoformat()
        
        await self.crawl_requests.insert_one(request_dict)
        
        # Process request asynchronously
        asyncio.create_task(self._process_crawl_request(crawl_request.id, user_id))
        
        logger.info(f"Created crawl request {crawl_request.id} for user {user_id}")
        return crawl_request
    
    async def _process_crawl_request(self, request_id: str, user_id: str):
        """
        Process a crawl request (background task)
        """
        try:
            # Update status to processing
            await self.crawl_requests.update_one(
                {"id": request_id},
                {"$set": {"status": "processing"}}
            )
            
            # Get request details
            request_dict = await self.crawl_requests.find_one({"id": request_id})
            if not request_dict:
                return
            
            # Perform crawl
            company_data = await self.orchestrator.crawl_company(
                query=request_dict['input_value'],
                query_type=request_dict['input_type'],
                user_id=user_id
            )
            
            # Update central ledger
            await self._update_central_ledger(company_data)
            
            # Update request with result
            result_dict = company_data.model_dump()
            result_dict['last_crawled'] = result_dict['last_crawled'].isoformat()
            
            await self.crawl_requests.update_one(
                {"id": request_id},
                {
                    "$set": {
                        "status": "completed",
                        "result": result_dict,
                        "completed_at": datetime.now(timezone.utc).isoformat()
                    }
                }
            )
            
            # Deduct credits
            await self.user_service.update_credits(user_id, -1)
            
            logger.info(f"Completed crawl request {request_id}")
        
        except Exception as e:
            logger.error(f"Error processing crawl request {request_id}: {str(e)}")
            await self.crawl_requests.update_one(
                {"id": request_id},
                {
                    "$set": {
                        "status": "failed",
                        "error": str(e),
                        "completed_at": datetime.now(timezone.utc).isoformat()
                    }
                }
            )
    
    async def _update_central_ledger(self, company_data: CompanyData):
        """
        Update central ledger with crawled company data
        """
        # Use domain or company_name as unique identifier
        identifier = company_data.domain or company_data.company_name
        if not identifier:
            return
        
        company_dict = company_data.model_dump()
        company_dict['last_crawled'] = company_dict['last_crawled'].isoformat()
        
        # Upsert to central ledger
        await self.central_ledger.update_one(
            {"domain": identifier},
            {"$set": company_dict},
            upsert=True
        )
    
    async def get_crawl_request(self, request_id: str, user_id: str) -> Optional[CrawlRequest]:
        """
        Get crawl request by ID
        """
        request_dict = await self.crawl_requests.find_one(
            {"id": request_id, "user_id": user_id},
            {"_id": 0}
        )
        
        if not request_dict:
            return None
        
        # Convert timestamps
        for field in ['created_at', 'completed_at']:
            if request_dict.get(field) and isinstance(request_dict[field], str):
                request_dict[field] = datetime.fromisoformat(request_dict[field])
        
        # Convert result if exists
        if request_dict.get('result'):
            result = request_dict['result']
            if isinstance(result['last_crawled'], str):
                result['last_crawled'] = datetime.fromisoformat(result['last_crawled'])
            request_dict['result'] = CompanyData(**result)
        
        return CrawlRequest(**request_dict)
    
    async def get_user_requests(self, user_id: str, limit: int = 50) -> List[CrawlRequest]:
        """
        Get user's crawl requests
        """
        requests_list = await self.crawl_requests.find(
            {"user_id": user_id},
            {"_id": 0}
        ).sort("created_at", -1).limit(limit).to_list(limit)
        
        result = []
        for req in requests_list:
            for field in ['created_at', 'completed_at']:
                if req.get(field) and isinstance(req[field], str):
                    req[field] = datetime.fromisoformat(req[field])
            
            if req.get('result'):
                res = req['result']
                if isinstance(res['last_crawled'], str):
                    res['last_crawled'] = datetime.fromisoformat(res['last_crawled'])
                req['result'] = CompanyData(**res)
            
            result.append(CrawlRequest(**req))
        
        return result
    
    async def search_central_ledger(self, query: str, limit: int = 10) -> List[CompanyData]:
        """
        Search central ledger for company data
        """
        # Search by domain or company name
        search_filter = {
            "$or": [
                {"domain": {"$regex": query, "$options": "i"}},
                {"company_name": {"$regex": query, "$options": "i"}}
            ]
        }
        
        companies = await self.central_ledger.find(search_filter, {"_id": 0}).limit(limit).to_list(limit)
        
        result = []
        for comp in companies:
            if isinstance(comp['last_crawled'], str):
                comp['last_crawled'] = datetime.fromisoformat(comp['last_crawled'])
            result.append(CompanyData(**comp))
        
        return result
