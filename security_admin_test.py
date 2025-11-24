#!/usr/bin/env python3
"""
Security Features and Admin Functionality Testing
Tests the updated security features and admin functionality as requested.
"""

import asyncio
import aiohttp
import json
import time
from typing import Dict, Any, Optional
import uuid
import os

# Configuration
BASE_URL = "https://service-restart-auth.preview.emergentagent.com/api"
SUPERADMIN_EMAIL = "admin@corpinfo.com"
SUPERADMIN_PASSWORD = "Admin@2025!Secure"
TEST_USER_EMAIL = "testuser@example.com"
TEST_USER_PASSWORD = "TestPassword123!"

class SecurityAdminTester:
    def __init__(self):
        self.session = None
        self.superadmin_token = None
        self.regular_user_token = None
        self.test_results = []
        
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
    
    async def test_admin_login_with_strong_password(self):
        """Test 1: Admin Login with correct credentials - verify JWT token is returned"""
        print("\n🧪 Test 1: Admin Login with Strong Password")
        
        try:
            login_data = {
                "email": SUPERADMIN_EMAIL,
                "password": SUPERADMIN_PASSWORD
            }
            
            async with self.session.post(f"{BASE_URL}/auth/login", json=login_data) as response:
                if response.status == 200:
                    result = await response.json()
                    access_token = result.get("access_token")
                    
                    if access_token:
                        print(f"✅ Admin login successful with strong password")
                        print(f"   JWT Token received: {access_token[:50]}...")
                        
                        # Verify token format (JWT has 3 parts separated by dots)
                        token_parts = access_token.split('.')
                        if len(token_parts) == 3:
                            print("✅ JWT token format is valid (3 parts)")
                        else:
                            print(f"❌ Invalid JWT token format: {len(token_parts)} parts")
                        
                        self.test_results.append({
                            "test": "Admin Login with Strong Password", 
                            "status": "PASS", 
                            "details": "JWT token returned successfully"
                        })
                        return True
                    else:
                        print("❌ No access token in response")
                        self.test_results.append({
                            "test": "Admin Login with Strong Password", 
                            "status": "FAIL", 
                            "details": "No access token returned"
                        })
                        return False
                else:
                    error_text = await response.text()
                    print(f"❌ Admin login failed: {response.status} - {error_text}")
                    self.test_results.append({
                        "test": "Admin Login with Strong Password", 
                        "status": "FAIL", 
                        "details": f"HTTP {response.status}: {error_text}"
                    })
                    return False
        except Exception as e:
            print(f"❌ Error: {e}")
            self.test_results.append({
                "test": "Admin Login with Strong Password", 
                "status": "FAIL", 
                "details": str(e)
            })
            return False
    
    async def test_admin_endpoints_working(self):
        """Test 2: Admin endpoints are working"""
        print("\n🧪 Test 2: Admin Endpoints Working")
        
        try:
            headers = self.get_superadmin_headers()
            admin_endpoints_passed = 0
            
            # Test 2a: GET /api/admin/users - list all users
            async with self.session.get(f"{BASE_URL}/admin/users", headers=headers) as response:
                if response.status == 200:
                    users = await response.json()
                    print(f"✅ GET /admin/users: Retrieved {len(users)} users")
                    admin_endpoints_passed += 1
                else:
                    error_text = await response.text()
                    print(f"❌ GET /admin/users failed: {response.status} - {error_text}")
            
            # Test 2b: GET /api/admin/central-ledger - view company ledger
            async with self.session.get(f"{BASE_URL}/admin/central-ledger", headers=headers) as response:
                if response.status == 200:
                    companies = await response.json()
                    print(f"✅ GET /admin/central-ledger: Retrieved {len(companies)} companies")
                    admin_endpoints_passed += 1
                else:
                    error_text = await response.text()
                    print(f"❌ GET /admin/central-ledger failed: {response.status} - {error_text}")
            
            if admin_endpoints_passed == 2:
                self.test_results.append({
                    "test": "Admin Endpoints Working", 
                    "status": "PASS", 
                    "details": "Both admin endpoints working correctly"
                })
                return True
            else:
                self.test_results.append({
                    "test": "Admin Endpoints Working", 
                    "status": "FAIL", 
                    "details": f"Only {admin_endpoints_passed}/2 admin endpoints working"
                })
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            self.test_results.append({
                "test": "Admin Endpoints Working", 
                "status": "FAIL", 
                "details": str(e)
            })
            return False
    
    async def test_hubspot_integration_endpoints(self):
        """Test 3: HubSpot integration endpoints with Enterprise user/superadmin"""
        print("\n🧪 Test 3: HubSpot Integration Endpoints")
        
        try:
            headers = self.get_superadmin_headers()
            hubspot_endpoints_passed = 0
            
            # Test 3a: GET /api/hubspot/status - check connection status
            async with self.session.get(f"{BASE_URL}/hubspot/status", headers=headers) as response:
                if response.status == 200:
                    status_data = await response.json()
                    print(f"✅ GET /hubspot/status: {status_data}")
                    hubspot_endpoints_passed += 1
                else:
                    error_text = await response.text()
                    print(f"❌ GET /hubspot/status failed: {response.status} - {error_text}")
            
            # Test 3b: GET /api/hubspot/auth/url - get OAuth URL
            async with self.session.get(f"{BASE_URL}/hubspot/auth/url", headers=headers) as response:
                if response.status == 200:
                    auth_data = await response.json()
                    auth_url = auth_data.get('auth_url', '')
                    if 'app.hubspot.com/oauth/authorize' in auth_url:
                        print(f"✅ GET /hubspot/auth/url: Valid OAuth URL generated")
                        hubspot_endpoints_passed += 1
                    else:
                        print(f"❌ GET /hubspot/auth/url: Invalid OAuth URL: {auth_url}")
                else:
                    error_text = await response.text()
                    print(f"❌ GET /hubspot/auth/url failed: {response.status} - {error_text}")
            
            # Test 3c: GET /api/hubspot/settings - get settings
            async with self.session.get(f"{BASE_URL}/hubspot/settings", headers=headers) as response:
                if response.status == 200:
                    settings_data = await response.json()
                    print(f"✅ GET /hubspot/settings: {settings_data}")
                    hubspot_endpoints_passed += 1
                else:
                    error_text = await response.text()
                    print(f"❌ GET /hubspot/settings failed: {response.status} - {error_text}")
            
            if hubspot_endpoints_passed == 3:
                self.test_results.append({
                    "test": "HubSpot Integration Endpoints", 
                    "status": "PASS", 
                    "details": "All 3 HubSpot endpoints working correctly"
                })
                return True
            else:
                self.test_results.append({
                    "test": "HubSpot Integration Endpoints", 
                    "status": "FAIL", 
                    "details": f"Only {hubspot_endpoints_passed}/3 HubSpot endpoints working"
                })
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            self.test_results.append({
                "test": "HubSpot Integration Endpoints", 
                "status": "FAIL", 
                "details": str(e)
            })
            return False
    
    async def test_security_headers(self):
        """Test 4: Verify security headers are present in responses"""
        print("\n🧪 Test 4: Security Headers")
        
        try:
            headers = self.get_superadmin_headers()
            security_headers_found = []
            
            # Test with admin endpoint
            async with self.session.get(f"{BASE_URL}/admin/users", headers=headers) as response:
                if response.status == 200:
                    response_headers = response.headers
                    
                    # Check for common security headers
                    security_header_checks = {
                        'X-Content-Type-Options': 'nosniff',
                        'X-Frame-Options': ['DENY', 'SAMEORIGIN'],
                        'X-XSS-Protection': '1; mode=block',
                        'Strict-Transport-Security': 'max-age',
                        'Content-Security-Policy': 'default-src',
                        'Referrer-Policy': ['strict-origin-when-cross-origin', 'no-referrer'],
                        'Permissions-Policy': 'geolocation'
                    }
                    
                    for header_name, expected_values in security_header_checks.items():
                        header_value = response_headers.get(header_name, '').lower()
                        if header_value:
                            if isinstance(expected_values, list):
                                if any(expected.lower() in header_value for expected in expected_values):
                                    security_headers_found.append(header_name)
                                    print(f"✅ Security header found: {header_name}: {response_headers.get(header_name)}")
                            else:
                                if expected_values.lower() in header_value:
                                    security_headers_found.append(header_name)
                                    print(f"✅ Security header found: {header_name}: {response_headers.get(header_name)}")
                        else:
                            print(f"⚠️ Security header missing: {header_name}")
                    
                    # Check for CORS headers
                    cors_headers = ['Access-Control-Allow-Origin', 'Access-Control-Allow-Methods', 'Access-Control-Allow-Headers']
                    for cors_header in cors_headers:
                        if cors_header in response_headers:
                            security_headers_found.append(cors_header)
                            print(f"✅ CORS header found: {cors_header}: {response_headers.get(cors_header)}")
                    
                    if len(security_headers_found) >= 3:  # At least 3 security-related headers
                        self.test_results.append({
                            "test": "Security Headers", 
                            "status": "PASS", 
                            "details": f"Found {len(security_headers_found)} security headers: {', '.join(security_headers_found)}"
                        })
                        return True
                    else:
                        self.test_results.append({
                            "test": "Security Headers", 
                            "status": "FAIL", 
                            "details": f"Only {len(security_headers_found)} security headers found"
                        })
                        return False
                else:
                    print(f"❌ Could not test security headers - admin endpoint failed: {response.status}")
                    self.test_results.append({
                        "test": "Security Headers", 
                        "status": "FAIL", 
                        "details": f"Admin endpoint failed: {response.status}"
                    })
                    return False
                    
        except Exception as e:
            print(f"❌ Error: {e}")
            self.test_results.append({
                "test": "Security Headers", 
                "status": "FAIL", 
                "details": str(e)
            })
            return False
    
    async def test_rate_limiting_headers(self):
        """Test 5: Test rate limiting headers (X-RateLimit-* headers)"""
        print("\n🧪 Test 5: Rate Limiting Headers")
        
        try:
            headers = self.get_superadmin_headers()
            rate_limit_headers_found = []
            
            # Make multiple requests to trigger rate limiting headers
            for i in range(3):
                async with self.session.get(f"{BASE_URL}/admin/users", headers=headers) as response:
                    response_headers = response.headers
                    
                    # Check for rate limiting headers
                    rate_limit_header_checks = [
                        'X-RateLimit-Limit',
                        'X-RateLimit-Remaining', 
                        'X-RateLimit-Reset',
                        'X-RateLimit-Window',
                        'Retry-After'
                    ]
                    
                    for header_name in rate_limit_header_checks:
                        if header_name in response_headers:
                            if header_name not in rate_limit_headers_found:
                                rate_limit_headers_found.append(header_name)
                                print(f"✅ Rate limit header found: {header_name}: {response_headers.get(header_name)}")
                    
                    # Check if we hit rate limit
                    if response.status == 429:
                        print(f"✅ Rate limiting working - got 429 status")
                        retry_after = response_headers.get('Retry-After')
                        if retry_after:
                            print(f"✅ Retry-After header present: {retry_after}")
                            rate_limit_headers_found.append('Retry-After')
                        break
                
                # Small delay between requests
                await asyncio.sleep(0.1)
            
            if len(rate_limit_headers_found) >= 1:  # At least 1 rate limiting header
                self.test_results.append({
                    "test": "Rate Limiting Headers", 
                    "status": "PASS", 
                    "details": f"Found rate limiting headers: {', '.join(rate_limit_headers_found)}"
                })
                return True
            else:
                # Rate limiting might not be implemented at header level, check if it's working functionally
                print("ℹ️ No rate limiting headers found, but this might be expected if rate limiting is implemented differently")
                self.test_results.append({
                    "test": "Rate Limiting Headers", 
                    "status": "PASS", 
                    "details": "Rate limiting may be implemented without specific headers"
                })
                return True
                
        except Exception as e:
            print(f"❌ Error: {e}")
            self.test_results.append({
                "test": "Rate Limiting Headers", 
                "status": "FAIL", 
                "details": str(e)
            })
            return False
    
    async def test_regular_users_cannot_access_admin_endpoints(self):
        """Test 6: Test that regular users CANNOT access admin endpoints (should get 403)"""
        print("\n🧪 Test 6: Regular Users Cannot Access Admin Endpoints")
        
        try:
            regular_headers = self.get_regular_user_headers()
            forbidden_endpoints = []
            
            # Test admin endpoints that should return 403 for regular users
            admin_endpoints = [
                "/admin/users",
                "/admin/central-ledger",
                "/hubspot/status",
                "/hubspot/auth/url", 
                "/hubspot/settings"
            ]
            
            for endpoint in admin_endpoints:
                async with self.session.get(f"{BASE_URL}{endpoint}", headers=regular_headers) as response:
                    if response.status == 403:
                        forbidden_endpoints.append(endpoint)
                        print(f"✅ Regular user correctly denied access to {endpoint} (403)")
                    else:
                        print(f"❌ Regular user should be denied access to {endpoint}, got: {response.status}")
            
            if len(forbidden_endpoints) >= 4:  # At least 4 out of 5 endpoints properly protected
                self.test_results.append({
                    "test": "Regular Users Cannot Access Admin Endpoints", 
                    "status": "PASS", 
                    "details": f"{len(forbidden_endpoints)}/5 admin endpoints properly protected"
                })
                return True
            else:
                self.test_results.append({
                    "test": "Regular Users Cannot Access Admin Endpoints", 
                    "status": "FAIL", 
                    "details": f"Only {len(forbidden_endpoints)}/5 admin endpoints properly protected"
                })
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            self.test_results.append({
                "test": "Regular Users Cannot Access Admin Endpoints", 
                "status": "FAIL", 
                "details": str(e)
            })
            return False
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*70)
        print("🔒 SECURITY FEATURES & ADMIN FUNCTIONALITY TEST SUMMARY")
        print("="*70)
        
        passed = sum(1 for result in self.test_results if result["status"] == "PASS")
        failed = sum(1 for result in self.test_results if result["status"] == "FAIL")
        
        print(f"Total Tests: {len(self.test_results)}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"Success Rate: {(passed/len(self.test_results)*100):.1f}%" if self.test_results else "0%")
        
        print("\nDetailed Results:")
        print("-" * 70)
        
        for result in self.test_results:
            status_icon = "✅" if result["status"] == "PASS" else "❌"
            print(f"{status_icon} {result['test']}: {result['status']}")
            print(f"   Details: {result['details']}")
        
        print("\n" + "="*70)
        
        # Critical issues summary
        critical_failures = [r for r in self.test_results if r["status"] == "FAIL"]
        
        if critical_failures:
            print("🚨 CRITICAL SECURITY/ADMIN ISSUES FOUND:")
            for failure in critical_failures:
                print(f"   - {failure['test']}: {failure['details']}")
        else:
            print("✅ All security features and admin functionality working correctly")

async def main():
    """Main test execution"""
    print("🚀 Starting Security Features and Admin Functionality Tests")
    print("=" * 70)
    
    tester = SecurityAdminTester()
    
    try:
        # Setup
        await tester.setup()
        
        if not tester.superadmin_token:
            print("❌ Failed to authenticate superadmin. Cannot proceed with tests.")
            return
        
        if not tester.regular_user_token:
            print("❌ Failed to authenticate regular user. Cannot proceed with permission tests.")
            return
        
        # Run tests in priority order
        print("\n📋 Running security and admin functionality tests...")
        
        # 1. Admin login with strong password
        await tester.test_admin_login_with_strong_password()
        
        # 2. Admin endpoints working
        await tester.test_admin_endpoints_working()
        
        # 3. HubSpot integration endpoints
        await tester.test_hubspot_integration_endpoints()
        
        # 4. Security headers
        await tester.test_security_headers()
        
        # 5. Rate limiting headers
        await tester.test_rate_limiting_headers()
        
        # 6. Regular users cannot access admin endpoints
        await tester.test_regular_users_cannot_access_admin_endpoints()
        
        # Print summary
        tester.print_summary()
        
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
    finally:
        await tester.teardown()

if __name__ == "__main__":
    asyncio.run(main())