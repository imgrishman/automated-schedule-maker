# 🚀 Automated Schedule Planner - Setup Guide

## Quick Start (Recommended)

### 1. Install Dependencies & Setup Database
\`\`\`bash
npm run setup
\`\`\`

### 2. Start Development Environment
\`\`\`bash
npm run start-dev
\`\`\`

This will start both the backend (port 8000) and frontend (port 3000) automatically.

## Manual Setup

### Backend Setup

1. **Navigate to backend directory:**
\`\`\`bash
cd backend
\`\`\`

2. **Install Python dependencies:**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

3. **Setup database with sample data:**
\`\`\`bash
python scripts/simple_setup.py
\`\`\`

4. **Start the backend server:**
\`\`\`bash
python main.py
\`\`\`

The backend will be available at: http://localhost:8000

### Frontend Setup

1. **Install Node.js dependencies:**
\`\`\`bash
npm install
\`\`\`

2. **Start the development server:**
\`\`\`bash
npm run dev
\`\`\`

The frontend will be available at: http://localhost:3000

## Environment Configuration

### Backend (.env)
\`\`\`env
MONGODB_URL=mongodb+srv://asp_user:asp_password_2024@cluster0.mongodb.net/
DATABASE_NAME=automated_schedule_planner
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440
\`\`\`

### Frontend (.env.local)
\`\`\`env
NEXT_PUBLIC_API_URL=http://localhost:8000
\`\`\`

## Demo Accounts

### Admin Access
- **Email:** admin@asp.com
- **Password:** admin123

### Manager Access
- **Email:** manager@asp.com
- **Password:** manager123

### Employee Access
- **Email:** demo@asp.com
- **Password:** demo123

## Troubleshooting

### "Failed to fetch" Error
This means the backend server is not running or not accessible.

**Solution:**
1. Make sure the backend is running: `cd backend && python main.py`
2. Check that the backend is accessible at http://localhost:8000
3. Verify CORS is properly configured in the backend

### Database Connection Issues
**Solution:**
1. Check your MongoDB Atlas connection string in `backend/.env`
2. Ensure your IP is whitelisted in MongoDB Atlas
3. Run the database setup script: `python scripts/simple_setup.py`

### Port Already in Use
**Solution:**
- Backend (8000): Kill the process using port 8000 or change the port in `main.py`
- Frontend (3000): Kill the process using port 3000 or Next.js will suggest an alternative port

## API Documentation

Once the backend is running, visit:
- **Interactive API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/api/health

## Features

✅ **Authentication & Authorization**
- JWT-based authentication
- Role-based access control (Admin/Manager/Employee)
- Demo login functionality

✅ **Employee Management**
- CRUD operations for employees
- Department and role management
- Employee profiles and contact information

✅ **AI-Powered Scheduling**
- Intelligent schedule generation
- Availability-based optimization
- Conflict detection and resolution

✅ **Availability Management**
- Weekly availability tracking
- Time-off requests
- Availability conflicts detection

✅ **Analytics & Insights**
- Dashboard with key metrics
- Employee satisfaction tracking
- Schedule efficiency analysis
- AI-powered insights

✅ **Responsive Design**
- Mobile-friendly interface
- Modern UI with Tailwind CSS
- Real-time updates

## Production Deployment

### Backend Deployment
1. Update environment variables for production
2. Use a production WSGI server like Gunicorn
3. Configure proper CORS origins
4. Set up SSL/HTTPS

### Frontend Deployment
1. Build the application: `npm run build`
2. Deploy to Vercel, Netlify, or your preferred platform
3. Update API URL environment variable

## Support

If you encounter any issues:
1. Check the console for error messages
2. Verify all services are running
3. Check the API documentation at http://localhost:8000/docs
4. Ensure your MongoDB Atlas connection is working

---

**Happy Scheduling! 🎉**
