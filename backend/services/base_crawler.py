from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from models.company import CompanyData
import logging

logger = logging.getLogger(__name__)

class BaseCrawler(ABC):
    """Abstract base class for all crawlers following Open/Closed Principle"""
    
    def __init__(self):
        self.source_name = self.__class__.__name__
    
    @abstractmethod
    async def crawl(self, query: str, query_type: str) -> Optional[Dict[str, Any]]:
        """
        Crawl data from source
        
        Args:
            query: The search query (company name, domain, or LinkedIn URL)
            query_type: Type of query ('company_name', 'domain', 'linkedin_url')
        
        Returns:
            Dictionary with company data or None if not found
        """
        pass
    
    def calculate_confidence(self, data: Dict[str, Any]) -> float:
        """
        Calculate confidence score based on data completeness
        
        Returns:
            Confidence score between 0.0 and 1.0
        """
        total_fields = 0
        filled_fields = 0
        
        important_fields = [
            'company_name', 'domain', 'linkedin_url',
            'industry', 'employee_size', 'description'
        ]
        
        for field in important_fields:
            total_fields += 1
            if data.get(field):
                filled_fields += 1
        
        return filled_fields / total_fields if total_fields > 0 else 0.0
    
    def normalize_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize raw data to standard format
        """
        return raw_data
