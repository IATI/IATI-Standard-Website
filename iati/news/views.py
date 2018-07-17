"""View defintions for the news app."""

from django.shortcuts import render


def news(request):
    """Render the news page."""
    return render(request, "news/news.html", {})
