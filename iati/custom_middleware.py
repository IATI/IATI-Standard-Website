"""Middleware for redirecting mixed case urls into lowercase."""
import urllib.parse
from django import http
from django.conf import settings
from wagtail.models import Site


class RedirectIATISites:
    """Middleware to redirect old URLs to new URLs."""

    def __init__(self, get_response):
        """Initialise class."""
        self.get_response = get_response
        self.path = ''
        self.stripped_path = ''
        self.lower_path = ''
        self.path_parts = ''

    def __call__(self, request):
        """Call response to redirect old urls externally."""
        self.path = request.get_full_path()
        self.lower_path = self.path.lower()

        # sanitize the path ready for comparison
        split_path = self.path.split('/')
        valid_path_parts = list(filter(None, split_path))
        self.path_parts = self.remove_language_code(valid_path_parts)
        self.is_download = "downloads" in self.path_parts
        self.stripped_path = '/'.join(self.path_parts)
        full_url = request.build_absolute_uri()
        parsed_url = urllib.parse.urlparse(full_url)
        domain = parsed_url.netloc

        if domain == 'reference.iatistandard.org' and parsed_url.path in ['/', '/en/', '/fr/']:
            return http.HttpResponsePermanentRedirect(f'{settings.REFERENCE_REDIRECT_BASE_URL}/iati-standard/')
        if self.path_is_redirect:
            return http.HttpResponsePermanentRedirect(self.redirected_url)
        elif not request.path_info.endswith('/') and self.path_is_not_exception:
            new_path = request.get_full_path(force_append_slash=True)
            if '%00' in new_path:
                new_path = self.remove_nul_bytes(new_path)
            if new_path != self.path:
                return http.HttpResponsePermanentRedirect(new_path)
        elif '%00' in self.path:
            new_path = self.remove_nul_bytes(self.path)
            return http.HttpResponsePermanentRedirect(new_path)

        return self.get_response(request)

    def remove_language_code(self, path_parts_list):
        """Remove language code from path parts if exists."""
        codes = [x[0] for x in settings.ACTIVE_LANGUAGES]
        if len(path_parts_list) > 0:
            if path_parts_list[0] in codes:
                return tuple(x for x in path_parts_list[1:])
        return tuple(x for x in path_parts_list)

    def remove_index_html(self, stripped_path):
        """Remove index.html from path if exists."""
        stripped_path_split = stripped_path.split('/')
        stripped_path_split = [x for x in stripped_path_split if x != "index.html"]
        return "/".join(stripped_path_split)

    def remove_nul_bytes(self, path):
        """Remove nul bytes from path."""
        return path.replace('%00', '')

    @property
    def exact_redirect_urls(self):
        """Construct tuple of cached redirect urls from settings."""
        return tuple(x for x in settings.EXACT_REFERENCE_NAMESPACES)

    @property
    def wildcard_redirect_urls(self):
        """Construct tuple of cached redirect urls from settings."""
        return tuple(x for x in settings.WILDCARD_REFERENCE_NAMESPACES)

    @property
    def path_is_redirect(self):
        """Verify if path is redirect."""
        if self.stripped_path.startswith(self.exact_redirect_urls) or self.stripped_path.startswith(self.wildcard_redirect_urls):
            return True
        return False

    @property
    def redirected_url(self):
        """Construct redirect URL from base url and request path."""
        if self.stripped_path.startswith(self.exact_redirect_urls):
            redirect_match = next(dict_value for dict_key, dict_value in settings.REFERENCE_NAMESPACE_EXACT_REDIRECT_DICT.items() if self.stripped_path.startswith(dict_key))
            return '{}{}'.format(settings.REFERENCE_REDIRECT_BASE_URL, redirect_match)
        if self.stripped_path.startswith(self.wildcard_redirect_urls):
            redirect_match = next(dict_value for dict_key, dict_value in settings.REFERENCE_NAMESPACE_WILDCARD_REDIRECT_DICT.items() if self.stripped_path.startswith(dict_key))
            self.stripped_path = self.remove_index_html(self.stripped_path)
            if self.is_download:
                return '{}{}{}'.format(settings.REFERENCE_REDIRECT_BASE_URL, redirect_match, self.stripped_path)
            return '{}{}{}{}'.format(settings.REFERENCE_REDIRECT_BASE_URL, redirect_match, self.stripped_path, "/")
        return self.path

    @property
    def exception_values(self):
        """Return values to except from lowercase ruling."""
        return [settings.ADMIN_URL, settings.MEDIA_URL, settings.DOCUMENTS_URL, settings.STATIC_URL, settings.REFERENCE_DOWNLOAD_URL, '/sitemap.xml']

    @property
    def path_is_not_exception(self):
        """Review exceptions to the lowercase ruling."""
        if self.path == '/':
            return False
        if any(item in self.path for item in self.exception_values):
            return False
        if self.path.startswith("/__debug__"):
            return False
        return True


class LowercaseMiddleware:
    """Middleware class to address incoming URLs with mixed cases into lowercase."""

    def __init__(self, get_response):
        """Initialise class."""
        self.get_response = get_response
        self.host = ''
        self.path = ''
        self.lower_path = ''
        self.site_host = ''
        self.request_host = ''
        self.site_hostname = ''

    def __call__(self, request):
        """Redirect url paths as lowercase except for documents or media files."""
        self.request_host = request.get_host()
        self.site_hostname = Site.find_for_request(request).hostname
        self.path = request.get_full_path()
        self.lower_path = self.path.lower()

        if self.path_is_not_lowercase and self.path_is_not_exception:
            return http.HttpResponsePermanentRedirect(self.lower_path)

        return self.get_response(request)

    @property
    def path_is_not_lowercase(self):
        """Check that path is not lowercase already."""
        return urllib.parse.unquote(self.path) != urllib.parse.unquote(self.lower_path)

    @property
    def exception_values(self):
        """Return values to except from lowercase ruling."""
        return [settings.ADMIN_URL, settings.MEDIA_URL, settings.DOCUMENTS_URL, settings.STATIC_URL, settings.REFERENCE_DOWNLOAD_URL]

    @property
    def path_is_not_exception(self):
        """Review exceptions to the lowercase ruling."""
        if self.path == '/':
            return False
        if any(item in self.path for item in self.exception_values):
            return False
        if self.path.startswith("/__debug__"):
            return False
        return True
