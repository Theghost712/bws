import logging
from typing import Dict, List, Optional

from .fallback_templates import generate_fallback_wish
from .validators import sanitize_extra, validate_wish_output
from ..ai.prompt_builder import build_prompt
from ..ai.router import AIRouter

logger = logging.getLogger(__name__)

_MAX_WISH_LEN = 500
_VARIANTS = 3


def _fallback_wish(context: Dict, variation: int = 0) -> str:
    return generate_fallback_wish(
        name=context.get("name") or "",
        relationship=context.get("relationship") or "friend",
        language=context.get("language") or "en",
        style=context.get("style") or "heartfelt",
        sender=context.get("sender") or "",
        extra=context.get("extra") or "",
        variation=variation,
    )


async def generate_wish(context: Dict, variation: int = 0) -> Dict:
    """Generate a single validated wish, using AI with fallback to local templates."""
    ai_router = AIRouter()
    prompt = build_prompt(context)
    system = "You write warm, natural birthday wishes. Write only the wish text. No titles, no quotes, no emojis unless asked, no explanations."

    wish_text = None
    try:
        wish_text = await ai_router.generate_with_fallback(prompt, system)
    except Exception as e:
        logger.error(f"Wish generation failed, using fallback: {e}")
        wish_text = None

    if not validate_wish_output(wish_text or "", context.get("language") or "en", max_length=_MAX_WISH_LEN):
        logger.warning("AI wish output invalid; regenerating once")
        try:
            wish_text = await ai_router.generate_with_fallback(prompt, system)
        except Exception:
            wish_text = None

    if not validate_wish_output(wish_text or "", context.get("language") or "en", max_length=_MAX_WISH_LEN):
        logger.warning("AI wish still invalid; using offline fallback")
        wish_text = _fallback_wish(context, variation)

    return {
        "text": wish_text,
        "language": context.get("language") or "en",
        "style": context.get("style") or "heartfelt",
        "variation": variation,
    }


async def generate_wishes(context: Dict, count: int = _VARIANTS) -> List[Dict]:
    """Generate ``count`` validated wish variants for the same context."""
    wishes = []
    for i in range(count):
        wishes.append(await generate_wish(context, variation=i))
    return wishes
