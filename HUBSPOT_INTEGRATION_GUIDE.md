# HubSpot CRM Integration Guide for CorpInfo

## Overview
CorpInfo now includes HubSpot CRM integration for **Enterprise plan users** and **Superadmins**. This integration allows you to:
- Push company data from the central ledger to HubSpot Companies
- Push contact data to HubSpot Contacts  
- Configure manual push or auto-sync after crawl events
- Manage sync settings per user

---

## HubSpot OAuth Configuration

### Required Credentials

To set up the HubSpot integration, you need to create an app in HubSpot Developer Portal:

**1. Create HubSpot App:**
   - Visit: https://developers.hubspot.com/
   - Navigate to "Apps" → "Create app"
   - Name your app (e.g., "CorpInfo CRM Sync")

**2. Configure OAuth Settings:**

**Redirect URL (Production):**
```
https://hubspot-crm-sync.preview.emergentagent.com/api/hubspot/callback
```

**Redirect URL (Development):**
```
http://localhost:8000/api/hubspot/callback
```

**Required Scopes:**
- `crm.objects.companies.read` - Read company records
- `crm.objects.companies.write` - Create/update company records
- `crm.objects.contacts.read` - Read contact records
- `crm.objects.contacts.write` - Create/update contact records

**3. Get Your Credentials:**
   - After creating the app, navigate to the "Auth" tab
   - Copy your **Client ID** and **Client Secret**
   - Update `/app/backend/.env` file with these values:

```env
HUBSPOT_CLIENT_ID="your_actual_client_id"
HUBSPOT_CLIENT_SECRET="your_actual_client_secret"
```

---

## Admin Credentials

### Superadmin Account

A superadmin account has been created with full access to all admin features:

**Email:** `admin@corpinfo.com`
**Password:** `Admin@2025!Secure`

⚠️ **IMPORTANT:** Change this password immediately after first login!

### Admin Capabilities

The superadmin can perform CRUD operations on:

1. **Users Management** (`/api/admin/users`)
   - `GET /api/admin/users` - View all users
   - `PUT /api/admin/users/{user_id}/credits` - Update user credits
   - `PUT /api/admin/users/{user_id}/status` - Activate/deactivate user
   - `PUT /api/admin/users/{user_id}/plan` - Update user plan (Free/Starter/Pro/Enterprise)

2. **Plans Management** (`/api/admin/plans`)
   - `POST /api/admin/plans` - Create new pricing plan
   - `PUT /api/admin/plans/{plan_id}` - Update existing plan
   - `DELETE /api/admin/plans/{plan_id}` - Delete plan

3. **Content Management** (`/api/content`)
   - **Blogs:**
     - `GET /api/blogs` - List all blogs
     - `POST /api/blogs` - Create new blog
     - `PUT /api/blogs/{slug}` - Update blog
     - `DELETE /api/blogs/{slug}` - Delete blog
   
   - **FAQs:**
     - `GET /api/faqs` - List all FAQs
     - `POST /api/faqs` - Create new FAQ
     - `PUT /api/faqs/{faq_id}` - Update FAQ
     - `DELETE /api/faqs/{faq_id}` - Delete FAQ

4. **Central Ledger** (`/api/admin/central-ledger`)
   - `GET /api/admin/central-ledger` - View all crawled companies across all users

5. **User Types & Roles**
   - **Roles:** `user`, `superadmin`
   - **Plans:** `Free`, `Starter`, `Pro`, `Enterprise`
   - Only superadmins can access admin endpoints
   - Only Enterprise users and superadmins can access HubSpot CRM features

---

## HubSpot API Endpoints

### Authentication & Status

**1. Get OAuth Authorization URL**
```http
GET /api/hubspot/auth/url
Authorization: Bearer {jwt_token}

Response:
{
  "auth_url": "https://app.hubspot.com/oauth/authorize?..."
}
```

**2. OAuth Callback** (Automatic redirect from HubSpot)
```http
GET /api/hubspot/callback?code={code}&state={state}
```

