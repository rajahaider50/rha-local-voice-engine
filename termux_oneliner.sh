#!/bin/bash
echo "============================================="
echo " RHA Local Voice Engine - Termux Installer   "
echo "============================================="
echo "Downloading the latest source code from GitHub..."

# Grant storage access first
echo "[1/4] Requesting storage permission..."
termux-setup-storage

# Update and install git
echo "[2/4] Installing Git..."
pkg update -y && pkg install git -y

# Clone repo if it doesn't exist
if [ ! -d "rha-local-voice-engine" ]; then
    echo "[3/4] Cloning RHA repository..."
    git clone https://github.com/rajahaider50/rha-local-voice-engine.git
else
    echo "[3/4] Repository already exists. Pulling latest updates..."
    cd rha-local-voice-engine
    git pull origin main
    cd ..
fi

# Enter repo and run setup
cd rha-local-voice-engine
echo "[4/4] Running automated setup..."
bash scripts/setup_termux.sh

echo "============================================="
echo " ✅ Setup Complete! "
echo " To start the engine now, run:"
echo "   cd rha-local-voice-engine"
echo "   source venv/bin/activate"
echo "   python scripts/download_models.py"
echo "   python engine/core/pipeline.py"
echo "============================================="
