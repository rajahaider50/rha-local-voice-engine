"""Audio capture with a native PyAudio backend and a test-safe fallback."""

try:
    import pyaudio
except ImportError:  # Optional on server-only Termux installs.
    pyaudio = None


class AudioCapture:
    def __init__(self, rate=16000, chunk=1024, channels=1, sample_rate=None, chunk_size=None):
        # Accept both the original names and the names used by test scripts.
        self.rate = sample_rate or rate
        self.chunk = chunk_size or chunk
        self.channels = channels
        self.stream = None
        self.pa = None

    def start_stream(self):
        if pyaudio is None:
            print("[AudioCapture] PyAudio not installed; yielding silence for diagnostics.")
            import time
            while True:
                time.sleep(self.chunk / self.rate)
                yield b"\x00" * (self.chunk * 2 * self.channels)
            return

        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk,
        )
        while True:
            yield self.stream.read(self.chunk, exception_on_overflow=False)

    def terminate(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        if self.pa:
            self.pa.terminate()
            self.pa = None
