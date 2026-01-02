#!/bin/bash
set -e

# Ensure we are in the script's directory
cd "$(dirname "$0")"

# Root run script to start both backend and frontend

# Read configurations from sub-projects
# Use subshell to source .env files to avoid variable collision and pollution
BACKEND_PORT=$(cd backend && [ -f .env ] && set -a && source .env >/dev/null 2>&1 && echo $PORT)
BACKEND_PORT=${BACKEND_PORT:-8000}

FRONTEND_PORT=$(cd frontend && [ -f .env ] && set -a && source .env >/dev/null 2>&1 && echo $PORT)
FRONTEND_PORT=${FRONTEND_PORT:-8080}

# Create logs directory
mkdir -p logs

echo "========================================"
echo "Starting EZCTF Platform..."
echo "========================================"

# Start Backend
echo "[1/2] Starting Backend..."
cd backend
chmod +x run.sh
./run.sh --background
cd ..

echo ""

# Start Frontend
echo "[2/2] Starting Frontend..."
cd frontend
chmod +x run.sh
./run.sh --background
cd ..

echo ""
echo "========================================"
echo "All services initiated."
echo "----------------------------------------"
echo "Backend API:    http://localhost:${BACKEND_PORT}"
echo "API Docs:       http://localhost:${BACKEND_PORT}/docs"
echo "Frontend App:   http://localhost:${FRONTEND_PORT}"
echo "----------------------------------------"
echo "Use './stop.sh' to stop all services."
echo "========================================"
