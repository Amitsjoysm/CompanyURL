# CorpInfo - Production-Ready Company Data Crawler

**CorpInfo** is a comprehensive, production-ready platform for crawling and enriching company data. Convert company names, domains, and LinkedIn URLs into complete company profiles with confidence scoring and multi-source verification.

## 🚀 Features

### Core Functionality
- ✅ **Multi-Input Search**: Domain → Company, Company → LinkedIn, LinkedIn → Full Data
- ✅ **Real-Time Crawling**: Live data from official websites, LinkedIn, news sources
- ✅ **Confidence Scoring**: 0-1 score for data reliability
- ✅ **Bulk Processing**: Upload CSV/Excel, download enriched results
- ✅ **Central Ledger**: Global company database across all users
- ✅ **Data Enrichment**: Industry, size, founders, contacts, news, social media

### Authentication & Access
- ✅ **JWT Authentication**: Secure email/password login
- ✅ **Role-Based Access**: User and Superadmin roles
- ✅ **API Token System**: Generate tokens for programmatic access
- ✅ **MCP Server Support**: AI assistant integration (Claude, ChatGPT)

### Business Features
- ✅ **Credit System**: Free (10), Starter ($25/1000), Pro ($49/2500), Enterprise (slider 2500-1M)
- ✅ **Razorpay Integration**: Secure payment processing
- ✅ **Rate Limiting**: Fair usage with plan-based limits
- ✅ **Usage Tracking**: Monitor API calls and credit consumption

### Admin Capabilities
- ✅ **User Management**: View, update credits, activate/deactivate accounts
- ✅ **Plan Management**: Full CRUD for pricing plans
- ✅ **Content CMS**: Manage blogs and FAQs
- ✅ **Central Ledger View**: Monitor all crawled companies
- ✅ **Analytics Dashboard**: Track system usage

### SEO & Content
- ✅ **10 SEO-Optimized Blogs**: How-to guides, best practices, API docs
- ✅ **FAQ System**: Comprehensive Q&A management
- ✅ **Dynamic Sitemap**: Auto-generated with blogs
- ✅ **LLMs.txt**: AI crawler optimization
- ✅ **robots.txt**: Search engine directives

## 📋 Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: React 19 + Tailwind CSS
- **Database**: MongoDB
- **Authentication**: JWT + bcrypt
- **Payments**: Razorpay
- **Crawling**: Playwright, BeautifulSoup, Groq AI
- **API**: RESTful with OpenAPI docs

## 🏗️ Architecture

```
┌─────────────────┐
│   React App     │  Port 3000
│  (Frontend)     │
└────────┬────────┘
         │
         │ HTTPS
         │
┌────────▼────────┐
│  FastAPI Server │  Port 8001
│   (Backend)     │  /api/*
└────────┬────────┘
         │
    ┌────┴────┬──────────┐
    │         │          │
┌───▼───┐ ┌──▼──┐   ┌───▼────┐
│MongoDB│ │Groq │   │Razorpay│
│  DB   │ │ AI  │   │Payments│
└───────┘ └─────┘   └────────┘
```

## 🔧 Setup

### Prerequisites
- Python 3.9+
- Node.js 16+
- MongoDB
- Yarn package manager

### Environment Configuration

**Backend** (`/app/backend/.env`):
```bash
# Database
MONGO_URL="mongodb://localhost:27017"
DB_NAME="corpinfo_db"

# Security
SECRET_KEY="your-secret-key-change-in-production"

# AI Crawling
GROQ_API_KEY="gsk_your_groq_key_here"

# Payments - Get from https://dashboard.razorpay.com/app/keys
RAZORPAY_KEY_ID="rzp_test_YOUR_KEY_ID"
RAZORPAY_KEY_SECRET="YOUR_KEY_SECRET"

# CORS
CORS_ORIGINS="*"
```

**Frontend** (`/app/frontend/.env`):
```bash
REACT_APP_BACKEND_URL=https://your-domain.com
```

### Installation

**Backend:**
```bash
cd /app/backend
pip install -r requirements.txt
python init_data.py  # Seed blogs and FAQs
uvicorn server:app --host 0.0.0.0 --port 8001
```

**Frontend:**
```bash
cd /app/frontend
yarn install
yarn start  # Development
yarn build  # Production
```

## 📚 Documentation

- **[API Usage Guide](./API_USAGE_GUIDE.md)** - Complete REST API documentation
- **[MCP Server Setup](./MCP_SERVER_SETUP.md)** - AI assistant integration guide
- **[MCP Config](./mcp-server-config.json)** - MCP server configuration
- **OpenAPI Docs**: `https://your-domain.com/docs`
- **ReDoc**: `https://your-domain.com/redoc`

