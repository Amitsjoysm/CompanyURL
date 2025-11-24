"""
Currency Service - Handles currency detection and conversion
"""
from motor.motor_asyncio import AsyncIOMotorDatabase
import httpx
import logging
from typing import Tuple

logger = logging.getLogger(__name__)

class CurrencyService:
    """Service for currency detection and exchange rates"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def detect_currency_from_ip(self, ip_address: str) -> Tuple[str, str]:
        """
        Detect currency based on IP address
        Returns (currency_code, country_code)
        """
        try:
            # Use ipapi.co for geolocation (free, no API key required)
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"https://ipapi.co/{ip_address}/json/")
                
                if response.status_code == 200:
                    data = response.json()
                    country_code = data.get("country_code", "US")
                    
                    # India gets INR, everyone else gets USD
                    currency = "INR" if country_code == "IN" else "USD"
                    logger.info(f"Detected country: {country_code}, currency: {currency}")
                    return currency, country_code
        except Exception as e:
            logger.warning(f"Error detecting currency from IP {ip_address}: {str(e)}")
        
        # Default to USD if detection fails
        return "USD", "US"
    
    async def get_exchange_rate(self) -> float:
        """
        Get USD to INR exchange rate
        First checks admin-configured fixed rate, then falls back to real-time API
        """
        # Check for admin-configured rate
        settings = await self.db.settings.find_one({"key": "exchange_rate"})
        if settings and settings.get("usd_to_inr_rate"):
            rate = settings["usd_to_inr_rate"]
            logger.info(f"Using admin-configured exchange rate: {rate}")
            return rate
        
        # Fall back to real-time rate from exchangerate-api.com (free tier)
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get("https://api.exchangerate-api.com/v4/latest/USD")
                
                if response.status_code == 200:
                    data = response.json()
                    rate = data["rates"]["INR"]
                    logger.info(f"Using real-time exchange rate: {rate}")
                    return rate
        except Exception as e:
            logger.warning(f"Error fetching real-time exchange rate: {str(e)}")
        
        # Default fallback rate
        default_rate = 83.0
        logger.info(f"Using default exchange rate: {default_rate}")
        return default_rate
    
    async def convert_usd_to_inr(self, usd_amount: float) -> float:
        """Convert USD amount to INR"""
        rate = await self.get_exchange_rate()
        return round(usd_amount * rate, 2)
    
    async def convert_inr_to_usd(self, inr_amount: float) -> float:
        """Convert INR amount to USD"""
        rate = await self.get_exchange_rate()
        return round(inr_amount / rate, 2)
    
    async def get_price_in_currency(self, usd_price: float, currency: str) -> float:
        """
        Get price in specified currency
        Base prices are stored in USD
        """
        if currency == "INR":
            return await self.convert_usd_to_inr(usd_price)
        return usd_price
    
    async def normalize_to_usd(self, amount: float, currency: str) -> float:
        """
        Normalize any currency amount to USD for internal processing
        """
        if currency == "INR":
            return await self.convert_inr_to_usd(amount)
        return amount
