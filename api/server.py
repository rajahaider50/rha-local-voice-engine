import sys
import os
import io
import wave
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
import uvicorn
import json
import asyncio

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# We will import models dynamically to prevent startup crashes if dependencies are missing
try:
    from engine.stt.whisper_engine import WhisperEngine
    from engine.language.router import LanguageRouter
    from engine.intent.router import IntentRouter
    from engine.llm.llama_engine import LlamaEngine
    from engine.memory.manager import MemoryManager
    MODELS_IMPORT_SUCCESS = True
except Exception as e:
    print(f"[Server Warning] Could not import AI models (missing dependencies like numpy): {e}")
    MODELS_IMPORT_SUCCESS = False

app = FastAPI(title="RHA Voice Engine API")

print("[Server] Loading AI Models... (This might take a moment)")
try:
    if MODELS_IMPORT_SUCCESS:
        stt = WhisperEngine()
        lang = LanguageRouter()
        intent = IntentRouter()
        llm = LlamaEngine()
        memory = MemoryManager()
        print("[Server] All models loaded. Server Ready!")
    else:
        raise Exception("Model modules were not imported.")
except Exception as e:
    print(f"[Server Warning] Failed to load some AI models natively: {e}")
    print("[Server] Server is running in MOCK mode until dependencies are fixed.")
    stt, lang, intent, llm, memory = None, None, None, None, None

@app.get("/")
def read_root():
    return {"status": "online", "message": "RHA Voice Server is actively running!", "endpoints": ["/ws/voice", "/health", "/api/models"]}

@app.get("/health")
def read_health():
    return {"status": "pass", "version": "2.1-Alpha", "engine": "RHA Local Voice Assistant"}

@app.get("/api/models")
def get_models():
    return {
        "stt": {"name": "Whisper tiny.en", "status": "installed" if stt else "missing", "size": "39MB"},
        "llm": {"name": "Qwen 1.5B", "status": "installed" if llm else "missing", "size": "890MB"},
        "tts": {"name": "Kokoro", "status": "missing", "size": "unknown"}
    }

@app.post("/api/v1/voice")
async def process_voice(audio: UploadFile = File(...)):
    return {"status": "success", "reply": "HTTP endpoint deprecated. Please use WebSocket."}

@app.websocket("/ws/voice")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_bytes()
            await websocket.send_json({"type": "state", "value": "PROCESSING"})
            
            if stt and intent:
                # 2. Speech to Text
                text = stt.transcribe_audio(data)
                if not text:
                    await websocket.send_json({"type": "error", "message": "No speech detected."})
                    await websocket.send_json({"type": "state", "value": "IDLE"})
                    continue
                    
                await websocket.send_json({"type": "transcription", "text": text})
                
                # 3. Intent Routing
                lang_detected, conf, norm = lang.detect_and_normalize(text)
                action, params, i_conf = intent.route_intent(norm, lang_detected)
                
                if action == "OPEN_APP":
                    await websocket.send_json({"type": "state", "value": "EXECUTING"})
                    await websocket.send_json({"type": "command", "action": "OPEN_APP", "package": params.get("app", "")})
                elif action == "WEB_SEARCH":
                    await websocket.send_json({"type": "state", "value": "EXECUTING"})
                    await websocket.send_json({"type": "command", "action": "WEB_SEARCH", "query": params.get("query", "")})
                else:
                    await websocket.send_json({"type": "state", "value": "THINKING"})
                    # Conversational LLM streaming
                    if llm:
                        context = memory.retrieve_relevant_context(norm) if memory else ""
                        prompt = f"{context}\nUser: {norm}" if context else norm
                        
                        full_reply = ""
                        sentence_buffer = ""
                        for token in llm.generate_stream(prompt):
                            full_reply += token
                            sentence_buffer += token
                            # Stream partial text back to Android
                            await websocket.send_json({"type": "llm_token", "text": token})
                            
                            # Simple sentence chunking for TTS
                            if any(punct in token for punct in [".", "?", "!", "\n", "۔"]):
                                if sentence_buffer.strip():
                                    await websocket.send_json({"type": "tts", "text": sentence_buffer.strip()})
                                sentence_buffer = ""
                        
                        if sentence_buffer.strip():
                            await websocket.send_json({"type": "tts", "text": sentence_buffer.strip()})
                            
                        # Save memory
                        if memory:
                            memory.save_interaction(norm, full_reply)
                    else:
                        await websocket.send_json({"type": "llm_token", "text": "LLM module offline."})
            else:
                # Fallback MOCK if AI models failed to load due to missing dependencies
                await asyncio.sleep(0.5)
                await websocket.send_json({"type": "transcription", "text": "Mock: Opening YouTube"})
                await websocket.send_json({"type": "state", "value": "EXECUTING"})
                await websocket.send_json({"type": "command", "action": "OPEN_APP", "package": "com.google.android.youtube"})
                
            await websocket.send_json({"type": "state", "value": "IDLE"})
            
    except WebSocketDisconnect:
        print("[Server] Client disconnected")
    except Exception as e:
        print(f"[Error] WebSocket error: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
