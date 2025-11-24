from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os

async def check_ledger():
    mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    db_name = os.getenv("DB_NAME", "corpinfo_db")
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    # Check both collections
    central_ledger_count = await db.central_ledger.count_documents({})
    companies_count = await db.companies.count_documents({})
    
    print(f"Central Ledger Collection: {central_ledger_count} documents")
    print(f"Companies Collection: {companies_count} documents")
    
    # Get samples
    if central_ledger_count > 0:
        print("\nSample from central_ledger:")
        sample = await db.central_ledger.find_one({})
        print(sample)
    
    if companies_count > 0:
        print("\nSample from companies:")
        sample = await db.companies.find_one({})
        print(sample)

asyncio.run(check_ledger())
