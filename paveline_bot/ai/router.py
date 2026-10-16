import asyncio
import logging
import time
from typing import List, Optional

from .. import config
from ..core.fallback_templates import generate_fallback_wish
from .base import AIProvider, FallbackProvider
from .gemini import GeminiProvider
from .groq import GroqProvider
from .ollama import OllamaProvider
from .openrouter import OpenRouterProvider
from .rate_limiter import RateLimiter

logger = logging.getLogger(__name__)

PROVIDER_ORDER = ["gemini", "groq", "openrouter", "ollama", "fallback"]


def _build_provider(key: str) -> AIProvider:
    if key == "fallback":
        return FallbackProvider(lambda: "Thinking of you on your special day!")
    if key == "gemini":
        return GeminiProvider()
    if key == "groq":
        return GroqProvider()
    if key == "openrouter":
        return OpenRouterProvider()
    if key == "ollama":
        return OllamaProvider()
    raise ValueError(f"Unknown provider: {key}")


def build_fallback_chain() -> List[AIProvider]:
    order = [config.AI_PROVIDER] + [p for p in PROVIDER_ORDER if p != config.AI_PROVIDER]
    providers: List[AIProvider] = []
    for key in order:
        try:
            providers.append(_build_provider(key))
        except Exception as e:
            logger.warning(f"Skipping provider {key}: {e}")
    providers.append(_build_provider("fallback"))
    return providers


class AIRouter:
    def __init__(self):
        self.providers = build_fallback_chain()
        self.rate_limiter = RateLimiter(min_interval=1.0)

    async def generate(self, prompt: str, system: Optional[str] = None) -> str:
        last_error: Optional[Exception] = None
        for provider in self.providers:
            if isinstance(provider, FallbackProvider):
                # Local fallback — always succeeds
                return await provider.generate(prompt, system)
            try:
                await self.rate_limiter.acquire()
                return await provider.generate(prompt, system)
            except Exception as e:
                last_error = e
                logger.warning(f"AI provider failed: {e}; trying next fallback")
                await asyncio.sleep(2)  # backoff before next provider
        raise last_error or Exception("All AI providers failed")

    async def generate_with_fallback(self, prompt: str, system: Optional[str] = None) -> str:
        """Returns generated text; on total failure returns a local fallback wish."""
        try:
            return await self.generate(prompt, system)
        except Exception as e:
            logger.error(f"All AI providers failed, using local fallback: {e}")
            fallback = generate_fallback_wish(name="", relationship="friend", language="en", style="heartfelt")
            return fallback
