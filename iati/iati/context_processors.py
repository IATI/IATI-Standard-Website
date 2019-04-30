"""Module containing custom context processors for IATI's website."""
from django.conf import settings


def assets_library_url(request):
    """Context processor for pattern library URL."""
    return {
        "PATTERN_LIBRARY_URL": settings.PATTERN_LIBRARY_URL,
    }
