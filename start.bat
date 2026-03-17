@echo off
REM NewsPulse Dashboard - Quick Start Script

echo.
echo ============================================
echo   NewsPulse - News Analytics Dashboard
echo ============================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/5] Python found. Checking dependencies...
echo.

REM Check if requirements installed
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo [2/5] Installing dependencies...
    call pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
    echo [2/5] Dependencies installed successfully!
    echo.
)

REM Download NLTK data
echo [3/5] Downloading NLTK data...
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)"
echo [3/5] NLTK data downloaded!
echo.

REM Check if .env exists
if not exist ".env" (
    echo [4/5] Creating .env file...
    echo NEWS_API_KEY=your_news_api_key_here > .env
    echo ADMIN_USERNAME=admin >> .env
    echo ADMIN_PASSWORD=NewsPulse@2024 >> .env
    echo DATABASE_PATH=./data/newspulse.db >> .env
    echo.
    echo *** IMPORTANT: Edit .env file and add your News API key ***
    echo Get it from: https://newsapi.org/
    echo.
    pause
)

REM Check if data directory exists
if not exist "data" (
    echo [4/5] Creating data directory...
    mkdir data
)

REM Check if models directory exists
if not exist "models" (
    echo [4/5] Creating models directory...
    mkdir models
)

echo [4/5] Directories ready!
echo.

REM Ask what to do
echo [5/5] What would you like to do?
echo.
echo   1. Fetch news data
echo   2. Train sentiment model
echo   3. Start dashboard
echo   4. All of the above
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo.
    echo Fetching news data...
    python news_scraper.py
    pause
) else if "%choice%"=="2" (
    echo.
    echo Training sentiment model...
    python train_model.py
    pause
) else if "%choice%"=="3" (
    echo.
    echo Starting NewsPulse Dashboard...
    echo Open your browser to: http://localhost:8501
    echo Login with: admin / NewsPulse@2024
    echo.
    streamlit run app.py
) else if "%choice%"=="4" (
    echo.
    echo Fetching news data...
    python news_scraper.py
    echo.
    echo Training sentiment model...
    python train_model.py
    echo.
    echo Starting NewsPulse Dashboard...
    echo Open your browser to: http://localhost:8501
    echo Login with: admin / NewsPulse@2024
    echo.
    streamlit run app.py
) else (
    echo Invalid choice. Starting dashboard...
    streamlit run app.py
)
