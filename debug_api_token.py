#!/usr/bin/env python3
"""
Debug API Token Creation Issue
"""

import asyncio
import aiohttp
import json

BASE_URL = "https://crm-sync-hub-2.preview.emergentagent.com/api"
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
                        
                        if response.status == 200:
                            token_info = await response.json()
                            api_key = token_info.get('token')
                            token_id = token_info.get('id')
                            
                            print(f"\n🧪 Testing API key authentication with: {api_key[:20]}...")
                            
                            # Test API key on different endpoints
                            api_headers = {"X-API-Key": api_key}
                            
                            # Test 1: /auth/me
                            async with session.get(f"{BASE_URL}/auth/me", headers=api_headers) as test_response:
                                print(f"   /auth/me: {test_response.status}")
                                if test_response.status != 200:
                                    error_text = await test_response.text()
                                    print(f"   Error: {error_text}")
                            
                            # Test 2: /crawl/history
                            async with session.get(f"{BASE_URL}/crawl/history", headers=api_headers) as test_response:
                                print(f"   /crawl/history: {test_response.status}")
                                if test_response.status != 200:
                                    error_text = await test_response.text()
                                    print(f"   Error: {error_text}")
                            
                            # Test 3: /api-tokens/ (list)
                            async with session.get(f"{BASE_URL}/api-tokens/", headers=api_headers) as test_response:
                                print(f"   /api-tokens/ (list): {test_response.status}")
                                if test_response.status != 200:
                                    error_text = await test_response.text()
                                    print(f"   Error: {error_text}")
                            
                            # Clean up - delete the token
                            async with session.delete(f"{BASE_URL}/api-tokens/{token_id}", headers=api_headers) as test_response:
                                print(f"   /api-tokens/{token_id} (delete): {test_response.status}")
                                if test_response.status != 200:
                                    error_text = await test_response.text()
                                    print(f"   Error: {error_text}")
            else:
                print(f"❌ Login failed: {response.status}")

if __name__ == "__main__":
    asyncio.run(debug_api_token())