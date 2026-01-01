#!/bin/bash

echo "========================================"
echo "Stopping EZCTF Platform..."
echo "========================================"

# Stop Backend (Port 8000)
echo "Stopping Backend (Port 8000)..."
PIDS_BACKEND=$(lsof -t -i:8000 2>/dev/null || true)
if [ -n "$PIDS_BACKEND" ]; then
    echo "Found backend process(es): $PIDS_BACKEND. Killing..."
    kill -9 $PIDS_BACKEND 2>/dev/null || true
    echo "Backend stopped."
else
    echo "No running backend process found on port 8000."
fi

# Stop Frontend (Port 8080)
echo "Stopping Frontend (Port 8080)..."
PIDS_FRONTEND=$(lsof -t -i:8080 2>/dev/null || true)
if [ -n "$PIDS_FRONTEND" ]; then
    echo "Found frontend process(es): $PIDS_FRONTEND. Killing..."
    kill -9 $PIDS_FRONTEND 2>/dev/null || true
    echo "Frontend stopped."
else
    echo "No running frontend process found on port 8080."
fi

# Clean up PID files if they exist (legacy cleanup)
rm -f .backend.pid .frontend.pid

echo "========================================"
echo "All services stopped."
echo "========================================"
