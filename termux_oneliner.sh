#!/bin/bash
# Strict error handling
set -Eeuo pipefail

# Error trap function
function error_handler() {
    local line_no=$1
    local err_code=$2
    echo "============================================="
    echo " ❌ INSTALLATION FAILED! "
    echo " Error on line $line_no (Exit code: $err_code)"
    echo " The installation could not complete."
    echo "============================================="
    exit $err_code
}
trap 'error_handler ${LINENO} $?' ERR

echo "============================================="
echo " RHA Local Voice Engine - Termux Installer   "
echo "============================================="

echo "[1/7] System Checks..."
if [ -z "${PREFIX:-}" ]; then
    echo "Warning: Not running in Termux. Proceeding with standard Linux setup..."
else
    echo "Termux environment detected."
    # Request storage only if not already granted
    if [ ! -d ~/storage ]; then
        echo "Requesting storage permission..."
        termux-setup-storage
        sleep 2
    fi
fi

echo "[2/7] Installing OS dependencies..."
if [ -n "${PREFIX:-}" ]; then
    pkg update -y
    pkg install -y git python clang cmake make libffi openssl pkg-config sqlite termux-api pulseaudio python-numpy
fi

echo "[3/7] Fetching Source Code..."
if [ ! -d "$HOME/rha-local-voice-engine" ]; then
    cd $HOME
    git clone https://github.com/rajahaider50/rha-local-voice-engine.git
    cd rha-local-voice-engine
else
    echo "Repository exists. Updating..."
    cd $HOME/rha-local-voice-engine
    git fetch
    git reset --hard origin/main
fi

echo "[4/7] Setting up Python Environment..."
if [ ! -d "venv" ]; then
    python -m venv --system-site-packages venv
fi
source venv/bin/activate
pip install --upgrade pip

echo "[5/7] Installing Core Packages..."
pip install -r requirements-core.txt

echo "[6/7] Verifying Dependencies..."
python -c "import fastapi" || { echo "FastAPI failed to install!"; exit 1; }
python -c "import uvicorn" || { echo "Uvicorn failed to install!"; exit 1; }
python -c "import multipart" || { echo "python-multipart failed to install!"; exit 1; }
echo "Core dependencies verified successfully."

echo "[7/7] Installing Global Commands..."
if [ -n "${PREFIX:-}" ]; then
    cp scripts/rha_cmd.sh $PREFIX/bin/rha
    chmod +x $PREFIX/bin/rha
    ln -sf $PREFIX/bin/rha $PREFIX/bin/rha-start
    ln -sf $PREFIX/bin/rha $PREFIX/bin/rha-stop
    ln -sf $PREFIX/bin/rha $PREFIX/bin/rha-status
    ln -sf $PREFIX/bin/rha $PREFIX/bin/rha-update
    ln -sf $PREFIX/bin/rha $PREFIX/bin/rha-repair
    ln -sf $PREFIX/bin/rha $PREFIX/bin/rha-logs
    ln -sf $PREFIX/bin/rha $PREFIX/bin/rha-models
    ln -sf $PREFIX/bin/rha $PREFIX/bin/rha-doctor
else
    sudo cp scripts/rha_cmd.sh /usr/local/bin/rha
    sudo chmod +x /usr/local/bin/rha
fi

echo "============================================="
echo " ✅ RHA INSTALLATION SUCCESSFUL! "
echo " You can now start the server by typing: rha"
echo "============================================="
