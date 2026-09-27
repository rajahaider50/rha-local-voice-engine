#!/data/data/com.termux/files/usr/bin/bash
# Local entrypoint; the same installer can also be run remotely via termux_oneliner.sh.
set -Eeuo pipefail
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
exec bash "$SCRIPT_DIR/../termux_oneliner.sh" "$@"
