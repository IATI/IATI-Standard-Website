from urllib.parse import urlsplit
from django import template

register = template.Library()


@register.filter
def nice_url(value):
    """Return the domain value only of a URL for nicer labels."""
    try:
        return urlsplit(value).netloc
    except Exception:
        return value
