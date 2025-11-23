@echo off
echo ===============================================
echo Chemical Equipment Visualizer - Desktop App
echo ===============================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

echo Activating virtual environment...
call venv\Scripts\activate
echo.

echo Installing dependencies...
pip install -r requirements.txt
echo.

REM Check if .env exists
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env file to configure your backend URL
    echo.
)

echo ===============================================
echo Installation complete!
echo ===============================================
echo.
echo To run the application:
echo   1. Make sure Django backend is running
echo   2. Run: python main.py
echo.
pause
