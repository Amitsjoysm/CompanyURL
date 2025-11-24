"""
Create superadmin user for CorpInfo
Run this script to create the initial admin account
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from core.config import get_settings
from core.auth import get_password_hash
from models.user import User
from datetime import datetime, timezone

settings = get_settings()

async def create_admin():
    """Create superadmin user"""
    client = AsyncIOMotorClient(settings.MONGO_URL)
    db = client[settings.DB_NAME]
    
    # Admin credentials
    admin_email = "admin@corpinfo.com"
    admin_password = "Admin@2025!Secure"
    
    # Check if admin already exists
    existing_admin = await db.users.find_one({"email": admin_email})
    
    if existing_admin:
        print(f"❌ Admin user already exists with email: {admin_email}")
        client.close()
        return
    
    # Create admin user with hashed password
    hashed_pwd = get_password_hash(admin_password)
    admin_user = User(
        email=admin_email,
        full_name="System Administrator",
        hashed_password=hashed_pwd,
        role="superadmin",
        credits=10000,  # Give admin plenty of credits
        created_at=datetime.now(timezone.utc),
        is_active=True
    )
    
    admin_dict = admin_user.model_dump()
    
    await db.users.insert_one(admin_dict)
    
    print("✅ Superadmin user created successfully!")
    print("\n" + "="*60)
    print("ADMIN CREDENTIALS")
    print("="*60)
    print(f"Email: {admin_email}")
    print(f"Password: {admin_password}")
    print("="*60)
    print("\n⚠️  Please change the password after first login!")
    print("⚠️  Store these credentials securely!")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(create_admin())
