#!/usr/bin/env python3
import sys
import os

# Add the project root to the python path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from engine.language.router import LanguageRouter
from engine.intent.router import IntentRouter
from engine.llm.llama_engine import LlamaEngine
from engine.tools.android import AndroidTools

def main():
    print("=======================================")
    print(" RHA Full Text Pipeline Test           ")
    print(" (Phases 6, 7, 8, 9, 10)               ")
    print("=======================================")
    
    print("\n[Init] Initializing LLM... (This may download ~1.2GB if missing)")
    llm = LlamaEngine()
    lang_router = LanguageRouter()
    intent_router = IntentRouter()
    tools = AndroidTools()
    
    print("\nSystem Ready! Type a command or question (or 'exit' to quit).")
    
    while True:
        try:
            text = input("\nYou: ")
            if text.lower() in ['exit', 'quit']:
                break
            if not text.strip():
                continue
                
            # Phase 6: Language Detection & Normalization
            language, conf, normalized = lang_router.detect_and_normalize(text)
            print(f"[Language] {language} (conf: {conf}), Normalized: '{normalized}'")
            
            # Phase 7: Intent Routing
            intent, params, i_conf = intent_router.route_intent(normalized, language)
            print(f"[Intent] {intent} (conf: {i_conf}), Params: {params}")
            
            # Phase 8: Execution
            if intent == "OPEN_APP":
                app_name = params.get('app', 'unknown app')
                print(f"[Action] Triggering Android tool to open: {app_name}")
                tools.open_app(app_name)
                
            elif intent == "SET_VOLUME":
                print("[Action] Triggering Android tool to change volume")
                tools.set_volume("music", 50)
                
            elif intent == "CONVERSATIONAL":
                # Phase 9 & 10: LLM Streaming Fallback
                print(f"[LLM Response] ", end="", flush=True)
                for token in llm.generate_stream(normalized):
                    sys.stdout.write(token)
                    sys.stdout.flush()
                print() # Newline after stream
            
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
