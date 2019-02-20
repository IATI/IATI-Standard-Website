"""Middleware for redirecting uppercase urls into lowercase."""
from django import http
from django.conf import settings


class LowercaseMiddleware:
    """Middleware class."""

    def __init__(self, get_response):
        """Initialise."""
        self.get_response = get_response

    def __call__(self, request):
        """Redirect url paths as lowercase except for documents or media files."""
        response = self.get_response(request)
        path = request.get_full_path()
        lower = path.lower()
        if lower != path and not("/documents/" in path or settings.MEDIA_URL in path):
            return http.HttpResponseRedirect(lower)
        return response
