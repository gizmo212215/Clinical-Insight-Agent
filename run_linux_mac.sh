#!/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' 

echo -e "${GREEN}======================================================${NC}"
echo -e "${GREEN}🧬 Clinical Insight Agent - Startup Script${NC}"
echo -e "${GREEN}======================================================${NC}"


if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}[INFO] Virtual environment not found. Creating one...${NC}"
    python3 -m venv .venv
else
    echo -e "${GREEN}[INFO] Virtual environment found.${NC}"
fi

source .venv/bin/activate

echo -e "${YELLOW}[INFO] Installing/Updating dependencies...${NC}"
pip install -r requirements.txt -q

if [ ! -f ".env" ]; then
    echo -e "${RED}[WARNING] .env file not found! Creating a template...${NC}"
    
    echo "GOOGLE_API_KEY=replace_with_your_api_key" > .env
    echo "DATABASE_URL=sqlite:///./data/clinical_trials.db" >> .env
    echo "CHROMA_PERSIST_DIR=./data/chroma_db" >> .env
    echo "PROJECT_NAME=Clinical Agent" >> .env
    echo "VERSION=1.0.0" >> .env
    echo "LOG_DIR=./data/raw_logs" >> .env

    echo -e "${RED}======================================================${NC}"
    echo -e "${RED}[IMPORTANT] A '.env' file has been created.${NC}"
    echo -e "${RED}Please open it and add your GOOGLE_API_KEY before running this script again.${NC}"
    echo -e "${RED}======================================================${NC}"
    exit 1
fi

cleanup() {
    echo -e "\n${YELLOW}[INFO] Shutting down services...${NC}"
    kill $BACKEND_PID
    exit
}

trap cleanup SIGINT

echo -e "${GREEN}[INFO] Starting Backend Server...${NC}"
uvicorn backend.main:app --reload &
BACKEND_PID=$! 

echo -e "${YELLOW}[INFO] Waiting 5 seconds for backend to initialize...${NC}"
sleep 5

echo -e "${GREEN}[INFO] Starting Frontend UI...${NC}"
echo -e "${GREEN}[INFO] Press Ctrl+C to stop the application.${NC}"
streamlit run frontend/app.py

wait