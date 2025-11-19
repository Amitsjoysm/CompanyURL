from services.base_crawler import BaseCrawler
from typing import Optional, Dict, Any
import logging
import aiohttp
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse

logger = logging.getLogger(__name__)

class WebsiteCrawler(BaseCrawler):
    """Crawler for extracting data from company websites"""
    
    def __init__(self):
        super().__init__()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    async def crawl(self, query: str, query_type: str) -> Optional[Dict[str, Any]]:
        """
        Crawl company website for information
        """
        try:
            if query_type == 'domain':
                url = f"https://{query}" if not query.startswith('http') else query
            elif query_type == 'company_name':
                # For company name, we'll try to construct a domain
                domain = self._company_name_to_domain(query)
                url = f"https://{domain}"
            else:
                return None
            
            logger.info(f"Crawling website: {url}")
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status != 200:
                        logger.warning(f"Failed to fetch {url}: {response.status}")
                        return None
                    
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    data = self._extract_data_from_html(soup, url)
                    return data
        
        except Exception as e:
            logger.error(f"Error crawling website {query}: {str(e)}")
            return None
    
    def _company_name_to_domain(self, company_name: str) -> str:
        """Convert company name to potential domain"""
        # Remove common suffixes
        name = re.sub(r'\b(Inc|LLC|Ltd|Corporation|Corp|Company|Co)\b', '', company_name, flags=re.IGNORECASE)
        # Convert to lowercase and replace spaces with nothing or hyphens
        domain = name.strip().lower().replace(' ', '')
        return f"{domain}.com"
    
    def _extract_data_from_html(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """Extract company data from HTML"""
        data = {
            'domain': urlparse(url).netloc.replace('www.', ''),
            'website_urls': [url]
        }
        
        # Extract title as potential company name
        if soup.title:
            data['company_name'] = soup.title.string.strip()
        
        # Extract meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            data['description'] = meta_desc.get('content').strip()
        
        # Try to find contact info
        text_content = soup.get_text()
        
        # Find emails
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text_content)
        if emails:
            data['emails'] = list(set(emails))[:5]  # Limit to 5 unique emails
        
        # Find phone numbers
        phones = re.findall(r'\b(?:\+?1[-.]?)?\(?([0-9]{3})\)?[-.]?([0-9]{3})[-.]?([0-9]{4})\b', text_content)
        if phones:
            data['phone_numbers'] = [f"+1-{p[0]}-{p[1]}-{p[2]}" for p in phones[:3]]
        
        # Try to find LinkedIn
        linkedin_links = soup.find_all('a', href=re.compile(r'linkedin\.com/company/'))
        if linkedin_links:
            data['linkedin_url'] = linkedin_links[0].get('href')
        
        # Try to find Twitter
        twitter_links = soup.find_all('a', href=re.compile(r'twitter\.com/'))
        if twitter_links:
            data['twitter_url'] = twitter_links[0].get('href')
        
        return data
