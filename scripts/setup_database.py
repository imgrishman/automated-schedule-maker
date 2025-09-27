import asyncio
import sys
import os
from datetime import datetime, date, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
import random

# Add parent directory to path to import models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user import UserRole, UserStatus
from models.employee import EmployeeStatus, ContractType
from models.availability import WeeklyAvailability, DayAvailability
from models.schedule import ScheduleStatus, ShiftStatus

# MongoDB connection
MONGODB_URL = "mongodb+srv://v0user:v0user@asp.d0jajzm.mongodb.net/automated_schedule_planner?retryWrites=true&w=majority&appName=ASP"
DATABASE_NAME = "automated_schedule_planner"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def setup_database():
    """Complete database setup with collections, indexes, and seed data"""
    print("🚀 Starting MongoDB Atlas Database Setup...")
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    
    try:
        # Test connection
        await client.admin.command('ping')
        print("✅ Connected to MongoDB Atlas successfully!")
        
        # Create collections and indexes
        await create_collections_and_indexes(db)
        
        # Seed initial data
        await seed_initial_data(db)
        
        print("🎉 Database setup completed successfully!")
        print(f"📊 Database: {DATABASE_NAME}")
        print("🔗 Connection: MongoDB Atlas")
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        raise
    finally:
        client.close()

async def create_collections_and_indexes(db):
    """Create all collections with proper indexes"""
    print("📋 Creating collections and indexes...")
    
    # Users collection
    await db.users.create_index("email", unique=True)
    await db.users.create_index("employee_id", unique=True, sparse=True)
    await db.users.create_index([("role", 1), ("status", 1)])
    print("✅ Users collection indexed")
    
    # Employees collection
    await db.employees.create_index("user_id", unique=True)
    await db.employees.create_index("employee_id", unique=True)
    await db.employees.create_index("department")
    await db.employees.create_index("status")
    await db.employees.create_index([("department", 1), ("status", 1)])
    print("✅ Employees collection indexed")
    
    # Availability collection
    await db.availability.create_index("employee_id")
    await db.availability.create_index([("employee_id", 1), ("effective_date", -1)])
    print("✅ Availability collection indexed")
    
    # Schedules collection
    await db.schedules.create_index([("week_start", 1), ("status", 1)])
    await db.schedules.create_index("created_by")
    await db.schedules.create_index([("status", 1), ("created_at", -1)])
    print("✅ Schedules collection indexed")
    
    # Shifts collection
    await db.shifts.create_index([("schedule_id", 1), ("employee_id", 1)])
    await db.shifts.create_index([("employee_id", 1), ("date", 1)])
    await db.shifts.create_index([("date", 1), ("start_time", 1)])
    await db.shifts.create_index("status")
    print("✅ Shifts collection indexed")
    
    # Requests collection
    await db.requests.create_index("employee_id")
    await db.requests.create_index([("status", 1), ("created_at", -1)])
    await db.requests.create_index([("employee_id", 1), ("status", 1)])
    print("✅ Requests collection indexed")

async def seed_initial_data(db):
    """Seed the database with initial data"""
    print("🌱 Seeding initial data...")
    
    # Clear existing data
    collections = ['users', 'employees', 'availability', 'schedules', 'shifts', 'requests']
    for collection in collections:
        await db[collection].delete_many({})
    
    # Create admin users
    admin_users = await create_admin_users(db)
    
    # Create employees
    employees = await create_employees(db, admin_users)
    
    # Create availability data
    await create_availability_data(db, employees)
    
    # Create sample schedules
    await create_sample_schedules(db, admin_users, employees)
    
    # Create sample requests
    await create_sample_requests(db, employees)
    
    print("✅ Initial data seeded successfully!")

