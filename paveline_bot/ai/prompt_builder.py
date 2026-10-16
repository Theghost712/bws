import os
from typing import Dict

from .. import config

DEFAULT_SYSTEM_PROMPT = (
    "You write warm, natural birthday wishes. Write only the wish text. "
    "No titles, no quotes, no emojis unless asked, no explanations."
)

DEFAULT_USER_TEMPLATE = (
    "Write a birthday wish.\n"
    "Recipient: {name}\n"
    "Relationship to sender: {relationship}\n"
    "Sender: {sender}\n"
    "Language: {language} (write natively, not a literal translation)\n"
    "Style: {style}  (romantic | heartfelt | funny | formal | religious)\n"
    "Age turning: {age or 'unknown, do not mention age'}\n"
    "Extra details to include: {extra}\n"
    "Length: {short = 1-2 sentences | medium = 3-4 | long = 5-7}\n"
    "Rules: be sincere and specific, avoid clichés, never invent facts about the person, "
    "keep it respectful for the relationship and culture, no hashtags.\n"
    "Return only the final wish."
)


def build_prompt(wish_context: Dict) -> str:
    template = DEFAULT_USER_TEMPLATE
    try:
        prompt_path = config.PROMPTS_DIR / "wish_prompt.txt"
        if prompt_path.exists():
            content = prompt_path.read_text(encoding="utf-8")
            for line in content.splitlines():
                line = line.strip()
                if line.startswith("User:"):
                    template = line.split("User:", 1)[1].strip()
                    break
    except Exception:
        pass

    try:
        return template.format(
            name=wish_context.get("name") or "",
            relationship=wish_context.get("relationship") or "friend",
            sender=wish_context.get("sender") or "",
            language=wish_context.get("language") or "en",
            style=wish_context.get("style") or "heartfelt",
            age=wish_context.get("age") or "unknown, do not mention age",
            extra=wish_context.get("extra") or "",
            short="1-2 sentences" if (wish_context.get("length") or "medium") == "short" else ("5-7 sentences" if (wish_context.get("length") or "medium") == "long" else "3-4 sentences"),
        )
    except Exception:
        return DEFAULT_USER_TEMPLATE.format(
            name=wish_context.get("name") or "",
            relationship=wish_context.get("relationship") or "friend",
            sender=wish_context.get("sender") or "",
            language=wish_context.get("language") or "en",
            style=wish_context.get("style") or "heartfelt",
            age=wish_context.get("age") or "unknown, do not mention age",
            extra=wish_context.get("extra") or "",
            short="1-2 sentences" if (wish_context.get("length") or "medium") == "short" else ("5-7 sentences" if (wish_context.get("length") or "medium") == "long" else "3-4 sentences"),
        )
