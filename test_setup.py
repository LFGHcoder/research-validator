"""
Test script to verify the setup is working correctly
"""
import os
import sys
from dotenv import load_dotenv

print("=" * 60)
print("Research Validator - Setup Verification")
print("=" * 60)
print()

# Load environment variables
load_dotenv()

# Check 1: Environment variables
print("1. Checking environment variables...")
you_key = os.getenv("YOU_API_KEY", "")
openai_key = os.getenv("OPENAI_API_KEY", "")

if you_key and you_key != "your-actual-you-api-key-here":
    print("   ✅ YOU_API_KEY is set")
else:
    print("   ❌ YOU_API_KEY is missing or not set properly")
    sys.exit(1)

if openai_key and openai_key != "your-openai-api-key-here":
    print("   ✅ OPENAI_API_KEY is set (optional)")
else:
    print("   ⚠️  OPENAI_API_KEY not set (using text-based fallback)")

print()

# Check 2: Import dependencies
print("2. Checking Python dependencies...")
try:
    import fastapi
    print("   ✅ fastapi")
except ImportError:
    print("   ❌ fastapi - Run: pip install fastapi")
    sys.exit(1)

try:
    import uvicorn
    print("   ✅ uvicorn")
except ImportError:
    print("   ❌ uvicorn - Run: pip install uvicorn")
    sys.exit(1)

try:
    import requests
    print("   ✅ requests")
except ImportError:
    print("   ❌ requests - Run: pip install requests")
    sys.exit(1)

try:
    import numpy
    print("   ✅ numpy (optional)")
except ImportError:
    print("   ⚠️  numpy not installed (optional, only needed for OpenAI)")

try:
    import openai
    print("   ✅ openai (optional)")
except ImportError:
    print("   ⚠️  openai not installed (optional, only needed for embeddings)")

print()

# Check 3: Import main modules
print("3. Checking code imports...")
try:
    from search_service import search_claim
    print("   ✅ search_service.py imports successfully")
except Exception as e:
    print(f"   ❌ search_service.py import failed: {e}")
    sys.exit(1)

try:
    import main
    print("   ✅ main.py imports successfully")
except Exception as e:
    print(f"   ❌ main.py import failed: {e}")
    sys.exit(1)

print()

# Check 4: Test search service (quick test)
print("4. Testing search service...")
try:
    # Quick test - this will make an actual API call
    print("   Testing with query: 'Python programming'")
    results = search_claim("Python programming")
    if isinstance(results, list):
        print(f"   ✅ Search service works! Got {len(results)} results")
        if results:
            print(f"   Sample result: {results[0].get('title', 'N/A')[:50]}...")
    else:
        print("   ⚠️  Search returned unexpected format")
except Exception as e:
    print(f"   ⚠️  Search test failed: {e}")
    print("   (This might be okay if API key is invalid or network issue)")

print()

# Check 5: Test similarity functions
print("5. Testing similarity functions...")
try:
    from main import compute_similarity, map_similarity_to_confidence
    
    # Test with simple text
    similarity = compute_similarity("Python is a language", "Python programming language")
    confidence = map_similarity_to_confidence(similarity)
    
    print(f"   ✅ Similarity function works! Score: {similarity:.3f}, Confidence: {confidence}")
except Exception as e:
    print(f"   ❌ Similarity test failed: {e}")
    sys.exit(1)

print()
print("=" * 60)
print("✅ Setup verification complete!")
print("=" * 60)
print()
print("Next steps:")
print("1. Run the API: python main.py")
print("2. Or use: uvicorn main:app --reload")
print("3. Visit: http://127.0.0.1:8000/docs")
print()
