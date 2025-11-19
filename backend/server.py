from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, FileResponse
from core.config import get_settings
from core.database import db_instance
from routers import auth, crawl, payment, content
import logging
from contextlib import asynccontextmanager
from services.payment_service import PaymentService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("Starting CorpInfo API...")
    db_instance.connect()
    
    # Initialize plans
    payment_service = PaymentService(db_instance.get_db())
    await payment_service.initialize_plans()
    
    logger.info("CorpInfo API started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down CorpInfo API...")
    db_instance.close()

app = FastAPI(
    title="CorpInfo API",
    description="Production-ready company information crawler",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=settings.CORS_ORIGINS.split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with /api prefix
app.include_router(auth.router, prefix="/api")
app.include_router(crawl.router, prefix="/api")
app.include_router(payment.router, prefix="/api")
app.include_router(content.router, prefix="/api")

# Health check
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "CorpInfo API"}

@app.get("/api/")
async def root():
    return {
        "message": "CorpInfo API",
        "version": "1.0.0",
        "docs": "/docs"
    }

# SEO files
@app.get("/robots.txt", response_class=PlainTextResponse)
async def robots():
    return """User-agent: *
Disallow: /api/
Allow: /

Sitemap: https://corpinfo.preview.emergentagent.com/sitemap.xml
"""

@app.get("/sitemap.xml", response_class=PlainTextResponse)
async def sitemap():
    """Generate sitemap"""
    # Get all blog slugs
    from core.database import get_db
    db = get_db()
    blogs = await db.blogs.find({"is_published": True}, {"_id": 0, "slug": 1}).to_list(100)
    
    urls = [
        '<url><loc>https://corpinfo.preview.emergentagent.com/</loc><priority>1.0</priority></url>',
        '<url><loc>https://corpinfo.preview.emergentagent.com/pricing</loc><priority>0.9</priority></url>',
        '<url><loc>https://corpinfo.preview.emergentagent.com/faq</loc><priority>0.8</priority></url>',
        '<url><loc>https://corpinfo.preview.emergentagent.com/blogs</loc><priority>0.8</priority></url>',
    ]
    
    for blog in blogs:
        urls.append(f'<url><loc>https://corpinfo.preview.emergentagent.com/blog/{blog["slug"]}</loc><priority>0.7</priority></url>')
    
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{"".join(urls)}
</urlset>'''

@app.get("/llms.txt", response_class=PlainTextResponse)
async def llms_txt():
    """LLMs.txt for AI crawlers"""
    return """# CorpInfo: Company Information Crawler
> Production-ready platform for converting company names to domains, domains to LinkedIn URLs, and comprehensive company data enrichment.

## Core Features
- [Company Domain Finder](https://corpinfo.preview.emergentagent.com/)
- [LinkedIn URL Lookup](https://corpinfo.preview.emergentagent.com/)
- [Bulk Company Data Enrichment](https://corpinfo.preview.emergentagent.com/)
- [Pricing Plans](https://corpinfo.preview.emergentagent.com/pricing)

## Guides & Resources
- [How to Find Company LinkedIn Pages](https://corpinfo.preview.emergentagent.com/blog/find-linkedin-company-url)
- [Company Domain to LinkedIn Converter](https://corpinfo.preview.emergentagent.com/blog/domain-to-linkedin)
- [FAQ: Company Finder Tool](https://corpinfo.preview.emergentagent.com/faq)

## API Access
- [API Documentation](https://corpinfo.preview.emergentagent.com/docs)
- [Authentication Guide](https://corpinfo.preview.emergentagent.com/blog/api-authentication)
"""
