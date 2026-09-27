#!/usr/bin/env bash
set -Eeuo pipefail
cd "$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
if [ -n "${PREFIX:-}" ]; then
  python -c 'import fastapi, uvicorn' 2>/dev/null || bash scripts/setup_termux.sh
else
  [ -x venv/bin/python ] || bash scripts/install.sh
  source venv/bin/activate
fi
args=(--host "${RHA_HOST:-0.0.0.0}" --port "${RHA_PORT:-8000}")
[ -z "${RHA_RELOAD:-}" ] || args+=(--reload)
exec python -m uvicorn api.server:app "${args[@]}"
