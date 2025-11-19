from typing import Dict, Any, List, Optional
from services.base_crawler import BaseCrawler
from services.website_crawler import WebsiteCrawler
from services.linkedin_crawler import LinkedInCrawler
from services.news_crawler import NewsCrawler
from services.ai_service import AIService
from models.company import CompanyData
import logging
import asyncio

logger = logging.getLogger(__name__)

class CrawlerOrchestrator:
    """Orchestrates multiple crawlers following Dependency Inversion Principle"""
    
    def __init__(self):
        # Initialize crawlers in priority order
        self.crawlers: List[BaseCrawler] = [
            WebsiteCrawler(),
            LinkedInCrawler(),
            NewsCrawler()
        ]
        self.ai_service = AIService()
    
    async def crawl_company(self, query: str, query_type: str, user_id: str) -> CompanyData:
        """
        Orchestrate crawling from multiple sources
        
        Args:
            query: Search query
            query_type: Type of query ('company_name', 'domain', 'linkedin_url')
            user_id: User ID for tracking
        
        Returns:
            CompanyData with aggregated information
        """
        logger.info(f"Starting crawl for {query} (type: {query_type})")
        
        # Collect data from all sources
        all_data = {}
        data_sources = []
        
        # Run crawlers in parallel with priority
        tasks = []
        for crawler in self.crawlers:
            tasks.append(self._safe_crawl(crawler, query, query_type))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Aggregate results
        for i, result in enumerate(results):
            if isinstance(result, dict) and result:
                crawler_name = self.crawlers[i].source_name
                data_sources.append(crawler_name)
                all_data = self._merge_data(all_data, result)
        
        # Use AI to enrich and validate data
        if all_data:
            enriched_data = await self.ai_service.enrich_company_data(all_data, query, query_type)
            all_data = self._merge_data(all_data, enriched_data)
        
        # Calculate confidence score
        confidence = self._calculate_overall_confidence(all_data, len(data_sources))
        
        # Create CompanyData object
        company_data = CompanyData(
            **all_data,
            confidence_score=confidence,
            data_sources=data_sources,
            crawled_by_user=user_id
        )
        
        logger.info(f"Crawl completed for {query}. Confidence: {confidence:.2f}")
        return company_data
    
    async def _safe_crawl(self, crawler: BaseCrawler, query: str, query_type: str) -> Optional[Dict[str, Any]]:
        """Safely execute crawler with error handling"""
        try:
            return await crawler.crawl(query, query_type)
        except Exception as e:
            logger.error(f"Error in {crawler.source_name}: {str(e)}")
            return None
    
    def _merge_data(self, base: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge new data into base data, prioritizing non-empty values
        """
        merged = base.copy()
        
        for key, value in new.items():
            if value is not None and value != "" and value != []:
                if key not in merged or not merged[key]:
                    merged[key] = value
                elif isinstance(value, list) and isinstance(merged.get(key), list):
                    # Merge lists and remove duplicates
                    merged[key] = list(set(merged[key] + value))
        
        return merged
    
    def _calculate_overall_confidence(self, data: Dict[str, Any], num_sources: int) -> float:
        """
        Calculate confidence score based on data completeness and number of sources
        """
        # Base score from data completeness
        important_fields = [
            'company_name', 'domain', 'linkedin_url',
            'industry', 'employee_size', 'description',
            'emails', 'phone_numbers', 'address'
        ]
        
        filled = sum(1 for field in important_fields if data.get(field))
        completeness_score = filled / len(important_fields)
        
        # Bonus for multiple sources
        source_bonus = min(num_sources * 0.1, 0.3)
        
        return min(completeness_score + source_bonus, 1.0)
