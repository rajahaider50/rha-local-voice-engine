"""Optional Silero VAD integration with a deterministic fallback."""

import warnings
warnings.filterwarnings("ignore")

try:
    import numpy as np
except ImportError:
    np = None


class VoiceActivityDetector:
    def __init__(self, sample_rate: int = 16000, threshold: float = 0.5):
        self.sample_rate = sample_rate
        self.threshold = threshold
        self.model = None
        self._load_model()

    def _load_model(self):
        try:
            import torch
            self.model, utils = torch.hub.load(
                repo_or_dir="snakers4/silero-vad", model="silero_vad",
                force_reload=False, onnx=False,
            )
            self.model.eval()
            print("[VAD] Silero VAD loaded successfully.")
        except Exception as exc:
            print(f"[VAD] Optional model unavailable; using energy fallback: {exc}")

    def is_speech(self, audio_chunk: bytes) -> bool:
        if not audio_chunk or np is None:
            return False
        try:
            audio_data = np.frombuffer(audio_chunk, dtype=np.int16)
            if not len(audio_data):
                return False
            if self.model is None:
                # A small RMS gate keeps the audio loop useful without torch.
                return float(np.sqrt(np.mean(audio_data.astype(np.float32) ** 2))) > 500.0
            import torch
            tensor_data = torch.from_numpy(audio_data.astype(np.float32) / 32768.0)
            return float(self.model(tensor_data, self.sample_rate).item()) >= self.threshold
        except Exception as exc:
            print(f"[VAD] Error processing chunk: {exc}")
            return False
