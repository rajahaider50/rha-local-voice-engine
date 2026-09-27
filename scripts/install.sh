#!/usr/bin/env bash
set -Eeuo pipefail
cd "$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
python3 -m venv venv
# Standard Linux keeps isolation; Termux uses termux_oneliner.sh and no venv.
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-core.txt
python -m compileall -q api engine
printf 'Setup complete. Start with: source venv/bin/activate && python -m uvicorn api.server:app\n'
