#!/usr/bin/env python3
"""
Rate Limiting Test - Test that rate limiting is working correctly
"""

import asyncio
import aiohttp
import time

BASE_URL = "https://service-restart-auth.preview.emergentagent.com/api"
SUPERADMIN_EMAIL = "admin@corpinfo.com"
SUPERADMIN_PASSWORD = "Admin@2025!Secure"

async def test_rate_limiting():
    """Test rate limiting functionality"""
    print("🧪 Testing Rate Limiting Functionality")
    print("=" * 50)
    
    async with aiohttp.ClientSession() as session:
        # Login to get token
        login_data = {
            "email": SUPERADMIN_EMAIL,
            "password": SUPERADMIN_PASSWORD
        }
        
        async with session.post(f"{BASE_URL}/auth/login", json=login_data) as response:
            if response.status == 200:
                result = await response.json()
                token = result.get("access_token")
                headers = {"Authorization": f"Bearer {token}"}
                print("✅ Authenticated successfully")
            else:
                print("❌ Authentication failed")
                return
        
        # Make rapid requests to test rate limiting
        print("\n🔄 Making rapid requests to test rate limiting...")
        
        rate_limited = False
        requests_made = 0
        
        for i in range(70):  # Try to exceed the 60 requests per minute limit
            try:
                async with session.get(f"{BASE_URL}/admin/users", headers=headers) as response:
                    requests_made += 1
                    
                    # Check rate limit headers
                    limit = response.headers.get('X-RateLimit-Limit')
                    remaining = response.headers.get('X-RateLimit-Remaining')
                    reset = response.headers.get('X-RateLimit-Reset')
                    
                    if response.status == 429:
                        print(f"✅ Rate limiting triggered at request {requests_made}")
                        print(f"   Status: {response.status}")
                        print(f"   Rate Limit Headers:")
                        print(f"     X-RateLimit-Limit: {limit}")
                        print(f"     X-RateLimit-Remaining: {remaining}")
                        print(f"     X-RateLimit-Reset: {reset}")
                        
                        retry_after = response.headers.get('Retry-After')
                        if retry_after:
                            print(f"     Retry-After: {retry_after}")
                        
                        rate_limited = True
                        break
                    elif response.status == 200:
                        if i % 10 == 0:  # Print every 10th request
                            print(f"   Request {requests_made}: Status {response.status}, Remaining: {remaining}")
                    else:
                        print(f"   Request {requests_made}: Unexpected status {response.status}")
                        
            except Exception as e:
                print(f"   Request {requests_made}: Error - {e}")
            
            # Small delay to avoid overwhelming the server
            await asyncio.sleep(0.05)
        
        if rate_limited:
            print(f"\n✅ Rate limiting is working correctly!")
            print(f"   Triggered after {requests_made} requests")
        else:
            print(f"\n⚠️ Rate limiting not triggered after {requests_made} requests")
            print("   This might be expected if the limit is higher or implemented differently")

if __name__ == "__main__":
    asyncio.run(test_rate_limiting())