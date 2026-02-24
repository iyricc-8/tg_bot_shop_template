@echo off
REM ========================
REM Telegram Bot Shop - Launch Script
REM Windows PowerShell version
REM ========================

echo.
echo    ==========================================
echo              TELEGRAM BOT ONLINE SHOP
echo              Launching Script
echo    ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.9+
    echo Visit: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python installed

REM Check if virtual environment exists
if not exist "venv\" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
pip list | findstr "aiogram" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing dependencies...
    pip install -r requirements.txt
    echo [OK] Dependencies installed
) else (
    echo [OK] Dependencies already installed
)

REM Check if .env file exists
if not exist ".env" (
    echo [WARNING] .env file not found!
    echo [INFO] Creating from .env.dist...
    copy .env.dist .env
    echo [OK] .env file created
    echo.
    echo [IMPORTANT] Please edit .env file with your settings:
    echo   - BOT_TOKEN=your_bot_token
    echo   - DB_HOST, DB_USER, DB_PASSWORD
    echo   - ADMINS=your_admin_id
    echo.
    pause
)

REM Check MySQL connection
echo.
echo [INFO] Checking MySQL connection...
python -c "import mysql.connector; print('[OK] MySQL driver available')" 2>nul
if errorlevel 1 (
    echo [WARNING] MySQL connector not available
)

REM Start the bot
echo.
echo [INFO] Starting bot...
echo ==========================================
echo.
python main.py

REM If bot stops, wait before exiting
echo.
echo ==========================================
echo Bot stopped. Waiting 5 seconds before closing...
timeout /t 5

