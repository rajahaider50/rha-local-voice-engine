#!/bin/bash
echo "Starting RHA Local Voice Engine as a Termux Background Service..."

# Ensure we are in the project root
cd "$(dirname "$0")/.." || exit

# Acquire wakelock so Android doesn't kill the CPU process when screen is off
termux-wake-lock

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Error: Virtual environment not found. Please run scripts/setup_termux.sh first."
    exit 1
fi

# Run Uvicorn server in the background, logging to a file
nohup python -m uvicorn api.server:app --host 0.0.0.0 --port 8000 > rha_service.log 2>&1 &
SERVICE_PID=$!

echo "RHA Service started in the background (PID: $SERVICE_PID)."
echo "Logs are being written to rha_service.log"
echo "To stop the service, run: ./scripts/stop_termux_service.sh"
