import os
import re
from typing import Iterator

class TTSInterface:
    def synthesize(self, text: str) -> Iterator[bytes]:
        """Yields raw audio chunks for playback."""
        pass

class TTSRouter:
    def __init__(self, config_path: str = "config/models.yaml"):
        """
        Initializes the TTS Router (Phases 11, 12, 13).
        Handles English (Kokoro) and Urdu routing, as well as text chunking for streaming.
        """
        print("[TTS] Initializing TTS Router...")
        self._check_termux()

    def _check_termux(self):
        try:
            import subprocess
            subprocess.run(["termux-info"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.is_termux = True
        except FileNotFoundError:
            self.is_termux = False

    def chunk_text(self, text_stream: Iterator[str]) -> Iterator[str]:
        """
        Phase 13: Streaming TTS Chunking.
        Takes a stream of tokens from the LLM and chunks them into sentences
        so TTS can begin processing before the full response is generated.
        """
        buffer = ""
        # Match punctuation that signifies a good pause for TTS
        delimiters = re.compile(r'([.?!,۔،\n])')
        
        for token in text_stream:
            buffer += token
            # If we find a sentence boundary, yield the chunk
            if delimiters.search(buffer):
                parts = delimiters.split(buffer, maxsplit=1)
                chunk = parts[0] + parts[1] # text + punctuation
                if chunk.strip():
                    yield chunk.strip()
                buffer = parts[2] if len(parts) > 2 else ""
                
        if buffer.strip():
            yield buffer.strip()

    def play_audio(self, text: str, language: str):
        """
        Synthesizes and immediately plays the audio.
        In a production Termux environment, we fallback to termux-tts-speak 
        until the Kokoro/Urdu ONNX models are compiled for the specific device.
        """
        if not text:
            return
            
        print(f"🔊 [TTS Speaking] {text}")
        
        if self.is_termux:
            import subprocess
            # Route to appropriate language engine on Android
            if language in ["urdu", "mixed_urdu_english"]:
                # Attempt to use Android's Urdu TTS if available
                subprocess.run(["termux-tts-speak", "-l", "ur", text])
            else:
                subprocess.run(["termux-tts-speak", "-l", "en", text])
        else:
            # Desktop fallback or Kokoro ONNX placeholder
            # Here we would load Kokoro ONNX and stream to PyAudio output
            pass
