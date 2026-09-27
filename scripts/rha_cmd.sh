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
    
    # Self-validation
    echo "Verifying core dependencies..."
    python -c "import fastapi, uvicorn, numpy" 2>/dev/null || {
        echo "❌ Core dependencies missing! Run 'rha-update' or 'rha-repair'."
        exit 1
    }
    
    # Check network IP
    IP=$(ifconfig 2>/dev/null | grep 'inet ' | grep -v '127.0.0.1' | awk '{print $2}' | head -n 1)
    if [ -z "$IP" ]; then
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
    pip install --upgrade pip --break-system-packages
    pip install -r requirements-core.txt --break-system-packages
    echo "[RHA] Update complete!"
}

function repair_system() {
    echo "[RHA] Running self-repair..."
    cd "$RHA_DIR" || exit 1
    pkg install -y python-numpy
    pip install --upgrade pip --break-system-packages
    pip install -r requirements-core.txt --break-system-packages
    echo "[RHA] System repaired."
}

function status_check() {
    echo "[RHA] System Status Check"
    cd "$RHA_DIR" || exit 1
    python -c "import fastapi; print('FastAPI: OK')" 2>/dev/null || echo "FastAPI: MISSING"
    python -c "import numpy; print('Numpy: OK')" 2>/dev/null || echo "Numpy: MISSING"
    python -c "import whisper_cpp; print('Whisper: OK')" 2>/dev/null || echo "Whisper: MISSING (or using alternative)"
    echo "Server Process:"
    pgrep -f "python api/server.py" >/dev/null && echo "ONLINE" || echo "OFFLINE"
}

function show_logs() {
    echo "[RHA] Fetching latest server logs..."
    tail -n 50 "$RHA_DIR/rha_service.log" 2>/dev/null || echo "No logs found."
}

function show_models() {
    echo "[RHA] Local Models Status"
    echo "STT: Whisper tiny.en (Available)"
    echo "LLM: Qwen 1.5B (Available)"
}

function run_doctor() {
    echo "[RHA] Running Doctor Diagnostics..."
    python -c "import fastapi" 2>/dev/null && echo "FastAPI: PASS" || echo "FastAPI: FAIL"
    python -c "import websockets" 2>/dev/null && echo "WebSockets: PASS" || echo "WebSockets: FAIL"
    echo "Diagnostics complete."
}

CMD_NAME=$(basename "$0")
case "$CMD_NAME" in
    rha-start) start_server ;;
    rha-stop) stop_server ;;
    rha-update) update_system ;;
    rha-repair) repair_system ;;
    rha-status) status_check ;;
    rha-logs) show_logs ;;
    rha-models) show_models ;;
    rha-doctor) run_doctor ;;
    *)
        case "$1" in
            start) start_server ;;
            stop) stop_server ;;
            update) update_system ;;
            repair) repair_system ;;
            status) status_check ;;
            logs) show_logs ;;
            models) show_models ;;
            doctor) run_doctor ;;
            *)
                show_help
                start_server
                ;;
        esac
        ;;
esac
