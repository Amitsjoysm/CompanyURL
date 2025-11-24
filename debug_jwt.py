#!/usr/bin/env python3
"""
Debug JWT Token
"""

import asyncio
import aiohttp
import json
import jwt

BASE_URL = "https://service-restart-auth.preview.emergentagent.com/api"
TEST_USER_EMAIL = "testuser@example.com"
TEST_USER_PASSWORD = "TestPassword123!"

async def debug_jwt():
    async with aiohttp.ClientSession() as session:
        # Login first
        login_data = {
            "email": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD
        }
        
        async with session.post(f"{BASE_URL}/auth/login", json=login_data) as response:
            if response.status == 200:
                result = await response.json()
                token = result.get("access_token")
                print(f"✅ Logged in successfully")
                print(f"Token: {token}")
                
                # Decode token without verification to see contents
                try:
                    decoded = jwt.decode(token, options={"verify_signature": False})
                    print(f"Decoded token: {json.dumps(decoded, indent=2)}")
                except Exception as e:
                    print(f"Error decoding token: {e}")
                
                # Test a simple authenticated endpoint
                headers = {"Authorization": f"Bearer {token}"}
                async with session.get(f"{BASE_URL}/crawl/history", headers=headers) as response:
                    print(f"Crawl history status: {response.status}")
                    if response.status != 200:
                        error_text = await response.text()
                        print(f"Crawl history error: {error_text}")
                
            else:
                print(f"❌ Login failed: {response.status}")

if __name__ == "__main__":
    asyncio.run(debug_jwt())