## 🔐 Authentication Methods

### 1. Web Login (JWT)
```bash
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "password"
}
```

### 2. API Token (Programmatic)
```bash
# Generate token in Dashboard > API Tokens
curl -H "X-API-Key: corp_your_token_here" \
  https://your-domain.com/api/crawl/history
```

## 🎯 Quick Start

### Search Company
```bash
curl -X POST \
  -H "X-API-Key: your_token" \
  -H "Content-Type: application/json" \
  -d '{
    "input_type": "domain",
    "input_value": "stripe.com"
  }' \
  https://your-domain.com/api/crawl/single
```

### Get History
```bash
curl -H "X-API-Key: your_token" \
  https://your-domain.com/api/crawl/history?limit=10
```

### Search Ledger
```bash
curl -H "X-API-Key: your_token" \
  "https://your-domain.com/api/crawl/search?query=fintech&limit=20"
```

## 💳 Pricing Plans

| Plan       | Price | Credits | Requests/Min | API Access |
|------------|-------|---------|--------------|------------|
| Free       | $0    | 10      | 60           | ❌         |
| Starter    | $25   | 1,000   | 120          | ✅         |
| Pro        | $49   | 2,500   | 300          | ✅         |
| Enterprise | Custom| Custom  | Custom       | ✅         |

## 🔒 Security

- ✅ **Password Hashing**: bcrypt with salt
- ✅ **JWT Tokens**: 7-day expiration
- ✅ **API Keys**: Secure token generation
- ✅ **Rate Limiting**: Per-plan request limits
- ✅ **HTTPS Only**: Encrypted transmission
- ✅ **Input Validation**: Pydantic models
- ✅ **CORS Protection**: Configurable origins

## 📊 Admin Features

Access admin dashboard at `/admin` (superadmin only):

- **Users**: View all users, update credits, activate/deactivate
- **Plans**: Create, edit, delete pricing plans
- **Blogs**: Full CRUD with markdown support
- **FAQs**: Categorized Q&A management
- **Ledger**: View all crawled companies globally

## 🧪 Testing

```bash
# Backend tests
cd /app/backend
pytest tests/

# Frontend tests
cd /app/frontend
yarn test

# E2E tests
yarn test:e2e
```

## 📈 Scalability

Built for 10,000+ concurrent users:

- **Async I/O**: FastAPI with async/await
- **Connection Pooling**: MongoDB Motor driver
- **Caching**: Response caching for frequent queries
- **Rate Limiting**: Prevent abuse and ensure fair use
- **Horizontal Scaling**: Stateless design for load balancing

## 🛠️ SOLID Principles

- **Single Responsibility**: Each service handles one domain
- **Open/Closed**: Extensible crawler architecture
- **Liskov Substitution**: Interchangeable crawler implementations
- **Interface Segregation**: Minimal, focused interfaces
- **Dependency Inversion**: Depend on abstractions, not concretions

## 📝 Data Model

**Company Data Fields:**
- Basic: name, domain, LinkedIn URL
- Metadata: industry, employee size, founded date
- Contacts: address, phones, emails
- Social: Twitter, Facebook URLs
- Intelligence: latest news, founders
- Quality: confidence score, data sources

## 🤝 MCP Integration

CorpInfo supports MCP (Model Context Protocol) for AI assistants:

1. Generate API token in dashboard
2. Configure MCP server using `mcp-server-config.json`
3. AI assistants can now query company data directly

See [MCP_SERVER_SETUP.md](./MCP_SERVER_SETUP.md) for details.

## 🚦 Rate Limits

| Plan       | Requests/Min | Requests/Day |
|------------|--------------|--------------|
| Free       | 60           | 500          |
| Starter    | 120          | 5,000        |
| Pro        | 300          | 15,000       |
| Enterprise | Custom       | Unlimited    |

## 📞 Support

- **Email**: support@corpinfo.com
- **Documentation**: https://docs.corpinfo.com
- **Status**: https://status.corpinfo.com
- **API Issues**: Check `/docs` for interactive testing

## 🔄 Updates

### v1.0.0 (2025-11-19)
- ✅ Initial production release
- ✅ Full CRUD admin dashboard
- ✅ API token system
- ✅ MCP server support
- ✅ 10 SEO blogs
- ✅ Razorpay integration
- ✅ Central company ledger
- ✅ Confidence scoring system

## 📜 License

Proprietary - All rights reserved

## 🙏 Credits

Built with modern best practices for production-ready SaaS applications.

---

**Ready to enrich your company data?** Start with 10 free credits! 🚀
