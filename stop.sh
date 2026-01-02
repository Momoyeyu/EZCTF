#!/bin/bash

# Read configurations from sub-projects
# Use subshell to source .env files to avoid variable collision and pollution
BACKEND_PORT=$(cd backend && [ -f .env ] && set -a && source .env >/dev/null 2>&1 && echo $PORT)
BACKEND_PORT=${BACKEND_PORT:-8000}

FRONTEND_PORT=$(cd frontend && [ -f .env ] && set -a && source .env >/dev/null 2>&1 && echo $PORT)
FRONTEND_PORT=${FRONTEND_PORT:-8080}

echo "========================================"
echo "Stopping EZCTF Platform..."
echo "========================================"

# Stop Backend (Port $BACKEND_PORT)
echo "Stopping Backend (Port $BACKEND_PORT)..."
PIDS_BACKEND=$(lsof -t -i:$BACKEND_PORT 2>/dev/null || true)
if [ -n "$PIDS_BACKEND" ]; then
    echo "Found backend process(es): $PIDS_BACKEND. Killing..."
    kill -9 $PIDS_BACKEND 2>/dev/null || true
    echo "Backend stopped."
else
    echo "No running backend process found on port $BACKEND_PORT."
fi

# Stop Frontend (Port $FRONTEND_PORT)
echo "Stopping Frontend (Port $FRONTEND_PORT)..."
PIDS_FRONTEND=$(lsof -t -i:$FRONTEND_PORT 2>/dev/null || true)
if [ -n "$PIDS_FRONTEND" ]; then
    echo "Found frontend process(es): $PIDS_FRONTEND. Killing..."
    kill -9 $PIDS_FRONTEND 2>/dev/null || true
    echo "Frontend stopped."
else
    echo "No running frontend process found on port $FRONTEND_PORT."
fi

# Clean up PID files if they exist (legacy cleanup)
rm -f .backend.pid .frontend.pid

echo "========================================"
echo "All services stopped."
echo "========================================"
