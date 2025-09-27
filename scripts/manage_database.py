import asyncio
import sys
from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URL = "mongodb+srv://v0user:v0user@asp.d0jajzm.mongodb.net/automated_schedule_planner?retryWrites=true&w=majority&appName=ASP"
DATABASE_NAME = "automated_schedule_planner"

async def reset_database():
    """Reset database - clear all data"""
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    
    try:
        collections = ['users', 'employees', 'availability', 'schedules', 'shifts', 'requests']
        for collection in collections:
            result = await db[collection].delete_many({})
            print(f"Cleared {result.deleted_count} documents from {collection}")
        
        print("✅ Database reset completed!")
        
    except Exception as e:
        print(f"❌ Reset failed: {e}")
    finally:
        client.close()

async def backup_database():
    """Create a simple backup by exporting collection counts"""
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    
    try:
        print("📊 Database Backup Summary:")
        print("-" * 40)
        
        collections = ['users', 'employees', 'availability', 'schedules', 'shifts', 'requests']
        for collection in collections:
            count = await db[collection].count_documents({})
            print(f"{collection}: {count} documents")
        
        print("✅ Backup summary completed!")
        
    except Exception as e:
        print(f"❌ Backup failed: {e}")
    finally:
        client.close()

async def main():
    if len(sys.argv) < 2:
        print("Usage: python manage_database.py [reset|backup]")
        return
    
    command = sys.argv[1]
    
    if command == "reset":
        confirm = input("⚠️  Are you sure you want to reset the database? (yes/no): ")
        if confirm.lower() == "yes":
            await reset_database()
        else:
            print("Reset cancelled.")
    elif command == "backup":
        await backup_database()
    else:
        print("Unknown command. Use 'reset' or 'backup'")

if __name__ == "__main__":
    asyncio.run(main())
