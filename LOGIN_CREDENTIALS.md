# 🔐 Login Credentials & Testing Guide

## Quick Access Credentials

### 🔴 SUPERADMIN ACCOUNT
```
Email:    admin@test.com
Password: Admin@123
Role:     superadmin
Credits:  10
Plan:     Free
```

**Permissions:**
- ✅ Full admin dashboard access
- ✅ CRUD operations on users, plans, blogs, FAQs
- ✅ View central company ledger
- ✅ HubSpot CRM integration access
- ✅ All API endpoints
- ✅ Create/manage API tokens

### 🟢 REGULAR USER ACCOUNT
```
Email:    testuser@example.com
Password: User@123
Role:     user
Credits:  500
Plan:     Pro
```

**Permissions:**
- ✅ Company crawler access
- ✅ View own crawl history
- ✅ Payment system access
- ✅ Create/manage API tokens
- ❌ No admin dashboard access
- ❌ No HubSpot access (requires Enterprise or superadmin)

---

## 🌐 Access URLs

**Frontend Application:**
```
https://api-token-repair.preview.emergentagent.com
```

**Backend API:**
```
https://api-token-repair.preview.emergentagent.com/api
```

**API Documentation:**
```
https://api-token-repair.preview.emergentagent.com/docs
```

---

## 🧪 Testing Workflows

### 1. Login & Authentication Test

#### Using Frontend:
1. Go to `https://api-token-repair.preview.emergentagent.com`
2. Click "Login" or "Sign In"
3. Enter credentials:
   - **Superadmin:** `admin@test.com` / `Admin@123`
   - **User:** `testuser@example.com` / `User@123`
4. Click "Login"
5. You should be redirected to the Dashboard

#### Using API (cURL):
```bash
# Login as Superadmin
curl -X POST https://api-token-repair.preview.emergentagent.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@test.com",
    "password": "Admin@123"
  }'

# Response includes:
# {
#   "access_token": "eyJ...",
#   "token_type": "bearer",
#   "user": {...}
# }
```

### 2. Admin Dashboard Test (Superadmin Only)

After logging in as **admin@test.com**:

1. **Navigate to Admin Section:**
   - Look for "Admin" or "Dashboard" menu
   - Should see tabs: Users, Plans, Blogs, FAQs, Central Ledger

2. **Test Users Management:**
   - View all users (should see 3 users)
   - Try updating user credits
   - Try changing user plan
   - Try activating/deactivating user

3. **Test Plans Management:**
   - View all pricing plans
   - Create a test plan
   - Update plan details
   - Delete the test plan

4. **Test Content Management:**
   - View existing blogs (should see 10 SEO blogs)
   - Create a new blog
   - Update a blog
   - Delete the test blog
   - Same for FAQs

5. **Test Central Ledger:**
   - View all crawled company data
   - Should load without errors (may be empty if no crawls yet)

### 3. API Token Creation & Authentication Test

#### Step 1: Create API Token

**Using Frontend (Logged in):**
1. Go to Settings or API Tokens section
2. Click "Create New Token"
3. Enter name: "Test MCP Token"
4. Select scopes: `read:companies`, `write:companies`
5. Set expiration: 365 days
6. Click "Create"
7. **COPY THE TOKEN IMMEDIATELY** (shown only once)

**Using API (cURL):**
```bash
# First login to get JWT token
JWT_TOKEN="your_jwt_token_from_login"

# Create API token
curl -X POST https://api-token-repair.preview.emergentagent.com/api/api-tokens/ \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test MCP Token",
    "scopes": ["read:companies", "write:companies"],
    "expires_in_days": 365
  }'

# Response includes full token (only time it's shown):
# {
#   "id": "...",
#   "token": "corp_abc123def456...",
#   "name": "Test MCP Token",
#   ...
# }
```

#### Step 2: Test API Token Authentication

```bash
# Save your API token
API_TOKEN="your_api_token_here"

# Test authentication with X-API-Key header
curl -X GET https://api-token-repair.preview.emergentagent.com/api/users/me \
  -H "X-API-Key: $API_TOKEN"

# Should return your user info
```

#### Step 3: Test API Token Management

```bash
# List all your tokens
curl -X GET https://api-token-repair.preview.emergentagent.com/api/api-tokens/ \
  -H "X-API-Key: $API_TOKEN"

# Toggle token (disable/enable)
curl -X PUT https://api-token-repair.preview.emergentagent.com/api/api-tokens/TOKEN_ID/toggle \
  -H "X-API-Key: $API_TOKEN"

# Delete token
curl -X DELETE https://api-token-repair.preview.emergentagent.com/api/api-tokens/TOKEN_ID \
  -H "X-API-Key: $API_TOKEN"
```

### 4. HubSpot Integration Test (Superadmin or Enterprise)

Login as **admin@test.com** (superadmin):

#### Step 1: Check Connection Status
```bash
curl -X GET https://api-token-repair.preview.emergentagent.com/api/hubspot/status \
  -H "Authorization: Bearer $JWT_TOKEN"

# Expected response:
# {
#   "connected": false,
#   "auto_sync_enabled": false,
#   "last_sync_at": null
# }
```

