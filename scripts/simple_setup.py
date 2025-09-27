import subprocess
import sys
import os
import time
from pathlib import Path

def run_command(command, description):
    """Run a command and return success status"""
    print(f"🔧 {description}...")
    try:
        if isinstance(command, list):
            result = subprocess.run(command, check=True, capture_output=True, text=True)
        else:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 AUTOMATED SCHEDULE PLANNER - SIMPLE SETUP")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt not found. Please run this script from the backend directory.")
        return False
    
    # Step 1: Install dependencies
    print("\n📦 STEP 1: Installing Dependencies")
    print("-" * 40)
    
    # Try different installation methods
    install_commands = [
        f"{sys.executable} -m pip install -r requirements.txt",
        f"{sys.executable} -m pip install --user -r requirements.txt",
        "pip install -r requirements.txt",
        "pip3 install -r requirements.txt"
    ]
    
    installed = False
    for cmd in install_commands:
        if run_command(cmd, f"Installing packages with: {cmd.split()[0]}"):
            installed = True
            break
        print("   Trying alternative method...")
    
    if not installed:
        print("❌ Failed to install dependencies with all methods")
        print("💡 Try manually: pip install fastapi uvicorn motor pymongo python-jose passlib python-dotenv pydantic bcrypt dnspython")
        return False
    
    # Step 2: Setup database
    print("\n🗄️ STEP 2: Setting Up Database")
    print("-" * 40)
    if not run_command(f"{sys.executable} scripts/setup_database_sync.py", "Setting up MongoDB database"):
        print("💡 Check your MongoDB connection string")
        return False
    
    # Step 3: Test setup
    print("\n✅ STEP 3: Setup Complete!")
    print("-" * 40)
    print("🎉 Automated Schedule Planner is ready!")
    print("\n🚀 To start the server:")
    print("   python main.py")
    print("\n🔗 Then visit:")
    print("   http://localhost:8000/docs")
    
    # Ask if user wants to start server now
    try:
        start_now = input("\n❓ Start the server now? (y/n): ").lower().strip()
        if start_now in ['y', 'yes']:
            print("\n🚀 Starting server...")
            print("📖 API docs will be at: http://localhost:8000/docs")
            print("🛑 Press Ctrl+C to stop the server")
            
            # Start server
            subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\n👋 Setup completed! Run 'python main.py' when ready.")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
