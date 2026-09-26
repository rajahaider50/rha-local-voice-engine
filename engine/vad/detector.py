import numpy as np
import torch
import warnings

# Suppress torchaudio warnings
warnings.filterwarnings("ignore")

class VoiceActivityDetector:
    def __init__(self, sample_rate: int = 16000, threshold: float = 0.5):
        """
        Initializes the Silero VAD model.
        """
        self.sample_rate = sample_rate
        self.threshold = threshold
        self.model = None
        self.get_speech_timestamps = None
        self._load_model()
        
    def _load_model(self):
        print("[VAD] Loading Silero VAD model...")
        try:
            # We use torch.hub to load the pre-trained Silero VAD model.
            # In a fully offline/production environment, we would save this model
            # locally to models/stt/silero_vad.onnx and load it via ONNX Runtime.
            # For this phase, we'll download it once via torch hub.
            self.model, utils = torch.hub.load(
                repo_or_dir='snakers4/silero-vad',
                model='silero_vad',
                force_reload=False,
                onnx=False
            )
            (self.get_speech_timestamps,
             self.save_audio,
             self.read_audio,
             self.VADIterator,
             self.collect_chunks) = utils
            
            self.model.eval()
            print("[VAD] Silero VAD loaded successfully.")
        except Exception as e:
            print(f"[VAD] Error loading Silero VAD: {e}")
            print("You may need an internet connection for the first run to download the model.")

    def is_speech(self, audio_chunk: bytes) -> bool:
        """
        Takes raw 16-bit PCM audio bytes and returns True if speech is detected.
        """
        if self.model is None:
            return False
            
        try:
            # Convert raw bytes to numpy array of 16-bit integers
            audio_data = np.frombuffer(audio_chunk, dtype=np.int16)
            
            # Convert to float32 tensor normalized between -1.0 and 1.0 (expected by Silero)
            audio_float32 = audio_data.astype(np.float32) / 32768.0
            tensor_data = torch.from_numpy(audio_float32)
            
            # Silero expects batches, but we process one chunk at a time.
            # Get speech probability
            speech_prob = self.model(tensor_data, self.sample_rate).item()
            
            return speech_prob >= self.threshold
        except Exception as e:
            print(f"[VAD] Error processing chunk: {e}")
            return False
