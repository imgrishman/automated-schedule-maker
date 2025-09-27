#!/usr/bin/env python3
"""
Simple startup script for the Automated Schedule Planner backend
"""
import os
import sys
import subprocess
import time
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)

def setup_environment():
    """Setup environment variables"""
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creating .env file...")
        with open(".env", "w") as f:
            f.write("""# MongoDB Configuration
MONGODB_URL=mongodb+srv://admin:admin123@cluster0.mongodb.net/
DATABASE_NAME=automated_schedule_planner

# JWT Configuration
SECRET_KEY=your-super-secret-jwt-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
""")
        print("✅ Environment file created")

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting Automated Schedule Planner API...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔗 Health Check: http://localhost:8000/api/health")
    print("🌐 Frontend should connect to: http://localhost:8000")
    print("\n" + "="*50)
    
    try:
        import uvicorn
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except ImportError:
        print("❌ uvicorn not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "uvicorn"])
        import uvicorn
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )

if __name__ == "__main__":
    print("🚀 Automated Schedule Planner - Backend Setup")
    print("=" * 50)
    
    check_python_version()
    setup_environment()
    install_dependencies()
    
    print("\n🎯 Starting server...")
    start_server()
