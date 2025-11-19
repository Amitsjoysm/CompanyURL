#!/usr/bin/env python3
"""
Test simple authenticated endpoint
"""

import asyncio
import aiohttp
import json

BASE_URL = "https://api-token-repair.preview.emergentagent.com/api"
TEST_USER_EMAIL = "testuser@example.com"
TEST_USER_PASSWORD = "TestPassword123!"

async def test_auth():
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
                
                headers = {"Authorization": f"Bearer {token}"}
                
                # Test different authenticated endpoints
                endpoints = [
                    "/crawl/history",
                    "/api-tokens/",  # GET should work
                    "/payment/transactions"
                ]
                
                for endpoint in endpoints:
                    async with session.get(f"{BASE_URL}{endpoint}", headers=headers) as response:
                        print(f"{endpoint}: {response.status}")
                        if response.status not in [200, 404]:
                            error_text = await response.text()
                            print(f"  Error: {error_text}")
                
            else:
                print(f"❌ Login failed: {response.status}")

if __name__ == "__main__":
    asyncio.run(test_auth())