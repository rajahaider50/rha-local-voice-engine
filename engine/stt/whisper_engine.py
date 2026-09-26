from abc import ABC, abstractmethod
from typing import Iterator, Optional

class STTInterface(ABC):
    @abstractmethod
    def process_audio_stream(self, audio_chunk: bytes) -> Iterator[str]:
        """
        Takes raw audio bytes and yields partial/final transcriptions.
        """
        pass

class WhisperEngine(STTInterface):
    def __init__(self, model_path: str):
        self.model_path = model_path

    def process_audio_stream(self, audio_chunk: bytes) -> Iterator[str]:
        # Placeholder for whisper processing
        yield "partial text"
