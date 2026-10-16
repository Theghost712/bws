import re
from typing import Optional

AI_FAILURE_PATTERNS = [
    r"as an ai",
    r"i cannot",
    r"i'm sorry",
    r"i apologize",
    r"language model",
    r"i don't have the ability",
    r"as a large language model",
]

FORBIDDEN_MARKDOWN = re.compile(r"[*_`#\[\]|<>]")


def validate_wish_output(text: str, language: str = "en", max_length: int = 500) -> bool:
    if not text or not text.strip():
        return False
    clean = text.strip()
    if len(clean) > max_length:
        return False
    lower = clean.lower()
    for pattern in AI_FAILURE_PATTERNS:
        if re.search(pattern, lower):
            return False
    if FORBIDDEN_MARKDOWN.search(clean):
        return False
    return True


def sanitize_extra(extra: Optional[str]) -> str:
    if not extra:
        return ""
    sanitized = re.sub(r"[\x00-\x1F\x7F]", " ", extra)
    sanitized = re.sub(r"\s+", " ", sanitized).strip()
    if len(sanitized) > 400:
        sanitized = sanitized[:400]
    return sanitized
