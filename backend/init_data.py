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
