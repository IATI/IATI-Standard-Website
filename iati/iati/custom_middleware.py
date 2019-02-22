"""Middleware for redirecting mixed case urls into lowercase."""
from django import http
from django.conf import settings
from django.utils.functional import cached_property


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
        # import pdb; pdb.set_trace()
        if self.path_is_exception(path, lower_path):
            return http.HttpResponsePermanentRedirect(lower_path)
        return response

    @cached_property
    def exception_values(self):
        """Return values to except from lowercase ruling."""
        return (settings.ADMIN_URL, settings.MEDIA_URL, settings.DOCUMENTS_URL)

    def path_is_exception(self, path, lower_path):
        """Review exceptions to the lowercase ruling."""
        if lower_path == path:
            return False
        if path == '/':
            return False
        if path.startswith(self.exception_values):
            return False
        return True
