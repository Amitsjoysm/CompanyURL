# MCP Server Setup Guide

This guide explains how to set up and use the CorpInfo MCP (Model Context Protocol) Server for AI assistant integration.

## What is MCP?

MCP (Model Context Protocol) allows AI assistants like Claude, ChatGPT, and others to directly access your CorpInfo company data through a standardized interface.

## Prerequisites

- Active CorpInfo account
- API token (generated from Dashboard)
- MCP-compatible AI assistant or application

## Quick Start

### 1. Generate API Token

1. Log in to CorpInfo Dashboard
2. Navigate to **Settings** or **API Tokens** section
3. Click **"Generate New Token"**
4. Give it a name (e.g., "MCP Server")
5. Select scopes: `crawl:read`, `crawl:write`
6. **Copy the token immediately** (shown only once)

Example token: `corp_abc123def456...`

### 2. Configure MCP Server

#### Option A: Using mcp-server-config.json

Copy the `mcp-server-config.json` file and add your API key:

```json
{
  "name": "corpinfo-mcp-server",
  "server": {
    "url": "https://api-access-restore.preview.emergentagent.com",
    "api_base": "/api"
  },
  "authentication": {
    "type": "api_key",
    "api_key": "YOUR_API_TOKEN_HERE"
  }
}
```

#### Option B: Environment Variables

Set environment variable:
```bash
export CORPINFO_API_KEY="your_api_token_here"
```

### 3. Test Connection

Use curl to verify:

```bash
curl -H "X-API-Key: your_api_token_here" \
  https://api-access-restore.preview.emergentagent.com/api/crawl/history
```

Expected response:
```json
[
  {
    "id": "...",
    "input_value": "example.com",
    "status": "completed",
    ...
  }
]
```

## Available Tools

### 1. search_company

Search for company information.

**Endpoint:** `POST /api/crawl/single`

**Parameters:**
- `input_type`: "domain" | "company_name" | "linkedin_url"
- `input_value`: The search value

**Example:**
```bash
curl -X POST \
  -H "X-API-Key: your_token" \
  -H "Content-Type: application/json" \
  -d '{
    "input_type": "domain",
    "input_value": "openai.com"
  }' \
  https://api-access-restore.preview.emergentagent.com/api/crawl/single
```

**Response:**
```json
{
  "id": "req_123",
  "status": "completed",
  "result": {
    "company_name": "OpenAI",
    "domain": "openai.com",
    "linkedin_url": "https://linkedin.com/company/openai",
    "industry": "Artificial Intelligence",
    "employee_size": "500-1000",
    "confidence_score": 0.95,
    ...
  }
}
```

### 2. get_crawl_history

Get your recent crawl requests.

**Endpoint:** `GET /api/crawl/history?limit=50`

**Example:**
```bash
curl -H "X-API-Key: your_token" \
  https://api-access-restore.preview.emergentagent.com/api/crawl/history?limit=10
```

### 3. search_central_ledger

Search all crawled companies.

**Endpoint:** `GET /api/crawl/search?query=tech&limit=10`

**Example:**
```bash
curl -H "X-API-Key: your_token" \
  https://api-access-restore.preview.emergentagent.com/api/crawl/search?query=technology
```

### 4. get_request_details

Get detailed info about a specific request.

**Endpoint:** `GET /api/crawl/request/{request_id}`

**Example:**
```bash
curl -H "X-API-Key: your_token" \
  https://api-access-restore.preview.emergentagent.com/api/crawl/request/req_123
```

## Integration Examples

### Claude Desktop

Add to `~/Library/Application Support/Claude/config.json`:

```json
{
  "mcpServers": {
    "corpinfo": {
      "url": "https://api-access-restore.preview.emergentagent.com",
      "apiKey": "your_api_token_here"
    }
  }
}
```

### Custom Python Integration

```python
import requests

API_URL = "https://api-access-restore.preview.emergentagent.com/api"
API_KEY = "your_api_token_here"

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

# Search for a company
response = requests.post(
    f"{API_URL}/crawl/single",
    json={
        "input_type": "domain",
        "input_value": "stripe.com"
    },
    headers=headers
)

company_data = response.json()
print(f"Company: {company_data['result']['company_name']}")
print(f"Employees: {company_data['result']['employee_size']}")
```

