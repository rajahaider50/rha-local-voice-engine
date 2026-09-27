#!/bin/bash
echo "============================================="
echo " RHA Local Voice Engine - Termux Installer   "
echo "============================================="

# 1. System Checks
echo "[1/6] Checking system..."
if [ -z "$PREFIX" ]; then
    echo "Warning: Not running in Termux! Some commands might fail."
else
    echo "Termux environment detected."
    # Request storage
    termux-setup-storage
fi

# 2. Dependencies
echo "[2/6] Installing OS dependencies..."
pkg update -y
pkg install -y git python clang cmake make libffi openssl pkg-config sqlite termux-api pulseaudio

# 3. Clone / Update Repository (Idempotent)
echo "[3/6] Fetching Source Code..."
if [ ! -d "$HOME/rha-local-voice-engine" ]; then
    cd $HOME
    git clone https://github.com/rajahaider50/rha-local-voice-engine.git
    cd rha-local-voice-engine
else
    echo "Repository already exists. Updating..."
    cd $HOME/rha-local-voice-engine
    git reset --hard
    git pull origin main
fi

# 4. Python Virtual Environment
echo "[4/6] Setting up Python Environment (This may take a while)..."
if [ ! -d "venv" ]; then
    python -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 5. Global Command Installation
echo "[5/6] Installing global 'rha' commands..."
if [ -n "$PREFIX" ]; then
    cp scripts/rha_cmd.sh $PREFIX/bin/rha
    chmod +x $PREFIX/bin/rha
    
    # Create symlinks for aliases
    ln -sf $PREFIX/bin/rha $PREFIX/bin/rha-start
    ln -sf $PREFIX/bin/rha $PREFIX/bin/rha-stop
    ln -sf $PREFIX/bin/rha $PREFIX/bin/rha-status
    ln -sf $PREFIX/bin/rha $PREFIX/bin/rha-update
    ln -sf $PREFIX/bin/rha $PREFIX/bin/rha-repair
else
    # Fallback for standard Linux
    sudo cp scripts/rha_cmd.sh /usr/local/bin/rha
    sudo chmod +x /usr/local/bin/rha
fi

# 6. Final Status
echo "============================================="
echo " ✅ Setup Complete! "
echo " You can now start the server anytime by typing:"
echo " "
echo "   rha "
echo " "
echo "============================================="

# Start immediately
rha start
