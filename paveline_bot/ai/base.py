from abc import ABC, abstractmethod
from typing import Optional


class AIProvider(ABC):
    """Abstract interface every AI provider adapter must implement."""

    @abstractmethod
    async def generate(self, prompt: str, system: Optional[str] = None) -> str:
        """Return the generated text. Raise on failure."""
        raise NotImplementedError


class FallbackProvider:
    """Local template generator used when every AI provider fails."""

    def __init__(self, generate_fn):
        self._generate_fn = generate_fn

    async def generate(self, prompt: str, system: Optional[str] = None) -> str:
        return self._generate_fn()
