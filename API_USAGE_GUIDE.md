# CorpInfo API Usage Guide

Complete guide for accessing CorpInfo programmatically via REST API.

## Authentication

CorpInfo supports two authentication methods:

### 1. JWT Token (Web Applications)

Used by the web frontend for logged-in users.

**Login to get token:**
```bash
curl -X POST https://service-worker-fix.preview.emergentagent.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "your_password"
  }'
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": "user_123",
    "email": "user@example.com",
    "credits": 1000
  }
}
```

**Use token in requests:**
```bash
curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
  https://service-worker-fix.preview.emergentagent.com/api/crawl/history
```

### 2. API Key (Programmatic Access) ⭐ **Recommended**

Long-lived tokens for scripts, integrations, and MCP servers.

**Generate API Key:**
1. Log in to CorpInfo Dashboard
2. Go to **API Tokens** section
3. Click **"Generate New Token"**
4. Copy token (format: `corp_...`)

**Use API Key:**
```bash
curl -H "X-API-Key: corp_abc123..." \
  https://service-worker-fix.preview.emergentagent.com/api/crawl/history
```

## Core Endpoints

### Company Search

Search for company data by domain, name, or LinkedIn URL.

**Endpoint:** `POST /api/crawl/single`

**Request:**
```bash
curl -X POST \
  -H "X-API-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "input_type": "domain",
    "input_value": "stripe.com"
  }' \
  https://service-worker-fix.preview.emergentagent.com/api/crawl/single
```

**Input Types:**
- `domain` - Company website (e.g., "stripe.com")
- `company_name` - Company name (e.g., "Stripe Inc")
- `linkedin_url` - LinkedIn URL (e.g., "https://linkedin.com/company/stripe")

**Response:**
```json
{
  "id": "req_xyz789",
  "user_id": "user_123",
  "input_type": "domain",
  "input_value": "stripe.com",
  "status": "completed",
  "result": {
    "id": "comp_456",
    "company_name": "Stripe",
    "domain": "stripe.com",
    "linkedin_url": "https://www.linkedin.com/company/stripe",
    "industry": "Financial Services",
    "employee_size": "1000-5000",
    "founded_on": "2010",
    "founders": ["Patrick Collison", "John Collison"],
    "description": "Stripe is a technology company that builds economic infrastructure for the internet...",
    "address": "510 Townsend Street, San Francisco, CA 94103",
    "phone_numbers": ["+1-888-926-2289"],
    "emails": ["support@stripe.com"],
    "country": "United States",
    "location": "San Francisco, CA",
    "twitter_url": "https://twitter.com/stripe",
    "facebook_url": "https://facebook.com/stripe",
    "confidence_score": 0.95,
    "data_sources": ["official_website", "linkedin", "crunchbase"],
    "last_crawled": "2025-11-19T10:30:00Z"
  },
  "created_at": "2025-11-19T10:29:45Z",
  "completed_at": "2025-11-19T10:30:00Z"
}
```

### Bulk Upload

Process multiple companies at once.

**Endpoint:** `POST /api/crawl/bulk-upload`

**CSV Format:**
```csv
input_type,input_value
domain,stripe.com
domain,openai.com
company_name,Microsoft
linkedin_url,https://linkedin.com/company/google
```

**Request:**
```bash
curl -X POST \
  -H "X-API-Key: your_api_key" \
  -F "file=@companies.csv" \
  -F "input_type=domain" \
  https://service-worker-fix.preview.emergentagent.com/api/crawl/bulk-upload
```

**Response:**
```json
{
  "message": "Bulk upload successful",
  "job_id": "job_abc123",
  "total_requests": 4,
  "status": "processing"
}
```

### Get Request Details

Retrieve detailed information about a specific crawl request.

**Endpoint:** `GET /api/crawl/request/{request_id}`

**Request:**
```bash
curl -H "X-API-Key: your_api_key" \
  https://service-worker-fix.preview.emergentagent.com/api/crawl/request/req_xyz789
```

### Crawl History

Get your recent crawl requests.

**Endpoint:** `GET /api/crawl/history?limit=50`

**Request:**
```bash
curl -H "X-API-Key: your_api_key" \
  https://service-worker-fix.preview.emergentagent.com/api/crawl/history?limit=10
```

