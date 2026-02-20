# Research Validator API

A FastAPI-based service that validates factual claims in text by searching for evidence and computing similarity scores using OpenAI embeddings.

## Features

- **Text Analysis**: Splits input text into factual sentences (up to 5)
- **Evidence Search**: Searches the web for supporting evidence using You.com API
- **Similarity Scoring**: Uses OpenAI embeddings to compute cosine similarity between claims and evidence
- **Confidence Levels**: Maps similarity scores to High/Medium/Low confidence levels

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

**Required:** `YOU_API_KEY` (for web search)  
**Optional:** `OPENAI_API_KEY` (for better similarity scoring - uses text-based fallback if missing)

Create a `.env` file in the project root:

```env
YOU_API_KEY=your-you-api-key-here
OPENAI_API_KEY=your-openai-api-key-here  # Optional
```

Or set them in your terminal:

**Windows (PowerShell):**
```powershell
$env:YOU_API_KEY="your-key-here"
$env:OPENAI_API_KEY="your-key-here"  # Optional
```

**Linux/Mac:**
```bash
export YOU_API_KEY="your-key-here"
export OPENAI_API_KEY="your-key-here"  # Optional
```

**Note:** The API will work with just `YOU_API_KEY`. Without OpenAI, it uses text-based similarity matching instead of embeddings.

### 3. Run the API

**Windows (Recommended - avoids multiprocessing issues):**
```bash
python main.py
```
Or double-click `run.bat`

**Windows (with auto-reload - may have issues):**
```bash
uvicorn main:app --reload
```
Or double-click `run_reload.bat`

**Linux/Mac:**
```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

**Note:** On Windows, if you encounter multiprocessing errors with `--reload`, use `python main.py` instead.

## API Documentation

Once running, visit:
- **Interactive Docs**: http://127.0.0.1:8000/docs
- **Alternative Docs**: http://127.0.0.1:8000/redoc

## API Endpoint

### POST `/validate`

Validates factual claims in the input text.

**Request:**
```json
{
  "text": "The Eiffel Tower is located in Paris. It was built in 1889."
}
```

**Response:**
```json
{
  "validated": true,
  "claims": [
    {
      "claim": "The Eiffel Tower is located in Paris.",
      "similarity_score": 0.85,
      "confidence": "High",
      "best_match_snippet": "The Eiffel Tower is a wrought-iron lattice tower...",
      "best_match_url": "https://example.com"
    }
  ],
  "message": "Processed 2 claim(s)."
}
```

## Confidence Levels

- **High**: Similarity score ≥ 0.8
- **Medium**: Similarity score ≥ 0.5 and < 0.8
- **Low**: Similarity score < 0.5

## Project Structure

```
research-validator/
├── main.py              # FastAPI app and validation logic
├── search_service.py    # You.com API integration
├── requirements.txt     # Python dependencies
├── .env                # Environment variables (not in git)
├── .env.example        # Example environment variables
└── README.md           # This file
```

## Testing

Test the API using curl:

```bash
curl -X POST "http://127.0.0.1:8000/validate" \
  -H "Content-Type: application/json" \
  -d '{"text": "The Eiffel Tower is in Paris."}'
```

Or use the interactive docs at `/docs` endpoint.

## Notes

- The API processes up to 5 factual sentences per request
- Each claim is searched independently
- Similarity scores are computed using OpenAI's `text-embedding-3-small` model
- The service gracefully handles API failures and missing results