**3. Check Connection Status**
```http
GET /api/hubspot/status
Authorization: Bearer {jwt_token}

Response:
{
  "connected": true,
  "auto_sync_enabled": false,
  "last_sync_at": "2025-01-19T10:30:00Z"
}
```

**4. Disconnect HubSpot**
```http
DELETE /api/hubspot/disconnect
Authorization: Bearer {jwt_token}
```

### Settings Management

**5. Get Sync Settings**
```http
GET /api/hubspot/settings
Authorization: Bearer {jwt_token}

Response:
{
  "auto_sync_enabled": false,
  "sync_companies": true,
  "sync_contacts": true,
  "last_sync_at": null
}
```

**6. Update Sync Settings**
```http
POST /api/hubspot/settings?auto_sync_enabled=true&sync_companies=true&sync_contacts=true
Authorization: Bearer {jwt_token}

Response:
{
  "message": "Settings updated successfully"
}
```

### Data Synchronization

**7. Manual Company Sync**
```http
POST /api/hubspot/sync/companies
Authorization: Bearer {jwt_token}
Content-Type: application/json

Body:
[
  {
    "name": "Acme Corporation",
    "domain": "acme.com",
    "city": "San Francisco",
    "state": "CA",
    "country": "USA",
    "industry": "Technology",
    "phone": "+1-555-1234",
    "website": "https://acme.com",
    "employee_size": "100-500",
    "description": "Leading tech company"
  }
]

Response:
{
  "success": true,
  "synced_companies": 1,
  "synced_contacts": 0,
  "failed_companies": [],
  "failed_contacts": [],
  "message": "Synced 1 companies, 0 failed"
}
```

**8. Manual Contact Sync**
```http
POST /api/hubspot/sync/contacts
Authorization: Bearer {jwt_token}
Content-Type: application/json

Body:
[
  {
    "email": "john.doe@acme.com",
    "firstname": "John",
    "lastname": "Doe",
    "phone": "+1-555-5678",
    "company": "Acme Corporation",
    "jobtitle": "CEO",
    "lifecyclestage": "customer"
  }
]

Response:
{
  "success": true,
  "synced_companies": 0,
  "synced_contacts": 1,
  "failed_companies": [],
  "failed_contacts": [],
  "message": "Synced 1 contacts, 0 failed"
}
```

---

## User Workflow

### For Enterprise Users

1. **Login to CorpInfo** with your Enterprise account
2. **Navigate to Dashboard** → HubSpot CRM section
3. **Click "Connect HubSpot"** - This initiates OAuth flow
4. **Authorize the app** on HubSpot's consent screen
5. **Configure sync settings:**
   - Enable/disable auto-sync after crawl events
   - Choose what to sync (companies, contacts, or both)
6. **Manual Sync:**
   - Select companies/contacts from your history
   - Click "Push to HubSpot"
7. **Auto-Sync:**
   - When enabled, every successful crawl automatically pushes data to HubSpot
   - Can be toggled on/off anytime

### For Superadmins

1. **Full access to all HubSpot features** (same as Enterprise users)
2. **Can manage user plans:**
   - Upgrade users to Enterprise plan to grant HubSpot access
   - View all user sync activities
3. **Access admin dashboard** at `/admin` to manage:
   - User accounts and plans
   - System-wide settings
   - Central company ledger

---

## Data Mapping

### Company Data → HubSpot Companies

| CorpInfo Field | HubSpot Property |
|---------------|------------------|
| name | name |
| domain | domain |
| city | city |
| state | state |
| country | country |
| industry | industry |
| phone | phone |
| website | website |
| employee_size | employee_size (custom) |
| description | description |

### Contact Data → HubSpot Contacts

| CorpInfo Field | HubSpot Property |
|---------------|------------------|
| email | email (unique identifier) |
| firstname | firstname |
| lastname | lastname |
| phone | phone |
| company | company |
| jobtitle | jobtitle |
| lifecyclestage | lifecyclestage |

---

## Testing Admin CRUD Operations

### Test User Management

