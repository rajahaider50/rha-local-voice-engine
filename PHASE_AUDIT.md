# Verified Project Audit — 2026-09-27

| Area | Status | Verification |
|---|---|---|
| Project structure | Complete | Python, Android, config, scripts and tests present |
| Termux installation | Complete | One canonical venv-free installer; native NumPy; smoke test |
| Core API | Complete | `/`, `/health`, `/self-test`, `/api/models`, WebSocket routes |
| Language/intent routing | Complete | English, Urdu and Roman Urdu routing; web-search intent |
| SQLite memory | Complete | Preferences, memories and conversation persistence |
| Android client | Implemented | AudioRecord, foreground service, WebSocket and native TTS |
| Optional AI backends | Device-dependent | Whisper/llama.cpp/openWakeWord require compatible mobile builds/models |
| Real-device verification | Pending | Requires physical Termux + Android APK test |
| LAN security | Limitation | No authentication; use localhost or trusted Wi-Fi only |

## Findings fixed in this pass

- Removed conflicting Termux virtualenv instructions and made `termux_oneliner.sh` canonical.
- Fixed missing `requirements.txt` reference in the Linux installer.
- Fixed `AudioCapture` constructor mismatch used by all audio test scripts.
- Made torch/openWakeWord optional imports so core server can start without AI wheels.
- Prevented API import from downloading large models automatically.
- Added `/self-test` and truthful unavailable-backend responses.
- Added missing `MemoryManager.save_interaction` and `WEB_SEARCH` query extraction.
- Replaced unsafe broad `pkill` service stop with PID-file management.

## Remaining work

Physical-device validation of microphone permissions, native AI wheels, Android foreground-service behavior, and model performance remains necessary before claiming end-to-end production readiness.
