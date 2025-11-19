from services.base_crawler import BaseCrawler
from typing import Optional, Dict, Any, List
import logging
import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class NewsCrawler(BaseCrawler):
    """Crawler for fetching latest company news"""
    
    def __init__(self):
        super().__init__()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    async def crawl(self, query: str, query_type: str) -> Optional[Dict[str, Any]]:
        """
        Fetch latest news about the company
        """
        try:
            # Get company name for search
            if query_type == 'company_name':
                company_name = query
            else:
                # Would need to get company name from other sources first
                return None
            
            logger.info(f"Fetching news for: {company_name}")
            
            # Use Google News or other news aggregators
            news_items = await self._fetch_google_news(company_name)
            
            if news_items:
                return {
                    'latest_news': news_items
                }
            
            return None
        
        except Exception as e:
            logger.error(f"Error fetching news for {query}: {str(e)}")
            return None
    
    async def _fetch_google_news(self, company_name: str) -> List[Dict[str, Any]]:
        """Fetch news from Google News"""
        try:
            # Google News RSS or search
            # Simplified implementation
            search_url = f"https://news.google.com/search?q={company_name}&hl=en-US&gl=US&ceid=US:en"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(search_url, headers=self.headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status != 200:
                        return []
                    
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Extract news items (structure may vary)
                    news_items = []
                    articles = soup.find_all('article', limit=5)
                    
                    for article in articles:
                        title_elem = article.find('h3')
                        if title_elem:
                            news_items.append({
                                'title': title_elem.get_text().strip(),
                                'date': datetime.now(timezone.utc).isoformat()
                            })
                    
                    return news_items
        
        except Exception as e:
            logger.error(f"Error fetching Google News: {str(e)}")
            return []