```bash
# Get all users
curl -X GET "http://localhost:8000/api/admin/users" \
  -H "Authorization: Bearer {superadmin_token}"

# Update user credits
curl -X PUT "http://localhost:8000/api/admin/users/{user_id}/credits" \
  -H "Authorization: Bearer {superadmin_token}" \
  -H "Content-Type: application/json" \
  -d '{"credits": 5000}'

# Update user plan to Enterprise
curl -X PUT "http://localhost:8000/api/admin/users/{user_id}/plan" \
  -H "Authorization: Bearer {superadmin_token}" \
  -H "Content-Type: application/json" \
  -d '{"current_plan": "Enterprise"}'

# Activate/deactivate user
curl -X PUT "http://localhost:8000/api/admin/users/{user_id}/status" \
  -H "Authorization: Bearer {superadmin_token}" \
  -H "Content-Type: application/json" \
  -d '{"is_active": false}'
```

### Test Plans Management

```bash
# Create new plan
curl -X POST "http://localhost:8000/api/admin/plans" \
  -H "Authorization: Bearer {superadmin_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Custom Plan",
    "price": 99.0,
    "credits": 5000,
    "is_active": true
  }'

# Update plan
curl -X PUT "http://localhost:8000/api/admin/plans/{plan_id}" \
  -H "Authorization: Bearer {superadmin_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "price": 89.0,
    "credits": 6000
  }'

# Delete plan
curl -X DELETE "http://localhost:8000/api/admin/plans/{plan_id}" \
  -H "Authorization: Bearer {superadmin_token}"
```

### Test Content Management

```bash
# Create blog
curl -X POST "http://localhost:8000/api/blogs" \
  -H "Authorization: Bearer {superadmin_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "slug": "test-blog",
    "title": "Test Blog Post",
    "excerpt": "This is a test",
    "content": "Full blog content here",
    "author": "Admin",
    "is_published": true
  }'

# Update blog
curl -X PUT "http://localhost:8000/api/blogs/test-blog" \
  -H "Authorization: Bearer {superadmin_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Test Blog"
  }'

# Delete blog
curl -X DELETE "http://localhost:8000/api/blogs/test-blog" \
  -H "Authorization: Bearer {superadmin_token}"
```

---

## Security & Best Practices

### Environment Variables
- **Never commit `.env` file** to version control
- Store HubSpot credentials securely
- Use HTTPS in production
- Rotate secrets regularly

### Access Control
- HubSpot features only accessible to:
  - Users with `current_plan: "Enterprise"`
  - Users with `role: "superadmin"`
- All admin endpoints require superadmin role
- JWT tokens expire after 7 days

### Rate Limiting
- HubSpot API: 110 requests per 10 seconds
- Batch operations recommended for bulk sync
- Automatic retry with exponential backoff implemented

### Error Handling
- Token refresh automatic before expiration
- Failed sync operations logged for review
- Partial failures handled gracefully
- Users notified of sync status

---

## Troubleshooting

### "HubSpot not connected"
- User needs to complete OAuth flow first
- Check if HubSpot credentials are configured in `.env`
- Verify redirect URL matches HubSpot app settings

### "Access denied"
- User must be on Enterprise plan or be a superadmin
- Admins can update user plan via `/api/admin/users/{user_id}/plan`

### "Failed to sync"
- Check HubSpot API status
- Verify access token is still valid
- Review data format matches HubSpot requirements
- Check rate limits

### Token Refresh Failed
- User may need to re-authorize the app
- Check HubSpot app credentials are correct
- Verify client secret hasn't been rotated

---

## API Documentation

Full interactive API documentation available at:
- Swagger UI: `https://hubspot-crm-sync.preview.emergentagent.com/docs`
- ReDoc: `https://hubspot-crm-sync.preview.emergentagent.com/redoc`

---

## Support

For issues or questions:
- Check logs: `/var/log/supervisor/backend.err.log`
- Review API responses for error details
- Contact system administrator

---

**Last Updated:** January 19, 2025
**Version:** 1.0.0
