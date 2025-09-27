# 🚀 Quick Start Guide

## Method 1: Super Simple (Recommended)

\`\`\`bash
# Navigate to backend directory
cd backend

# Run the simple setup (does everything automatically)
python scripts/simple_setup.py
\`\`\`

## Method 2: Step by Step

### Step 1: Install Dependencies
\`\`\`bash
python scripts/install_dependencies.py
\`\`\`

### Step 2: Setup Database
\`\`\`bash
python scripts/setup_database_sync.py
\`\`\`

### Step 3: Start Server
\`\`\`bash
python main.py
\`\`\`

### Step 4: Test API
\`\`\`bash
# In another terminal
python scripts/test_api_sync.py
\`\`\`

## Method 3: Manual Installation

\`\`\`bash
# Install packages
pip install fastapi uvicorn motor pymongo python-jose passlib python-dotenv pydantic bcrypt dnspython requests

# Setup database
python scripts/setup_database_sync.py

# Start server
python main.py
\`\`\`

## 🔗 Access Points

- **API Server**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

## 🔐 Demo Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@asp.com | admin123 |
| Manager | manager@asp.com | manager123 |
| Employee | demo@asp.com | demo123 |

## ✅ What Gets Created

- **13 Users** (3 admin/manager + 10 employees)
- **11 Employee Profiles** with departments and skills
- **11 Availability Records** with weekly schedules
- **3 Schedules** (current week + 2 future weeks)
- **Multiple Shifts** assigned to employees
- **8 Sample Requests** (time-off, swaps, etc.)

## 🧪 Testing

1. Visit http://localhost:8000/docs
2. Click "Authorize" button
3. Login with admin@asp.com / admin123
4. Test any endpoint

## 🎯 Key Features Working

✅ JWT Authentication  
✅ Employee Management  
✅ AI Schedule Generation  
✅ Availability Tracking  
✅ Request System  
✅ Analytics Dashboard  
✅ Export Functionality  

## 🆘 Troubleshooting

### Can't install packages?
\`\`\`bash
pip install --user fastapi uvicorn motor pymongo python-jose passlib python-dotenv pydantic bcrypt dnspython
\`\`\`

### Database connection issues?
- Check internet connection
- Verify MongoDB Atlas credentials
- Ensure IP is whitelisted

### Server won't start?
- Check if port 8000 is available
- Try: python -m uvicorn main:app --host 0.0.0.0 --port 8000

### Import errors?
- Make sure you're in the backend directory
- Check Python version (3.8+ required)
