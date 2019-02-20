"""Middleware for redirecting mixed case urls into lowercase."""
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


def check_exceptions(path):
    """Review exceptions to the lowercase ruling."""
    if path.startswith(settings.MEDIA_URL):
        #Make sure it's not a media file
        return False
    for code, lang in settings.ACTIVE_LANGUAGES:
        #Check for all active languages
        if path.startswith("/" + code + "/documents/"):
            print("Exit here")
            return False
        for external in EXTERNAL_REDIRECTS:
            if path.startswith("/" + code + external):
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
        lower_path = path.lower()
        if lower_path != path and check_exceptions(path):
            return http.HttpResponseRedirect(lower_path)
        return response
