from abc import ABC, abstractmethod
from typing import Iterator

class TTSInterface(ABC):
    @abstractmethod
    def synthesize_chunk(self, text_chunk: str) -> Iterator[bytes]:
        """
        Converts a chunk of text into a stream of audio bytes.
        """
        pass

class TTSRouter:
    def __init__(self, config: dict):
        self.config = config
        # Initialize engines based on config
        self.engines = {}

    def route_and_synthesize(self, text_chunk: str, language: str) -> Iterator[bytes]:
        """
        Routes the text to the appropriate TTS engine based on language.
        """
        # Placeholder routing
        yield b""