### Node.js Integration

```javascript
const axios = require('axios');

const API_URL = 'https://api-access-restore.preview.emergentagent.com/api';
const API_KEY = 'your_api_token_here';

async function searchCompany(domain) {
  const response = await axios.post(
    `${API_URL}/crawl/single`,
    {
      input_type: 'domain',
      input_value: domain
    },
    {
      headers: {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json'
      }
    }
  );
  
  return response.data;
}

// Usage
searchCompany('github.com').then(data => {
  console.log(data.result);
});
```

## Rate Limits

Limits vary by plan:

| Plan       | Requests/Min | Requests/Day | Total Credits |
|------------|--------------|--------------|---------------|
| Free       | 60           | 500          | 10            |
| Starter    | 120          | 5,000        | 1,000         |
| Pro        | 300          | 15,000       | 2,500         |
| Enterprise | Custom       | Unlimited    | Custom        |

## Security Best Practices

### Token Management
- ✅ Store tokens in environment variables
- ✅ Never commit tokens to version control
- ✅ Rotate tokens regularly
- ✅ Use separate tokens for different apps
- ✅ Revoke unused tokens

### Access Control
- ✅ Use minimum required scopes
- ✅ Set expiration dates for tokens
- ✅ Monitor token usage in dashboard
- ✅ Revoke tokens immediately if compromised

## Troubleshooting

### 401 Unauthorized

**Cause:** Invalid or expired API key

**Solution:**
1. Verify API key is correct
2. Check if token is active in dashboard
3. Ensure token hasn't expired
4. Generate new token if needed

### 429 Rate Limit Exceeded

**Cause:** Too many requests

**Solution:**
1. Implement exponential backoff
2. Check rate limit headers in response
3. Upgrade plan if needed
4. Use bulk endpoints instead of individual requests

### 403 Forbidden

**Cause:** Insufficient permissions

**Solution:**
1. Check token scopes
2. Verify user account is active
3. Ensure you have credits remaining

## API Response Headers

Every response includes:

```
X-RateLimit-Limit: 120
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1700000000
X-Request-ID: req_abc123
```

## Support

- **Documentation:** https://docs.corpinfo.com
- **API Status:** https://status.corpinfo.com
- **Email:** support@corpinfo.com
- **Discord:** https://discord.gg/corpinfo

## Advanced Usage

### Bulk Processing

For processing many companies, use the bulk upload endpoint:

```bash
curl -X POST \
  -H "X-API-Key: your_token" \
  -F "file=@companies.csv" \
  https://api-access-restore.preview.emergentagent.com/api/crawl/bulk-upload
```

### Webhook Notifications

Set up webhooks to receive notifications when crawls complete:

```bash
curl -X POST \
  -H "X-API-Key: your_token" \
  -H "Content-Type: application/json" \
  -d '{
    "webhook_url": "https://your-app.com/webhook",
    "events": ["crawl.completed", "crawl.failed"]
  }' \
  https://api-access-restore.preview.emergentagent.com/api/webhooks
```

## MCP Server Architecture

```
┌─────────────────┐
│  AI Assistant   │
│  (Claude, GPT)  │
└────────┬────────┘
         │
         │ MCP Protocol
         │
┌────────▼────────┐
│  MCP Server     │
│  Configuration  │
└────────┬────────┘
         │
         │ HTTPS + API Key
         │
┌────────▼────────┐
│  CorpInfo API   │
│  /api/*         │
└────────┬────────┘
         │
         │
┌────────▼────────┐
│  Company Data   │
│  Database       │
└─────────────────┘
```

## Next Steps

1. ✅ Generate your API token
2. ✅ Test with curl commands
3. ✅ Integrate with your AI assistant
4. ✅ Build custom applications
5. ✅ Monitor usage in dashboard

Happy building with CorpInfo MCP Server! 🚀
