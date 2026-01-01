#!/bin/bash
set -e

# Ensure we are in the script's directory
cd "$(dirname "$0")"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "=== Frontend Setup & Start ==="

# 1. Check Node.js environment
if ! command_exists node; then
    echo "Node.js not found."
    if [ -s "$HOME/.nvm/nvm.sh" ]; then
        echo "Loading NVM..."
        source "$HOME/.nvm/nvm.sh"
    elif [ -s "/usr/local/opt/nvm/nvm.sh" ]; then
         source "/usr/local/opt/nvm/nvm.sh"
    fi

    if ! command_exists node; then
        echo "Attempting to install Node.js..."
        if command_exists nvm; then
            echo "Installing Node.js LTS via nvm..."
            nvm install --lts
            nvm use --lts
        elif command_exists brew; then
            echo "Installing Node.js via Homebrew..."
            brew install node
        else
            echo "Error: Node.js is required but not found."
            echo "Please install Node.js manually: https://nodejs.org/"
            exit 1
        fi
    fi
else
    echo "Node.js is installed: $(node -v)"
fi

# 2. Install Dependencies
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies (npm install)..."
    npm install
else
    echo "node_modules exists. Skipping npm install."
fi

# 3. Check for existing process on port 8080 and kill it
PORT=8080
PIDS=$(lsof -t -i:$PORT 2>/dev/null || true)
if [ -n "$PIDS" ]; then
    echo "Port $PORT is already in use by PID(s): $PIDS. Killing..."
    kill -9 $PIDS 2>/dev/null || true
fi

# 4. Start Application
echo "Starting Vue.js application..."

if [ "$1" == "--background" ]; then
    mkdir -p ../../logs
    # Start in background
    nohup npm run serve > ../../logs/frontend.log 2>&1 &
    PID=$!
    echo "Frontend started in background (PID: $PID)"
    echo "Logs: logs/frontend.log"
else
    npm run serve
fi

echo "Frontend Service URL: http://localhost:$PORT"
