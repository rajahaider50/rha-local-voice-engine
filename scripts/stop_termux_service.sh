#!/bin/bash
echo "Stopping RHA Local Voice Engine Termux Service..."

# Find and kill the uvicorn process running our app
pkill -f "uvicorn api.server:app"

# Release the wakelock
termux-wake-unlock

echo "Service stopped and wakelock released."
