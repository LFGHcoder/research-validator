from search_service import search_claim

results = search_claim("The Eiffel Tower is located in Paris.")

for r in results:
    print(r)