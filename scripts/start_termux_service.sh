#!/data/data/com.termux/files/usr/bin/bash
set -Eeuo pipefail
cd "$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
command -v termux-wake-lock >/dev/null 2>&1 && termux-wake-lock || true
exec scripts/rha_cmd.sh start
