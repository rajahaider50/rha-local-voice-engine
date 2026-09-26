from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(
    title="RHA Local Voice Engine API",
    description="Development API for testing the RHA engine components locally.",
    version="0.1.0"
)

class ChatRequest(BaseModel):
    text: str
    language: str = "auto"

class ChatResponse(BaseModel):
    response: str
    intent: str
    language_detected: str

@app.get("/")
def read_root():
    return {"status": "online", "system": "RHA Local Voice Engine"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "components": {"stt": "mock", "llm": "mock", "tts": "mock"}}

@app.post("/api/v1/test_intent", response_model=ChatResponse)
def test_intent_routing(request: ChatRequest):
    """
    Mock endpoint to test the language and intent router logic.
    """
    # In a real scenario, this would call engine.language.router and engine.intent.router
    # Here we mock it based on the skeleton we built.
    text_lower = request.text.lower()
    
    intent = "UNKNOWN"
    detected_lang = "english"
    
    if "kholo" in text_lower or "karo" in text_lower:
        detected_lang = "roman_urdu"
        if "youtube kholo" in text_lower:
            intent = "OPEN_APP"
    elif any(c in "ابپتٹثجچحخدڈذرڑزژسشصضطظعغفقکگلمنںوؤہہیئے" for c in text_lower):
        detected_lang = "urdu"
        intent = "CONVERSATIONAL"
    else:
        if "open" in text_lower:
            intent = "OPEN_APP"
        
    return ChatResponse(
        response=f"Processed test command: {request.text}",
        intent=intent,
        language_detected=detected_lang
    )

if __name__ == "__main__":
    uvicorn.run("api.server:app", host="0.0.0.0", port=8000, reload=True)
