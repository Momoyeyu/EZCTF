#!/bin/bash
set -e

# Ensure we are in the script's directory
cd "$(dirname "$0")"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "=== Backend Setup & Start ==="

# Load environment variables from .env if it exists
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# 1. Check and Install uv
if ! command_exists uv; then
    echo "uv not found. Installing uv..."
    if command_exists curl; then
        curl -LsSf https://astral.sh/uv/install.sh | sh
        if [ -f "$HOME/.cargo/env" ]; then
            source "$HOME/.cargo/env"
        fi
    else
        echo "Error: curl is required to install uv."
        exit 1
    fi
else
    echo "uv is already installed."
fi

# Ensure uv is in path
if ! command_exists uv; then
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# 2. Sync Dependencies
echo "Syncing dependencies with uv..."
uv sync

# 3. Check for existing process on port and kill it
PORT=${PORT:-8000}
HOST=${HOST:-0.0.0.0}
PIDS=$(lsof -t -i:$PORT 2>/dev/null || true)
if [ -n "$PIDS" ]; then
    echo "Port $PORT is already in use by PID(s): $PIDS. Killing..."
    kill -9 $PIDS 2>/dev/null || true
fi

# 4. Start Application
echo "Starting FastAPI application..."
if [ "$1" == "--background" ]; then
    mkdir -p ../logs
    # Start in background and save PID
    nohup uv run uvicorn main:app --app-dir src --reload --host 0.0.0.0 --port $PORT > ../logs/backend.log 2>&1 &
    PID=$!
    echo "Backend started in background (PID: $PID)"
    echo "Logs: logs/backend.log"
else
    uv run uvicorn main:app --app-dir src --reload --host 0.0.0.0 --port $PORT
fi

echo "Backend Service URL: http://localhost:$PORT"
echo "API Documentation: http://localhost:$PORT/docs"