**Response:**
```json
[
  {
    "id": "req_xyz789",
    "input_type": "domain",
    "input_value": "stripe.com",
    "status": "completed",
    "result": { ... },
    "created_at": "2025-11-19T10:29:45Z"
  },
  ...
]
```

### Search Central Ledger

Search all crawled companies (global database).

**Endpoint:** `GET /api/crawl/search?query={query}&limit={limit}`

**Request:**
```bash
curl -H "X-API-Key: your_api_key" \
  "https://service-worker-fix.preview.emergentagent.com/api/crawl/search?query=fintech&limit=20"
```

**Response:**
```json
[
  {
    "id": "comp_123",
    "company_name": "Stripe",
    "domain": "stripe.com",
    "linkedin_url": "...",
    "industry": "Financial Services",
    "confidence_score": 0.95,
    "last_crawled": "2025-11-19T10:30:00Z"
  },
  ...
]
```

## API Token Management

### List Your Tokens

**Endpoint:** `GET /api/api-tokens`

```bash
curl -H "Authorization: Bearer jwt_token" \
  https://service-worker-fix.preview.emergentagent.com/api/api-tokens
```

### Create New Token

**Endpoint:** `POST /api/api-tokens`

```bash
curl -X POST \
  -H "Authorization: Bearer jwt_token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Production API",
    "scopes": ["crawl:read", "crawl:write"],
    "expires_in_days": 90
  }' \
  https://service-worker-fix.preview.emergentagent.com/api/api-tokens
```

**Response:**
```json
{
  "id": "token_123",
  "name": "Production API",
  "token": "corp_abc123def456...",
  "scopes": ["crawl:read", "crawl:write"],
  "created_at": "2025-11-19T10:00:00Z",
  "expires_at": "2026-02-19T10:00:00Z"
}
```

⚠️ **Important:** Token is shown only once. Save it securely!

### Revoke Token

**Endpoint:** `DELETE /api/api-tokens/{token_id}`

```bash
curl -X DELETE \
  -H "Authorization: Bearer jwt_token" \
  https://service-worker-fix.preview.emergentagent.com/api/api-tokens/token_123
```

### Toggle Token (Enable/Disable)

**Endpoint:** `PUT /api/api-tokens/{token_id}/toggle`

```bash
curl -X PUT \
  -H "Authorization: Bearer jwt_token" \
  https://service-worker-fix.preview.emergentagent.com/api/api-tokens/token_123/toggle
```

## Code Examples

### Python

```python
import requests

API_URL = "https://service-worker-fix.preview.emergentagent.com/api"
API_KEY = "corp_your_api_key_here"

class CorpInfoClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        }
    
    def search_company(self, input_type, input_value):
        """Search for company data"""
        response = requests.post(
            f"{API_URL}/crawl/single",
            json={
                "input_type": input_type,
                "input_value": input_value
            },
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def get_history(self, limit=50):
        """Get crawl history"""
        response = requests.get(
            f"{API_URL}/crawl/history",
            params={"limit": limit},
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def search_ledger(self, query, limit=10):
        """Search central ledger"""
        response = requests.get(
            f"{API_URL}/crawl/search",
            params={"query": query, "limit": limit},
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

# Usage
client = CorpInfoClient(API_KEY)

# Search for a company
result = client.search_company("domain", "openai.com")
print(f"Company: {result['result']['company_name']}")
print(f"LinkedIn: {result['result']['linkedin_url']}")
print(f"Confidence: {result['result']['confidence_score']}")

# Get history
history = client.get_history(limit=10)
print(f"Recent requests: {len(history)}")

# Search ledger
companies = client.search_ledger("artificial intelligence", limit=5)
for company in companies:
    print(f"- {company['company_name']}: {company['domain']}")
```

### JavaScript/Node.js

