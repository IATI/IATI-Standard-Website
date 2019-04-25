"""Module containing custom context processors for IATI's website."""
from django.conf import settings


def assets_library_url(request):
    return {
        "PATTERN_LIBRARY_URL": settings.PATTERN_LIBRARY_URL,
    }
