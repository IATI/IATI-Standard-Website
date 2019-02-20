"""Middleware for redirecting uppercase urls into lowercase."""
from django import http
from django.conf import settings

EXTERNAL_REDIRECTS = [
    "/101/",
    "/102/",
    "/103/",
    "/104/",
    "/105/",
    "/201/",
    "/202/",
    "/203/",
    "/activity-standard/",
    "/codelists/",
    "/developer/",
    "/introduction/",
    "/namespaces-extensions/",
    "/organisation-identifiers/",
    "/organisation-standard/",
    "/reference/",
    "/rulesets/",
    "/schema/",
    "/upgrades/",
    "/guidance/datastore/",
]


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
        for external in EXTERNAL_REDIRECTS:
            if external in path:
                return response
        if lower != path and not("/documents/" in path or settings.MEDIA_URL in path):
            return http.HttpResponseRedirect(lower)
        return response
