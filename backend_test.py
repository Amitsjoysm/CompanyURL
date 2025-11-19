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
        self.auth_token = None
        self.user_id = None
        self.test_results = []
        
    async def setup(self):
        """Initialize test session and authenticate"""
        self.session = aiohttp.ClientSession()
        
        # Register and login test user
        await self.register_test_user()
        await self.login_test_user()
        
    async def teardown(self):
        """Clean up test session"""
        if self.session:
            await self.session.close()
    
    async def register_test_user(self):
        """Register a test user"""
        try:
            register_data = {
                "email": TEST_USER_EMAIL,
                "password": TEST_USER_PASSWORD,
                "full_name": "Test User"
            }
            
            async with self.session.post(f"{BASE_URL}/auth/register", json=register_data) as response:
                if response.status in [200, 201]:
                    print("✅ Test user registered successfully")
                elif response.status == 400:
                    # User might already exist
                    print("ℹ️ Test user already exists")
                else:
                    print(f"⚠️ Registration failed with status {response.status}")
        except Exception as e:
            print(f"⚠️ Registration error: {e}")
    
    async def login_test_user(self):
        """Login test user and get auth token"""
        try:
            login_data = {
                "email": TEST_USER_EMAIL,
                "password": TEST_USER_PASSWORD
            }
            
            async with self.session.post(f"{BASE_URL}/auth/login", json=login_data) as response:
                if response.status == 200:
                    result = await response.json()
                    self.auth_token = result.get("access_token")
                    # Decode user info from token (simplified)
                    self.user_id = "test-user-id"
                    print("✅ Test user logged in successfully")
                    return True
                else:
                    print(f"❌ Login failed with status {response.status}")
                    return False
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    def get_auth_headers(self) -> Dict[str, str]:
        """Get authorization headers"""
        if not self.auth_token:
            return {}
        return {"Authorization": f"Bearer {self.auth_token}"}
    
    async def test_get_razorpay_key(self):
        """Test 1: Get Razorpay public key"""
        print("\n🧪 Test 1: Get Razorpay Public Key")
        try:
            async with self.session.get(f"{BASE_URL}/payment/razorpay-key") as response:
                if response.status == 200:
                    result = await response.json()
                    key = result.get("key")
                    if key and key.startswith("rzp_test_"):
                        print(f"✅ Razorpay key retrieved: {key}")
                        self.test_results.append({"test": "Get Razorpay Key", "status": "PASS", "details": f"Key: {key}"})
                        return True
                    else:
                        print(f"❌ Invalid key format: {key}")
                        self.test_results.append({"test": "Get Razorpay Key", "status": "FAIL", "details": f"Invalid key: {key}"})
                        return False
                else:
                    print(f"❌ Failed with status {response.status}")
                    self.test_results.append({"test": "Get Razorpay Key", "status": "FAIL", "details": f"HTTP {response.status}"})
                    return False
        except Exception as e:
            print(f"❌ Error: {e}")
            self.test_results.append({"test": "Get Razorpay Key", "status": "FAIL", "details": str(e)})
            return False
    
    async def test_get_plans(self):
        """Test 2: Get available plans"""
        print("\n🧪 Test 2: Get Available Plans")
        try:
            async with self.session.get(f"{BASE_URL}/payment/plans") as response:
                if response.status == 200:
                    plans = await response.json()
                    if isinstance(plans, list) and len(plans) > 0:
                        print(f"✅ Retrieved {len(plans)} plans")
                        for plan in plans:
                            print(f"   - {plan.get('name')}: ₹{plan.get('price')} for {plan.get('credits')} credits")
                        self.test_results.append({"test": "Get Plans", "status": "PASS", "details": f"{len(plans)} plans retrieved"})
                        return plans
                    else:
                        print("❌ No plans found")
                        self.test_results.append({"test": "Get Plans", "status": "FAIL", "details": "No plans found"})
                        return []
                else:
                    print(f"❌ Failed with status {response.status}")
                    self.test_results.append({"test": "Get Plans", "status": "FAIL", "details": f"HTTP {response.status}"})
                    return []
        except Exception as e:
            print(f"❌ Error: {e}")
            self.test_results.append({"test": "Get Plans", "status": "FAIL", "details": str(e)})
            return []
    
    async def test_create_payment_order(self, plan_data: Dict[str, Any]):
        """Test 3: Create payment order"""
        print("\n🧪 Test 3: Create Payment Order")
        
        # Create a separate test user for order creation to avoid rate limiting
        order_email = f"order_test_{int(time.time())}@example.com"
        order_password = "OrderTest123!"
        
        try:
            # Register order test user
            register_data = {
                "email": order_email,
                "password": order_password,
                "full_name": "Order Test User"
            }
            
            async with self.session.post(f"{BASE_URL}/auth/register", json=register_data) as response:
                if response.status in [200, 201]:
                    # Login with order user
                    login_data = {"email": order_email, "password": order_password}
                    async with self.session.post(f"{BASE_URL}/auth/login", json=login_data) as login_response:
                        if login_response.status == 200:
                            result = await login_response.json()
                            order_token = result.get("access_token")
                            headers = {"Authorization": f"Bearer {order_token}"}
                            print("   Using separate order test user")
                        else:
                            headers = self.get_auth_headers()
                            print("   Using main test user")
                else:
                    headers = self.get_auth_headers()
                    print("   Using main test user")
        except:
            headers = self.get_auth_headers()
            print("   Using main test user")
        
        try:
            order_data = {
                "plan_name": plan_data.get("name", "Starter"),
                "amount": plan_data.get("price", 25.0),
                "credits": plan_data.get("credits", 1000)
            }
            async with self.session.post(f"{BASE_URL}/payment/create-order", json=order_data, headers=headers) as response:
                if response.status == 200:
                    transaction = await response.json()
                    razorpay_order_id = transaction.get("razorpay_order_id")
                    transaction_id = transaction.get("id")
                    
                    if razorpay_order_id and transaction_id:
                        print(f"✅ Order created successfully")
                        print(f"   Transaction ID: {transaction_id}")
                        print(f"   Razorpay Order ID: {razorpay_order_id}")
                        self.test_results.append({"test": "Create Payment Order", "status": "PASS", "details": f"Transaction: {transaction_id}"})
                        return transaction
                    else:
                        print("❌ Missing order details in response")
                        self.test_results.append({"test": "Create Payment Order", "status": "FAIL", "details": "Missing order details"})
                        return None
                else:
                    error_text = await response.text()
                    print(f"❌ Failed with status {response.status}: {error_text}")
                    self.test_results.append({"test": "Create Payment Order", "status": "FAIL", "details": f"HTTP {response.status}: {error_text}"})
                    return None
        except Exception as e:
            print(f"❌ Error: {e}")
            self.test_results.append({"test": "Create Payment Order", "status": "FAIL", "details": str(e)})
            return None
    
    async def test_payment_rate_limiting(self):
        """Test 4: Payment rate limiting"""
        print("\n🧪 Test 4: Payment Rate Limiting")
        try:
            order_data = {
                "plan_name": "Starter",
                "amount": 25.0,
                "credits": 1000
            }
            
            headers = self.get_auth_headers()
            rate_limited = False
            
            # Try to create 12 orders rapidly (limit is 10 per hour)
            for i in range(12):
                async with self.session.post(f"{BASE_URL}/payment/create-order", json=order_data, headers=headers) as response:
                    if response.status == 429:
                        error_text = await response.text()
                        print(f"✅ Rate limiting triggered at attempt {i+1}")
                        print(f"   Error: {error_text}")
                        rate_limited = True
                        break
                    elif response.status != 200:
                        print(f"⚠️ Unexpected error at attempt {i+1}: {response.status}")
                        break
                
                # Small delay between requests
                await asyncio.sleep(0.1)
            
            if rate_limited:
                self.test_results.append({"test": "Payment Rate Limiting", "status": "PASS", "details": "Rate limiting working correctly"})
                return True
            else:
                print("❌ Rate limiting not triggered")
                self.test_results.append({"test": "Payment Rate Limiting", "status": "FAIL", "details": "Rate limiting not triggered"})
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            self.test_results.append({"test": "Payment Rate Limiting", "status": "FAIL", "details": str(e)})
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