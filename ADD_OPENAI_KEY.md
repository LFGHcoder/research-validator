# Adding Your OpenAI API Key

## Quick Steps:

1. **Open the `.env` file** in your project folder:
   ```
   c:\Users\Shubha pandey\OneDrive\Desktop\research-validator\.env
   ```

2. **Add your OpenAI API key** on a new line:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```
   
   Replace `sk-your-actual-key-here` with your real OpenAI API key.

3. **Save the file**

4. **Restart your backend** (if it's running):
   - Press `Ctrl+C` to stop it
   - Run `python main.py` again

## Verify It's Working:

1. Visit: http://127.0.0.1:8000/health
2. You should see:
   ```json
   {
     "openai_api_key": "set",
     "similarity_method": "OpenAI embeddings"
   }
   ```

## What This Does:

- ✅ Uses **OpenAI embeddings** for much more accurate similarity scoring
- ✅ Better at detecting if claims are actually true or false
- ✅ More reliable confidence levels (High/Medium/Low)

Your API will now use AI-powered similarity instead of simple text matching!
