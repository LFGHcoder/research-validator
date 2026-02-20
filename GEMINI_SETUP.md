# Gemini API Setup - Quick Guide

## Step 1: Add Your Gemini API Key

1. **Open the `.env` file**:
   ```
   c:\Users\Shubha pandey\OneDrive\Desktop\research-validator\.env
   ```

2. **Replace this line**:
   ```
   GEMINI_API_KEY=your-gemini-api-key-here
   ```
   
   **With your actual Gemini key**:
   ```
   GEMINI_API_KEY=your-actual-gemini-key-here
   ```

3. **Save the file**

## Step 2: Install Gemini Library

Run this command in PowerShell:

```powershell
pip install google-generativeai
```

Or install all dependencies:

```powershell
pip install -r requirements.txt
```

## Step 3: Restart Your Backend

1. **Stop the server** (if running): Press `Ctrl+C`
2. **Start it again**:
   ```powershell
   python main.py
   ```

## Step 4: Verify It's Working

Visit: http://127.0.0.1:8000/health

You should see:
```json
{
  "gemini_api_key": "set",
  "similarity_method": "Gemini embeddings (free tier)"
}
```

## How It Works Now

The API will try embeddings in this order:
1. **Gemini** (free tier) - First choice ✅
2. **OpenAI** (if Gemini fails) - Fallback
3. **Text matching** (if both fail) - Last resort

This gives you:
- ✅ **Free tier** for hackathons (Gemini)
- ✅ **Backup option** (OpenAI)
- ✅ **Always works** (text fallback)

## Get Your Gemini API Key

If you don't have one yet:
1. Go to: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key
4. Add it to your `.env` file

That's it! Your API now uses Gemini's free tier for better accuracy! 🎉
