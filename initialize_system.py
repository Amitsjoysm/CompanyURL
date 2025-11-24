#!/usr/bin/env python3
"""
System Initialization Script
- Creates database indexes
- Initializes default data
- Verifies setup
"""
import asyncio
import sys
import os
from motor.motor_asyncio import AsyncIOMotorClient
from core.db_indexes import create_indexes
from backend.init_data import init_data

async def initialize():
    """Initialize the system"""
    try:
        # Connect to MongoDB
        mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        db_name = os.getenv("DB_NAME", "corpinfo_db")
        
        print(f"🔌 Connecting to MongoDB: {mongo_url}")
        client = AsyncIOMotorClient(mongo_url)
        db = client[db_name]
        
        # Test connection
        await db.command("ping")
        print("✅ MongoDB connection successful")
        
        # Create indexes
        print("\n📊 Creating database indexes...")
        await create_indexes(db)
        
        # List all collections and their indexes
        print("\n📋 Database Collections:")
        collections = await db.list_collection_names()
        for coll_name in sorted(collections):
            indexes = await db[coll_name].list_indexes().to_list(None)
            print(f"  - {coll_name}: {len(indexes)} indexes")
        
        # Verify collections
        print("\n🔍 Verifying setup...")
        
        # Check users
        user_count = await db.users.count_documents({})
        print(f"  - Users: {user_count}")
        
        # Check plans
        plan_count = await db.plans.count_documents({})
        print(f"  - Plans: {plan_count}")
        
        # Check central ledger
        ledger_count = await db.central_ledger.count_documents({})
        print(f"  - Central Ledger: {ledger_count} companies")
        
        # Check blogs
        blog_count = await db.blogs.count_documents({})
        print(f"  - Blogs: {blog_count}")
        
        # Check FAQs
        faq_count = await db.faqs.count_documents({})
        print(f"  - FAQs: {faq_count}")
        
        # Check exchange rate setting
        exchange_rate = await db.settings.find_one({"key": "exchange_rate"})
        if exchange_rate:
            print(f"  - Exchange Rate: USD 1 = INR {exchange_rate.get('usd_to_inr_rate', 'Not set')}")
        else:
            # Set default exchange rate
            await db.settings.insert_one({
                "key": "exchange_rate",
                "usd_to_inr_rate": 83.0,
                "updated_at": "2024-01-01T00:00:00"
            })
            print(f"  - Exchange Rate: USD 1 = INR 83.0 (default set)")
        
        print("\n✅ System initialization complete!")
        print("\n📚 Next steps:")
        print("  1. Verify admin credentials:")
        print("     - Email: admin@test.com")
        print("     - Password: Admin@123")
        print("  2. Test API endpoints")
        print("  3. Check HubSpot integration")
        print("  4. Test multi-currency payments")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during initialization: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        client.close()

if __name__ == "__main__":
    sys.path.insert(0, "/app/backend")
    result = asyncio.run(initialize())
    sys.exit(0 if result else 1)
