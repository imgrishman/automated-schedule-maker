# 🚀 Automated Schedule Planner - Backend

AI-Powered Workforce Scheduling System with MongoDB Atlas

## ⚡ Quick Start

### Option 1: Full Automated Setup (Recommended)
\`\`\`bash
python scripts/full_startup.py
\`\`\`

### Option 2: Step by Step
\`\`\`bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup database
python scripts/complete_setup.py

# 3. Start server
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

## 🎯 Features

✅ **Authentication & Authorization**
- JWT-based authentication
- Role-based access control (Admin/Manager/Employee)
- Secure password hashing

✅ **Employee Management**
- Employee profiles and information
- Department and position tracking
- Skills and availability management

✅ **AI-Powered Scheduling**
- Automated schedule generation
- Fairness optimization
- Conflict detection and resolution

✅ **Availability System**
- Weekly availability tracking
- Time preferences
- Maximum hours constraints

✅ **Request Management**
- Time-off requests
- Shift swap requests
- Schedule change requests

✅ **Analytics Dashboard**
- Employee satisfaction metrics
- Schedule efficiency tracking
- Department hours distribution
- AI insights and recommendations

## 📊 Database Collections

- **users** - User accounts and authentication
- **employees** - Employee profiles and details
- **availability** - Weekly availability schedules
- **schedules** - AI-generated work schedules
- **shifts** - Individual shift assignments
- **requests** - Employee requests and approvals

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/demo-login` - Demo login

### Employees
- `GET /api/employees/` - List all employees
- `GET /api/employees/me` - Get current user profile
- `POST /api/employees/` - Create employee
- `PUT /api/employees/{id}` - Update employee

### Schedules
- `POST /api/schedules/generate` - Generate AI schedule
- `GET /api/schedules/` - List schedules
- `GET /api/schedules/{id}` - Get schedule details
- `PUT /api/schedules/{id}/publish` - Publish schedule

### Availability
- `GET /api/availability/` - List availability
- `POST /api/availability/` - Create availability
- `PUT /api/availability/{id}` - Update availability

### Analytics
- `GET /api/analytics/dashboard` - Dashboard metrics
- `GET /api/analytics/employee-satisfaction` - Satisfaction data
- `GET /api/analytics/schedule-efficiency` - Efficiency trends

## 🛠️ Development

### Requirements
- Python 3.8+
- MongoDB Atlas account
- Internet connection

### Environment Variables
\`\`\`env
MONGODB_URL=mongodb+srv://...
DATABASE_NAME=automated_schedule_planner
SECRET_KEY=your-secret-key
\`\`\`

### Testing
\`\`\`bash
# Test API endpoints
python scripts/test_api.py

# Verify database
python scripts/verify_database.py
\`\`\`

## 🚀 Production Deployment

1. Update environment variables
2. Set proper CORS origins
3. Use production MongoDB cluster
4. Deploy to cloud platform (Vercel, Railway, etc.)

## 📞 Support

- Check API documentation at `/docs`
- Verify database connection
- Ensure all dependencies are installed
- Check MongoDB Atlas network access
