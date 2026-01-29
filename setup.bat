@echo off
REM Project Setup Script for Windows

echo.
echo =========================================
echo Olympic Efficiency Analysis - Setup
echo =========================================
echo.

REM Check Python version
python --version

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Install package in development mode
echo Installing package...
pip install -e .

REM Create necessary directories
echo Creating directories...
if not exist "data\raw" mkdir data\raw
if not exist "data\processed" mkdir data\processed
if not exist "notebooks" mkdir notebooks
if not exist "logs" mkdir logs
if not exist "models" mkdir models
if not exist "outputs\plots" mkdir outputs\plots
if not exist "outputs\reports" mkdir outputs\reports
if not exist "outputs\metrics" mkdir outputs\metrics

echo.
echo =========================================
echo Setup Complete!
echo =========================================
echo.
echo Next steps:
echo 1. Activate environment: venv\Scripts\activate.bat
echo 2. Run pipeline: python mlops_pipeline.py
echo 3. Start Flask: python flask_app.py
echo 4. Run tests: pytest tests\
echo.
pause
