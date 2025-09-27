import asyncio
import aiohttp
import json

BASE_URL = "http://localhost:8000"

async def test_api():
    """Test the API endpoints"""
    print("🧪 Testing API Endpoints...")
    print("=" * 50)
    
    async with aiohttp.ClientSession() as session:
        # Test health endpoint
        try:
            async with session.get(f"{BASE_URL}/api/health") as response:
                if response.status == 200:
                    data = await response.json()
                    print("✅ Health check passed")
                else:
                    print("❌ Health check failed")
        except Exception as e:
            print(f"❌ Cannot connect to API: {e}")
            print("💡 Make sure the server is running: python main.py")
            return
        
        # Test login
        login_data = {
            "email": "admin@asp.com",
            "password": "admin123"
        }
        
        try:
            async with session.post(f"{BASE_URL}/api/auth/login", json=login_data) as response:
                if response.status == 200:
                    auth_data = await response.json()
                    token = auth_data["access_token"]
                    print("✅ Admin login successful")
                    
                    # Test authenticated endpoint
                    headers = {"Authorization": f"Bearer {token}"}
                    async with session.get(f"{BASE_URL}/api/employees/", headers=headers) as emp_response:
                        if emp_response.status == 200:
                            employees = await emp_response.json()
                            print(f"✅ Retrieved {len(employees)} employees")
                        else:
                            print("❌ Failed to retrieve employees")
                else:
                    print("❌ Admin login failed")
        except Exception as e:
            print(f"❌ Login test failed: {e}")
    
    print("\n🎉 API testing completed!")

if __name__ == "__main__":
    asyncio.run(test_api())
