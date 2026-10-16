import logging
from typing import Optional

import httpx

from .. import config
from .base import AIProvider

logger = logging.getLogger(__name__)


class OllamaProvider(AIProvider):
    def __init__(self):
        self.base_url = config.OLLAMA_BASE_URL
        self.model = config.OLLAMA_MODEL

    async def generate(self, prompt: str, system: Optional[str] = None) -> str:
        async with httpx.AsyncClient(timeout=60.0) as client:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "system": system or "",
                "stream": False,
            }
            resp = await client.post(f"{self.base_url}/api/generate", json=payload)
            if resp.status_code == 200:
                data = resp.json()
                text = data.get("response", "")
                if not text or not text.strip():
                    raise Exception("Empty response from Ollama")
                return text.strip()
            raise Exception(f"Ollama HTTP {resp.status_code}")
