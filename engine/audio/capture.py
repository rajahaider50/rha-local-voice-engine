try:
    import pyaudio
except ImportError:
    pyaudio = None

class AudioCapture:
    def __init__(self, rate=16000, chunk=1024):
        self.rate = rate
        self.chunk = chunk
        self.stream = None
        self.pa = None
        
    def start_stream(self):
        if pyaudio is None:
            print("[AudioCapture] PyAudio not installed. Expecting audio chunks from Native Android wrapper.")
            # In a real native integration, we'd yield chunks passed from Kotlin via a queue.
            # For now, yield empty chunks to prevent crash during testing.
            import time
            while True:
                time.sleep(self.chunk / self.rate)
                yield b'\x00' * (self.chunk * 2)

        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )
        
        while True:
            yield self.stream.read(self.chunk, exception_on_overflow=False)
            
    def terminate(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.pa:
            self.pa.terminate()