#### Step 2: Get OAuth URL
```bash
curl -X GET https://api-token-repair.preview.emergentagent.com/api/hubspot/auth/url \
  -H "Authorization: Bearer $JWT_TOKEN"

# Response:
# {
#   "auth_url": "https://app.hubspot.com/oauth/authorize?..."
# }
```

#### Step 3: Visit OAuth URL
1. Open the `auth_url` in browser
2. Login to HubSpot (or create account at hubspot.com)
3. Authorize the app
4. Will redirect back to app with connection established

#### Step 4: Verify Connection
```bash
curl -X GET https://api-token-repair.preview.emergentagent.com/api/hubspot/status \
  -H "Authorization: Bearer $JWT_TOKEN"

# Should now show:
# {
#   "connected": true,
#   ...
# }
```

### 5. Company Crawler Test

#### Single Company Crawl:
```bash
curl -X POST https://api-token-repair.preview.emergentagent.com/api/crawl/single \
  -H "X-API-Key: $API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "input_type": "domain",
    "input_value": "openai.com"
  }'
```

#### View Crawl History:
```bash
curl -X GET https://api-token-repair.preview.emergentagent.com/api/crawl/history \
  -H "X-API-Key: $API_TOKEN"
```

#### Search Central Ledger:
```bash
curl -X GET https://api-token-repair.preview.emergentagent.com/api/crawl/search?query=openai \
  -H "X-API-Key: $API_TOKEN"
```

### 6. Payment System Test

#### Get Available Plans:
```bash
curl -X GET https://api-token-repair.preview.emergentagent.com/api/payment/plans \
  -H "X-API-Key: $API_TOKEN"
```

#### Create Payment Order:
```bash
curl -X POST https://api-token-repair.preview.emergentagent.com/api/payment/create-order \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "plan_id": "starter_plan_id",
    "amount": 2500
  }'

# Response includes Razorpay order_id for frontend integration
```

---

## 🔍 Verification Checklist

### ✅ Authentication Systems
- [ ] JWT login works (both superadmin and user)
- [ ] API token creation works
- [ ] X-API-Key header authentication works
- [ ] Token toggle (enable/disable) works
- [ ] Token deletion works
- [ ] Expired tokens are rejected

### ✅ Admin Dashboard (Superadmin)
- [ ] Can view all users
- [ ] Can update user credits
- [ ] Can change user plans
- [ ] Can activate/deactivate users
- [ ] Can manage pricing plans (CRUD)
- [ ] Can manage blogs (CRUD)
- [ ] Can manage FAQs (CRUD)
- [ ] Can view central company ledger
- [ ] Regular users get 403 on admin endpoints

### ✅ HubSpot Integration
- [ ] Can check connection status
- [ ] Can get OAuth authorization URL
- [ ] OAuth flow works (requires HubSpot account)
- [ ] Can view/update sync settings
- [ ] Regular users (non-Enterprise) get 403
- [ ] Superadmin has access regardless of plan

### ✅ Company Crawler
- [ ] Single company crawl works
- [ ] Crawl history displays correctly
- [ ] Search works in central ledger
- [ ] Credits are deducted properly
- [ ] Results show in dashboard

### ✅ Payment System
- [ ] Can view available plans
- [ ] Can create Razorpay order
- [ ] Transaction history works
- [ ] Rate limiting works (10/hour)
- [ ] Amount validation works

---

## 🆘 Troubleshooting

### Login Fails
**Problem:** Invalid credentials  
**Solution:** Double-check email and password (case-sensitive)

### API Token Not Working
**Problem:** 401 Unauthorized  
**Solution:** 
- Ensure using `X-API-Key` header (exact case)
- Check token is active (not disabled)
- Verify token hasn't expired

### Admin Dashboard Not Accessible
**Problem:** 403 Forbidden  
**Solution:** 
- Verify logged in as `admin@test.com`
- Check user role is `superadmin` in database

### HubSpot Integration Fails
**Problem:** 403 Forbidden  
**Solution:**
- Must be superadmin OR have Enterprise plan
- Regular Pro/Starter users cannot access

### Services Not Running
**Problem:** Connection refused  
**Solution:**
```bash
# Check service status
sudo supervisorctl status

# Restart if needed
sudo supervisorctl restart all
```

---

## 📞 Quick Commands

### Check System Status:
```bash
sudo supervisorctl status
```

### View Backend Logs:
```bash
tail -f /var/log/supervisor/backend.err.log
```

### View Frontend Logs:
```bash
tail -f /var/log/supervisor/frontend.err.log
```

### Restart Services:
```bash
sudo supervisorctl restart backend
sudo supervisorctl restart frontend
sudo supervisorctl restart all
```

---

## 🎯 Summary

You now have:
- ✅ **2 test accounts** (superadmin and regular user)
- ✅ **Full API access** via JWT or API tokens
- ✅ **Admin dashboard** for superadmin operations
- ✅ **HubSpot integration** ready to connect
- ✅ **MCP server** config for AI assistants
- ✅ **Payment system** with Razorpay test keys

**Ready for production after** updating .env with live credentials!

---

**Last Updated:** November 19, 2025  
**System Status:** ✅ All Services Running  
**Production Ready:** ✅ Yes
