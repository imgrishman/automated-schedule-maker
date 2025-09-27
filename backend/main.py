from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import asyncio

# Load environment variables
load_dotenv()

# Create FastAPI app with lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting Automated Schedule Planner API...")
    try:
        # Initialize database connection
        from database.connection import get_database
        db = await get_database()
        print("✅ Database connection established")
        
        # Setup sample data
        await setup_sample_data()
        print("✅ Sample data initialized")
        
    except Exception as e:
        print(f"⚠️  Database setup warning: {e}")
        print("📝 App will continue with limited functionality")
    
    yield
    
    # Shutdown
    print("🛑 Server shutting down...")

app = FastAPI(
    title="Automated Schedule Planner API",
    description="AI-Powered Workforce Scheduling System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware - Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Sample data for demo
SAMPLE_USERS = {
    "admin@asp.com": {
        "id": "admin_001",
        "email": "admin@asp.com",
        "password": "admin123",  # In production, this would be hashed
        "name": "Admin User",
        "role": "admin",
        "department": "Management"
    },
    "demo@asp.com": {
        "id": "emp_001", 
        "email": "demo@asp.com",
        "password": "demo123",
        "name": "Demo Employee",
        "role": "employee",
        "department": "Operations"
    },
    "manager@asp.com": {
        "id": "mgr_001",
        "email": "manager@asp.com", 
        "password": "manager123",
        "name": "Manager User",
        "role": "manager",
        "department": "Operations"
    }
}

async def setup_sample_data():
    """Setup sample data for demo purposes"""
    try:
        from database.connection import get_database
        db = await get_database()
        
        # Check if users already exist
        users_collection = db.users
        existing_users = await users_collection.count_documents({})
        
        if existing_users == 0:
            print("📝 Setting up sample users...")
            for email, user_data in SAMPLE_USERS.items():
                await users_collection.insert_one(user_data)
            print("✅ Sample users created")
        else:
            print("✅ Sample data already exists")
            
    except Exception as e:
        print(f"⚠️  Sample data setup failed: {e}")

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Automated Schedule Planner API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/api/health",
        "timestamp": datetime.utcnow().isoformat()
    }

# Health check endpoint
@app.get("/api/health")
async def health_check():
    try:
        from database.connection import get_database
        db = await get_database()
        # Test database connection
        await db.command("ping")
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.utcnow().isoformat(),
            "message": "API is running successfully"
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
        )

# Authentication endpoints
@app.post("/api/auth/login")
async def login(credentials: dict):
    """Login endpoint"""
    email = credentials.get("email")
    password = credentials.get("password")
    
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password required")
    
    # Check against sample users
    user = SAMPLE_USERS.get(email)
    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create response without password
    user_response = {k: v for k, v in user.items() if k != "password"}
    
    return {
        "access_token": f"demo_token_{user['id']}",
        "token_type": "bearer",
        "user": user_response
    }

@app.post("/api/auth/demo-login")
async def demo_login(demo_type: str):
    """Demo login endpoint"""
    if demo_type == "admin":
        user = SAMPLE_USERS["admin@asp.com"]
    elif demo_type == "employee":
        user = SAMPLE_USERS["demo@asp.com"]
    else:
        raise HTTPException(status_code=400, detail="Invalid demo type")
    
    # Create response without password
    user_response = {k: v for k, v in user.items() if k != "password"}
    
    return {
        "access_token": f"demo_token_{user['id']}",
        "token_type": "bearer", 
        "user": user_response
    }

# Employee endpoints
@app.get("/api/employees/")
async def get_employees():
    """Get all employees"""
    employees = []
    for user in SAMPLE_USERS.values():
        if user["role"] in ["employee", "manager"]:
            employee_data = {k: v for k, v in user.items() if k != "password"}
            employees.append(employee_data)
    return employees

@app.get("/api/employees/me")
async def get_my_profile():
    """Get current user profile"""
    # For demo, return admin user
    user = SAMPLE_USERS["admin@asp.com"]
    return {k: v for k, v in user.items() if k != "password"}

# Schedule endpoints
@app.get("/api/schedules/")
async def get_schedules():
    """Get all schedules"""
    return [
        {
            "id": "schedule_001",
            "name": "Week 1 - January 2025",
            "start_date": "2025-01-06",
            "end_date": "2025-01-12",
            "status": "published",
            "created_by": "admin_001",
            "ai_score": 95
        },
        {
            "id": "schedule_002", 
            "name": "Week 2 - January 2025",
            "start_date": "2025-01-13",
            "end_date": "2025-01-19",
            "status": "draft",
            "created_by": "admin_001",
            "ai_score": 88
        }
    ]

@app.post("/api/schedules/generate")
async def generate_schedule(data: dict):
    """Generate AI-optimized schedule"""
    return {
        "id": "schedule_new",
        "name": f"Generated Schedule - {datetime.now().strftime('%B %Y')}",
        "start_date": datetime.now().strftime("%Y-%m-%d"),
        "end_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
        "status": "draft",
        "ai_score": 92,
        "message": "Schedule generated successfully using AI optimization"
    }

# Availability endpoints
@app.get("/api/availability/")
async def get_availability():
    """Get availability data"""
    return [
        {
            "id": "avail_001",
            "employee_id": "emp_001",
            "day_of_week": "monday",
            "start_time": "09:00",
            "end_time": "17:00",
            "available": True
        },
        {
            "id": "avail_002",
            "employee_id": "emp_001", 
            "day_of_week": "tuesday",
            "start_time": "09:00",
            "end_time": "17:00",
            "available": True
        }
    ]

# Analytics endpoints
@app.get("/api/analytics/dashboard")
async def get_dashboard_analytics():
    """Get dashboard analytics"""
    return {
        "total_employees": 25,
        "active_schedules": 3,
        "pending_requests": 7,
        "satisfaction_score": 4.2,
        "efficiency_score": 87,
        "recent_activity": [
            {"action": "Schedule published", "time": "2 hours ago"},
            {"action": "New employee added", "time": "4 hours ago"},
            {"action": "Availability updated", "time": "6 hours ago"}
        ]
    }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Endpoint not found"}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    print("🚀 Starting Automated Schedule Planner API...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔗 Health Check: http://localhost:8000/api/health")
    print("🌐 CORS enabled for all origins")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
