import logging
from typing import Optional

import httpx

from .. import config
from .base import AIProvider

logger = logging.getLogger(__name__)


class OpenRouterProvider(AIProvider):
    def __init__(self):
        self.api_key = config.OPENROUTER_API_KEY
        self.model = config.OPENROUTER_MODEL
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    async def generate(self, prompt: str, system: Optional[str] = None) -> str:
        if not self.api_key:
            raise Exception("OpenRouter API key not configured")
        async with httpx.AsyncClient(timeout=60.0) as client:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/paveline",
                "X-Title": "Paveline Bot",
            }
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            payload = {"model": self.model, "messages": messages}
            resp = await client.post(self.base_url, headers=headers, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                text = data["choices"][0]["message"]["content"]
                if not text or not text.strip():
                    raise Exception("Empty response from OpenRouter")
                return text.strip()
            raise Exception(f"OpenRouter HTTP {resp.status_code}")
