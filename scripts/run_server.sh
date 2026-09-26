#!/bin/bash

echo "Starting RHA Local Development Server..."

# Ensure we are in the project root
cd "$(dirname "$0")/.." || exit

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running install script..."
    bash scripts/install.sh
fi

# Activate virtual environment
source venv/bin/activate

# Start the FastAPI server using Uvicorn
echo "Server will be available at: http://localhost:8000"
echo "API Docs will be available at: http://localhost:8000/docs"
python -m uvicorn api.server:app --host 0.0.0.0 --port 8000 --reload
