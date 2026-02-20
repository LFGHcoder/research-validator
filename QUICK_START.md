# 🚀 Quick Start Guide

## Step 1: Install Dependencies

Open PowerShell or Command Prompt in your project folder and run:

```powershell
pip install fastapi uvicorn python-dotenv requests
```

**Or install everything (including optional OpenAI dependencies):**
```powershell
pip install -r requirements.txt
```

## Step 2: Verify Your API Key

Make sure your `.env` file contains:
```
YOU_API_KEY=ydc-sk-your-actual-key-here
```

## Step 3: Run the API

### Option A: Double-click `run.bat`
Just double-click the `run.bat` file in your project folder!

### Option B: Command Line
Open PowerShell/Command Prompt in your project folder:

```powershell
python main.py
```

### Option C: With Auto-Reload (for development)
```powershell
uvicorn main:app --reload
```

## Step 4: Test It!

Once you see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

Open your browser and go to:
- **Interactive API Docs**: http://127.0.0.1:8000/docs
- **Health Check**: http://127.0.0.1:8000/health

## Using the API

### In Browser (Easiest):
1. Go to http://127.0.0.1:8000/docs
2. Click on `POST /validate`
3. Click "Try it out"
4. Enter your text:
   ```json
   {
     "text": "The Eiffel Tower is located in Paris."
   }
   ```
5. Click "Execute"

### Using PowerShell:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/validate" -Method POST -ContentType "application/json" -Body '{"text":"The Eiffel Tower is in Paris."}'
```

## Troubleshooting

**Problem: "Module not found"**
- Solution: Run `pip install -r requirements.txt`

**Problem: "API key not found"**
- Solution: Make sure `.env` file exists with `YOU_API_KEY=your-key`

**Problem: Port already in use**
- Solution: Stop other servers or change port in `main.py`

**Problem: Can't connect**
- Solution: Make sure the server is running (you should see "Uvicorn running")

## Stop the Server

Press `Ctrl+C` in the terminal where it's running.
