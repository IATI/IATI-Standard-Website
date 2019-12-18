from urllib.parse import urlsplit
from django import template

register = template.Library()


@register.filter
def nice_url(value):
    try:
        return urlsplit(value).netloc
    except Exception:
        return value
