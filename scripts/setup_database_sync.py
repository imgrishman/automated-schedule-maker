import pymongo
import sys
import os
from datetime import datetime, date, timedelta
from passlib.context import CryptContext
import random

# MongoDB connection
MONGODB_URL = "mongodb+srv://v0user:v0user@asp.d0jajzm.mongodb.net/automated_schedule_planner?retryWrites=true&w=majority&appName=ASP"
DATABASE_NAME = "automated_schedule_planner"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def setup_database():
    """Complete database setup with all collections and data"""
    print("🚀 Starting MongoDB Atlas Database Setup...")
    print("=" * 60)
    
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(MONGODB_URL)
        db = client[DATABASE_NAME]
        
        # Test connection
        client.admin.command('ping')
        print("✅ Connected to MongoDB Atlas successfully!")
        
        # Clear existing data
        print("\n🧹 Clearing existing data...")
        collections = ['users', 'employees', 'availability', 'schedules', 'shifts', 'requests']
        for collection in collections:
            result = db[collection].delete_many({})
            print(f"   Cleared {result.deleted_count} documents from {collection}")
        
        # Create indexes
        create_all_indexes(db)
        
        # Create all data
        users = create_users(db)
        employees = create_employees(db, users)
        create_availability(db, employees)
        schedules = create_schedules(db, users[0], employees)
        create_requests(db, employees)
        
        # Verify setup
        verify_setup(db)
        
        print("\n🎉 Database setup completed successfully!")
        print("=" * 60)
        print("🔗 Database: automated_schedule_planner")
        print("🌐 Platform: MongoDB Atlas")
        print("✅ Status: Fully Functional")
        
        print("\n🔐 Login Credentials:")
        print("-" * 30)
        print("👑 Admin:")
        print("   Email: admin@asp.com")
        print("   Password: admin123")
        print("\n👨‍💼 Manager:")
        print("   Email: manager@asp.com")
        print("   Password: manager123")
        print("\n👤 Employee:")
        print("   Email: demo@asp.com")
        print("   Password: demo123")
        
        print("\n🚀 Next Steps:")
        print("1. Run: python main.py")
        print("2. Open: http://localhost:8000/docs")
        print("3. Test API endpoints")
        
        return True
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        try:
            client.close()
        except:
            pass

def create_all_indexes(db):
    """Create all necessary indexes"""
    print("\n📋 Creating database indexes...")
    
    try:
        # Users indexes
        db.users.create_index("email", unique=True)
        db.users.create_index("employee_id", unique=True, sparse=True)
        db.users.create_index([("role", 1), ("status", 1)])
        
        # Employees indexes
        db.employees.create_index("user_id", unique=True)
        db.employees.create_index("employee_id", unique=True)
        db.employees.create_index("department")
        db.employees.create_index("status")
        
        # Availability indexes
        db.availability.create_index("employee_id")
        db.availability.create_index([("employee_id", 1), ("effective_date", -1)])
        
        # Schedules indexes
        db.schedules.create_index([("week_start", 1), ("status", 1)])
        db.schedules.create_index("created_by")
        
        # Shifts indexes
        db.shifts.create_index([("schedule_id", 1), ("employee_id", 1)])
        db.shifts.create_index([("employee_id", 1), ("date", 1)])
        db.shifts.create_index([("date", 1), ("start_time", 1)])
        
        # Requests indexes
        db.requests.create_index("employee_id")
        db.requests.create_index([("status", 1), ("created_at", -1)])
        
        print("✅ All indexes created successfully")
    except Exception as e:
        print(f"⚠️ Some indexes may already exist: {e}")

