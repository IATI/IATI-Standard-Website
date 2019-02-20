"""Middleware for redirecting mixed case urls into lowercase."""
from django import http
from django.conf import settings


def check_exceptions(path):
    """Review exceptions to the lowercase ruling."""
    if path.startswith(settings.MEDIA_URL):
        # Make sure it's not a media file
        return False
    for code, _ in settings.ACTIVE_LANGUAGES:
        # Check for all active languages
        if path.startswith("/" + code + "/documents/"):
            return False
    return True


class LowercaseMiddleware:
    """Middleware class to address incoming URLs with mixed cases into lowercase."""

    def __init__(self, get_response):
        """Initialise class."""
        self.get_response = get_response

    def __call__(self, request):
        """Redirect url paths as lowercase except for documents or media files."""
        response = self.get_response(request)
        path = request.get_full_path()
        if not response.get_host().startswith("iatistandard.org") or not check_exceptions(path):
            return response
        lower_path = path.lower()
        return http.HttpResponsePermanentRedirect(lower_path)
