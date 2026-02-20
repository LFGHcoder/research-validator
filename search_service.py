import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

YOU_API_KEY = os.getenv("YOU_API_KEY", "")

def search_claim(claim: str):
    url = "https://api.you.com/v1/search"

    headers = {
        "X-API-Key": YOU_API_KEY
    }

    params = {
        "query": claim,
        "num_web_results": 3
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code != 200:
            # Debug: print status for troubleshooting
            print(f"Search API returned status {response.status_code}")
            return []
        
        data = response.json()
    except requests.exceptions.RequestException as e:
        # Log error for debugging
        print(f"Search API request failed: {e}")
        return []
    except Exception as e:
        # Handle JSON parsing errors or other issues
        print(f"Search API JSON parsing failed: {e}")
        return []

    results = []
    for item in data.get("web", {}).get("results", []):
        results.append({
            "title": item.get("title"),
            "snippet": item.get("snippet"),
            "url": item.get("url")
        })

    return results