"""View definitions for the contact app."""

from django.shortcuts import render


def contact(request):
    """Render the contact page."""
    return render(request, "contact/contact.html", {})
