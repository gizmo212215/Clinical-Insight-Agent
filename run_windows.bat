@echo off
SETLOCAL
TITLE Clinical Insight Agent Launcher

echo ======================================================
echo 🧬 Clinical Insight Agent - Startup Script
echo ======================================================

if not exist ".venv" (
    echo [INFO] Virtual environment not found. Creating one...
    python -m venv .venv
) else (
    echo [INFO] Virtual environment found.
)

call .venv\Scripts\activate

echo [INFO] Checking dependencies...
pip install -r requirements.txt --quiet
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install dependencies. Please check your internet connection.
    pause
    exit /b
)

if not exist ".env" (
    echo [WARNING] .env file not found! Creating a template...
    echo GOOGLE_API_KEY=replace_with_your_api_key> .env
    echo DATABASE_URL=sqlite:///./data/clinical_trials.db>> .env
    echo CHROMA_PERSIST_DIR=./data/chroma_db>> .env
    echo PROJECT_NAME=Clinical Agent>> .env
    echo VERSION=1.0.0>> .env
    echo LOG_DIR=./data/raw_logs>> .env
    
    echo ======================================================
    echo [IMPORTANT] A '.env' file has been created.
    echo Please open it and paste your GOOGLE_API_KEY before continuing.
    echo ======================================================
    pause
    exit /b
)

echo [INFO] Launching Backend Server...
start "Backend API (FastAPI)" cmd /k "call .venv\Scripts\activate && uvicorn backend.main:app --reload"

timeout /t 5 /nobreak >nul

echo [INFO] Launching Frontend UI...
start "Frontend UI (Streamlit)" cmd /k "call .venv\Scripts\activate && streamlit run frontend/app.py"

echo.
echo [SUCCESS] System is running!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:8501
echo.
echo Press any key to exit this launcher (Servers will keep running)...
pause >nul