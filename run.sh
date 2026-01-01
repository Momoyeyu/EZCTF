#!/bin/bash
set -e

# Ensure we are in the script's directory
cd "$(dirname "$0")"

# Root run script to start both backend and frontend

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
echo "Backend API:    http://localhost:8000"
echo "API Docs:       http://localhost:8000/docs"
echo "Frontend App:   http://localhost:8080"
echo "----------------------------------------"
echo "Use './stop.sh' to stop all services."
echo "========================================"
