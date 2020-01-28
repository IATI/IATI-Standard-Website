"""Module for IATI Standard utilities."""
import re
from django.utils.text import slugify


def URLify(s):
    """Python port of Wagtail admin JS function for creating page slugs"""
    removelist = [
        'a', 'an', 'as', 'at', 'before', 'but', 'by', 'for', 'from', 'is',
        'in', 'into', 'like', 'of', 'off', 'on', 'onto', 'per', 'since',
        'than', 'the', 'this', 'that', 'to', 'up', 'via', 'with'
    ]
    r = r'\b(' + r'|'.join(removelist) + r')\b'
    slug = re.sub(r, r'', s, flags=re.I)
    slug = slugify(slug, allow_unicode=True)
    return slug
