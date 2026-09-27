#!/bin/bash
# RHA Local Voice Engine - Global Command System

RHA_DIR="$HOME/rha-local-voice-engine"

function show_help() {
    echo "=========================================="
    echo "  RHA Local Voice Engine - Command Suite  "
    echo "=========================================="
    echo "Commands:"
    echo "  rha-start    - Start the RHA AI Server"
    echo "  rha-stop     - Stop the RHA AI Server"
    echo "  rha-status   - Check server and model status"
    echo "  rha-update   - Safely update source code"
    echo "  rha-repair   - Fix broken dependencies"
    echo "  rha          - Interactive dashboard/start"
    echo "=========================================="
}

function start_server() {
    echo "[RHA] Starting AI Server..."
    cd "$RHA_DIR" || { echo "Project directory not found!"; exit 1; }
    source venv/bin/activate
    
    # Check network IP
    IP=$(ifconfig 2>/dev/null | grep 'inet ' | grep -v '127.0.0.1' | awk '{print $2}' | head -n 1)
    if [ -z "$IP" ]; then
        # fallback for ip command
        IP=$(ip addr show 2>/dev/null | grep -w inet | grep -v 127.0.0.1 | awk '{print $2}' | cut -d/ -f1 | head -n 1)
    fi
    
    echo "------------------------------------------------"
    echo " RHA SERVER ONLINE "
    echo " Local: http://127.0.0.1:8000"
    if [ ! -z "$IP" ]; then
        echo " LAN:   http://$IP:8000"
    fi
    echo "------------------------------------------------"
    
    # Start the server (uvicorn)
    python api/server.py
}

function stop_server() {
    echo "[RHA] Stopping AI Server..."
    pkill -f "python api/server.py"
    echo "[RHA] Server stopped."
}

function update_system() {
    echo "[RHA] Updating RHA System safely..."
    cd "$RHA_DIR" || exit 1
    git fetch
    git pull origin main
    if [ ! -d "venv" ]; then
        python -m venv venv
    fi
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "[RHA] Update complete!"
}

function repair_system() {
    echo "[RHA] Running self-repair..."
    cd "$RHA_DIR" || exit 1
    rm -rf venv
    python -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "[RHA] Virtual environment repaired."
}

function status_check() {
    echo "[RHA] System Status Check"
    cd "$RHA_DIR" || exit 1
    source venv/bin/activate
    python -c "import fastapi; print('FastAPI: OK')" 2>/dev/null || echo "FastAPI: MISSING"
    python -c "import whisper_cpp; print('Whisper: OK')" 2>/dev/null || echo "Whisper: MISSING (or using alternative)"
    echo "Server Process:"
    pgrep -f "python api/server.py" >/dev/null && echo "ONLINE" || echo "OFFLINE"
}

CMD_NAME=$(basename "$0")
case "$CMD_NAME" in
    rha-start) start_server ;;
    rha-stop) stop_server ;;
    rha-update) update_system ;;
    rha-repair) repair_system ;;
    rha-status) status_check ;;
    *)
        case "$1" in
            start) start_server ;;
            stop) stop_server ;;
            update) update_system ;;
            repair) repair_system ;;
            status) status_check ;;
            *)
                show_help
                start_server
                ;;
        esac
        ;;
esac
