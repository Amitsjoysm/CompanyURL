"""
Test script to verify admin CRUD capabilities
"""
import requests
import json
from typing import Optional

BASE_URL = "http://localhost:8001/api"  # Backend runs on 8001
ADMIN_EMAIL = "admin@corpinfo.com"
ADMIN_PASSWORD = "Admin@2025!Secure"

class AdminTester:
    def __init__(self):
        self.token: Optional[str] = None
        self.headers: dict = {}
    
    def test_admin_login(self) -> bool:
        """Test admin login"""
        print("\n=== Testing Admin Login ===")
        try:
            response = requests.post(
                f"{BASE_URL}/auth/login",
                json={
                    "email": ADMIN_EMAIL,
                    "password": ADMIN_PASSWORD
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data["access_token"]
                self.headers = {"Authorization": f"Bearer {self.token}"}
                print(f"✅ Admin login successful")
                print(f"   User: {data['user']['email']}")
                print(f"   Role: {data['user']['role']}")
                return True
            else:
                print(f"❌ Login failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Login error: {str(e)}")
            return False
    
    def test_get_users(self) -> bool:
        """Test GET all users"""
        print("\n=== Testing GET /admin/users ===")
        try:
            response = requests.get(
                f"{BASE_URL}/admin/users",
                headers=self.headers
            )
            
            if response.status_code == 200:
                users = response.json()
                print(f"✅ Retrieved {len(users)} users")
                for user in users[:3]:  # Show first 3
                    print(f"   - {user['email']} ({user['role']}) - Plan: {user.get('current_plan', 'N/A')}")
                return True
            else:
                print(f"❌ Failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    def test_get_plans(self) -> bool:
        """Test GET all plans"""
        print("\n=== Testing GET /plans ===")
        try:
            response = requests.get(
                f"{BASE_URL}/payment/plans",
                headers=self.headers
            )
            
            if response.status_code == 200:
                plans = response.json()
                print(f"✅ Retrieved {len(plans)} plans")
                for plan in plans:
                    print(f"   - {plan['name']}: ${plan['price']} ({plan['credits']} credits)")
                return True
            else:
                print(f"❌ Failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    def test_get_central_ledger(self) -> bool:
        """Test GET central ledger"""
        print("\n=== Testing GET /admin/central-ledger ===")
        try:
            response = requests.get(
                f"{BASE_URL}/admin/central-ledger?limit=5",
                headers=self.headers
            )
            
            if response.status_code == 200:
                companies = response.json()
                print(f"✅ Retrieved {len(companies)} companies from central ledger")
                for company in companies[:3]:
                    print(f"   - {company.get('name', 'N/A')} ({company.get('domain', 'N/A')})")
                return True
            else:
                print(f"❌ Failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    def test_create_plan(self) -> Optional[str]:
        """Test POST /admin/plans"""
        print("\n=== Testing POST /admin/plans (Create) ===")
        try:
            response = requests.post(
                f"{BASE_URL}/admin/plans",
                headers=self.headers,
                json={
                    "name": "Test Plan",
                    "price": 75.0,
                    "credits": 3500,
                    "is_active": True
                }
            )
            
            if response.status_code == 200:
                plan = response.json()
                print(f"✅ Created plan: {plan['name']}")
                print(f"   ID: {plan['id']}")
                print(f"   Price: ${plan['price']}")
                print(f"   Credits: {plan['credits']}")
                return plan['id']
            else:
                print(f"❌ Failed: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return None
    
    def test_update_plan(self, plan_id: str) -> bool:
        """Test PUT /admin/plans/{plan_id}"""
        print("\n=== Testing PUT /admin/plans/{plan_id} (Update) ===")
        try:
            response = requests.put(
                f"{BASE_URL}/admin/plans/{plan_id}",
                headers=self.headers,
                json={
                    "price": 79.99,
                    "credits": 4000
                }
            )
            
            if response.status_code == 200:
                plan = response.json()
                print(f"✅ Updated plan: {plan['name']}")
                print(f"   New Price: ${plan['price']}")
                print(f"   New Credits: {plan['credits']}")
                return True
            else:
                print(f"❌ Failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    def test_delete_plan(self, plan_id: str) -> bool:
        """Test DELETE /admin/plans/{plan_id}"""
        print("\n=== Testing DELETE /admin/plans/{plan_id} ===")
        try:
            response = requests.delete(
                f"{BASE_URL}/admin/plans/{plan_id}",
                headers=self.headers
            )
            
            if response.status_code == 200:
                print(f"✅ Deleted plan successfully")
                return True
            else:
                print(f"❌ Failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    def test_get_blogs(self) -> bool:
        """Test GET blogs"""
        print("\n=== Testing GET /blogs ===")
        try:
            response = requests.get(f"{BASE_URL}/content/blogs")
            
            if response.status_code == 200:
                blogs = response.json()
                print(f"✅ Retrieved {len(blogs)} blogs")
                for blog in blogs[:3]:
                    print(f"   - {blog['title']}")
                return True
            else:
                print(f"❌ Failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    def test_get_faqs(self) -> bool:
        """Test GET FAQs"""
        print("\n=== Testing GET /faqs ===")
        try:
            response = requests.get(f"{BASE_URL}/content/faqs")
            
            if response.status_code == 200:
                faqs = response.json()
                print(f"✅ Retrieved {len(faqs)} FAQs")
                for faq in faqs[:3]:
                    print(f"   - {faq['question'][:60]}...")
                return True
            else:
                print(f"❌ Failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print("="*70)
        print("ADMIN CAPABILITIES TEST SUITE")
        print("="*70)
        
        results = {}
        
        # Test login
        results['login'] = self.test_admin_login()
        if not results['login']:
            print("\n❌ Cannot proceed without admin login")
            return
        
        # Test Read operations
        results['get_users'] = self.test_get_users()
        results['get_plans'] = self.test_get_plans()
        results['get_ledger'] = self.test_get_central_ledger()
        results['get_blogs'] = self.test_get_blogs()
        results['get_faqs'] = self.test_get_faqs()
        
        # Test Create, Update, Delete for plans
        plan_id = self.test_create_plan()
        if plan_id:
            results['create_plan'] = True
            results['update_plan'] = self.test_update_plan(plan_id)
            results['delete_plan'] = self.test_delete_plan(plan_id)
        else:
            results['create_plan'] = False
            results['update_plan'] = False
            results['delete_plan'] = False
        
        # Summary
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        
        passed = sum(1 for v in results.values() if v)
        total = len(results)
        
        for test, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} - {test}")
        
        print("="*70)
        print(f"TOTAL: {passed}/{total} tests passed ({int(passed/total*100)}%)")
        print("="*70)

if __name__ == "__main__":
    tester = AdminTester()
    tester.run_all_tests()
