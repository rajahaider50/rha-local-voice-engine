# RHA Local Voice Engine

RHA ایک privacy-first local voice assistant project ہے جو Urdu، Roman Urdu اور English کے لیے modular Python server اور Android client فراہم کرتا ہے۔ Core API cloud AI کے بغیر چل سکتی ہے؛ optional STT/LLM/wake-word backends device کے حساب سے فعال کیے جاتے ہیں۔

## Features

- FastAPI server with health, self-test, model status and WebSocket endpoints
- Deterministic multilingual intent routing
- Local SQLite conversation memory
- Android AudioRecord + WebSocket client and native TTS
- Termux global command suite: `rha start|stop|status|doctor|repair`
- Optional Whisper.cpp, llama.cpp, Silero VAD and openWakeWord integrations

## Termux quick start

```bash
curl -fsSL https://raw.githubusercontent.com/rajahaider50/rha-local-voice-engine/main/termux_oneliner.sh | bash
rha start
rha doctor
```

تفصیلی ہدایات: [`TERMUX_GUIDE.md`](TERMUX_GUIDE.md)۔ Termux میں native `python-numpy` کی وجہ سے virtualenv intentionally استعمال نہیں کیا جاتا۔

## Standard Linux

```bash
bash scripts/install.sh
source venv/bin/activate
python -m uvicorn api.server:app --host 0.0.0.0 --port 8000
```

## API

- `GET /` — service summary
- `GET /health` — live backend status
- `GET /self-test` — diagnostic checks
- `GET /api/models` — local model status
- `WS /ws/voice` — PCM chunks in, transcription/command/LLM/TTS events out
- `POST /api/v1/voice` — one-shot transcription when Whisper is available

See [`API_GUIDE.md`](API_GUIDE.md) for Android/server connection details.

## Development checks

```bash
python -m compileall -q api engine
python -m pytest -q
```

AI model binaries are downloaded at runtime and are not committed to this repository. See [`MODEL_LICENSE.md`](MODEL_LICENSE.md) before redistributing any model.
