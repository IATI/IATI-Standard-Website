"""View definitions for the home app."""

from django.shortcuts import redirect


def reference_redirect(request, *args, **kwargs):
    """Functional view that accepts any request starting with a reference namespace.

    NOTE: args and kwargs are not used, but are required to catch all positional arguments.
    """
    base_url = "http://reference.iatistandard.org"
    slug = request.get_full_path()
    redirection_url = base_url + slug
    return redirect(to=redirection_url, permanent=True)
