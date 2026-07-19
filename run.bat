@echo off
echo ==========================================
echo    LUMIORA - Online Learning Platform
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo [1/4] Python found: 
python --version
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo [2/4] Creating virtual environment...
    python -m venv venv
) else (
    echo [2/4] Virtual environment already exists
)

REM Activate virtual environment
echo [3/4] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo [4/4] Installing dependencies...
pip install -r requirements.txt

echo.
echo ==========================================
echo    Starting Lumiora Server...
echo ==========================================
echo.
echo Open your browser and go to: http://127.0.0.1:5000
echo.
echo Press CTRL+C to stop the server
echo.

python app.py

echo.
echo Server stopped.
pause
