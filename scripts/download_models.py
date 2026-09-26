#!/usr/bin/env python3
import os
import urllib.request

MODELS = {
    "stt": {
        "url": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.bin",
        "path": "models/stt/ggml-base.bin"
    },
    "llm": {
        "url": "https://huggingface.co/Qwen/Qwen1.5-1.8B-Chat-GGUF/resolve/main/qwen1_5-1_8b-chat-q4_k_m.gguf",
        "path": "models/llm/qwen-1_5b-chat-q4_k_m.gguf"
    }
}

def download_model(name: str, info: dict):
    path = info["path"]
    url = info["url"]
    
    if os.path.exists(path):
        print(f"✅ {name} already exists at {path}")
        return
        
    print(f"⬇️ Downloading {name} to {path}...")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    try:
        urllib.request.urlretrieve(url, path)
        print(f"✅ {name} downloaded successfully!")
    except Exception as e:
        print(f"❌ Failed to download {name}: {e}")

def main():
    print("=======================================")
    print(" RHA Model Downloader                  ")
    print("=======================================")
    print("This script downloads the required offline AI models.")
    
    for name, info in MODELS.items():
        download_model(name, info)
        
    print("\nAll model checks complete.")

if __name__ == "__main__":
    main()
