"""Module to clean up tags from text content."""
import bleach
from django import template
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
    """Helper function to return untruncated stripped content."""
    return mark_safe(str(content).replace('><', '> <')) if content else None