async def create_admin_users(db):
    """Create admin and demo users"""
    print("👥 Creating admin users...")
    
    users_data = [
        {
            "email": "admin@asp.com",
            "password": "admin123",
            "first_name": "System",
            "last_name": "Administrator",
            "role": UserRole.ADMIN,
            "status": UserStatus.ACTIVE
        },
        {
            "email": "manager@asp.com",
            "password": "manager123",
            "first_name": "John",
            "last_name": "Manager",
            "role": UserRole.MANAGER,
            "status": UserStatus.ACTIVE
        },
        {
            "email": "demo@asp.com",
            "password": "demo123",
            "first_name": "Demo",
            "last_name": "User",
            "role": UserRole.EMPLOYEE,
            "status": UserStatus.ACTIVE
        }
    ]
    
    created_users = []
    for user_data in users_data:
        hashed_password = pwd_context.hash(user_data.pop("password"))
        user_doc = {
            **user_data,
            "hashed_password": hashed_password,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = await db.users.insert_one(user_doc)
        user_doc["_id"] = result.inserted_id
        created_users.append(user_doc)
    
    print(f"✅ Created {len(created_users)} admin users")
    return created_users

async def create_employees(db, admin_users):
    """Create employee profiles"""
    print("👷 Creating employee profiles...")
    
    # Sample employee data
    employee_names = [
        ("Alice", "Johnson", "alice.johnson@asp.com"),
        ("Bob", "Smith", "bob.smith@asp.com"),
        ("Carol", "Davis", "carol.davis@asp.com"),
        ("David", "Wilson", "david.wilson@asp.com"),
        ("Emma", "Brown", "emma.brown@asp.com"),
        ("Frank", "Miller", "frank.miller@asp.com"),
        ("Grace", "Taylor", "grace.taylor@asp.com"),
        ("Henry", "Anderson", "henry.anderson@asp.com"),
        ("Ivy", "Thomas", "ivy.thomas@asp.com"),
        ("Jack", "Jackson", "jack.jackson@asp.com")
    ]
    
    departments = ["Sales", "Customer Service", "Kitchen", "Management", "Maintenance"]
    positions = ["Associate", "Senior Associate", "Team Lead", "Supervisor", "Specialist"]
    
    created_employees = []
    
    for i, (first_name, last_name, email) in enumerate(employee_names):
        # Create user account
        user_doc = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "hashed_password": pwd_context.hash("employee123"),
            "role": UserRole.EMPLOYEE,
            "status": UserStatus.ACTIVE,
            "employee_id": f"EMP{1000 + i}",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        user_result = await db.users.insert_one(user_doc)
        user_id = str(user_result.inserted_id)
        
        # Create employee profile
        employee_doc = {
            "user_id": user_id,
            "employee_id": f"EMP{1000 + i}",
            "department": random.choice(departments),
            "position": random.choice(positions),
            "contract_type": random.choice([ContractType.FULL_TIME, ContractType.PART_TIME]),
            "max_hours_per_week": random.choice([20, 30, 40]),
            "hourly_rate": round(random.uniform(15.0, 25.0), 2),
            "skills": random.sample(["Customer Service", "Sales", "Leadership", "Communication", "Problem Solving"], 2),
            "phone": f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
            "hire_date": datetime.utcnow() - timedelta(days=random.randint(30, 365)),
            "status": EmployeeStatus.ACTIVE,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        emp_result = await db.employees.insert_one(employee_doc)
        employee_doc["_id"] = emp_result.inserted_id
        created_employees.append(employee_doc)
    
    print(f"✅ Created {len(created_employees)} employee profiles")
    return created_employees

async def create_availability_data(db, employees):
    """Create availability data for employees"""
    print("📅 Creating availability data...")
    
    for employee in employees:
        # Create realistic availability patterns
        weekly_availability = {}
        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        
        for day in days:
            if random.random() > 0.2:  # 80% chance of being available
                start_hour = random.choice([6, 7, 8, 9])
                end_hour = random.choice([17, 18, 19, 20, 21, 22])
                
                weekly_availability[day] = {
                    "available": True,
                    "start_time": f"{start_hour:02d}:00",
                    "end_time": f"{end_hour:02d}:00"
                }
            else:
                weekly_availability[day] = {
                    "available": False,
                    "start_time": None,
                    "end_time": None
                }
        
        availability_doc = {
            "employee_id": str(employee["_id"]),
            "weekly_availability": weekly_availability,
            "max_hours_per_week": employee["max_hours_per_week"],
            "preferred_shift_length": random.choice([6, 8, 10]),
            "notes": f"Standard availability for {employee['employee_id']}",
            "effective_date": datetime.utcnow(),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        await db.availability.insert_one(availability_doc)
    
    print(f"✅ Created availability for {len(employees)} employees")

async def create_sample_schedules(db, admin_users, employees):
    """Create sample schedules with shifts"""
    print("📊 Creating sample schedules...")
    
    admin_id = str(admin_users[0]["_id"])
    
    # Create schedules for current and next week
    for week_offset in [0, 1]:
        week_start = datetime.utcnow().date()
        week_start -= timedelta(days=week_start.weekday())  # Get Monday
        week_start += timedelta(weeks=week_offset)
        week_end = week_start + timedelta(days=6)
        
        schedule_doc = {
            "name": f"Schedule for Week {week_start.strftime('%Y-%m-%d')}",
            "week_start": week_start,
            "week_end": week_end,
            "status": ScheduleStatus.PUBLISHED if week_offset == 0 else ScheduleStatus.DRAFT,
            "created_by": admin_id,
            "notes": f"AI-generated schedule for week starting {week_start}",
            "ai_optimization_score": round(random.uniform(85.0, 95.0), 1),
            "total_hours": 0,
            "conflicts_count": random.randint(0, 2),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        schedule_result = await db.schedules.insert_one(schedule_doc)
        schedule_id = str(schedule_result.inserted_id)
        
        # Create shifts for this schedule
        total_hours = await create_shifts_for_schedule(db, schedule_id, week_start, employees)
        
        # Update schedule with total hours
        await db.schedules.update_one(
            {"_id": schedule_result.inserted_id},
            {"$set": {"total_hours": total_hours}}
        )
    
    print("✅ Created sample schedules with shifts")

async def create_shifts_for_schedule(db, schedule_id, week_start, employees):
    """Create shifts for a specific schedule"""
    shift_templates = [
        ("09:00", "17:00", "Morning Shift"),
        ("10:00", "18:00", "Day Shift"),
        ("14:00", "22:00", "Evening Shift"),
        ("12:00", "20:00", "Afternoon Shift")
    ]
    
    total_hours = 0
    
    for day_offset in range(7):  # 7 days
        shift_date = week_start + timedelta(days=day_offset)
        
        # Create 2-3 shifts per day
        daily_shifts = random.randint(2, 3)
        selected_templates = random.sample(shift_templates, daily_shifts)
        available_employees = employees.copy()
        
        for start_time, end_time, shift_name in selected_templates:
            if not available_employees:
                break
                
            employee = random.choice(available_employees)
            available_employees.remove(employee)  # Avoid double booking
            
            # Calculate shift hours
            start_hour = int(start_time.split(':')[0])
            end_hour = int(end_time.split(':')[0])
            shift_hours = end_hour - start_hour
            total_hours += shift_hours
            
            shift_doc = {
                "schedule_id": schedule_id,
                "employee_id": str(employee["_id"]),
                "date": shift_date,
                "start_time": start_time,
                "end_time": end_time,
                "position": employee["position"],
                "location": employee["department"],
                "break_duration": 30,
                "status": ShiftStatus.SCHEDULED,
                "notes": f"{shift_name} assignment",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            await db.shifts.insert_one(shift_doc)
    
    return total_hours

async def create_sample_requests(db, employees):
    """Create sample time-off and schedule change requests"""
    print("📝 Creating sample requests...")
    
    request_types = ["time_off", "shift_swap", "schedule_change"]
    statuses = ["pending", "approved", "rejected"]
    
    for i in range(5):  # Create 5 sample requests
        employee = random.choice(employees)
        request_date = datetime.utcnow().date() + timedelta(days=random.randint(1, 14))
        
        request_doc = {
            "employee_id": str(employee["_id"]),
            "request_type": random.choice(request_types),
            "start_date": request_date,
            "end_date": request_date + timedelta(days=random.randint(0, 2)),
            "reason": f"Sample {random.choice(['personal', 'medical', 'family'])} request",
            "status": random.choice(statuses),
            "notes": "Sample request for testing",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        await db.requests.insert_one(request_doc)
    
    print("✅ Created sample requests")

if __name__ == "__main__":
    asyncio.run(setup_database())
