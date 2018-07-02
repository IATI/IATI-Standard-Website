from django.shortcuts import redirect


def reference_redirect(request, *args, **kwargs):
    base_url = "http://reference.iatistandard.org"
    slug = request.get_full_path()
    redirection_url = base_url + slug
    return redirect(to=redirection_url, permanent=True)
