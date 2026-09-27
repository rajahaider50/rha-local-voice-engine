#!/data/data/com.termux/files/usr/bin/bash
set -Eeuo pipefail
cd "$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
scripts/rha_cmd.sh stop
command -v termux-wake-unlock >/dev/null 2>&1 && termux-wake-unlock || true
