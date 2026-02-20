"""
Debug script to test the sentence splitting and see what's happening
"""
from main import split_into_factual_sentences
from search_service import search_claim
import os
from dotenv import load_dotenv

load_dotenv()

# Test different types of input
test_texts = [
    "The Eiffel Tower is located in Paris.",
    "The Eiffel Tower is located in Paris. It was built in 1889.",
    "Python is a programming language",
    "The moon landing happened in 1969",
    "Water boils at 100 degrees Celsius",
    "What is Python?",
    "I think Python is great",
]

print("=" * 60)
print("Testing Sentence Splitting")
print("=" * 60)

for text in test_texts:
    print(f"\nInput: '{text}'")
    sentences = split_into_factual_sentences(text, max_sentences=5)
    print(f"Found {len(sentences)} sentences:")
    for i, s in enumerate(sentences, 1):
        print(f"  {i}. {s}")

print("\n" + "=" * 60)
print("Testing Search API")
print("=" * 60)

# Test search
test_query = "The Eiffel Tower is located in Paris"
print(f"\nSearching for: '{test_query}'")
results = search_claim(test_query)
print(f"Got {len(results)} results")
if results:
    for i, r in enumerate(results[:2], 1):
        print(f"\nResult {i}:")
        print(f"  Title: {r.get('title', 'N/A')}")
        print(f"  Snippet: {r.get('snippet', 'N/A')[:100]}...")
        print(f"  URL: {r.get('url', 'N/A')}")
else:
    print("No results found!")
    print(f"API Key set: {bool(os.getenv('YOU_API_KEY'))}")
