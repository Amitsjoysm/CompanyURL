"""
Initialize database with blog posts and FAQs
Run this script once to populate initial content
"""
import asyncio
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from core.config import get_settings
from models.content import Blog, FAQ
from datetime import datetime, timezone

settings = get_settings()

INITIAL_BLOGS = [
    {
        "slug": "find-linkedin-company-url",
        "title": "How to Find a Company's LinkedIn Page from Website Domain",
        "excerpt": "Learn the best methods to discover company LinkedIn URLs using domain names and company information.",
        "content": """Finding a company's LinkedIn page from their website domain is a common task for sales professionals, recruiters, and researchers. Here's a comprehensive guide to help you discover LinkedIn company URLs efficiently.

## Method 1: Direct LinkedIn Search
The simplest approach is to use LinkedIn's search functionality. Navigate to LinkedIn and search for the company name. LinkedIn's algorithm usually surfaces the official company page as the top result.

## Method 2: Using CorpInfo Tool
Our platform automates this process by crawling multiple sources to find verified LinkedIn URLs. Simply enter the company domain, and our AI-powered crawler will:
- Search official company websites
- Verify LinkedIn URLs
- Provide confidence scores
- Enrich data with additional company information

## Method 3: Google Search Operators
Use Google search with the operator: site:linkedin.com/company [company name]. This limits results to LinkedIn company pages only.

## Why LinkedIn URLs Matter
LinkedIn company pages provide valuable insights:
- Employee count and growth
- Company updates and news
- Key decision-makers
- Industry classification
- Verified company information

## Best Practices
1. Always verify the LinkedIn URL matches the company
2. Check for official verification badges
3. Cross-reference with company website
4. Use multiple data sources for validation

CorpInfo's crawler follows these best practices automatically, providing you with verified, high-confidence LinkedIn URLs for your business needs.
"""
    },
    {
        "slug": "domain-to-linkedin",
        "title": "Convert Company Domain to LinkedIn URL: Complete Guide",
        "excerpt": "Discover how to efficiently convert any company domain into its LinkedIn company page URL with high accuracy.",
        "content": """Converting company domains to LinkedIn URLs is essential for B2B sales, recruitment, and market research. This guide covers proven techniques and tools.

## Understanding the Challenge
Not all companies use predictable LinkedIn URL patterns. While some use their domain name, others use abbreviated versions, full legal names, or entirely different slugs.

## Automated Solutions
CorpInfo solves this challenge through:

### Multi-Source Crawling
- Analyzes company websites for LinkedIn links
- Searches social media footprints
- Validates against company databases
- Uses AI to verify matches

### Confidence Scoring
Each LinkedIn URL comes with a confidence score based on:
- Direct website linking
- URL slug similarity
- Social media verification
- Database cross-referencing

## Manual Techniques
If you prefer manual methods:

1. **Website Footer Check**: Most companies link their LinkedIn in the footer
2. **LinkedIn Search**: Use "site:linkedin.com/company domain.com" in Google
3. **Social Media**: Check other social profiles for LinkedIn links
4. **WHOIS Data**: Sometimes includes social media information

## Bulk Processing
For processing multiple domains:
- Upload CSV/Excel files
- Maintain input sequence in results
- Get detailed reports
- Export enriched data

## Use Cases
### Sales Teams
- Build prospect lists
- Identify decision-makers
- Research company size and growth

### Recruiters
- Find hiring managers
- Understand company culture
- Track employee growth

### Market Researchers
- Industry analysis
- Competitive intelligence
- Company monitoring

Start using CorpInfo's domain-to-LinkedIn converter for accurate, scalable company data enrichment.
"""
    },
    {
        "slug": "company-data-enrichment",
        "title": "Complete Company Data Enrichment: Beyond LinkedIn URLs",
        "excerpt": "Comprehensive guide to enriching company data with industry, size, founders, contact information, and latest news.",
        "content": """Company data enrichment goes far beyond finding LinkedIn URLs. Modern businesses need comprehensive company intelligence for effective operations.

## What is Company Data Enrichment?
Data enrichment is the process of enhancing existing company information with additional data points from multiple sources.

## Key Data Points We Collect

### Basic Information
- Official company name
- Primary domain
- LinkedIn URL
- Industry classification
- Company description

### Size and Scale
- Employee count
- Revenue range (when available)
- Growth trajectory
- Office locations

### Leadership Data
- Founders and founding date
- Key executives
- Board members

### Contact Information
- Official email addresses
- Phone numbers
- Physical addresses
- Regional offices

### Latest Intelligence
- Recent news articles
- Funding announcements
- Product launches
- Strategic partnerships

## Data Sources Priority
CorpInfo follows a strategic crawling approach:

1. **Official Website** (Highest Priority)
   - Most accurate source
   - Company-verified information
   - Contact details
   - About us pages

2. **LinkedIn** (High Priority)
   - Employee data
   - Company updates
   - Leadership information

3. **News Aggregators** (Medium Priority)
   - Latest developments
   - Industry trends
   - Competitive moves

4. **Business Databases** (Supporting)
   - Crunchbase data
   - Industry directories
   - Government records

## Confidence Scoring System
Every data point receives a confidence score:
- **0.9-1.0**: Multiple sources, verified
- **0.7-0.9**: Single reliable source
- **0.5-0.7**: Inferred or estimated
- **Below 0.5**: Uncertain, needs verification

## API Integration
CorpInfo provides API access for:
- Real-time enrichment
- Bulk processing
- Custom integrations
- MCP server support

## Use Cases

### Sales Intelligence
- Pre-call research
- Account prioritization
- Personalized outreach

### Due Diligence
- Investment research
- Partnership evaluation
- Vendor assessment

### Market Analysis
- Industry mapping
- Competitive landscape
- Market sizing

### Compliance
- KYC processes
- Risk assessment
- Regulatory reporting

Get started with CorpInfo's comprehensive company data enrichment platform today.
"""
    },
    {
        "slug": "linkedin-company-finder-tool",
        "title": "LinkedIn Company Finder Tool: Features and Benefits",
        "excerpt": "Explore the powerful features of modern LinkedIn company finder tools and how they transform business operations.",
        "content": """LinkedIn company finder tools have become essential for modern business operations. This article explores key features and benefits.

## Core Features

### Instant Lookup
Convert any input (company name, domain, or LinkedIn URL) to complete company profiles instantly.

### Bulk Processing
Upload CSV or Excel files with hundreds or thousands of companies. The tool maintains sequence and provides downloadable results.

### Data Verification
AI-powered verification ensures accuracy:
- Cross-reference multiple sources
- Validate LinkedIn URLs
- Confirm company details
- Flag inconsistencies

### Real-time Crawling
Unlike static databases, real-time crawling provides:
- Up-to-date information
- Latest company news
- Current employee counts
- Recent updates

## Business Benefits

### Time Savings
Manual research takes 5-10 minutes per company. Automated tools reduce this to seconds.

### Higher Accuracy
Human error in manual searches is eliminated through:
- Automated verification
- Multiple source validation
- Confidence scoring
- Consistency checks

### Scalability
Process from 1 to 10,000+ companies without additional effort or cost multiplication.

### Cost Efficiency
Compared to premium data providers:
- Lower per-search cost
- No minimum commitments
- Pay-as-you-go pricing
- Volume discounts

## Technical Capabilities

### API Access
- RESTful API
- MCP server support
- Webhook notifications
- Real-time updates

### Integration Options
- CRM systems
- Marketing automation
- Sales enablement
- Custom applications

### Data Export
- CSV format
- Excel spreadsheets
- JSON for developers
- API responses

## Security and Compliance
- Secure data handling
- GDPR compliance
- Data encryption
- Access controls

## Pricing Models

### Free Tier
- 10 free searches
- Basic features
- Manual processing

### Starter Plan ($25)
- 1,000 searches
- Bulk upload
- Priority processing

### Pro Plan ($49)
- 2,500 searches
- API access
- Advanced features

### Enterprise
- Custom volume
- Dedicated support
- SLA guarantees
- Custom integrations

Choose CorpInfo for reliable, scalable company data enrichment.
"""
    },
    {
        "slug": "b2b-lead-generation-linkedin",
        "title": "B2B Lead Generation Using LinkedIn Company Data",
        "excerpt": "Master B2B lead generation strategies using LinkedIn company information and data enrichment tools.",
        "content": """LinkedIn company data is a goldmine for B2B lead generation. This guide shows you how to leverage it effectively.

## Why LinkedIn for B2B?
LinkedIn is the world's largest professional network with:
- 900+ million users
- 58 million companies
- Decision-maker access
- Professional context

## Lead Generation Strategy

### 1. Ideal Customer Profile (ICP)
Define your target companies:
- Industry sectors
- Company size
- Geographic location
- Growth indicators
- Tech stack

### 2. Company Discovery
Use CorpInfo to:
- Find target companies
- Verify LinkedIn pages
- Enrich company data
- Score lead quality

### 3. Contact Identification
Navigate to LinkedIn company pages to:
- Identify decision-makers
- Understand org structure
- Find common connections
- Gauge engagement

### 4. Personalized Outreach
Use enriched data for:
- Relevant messaging
- Timely contact
- Value propositions
- Follow-up sequences

## Data Points for Lead Scoring

### Company Signals
- Recent funding
- Growth trajectory
- Job postings
- News mentions

### Engagement Indicators
- Social media activity
- Content publishing
- Employee engagement
- Company updates

### Intent Signals
- Technology adoption
- Expansion plans
- Leadership changes
- Market moves

## Automation Workflow

### Step 1: Data Collection
- Upload company lists
- Run enrichment
- Download results

### Step 2: Segmentation
- Score companies
- Group by criteria
- Prioritize targets

### Step 3: Outreach
- CRM integration
- Email sequences
- LinkedIn InMail
- Multi-touch campaigns

### Step 4: Monitoring
- Track responses
- Update data
- Refine targeting

## Best Practices

### Do's
✓ Personalize every message
✓ Add value first
✓ Research thoroughly
✓ Follow up consistently
✓ Track metrics

### Don'ts
✗ Generic templates
✗ Aggressive sales
✗ Outdated data
✗ Single touchpoint
✗ Ignore responses

## Measuring Success

### Key Metrics
- Response rate
- Conversion rate
- Pipeline value
- Cost per lead
- ROI

### Optimization
- A/B test messaging
- Refine targeting
- Update cadences
- Improve data quality

## Tools Integration
- Salesforce
- HubSpot
- Outreach
- SalesLoft
- Custom CRM

Transform your B2B lead generation with CorpInfo's comprehensive company data platform.
"""
    },
    {
        "slug": "recruiting-company-research",
        "title": "Company Research for Recruiters: LinkedIn Data Guide",
        "excerpt": "Essential guide for recruiters to research companies, find hiring managers, and understand organizational structure.",
        "content": """Effective recruiting starts with thorough company research. LinkedIn company data provides crucial insights for recruitment success.

## Why Company Research Matters

### For Recruiters
- Understand company culture
- Identify hiring managers
- Gauge growth trajectory
- Assess candidate fit

### For Candidates
- Company legitimacy
- Growth opportunities
- Work environment
- Team structure

## Research Workflow

### Phase 1: Company Discovery
Start with CorpInfo to:
- Verify company existence
- Find LinkedIn page
- Get basic information
- Check legitimacy

### Phase 2: Deep Dive
Analyze LinkedIn page for:
- Company size
- Growth rate
- Recent hires
- Employee tenure
- Office locations

### Phase 3: Key People
Identify:
- Hiring managers
- Department heads
- HR contacts
- Team leads
- Potential referrers

### Phase 4: Context Building
Research:
- Recent news
- Funding rounds
- Product launches
- Market position
- Competitors

## LinkedIn Signals

### Growth Indicators
- Employee count increase
- New job postings
- Office expansions
- Funding announcements

### Culture Signals
- Employee engagement
- Content quality
- Values statements
- Employee testimonials

### Hiring Patterns
- Active job posts
- Hiring velocity
- Team expansions
- Role levels

## Outreach Strategy

### For Active Candidates
1. Company overview
2. Role specifics
3. Growth opportunities
4. Culture fit

### For Passive Candidates
1. Personalized approach
2. Career growth angle
3. Unique opportunities
4. Network connections

## Data Points to Collect

### Essential
- Company name
- Industry
- Size
- Location
- LinkedIn URL

### Important
- Growth trajectory
- Recent news
- Key people
- Tech stack
- Culture indicators

### Nice-to-Have
- Funding history
- Competitors
- Benefits
- Reviews
- Awards

## Tools for Recruiters

### CorpInfo Features
- Bulk company lookup
- Data enrichment
- LinkedIn verification
- Export capabilities

### Complementary Tools
- LinkedIn Recruiter
- Job boards
- ATS systems
- Email finders

## Compliance Considerations
- Data privacy
- GDPR compliance
- Candidate consent
- Information accuracy

## Best Practices

### Research
✓ Verify all information
✓ Check multiple sources
✓ Update regularly
✓ Document findings

### Outreach
✓ Personalize messages
✓ Reference research
✓ Add value
✓ Respect preferences

### Process
✓ Systematic approach
✓ Track interactions
✓ Follow up
✓ Measure results

Elevate your recruiting with comprehensive company research using CorpInfo.
"""
    },
    {
        "slug": "api-authentication-guide",
        "title": "API Authentication Guide: Secure Company Data Access",
        "excerpt": "Complete guide to authenticating with CorpInfo API, managing tokens, and implementing secure data access.",
        "content": """Secure API authentication is crucial for protecting your data and maintaining system integrity. This guide covers CorpInfo's authentication system.

## Authentication Methods

### JWT Token-Based Auth
CorpInfo uses JSON Web Tokens (JWT) for secure API authentication:
- Stateless authentication
- Encrypted tokens
- Automatic expiration
- Refresh capability

### Getting Started

#### 1. Register Account
```
POST /api/auth/register
{
  "email": "user@example.com",
  "password": "secure_password",
  "full_name": "Your Name"
}
```

#### 2. Obtain Access Token
```
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

Response includes:
- access_token
- token_type
- user information

#### 3. Use Token in Requests
Include in Authorization header:
```
Authorization: Bearer <your_access_token>
```

## API Endpoints

### Company Search
```
POST /api/crawl/single
{
  "input_type": "domain",
  "input_value": "example.com"
}
```

### Bulk Upload
```
POST /api/crawl/bulk-upload
Content-Type: multipart/form-data
file: companies.csv
```

### Search History
```
GET /api/crawl/history?limit=50
```

### Central Ledger Search
```
GET /api/crawl/search?query=tech&limit=10
```

## Security Best Practices

### Token Management
- Store tokens securely
- Never commit to version control
- Rotate regularly
- Use environment variables

### API Rate Limiting
- Free: 60 requests/minute
- Starter: 120 requests/minute
- Pro: 300 requests/minute
- Enterprise: Custom limits

### Error Handling
Common status codes:
- 200: Success
- 401: Unauthorized
- 403: Forbidden
- 429: Rate limit exceeded
- 500: Server error

## MCP Server Integration

### What is MCP?
Model Context Protocol allows AI assistants to access your company data directly.

### Setup Steps
1. Configure MCP server URL
2. Provide API credentials
3. Define data access scope
4. Test connection

### Use Cases
- AI-powered research
- Automated enrichment
- Chatbot integration
- Custom workflows

## Code Examples

### Python
```python
import requests

API_URL = "https://api.corpinfo.com"
token = "your_access_token"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

response = requests.post(
    f"{API_URL}/api/crawl/single",
    json={
        "input_type": "domain",
        "input_value": "example.com"
    },
    headers=headers
)

data = response.json()
```

### JavaScript
```javascript
const API_URL = "https://api.corpinfo.com";
const token = "your_access_token";

const response = await fetch(`${API_URL}/api/crawl/single`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    input_type: 'domain',
    input_value: 'example.com'
  })
});

const data = await response.json();
```

## Troubleshooting

### Token Expiration
- Tokens expire after 7 days
- Implement refresh logic
- Handle 401 errors gracefully

### Rate Limiting
- Implement exponential backoff
- Cache responses when possible
- Upgrade plan for higher limits

### API Errors
- Log error details
- Check API status page
- Contact support for persistent issues

Start building with CorpInfo's secure, reliable API today.
"""
    },
    {
        "slug": "confidence-scoring-system",
        "title": "Understanding Confidence Scores: Data Quality Assurance",
        "excerpt": "Deep dive into CorpInfo's confidence scoring system and how to interpret data quality metrics.",
        "content": """Data quality is paramount in business intelligence. CorpInfo's confidence scoring system helps you assess the reliability of every data point.

## What is Confidence Scoring?

Confidence scores indicate how certain we are about data accuracy, ranging from 0.0 (uncertain) to 1.0 (highly confident).

## Score Ranges

### High Confidence (0.9-1.0)
- Multiple independent sources confirm data
- Direct verification from official sources
- Recent validation (within 30 days)
- No conflicting information

### Good Confidence (0.7-0.9)
- Single reliable source
- Official company website or LinkedIn
- Validated within 90 days
- Minor discrepancies resolved

### Medium Confidence (0.5-0.7)
- Inferred from related data
- Secondary sources
- Older validation (90-180 days)
- Some uncertainty remains

### Low Confidence (Below 0.5)
- Limited sources
- Estimated data
- Outdated information
- Conflicting signals

## Scoring Factors

### Source Reliability
Weighted by trustworthiness:
- Official website: 1.0
- LinkedIn (verified): 0.95
- Crunchbase: 0.85
- News articles: 0.75
- Third-party databases: 0.65

### Data Freshness
Time decay factor:
- 0-30 days: 1.0x
- 31-90 days: 0.9x
- 91-180 days: 0.75x
- 180+ days: 0.5x

### Cross-Validation
Multiple source bonus:
- 1 source: baseline
- 2 sources: +0.1
- 3+ sources: +0.2
- All agree: +0.3

### Data Completeness
Fields filled percentage:
- 90-100%: +0.1
- 70-90%: +0.05
- Below 70%: 0.0

## Field-Level Scores

Different fields may have different confidence levels:

### Company Name
Usually high confidence:
- Direct from website
- Multiple validations
- Legal name verification

### Domain
Highest confidence:
- Direct input or verification
- WHOIS confirmation
- Website accessibility

### LinkedIn URL
Variable confidence:
- Direct link: 0.95+
- Search result: 0.8-0.9
- Inferred: 0.5-0.7
- Not found: 0.0

### Employee Size
Medium confidence:
- LinkedIn data: 0.8
- Job posting estimates: 0.6
- Third-party data: 0.5

### Contact Information
Varies widely:
- From website: 0.9
- From directory: 0.7
- From inference: 0.4

## Using Confidence Scores

### Decision Making
- High confidence (0.9+): Use immediately
- Good confidence (0.7-0.9): Use with awareness
- Medium (0.5-0.7): Verify if critical
- Low (<0.5): Manual verification needed

### Filtering Results
Filter by minimum confidence:
```
GET /api/crawl/search?query=tech&min_confidence=0.7
```

### Reporting
Include confidence in exports:
- Mark low-confidence fields
- Provide validation status
- Suggest verification steps

## Improving Confidence

### Data Updates
- Re-crawl periodically
- Update stale information
- Add new sources

### User Feedback
- Report inaccuracies
- Provide corrections
- Confirm accuracy

### Source Expansion
- Add authoritative sources
- Cross-reference more databases
- Improve crawling logic

## API Response Example

```json
{
  "company_name": "Example Corp",
  "domain": "example.com",
  "linkedin_url": "https://linkedin.com/company/example",
  "confidence_score": 0.92,
  "field_confidence": {
    "company_name": 0.98,
    "domain": 1.0,
    "linkedin_url": 0.95,
    "employee_size": 0.85,
    "industry": 0.90
  },
  "data_sources": [
    "official_website",
    "linkedin",
    "crunchbase"
  ],
  "last_updated": "2025-11-19T06:00:00Z"
}
```

## Quality Assurance

### Automated Checks
- URL validation
- Format verification
- Duplicate detection
- Consistency checks

### Manual Review
For low-confidence results:
- Human verification
- Source investigation
- Data correction
- Score update

## Best Practices

### For High-Stakes Decisions
- Use only high-confidence data
- Verify critical fields manually
- Cross-reference multiple sources
- Document verification steps

### For General Research
- Accept good confidence (0.7+)
- Note medium confidence fields
- Plan verification for critical use
- Update data periodically

### For Bulk Operations
- Set minimum confidence threshold
- Flag low-confidence results
- Batch verification
- Track quality metrics

Trust CorpInfo's transparent confidence scoring for data-driven decisions.
"""
    },
    {
        "slug": "rate-limiting-fair-usage",
        "title": "Rate Limiting and Fair Usage: API Guidelines",
        "excerpt": "Understand CorpInfo's rate limiting policies and best practices for optimal API performance.",
        "content": """Rate limiting ensures system stability and fair access for all users. This guide explains CorpInfo's approach and optimization strategies.

## Why Rate Limiting?

### System Protection
- Prevent server overload
- Ensure service availability
- Maintain response times
- Protect infrastructure

### Fair Access
- Equal opportunity for all users
- Prevent abuse
- Sustainable resource allocation
- Quality service delivery

## Rate Limits by Plan

### Free Plan
- 60 requests per minute
- 500 requests per day
- 10 total credits
- Single concurrent request

### Starter Plan ($25)
- 120 requests per minute
- 5,000 requests per day
- 1,000 total credits
- 2 concurrent requests

### Pro Plan ($49)
- 300 requests per minute
- 15,000 requests per day
- 2,500 total credits
- 5 concurrent requests

### Enterprise
- Custom rate limits
- Unlimited daily requests
- Custom credit packages
- Priority processing
- Dedicated resources

## Rate Limit Headers

Every API response includes:

```
X-RateLimit-Limit: 120
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1700000000
```

### Header Meanings
- `Limit`: Requests allowed per window
- `Remaining`: Requests left in window
- `Reset`: Unix timestamp for window reset

## Handling Rate Limits

### Status Code 429
When exceeded:
```json
{
  "error": "Rate limit exceeded",
  "retry_after": 45,
  "limit": 120,
  "window": "1 minute"
}
```

### Response Strategy
1. Check `retry_after` seconds
2. Implement exponential backoff
3. Queue remaining requests
4. Resume after window reset

## Best Practices

### Request Optimization

#### Batch Requests
Use bulk endpoints:
```
POST /api/crawl/bulk-upload
```
Instead of individual requests.

#### Cache Responses
- Store frequently accessed data
- Set appropriate TTL
- Reduce redundant requests

#### Efficient Querying
- Request only needed fields
- Use appropriate limits
- Filter at API level

### Implementation Patterns

#### Exponential Backoff
```python
import time

def make_request_with_backoff(url, max_retries=5):
    for i in range(max_retries):
        response = requests.get(url)
        if response.status_code == 429:
            wait_time = 2 ** i
            time.sleep(wait_time)
            continue
        return response
    raise Exception("Max retries exceeded")
```

#### Rate Limit Tracking
```javascript
class RateLimiter {
  constructor(limit) {
    this.limit = limit;
    this.remaining = limit;
    this.resetTime = Date.now() + 60000;
  }

  async request(fn) {
    if (this.remaining === 0) {
      const wait = this.resetTime - Date.now();
      if (wait > 0) {
        await new Promise(resolve => setTimeout(resolve, wait));
        this.remaining = this.limit;
        this.resetTime = Date.now() + 60000;
      }
    }
    this.remaining--;
    return fn();
  }
}
```

#### Request Queue
```python
from queue import Queue
import threading
import time

class RequestQueue:
    def __init__(self, rate_limit=60):
        self.queue = Queue()
        self.rate_limit = rate_limit
        self.start_worker()
    
    def add_request(self, request_fn):
        self.queue.put(request_fn)
    
    def start_worker(self):
        def worker():
            while True:
                request_fn = self.queue.get()
                request_fn()
                time.sleep(60 / self.rate_limit)
                self.queue.task_done()
        
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
```

## Monitoring Usage

### Dashboard Metrics
Track in your dashboard:
- Current rate limit
- Requests used
- Credits remaining
- Error rates

### API Endpoint
Check usage programmatically:
```
GET /api/usage/current
```

Response:
```json
{
  "plan": "Pro",
  "rate_limit": {
    "requests_per_minute": 300,
    "requests_remaining": 245,
    "window_reset": "2025-11-19T10:15:00Z"
  },
  "credits": {
    "total": 2500,
    "used": 1234,
    "remaining": 1266
  }
}
```

## Fair Usage Policy

### Acceptable Use
✓ Legitimate business purposes
✓ Reasonable request patterns
✓ Respect rate limits
✓ Efficient API usage

### Prohibited Actions
✗ Automated scraping
✗ Circumventing limits
✗ Sharing API credentials
✗ Abusive request patterns
✗ Reselling data

## Optimization Strategies

### Bulk Operations
Process 100+ companies in one upload instead of individual requests.

### Intelligent Caching
Cache company data for:
- Frequently accessed companies
- Recent search results
- Static information

### Off-Peak Processing
Schedule bulk jobs during off-peak hours for better performance.

### Upgrade When Needed
Monitor usage patterns and upgrade before hitting limits regularly.

## Troubleshooting

### Consistent 429 Errors
- Check current plan limits
- Review request patterns
- Consider plan upgrade
- Implement proper backoff

### Slow Response Times
- Check system status
- Reduce request frequency
- Optimize queries
- Use caching

### Credit Exhaustion
- Monitor credit usage
- Set alerts at 80%
- Plan refills in advance
- Upgrade if needed

## Getting Help

### Support Channels
- Email: support@corpinfo.com
- Docs: docs.corpinfo.com
- Status: status.corpinfo.com

### Enterprise Support
- Dedicated account manager
- Custom rate limit configuration
- Priority troubleshooting
- Architecture consultation

Optimize your API usage with CorpInfo's transparent rate limiting system.
"""
    },
    {
        "slug": "startup-founder-company-research",
        "title": "Company Research for Startup Founders: Competitive Intelligence",
        "excerpt": "Essential guide for startup founders to research competitors, partners, and market landscape using company data.",
        "content": """Startup founders need comprehensive market intelligence to make informed decisions. This guide shows how to leverage company data effectively.

## Why Company Research Matters

### For Startup Success
- Understand competition
- Identify partners
- Find investors
- Validate market
- Price products
- Hire talent

### Strategic Advantages
- Market positioning
- Differentiation strategy
- Partnership opportunities
- Investment readiness
- Talent acquisition

## Research Categories

### 1. Competitive Analysis

#### Direct Competitors
Identify companies:
- Same market segment
- Similar product offerings
- Target customer overlap
- Geographic presence

#### Data to Collect
- Company size (employees)
- Funding history
- Growth trajectory
- Product features
- Pricing models
- Customer base
- Market share

#### Using CorpInfo
```
1. Search competitor domains
2. Get LinkedIn URLs
3. Analyze employee count trends
4. Track company news
5. Monitor growth signals
```

### 2. Partner Discovery

#### Potential Partners
Find companies that:
- Serve complementary markets
- Share target customers
- Have synergistic products
- Align strategically

#### Evaluation Criteria
- Company stability
- Market reputation
- Technical compatibility
- Strategic fit
- Growth stage

### 3. Investor Research

#### Target Investors
Research:
- Portfolio companies
- Investment thesis
- Ticket sizes
- Stage focus
- Industry preferences

#### Approach Strategy
- Warm introductions
- Relevant traction
- Market validation
- Competitive positioning

### 4. Market Mapping

#### Industry Landscape
Map your market:
- Total companies
- Size distribution
- Geographic spread
- Growth trends
- Market gaps

#### Opportunity Identification
- Underserved segments
- Emerging trends
- Market consolidation
- Technology shifts

## Research Workflow

### Phase 1: List Building

#### Competitor List
1. Direct competitors (obvious ones)
2. Google search competitors
3. Category leaders
4. Emerging players

#### Partner List
1. Complementary products
2. Distribution channels
3. Technology partners
4. Strategic alliances

### Phase 2: Data Collection

Use CorpInfo to gather:
- Company names → domains
- Domains → LinkedIn URLs
- LinkedIn → employee data
- Websites → contact info
- News → recent activities

### Phase 3: Analysis

#### Comparative Analysis
Create spreadsheet with:
- Company names
- Employee counts
- Funding amounts
- Years founded
- Growth rates
- Key products
- Target markets

#### Visualization
- Market map diagrams
- Competitive positioning
- Growth charts
- Feature comparison matrices

### Phase 4: Insights

#### Strategic Questions
- Where are market gaps?
- Who are rising competitors?
- What's working for others?
- Where should we focus?
- Who should we partner with?

## Specific Use Cases

### Product Development

#### Feature Comparison
- Competitors' offerings
- Market expectations
- Differentiation opportunities
- Pricing insights

#### Technology Stack
Research competitors':
- Technologies used
- Technical hiring
- Product architecture
- Innovation pace

### Pricing Strategy

#### Market Research
Analyze competitors':
- Pricing models
- Price points
- Value propositions
- Packaging strategies

#### Positioning
- Premium vs. budget
- Feature comparison
- Value messaging
- Target segments

### Hiring Strategy

#### Talent Pool
Identify companies:
- Similar stage
- Same tech stack
- Facing challenges
- Restructuring
- Geographic proximity

#### Compensation Benchmarks
Research:
- Company sizes
- Funding stages
- Location factors
- Role expectations

### Fundraising Prep

#### Investor Targets
Research:
- Portfolio companies
- Investment sizes
- Success stories
- Strategic focus

#### Pitch Preparation
- Market size data
- Competitor analysis
- Growth benchmarks
- Traction metrics

## Tools and Techniques

### CorpInfo Features

#### Bulk Processing
Upload competitor list:
```csv
company_name,domain
Competitor A,competitora.com
Competitor B,competitorb.com
Partner X,partnerx.com
```

#### Search and Filter
```
GET /api/crawl/search?query=fintech&industry=financial
```

#### Export Data
Download enriched data:
- CSV for analysis
- JSON for integration
- Excel for sharing

### Complementary Tools

#### Market Intelligence
- Crunchbase (funding data)
- LinkedIn Sales Navigator
- Google Trends
- SimilarWeb (traffic data)

#### Competitive Tracking
- Product Hunt
- G2 reviews
- Capterra ratings
- Social media monitoring

## Monitoring Strategy

### Regular Updates

#### Quarterly Deep Dive
- Competitor funding rounds
- Product launches
- Team growth
- Market moves

#### Monthly Check
- News mentions
- Employee changes
- Content publishing
- Social activity

#### Weekly Alerts
- Major announcements
- Executive changes
- Funding news
- Product updates

### Automation

#### Set Up Alerts
- Google Alerts for competitors
- LinkedIn notifications
- News feed subscriptions
- Industry newsletters

#### Automated Tracking
- Regular CorpInfo searches
- Data refresh schedules
- Change detection
- Report generation

## Best Practices

### Do's
✓ Stay updated continuously
✓ Verify data from multiple sources
✓ Focus on actionable insights
✓ Document key findings
✓ Share with team

### Don'ts
✗ Copy competitors blindly
✗ Ignore emerging players
✗ Rely on outdated data
✗ Forget about partners
✗ Skip market context

## Privacy and Ethics

### Ethical Research
- Use public information only
- Respect privacy laws
- Don't misrepresent yourself
- Follow terms of service

### Legal Compliance
- GDPR considerations
- Copyright respect
- Trademark awareness
- Fair competition

## Taking Action

### Strategic Planning
Use research for:
- Product roadmap
- Marketing strategy
- Sales approach
- Partnership deals
- Hiring plans
- Fundraising strategy

### Execution
- Prioritize opportunities
- Test hypotheses
- Measure results
- Iterate quickly
- Stay informed

Build your startup on solid market intelligence with CorpInfo's comprehensive company data platform.
"""
    }
]

