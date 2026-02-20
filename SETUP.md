# Quick Setup Guide

## Minimum Setup (YOU_API_KEY only)

1. **Create `.env` file** in the project root:
   ```
   YOU_API_KEY=your-you-api-key-here
   ```

2. **Install basic dependencies:**
   ```bash
   pip install fastapi uvicorn python-dotenv requests
   ```

3. **Run the API:**
   ```bash
   python main.py
   ```
   Or double-click `run.bat`

4. **Test it:**
   - Visit: http://127.0.0.1:8000/docs
   - Or check health: http://127.0.0.1:8000/health

## With OpenAI (Optional - Better Similarity Scoring)

If you want better similarity scoring, add OpenAI:

1. **Add to `.env`:**
   ```
   YOU_API_KEY=your-you-api-key-here
   OPENAI_API_KEY=your-openai-api-key-here
   ```

2. **Install full dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## How It Works

- **With only YOU_API_KEY**: Uses text-based keyword matching for similarity
- **With both keys**: Uses OpenAI embeddings for more accurate similarity scoring

Both methods work! OpenAI just gives better results.
