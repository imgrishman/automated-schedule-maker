import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_api():
    """Test the API endpoints"""
    print("🧪 Testing API Endpoints...")
    print("=" * 50)
    
    # Test health endpoint
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check passed")
            print(f"   Status: {data.get('status')}")
            print(f"   Service: {data.get('service')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to API: {e}")
        print("💡 Make sure the server is running: python main.py")
        return False
    
    # Test login
    login_data = {
        "email": "admin@asp.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data, timeout=10)
        if response.status_code == 200:
            auth_data = response.json()
            token = auth_data["access_token"]
            user = auth_data["user"]
            print("✅ Admin login successful")
            print(f"   User: {user['first_name']} {user['last_name']}")
            print(f"   Role: {user['role']}")
            
            # Test authenticated endpoint
            headers = {"Authorization": f"Bearer {token}"}
            emp_response = requests.get(f"{BASE_URL}/api/employees/", headers=headers, timeout=10)
            if emp_response.status_code == 200:
                employees = emp_response.json()
                print(f"✅ Retrieved {len(employees)} employees")
                
                # Test analytics endpoint
                analytics_response = requests.get(f"{BASE_URL}/api/analytics/dashboard", headers=headers, timeout=10)
                if analytics_response.status_code == 200:
                    analytics = analytics_response.json()
                    print(f"✅ Analytics dashboard loaded")
                    print(f"   Total Employees: {analytics.get('total_employees')}")
                    print(f"   AI Efficiency: {analytics.get('ai_efficiency')}%")
                else:
                    print("❌ Failed to retrieve analytics")
            else:
                print("❌ Failed to retrieve employees")
        else:
            print(f"❌ Admin login failed: {response.status_code}")
            if response.text:
                print(f"   Error: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Login test failed: {e}")
        return False
    
    print("\n🎉 API testing completed successfully!")
    return True

def wait_for_server(max_attempts=30):
    """Wait for server to start"""
    print("⏳ Waiting for server to start...")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{BASE_URL}/api/health", timeout=2)
            if response.status_code == 200:
                print("✅ Server is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        time.sleep(1)
        if attempt % 5 == 0:
            print(f"   Still waiting... ({attempt}/{max_attempts})")
    
    print("❌ Server did not start in time")
    return False

if __name__ == "__main__":
    if wait_for_server():
        test_api()
    else:
        print("💡 Start the server manually: python main.py")
