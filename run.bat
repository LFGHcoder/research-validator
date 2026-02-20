@echo off
REM Windows batch script to run the FastAPI server
REM This avoids multiprocessing issues with --reload on Windows

echo Starting Research Validator API...
echo.
echo Make sure you have set your API keys in .env file or environment variables
echo.

python main.py
