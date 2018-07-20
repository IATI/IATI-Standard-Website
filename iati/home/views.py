"""View definitions for the home app."""

from django.shortcuts import redirect


<<<<<<< HEAD
def reference_redirect(request):
    """Functional view that accepts any request starting with a reference namespace."""
=======
def reference_redirect(request, *args, **kwargs):
    """A functional view that accepts any request starting with a reference namespace."""
>>>>>>> parent of 9d7e6e3... Remove unused arbitrary args
    base_url = "http://reference.iatistandard.org"
    slug = request.get_full_path()
    redirection_url = base_url + slug
    return redirect(to=redirection_url, permanent=True)