```javascript
const axios = require('axios');

const API_URL = 'https://service-worker-fix.preview.emergentagent.com/api';
const API_KEY = 'corp_your_api_key_here';

class CorpInfoClient {
  constructor(apiKey) {
    this.apiKey = apiKey;
    this.axios = axios.create({
      baseURL: API_URL,
      headers: {
        'X-API-Key': apiKey,
        'Content-Type': 'application/json'
      }
    });
  }

  async searchCompany(inputType, inputValue) {
    const response = await this.axios.post('/crawl/single', {
      input_type: inputType,
      input_value: inputValue
    });
    return response.data;
  }

  async getHistory(limit = 50) {
    const response = await this.axios.get('/crawl/history', {
      params: { limit }
    });
    return response.data;
  }

  async searchLedger(query, limit = 10) {
    const response = await this.axios.get('/crawl/search', {
      params: { query, limit }
    });
    return response.data;
  }
}

// Usage
const client = new CorpInfoClient(API_KEY);

(async () => {
  // Search for a company
  const result = await client.searchCompany('domain', 'stripe.com');
  console.log(`Company: ${result.result.company_name}`);
  console.log(`LinkedIn: ${result.result.linkedin_url}`);
  
  // Get history
  const history = await client.getHistory(10);
  console.log(`Recent requests: ${history.length}`);
  
  // Search ledger
  const companies = await client.searchLedger('fintech', 5);
  companies.forEach(company => {
    console.log(`- ${company.company_name}: ${company.domain}`);
  });
})();
```

### cURL Examples

**Search company:**
```bash
curl -X POST \
  -H "X-API-Key: corp_your_key" \
  -H "Content-Type: application/json" \
  -d '{"input_type":"domain","input_value":"github.com"}' \
  https://service-worker-fix.preview.emergentagent.com/api/crawl/single
```

**Get history:**
```bash
curl -H "X-API-Key: corp_your_key" \
  "https://service-worker-fix.preview.emergentagent.com/api/crawl/history?limit=10"
```

**Search ledger:**
```bash
curl -H "X-API-Key: corp_your_key" \
  "https://service-worker-fix.preview.emergentagent.com/api/crawl/search?query=saas&limit=20"
```

## Error Handling

### HTTP Status Codes

- `200` - Success
- `400` - Bad request (invalid parameters)
- `401` - Unauthorized (invalid/missing API key)
- `403` - Forbidden (insufficient credits or permissions)
- `404` - Not found
- `429` - Rate limit exceeded
- `500` - Server error

### Error Response Format

```json
{
  "detail": "Error message description",
  "error_code": "INVALID_API_KEY",
  "request_id": "req_xyz123"
}
```

### Common Errors

**401 Unauthorized:**
```json
{
  "detail": "Invalid API key"
}
```

**429 Rate Limit:**
```json
{
  "detail": "Rate limit exceeded",
  "retry_after": 45,
  "limit": 120,
  "window": "1 minute"
}
```

**403 Insufficient Credits:**
```json
{
  "detail": "Insufficient credits. Please purchase more."
}
```

## Rate Limits

Rate limits are applied per API key:

| Plan       | Requests/Min | Requests/Day | Credits |
|------------|--------------|--------------|---------|
| Free       | 60           | 500          | 10      |
| Starter    | 120          | 5,000        | 1,000   |
| Pro        | 300          | 15,000       | 2,500   |
| Enterprise | Custom       | Unlimited    | Custom  |

### Rate Limit Headers

Every response includes:
```
X-RateLimit-Limit: 120
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1700000000
```

### Handling Rate Limits

**Python Example:**
```python
import time
import requests

def make_request_with_retry(url, headers, max_retries=3):
    for attempt in range(max_retries):
        response = requests.get(url, headers=headers)
        
        if response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 60))
            print(f"Rate limited. Waiting {retry_after}s...")
            time.sleep(retry_after)
            continue
        
        return response
    
    raise Exception("Max retries exceeded")
```

## Best Practices

### Security
- ✅ Store API keys in environment variables
- ✅ Never commit keys to version control
- ✅ Use separate keys for dev/staging/production
- ✅ Rotate keys regularly
- ✅ Revoke unused keys immediately

### Performance
- ✅ Use bulk upload for multiple companies
- ✅ Cache responses when appropriate
- ✅ Implement exponential backoff for retries
- ✅ Monitor rate limit headers
- ✅ Use webhooks for async processing

### Data Quality
- ✅ Check confidence scores
- ✅ Validate critical data points
- ✅ Handle missing fields gracefully
- ✅ Update stale data periodically

## Support

- **Documentation:** Full API docs at `/docs` endpoint
- **Status Page:** https://status.corpinfo.com
- **Email:** support@corpinfo.com
- **Response Time:** 24-48 hours

## Changelog

### v1.0.0 (2025-11-19)
- ✅ Initial API release
- ✅ JWT and API key authentication
- ✅ Company search endpoints
- ✅ Bulk upload support
- ✅ Central ledger search
- ✅ MCP server configuration

---

**Ready to start?** Generate your API key in the Dashboard and start building! 🚀
