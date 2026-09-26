import sys
import os
import io
import wave
from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.responses import JSONResponse
import uvicorn

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from engine.stt.whisper_engine import WhisperEngine
from engine.language.router import LanguageRouter
from engine.intent.router import IntentRouter
from engine.llm.llama_engine import LlamaEngine
from engine.memory.manager import MemoryManager

app = FastAPI(title="RHA Voice Engine API")

print("[Server] Loading AI Models... (This might take a moment)")
stt = WhisperEngine()
lang = LanguageRouter()
intent = IntentRouter()
llm = LlamaEngine()
memory = MemoryManager()
print("[Server] All models loaded. Server Ready!")

@app.get("/")
def read_root():
    return {"status": "online", "engine": "RHA Local Voice Assistant"}

@app.post("/api/v1/voice")
async def process_voice(audio: UploadFile = File(...)):
    """
    Receives raw audio from the Android App, runs STT, Intent, and LLM.
    Returns the AI's response text and command intent.
    """
    try:
        # 1. Read Audio Data
        audio_bytes = await audio.read()
        
        # 2. Speech to Text (Phase 5)
        text = stt.transcribe_audio(audio_bytes)
        if not text:
            return {"status": "error", "message": "No speech detected."}
            
        # 3. Language & Intent Routing (Phases 6 & 7)
        lang_detected, conf, norm = lang.detect_and_normalize(text)
        action, params, i_conf = intent.route_intent(norm, lang_detected)
        
        response_data = {
            "status": "success",
            "recognized_text": text,
            "normalized_text": norm,
            "language": lang_detected,
            "intent": action,
            "parameters": params,
            "reply": ""
        }
        
        # 4. LLM Response if Conversational (Phases 9 & 10)
        if action == "CONVERSATIONAL":
            context = memory.retrieve_relevant_context(norm)
            prompt = f"{context}\nUser: {norm}" if context else norm
            
            # Since we are returning a JSON response, we collect the stream
            # (In an advanced WebSockets setup, we'd stream this back)
            full_reply = ""
            for token in llm.generate_stream(prompt):
                full_reply += token
                
            response_data["reply"] = full_reply.strip()
            
        return response_data
        
    except Exception as e:
        print(f"[Error] API processing failed: {e}")
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
