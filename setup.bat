@echo off
setlocal EnableExtensions EnableDelayedExpansion

echo ========================================
echo Missing Person Detection System Setup
echo ========================================
echo.

REM Check prerequisites
echo [1/6] Checking Prerequisites...
where python >nul 2>&1 || (echo ERROR: Python not found! && pause && exit /b 1)
where node >nul 2>&1 || (echo ERROR: Node.js not found! && pause && exit /b 1)
where npm >nul 2>&1 || (echo ERROR: npm not found! && pause && exit /b 1)
echo ✓ All prerequisites found

echo.
echo [2/6] Setting up Backend...
cd backend

REM Check if venv exists and has face-recognition
if exist "venv\Scripts\python.exe" (
    call venv\Scripts\activate
    python -c "import face_recognition" >nul 2>&1
    if not errorlevel 1 (
        echo ✓ Virtual environment with face-recognition already exists
        goto skip_install
    )
    call venv\Scripts\deactivate
)

REM Remove old venv and create new one
if exist venv rmdir /s /q venv
python -m venv venv --clear
call venv\Scripts\activate

REM Install core dependencies (skip face-recognition for now)
echo Installing core dependencies...
python -m pip install --upgrade pip setuptools wheel
python -m pip install fastapi uvicorn[standard] sqlalchemy python-multipart
python -m pip install python-jose[cryptography] passlib[bcrypt]
python -m pip install python-dotenv pydantic email-validator aiofiles
python -m pip install numpy opencv-python Pillow

REM Try to install face-recognition with fallback
echo Installing face recognition (this may take time)...
python -m pip install face-recognition >nul 2>&1
if errorlevel 1 (
    echo WARNING: face-recognition failed to install. Installing alternative...
    python -m pip install opencv-python mediapipe
)

:skip_install
REM Setup .env
if not exist .env (
    if exist .env.example (
        copy .env.example .env >nul
    ) else (
        echo DATABASE_URL=sqlite:///./missing_persons.db > .env
        echo SECRET_KEY=missing-person-secret-key >> .env
        echo SMTP_SERVER=smtp.gmail.com >> .env
        echo SMTP_PORT=587 >> .env
        echo SMTP_USERNAME=your-email@gmail.com >> .env
        echo SMTP_PASSWORD=your-app-password >> .env
        echo FROM_EMAIL=your-email@gmail.com >> .env
        echo FACE_MATCH_THRESHOLD=0.6 >> .env
    )
)

REM Create directories
if not exist uploads mkdir uploads
if not exist uploads\cases mkdir uploads\cases
if not exist uploads\sightings mkdir uploads\sightings

call venv\Scripts\deactivate
cd ..

echo.
echo [3/6] Setting up Frontend...
cd frontend
if not exist node_modules npm install --silent
cd ..

echo.
echo [4/6] Starting Backend Server...
start "Backend Server" cmd /k "cd /d "%cd%\backend" && call venv\Scripts\activate && echo Backend starting at http://localhost:8000 && python main.py"

echo.
echo [5/6] Starting Frontend Server...
timeout /t 3 /nobreak >nul
start "Frontend Server" cmd /k "cd /d "%cd%\frontend" && echo Frontend starting at http://localhost:3000 && npm start"

echo.
echo [6/6] Opening Application...
timeout /t 8 /nobreak >nul
start "" "http://localhost:3000"

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo ✓ Backend: http://localhost:8000
echo ✓ Frontend: http://localhost:3000
echo ✓ API Docs: http://localhost:8000/docs
echo.
echo Both servers are running in separate windows.
echo The browser should open automatically.
echo.
echo To stop: Close the server windows
echo To restart: Run setup.bat again
echo.
pause