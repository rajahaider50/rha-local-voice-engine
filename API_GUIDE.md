# RHA Voice Engine API and Android connection

RHA کا production shape local client-server ہے:

1. Termux میں Python FastAPI server چلتا ہے۔
2. Android app `AudioRecord` سے 16 kHz mono PCM chunks WebSocket پر بھیجتی ہے۔
3. Server available ہونے پر Whisper، intent router اور local LLM سے events واپس بھیجتا ہے۔
4. Android native `TextToSpeech` جواب پڑھتا ہے۔

## Start server

### Termux

```bash
rha start
curl http://127.0.0.1:8000/health
```

### Linux

```bash
bash scripts/install.sh
source venv/bin/activate
python -m uvicorn api.server:app --host 0.0.0.0 --port 8000
```

## Endpoints

- `GET /health` — server اور backend status
- `GET /self-test` — diagnostic response
- `GET /api/models` — STT/LLM/TTS availability
- `POST /api/v1/voice` — multipart `audio`; Whisper available نہ ہو تو HTTP 503
- `WS /ws/voice` — binary PCM chunks؛ events: `state`, `transcription`, `command`, `llm_token`, `tts`, `error`

Server AI files نہ ملنے پر fake “YouTube opened” response نہیں دیتا؛ واضح diagnostic error واپس کرتا ہے۔

## Android settings

App میں Server screen پر `127.0.0.1` اور `8000` رکھیں اگر Python اسی فون کے Termux میں ہے۔ اگر Python laptop پر ہے تو laptop کا trusted Wi-Fi IP اور port دیں۔ Android app کو microphone permission دیں؛ Accessibility service صرف اس وقت enable کریں جب واقعی UI automation درکار ہو۔

LAN استعمال trusted network تک محدود رکھیں، کیونکہ current API authentication نہیں دیتی۔
