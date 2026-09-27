#!/data/data/com.termux/files/usr/bin/bash
# RHA Local Voice Engine - one-command Termux installer
# Usage: curl -fsSL https://raw.githubusercontent.com/rajahaider50/rha-local-voice-engine/main/termux_oneliner.sh | bash
set -Eeuo pipefail

REPO_URL="${RHA_REPO_URL:-https://github.com/rajahaider50/rha-local-voice-engine.git}"
RHA_DIR="${RHA_DIR:-$HOME/rha-local-voice-engine}"

fail() { printf '\n[RHA] ERROR: %s\n' "$*" >&2; exit 1; }
command -v pkg >/dev/null 2>&1 || fail "یہ installer صرف Termux میں چلائیں۔"

printf '\n=== RHA Local Voice Engine — Termux setup ===\n'
termux-setup-storage >/dev/null 2>&1 || true
pkg update -y
pkg install -y git curl python clang cmake make pkg-config libffi openssl sqlite pulseaudio termux-api python-numpy

if [ -d "$RHA_DIR/.git" ]; then
  git -C "$RHA_DIR" fetch --depth=1 origin main
  git -C "$RHA_DIR" reset --hard origin/main
else
  rm -rf "$RHA_DIR"
  git clone --depth=1 "$REPO_URL" "$RHA_DIR"
fi
cd "$RHA_DIR"

# Termux uses native packages (especially numpy); do not create a venv.
pip_install() {
  python -m pip install --disable-pip-version-check --break-system-packages "$@" 2>/dev/null \
    || python -m pip install --disable-pip-version-check "$@"
}
pip_install -r requirements-core.txt

mkdir -p models/stt models/llm
if [ "${RHA_DOWNLOAD_MODELS:-1}" = "1" ] && [ ! -s models/stt/ggml-base.bin ]; then
  echo "[RHA] Downloading multilingual Whisper base model (~142 MB)..."
  curl -fL --retry 3 --continue-at - \
    -o models/stt/ggml-base.bin \
    https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.bin
fi

install -m 755 scripts/rha_cmd.sh "$PREFIX/bin/rha"
for command_name in start stop update repair status logs models doctor; do
  ln -sf "$PREFIX/bin/rha" "$PREFIX/bin/rha-$command_name"
done

python -m compileall -q api engine || fail "Python syntax check ناکام ہوئی۔"
python - <<'PY'
from engine.language.router import LanguageRouter
from engine.intent.router import IntentRouter
lang, _, text = LanguageRouter().detect_and_normalize('youtube kholo')
intent, params, _ = IntentRouter().route_intent(text, lang)
assert intent == 'OPEN_APP' and params.get('app') == 'youtube'
print('[RHA] Smoke test: PASS')
PY

cat <<EOF

[RHA] Installation complete.
  Project: $RHA_DIR
  Start:   rha start
  Status:  rha status
  Doctor:  rha doctor
  Stop:    rha stop

AI backends (llama.cpp/whisper-cpp) are optional native builds on Termux.
Set RHA_DOWNLOAD_MODELS=0 to skip model download and run the core server first.
EOF
