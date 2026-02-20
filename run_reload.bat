@echo off
REM Windows batch script to run the FastAPI server with reload
REM Note: --reload may have issues on Windows, use run.bat if this fails

echo Starting Research Validator API with auto-reload...
echo.
echo Make sure you have set your API keys in .env file or environment variables
echo.

uvicorn main:app --reload --host 127.0.0.1 --port 8000
