"""Birthday wish generation service.

Pure Python: no HTTP, no database, no external API. Views call these
functions, which makes the generator easy to test and easy to upgrade later
(e.g. swapping in an AI provider behind the same interface).
"""

from core.constants import LANGUAGE_CODES, TONE_CHOICES
from core.dates import age_turning, is_birthday_today, local_today

from .messages import AGE_LINE, BODIES, GREETINGS, HELLO, LONG_CLOSERS, SIGNOFF

_VALID_TONES = {code for code, _ in TONE_CHOICES}
_DEFAULT_LANG = "en"
_DEFAULT_TONE = "heartfelt"
_DEFAULT_RELATIONSHIP = "friend"

_MAX_NAME = 60
_MAX_SENDER = 60
_MAX_PERSONAL = 400


def _clean(value, limit):
    if not value:
        return ""
    return str(value).strip()[:limit]


def _normalise_language(language):
    return language if language in LANGUAGE_CODES else _DEFAULT_LANG


def _normalise_tone(tone):
    return tone if tone in _VALID_TONES else _DEFAULT_TONE


def _normalise_relationship(relationship):
    if relationship in GREETINGS[_DEFAULT_LANG]:
        return relationship
    return _DEFAULT_RELATIONSHIP


def _compose_body(language, tone, length, variation):
    variants = BODIES[language][tone]
    sentences = variants[variation % len(variants)]

    if length == "short":
        body = " ".join(sentences[:1])
    elif length == "long":
        body = " ".join(sentences)
    else:  # medium
        body = " ".join(sentences[:2]) if len(sentences) > 1 else sentences[0]

    if length == "long":
        closers = LONG_CLOSERS[language]
        body = f"{body} {closers[variation % len(closers)]}"
    return body


def generate_wish(
    *,
    name="",
    relationship=_DEFAULT_RELATIONSHIP,
    tone=_DEFAULT_TONE,
    length="medium",
    language=_DEFAULT_LANG,
    sender="",
    personal="",
    birth_month=None,
    birth_day=None,
    birth_year=None,
    include_age=False,
    variation=0,
    today=None,
):
    """Generate a single personalised birthday wish.

    Returns a plain dict so it can be serialised, rendered or stored easily.
    """
    language = _normalise_language(language)
    tone = _normalise_tone(tone)
    relationship = _normalise_relationship(relationship)

    name = _clean(name, _MAX_NAME)
    sender = _clean(sender, _MAX_SENDER)
    personal = _clean(personal, _MAX_PERSONAL)

    display_name = name or GREETINGS[language][relationship]
    heading = f"{HELLO[language]}, {display_name}!"

    body = _compose_body(language, tone, length, variation)

    is_today = False
    age = None
    if birth_month and birth_day:
        today = today or local_today()
        is_today = is_birthday_today(birth_month, birth_day, today)
        if include_age and birth_year:
            age = age_turning(birth_year, birth_month, birth_day, today)

    parts = []
    if age:
        parts.append(AGE_LINE[language].format(age=age))
    parts.append(body)
    if personal:
        parts.append(personal)

    message = " ".join(parts)

    signoff = SIGNOFF[language]
    if sender:
        signoff = f"{signoff}, {sender}"

    return {
        "heading": heading,
        "message": message,
        "signoff": signoff,
        "language": language,
        "tone": tone,
        "length": length,
        "relationship": relationship,
        "recipient_name": name,
        "sender_name": sender,
        "personal_message": personal,
        "is_today": is_today,
        "age": age,
    }


def generate_alternatives(context, count=3):
    """Return ``count`` distinct variations for the same inputs."""
    return [generate_wish(variation=index, **context) for index in range(count)]


def as_share_text(wish):
    """Plain-text form suitable for copying or WhatsApp sharing."""
    return f"{wish['heading']}\n\n{wish['message']}\n\n{wish['signoff']}"
