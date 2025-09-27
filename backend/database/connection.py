import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

class Database:
    client: AsyncIOMotorClient = None
    database = None

db = Database()

async def get_database():
    """Get database instance"""
    if db.database is None:
        try:
            # Try to connect to MongoDB
            mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
            db.client = AsyncIOMotorClient(mongodb_url)
            db.database = db.client[os.getenv("DATABASE_NAME", "automated_schedule_planner")]
            
            # Test connection
            await db.client.admin.command('ping')
            print("✅ MongoDB connection successful")
            
        except Exception as e:
            print(f"⚠️  MongoDB connection failed: {e}")
            print("📝 Using in-memory data for demo")
            # Return a mock database object for demo purposes
            return MockDatabase()
    
    return db.database

async def init_db():
    """Initialize database connection"""
    return await get_database()

class MockDatabase:
    """Mock database for demo purposes when MongoDB is not available"""
    
    def __init__(self):
        self.collections = {}
    
    def __getattr__(self, name):
        if name not in self.collections:
            self.collections[name] = MockCollection()
        return self.collections[name]
    
    async def command(self, cmd):
        if cmd == "ping":
            return {"ok": 1}
        return {"ok": 1}

class MockCollection:
    """Mock collection for demo purposes"""
    
    def __init__(self):
        self.data = []
    
    async def find(self, query=None):
        return MockCursor(self.data)
    
    async def find_one(self, query):
        return None
    
    async def insert_one(self, document):
        self.data.append(document)
        return MockInsertResult()
    
    async def update_one(self, query, update):
        return MockUpdateResult()
    
    async def delete_one(self, query):
        return MockDeleteResult()
    
    async def count_documents(self, query):
        return len(self.data)

class MockCursor:
    def __init__(self, data):
        self.data = data
    
    def to_list(self, length=None):
        return self.data[:length] if length else self.data

class MockInsertResult:
    def __init__(self):
        self.inserted_id = "mock_id"

class MockUpdateResult:
    def __init__(self):
        self.modified_count = 1

class MockDeleteResult:
    def __init__(self):
        self.deleted_count = 1
