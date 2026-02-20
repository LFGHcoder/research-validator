"""
Quick test script for the Research Validator API
Run this after starting the server with: uvicorn main:app --reload
"""
import requests
import json

API_URL = "http://127.0.0.1:8000"

def test_health():
    """Test health check endpoint"""
    print("Testing /health endpoint...")
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_validate():
    """Test validate endpoint"""
    print("Testing /validate endpoint...")
    test_text = "The Eiffel Tower is located in Paris. It was built in 1889. Python is a programming language."
    
    response = requests.post(
        f"{API_URL}/validate",
        json={"text": test_text},
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Validated: {result['validated']}")
        print(f"Claims processed: {len(result['claims'])}")
        print("\nClaim Results:")
        for i, claim in enumerate(result['claims'], 1):
            print(f"\n{i}. Claim: {claim['claim']}")
            print(f"   Similarity: {claim['similarity_score']}")
            print(f"   Confidence: {claim['confidence']}")
            if claim['best_match_url']:
                print(f"   URL: {claim['best_match_url']}")
    else:
        print(f"Error: {response.text}")
    print()

if __name__ == "__main__":
    try:
        test_health()
        test_validate()
        print("✅ Tests completed!")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API. Make sure the server is running:")
        print("   uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ Error: {e}")
