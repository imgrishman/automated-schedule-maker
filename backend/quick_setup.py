#!/usr/bin/env python3
"""
Quick setup script for Automated Schedule Planner
This script will install dependencies and set up the database
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 Automated Schedule Planner - Quick Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt not found. Please run this script from the backend directory.")
        sys.exit(1)
    
    # Install requirements
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing Python packages"):
        print("💡 Try running: pip install --upgrade pip")
        sys.exit(1)
    
    # Set up database
    if not run_command(f"{sys.executable} scripts/setup_database.py", "Setting up MongoDB database"):
        print("💡 Check your MongoDB connection string in the .env file")
        sys.exit(1)
    
    # Verify database
    if not run_command(f"{sys.executable} scripts/verify_database.py", "Verifying database setup"):
        print("💡 Database verification failed, but setup might still work")
    
    print("\n🎉 Setup completed successfully!")
    print("\n🚀 Next steps:")
    print("1. Start the server: python main.py")
    print("2. Open your browser: http://localhost:8000")
    print("3. View API docs: http://localhost:8000/docs")
    print("\n🔐 Demo credentials:")
    print("   Admin: admin@asp.com / admin123")
    print("   Employee: demo@asp.com / demo123")

if __name__ == "__main__":
    main()
