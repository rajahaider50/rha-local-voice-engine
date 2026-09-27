# Project Status

- **Version:** 3.1.0-dev
- **Core server:** Ready for local/Termux startup
- **Termux installer:** Ready — one command, no virtualenv, repeatable updates
- **Android client:** Implemented; requires physical-device validation
- **Optional AI:** Whisper/llama.cpp/openWakeWord are not guaranteed by core install and are reported through `/self-test`

## Immediate commands

```bash
curl -fsSL https://raw.githubusercontent.com/rajahaider50/rha-local-voice-engine/main/termux_oneliner.sh | bash
rha start
rha doctor
```

## Verification status

- Python compilation: checked locally after changes
- Intent smoke path: checked (`youtube kholo` -> `OPEN_APP`)
- HTTP/WebSocket flow: requires installed core packages and a running server
- Real Android microphone and native model performance: pending physical device test