INITIAL_FAQS = [
    {
        "question": "How accurate is the LinkedIn URL finder?",
        "answer": "Our LinkedIn URL finder achieves 85-95% accuracy through multi-source verification. Each result includes a confidence score, allowing you to assess reliability. We prioritize direct website links and cross-reference multiple sources for validation.",
        "category": "Accuracy",
        "order": 1
    },
    {
        "question": "What data sources does CorpInfo crawl?",
        "answer": "We crawl in priority order: 1) Official company websites, 2) LinkedIn company pages, 3) News aggregators, 4) Business databases like Crunchbase. This ensures you get the most accurate and up-to-date information.",
        "category": "Features",
        "order": 2
    },
    {
        "question": "How does bulk upload work?",
        "answer": "Simply upload a CSV or Excel file with company names, domains, or LinkedIn URLs (one per row). Our system processes each entry, maintains the original sequence, and generates a downloadable report with all enriched data.",
        "category": "Features",
        "order": 3
    },
    {
        "question": "What's included in company data enrichment?",
        "answer": "We provide: company name, domain, LinkedIn URL, industry, employee size, founded date, founders, description, address, phone numbers, emails, social media URLs, and latest news. Not all fields are available for every company.",
        "category": "Features",
        "order": 4
    },
    {
        "question": "How does the credit system work?",
        "answer": "Each successful search costs 1 credit. Free plan includes 10 credits. Starter ($25) provides 1,000 credits. Pro ($49) includes 2,500 credits. Enterprise plans offer custom volumes with volume discounts.",
        "category": "Pricing",
        "order": 5
    },
    {
        "question": "Can I get a refund if data is inaccurate?",
        "answer": "We provide confidence scores with each result. If you find inaccuracies in high-confidence results, contact support with details. We review each case and may issue credit refunds for verified inaccuracies.",
        "category": "Pricing",
        "order": 6
    },
    {
        "question": "Is API access available?",
        "answer": "Yes! Pro and Enterprise plans include API access. We provide RESTful API endpoints and MCP server support for seamless integration with your applications and workflows.",
        "category": "Technical",
        "order": 7
    },
    {
        "question": "How long does crawling take?",
        "answer": "Single searches typically complete in 5-15 seconds. Bulk uploads process at approximately 100-200 requests per minute depending on server load. You'll receive notifications when bulk jobs complete.",
        "category": "Technical",
        "order": 8
    },
    {
        "question": "Is my data secure?",
        "answer": "Yes. We use encryption for data transmission and storage. Your search history and uploaded files are private and accessible only to you. We're GDPR compliant and never share your data with third parties.",
        "category": "Security",
        "order": 9
    },
    {
        "question": "What if I can't find a company's LinkedIn?",
        "answer": "Some companies don't have LinkedIn pages or have unlisted pages. Our crawler will still provide available data from other sources. Results include a status indicating whether LinkedIn was found and the confidence level.",
        "category": "Troubleshooting",
        "order": 10
    }
]

