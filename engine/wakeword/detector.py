import os
from openwakeword.model import Model

class WakeWordDetector:
    def __init__(self, model_paths: list = None, threshold: float = 0.5):
        """
        Initializes the openWakeWord model.
        Uses default pre-trained models (e.g., 'hey_jarvis' or 'alexa') unless custom paths are provided.
        For RHA, we will use a default model until a custom "Hey RHA" model is trained.
        """
        self.threshold = threshold
        self.model = None
        self._load_model(model_paths)
        
    def _load_model(self, model_paths):
        print("[WakeWord] Loading openWakeWord models...")
        try:
            # If no custom model is provided, load a lightweight default for testing
            if not model_paths:
                print("[WakeWord] No custom model provided. Using default 'hey_jarvis' for testing.")
                self.model = Model(wakeword_models=['hey_jarvis'], inference_framework='onnx')
            else:
                self.model = Model(wakeword_models=model_paths, inference_framework='onnx')
            print("[WakeWord] Models loaded successfully.")
        except Exception as e:
            print(f"[WakeWord] Error loading models: {e}")

    def process_chunk(self, audio_chunk: bytes) -> bool:
        """
        Takes raw 16-bit PCM audio bytes (16kHz).
        Returns True if the wake word is detected in the stream.
        """
        if self.model is None:
            return False
            
        try:
            import numpy as np
            # Convert to numpy array of 16-bit integers
            audio_data = np.frombuffer(audio_chunk, dtype=np.int16)
            
            # Predict
            prediction = self.model.predict(audio_data)
            
            # Check if any model crossed the threshold
            for mdl, score in prediction.items():
                if score >= self.threshold:
                    # Reset internal state after detection to prevent double-triggers
                    self.model.reset()
                    return True
            return False
        except Exception as e:
            print(f"[WakeWord] Error processing chunk: {e}")
            return False
