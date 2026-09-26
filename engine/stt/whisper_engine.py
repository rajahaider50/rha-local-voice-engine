import os
import numpy as np
from typing import Iterator

class STTInterface:
    def transcribe_audio(self, audio_data: np.ndarray) -> str:
        pass

class WhisperEngine(STTInterface):
    def __init__(self, model_path: str = "models/stt/ggml-base.bin", download_if_missing: bool = True):
        """
        Initializes the Whisper.cpp STT engine.
        Using base model as a starting point for mobile compatibility.
        """
        self.model_path = model_path
        self.model = None
        
        if not os.path.exists(self.model_path):
            if download_if_missing:
                self._download_model()
            else:
                raise FileNotFoundError(f"Whisper model not found at {self.model_path}")
                
        self._load_model()

    def _download_model(self):
        print(f"[STT] Model not found locally. Downloading base model to {self.model_path}...")
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        # We download the standard ggml base model (multilingual to support Urdu)
        # Using a reliable HF mirror or direct whisper.cpp URL
        url = "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.bin"
        import urllib.request
        try:
            urllib.request.urlretrieve(url, self.model_path)
            print("[STT] Download complete.")
        except Exception as e:
            print(f"[STT] Error downloading model: {e}")

    def _load_model(self):
        print("[STT] Loading Whisper.cpp model into memory...")
        try:
            from whisper_cpp_python import Whisper
            # n_threads=4 is usually optimal for mobile ARM processors
            self.model = Whisper(model_path=self.model_path, n_threads=4)
            print("[STT] Whisper model loaded successfully.")
        except ImportError:
            print("[STT] whisper_cpp_python not installed.")
        except Exception as e:
            print(f"[STT] Error loading model: {e}")

    def transcribe_audio(self, audio_chunk: bytes) -> str:
        """
        Takes raw 16-bit PCM audio bytes, converts to float32, and transcribes.
        Returns the recognized text string.
        """
        if self.model is None:
            return ""
            
        try:
            # Whisper expects 16kHz float32 audio normalized between -1.0 and 1.0
            audio_data = np.frombuffer(audio_chunk, dtype=np.int16)
            audio_float32 = audio_data.astype(np.float32) / 32768.0
            
            # Run transcription without language forcing (auto-detect)
            # language='auto' allows detecting Urdu or English dynamically
            output = self.model.transcribe(audio_float32)
            
            # The output contains segments
            text = "".join([segment["text"] for segment in output["segments"]])
            return text.strip()
        except Exception as e:
            print(f"[STT] Transcription error: {e}")
            return ""
