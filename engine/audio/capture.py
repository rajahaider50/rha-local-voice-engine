from typing import Iterator

class AudioCapture:
    def __init__(self, sample_rate: int = 16000, chunk_size: int = 512):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.is_capturing = False

    def start_stream(self) -> Iterator[bytes]:
        """
        Yields raw PCM audio bytes.
        """
        self.is_capturing = True
        print("[AudioCapture] Starting microphone stream...")
        # Placeholder yielding empty chunks
        while self.is_capturing:
            yield b"\x00" * self.chunk_size

    def stop_stream(self):
        self.is_capturing = False
        print("[AudioCapture] Stopped microphone stream.")