def create_users(db):
    """Create system users"""
    print("\n👥 Creating system users...")
    
    users_data = [
        {
            "email": "admin@asp.com",
            "password": "admin123",
            "first_name": "System",
            "last_name": "Administrator",
            "role": "admin",
            "status": "active"
        },
        {
            "email": "manager@asp.com",
            "password": "manager123",
            "first_name": "John",
            "last_name": "Manager",
            "role": "manager",
            "status": "active"
        },
        {
            "email": "demo@asp.com",
            "password": "demo123",
            "first_name": "Demo",
            "last_name": "Employee",
            "role": "employee",
            "status": "active",
            "employee_id": "EMP001"
        }
    ]
    
    created_users = []
    for user_data in users_data:
        password = user_data.pop("password")
        hashed_password = pwd_context.hash(password)
        
        user_doc = {
            **user_data,
            "hashed_password": hashed_password,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = db.users.insert_one(user_doc)
        user_doc["_id"] = result.inserted_id
        created_users.append(user_doc)
    
    print(f"✅ Created {len(created_users)} system users")
    return created_users

def create_employees(db, users):
    """Create employee profiles"""
    print("\n👷 Creating employee profiles...")
    
    # Employee data
    employee_data = [
        ("Alice", "Johnson", "alice.johnson@asp.com", "Sales", "Sales Associate"),
        ("Bob", "Smith", "bob.smith@asp.com", "Customer Service", "Support Specialist"),
        ("Carol", "Davis", "carol.davis@asp.com", "Kitchen", "Chef"),
        ("David", "Wilson", "david.wilson@asp.com", "Sales", "Senior Associate"),
        ("Emma", "Brown", "emma.brown@asp.com", "Customer Service", "Team Lead"),
        ("Frank", "Miller", "frank.miller@asp.com", "Kitchen", "Prep Cook"),
        ("Grace", "Taylor", "grace.taylor@asp.com", "Management", "Supervisor"),
        ("Henry", "Anderson", "henry.anderson@asp.com", "Maintenance", "Technician"),
        ("Ivy", "Thomas", "ivy.thomas@asp.com", "Sales", "Associate"),
        ("Jack", "Jackson", "jack.jackson@asp.com", "Customer Service", "Associate")
    ]
    
    created_employees = []
    
    # Create demo employee profile for existing demo user
    demo_user = next(u for u in users if u["email"] == "demo@asp.com")
    demo_employee = {
        "user_id": str(demo_user["_id"]),
        "employee_id": "EMP001",
        "department": "Sales",
        "position": "Demo Associate",
        "contract_type": "full_time",
        "max_hours_per_week": 40,
        "hourly_rate": 18.50,
        "skills": ["Customer Service", "Sales"],
        "phone": "+1-555-DEMO-001",
        "hire_date": datetime.utcnow() - timedelta(days=90),
        "status": "active",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = db.employees.insert_one(demo_employee)
    demo_employee["_id"] = result.inserted_id
    created_employees.append(demo_employee)
    
    # Create additional employees
    for i, (first_name, last_name, email, department, position) in enumerate(employee_data, 2):
        # Create user account
        user_doc = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "hashed_password": pwd_context.hash("employee123"),
            "role": "employee",
            "status": "active",
            "employee_id": f"EMP{i:03d}",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        user_result = db.users.insert_one(user_doc)
        
        # Create employee profile
        employee_doc = {
            "user_id": str(user_result.inserted_id),
            "employee_id": f"EMP{i:03d}",
            "department": department,
            "position": position,
            "contract_type": random.choice(["full_time", "part_time"]),
            "max_hours_per_week": random.choice([20, 30, 40]),
            "hourly_rate": round(random.uniform(15.0, 25.0), 2),
            "skills": random.sample(["Customer Service", "Sales", "Leadership", "Communication", "Problem Solving", "Technical"], 2),
            "phone": f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
            "hire_date": datetime.utcnow() - timedelta(days=random.randint(30, 365)),
            "status": "active",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        emp_result = db.employees.insert_one(employee_doc)
        employee_doc["_id"] = emp_result.inserted_id
        created_employees.append(employee_doc)
    
    print(f"✅ Created {len(created_employees)} employee profiles")
    return created_employees

def create_availability(db, employees):
    """Create availability data for all employees"""
    print("\n📅 Creating availability data...")
    
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    
    for employee in employees:
        weekly_availability = {}
        
        for day in days:
            # 85% chance of being available each day
            if random.random() > 0.15:
                start_hour = random.choice([6, 7, 8, 9, 10])
                end_hour = random.choice([16, 17, 18, 19, 20, 21, 22])
                
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
        
        db.availability.insert_one(availability_doc)
    
    print(f"✅ Created availability for {len(employees)} employees")

def create_schedules(db, admin_user, employees):
    """Create sample schedules with shifts"""
    print("\n📊 Creating sample schedules...")
    
    admin_id = str(admin_user["_id"])
    created_schedules = []
    
    # Create schedules for current week and next 2 weeks
    for week_offset in [0, 1, 2]:
        week_start = datetime.utcnow().date()
        week_start -= timedelta(days=week_start.weekday())  # Get Monday
        week_start += timedelta(weeks=week_offset)
        week_end = week_start + timedelta(days=6)
        
        status = "published" if week_offset == 0 else "draft"
        
        schedule_doc = {
            "name": f"Schedule for Week {week_start.strftime('%Y-%m-%d')}",
            "week_start": week_start,
            "week_end": week_end,
            "status": status,
            "created_by": admin_id,
            "notes": f"AI-generated schedule for week starting {week_start}",
            "ai_optimization_score": round(random.uniform(85.0, 95.0), 1),
            "total_hours": 0,
            "conflicts_count": random.randint(0, 2),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        schedule_result = db.schedules.insert_one(schedule_doc)
        schedule_id = str(schedule_result.inserted_id)
        
        # Create shifts for this schedule
        total_hours = create_shifts(db, schedule_id, week_start, employees)
        
        # Update schedule with total hours
        db.schedules.update_one(
            {"_id": schedule_result.inserted_id},
            {"$set": {"total_hours": total_hours}}
        )
        
        schedule_doc["_id"] = schedule_result.inserted_id
        created_schedules.append(schedule_doc)
    
    print(f"✅ Created {len(created_schedules)} schedules with shifts")
    return created_schedules

def create_shifts(db, schedule_id, week_start, employees):
    """Create shifts for a schedule"""
    shift_templates = [
        ("09:00", "17:00", "Morning Shift"),
        ("10:00", "18:00", "Day Shift"),
        ("13:00", "21:00", "Afternoon Shift"),
        ("14:00", "22:00", "Evening Shift")
    ]
    
    total_hours = 0
    
    for day_offset in range(7):  # 7 days
        shift_date = week_start + timedelta(days=day_offset)
        
        # Create 3-4 shifts per day
        daily_shifts = random.randint(3, 4)
        selected_templates = random.sample(shift_templates, daily_shifts)
        available_employees = employees.copy()
        random.shuffle(available_employees)
        
        for i, (start_time, end_time, shift_name) in enumerate(selected_templates):
            if i >= len(available_employees):
                break
                
            employee = available_employees[i]
            
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
                "status": "scheduled",
                "notes": f"{shift_name} assignment",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            db.shifts.insert_one(shift_doc)
    
    return total_hours

def create_requests(db, employees):
    """Create sample employee requests"""
    print("\n📝 Creating sample requests...")
    
    request_types = ["time_off", "shift_swap", "schedule_change"]
    statuses = ["pending", "approved", "rejected"]
    reasons = [
        "Family emergency",
        "Medical appointment",
        "Personal day",
        "Vacation request",
        "Schedule conflict",
        "Transportation issue"
    ]
    
    for i in range(8):  # Create 8 sample requests
        employee = random.choice(employees)
        request_date = datetime.utcnow().date() + timedelta(days=random.randint(1, 21))
        
        request_doc = {
            "employee_id": str(employee["_id"]),
            "request_type": random.choice(request_types),
            "start_date": request_date,
            "end_date": request_date + timedelta(days=random.randint(0, 3)),
            "reason": random.choice(reasons),
            "status": random.choice(statuses),
            "notes": f"Sample request from {employee['employee_id']}",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        db.requests.insert_one(request_doc)
    
    print("✅ Created 8 sample requests")

def verify_setup(db):
    """Verify the database setup"""
    print("\n🔍 Verifying database setup...")
    
    collections = {
        'users': 'User accounts',
        'employees': 'Employee profiles',
        'availability': 'Availability records',
        'schedules': 'Schedule records',
        'shifts': 'Shift assignments',
        'requests': 'Employee requests'
    }
    
    print("\n📊 Collection Statistics:")
    print("-" * 40)
    
    total_documents = 0
    for collection_name, description in collections.items():
        count = db[collection_name].count_documents({})
        total_documents += count
        print(f"{description:<20}: {count:>5} documents")
    
    print("-" * 40)
    print(f"{'Total Documents':<20}: {total_documents:>5}")
    
    # Test key relationships
    print("\n🔗 Testing Relationships:")
    print("-" * 40)
    
    # Check admin user
    admin = db.users.find_one({"email": "admin@asp.com"})
    print(f"Admin user exists: {'✅' if admin else '❌'}")
    
    # Check employee with availability
    employee_with_avail = list(db.employees.aggregate([
        {"$lookup": {
            "from": "availability",
            "localField": "_id",
            "foreignField": "employee_id",
            "as": "availability"
        }},
        {"$match": {"availability": {"$ne": []}}},
        {"$limit": 1}
    ]))
    
    print(f"Employee-Availability link: {'✅' if employee_with_avail else '❌'}")
    
    # Check schedule with shifts
    schedule_with_shifts = list(db.schedules.aggregate([
        {"$lookup": {
            "from": "shifts",
            "localField": "_id",
            "foreignField": "schedule_id",
            "as": "shifts"
        }},
        {"$match": {"shifts": {"$ne": []}}},
        {"$limit": 1}
    ]))
    
    print(f"Schedule-Shifts link: {'✅' if schedule_with_shifts else '❌'}")
    
    print("\n✅ Database verification completed!")

if __name__ == "__main__":
    success = setup_database()
    if not success:
        sys.exit(1)
