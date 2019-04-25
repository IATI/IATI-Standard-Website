"""View definitions for the guidance_and_support app."""

from django.shortcuts import render


def guidance_and_support(request):
    """Render the guidance and support page."""
    return render(request, "guidance_and_support/guidance_and_support.html", {})


def community(request):
    """Render the community page."""
    return render(request, "guidance_and_support/community_page.html", {})
