#!/usr/bin/env python3
"""
Debug user management
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def debug_users():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["corpinfo_db"]
    
    # Get all users
    users = await db.users.find({}).to_list(10)
    print(f"Users: {len(users)}")
    for user in users:
        print(f"  - ID: {user.get('id')}")
        print(f"    Email: {user.get('email')}")
        print(f"    Role: {user.get('role')}")
        print(f"    Credits: {user.get('credits')}")
        print(f"    Plan: {user.get('current_plan')}")
        print(f"    Active: {user.get('is_active')}")
        print()
    
    client.close()

if __name__ == "__main__":
    asyncio.run(debug_users())