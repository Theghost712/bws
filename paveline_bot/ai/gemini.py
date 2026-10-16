import logging
from typing import Optional

from .. import config
from .base import AIProvider

logger = logging.getLogger(__name__)


class GeminiProvider(AIProvider):
    def __init__(self):
        self.api_key = config.GEMINI_API_KEY
        self.model = config.GEMINI_MODEL

    async def generate(self, prompt: str, system: Optional[str] = None) -> str:
        if not self.api_key:
            raise Exception("Gemini API key not configured")
        try:
            from google import genai

            client = genai.Client(api_key=self.api_key)
            response = client.models.generate_content(
                model=self.model,
                contents=prompt,
                config={"system_instruction": system} if system else None,
            )
            text = response.text
            if not text or not text.strip():
                raise Exception("Empty response from Gemini")
            return text.strip()
        except Exception as e:
            logger.error(f"Gemini error: {e}")
            raise