async def init_content():
    """Initialize blogs and FAQs"""
    client = AsyncIOMotorClient(settings.MONGO_URL)
    db = client[settings.DB_NAME]
    
    print("Initializing blog posts...")
    for blog_data in INITIAL_BLOGS:
        existing = await db.blogs.find_one({"slug": blog_data["slug"]})
        if not existing:
            blog = Blog(
                **blog_data,
                author="CorpInfo Team",
                is_published=True
            )
            blog_dict = blog.model_dump()
            blog_dict['created_at'] = blog_dict['created_at'].isoformat()
            blog_dict['updated_at'] = blog_dict['updated_at'].isoformat()
            await db.blogs.insert_one(blog_dict)
            print(f"  ✓ Created blog: {blog_data['title']}")
        else:
            print(f"  - Blog already exists: {blog_data['title']}")
    
    print("\nInitializing FAQs...")
    for faq_data in INITIAL_FAQS:
        faq = FAQ(**faq_data, is_published=True)
        faq_dict = faq.model_dump()
        faq_dict['created_at'] = faq_dict['created_at'].isoformat()
        faq_dict['updated_at'] = faq_dict['updated_at'].isoformat()
        await db.faqs.insert_one(faq_dict)
        print(f"  ✓ Created FAQ: {faq_data['question'][:50]}...")
    
    print("\n✓ Content initialization complete!")
    client.close()

if __name__ == "__main__":
    asyncio.run(init_content())
