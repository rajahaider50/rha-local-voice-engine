"""Optional openWakeWord integration."""


class WakeWordDetector:
    def __init__(self, model_paths: list = None, threshold: float = 0.5):
        self.threshold = threshold
        self.model = None
        self._load_model(model_paths)

    def _load_model(self, model_paths):
        try:
            from openwakeword.model import Model
            names = model_paths or ["hey_jarvis"]
            self.model = Model(wakeword_models=names, inference_framework="onnx")
            print(f"[WakeWord] Loaded: {', '.join(names)}")
        except Exception as exc:
            print(f"[WakeWord] Optional model unavailable: {exc}")

    def process_chunk(self, audio_chunk: bytes) -> bool:
        if self.model is None:
            return False
        try:
            import numpy as np
            prediction = self.model.predict(np.frombuffer(audio_chunk, dtype=np.int16))
            if any(score >= self.threshold for score in prediction.values()):
                self.model.reset()
                return True
        except Exception as exc:
            print(f"[WakeWord] Error processing chunk: {exc}")
        return False
