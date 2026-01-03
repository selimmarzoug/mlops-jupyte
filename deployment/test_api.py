#!/usr/bin/env python3
"""
Script de test de l'API locale
"""

import requests
import json

# Configuration
API_URL = "http://localhost:8080"

def test_health():
    """Test health endpoint"""
    print("Testing /health...")
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_info():
    """Test info endpoint"""
    print("Testing /info...")
    response = requests.get(f"{API_URL}/info")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print()

def test_predict():
    """Test predict endpoint"""
    print("Testing /predict...")
    
    # Exemple de données
    data = {
        "instances": [
            {
                "Rating": 4.5,
                "Reviews": 10000,
                "Size": 25.0,
                "Installs": 1000000,
                "Price": 0.0
            }
        ]
    }
    
    response = requests.post(
        f"{API_URL}/predict",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

if __name__ == "__main__":
    print("="*50)
    print("🧪 Testing MLflow Model API")
    print("="*50)
    print()
    
    try:
        test_health()
        test_info()
        test_predict()
        print("✅ All tests passed!")
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
