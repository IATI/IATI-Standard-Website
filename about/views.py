"""View definitions for the about app."""

from django.shortcuts import render


def about(request):
    """Render the about page."""
    return render(request, "about/about.html", {})
