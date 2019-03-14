"""Middleware for redirecting mixed case urls into lowercase."""
from django import http
from django.conf import settings
from django.utils.functional import cached_property


class LowercaseMiddleware:
    """Middleware class to address incoming URLs with mixed cases into lowercase."""

    def __init__(self, get_response):
        """Initialise class."""
        self.get_response = get_response
        self.path = ''
        self.stripped_path = ''
        self.lower_path = ''
        self.path_parts = ''

    def __call__(self, request):
        """Redirect url paths as lowercase except for documents or media files."""
        response = self.get_response(request)
        self.path = request.get_full_path()
        self.lower_path = self.path.lower()

        # sanitize the path ready for comparison
        split_path = self.path.split('/')
        valid_path_parts = list(filter(None, split_path))
        self.path_parts = self.remove_language_code(valid_path_parts)
        self.stripped_path = '/'.join(self.path_parts)

        # if self.path_is_redirect:
        #     return http.HttpResponsePermanentRedirect(self.redirected_url)

        if self.path_is_exception:
            return http.HttpResponsePermanentRedirect(self.lower_path)

        return response

    def remove_language_code(self, path_parts_list):
        """Remove language code from path parts if exists."""
        codes = [x[0] for x in settings.ACTIVE_LANGUAGES]
        return tuple(x for x in path_parts_list if x not in codes)

    @cached_property
    def redirect_urls(self):
        """Construct tuple of cached redirect urls from settings."""
        return tuple(x for x in settings.REFERENCE_NAMESPACES)

    @property
    def path_is_redirect(self):
        """Verify if path is redirect."""
        if self.stripped_path.startswith(self.redirect_urls):
            return True
        return False

    @property
    def redirected_url(self):
        """Construct redirect URL from base url and request path."""
        return '{}{}'.format(settings.REFERENCE_REDIRECT_BASE_URL, self.path)

    @cached_property
    def exception_values(self):
        """Return values to except from lowercase ruling."""
        return (settings.ADMIN_URL, settings.MEDIA_URL, settings.DOCUMENTS_URL, settings.STATIC_URL)

    @cached_property
    def path_is_exception(self):
        """Review exceptions to the lowercase ruling."""
        if self.lower_path == self.path:
            return False
        if self.path == '/':
            return False
        if self.path.startswith(self.exception_values):
            return False
        return True
