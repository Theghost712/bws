"""Template context shared across every page."""

from django.conf import settings
from django.utils import translation

from .constants import RTL_LANGUAGES, SUPPORTED_LANGUAGES


def site_context(request):
    current = translation.get_language() or settings.LANGUAGE_CODE
    return {
        "SITE_NAME": "Paveline",
        "SITE_EMAIL": settings.SITE_EMAIL,
        "SITE_PHONE": settings.SITE_PHONE,
        "SITE_PHONE_TEL": settings.SITE_PHONE.replace(" ", ""),
        "SUPPORTED_LANGUAGES": SUPPORTED_LANGUAGES,
        "CURRENT_LANGUAGE": current,
        "IS_RTL": current in RTL_LANGUAGES,
        "CURRENT_PATH": request.get_full_path(),
    }
