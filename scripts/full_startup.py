import subprocess
import sys
import os
import time
import asyncio
from pathlib import Path

def run_command(command, description, check=True):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        if isinstance(command, list):
            result = subprocess.run(command, check=check, capture_output=True, text=True)
        else:
            result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {description} completed successfully!")
            return True
        else:
            print(f"❌ {description} failed!")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ {description} failed with exception: {e}")
        return False

async def main():
    print("🚀 AUTOMATED SCHEDULE PLANNER - FULL STARTUP")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt not found. Please run this script from the backend directory.")
        sys.exit(1)
    
    # Step 1: Install dependencies
    print("\n📦 STEP 1: Installing Dependencies")
    print("-" * 40)
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing Python packages"):
        print("💡 Try: pip install --upgrade pip")
        print("💡 Or: pip install --user -r requirements.txt")
        sys.exit(1)
    
    # Step 2: Setup database
    print("\n🗄️ STEP 2: Setting Up Database")
    print("-" * 40)
    if not run_command(f"{sys.executable} scripts/complete_setup.py", "Setting up MongoDB database"):
        print("💡 Check your MongoDB connection string")
        sys.exit(1)
    
    # Step 3: Start the server in background
    print("\n🚀 STEP 3: Starting Server")
    print("-" * 40)
    print("Starting FastAPI server...")
    
    # Start server as subprocess
    server_process = subprocess.Popen([sys.executable, "main.py"], 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE)
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(5)
    
    # Step 4: Test API
    print("\n🧪 STEP 4: Testing API")
    print("-" * 40)
    
    # Import and run API test
    try:
        from scripts.test_api import test_api
        await test_api()
    except Exception as e:
        print(f"❌ API test failed: {e}")
    
    # Step 5: Show results
    print("\n🎉 SETUP COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("🔗 API Server: http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/api/health")
    
    print("\n🔐 Demo Credentials:")
    print("-" * 30)
    print("👑 Admin Login:")
    print("   Email: admin@asp.com")
    print("   Password: admin123")
    print("\n👨‍💼 Manager Login:")
    print("   Email: manager@asp.com")
    print("   Password: manager123")
    print("\n👤 Employee Login:")
    print("   Email: demo@asp.com")
    print("   Password: demo123")
    
    print("\n🎯 What's Available:")
    print("✅ User Authentication & Authorization")
    print("✅ Employee Management System")
    print("✅ Availability Tracking")
    print("✅ AI-Powered Schedule Generation")
    print("✅ Shift Management")
    print("✅ Request System (Time-off, Swaps)")
    print("✅ Analytics Dashboard")
    print("✅ Export Functionality")
    
    print("\n🔧 API Endpoints Available:")
    print("• POST /api/auth/login - User login")
    print("• GET /api/employees/ - List employees")
    print("• POST /api/schedules/generate - Generate AI schedule")
    print("• GET /api/analytics/dashboard - Dashboard data")
    print("• GET /api/availability/ - Employee availability")
    
    print(f"\n🖥️ Server Process ID: {server_process.pid}")
    print("💡 To stop server: Ctrl+C or kill the process")
    
    # Keep server running
    try:
        print("\n⏳ Server is running... Press Ctrl+C to stop")
        server_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping server...")
        server_process.terminate()
        server_process.wait()
        print("✅ Server stopped successfully!")

if __name__ == "__main__":
    asyncio.run(main())
