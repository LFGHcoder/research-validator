# 📝 How to Use the Research Validator API

## Where to Send Your Text/Prompt

You have **3 easy ways** to validate your research text:

---

## Method 1: Interactive Web Interface (Easiest! 🌟)

**Best for:** Quick testing and seeing results visually

1. **Start the API** (if not running):
   ```powershell
   python main.py
   ```

2. **Open your browser** and go to:
   ```
   http://127.0.0.1:8000/docs
   ```
   (or http://127.0.0.1:8001/docs if port 8000 was busy)

3. **Click on `POST /validate`**

4. **Click "Try it out"** button

5. **Enter your research text** in the Request body:
   ```json
   {
     "text": "Your research text goes here. For example: The Eiffel Tower is located in Paris. It was built in 1889. Python is a programming language."
   }
   ```

6. **Click "Execute"**

7. **See the results!** You'll get:
   - Each factual claim found
   - Similarity scores
   - Confidence levels (High/Medium/Low)
   - Best matching evidence snippets and URLs

---

## Method 2: Using PowerShell/Command Line

**Best for:** Quick testing from terminal

**Windows PowerShell:**
```powershell
$body = @{
    text = "The Eiffel Tower is located in Paris. It was built in 1889."
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/validate" -Method POST -ContentType "application/json" -Body $body
```

**Or simpler one-liner:**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/validate" -Method POST -ContentType "application/json" -Body '{"text":"The Eiffel Tower is in Paris."}'
```

---

## Method 3: From Your Frontend/Application

**Best for:** Integrating into your hackathon project

### JavaScript/React Example:
```javascript
async function validateResearch(text) {
  const response = await fetch('http://127.0.0.1:8000/validate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      text: text
    })
  });
  
  const data = await response.json();
  return data;
}

// Use it:
validateResearch("The Eiffel Tower is located in Paris.")
  .then(result => {
    console.log(result);
    // result.validated - true/false
    // result.claims - array of validated claims
    // result.message - status message
  });
```

### Python Example:
```python
import requests

def validate_research(text):
    response = requests.post(
        "http://127.0.0.1:8000/validate",
        json={"text": text}
    )
    return response.json()

# Use it:
result = validate_research("The Eiffel Tower is located in Paris.")
print(result)
```

### cURL Example:
```bash
curl -X POST "http://127.0.0.1:8000/validate" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"The Eiffel Tower is located in Paris.\"}"
```

---

## Example Request & Response

### Request:
```json
{
  "text": "The Eiffel Tower is located in Paris. It was built in 1889. Python is a programming language."
}
```

### Response:
```json
{
  "validated": true,
  "claims": [
    {
      "claim": "The Eiffel Tower is located in Paris.",
      "similarity_score": 0.8523,
      "confidence": "High",
      "best_match_snippet": "The Eiffel Tower is a wrought-iron lattice tower...",
      "best_match_url": "https://example.com/eiffel-tower"
    },
    {
      "claim": "It was built in 1889.",
      "similarity_score": 0.7234,
      "confidence": "Medium",
      "best_match_snippet": "Construction of the Eiffel Tower began in 1887...",
      "best_match_url": "https://example.com/eiffel-history"
    },
    {
      "claim": "Python is a programming language.",
      "similarity_score": 0.9123,
      "confidence": "High",
      "best_match_snippet": "Python is a high-level programming language...",
      "best_match_url": "https://example.com/python"
    }
  ],
  "message": "Processed 3 claim(s) using text-based matching."
}
```

---

## Understanding the Response

- **`validated`**: `true` if at least one claim has Medium or High confidence
- **`claims`**: Array of each factual sentence found:
  - **`claim`**: The factual sentence extracted
  - **`similarity_score`**: 0.0 to 1.0 (higher = more similar to evidence)
  - **`confidence`**: "High", "Medium", or "Low"
  - **`best_match_snippet`**: Best matching evidence text found
  - **`best_match_url`**: URL of the source
- **`message`**: Status message

---

## Tips

1. **Best Results**: Write clear, factual statements (not questions or opinions)
2. **Multiple Claims**: The API processes up to 5 factual sentences
3. **Confidence Levels**:
   - **High** (≥0.8): Strong evidence found
   - **Medium** (≥0.5): Some evidence found
   - **Low** (<0.5): Weak or no evidence found

---

## Quick Test

Try this example text:
```
The Great Wall of China is visible from space. The moon landing happened in 1969. Water boils at 100 degrees Celsius.
```

This will test multiple claims and show you how the validation works!
