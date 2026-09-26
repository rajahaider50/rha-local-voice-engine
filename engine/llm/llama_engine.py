from abc import ABC, abstractmethod
from typing import Iterator

class LLMInterface(ABC):
    @abstractmethod
    def generate_stream(self, prompt: str) -> Iterator[str]:
        """
        Takes a prompt and yields tokens as they are generated.
        """
        pass

class LlamaEngine(LLMInterface):
    def __init__(self, model_path: str):
        self.model_path = model_path
        # Initialize llama.cpp here

    def generate_stream(self, prompt: str) -> Iterator[str]:
        # Placeholder for streaming generation
        yield "Placeholder "
        yield "response."
