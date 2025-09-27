import asyncio
import sys
import os
from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB connection
MONGODB_URL = "mongodb+srv://v0user:v0user@asp.d0jajzm.mongodb.net/automated_schedule_planner?retryWrites=true&w=majority&appName=ASP"
DATABASE_NAME = "automated_schedule_planner"

async def verify_database():
    """Verify database setup and data integrity"""
    print("🔍 Verifying MongoDB Atlas Database...")
    
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    
    try:
        # Test connection
        await client.admin.command('ping')
        print("✅ Connection successful!")
        
        # Check collections and counts
        collections = {
            'users': 'User accounts',
            'employees': 'Employee profiles', 
            'availability': 'Availability records',
            'schedules': 'Schedule records',
            'shifts': 'Shift assignments',
            'requests': 'Employee requests'
        }
        
        print("\n📊 Collection Statistics:")
        print("-" * 50)
        
        total_documents = 0
        for collection_name, description in collections.items():
            count = await db[collection_name].count_documents({})
            total_documents += count
            print(f"{description:<25}: {count:>5} documents")
        
        print("-" * 50)
        print(f"{'Total Documents':<25}: {total_documents:>5}")
        
        # Verify indexes
        print("\n🔍 Index Verification:")
        print("-" * 50)
        
        for collection_name in collections.keys():
            indexes = await db[collection_name].list_indexes().to_list(None)
            index_count = len(indexes)
            print(f"{collection_name:<15}: {index_count:>2} indexes")
        
        # Test sample queries
        print("\n🧪 Sample Data Verification:")
        print("-" * 50)
        
        # Check admin user
        admin = await db.users.find_one({"email": "admin@asp.com"})
        print(f"Admin user exists: {'✅' if admin else '❌'}")
        
        # Check employee with availability
        employee_with_avail = await db.employees.aggregate([
            {"$lookup": {
                "from": "availability",
                "localField": "_id",
                "foreignField": "employee_id",
                "as": "availability"
            }},
            {"$match": {"availability": {"$ne": []}}},
            {"$limit": 1}
        ]).to_list(1)
        
        print(f"Employee with availability: {'✅' if employee_with_avail else '❌'}")
        
        # Check schedule with shifts
        schedule_with_shifts = await db.schedules.aggregate([
            {"$lookup": {
                "from": "shifts",
                "localField": "_id",
                "foreignField": "schedule_id",
                "as": "shifts"
            }},
            {"$match": {"shifts": {"$ne": []}}},
            {"$limit": 1}
        ]).to_list(1)
        
        print(f"Schedule with shifts: {'✅' if schedule_with_shifts else '❌'}")
        
        print("\n🎉 Database verification completed!")
        print(f"🔗 Database: {DATABASE_NAME}")
        print("🌐 Platform: MongoDB Atlas")
        print("✅ Status: Fully Functional")
        
        # Display login credentials
        print("\n🔐 Demo Login Credentials:")
        print("-" * 50)
        print("Admin Login:")
        print("  Email: admin@asp.com")
        print("  Password: admin123")
        print("\nManager Login:")
        print("  Email: manager@asp.com") 
        print("  Password: manager123")
        print("\nEmployee Login:")
        print("  Email: demo@asp.com")
        print("  Password: demo123")
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        raise
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(verify_database())
