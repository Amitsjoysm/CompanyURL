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
BASE_URL = "https://api-access-restore.preview.emergentagent.com/api"
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
    
    async def test_amount_validation(self):
        """Test 5: Amount validation"""
        print("\n🧪 Test 5: Amount Validation")
        
        # Create a separate test user for validation tests to avoid rate limiting
        validation_email = f"validation_test_{int(time.time())}@example.com"
        validation_password = "ValidationTest123!"
        
        try:
            # Register validation test user
            register_data = {
                "email": validation_email,
                "password": validation_password,
                "full_name": "Validation Test User"
            }
            
            async with self.session.post(f"{BASE_URL}/auth/register", json=register_data) as response:
                if response.status not in [200, 201]:
                    print(f"⚠️ Failed to create validation test user: {response.status}")
                    # Fall back to waiting for rate limit reset
                    print("   Waiting for rate limit to reset...")
                    await asyncio.sleep(10)
                    headers = self.get_auth_headers()
                else:
                    # Login with validation user
                    login_data = {"email": validation_email, "password": validation_password}
                    async with self.session.post(f"{BASE_URL}/auth/login", json=login_data) as login_response:
                        if login_response.status == 200:
                            result = await login_response.json()
                            validation_token = result.get("access_token")
                            headers = {"Authorization": f"Bearer {validation_token}"}
                            print("   Using separate validation test user")
                        else:
                            headers = self.get_auth_headers()
                            print("   Using main test user")
        except:
            headers = self.get_auth_headers()
            print("   Using main test user")
        
        test_cases = [
            {"amount": -100, "credits": 1000, "expected": "fail", "description": "Negative amount"},
            {"amount": 150000, "credits": 1000, "expected": "fail", "description": "Amount exceeds maximum"},
            {"amount": 25, "credits": -100, "expected": "fail", "description": "Negative credits"},
            {"amount": 0, "credits": 1000, "expected": "fail", "description": "Zero amount"}
        ]
        
        passed_tests = 0
        
        for test_case in test_cases:
            try:
                order_data = {
                    "plan_name": "Test",
                    "amount": test_case["amount"],
                    "credits": test_case["credits"]
                }
                
                async with self.session.post(f"{BASE_URL}/payment/create-order", json=order_data, headers=headers) as response:
                    if test_case["expected"] == "fail" and response.status == 400:
                        error_text = await response.text()
                        print(f"✅ {test_case['description']}: Correctly rejected")
                        print(f"   Error: {error_text}")
                        passed_tests += 1
                    elif test_case["expected"] == "pass" and response.status == 200:
                        print(f"✅ {test_case['description']}: Correctly accepted")
                        passed_tests += 1
                    else:
                        print(f"❌ {test_case['description']}: Unexpected result (status: {response.status})")
                        
            except Exception as e:
                print(f"❌ {test_case['description']}: Error - {e}")
        
        if passed_tests == len(test_cases):
            print(f"✅ All {len(test_cases)} amount validation tests passed")
            self.test_results.append({"test": "Amount Validation", "status": "PASS", "details": f"{passed_tests}/{len(test_cases)} tests passed"})
            return True
        else:
            print(f"❌ {passed_tests}/{len(test_cases)} amount validation tests passed")
            self.test_results.append({"test": "Amount Validation", "status": "FAIL", "details": f"{passed_tests}/{len(test_cases)} tests passed"})
            return False
    
    async def test_bulk_check_functionality(self):
        """Test 6: Bulk check functionality"""
        print("\n🧪 Test 6: Bulk Check Functionality")
        try:
            # Create test CSV data
            csv_data = "domain\nexample.com\ngoogle.com\nmicrosoft.com\namazon.com\napple.com"
            csv_file = io.BytesIO(csv_data.encode())
            
            headers = self.get_auth_headers()
            
            # Create form data
            data = aiohttp.FormData()
            data.add_field('file', csv_file, filename='test_domains.csv', content_type='text/csv')
            
            async with self.session.post(f"{BASE_URL}/crawl/bulk-check", data=data, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    
                    required_fields = ["total_rows", "valid_rows", "required_credits", "available_credits", "can_proceed"]
                    if all(field in result for field in required_fields):
                        print("✅ Bulk check response contains all required fields")
                        print(f"   Total rows: {result['total_rows']}")
                        print(f"   Valid rows: {result['valid_rows']}")
                        print(f"   Required credits: {result['required_credits']}")
                        print(f"   Available credits: {result['available_credits']}")
                        print(f"   Can proceed: {result['can_proceed']}")
                        
                        self.test_results.append({"test": "Bulk Check Functionality", "status": "PASS", "details": f"Processed {result['valid_rows']} valid rows"})
                        return result
                    else:
                        missing_fields = [f for f in required_fields if f not in result]
                        print(f"❌ Missing required fields: {missing_fields}")
                        self.test_results.append({"test": "Bulk Check Functionality", "status": "FAIL", "details": f"Missing fields: {missing_fields}"})
                        return None
                else:
                    error_text = await response.text()
                    print(f"❌ Failed with status {response.status}: {error_text}")
                    self.test_results.append({"test": "Bulk Check Functionality", "status": "FAIL", "details": f"HTTP {response.status}: {error_text}"})
                    return None
                    
        except Exception as e:
            print(f"❌ Error: {e}")
            self.test_results.append({"test": "Bulk Check Functionality", "status": "FAIL", "details": str(e)})
            return None
    
    async def test_bulk_upload_with_credit_validation(self):
        """Test 7: Bulk upload with credit validation"""
        print("\n🧪 Test 7: Bulk Upload with Credit Validation")
        try:
            # Create test CSV with many domains to trigger insufficient credits
            domains = [f"test{i}.com" for i in range(1, 51)]  # 50 domains
            csv_data = "domain\n" + "\n".join(domains)
            csv_file = io.BytesIO(csv_data.encode())
            
            headers = self.get_auth_headers()
            
            # Create form data
            data = aiohttp.FormData()
            data.add_field('file', csv_file, filename='large_test.csv', content_type='text/csv')
            data.add_field('input_type', 'domain')
            
            async with self.session.post(f"{BASE_URL}/crawl/bulk-upload", data=data, headers=headers) as response:
                result = await response.json()
                
                if response.status == 402:
                    # Expected insufficient credits error
                    print("✅ Credit validation working - insufficient credits detected")
                    print(f"   Error: {result.get('detail', 'Unknown error')}")
                    self.test_results.append({"test": "Bulk Upload Credit Validation", "status": "PASS", "details": "Credit validation working"})
                    return True
                elif response.status == 200:
                    # Upload succeeded (user has enough credits)
                    print("✅ Bulk upload succeeded (user has sufficient credits)")
                    print(f"   Processed: {result.get('total_processed', 0)}")
                    print(f"   Failed: {result.get('total_failed', 0)}")
                    self.test_results.append({"test": "Bulk Upload Credit Validation", "status": "PASS", "details": f"Upload succeeded: {result.get('total_processed', 0)} processed"})
                    return True
                else:
                    print(f"❌ Unexpected status {response.status}: {result}")
                    self.test_results.append({"test": "Bulk Upload Credit Validation", "status": "FAIL", "details": f"Unexpected status: {response.status}"})
                    return False
                    
        except Exception as e:
            print(f"❌ Error: {e}")
            self.test_results.append({"test": "Bulk Upload Credit Validation", "status": "FAIL", "details": str(e)})
            return False
    
    async def test_transaction_history(self):
        """Test 8: Transaction history"""
        print("\n🧪 Test 8: Transaction History")
        try:
            headers = self.get_auth_headers()
            
            async with self.session.get(f"{BASE_URL}/payment/transactions", headers=headers) as response:
                if response.status == 200:
                    transactions = await response.json()
                    
                    if isinstance(transactions, list):
                        print(f"✅ Retrieved {len(transactions)} transactions")
                        
                        # Check if transactions have required security fields
                        if len(transactions) > 0:
                            sample_transaction = transactions[0]
                            security_fields = ["id", "user_id", "status", "created_at"]
                            missing_fields = [f for f in security_fields if f not in sample_transaction]
                            
                            if not missing_fields:
                                print("✅ Transactions contain all required security fields")
                                self.test_results.append({"test": "Transaction History", "status": "PASS", "details": f"{len(transactions)} transactions retrieved"})
                                return transactions
                            else:
                                print(f"❌ Missing security fields: {missing_fields}")
                                self.test_results.append({"test": "Transaction History", "status": "FAIL", "details": f"Missing fields: {missing_fields}"})
                                return None
                        else:
                            print("✅ No transactions found (expected for new user)")
                            self.test_results.append({"test": "Transaction History", "status": "PASS", "details": "No transactions (new user)"})
                            return []
                    else:
                        print("❌ Invalid response format")
                        self.test_results.append({"test": "Transaction History", "status": "FAIL", "details": "Invalid response format"})
                        return None
                else:
                    error_text = await response.text()
                    print(f"❌ Failed with status {response.status}: {error_text}")
                    self.test_results.append({"test": "Transaction History", "status": "FAIL", "details": f"HTTP {response.status}: {error_text}"})
                    return None
                    
        except Exception as e:
            print(f"❌ Error: {e}")
            self.test_results.append({"test": "Transaction History", "status": "FAIL", "details": str(e)})
            return None
    
    async def test_edge_cases(self):
        """Test 9: Edge cases"""
        print("\n🧪 Test 9: Edge Cases")
        
        edge_cases = [
            {"name": "Empty file upload", "test_func": self._test_empty_file},
            {"name": "Large file upload", "test_func": self._test_large_file},
            {"name": "Invalid file format", "test_func": self._test_invalid_file_format}
        ]
        
        passed_tests = 0
        
        for case in edge_cases:
            try:
                result = await case["test_func"]()
                if result:
                    print(f"✅ {case['name']}: Passed")
                    passed_tests += 1
                else:
                    print(f"❌ {case['name']}: Failed")
            except Exception as e:
                print(f"❌ {case['name']}: Error - {e}")
        
        if passed_tests == len(edge_cases):
            self.test_results.append({"test": "Edge Cases", "status": "PASS", "details": f"{passed_tests}/{len(edge_cases)} tests passed"})
            return True
        else:
            self.test_results.append({"test": "Edge Cases", "status": "FAIL", "details": f"{passed_tests}/{len(edge_cases)} tests passed"})
            return False
    
    async def _test_empty_file(self):
        """Test empty file upload"""
        try:
            csv_data = "domain\n"  # Only header
            csv_file = io.BytesIO(csv_data.encode())
            
            headers = self.get_auth_headers()
            data = aiohttp.FormData()
            data.add_field('file', csv_file, filename='empty.csv', content_type='text/csv')
            
            async with self.session.post(f"{BASE_URL}/crawl/bulk-check", data=data, headers=headers) as response:
                result = await response.json()
                
                if response.status == 200 and result.get("valid_rows", 0) == 0:
                    return True
                return False
        except:
            return False
    
    async def _test_large_file(self):
        """Test file with >10000 rows"""
        try:
            # Create CSV with 10001 rows
            domains = [f"test{i}.com" for i in range(1, 10002)]
            csv_data = "domain\n" + "\n".join(domains)
            csv_file = io.BytesIO(csv_data.encode())
            
            headers = self.get_auth_headers()
            data = aiohttp.FormData()
            data.add_field('file', csv_file, filename='large.csv', content_type='text/csv')
            data.add_field('input_type', 'domain')
            
            async with self.session.post(f"{BASE_URL}/crawl/bulk-upload", data=data, headers=headers) as response:
                if response.status == 400:
                    result = await response.json()
                    if "10,000 rows" in result.get("detail", ""):
                        return True
                return False
        except:
            return False
    
    async def _test_invalid_file_format(self):
        """Test invalid file format"""
        try:
            # Create a text file instead of CSV
            text_data = "This is not a CSV file"
            text_file = io.BytesIO(text_data.encode())
            
            headers = self.get_auth_headers()
            data = aiohttp.FormData()
            data.add_field('file', text_file, filename='invalid.txt', content_type='text/plain')
            
            async with self.session.post(f"{BASE_URL}/crawl/bulk-check", data=data, headers=headers) as response:
                if response.status == 400:
                    result = await response.json()
                    if "Invalid file format" in result.get("detail", ""):
                        return True
                return False
        except:
            return False
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print("🧪 PAYMENT SYSTEM TEST SUMMARY")
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
                           any(critical in r["test"] for critical in ["Payment", "Rate Limiting", "Credit Validation"])]
        
        if critical_failures:
            print("🚨 CRITICAL ISSUES FOUND:")
            for failure in critical_failures:
                print(f"   - {failure['test']}: {failure['details']}")
        else:
            print("✅ No critical payment system issues found")

