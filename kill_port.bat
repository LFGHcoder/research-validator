@echo off
REM Script to kill process using port 8000
echo Finding process using port 8000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    echo Killing process ID: %%a
    taskkill /F /PID %%a
)
echo Done!
pause
