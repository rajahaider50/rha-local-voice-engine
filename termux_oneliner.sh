#!/bin/bash
echo "============================================="
echo " RHA Local Voice Engine - Termux Installer   "
echo "============================================="
echo "Downloading the latest source code from GitHub..."

# Grant storage access first
echo "[1/4] Requesting storage permission..."
termux-setup-storage

# Update and install git
echo "[2/4] Installing dependencies..."
pkg update -y && pkg install git python -y

# Clone repo if it doesn't exist
if [ ! -d "rha-local-voice-engine" ]; then
    echo "[3/4] Cloning RHA repository..."
    git clone https://github.com/rajahaider50/rha-local-voice-engine.git
    cd rha-local-voice-engine
    bash scripts/setup_termux.sh
else
    echo "[3/4] Repository already exists. Pulling latest updates..."
    cd rha-local-voice-engine
    git reset --hard
    git pull origin main
fi

# Always update Python requirements just in case
echo "[4/4] Updating Python packages (FastAPI, etc)..."
if [ ! -d "venv" ]; then
    python -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "============================================="
echo " ✅ Setup Complete! "
echo " To start the engine now, run:"
echo "   cd rha-local-voice-engine"
echo "   source venv/bin/activate"
echo "   python api/server.py"
echo "============================================="
