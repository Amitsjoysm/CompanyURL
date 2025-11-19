from typing import Dict, Any, Optional
import logging
from groq import Groq
from core.config import get_settings
import json

logger = logging.getLogger(__name__)
settings = get_settings()

class AIService:
    """AI service for enriching and validating company data using Groq"""
    
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY) if settings.GROQ_API_KEY else None
        self.model = "llama-3.3-70b-versatile"  # Fast and accurate model
    
    async def enrich_company_data(self, data: Dict[str, Any], query: str, query_type: str) -> Dict[str, Any]:
        """
        Use AI to enrich and validate company data
        
        Args:
            data: Current company data
            query: Original search query
            query_type: Type of query
        
        Returns:
            Enriched data dictionary
        """
        if not self.client:
            logger.warning("Groq API key not configured")
            return {}
        
        try:
            # Create prompt for AI
            prompt = self._create_enrichment_prompt(data, query, query_type)
            
            # Call Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a business intelligence assistant specialized in company data enrichment. Provide accurate, structured information about companies. Always respond in valid JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,  # Low temperature for consistency
                max_tokens=1000
            )
            
            # Parse response
            ai_response = response.choices[0].message.content
            
            # Extract JSON from response
            enriched_data = self._parse_ai_response(ai_response)
            
            return enriched_data
        
        except Exception as e:
            logger.error(f"Error in AI enrichment: {str(e)}")
            return {}
    
    def _create_enrichment_prompt(self, data: Dict[str, Any], query: str, query_type: str) -> str:
        """
        Create prompt for AI enrichment
        """
        return f"""Given the following partially complete company information, please enrich and validate it:

Query: {query}
Query Type: {query_type}

Current Data:
{json.dumps(data, indent=2)}

Please provide:
1. Missing company information if you can infer it
2. Validation of existing data
3. Industry classification
4. Approximate employee size if not present
5. Brief description if missing

Respond in JSON format with only the fields you can confidently fill or correct. Use this structure:
{{
    "company_name": "validated or enriched name",
    "industry": "primary industry",
    "employee_size": "size range (e.g., 50-200, 1000+)",
    "description": "brief company description",
    "founded_on": "year if known"
}}

Only include fields you are confident about. Return empty JSON {{}} if you cannot enrich the data."""
    
    def _parse_ai_response(self, response: str) -> Dict[str, Any]:
        """
        Parse AI response and extract JSON
        """
        try:
            # Try to find JSON in response
            start = response.find('{')
            end = response.rfind('}') + 1
            
            if start != -1 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
            
            return {}
        
        except Exception as e:
            logger.error(f"Error parsing AI response: {str(e)}")
            return {}
    
    async def validate_linkedin_url(self, url: str, company_name: str) -> float:
        """
        Validate if LinkedIn URL matches company name
        
        Returns:
            Confidence score (0.0 to 1.0)
        """
        if not self.client or not url or not company_name:
            return 0.5
        
        try:
            prompt = f"""Does the LinkedIn URL '{url}' likely belong to the company '{company_name}'?
            
Respond with only a number between 0.0 and 1.0 representing confidence, where:
- 1.0 = definitely matches
- 0.5 = uncertain
- 0.0 = definitely does not match

Consider:
- URL slug similarity to company name
- Common company naming patterns
- Abbreviations and variations

Response (number only):"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a data validation expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=10
            )
            
            score_str = response.choices[0].message.content.strip()
            return float(score_str)
        
        except Exception as e:
            logger.error(f"Error validating LinkedIn URL: {str(e)}")
            return 0.5
