@echo off
echo ===============================================
echo Chemical Equipment Visualizer - Desktop App
echo ===============================================
echo.

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate
) else (
    echo ERROR: Virtual environment not found!
    echo Please run install.bat first
    pause
    exit /b 1
)

REM Check if .env exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Creating from template...
    copy .env.example .env
    echo.
    echo Please edit .env to configure your backend URL
    echo Press any key to continue or Ctrl+C to exit and configure first
    pause
)

echo Starting Chemical Equipment Visualizer...
echo.
echo Make sure your Django backend is running at:
type .env | findstr API_BASE_URL
echo.

python main.py

pause
