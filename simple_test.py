"""
Simple test to see what's happening
"""
import requests
import json

url = "http://127.0.0.1:8000/validate"

# Test with simple text
test_data = {
    "text": "The Eiffel Tower is located in Paris"
}

print("Sending request...")
print(f"Text: {test_data['text']}")

try:
    response = requests.post(url, json=test_data, timeout=30)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")
