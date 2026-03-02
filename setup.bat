@echo off
REM Digital Catalyst - Quick Start Installation Script for Windows
REM This script automates the setup process

echo ==================================
echo Digital Catalyst - Quick Setup
echo ==================================
echo.

REM Check Python version
echo Checking Python version...
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
echo Virtual environment created
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
echo Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo Dependencies installed
echo.

REM Display success message
echo ==================================
echo Setup Complete!
echo ==================================
echo.
echo To start the application:
echo 1. Activate virtual environment: venv\Scripts\activate
echo 2. Run the app: python app.py
echo 3. Open browser: http://localhost:5000
echo.
echo Default login credentials:
echo Username: admin
echo Password: admin123
echo.
echo Happy coding!
echo.
pause
