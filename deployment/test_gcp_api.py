#!/usr/bin/env python3
"""
Test de l'API déployée sur GCP Cloud Run
"""

import requests
import json
import sys

def test_gcp_api(base_url):
    """Test l'API déployée sur GCP"""
    
    print("="*60)
    print(f"🧪 Testing GCP API: {base_url}")
    print("="*60)
    print()
    
    # 1. Test Health
    print("1️⃣ Testing /health...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        if response.status_code == 200:
            print("   ✅ Health check passed")
        else:
            print("   ❌ Health check failed")
        print()
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        print()
        return False
    
    # 2. Test Info
    print("2️⃣ Testing /info...")
    try:
        response = requests.get(f"{base_url}/info", timeout=10)
        print(f"   Status: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        print("   ✅ Info endpoint working")
        print()
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        print()
    
    # 3. Test Predict
    print("3️⃣ Testing /predict...")
    data = {
        "instances": [
            {
                "Rating": 4.5,
                "Reviews": 10000,
                "Size": 25.0,
                "Installs": 1000000,
                "Price": 0.0
            },
            {
                "Rating": 3.0,
                "Reviews": 100,
                "Size": 10.0,
                "Installs": 1000,
                "Price": 2.99
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{base_url}/predict",
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        if response.status_code == 200:
            print("   ✅ Prediction successful")
        else:
            print("   ❌ Prediction failed")
        print()
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        print()
        return False
    
    print("="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_gcp_api.py <API_URL>")
        print("Example: python test_gcp_api.py https://playstore-model-api-xxxx.a.run.app")
        sys.exit(1)
    
    api_url = sys.argv[1].rstrip('/')
    success = test_gcp_api(api_url)
    sys.exit(0 if success else 1)
