#!/data/data/com.termux/files/usr/bin/bash
set -Eeuo pipefail
RHA_DIR="${RHA_DIR:-$HOME/rha-local-voice-engine}"
PID_FILE="$RHA_DIR/.rha-server.pid"

need_project() { [ -d "$RHA_DIR" ] || { echo "Project not found: $RHA_DIR. Run the installer first." >&2; exit 1; }; }
server_pid() { [ -s "$PID_FILE" ] && cat "$PID_FILE" || true; }

start_server() {
  need_project; cd "$RHA_DIR"
  if pid=$(server_pid) && [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then echo "RHA already running (PID $pid)"; return; fi
  python -c 'import fastapi, uvicorn' 2>/dev/null || { echo "Core packages missing. Run: rha repair" >&2; exit 1; }
  echo "RHA server: http://127.0.0.1:${RHA_PORT:-8000}"
  nohup python -m uvicorn api.server:app --host 0.0.0.0 --port "${RHA_PORT:-8000}" >"$RHA_DIR/rha_service.log" 2>&1 &
  echo $! > "$PID_FILE"
  sleep 1
  status_check
}

stop_server() {
  need_project
  if pid=$(server_pid) && [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then kill "$pid"; rm -f "$PID_FILE"; echo "RHA server stopped."; else echo "RHA server is not running."; fi
}

update_system() { need_project; cd "$RHA_DIR"; git pull --ff-only origin main; python -m pip install -r requirements-core.txt --break-system-packages || python -m pip install -r requirements-core.txt; }
repair_system() { need_project; command -v pkg >/dev/null && pkg install -y python-numpy || true; update_system; python -m compileall -q api engine; echo "RHA repair complete."; }
status_check() { need_project; echo "Project: $RHA_DIR"; python -c 'import fastapi; print("FastAPI: OK")' 2>/dev/null || echo "FastAPI: MISSING"; python -c 'import numpy; print("NumPy: OK")' 2>/dev/null || echo "NumPy: MISSING"; pid=$(server_pid); if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then echo "Server: ONLINE (PID $pid)"; else echo "Server: OFFLINE"; fi; }
show_logs() { need_project; tail -n 80 "$RHA_DIR/rha_service.log" 2>/dev/null || echo "No logs found."; }
show_models() { need_project; for f in models/stt/ggml-base.bin models/llm/qwen-1_5b-chat-q4_k_m.gguf; do [ -s "$RHA_DIR/$f" ] && echo "$f: present" || echo "$f: missing"; done; }
run_doctor() { need_project; cd "$RHA_DIR"; python -m compileall -q api engine && echo "Python syntax: PASS" || echo "Python syntax: FAIL"; python -c 'import fastapi, uvicorn, yaml; print("Core imports: PASS")' 2>/dev/null || echo "Core imports: FAIL"; curl -fsS "http://127.0.0.1:${RHA_PORT:-8000}/self-test" 2>/dev/null || echo "Server self-test: unavailable (start with rha start)"; }
show_help() { echo "Usage: rha {start|stop|status|update|repair|logs|models|doctor}"; }

cmd="${1:-status}"
case "$cmd" in start) start_server ;; stop) stop_server ;; update) update_system ;; repair) repair_system ;; status) status_check ;; logs) show_logs ;; models) show_models ;; doctor) run_doctor ;; *) show_help; exit 2 ;; esac
