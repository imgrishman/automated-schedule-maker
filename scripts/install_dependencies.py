import subprocess
import sys
import os

def install_package(package):
    """Install a single package"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        try:
            # Try with --user flag
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", package])
            return True
        except subprocess.CalledProcessError:
            return False

def main():
    print("🚀 Installing Automated Schedule Planner Dependencies...")
    print("=" * 60)
    
    # Required packages
    packages = [
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0", 
        "motor==3.3.2",
        "pymongo==4.6.0",
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4",
        "python-multipart==0.0.6",
        "python-dotenv==1.0.0",
        "pydantic[email]==2.5.0",
        "bcrypt==4.1.2",
        "dnspython==2.4.2",
        "email-validator==2.1.0",
        "aiohttp==3.9.1"
    ]
    
    print(f"📦 Installing {len(packages)} packages...")
    
    failed_packages = []
    for i, package in enumerate(packages, 1):
        package_name = package.split("==")[0]
        print(f"[{i}/{len(packages)}] Installing {package_name}...")
        
        if install_package(package):
            print(f"✅ {package_name} installed successfully")
        else:
            print(f"❌ Failed to install {package_name}")
            failed_packages.append(package_name)
    
    print("\n" + "=" * 60)
    if failed_packages:
        print(f"❌ Failed to install: {', '.join(failed_packages)}")
        print("\n💡 Try running manually:")
        for pkg in failed_packages:
            print(f"   pip install {pkg}")
    else:
        print("✅ All dependencies installed successfully!")
        print("\n🎉 Ready to set up database!")
        print("Next step: python scripts/setup_database_sync.py")
    
    return len(failed_packages) == 0

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
