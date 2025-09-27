# 🚀 Automated Schedule Planner (ASP)

A full-stack AI-powered workforce scheduling system built with Next.js and Python FastAPI.

## ✨ Features

### 🤖 AI-Powered Scheduling
- Intelligent schedule generation using machine learning
- Fairness optimization across employees
- Conflict detection and resolution
- Real-time optimization scoring

### 👥 Employee Management
- Complete employee profiles and information
- Department and position tracking
- Skills and availability management
- Role-based access control

### 📅 Schedule Management
- Weekly schedule creation and publishing
- Shift assignment and tracking
- Schedule templates and automation
- Export functionality (JSON/CSV)

### ⏰ Availability System
- Weekly availability tracking
- Time preferences and constraints
- Maximum hours management
- Flexible scheduling options

### 📊 Analytics Dashboard
- Employee satisfaction metrics
- Schedule efficiency tracking
- Department performance analysis
- AI insights and recommendations

### 🔐 Authentication & Security
- JWT-based authentication
- Role-based permissions (Admin/Manager/Employee)
- Secure password hashing
- Session management

## 🛠️ Tech Stack

### Frontend
- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Shadcn/UI** - Component library
- **Lucide React** - Icons

### Backend
- **FastAPI** - Python web framework
- **MongoDB Atlas** - Cloud database
- **Motor** - Async MongoDB driver
- **JWT** - Authentication
- **Pydantic** - Data validation

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- MongoDB Atlas account (free tier works)

### Option 1: Automated Setup (Recommended)

\`\`\`bash
# Clone and setup everything automatically
git clone <repository>
cd automated-schedule-planner
npm run setup
\`\`\`

### Option 2: Manual Setup

#### Frontend Setup
\`\`\`bash
# Install frontend dependencies
npm install

# Start development server
npm run dev
\`\`\`

#### Backend Setup
\`\`\`bash
# Navigate to backend
cd backend

# Install Python dependencies
python scripts/install_dependencies.py

# Setup database with sample data
python scripts/setup_database_sync.py

# Start API server
python main.py
\`\`\`

## 🔗 Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

## 🔐 Demo Credentials

| Role | Email | Password | Access Level |
|------|-------|----------|--------------|
| Admin | admin@asp.com | admin123 | Full system access |
| Manager | manager@asp.com | manager123 | Team management |
| Employee | demo@asp.com | demo123 | Personal schedule view |

## 📱 Screenshots

### Dashboard
- Real-time metrics and KPIs
- Quick actions and notifications
- Role-based content

### Employee Management
- Complete employee directory
- Department filtering
- Skills and availability tracking

### Schedule Generation
- AI-powered optimization
- Conflict detection
- One-click publishing

### Analytics
- Performance insights
- Employee satisfaction tracking
- AI recommendations

## 🗄️ Database Schema

### Collections
- **users** - Authentication and user profiles
- **employees** - Employee information and details
- **availability** - Weekly availability schedules
- **schedules** - Generated work schedules
- **shifts** - Individual shift assignments
- **requests** - Time-off and schedule requests

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/demo-login` - Demo access

### Employees
- `GET /api/employees/` - List employees
- `POST /api/employees/` - Create employee
- `GET /api/employees/me` - Current user profile
- `PUT /api/employees/{id}` - Update employee

### Schedules
- `GET /api/schedules/` - List schedules
- `POST /api/schedules/generate` - AI schedule generation
- `GET /api/schedules/{id}` - Schedule details
- `PUT /api/schedules/{id}/publish` - Publish schedule

### Availability
- `GET /api/availability/` - List availability
- `POST /api/availability/` - Create availability
- `PUT /api/availability/{id}` - Update availability

### Analytics
- `GET /api/analytics/dashboard` - Dashboard metrics
- `GET /api/analytics/employee-satisfaction` - Satisfaction data
- `GET /api/analytics/ai-insights` - AI recommendations

## 🧪 Testing

### Frontend Testing
\`\`\`bash
npm run test
npm run test:e2e
\`\`\`

### Backend Testing
\`\`\`bash
cd backend
python scripts/test_api_sync.py
\`\`\`

## 🚀 Deployment

### Frontend (Vercel)
\`\`\`bash
npm run build
vercel deploy
\`\`\`

### Backend (Railway/Heroku)
\`\`\`bash
cd backend
# Update environment variables
# Deploy using platform CLI
\`\`\`

## 🔧 Configuration

### Environment Variables

#### Frontend (.env.local)
\`\`\`env
NEXT_PUBLIC_API_URL=http://localhost:8000
\`\`\`

#### Backend (.env)
\`\`\`env
MONGODB_URL=mongodb+srv://...
DATABASE_NAME=automated_schedule_planner
SECRET_KEY=your-secret-key
\`\`\`

## 📈 Performance

- **AI Schedule Generation**: < 5 seconds
- **Database Queries**: < 100ms average
- **Frontend Load Time**: < 2 seconds
- **API Response Time**: < 200ms average

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Common Issues

#### Can't connect to database
- Check MongoDB Atlas connection string
- Verify IP whitelist settings
- Ensure credentials are correct

#### Frontend won't start
- Check Node.js version (18+ required)
- Clear node_modules and reinstall
- Verify environment variables

#### Backend API errors
- Check Python version (3.8+ required)
- Verify all dependencies installed
- Check database connection

### Getting Help
- Check the [Issues](issues) page
- Review API documentation at `/docs`
- Contact support team

## 🎯 Roadmap

- [ ] Mobile app (React Native)
- [ ] Real-time notifications (WebSocket)
- [ ] Advanced AI features
- [ ] Multi-tenant support
- [ ] Integration APIs
- [ ] Advanced reporting

---

**Built with ❤️ by the ASP Team**
