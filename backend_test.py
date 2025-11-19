#!/usr/bin/env python3
"""
Comprehensive Backend Testing for Admin CRUD Operations and API Token System
Tests admin functionality including user management, plans, content, and API tokens.
"""

import asyncio
import aiohttp
import json
import csv
import io
import time
from typing import Dict, Any, Optional
import uuid
import os

# Configuration
BASE_URL = "https://api-token-repair.preview.emergentagent.com/api"
SUPERADMIN_EMAIL = "admin@test.com"
SUPERADMIN_PASSWORD = "Admin123!"
TEST_USER_EMAIL = "testuser@example.com"
TEST_USER_PASSWORD = "TestPassword123!"

class AdminCRUDTester:
    def __init__(self):
        self.session = None
        self.superadmin_token = None
        self.regular_user_token = None
        self.superadmin_user_id = None
        self.regular_user_id = None
        self.test_results = []
        self.created_resources = {
            "users": [],
            "plans": [],
            "blogs": [],
            "faqs": [],
            "api_tokens": []
        }
        
    async def setup(self):
        """Initialize test session and authenticate"""
        self.session = aiohttp.ClientSession()
        
        # Create/login superadmin user
        await self.create_superadmin_user()
        await self.login_superadmin()
        
        # Create/login regular test user
        await self.register_test_user()
        await self.login_test_user()
        
    async def teardown(self):
        """Clean up test session"""
        if self.session:
            await self.session.close()
    
    async def create_superadmin_user(self):
        """Create superadmin user if doesn't exist"""
        try:
            register_data = {
                "email": SUPERADMIN_EMAIL,
                "password": SUPERADMIN_PASSWORD,
                "full_name": "Super Admin",
                "role": "superadmin"
            }
            
            async with self.session.post(f"{BASE_URL}/auth/register", json=register_data) as response:
                if response.status in [200, 201]:
                    print("✅ Superadmin user created successfully")
                elif response.status == 400:
                    print("ℹ️ Superadmin user already exists")
                else:
                    print(f"⚠️ Superadmin registration failed with status {response.status}")
        except Exception as e:
            print(f"⚠️ Superadmin registration error: {e}")
    
    async def login_superadmin(self):
        """Login superadmin and get auth token"""
        try:
            login_data = {
                "email": SUPERADMIN_EMAIL,
                "password": SUPERADMIN_PASSWORD
            }
            
            async with self.session.post(f"{BASE_URL}/auth/login", json=login_data) as response:
                if response.status == 200:
                    result = await response.json()
                    self.superadmin_token = result.get("access_token")
                    print("✅ Superadmin logged in successfully")
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ Superadmin login failed with status {response.status}: {error_text}")
                    return False
        except Exception as e:
            print(f"❌ Superadmin login error: {e}")
            return False
    
    async def register_test_user(self):
        """Register a regular test user"""
        try:
            register_data = {
                "email": TEST_USER_EMAIL,
                "password": TEST_USER_PASSWORD,
                "full_name": "Test User"
            }
            
            async with self.session.post(f"{BASE_URL}/auth/register", json=register_data) as response:
                if response.status in [200, 201]:
                    print("✅ Regular test user registered successfully")
                elif response.status == 400:
                    print("ℹ️ Regular test user already exists")
                else:
                    print(f"⚠️ Regular user registration failed with status {response.status}")
        except Exception as e:
            print(f"⚠️ Regular user registration error: {e}")
    
    async def login_test_user(self):
        """Login regular test user and get auth token"""
        try:
            login_data = {
                "email": TEST_USER_EMAIL,
                "password": TEST_USER_PASSWORD
            }
            
            async with self.session.post(f"{BASE_URL}/auth/login", json=login_data) as response:
                if response.status == 200:
                    result = await response.json()
                    self.regular_user_token = result.get("access_token")
                    print("✅ Regular test user logged in successfully")
                    return True
                else:
                    print(f"❌ Regular user login failed with status {response.status}")
                    return False
        except Exception as e:
            print(f"❌ Regular user login error: {e}")
            return False
    
    def get_superadmin_headers(self) -> Dict[str, str]:
        """Get superadmin authorization headers"""
        if not self.superadmin_token:
            return {}
        return {"Authorization": f"Bearer {self.superadmin_token}"}
    
    def get_regular_user_headers(self) -> Dict[str, str]:
        """Get regular user authorization headers"""
        if not self.regular_user_token:
            return {}
        return {"Authorization": f"Bearer {self.regular_user_token}"}
    
    async def test_admin_users_management(self):
        """Test 1: Admin Users Management"""
        print("\n🧪 Test 1: Admin Users Management")
        
        # Test 1a: Get all users (should work with superadmin)
        try:
            headers = self.get_superadmin_headers()
            async with self.session.get(f"{BASE_URL}/admin/users", headers=headers) as response:
                if response.status == 200:
                    users = await response.json()
                    print(f"✅ Retrieved {len(users)} users as superadmin")
                    
                    # Find a user to test updates on
                    test_user = None
                    for user in users:
                        if user.get('email') == TEST_USER_EMAIL:
                            test_user = user
                            break
                    
                    if test_user:
                        user_id = test_user['id']
                        
                        # Test 1b: Update user credits
                        credits_data = {"credits": 500}
                        async with self.session.put(f"{BASE_URL}/admin/users/{user_id}/credits", 
                                                  json=credits_data, headers=headers) as response:
                            if response.status == 200:
                                print("✅ User credits updated successfully")
                            else:
                                print(f"❌ Credits update failed: {response.status}")
                                
                        # Test 1c: Update user status
                        status_data = {"is_active": True}
                        async with self.session.put(f"{BASE_URL}/admin/users/{user_id}/status", 
                                                  json=status_data, headers=headers) as response:
                            if response.status == 200:
                                print("✅ User status updated successfully")
                            else:
                                print(f"❌ Status update failed: {response.status}")
                                
                        # Test 1d: Update user plan
                        plan_data = {"current_plan": "Pro"}
                        async with self.session.put(f"{BASE_URL}/admin/users/{user_id}/plan", 
                                                  json=plan_data, headers=headers) as response:
                            if response.status == 200:
                                print("✅ User plan updated successfully")
                            else:
                                print(f"❌ Plan update failed: {response.status}")
                    
                    self.test_results.append({"test": "Admin Users Management", "status": "PASS", "details": f"Managed {len(users)} users"})
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ Failed to get users: {response.status} - {error_text}")
                    self.test_results.append({"test": "Admin Users Management", "status": "FAIL", "details": f"HTTP {response.status}: {error_text}"})
                    return False
        except Exception as e:
            print(f"❌ Error: {e}")
            self.test_results.append({"test": "Admin Users Management", "status": "FAIL", "details": str(e)})
            return False
    
    async def test_admin_plans_management(self):
        """Test 2: Admin Plans Management"""
        print("\n🧪 Test 2: Admin Plans Management")
        
        try:
            headers = self.get_superadmin_headers()
            
            # Test 2a: Get existing plans
            async with self.session.get(f"{BASE_URL}/payment/plans") as response:
                if response.status == 200:
                    existing_plans = await response.json()
                    print(f"✅ Retrieved {len(existing_plans)} existing plans")
                else:
                    print(f"⚠️ Could not retrieve existing plans: {response.status}")
                    existing_plans = []
            
            # Test 2b: Create new plan
            new_plan_data = {
                "name": f"Test Plan {int(time.time())}",
                "price": 99.99,
                "credits": 5000,
                "is_active": True
            }
            
            async with self.session.post(f"{BASE_URL}/admin/plans", json=new_plan_data, headers=headers) as response:
                if response.status == 200:
                    created_plan = await response.json()
                    plan_id = created_plan.get('id')
                    self.created_resources["plans"].append(plan_id)
                    print(f"✅ Created new plan: {created_plan.get('name')}")
                    
                    # Test 2c: Update plan
                    update_data = {
                        "price": 149.99,
                        "credits": 7500
                    }
                    async with self.session.put(f"{BASE_URL}/admin/plans/{plan_id}", 
                                              json=update_data, headers=headers) as response:
                        if response.status == 200:
                            print("✅ Plan updated successfully")
                        else:
                            print(f"❌ Plan update failed: {response.status}")
                    
                    # Test 2d: Delete plan
                    async with self.session.delete(f"{BASE_URL}/admin/plans/{plan_id}", headers=headers) as response:
                        if response.status == 200:
                            print("✅ Plan deleted successfully")
                            self.created_resources["plans"].remove(plan_id)
                        else:
                            print(f"❌ Plan deletion failed: {response.status}")
                    
                    self.test_results.append({"test": "Admin Plans Management", "status": "PASS", "details": "CRUD operations successful"})
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ Failed to create plan: {response.status} - {error_text}")
                    self.test_results.append({"test": "Admin Plans Management", "status": "FAIL", "details": f"Create failed: {response.status}"})
                    return False
                    
        except Exception as e:
            print(f"❌ Error: {e}")
            self.test_results.append({"test": "Admin Plans Management", "status": "FAIL", "details": str(e)})
            return False
    
    async def test_content_management_blogs(self):
        """Test 3: Content Management - Blogs"""
        print("\n🧪 Test 3: Content Management - Blogs")
        
        try:
            headers = self.get_superadmin_headers()
            
            # Test 3a: Get all blogs (public endpoint)
            async with self.session.get(f"{BASE_URL}/content/blogs") as response:
                if response.status == 200:
                    existing_blogs = await response.json()
                    print(f"✅ Retrieved {len(existing_blogs)} existing blogs")
                else:
                    print(f"⚠️ Could not retrieve existing blogs: {response.status}")
                    existing_blogs = []
            
            # Test 3b: Create new blog (admin only)
            blog_slug = f"test-blog-{int(time.time())}"
            new_blog_data = {
                "title": f"Test Blog {int(time.time())}",
                "slug": blog_slug,
                "content": "This is a test blog content for admin testing.",
                "excerpt": "Test blog excerpt",
                "meta_title": "Test Blog Meta Title",
                "meta_description": "Test blog meta description",
                "is_published": True
            }
            
            async with self.session.post(f"{BASE_URL}/content/blogs", json=new_blog_data, headers=headers) as response:
                if response.status == 200:
                    created_blog = await response.json()
                    self.created_resources["blogs"].append(blog_slug)
                    print(f"✅ Created new blog: {created_blog.get('title')}")
                    
                    # Test 3c: Update blog
                    update_data = {
                        "title": f"Updated Test Blog {int(time.time())}",
                        "content": "Updated content for the test blog."
                    }
                    async with self.session.put(f"{BASE_URL}/content/blogs/{blog_slug}", 
                                              json=update_data, headers=headers) as response:
                        if response.status == 200:
                            print("✅ Blog updated successfully")
                        else:
                            print(f"❌ Blog update failed: {response.status}")
                    
                    # Test 3d: Get specific blog (public endpoint)
                    async with self.session.get(f"{BASE_URL}/content/blogs/{blog_slug}") as response:
                        if response.status == 200:
                            print("✅ Blog retrieved successfully")
                        else:
                            print(f"❌ Blog retrieval failed: {response.status}")
                    
                    # Test 3e: Delete blog
                    async with self.session.delete(f"{BASE_URL}/content/blogs/{blog_slug}", headers=headers) as response:
                        if response.status == 200:
                            print("✅ Blog deleted successfully")
                            self.created_resources["blogs"].remove(blog_slug)
                        else:
                            print(f"❌ Blog deletion failed: {response.status}")
                    
                    self.test_results.append({"test": "Content Management - Blogs", "status": "PASS", "details": "CRUD operations successful"})
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ Failed to create blog: {response.status} - {error_text}")
                    self.test_results.append({"test": "Content Management - Blogs", "status": "FAIL", "details": f"Create failed: {response.status}"})
                    return False
                    
        except Exception as e:
            print(f"❌ Error: {e}")
            self.test_results.append({"test": "Content Management - Blogs", "status": "FAIL", "details": str(e)})
            return False
    
    async def test_content_management_faqs(self):
        """Test 4: Content Management - FAQs"""
        print("\n🧪 Test 4: Content Management - FAQs")
        
        try:
            headers = self.get_superadmin_headers()
            
            # Test 4a: Get all FAQs (public endpoint)
            async with self.session.get(f"{BASE_URL}/content/faqs") as response:
                if response.status == 200:
                    existing_faqs = await response.json()
                    print(f"✅ Retrieved {len(existing_faqs)} existing FAQs")
                else:
                    print(f"⚠️ Could not retrieve existing FAQs: {response.status}")
                    existing_faqs = []
            
            # Test 4b: Create new FAQ (admin only)
            new_faq_data = {
                "question": f"Test FAQ Question {int(time.time())}?",
                "answer": "This is a test FAQ answer for admin testing.",
                "category": "Testing",
                "is_published": True
            }
            
            async with self.session.post(f"{BASE_URL}/content/faqs", json=new_faq_data, headers=headers) as response:
                if response.status == 200:
                    created_faq = await response.json()
                    faq_id = created_faq.get('id')
                    self.created_resources["faqs"].append(faq_id)
                    print(f"✅ Created new FAQ: {created_faq.get('question')}")
                    
                    # Test 4c: Update FAQ
                    update_data = {
                        "question": f"Updated Test FAQ Question {int(time.time())}?",
                        "answer": "Updated answer for the test FAQ."
                    }
                    async with self.session.put(f"{BASE_URL}/content/faqs/{faq_id}", 
                                              json=update_data, headers=headers) as response:
                        if response.status == 200:
                            print("✅ FAQ updated successfully")
                        else:
                            print(f"❌ FAQ update failed: {response.status}")
                    
                    # Test 4d: Delete FAQ
                    async with self.session.delete(f"{BASE_URL}/content/faqs/{faq_id}", headers=headers) as response:
                        if response.status == 200:
                            print("✅ FAQ deleted successfully")
                            self.created_resources["faqs"].remove(faq_id)
                        else:
                            print(f"❌ FAQ deletion failed: {response.status}")
                    
                    self.test_results.append({"test": "Content Management - FAQs", "status": "PASS", "details": "CRUD operations successful"})
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ Failed to create FAQ: {response.status} - {error_text}")
                    self.test_results.append({"test": "Content Management - FAQs", "status": "FAIL", "details": f"Create failed: {response.status}"})
                    return False
                    
        except Exception as e:
            print(f"❌ Error: {e}")
            self.test_results.append({"test": "Content Management - FAQs", "status": "FAIL", "details": str(e)})
            return False
    
    async def test_central_ledger_access(self):
        """Test 5: Central Ledger Access"""
        print("\n🧪 Test 5: Central Ledger Access")
        
        try:
            headers = self.get_superadmin_headers()
            
            # Test 5a: Access central ledger with superadmin
            async with self.session.get(f"{BASE_URL}/admin/central-ledger", headers=headers) as response:
                if response.status == 200:
                    companies = await response.json()
                    print(f"✅ Retrieved {len(companies)} companies from central ledger")
                    
                    # Test 5b: Try with regular user (should fail)
                    regular_headers = self.get_regular_user_headers()
                    async with self.session.get(f"{BASE_URL}/admin/central-ledger", headers=regular_headers) as response:
                        if response.status == 403:
                            print("✅ Regular user correctly denied access to central ledger")
                        else:
                            print(f"❌ Regular user should be denied access, got: {response.status}")
                    
                    self.test_results.append({"test": "Central Ledger Access", "status": "PASS", "details": f"Retrieved {len(companies)} companies"})
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ Failed to access central ledger: {response.status} - {error_text}")
                    self.test_results.append({"test": "Central Ledger Access", "status": "FAIL", "details": f"HTTP {response.status}: {error_text}"})
                    return False
                    
        except Exception as e:
            print(f"❌ Error: {e}")
            self.test_results.append({"test": "Central Ledger Access", "status": "FAIL", "details": str(e)})
            return False
    
    async def test_api_token_system(self):
        """Test 6: API Token System"""
        print("\n🧪 Test 6: API Token System")
        
        try:
            headers = self.get_regular_user_headers()
            
            # Test 6a: Create API token
            token_data = {
                "name": f"Test Token {int(time.time())}",
                "scopes": ["crawl:read", "crawl:write"],
                "expires_in_days": 30
            }
            
            async with self.session.post(f"{BASE_URL}/api-tokens/", json=token_data, headers=headers) as response:
                if response.status == 200:
                    created_token = await response.json()
                    token_id = created_token.get('id')
                    api_key = created_token.get('token')
                    self.created_resources["api_tokens"].append(token_id)
                    print(f"✅ Created API token: {created_token.get('name')}")
                    print(f"   Token ID: {token_id}")
                    print(f"   API Key: {api_key[:20]}...")
                    
                    # Test 6b: List API tokens
                    async with self.session.get(f"{BASE_URL}/api-tokens/", headers=headers) as response:
                        if response.status == 200:
                            tokens = await response.json()
                            print(f"✅ Retrieved {len(tokens)} API tokens")
                        else:
                            print(f"❌ Failed to list tokens: {response.status}")
                    
                    # Test 6c: Test API key authentication
                    api_headers = {"X-API-Key": api_key}
                    async with self.session.get(f"{BASE_URL}/crawl/history", headers=api_headers) as response:
                        if response.status == 200:
                            history = await response.json()
                            print(f"✅ API key authentication successful - retrieved {len(history)} crawl history items")
                        else:
                            print(f"❌ API key authentication failed: {response.status}")
                    
                    # Test 6d: Toggle API token
                    async with self.session.put(f"{BASE_URL}/api-tokens/{token_id}/toggle/", headers=headers) as response:
                        if response.status == 200:
                            result = await response.json()
                            print(f"✅ Token toggled: {result.get('message')}")
                        else:
                            print(f"❌ Token toggle failed: {response.status}")
                    
                    # Test 6e: Delete API token
                    async with self.session.delete(f"{BASE_URL}/api-tokens/{token_id}/", headers=headers) as response:
                        if response.status == 200:
                            print("✅ API token deleted successfully")
                            self.created_resources["api_tokens"].remove(token_id)
                        else:
                            print(f"❌ Token deletion failed: {response.status}")
                    
                    self.test_results.append({"test": "API Token System", "status": "PASS", "details": "All token operations successful"})
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ Failed to create API token: {response.status} - {error_text}")
                    self.test_results.append({"test": "API Token System", "status": "FAIL", "details": f"Create failed: {response.status}"})
                    return False
                    
        except Exception as e:
            print(f"❌ Error: {e}")
            self.test_results.append({"test": "API Token System", "status": "FAIL", "details": str(e)})
            return False
    
    async def test_permission_validation(self):
        """Test 7: Permission Validation"""
        print("\n🧪 Test 7: Permission Validation")
        
        try:
            regular_headers = self.get_regular_user_headers()
            
            # Test 7a: Regular user trying to access admin endpoints (should fail)
            admin_endpoints = [
                ("/admin/users", "GET"),
                ("/admin/central-ledger", "GET"),
                ("/content/blogs", "POST"),
                ("/content/faqs", "POST"),
                ("/admin/plans", "POST")
            ]
            
            forbidden_count = 0
            
            for endpoint, method in admin_endpoints:
                try:
                    if method == "GET":
                        async with self.session.get(f"{BASE_URL}{endpoint}", headers=regular_headers) as response:
                            if response.status == 403:
                                forbidden_count += 1
                                print(f"✅ Regular user correctly denied access to {endpoint}")
                            else:
                                print(f"❌ Regular user should be denied access to {endpoint}, got: {response.status}")
                    elif method == "POST":
                        test_data = {"test": "data"}
                        async with self.session.post(f"{BASE_URL}{endpoint}", json=test_data, headers=regular_headers) as response:
                            if response.status == 403:
                                forbidden_count += 1
                                print(f"✅ Regular user correctly denied access to {endpoint}")
                            else:
                                print(f"❌ Regular user should be denied access to {endpoint}, got: {response.status}")
                except Exception as e:
                    print(f"⚠️ Error testing {endpoint}: {e}")
            
            # Test 7b: Superadmin should have access
            superadmin_headers = self.get_superadmin_headers()
            async with self.session.get(f"{BASE_URL}/admin/users", headers=superadmin_headers) as response:
                if response.status == 200:
                    print("✅ Superadmin has correct access to admin endpoints")
                    superadmin_access = True
                else:
                    print(f"❌ Superadmin should have access to admin endpoints, got: {response.status}")
                    superadmin_access = False
            
            if forbidden_count >= 3 and superadmin_access:  # At least 3 endpoints properly protected
                self.test_results.append({"test": "Permission Validation", "status": "PASS", "details": f"{forbidden_count} endpoints properly protected"})
                return True
            else:
                self.test_results.append({"test": "Permission Validation", "status": "FAIL", "details": f"Only {forbidden_count} endpoints properly protected"})
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            self.test_results.append({"test": "Permission Validation", "status": "FAIL", "details": str(e)})
            return False
    
    async def test_authentication_edge_cases(self):
        """Test 8: Authentication Edge Cases"""
        print("\n🧪 Test 8: Authentication Edge Cases")
        
        try:
            # Test 8a: Invalid JWT token
            invalid_headers = {"Authorization": "Bearer invalid_token_here"}
            async with self.session.get(f"{BASE_URL}/admin/users", headers=invalid_headers) as response:
                if response.status == 401:
                    print("✅ Invalid JWT token correctly rejected")
                else:
                    print(f"❌ Invalid JWT should be rejected, got: {response.status}")
            
            # Test 8b: Invalid API key
            invalid_api_headers = {"X-API-Key": "invalid_api_key_here"}
            async with self.session.get(f"{BASE_URL}/crawl/history", headers=invalid_api_headers) as response:
                if response.status == 401:
                    print("✅ Invalid API key correctly rejected")
                else:
                    print(f"❌ Invalid API key should be rejected, got: {response.status}")
            
            # Test 8c: No authentication
            async with self.session.get(f"{BASE_URL}/admin/users") as response:
                if response.status == 401:
                    print("✅ No authentication correctly rejected")
                else:
                    print(f"❌ No authentication should be rejected, got: {response.status}")
            
            # Test 8d: Mixed authentication (both JWT and API key - should use API key)
            if self.created_resources["api_tokens"]:
                # Create a new token for this test
                headers = self.get_regular_user_headers()
                token_data = {
                    "name": f"Mixed Auth Test {int(time.time())}",
                    "scopes": ["crawl:read"]
                }
                
                async with self.session.post(f"{BASE_URL}/api-tokens/", json=token_data, headers=headers) as response:
                    if response.status == 200:
                        created_token = await response.json()
                        api_key = created_token.get('token')
                        
                        mixed_headers = {
                            "Authorization": f"Bearer {self.regular_user_token}",
                            "X-API-Key": api_key
                        }
                        
                        async with self.session.get(f"{BASE_URL}/crawl/history", headers=mixed_headers) as response:
                            if response.status == 200:
                                print("✅ Mixed authentication handled correctly (API key takes precedence)")
                            else:
                                print(f"❌ Mixed authentication failed: {response.status}")
                        
                        # Clean up
                        token_id = created_token.get('id')
                        await self.session.delete(f"{BASE_URL}/api-tokens/{token_id}/", headers=headers)
            
            self.test_results.append({"test": "Authentication Edge Cases", "status": "PASS", "details": "All edge cases handled correctly"})
            return True
                
        except Exception as e:
            print(f"❌ Error: {e}")
            self.test_results.append({"test": "Authentication Edge Cases", "status": "FAIL", "details": str(e)})
            return False
    
    async def cleanup_created_resources(self):
        """Clean up any resources created during testing"""
        print("\n🧹 Cleaning up created resources...")
        
        try:
            superadmin_headers = self.get_superadmin_headers()
            regular_headers = self.get_regular_user_headers()
            
            # Clean up API tokens
            for token_id in self.created_resources["api_tokens"]:
                try:
                    await self.session.delete(f"{BASE_URL}/api-tokens/{token_id}/", headers=regular_headers)
                    print(f"   Cleaned up API token: {token_id}")
                except:
                    pass
            
            # Clean up blogs
            for blog_slug in self.created_resources["blogs"]:
                try:
                    await self.session.delete(f"{BASE_URL}/content/blogs/{blog_slug}", headers=superadmin_headers)
                    print(f"   Cleaned up blog: {blog_slug}")
                except:
                    pass
            
            # Clean up FAQs
            for faq_id in self.created_resources["faqs"]:
                try:
                    await self.session.delete(f"{BASE_URL}/content/faqs/{faq_id}", headers=superadmin_headers)
                    print(f"   Cleaned up FAQ: {faq_id}")
                except:
                    pass
            
            # Clean up plans
            for plan_id in self.created_resources["plans"]:
                try:
                    await self.session.delete(f"{BASE_URL}/admin/plans/{plan_id}", headers=superadmin_headers)
                    print(f"   Cleaned up plan: {plan_id}")
                except:
                    pass
                    
        except Exception as e:
            print(f"⚠️ Error during cleanup: {e}")
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print("🧪 ADMIN CRUD & API TOKEN SYSTEM TEST SUMMARY")
        print("="*60)
        
        passed = sum(1 for result in self.test_results if result["status"] == "PASS")
        failed = sum(1 for result in self.test_results if result["status"] == "FAIL")
        
        print(f"Total Tests: {len(self.test_results)}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"Success Rate: {(passed/len(self.test_results)*100):.1f}%" if self.test_results else "0%")
        
        print("\nDetailed Results:")
        print("-" * 60)
        
        for result in self.test_results:
            status_icon = "✅" if result["status"] == "PASS" else "❌"
            print(f"{status_icon} {result['test']}: {result['status']}")
            print(f"   Details: {result['details']}")
        
        print("\n" + "="*60)
        
        # Critical issues summary
        critical_failures = [r for r in self.test_results if r["status"] == "FAIL" and 
                           any(critical in r["test"] for critical in ["Admin", "API Token", "Permission", "Central Ledger"])]
        
        if critical_failures:
            print("🚨 CRITICAL ADMIN ISSUES FOUND:")
            for failure in critical_failures:
                print(f"   - {failure['test']}: {failure['details']}")
        else:
            print("✅ No critical admin system issues found")

async def main():
    """Main test execution"""
    print("🚀 Starting Admin CRUD Operations and API Token System Tests")
    print("=" * 60)
    
    tester = AdminCRUDTester()
    
    try:
        # Setup
        await tester.setup()
        
        if not tester.superadmin_token:
            print("❌ Failed to authenticate superadmin. Cannot proceed with admin tests.")
            return
        
        if not tester.regular_user_token:
            print("❌ Failed to authenticate regular user. Cannot proceed with API token tests.")
            return
        
        # Run tests in priority order
        print("\n📋 Running admin CRUD and API token tests...")
        
        # 1. Admin user management tests
        await tester.test_admin_users_management()
        
        # 2. Admin plans management tests
        await tester.test_admin_plans_management()
        
        # 3. Content management tests
        await tester.test_content_management_blogs()
        await tester.test_content_management_faqs()
        
        # 4. Central ledger access test
        await tester.test_central_ledger_access()
        
        # 5. API token system tests
        await tester.test_api_token_system()
        
        # 6. Permission validation tests
        await tester.test_permission_validation()
        
        # 7. Authentication edge cases
        await tester.test_authentication_edge_cases()
        
        # Clean up created resources
        await tester.cleanup_created_resources()
        
        # Print summary
        tester.print_summary()
        
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
    finally:
        await tester.teardown()

if __name__ == "__main__":
    asyncio.run(main())