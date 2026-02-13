@echo off
title Missing Person Detection System - Setup and Launch
color 0A

echo ========================================
echo  Missing Person Detection System
echo ========================================
echo.

:: Check if Python is installed
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)
echo ✓ Python found

:: Check if Node.js is installed
echo [2/6] Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js and try again
    pause
    exit /b 1
)
echo ✓ Node.js found

:: Create virtual environment if it doesn't exist
echo [3/6] Setting up Python virtual environment...
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)

:: Activate virtual environment and install backend dependencies
echo [4/6] Installing backend dependencies...
call venv\Scripts\activate.bat
cd backend
echo Resetting database for fresh start...
if exist missing_persons.db del missing_persons.db
echo Installing Python packages...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install backend dependencies
    pause
    exit /b 1
)
echo ✓ Backend dependencies installed
cd ..

:: Install frontend dependencies
echo [5/6] Installing frontend dependencies...
cd frontend
echo Installing Node.js packages...
call npm install
if errorlevel 1 (
    echo ERROR: Failed to install frontend dependencies
    pause
    exit /b 1
)
echo ✓ Frontend dependencies installed
cd ..

echo [6/6] Starting servers...
echo.
echo ========================================
echo  Launching Application
echo ========================================
echo.
echo Backend will start on: http://localhost:8000
echo Frontend will start on: http://localhost:3000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C in any window to stop the servers
echo ========================================
echo.

:: Start backend server in new window
echo Starting backend server...
start "Missing Person - Backend Server" cmd /k "cd /d "%~dp0" && call venv\Scripts\activate.bat && cd backend && python main.py"

:: Wait a moment for backend to start
timeout /t 3 /nobreak >nul

:: Start frontend server in new window and open browser
echo Starting frontend server...
start "Missing Person - Frontend Server" cmd /k "cd /d "%~dp0frontend" && npm start"

:: Wait for frontend to start and open browser
echo.
echo Waiting for servers to start...
timeout /t 8 /nobreak >nul

:: Open browser automatically
echo Opening application in browser...
start http://localhost:3000

echo.
echo ========================================
echo  Application Started Successfully!
echo ========================================
echo.
echo Frontend: http://localhost:3000
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Both servers are running in separate windows.
echo Close those windows or press Ctrl+C to stop the servers.
echo.
pause