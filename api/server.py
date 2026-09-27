"""RHA local API server.

The HTTP server is deliberately usable without optional AI wheels.  Termux can
start it immediately, while `/self-test` reports which optional backends are
available instead of silently pretending to process audio.
"""

import asyncio
import os
import sys
from typing import Any

from fastapi import FastAPI, File, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
import uvicorn

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
os.chdir(PROJECT_ROOT)

app = FastAPI(title="RHA Voice Engine API", version="3.1.0")
stt = lang = intent = llm = memory = None
load_error: str | None = None

try:
    from engine.stt.whisper_engine import WhisperEngine
    stt = WhisperEngine(download_if_missing=False)
except Exception as exc:
    load_error = f"STT: {exc}"
    print(f"[Server] STT unavailable: {exc}")
try:
    from engine.language.router import LanguageRouter
    lang = LanguageRouter()
except Exception as exc:
    load_error = f"{load_error or ''} Language: {exc}".strip()
try:
    from engine.intent.router import IntentRouter
    intent = IntentRouter()
except Exception as exc:
    load_error = f"{load_error or ''} Intent: {exc}".strip()
try:
    from engine.llm.llama_engine import LlamaEngine
    llm = LlamaEngine(download_if_missing=False)
except Exception as exc:
    load_error = f"{load_error or ''} LLM: {exc}".strip()
try:
    from engine.memory.manager import MemoryManager
    memory = MemoryManager()
except Exception as exc:
    load_error = f"{load_error or ''} Memory: {exc}".strip()


def backend_status() -> dict[str, Any]:
    return {
        "stt": "ready" if stt and getattr(stt, "model", None) else "missing",
        "llm": "ready" if llm and getattr(llm, "model", None) else "missing",
        "intent": "ready" if intent else "missing",
        "memory": "ready" if memory else "missing",
        "error": load_error,
    }


@app.get("/")
def read_root():
    return {"status": "online", "service": "RHA Local Voice Engine", "endpoints": ["/health", "/self-test", "/api/models", "/ws/voice"]}


@app.get("/health")
def read_health():
    status = backend_status()
    return {"status": "pass", "server": "online", "backends": status}


@app.get("/self-test")
def self_test():
    status = backend_status()
    ai_ready = status["stt"] == "ready" and status["llm"] == "ready"
    return {"status": "pass" if ai_ready else "degraded", "checks": status}


@app.get("/api/models")
def get_models():
    status = backend_status()
    return {
        "stt": {"name": "Whisper multilingual", "status": status["stt"]},
        "llm": {"name": "Qwen 1.8B GGUF", "status": status["llm"]},
        "tts": {"name": "Termux/Android native TTS", "status": "client-side"},
    }


@app.post("/api/v1/voice")
async def process_voice(audio: UploadFile = File(...)):
    data = await audio.read()
    if not stt or not getattr(stt, "model", None):
        return JSONResponse(status_code=503, content={"status": "unavailable", "message": "Whisper backend is not installed or model is missing. See /self-test."})
    text = stt.transcribe_audio(data)
    return {"status": "success", "text": text}


@app.websocket("/ws/voice")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_bytes()
            await websocket.send_json({"type": "state", "value": "PROCESSING"})
            if not stt or not getattr(stt, "model", None) or not intent:
                await websocket.send_json({"type": "error", "message": "AI backend unavailable. Run rha doctor and install a model/backend."})
                await websocket.send_json({"type": "state", "value": "IDLE"})
                continue

            text = stt.transcribe_audio(data)
            if not text:
                await websocket.send_json({"type": "error", "message": "No speech detected."})
                await websocket.send_json({"type": "state", "value": "IDLE"})
                continue
            await websocket.send_json({"type": "transcription", "text": text})

            language, _, normalized = lang.detect_and_normalize(text)
            action, params, _ = intent.route_intent(normalized, language)
            if action == "OPEN_APP":
                await websocket.send_json({"type": "command", "action": action, "package": params.get("app", "")})
            elif action == "WEB_SEARCH":
                await websocket.send_json({"type": "command", "action": action, "query": params.get("query", normalized)})
            elif llm and getattr(llm, "model", None):
                await websocket.send_json({"type": "state", "value": "THINKING"})
                context = memory.retrieve_relevant_context(normalized) if memory else ""
                full_reply = ""
                buffer = ""
                for token in llm.generate_stream(f"{context}\nUser: {normalized}" if context else normalized):
                    full_reply += token
                    buffer += token
                    await websocket.send_json({"type": "llm_token", "text": token})
                    if any(mark in token for mark in [".", "?", "!", "\n", "۔"]):
                        await websocket.send_json({"type": "tts", "text": buffer.strip()})
                        buffer = ""
                if buffer.strip():
                    await websocket.send_json({"type": "tts", "text": buffer.strip()})
                if memory:
                    memory.save_interaction(normalized, full_reply)
            else:
                await websocket.send_json({"type": "llm_token", "text": "LLM backend is not installed."})
            await websocket.send_json({"type": "state", "value": "IDLE"})
    except WebSocketDisconnect:
        print("[Server] Client disconnected")
    except Exception as exc:
        print(f"[Server] WebSocket error: {exc}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("RHA_PORT", "8000")))
