"""Server-side birthday card rendering with Pillow.

Produces a PNG from a :class:`~cards.models.CardTemplate` and user content.
Text is wrapped to fit, long words are broken, and Arabic text is shaped with
``arabic-reshaper``/``python-bidi`` when those optional packages are present
(they are listed in requirements.txt).
"""

import io
import math
import os
import textwrap

from django.conf import settings
from PIL import Image, ImageDraw, ImageFont

try:  # optional but strongly recommended for Arabic cards
    import arabic_reshaper
    from bidi.algorithm import get_display

    _SHAPING = True
except Exception:  # pragma: no cover - graceful degradation
    _SHAPING = False


LANDSCAPE_SIZE = (1200, 800)
PORTRAIT_SIZE = (800, 1200)

_SANS_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
]
_SANS_BOLD_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
]
_SERIF_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSerif.ttf",
]
_SERIF_BOLD_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf",
]
_ARABIC_CANDIDATES = [
    "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf",
    "/usr/share/fonts/truetype/noto/NotoKufiArabic-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]
_ARABIC_BOLD_CANDIDATES = [
    "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoKufiArabic-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]

FONT_CHOICES = [
    ("serif", "Elegant serif"),
    ("sans", "Clean sans"),
    ("display", "Display serif"),
]

_FONT_SETS = {
    "serif": (_SERIF_CANDIDATES, _SERIF_BOLD_CANDIDATES),
    "sans": (_SANS_CANDIDATES, _SANS_BOLD_CANDIDATES),
    "display": (_SERIF_CANDIDATES, _SERIF_BOLD_CANDIDATES),
    "arabic": (_ARABIC_CANDIDATES, _ARABIC_BOLD_CANDIDATES),
}


def contains_arabic(text):
    return any("\u0600" <= char <= "\u06ff" for char in text or "")


def _first_existing(paths):
    for path in paths:
        if os.path.exists(path):
            return path
    return None


def _load_font(path_candidates, size, bold_candidates=None):
    path = _first_existing(path_candidates)
    if path is None and bold_candidates:
        path = _first_existing(bold_candidates)
    if path:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    return ImageFont.load_default(size=size)


def get_font(font_name, size, bold=False, rtl=False):
    if rtl:
        regular, bold_set = _FONT_SETS["arabic"]
    else:
        regular, bold_set = _FONT_SETS.get(font_name, _FONT_SETS["sans"])
    if bold:
        return _load_font(bold_set or regular, size, regular)
    return _load_font(regular, size, bold_set)


def shape_text(text, rtl):
    if rtl and _SHAPING and contains_arabic(text):
        return get_display(arabic_reshaper.reshape(text))
    return text


def hex_to_rgb(value, default=(200, 200, 200)):
    value = (value or "").lstrip("#")
    if len(value) != 6:
        return default
    try:
        return tuple(int(value[index:index + 2], 16) for index in (0, 2, 4))
    except ValueError:
        return default


def _mix(color_a, color_b, ratio):
    return tuple(round(a + (b - a) * ratio) for a, b in zip(color_a, color_b))


def _gradient(size, start, end):
    width, height = size
    base = Image.new("RGB", size, start)
    draw = ImageDraw.Draw(base)
    for y in range(height):
        draw.line([(0, y), (width, y)], fill=_mix(start, end, y / max(1, height - 1)))
    return base


def _wrap(draw, text, font, max_width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if draw.textlength(candidate, font=font) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            # break over-long words
            if draw.textlength(word, font=font) > max_width:
                chunk = ""
                for char in word:
                    if draw.textlength(chunk + char, font=font) <= max_width:
                        chunk += char
                    else:
                        lines.append(chunk)
                        chunk = char
                current = chunk
            else:
                current = word
    if current:
        lines.append(current)
    return lines


def _circular_photo(photo, diameter):
    image = Image.open(photo).convert("RGB")
    side = min(image.size)
    left = (image.width - side) // 2
    top = (image.height - side) // 2
    image = image.crop((left, top, left + side, top + side)).resize((diameter, diameter), Image.LANCZOS)
    mask = Image.new("L", (diameter, diameter), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, diameter, diameter), fill=255)
    output = Image.new("RGBA", (diameter, diameter), (0, 0, 0, 0))
    output.paste(image, (0, 0), mask)
    return output



def _draw_floral_decoration(image, template_slug, accent_rgb, text_rgb, bg2_rgb):
    """Draw subtle floral elements for floral/romantic templates."""
    draw = ImageDraw.Draw(image, "RGBA")
    w, h = image.size
    if template_slug in ("floral-garden",):
        # soft corner blooms
        for cx, cy, sz in ((w*0.08, h*0.12, w*0.05), (w*0.92, h*0.88, w*0.04), (w*0.12, h*0.85, w*0.035)):
            r = int(sz)
            # petals
            petal = tuple(int(c*0.8 + a*0.2) for c,a in zip(text_rgb[:3], accent_rgb[:3]))
            petal = (*petal, 60)
            center = (*text_rgb[:3], 90)
            for i in range(5):
                ang = 2*math.pi*i/5 - math.pi/2
                x = cx + r*0.5*math.cos(ang)
                y = cy + r*0.5*math.sin(ang)
                draw.ellipse([x-r*0.28, y-r*0.28, x+r*0.28, y+r*0.28], fill=petal)
            draw.ellipse([cx-r*0.18, cy-r*0.18, cx+r*0.18, cy+r*0.18], fill=center)
    elif template_slug in ("romantic-blush",):
        # delicate scattered blooms
        for cx, cy, sz in ((w*0.06, h*0.08, w*0.04), (w*0.94, h*0.92, w*0.035), (w*0.10, h*0.90, w*0.03)):
            r = int(sz)
            petal = (*accent_rgb[:3], 40)
            center = (*accent_rgb[:3], 70)
            for i in range(6):
                ang = 2*math.pi*i/6
                x = cx + r*0.6*math.cos(ang)
                y = cy + r*0.6*math.sin(ang)
                draw.ellipse([x-r*0.22, y-r*0.22, x+r*0.22, y+r*0.22], fill=petal)
            draw.ellipse([cx-r*0.16, cy-r*0.16, cx+r*0.16, cy+r*0.16], fill=center)
    else:
        # subtle vine-like accents for others with floral-ish feel
        if template_slug in ("elegant-midnight", "minimalist-linen"):
            return
        # faint corner sprigs
        for cx, cy in ((w*0.05, h*0.95), (w*0.95, h*0.05)):
            draw.line([cx, cy, cx+w*0.08, cy-h*0.06] if cx<w/2 else [cx, cy, cx-w*0.08, cy+h*0.06],
                      fill=(*accent_rgb[:3], 25), width=2)

def render_card(
    template,
    *,
    heading,
    message,
    signoff,
    font_name="serif",
    accent=None,
    orientation=None,
    photo=None,
):
    """Render a card and return a Pillow ``Image`` in RGB mode."""
    orientation = orientation or template.orientation
    size = PORTRAIT_SIZE if orientation == "portrait" else LANDSCAPE_SIZE

    bg = hex_to_rgb(template.background, (248, 223, 198))
    bg2 = hex_to_rgb(template.background_secondary, (236, 213, 220))
    accent_rgb = hex_to_rgb(accent or template.accent, (189, 104, 95))
    text_rgb = hex_to_rgb(template.text_color, (75, 49, 66))
    bg2_rgb = bg2


    image = _gradient(size, bg, bg2)
    draw = ImageDraw.Draw(image, "RGBA")
    width, height = size

    # Decorative translucent circles.
    draw.ellipse(
        [width - 320, -160, width + 120, 280],
        outline=accent_rgb + (90,),
        width=3,
    )
    draw.ellipse(
        [-160, height - 320, 240, height + 120],
        outline=accent_rgb + (70,),
        width=3,
    )
    _draw_floral_decoration(image, template.slug, accent_rgb, text_rgb, bg2)

    rtl = contains_arabic(heading) or contains_arabic(message)
    margin = int(width * 0.11)
    content_width = width - margin * 2
    cursor_y = int(height * (0.16 if not photo else 0.24))

    if photo is not None:
        try:
            diameter = int(height * 0.16)
            avatar = _circular_photo(photo, diameter)
            image.paste(avatar, (margin, int(height * 0.05)), avatar)
            cursor_y = int(height * 0.28)
        except Exception:
            cursor_y = int(height * 0.16)

    heading_font = get_font(font_name, int(height * 0.075), bold=True, rtl=rtl)
    body_font = get_font(font_name, int(height * 0.036), rtl=rtl)
    signoff_font = get_font(font_name, int(height * 0.032), bold=True, rtl=rtl)

    heading_text = shape_text(heading, rtl)
    anchor = "ra" if rtl else "la"
    draw.text((margin, cursor_y), heading_text, font=heading_font, fill=accent_rgb, anchor=anchor)
    cursor_y += int(height * 0.11)

    body_lines = _wrap(draw, shape_text(message, rtl), body_font, content_width)
    line_height = int(height * 0.052)
    for line in body_lines:
        draw.text((margin, cursor_y), line, font=body_font, fill=text_rgb, anchor=anchor)
        cursor_y += line_height

    draw.text(
        (margin, height - int(height * 0.14)),
        shape_text(signoff, rtl),
        font=signoff_font,
        fill=accent_rgb,
        anchor=anchor,
    )

    return image


def image_to_bytes(image, fmt="PNG"):
    buffer = io.BytesIO()
    if fmt.upper() == "PNG":
        image.save(buffer, format="PNG", optimize=True)
    else:
        image.convert("RGB").save(buffer, format=fmt, quality=92)
    buffer.seek(0)
    return buffer


def validate_upload(upload, max_bytes=None):
    """Return ``(ok, error_message)`` for an uploaded photo."""
    max_bytes = max_bytes or getattr(settings, "MAX_UPLOAD_SIZE", 5 * 1024 * 1024)
    if upload is None:
        return True, None
    if upload.size > max_bytes:
        return False, f"Image must be smaller than {max_bytes // (1024 * 1024)} MB."
    content_type = getattr(upload, "content_type", "")
    if content_type not in {"image/jpeg", "image/png", "image/webp", "image/gif"}:
        return False, "Please upload a JPG, PNG, WEBP or GIF image."
    return True, None
