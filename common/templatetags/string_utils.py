"""Module to clean up tags from text content."""
import bleach
import urllib
import uuid
from django import template
from django.http.request import QueryDict
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='strip_tags')
def strip_tags(text):
    """Strip tags."""
    return mark_safe(bleach.clean(
        text,
        tags=[],
        attributes=[],
        styles=[],
        strip=True,
        strip_comments=True
    ))


def return_all_content(content):
    """Help function to return untruncated stripped content."""
    return mark_safe(str(content).replace('><', '> <')) if content else None


@register.simple_tag
def active_class(var, prop, active):
    """Tag to return an active class if the var and prop test matches."""
    try:
        return active if var == prop else ''
    except Exception:
        return ''


@register.simple_tag
def query_filter(filters, key, value=None):
    """Filter to return a formatted query string for appending to urls."""
    query = filters.copy() if isinstance(filters, QueryDict) else QueryDict().copy()
    try:
        if not value:
            del query[key]
        else:
            query[key] = value
        return '?%s' % urllib.parse.urlencode(query) if query else ''
    except KeyError:
        return '?%s' % urllib.parse.urlencode(query) if query else ''


@register.filter
def lookup(d, key):
    """Filter to enable dictionary lookups by key in templates."""
    return d[key]


@register.simple_tag
def uid():
    """Filter to return a short and very likely unique id per page view."""
    return str(uuid.uuid4())[:6]
