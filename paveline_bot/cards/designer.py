import io
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

from PIL import Image, ImageDraw, ImageFont

try:
    import arabic_reshaper
    from bidi.algorithm import get_display

    _SHAPING = True
except Exception:
    _SHAPING = False

from .. import config


LANDSCAPE_SIZE = config.CARD_STORY_SIZE
PORTRAIT_SIZE = config.CARD_POST_SIZE

# Font candidates
_SANS_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
]
_ARABIC_CANDIDATES = [
    "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def contains_arabic(text: str) -> bool:
    return any("\u0600" <= char <= "\u06ff" for char in text or "")


def _first_existing(paths):
    for path in paths:
        if os.path.exists(path):
            return path
    return None


def _load_font(path_candidates, size):
    path = _first_existing(path_candidates)
    if path:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    return ImageFont.load_default(size=size)


def get_font(size: int, rtl: bool = False) -> ImageFont.FreeTypeFont:
    if rtl:
        return _load_font(_ARABIC_CANDIDATES, size)
    return _load_font(_SANS_CANDIDATES, size)


def shape_text(text: str, rtl: bool) -> str:
    if rtl and _SHAPING and contains_arabic(text):
        try:
            return get_display(arabic_reshaper.reshape(text))
        except Exception:
            pass
    return text


def hex_to_rgb(value: str, default=(200, 200, 200)) -> Tuple[int, int, int]:
    value = (value or "").lstrip("#")
    if len(value) != 6:
        return default
    try:
        return tuple(int(value[index : index + 2], 16) for index in (0, 2, 4))
    except ValueError:
        return default


def _gradient(size: Tuple[int, int], start, end):
    width, height = size
    base = Image.new("RGB", size, start)
    draw = ImageDraw.Draw(base)
    for y in range(height):
        ratio = y / max(1, height - 1)
        r = round(start[0] + (end[0] - start[0]) * ratio)
        g = round(start[1] + (end[1] - start[1]) * ratio)
        b = round(start[2] + (end[2] - start[2]) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    return base


def _wrap(draw: ImageDraw.Draw, text: str, font, max_width: int):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        try:
            if draw.textlength(candidate, font=font) <= max_width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word
        except Exception:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def render_card(
    heading: str,
    message: str,
    signoff: str,
    size: Tuple[int, int] = config.CARD_POST_SIZE,
    design: str = "modern",
    photo: Optional[bytes] = None,
) -> Image.Image:
    if design == "romantic":
        bg_start = hex_to_rgb("#f8dfc6")
        bg_end = hex_to_rgb("#ecd5dc")
        accent = hex_to_rgb("#bd685f")
        text_color = hex_to_rgb("#4b3142")
    elif design == "elegant":
        bg_start = hex_to_rgb("#f0f4ff")
        bg_end = hex_to_rgb("#e9d5ff")
        accent = hex_to_rgb("#6b46c1")
        text_color = hex_to_rgb("#1a202c")
    elif design == "colorful":
        bg_start = hex_to_rgb("#d3f9d8")
        bg_end = hex_to_rgb("#dbeafe")
        accent = hex_to_rgb("#34d399")
        text_color = hex_to_rgb("#1f2937")
    elif design == "children":
        bg_start = hex_to_rgb("#fef3c7")
        bg_end = hex_to_rgb("#d1fae5")
        accent = hex_to_rgb("#f59e0b")
        text_color = hex_to_rgb("#1f2937")
    elif design == "religious":
        bg_start = hex_to_rgb("#eef2ff")
        bg_end = hex_to_rgb("#f5f3ff")
        accent = hex_to_rgb("#4f46e5")
        text_color = hex_to_rgb("#1a202c")
    else:  # modern
        bg_start = hex_to_rgb("#f3f4f6")
        bg_end = hex_to_rgb("#e5e7eb")
        accent = hex_to_rgb("#3b82f6")
        text_color = hex_to_rgb("#111827")

    image = _gradient(size, bg_start, bg_end)
    draw = ImageDraw.Draw(image)
    width, height = size

    rtl = contains_arabic(heading) or contains_arabic(message)
    margin = int(width * 0.1)
    content_width = width - margin * 2
    cursor_y = int(height * 0.15)

    heading_font = get_font(int(height * 0.08), rtl=rtl)
    body_font = get_font(int(height * 0.04), rtl=rtl)
    signoff_font = get_font(int(height * 0.035), rtl=rtl)

    heading_text = shape_text(heading, rtl)
    anchor = "ra" if rtl else "la"
    try:
        draw.text((margin, cursor_y), heading_text, font=heading_font, fill=accent, anchor=anchor)
    except Exception:
        draw.text((margin, cursor_y), heading_text, font=heading_font, fill=accent)
    cursor_y += int(height * 0.12)

    body_lines = _wrap(draw, shape_text(message, rtl), body_font, content_width)
    line_height = int(height * 0.06)
    for line in body_lines:
        try:
            draw.text((margin, cursor_y), line, font=body_font, fill=text_color, anchor=anchor)
        except Exception:
            draw.text((margin, cursor_y), line, font=body_font, fill=text_color)
        cursor_y += line_height

    try:
        draw.text((margin, height - int(height * 0.12)), shape_text(signoff, rtl), font=signoff_font, fill=accent, anchor=anchor)
    except Exception:
        draw.text((margin, height - int(height * 0.12)), shape_text(signoff, rtl), font=signoff_font, fill=accent)

    return image


def card_to_bytes(image: Image.Image, fmt: str = "PNG") -> bytes:
    buffer = io.BytesIO()
    if fmt.upper() == "PNG":
        image.save(buffer, format="PNG", optimize=True)
    else:
        image.convert("RGB").save(buffer, format=fmt, quality=92)
    buffer.seek(0)
    return buffer.getvalue()


def save_card(image: Image.Image, name: Optional[str] = None) -> Path:
    config.OUTPUT_DIR.mkdir(exist_ok=True)
    if not name:
        name = f"{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.png"
    path = config.OUTPUT_DIR / name
    image.save(path, format="PNG", optimize=True)
    return path