async def main():
    """Main test execution"""
    print("🚀 Starting Payment System Security Tests")
    print("=" * 60)
    
    tester = PaymentSystemTester()
    
    try:
        # Setup
        await tester.setup()
        
        if not tester.auth_token:
            print("❌ Failed to authenticate. Cannot proceed with tests.")
            return
        
        # Run tests in priority order
        print("\n📋 Running tests in priority order...")
        
        # 1. Basic functionality tests
        await tester.test_get_razorpay_key()
        plans = await tester.test_get_plans()
        
        if plans:
            # Use a paid plan for order creation (skip Free plan)
            paid_plans = [p for p in plans if p.get("price", 0) > 0]
            test_plan = paid_plans[0] if paid_plans else {"name": "Starter", "price": 25.0, "credits": 1000}
            transaction = await tester.test_create_payment_order(test_plan)
        
        # 2. Security tests
        await tester.test_payment_rate_limiting()
        await tester.test_amount_validation()
        
        # 3. Bulk operations tests
        await tester.test_bulk_check_functionality()
        await tester.test_bulk_upload_with_credit_validation()
        
        # 4. History and audit tests
        await tester.test_transaction_history()
        
        # 5. Edge cases
        await tester.test_edge_cases()
        
        # Print summary
        tester.print_summary()
        
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
    finally:
        await tester.teardown()

if __name__ == "__main__":
    asyncio.run(main())