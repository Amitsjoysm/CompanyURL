#!/usr/bin/env python3
"""
Debug API Token Creation Issue
"""

import asyncio
import aiohttp
import json

BASE_URL = "https://api-token-repair.preview.emergentagent.com/api"
TEST_USER_EMAIL = "testuser@example.com"
TEST_USER_PASSWORD = "TestPassword123!"

async def debug_api_token():
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
                print(f"✅ Logged in successfully, token: {token[:20]}...")
                
                headers = {"Authorization": f"Bearer {token}"}
                
                # Try to create API token
                token_data = {
                    "name": "Debug Test Token",
                    "scopes": ["crawl:read", "crawl:write"]
                }
                
                print(f"Attempting to create API token with data: {token_data}")
                
                async with session.post(f"{BASE_URL}/api-tokens/", json=token_data, headers=headers) as response:
                    print(f"Response status: {response.status}")
                    print(f"Response headers: {dict(response.headers)}")
                    
                    if response.status == 307:
                        print("Got redirect, following...")
                        redirect_url = response.headers.get('Location')
                        print(f"Redirect URL: {redirect_url}")
                        
                        # Follow redirect manually
                        async with session.post(redirect_url, json=token_data, headers=headers) as redirect_response:
                            print(f"Redirect response status: {redirect_response.status}")
                            redirect_text = await redirect_response.text()
                            print(f"Redirect response: {redirect_text}")
                    else:
                        response_text = await response.text()
                        print(f"Response: {response_text}")
            else:
                print(f"❌ Login failed: {response.status}")

if __name__ == "__main__":
    asyncio.run(debug_api_token())