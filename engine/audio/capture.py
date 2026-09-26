import pyaudio
from typing import Iterator

class AudioCapture:
    def __init__(self, sample_rate: int = 16000, chunk_size: int = 512, channels: int = 1):
        """
        Initializes the PyAudio capture interface.
        16kHz, Mono, 16-bit PCM is standard for STT/VAD models.
        """
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.channels = channels
        self.is_capturing = False
        self.pa = pyaudio.PyAudio()
        self.stream = None

    def start_stream(self) -> Iterator[bytes]:
        """
        Yields raw PCM audio bytes from the default microphone.
        """
        self.is_capturing = True
        print(f"[AudioCapture] Starting microphone stream ({self.sample_rate}Hz, {self.channels} channel(s))...")
        
        try:
            self.stream = self.pa.open(
                format=pyaudio.paInt16,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            
            while self.is_capturing:
                try:
                    # Capture a chunk of audio
                    # exception_on_overflow=False prevents crashes if processing is too slow
                    data = self.stream.read(self.chunk_size, exception_on_overflow=False)
                    yield data
                except Exception as e:
                    print(f"[AudioCapture] Error reading audio chunk: {e}")
                    break
        except Exception as e:
            print(f"[AudioCapture] Failed to open audio stream: {e}")
            print("Make sure your microphone is connected and permissions are granted.")
        finally:
            self.stop_stream()

    def stop_stream(self):
        """Stops the current audio stream."""
        if self.is_capturing:
            self.is_capturing = False
            print("[AudioCapture] Stopped microphone stream.")
            if self.stream and self.stream.is_active():
                self.stream.stop_stream()
                self.stream.close()
            self.stream = None
            
    def terminate(self):
        """Closes PyAudio entirely. Call this when shutting down the application."""
        self.stop_stream()
        self.pa.terminate()
