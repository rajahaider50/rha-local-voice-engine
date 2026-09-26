import os
from typing import Iterator

class LLMInterface:
    def generate_stream(self, prompt: str) -> Iterator[str]:
        pass

class LlamaEngine(LLMInterface):
    def __init__(self, model_path: str = "models/llm/qwen-1_5b-chat-q4_k_m.gguf", 
                 n_ctx: int = 2048, download_if_missing: bool = True):
        """
        Initializes the llama.cpp engine.
        Optimized for streaming responses on CPU/mobile.
        """
        self.model_path = model_path
        self.n_ctx = n_ctx
        self.model = None
        
        if not os.path.exists(self.model_path):
            if download_if_missing:
                self._download_model()
            else:
                print(f"[LLM] Model not found at {self.model_path}. Please download it.")
                
        self._load_model()

    def _download_model(self):
        print(f"[LLM] Model not found locally. Downloading Qwen 1.5B (Q4) to {self.model_path}...")
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        # Direct URL to the Qwen 1.5B Q4_K_M GGUF model on HuggingFace
        url = "https://huggingface.co/Qwen/Qwen1.5-1.8B-Chat-GGUF/resolve/main/qwen1_5-1_8b-chat-q4_k_m.gguf"
        import urllib.request
        try:
            urllib.request.urlretrieve(url, self.model_path)
            print("[LLM] Download complete.")
        except Exception as e:
            print(f"[LLM] Error downloading model: {e}")

    def _load_model(self):
        print("[LLM] Loading Llama.cpp model...")
        try:
            from llama_cpp import Llama
            # n_threads=4 is optimal for quad-core ARM devices
            self.model = Llama(
                model_path=self.model_path, 
                n_ctx=self.n_ctx,
                n_threads=4,
                verbose=False
            )
            print("[LLM] Model loaded successfully.")
        except ImportError:
            print("[LLM] llama-cpp-python not installed. Run: pip install llama-cpp-python")
        except Exception as e:
            print(f"[LLM] Error loading model: {e}")

    def generate_stream(self, prompt: str) -> Iterator[str]:
        """
        Streams tokens one by one as they are generated.
        """
        if self.model is None:
            yield "LLM is not loaded."
            return
            
        system_prompt = (
            "You are RHA, a fast, offline AI voice assistant. "
            "Keep answers extremely concise, natural, and helpful. "
            "Respond in the language the user speaks (English, Urdu, or Roman Urdu). "
            "Do not use emojis."
        )
        
        full_prompt = f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
        
        try:
            # Stream the response
            stream = self.model(
                full_prompt,
                max_tokens=256,
                stop=["<|im_end|>"],
                stream=True
            )
            
            for output in stream:
                token = output['choices'][0]['text']
                yield token
        except Exception as e:
            print(f"[LLM] Error generating text: {e}")
            yield " Sorry, I encountered an error."
