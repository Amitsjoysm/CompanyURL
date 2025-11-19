#!/usr/bin/env python3
"""
Check database collections
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def check_db():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["corpinfo_db"]
    
    # List all collections
    collections = await db.list_collection_names()
    print(f"Collections: {collections}")
    
    # Check if api_tokens collection exists
    if "api_tokens" in collections:
        count = await db.api_tokens.count_documents({})
        print(f"API tokens count: {count}")
    else:
        print("API tokens collection does not exist")
    
    # Check users
    if "users" in collections:
        users = await db.users.find({}).to_list(10)
        print(f"Users: {len(users)}")
        for user in users:
            print(f"  - {user.get('email')} ({user.get('role')})")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check_db())