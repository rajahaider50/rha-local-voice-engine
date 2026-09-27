# RHA Local Voice Engine — Termux Setup

یہ setup **Termux (F-Droid)** اور الگ **Termux:API** app کے لیے ہے۔ Google Play والا پرانا Termux استعمال نہ کریں۔ microphone کے لیے Android permission بھی allow کریں۔

## One-command installation

Termux میں یہ ایک command چلائیں:

```bash
curl -fsSL https://raw.githubusercontent.com/rajahaider50/rha-local-voice-engine/main/termux_oneliner.sh | bash
```

Installer `pkg` dependencies، repository، core Python packages، native NumPy، Whisper base model، global `rha` command اور smoke test خود کرتا ہے۔ Termux میں virtualenv **نہیں** بنایا جاتا کیونکہ native `python-numpy` کے ساتھ venv اکثر binary compatibility توڑ دیتا ہے۔

اگر پہلے صرف server/core setup چاہیے:

```bash
RHA_DOWNLOAD_MODELS=0 curl -fsSL https://raw.githubusercontent.com/rajahaider50/rha-local-voice-engine/main/termux_oneliner.sh | bash
```

موجودہ clone کے اندر local setup کے لیے:

```bash
cd ~/rha-local-voice-engine && bash scripts/setup_termux.sh
```

## Commands

```bash
rha start     # background server on 0.0.0.0:8000
rha status    # dependencies and process status
rha doctor    # syntax/import/API self-test
rha models    # model files status
rha logs      # last server logs
rha stop      # stop only the recorded RHA process
rha update    # fast-forward source and refresh core packages
rha repair    # reinstall native NumPy/core packages
```

Health checks:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/self-test
```

## Optional AI backends

FastAPI server core intentionally starts even when mobile-native AI wheels are unavailable. `/self-test` reports `missing` backends instead of returning fake voice results. Whisper/llama.cpp/openWakeWord builds are device-specific and can be installed separately after checking Termux-compatible wheels/build flags. Model files are never bundled in Git.

## Troubleshooting

- `termux-* command not found`: install the separate **Termux:API** Android app, then run `pkg install termux-api`.
- `Permission denied`: run `termux-setup-storage` and allow microphone/storage permissions.
- Server does not start: run `rha doctor` and `rha logs`.
- Port conflict: run `RHA_PORT=8001 rha start`; configure the Android app to the same port.
- For a LAN client, use the phone's local IP and keep the server on a trusted Wi-Fi network; this API has no authentication layer yet.
