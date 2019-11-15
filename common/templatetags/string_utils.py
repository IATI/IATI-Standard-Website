import bleach
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='strip_tags')
def strip_tags(text):
    return mark_safe(bleach.clean(
        text,
        tags=[],
        attributes=[],
        styles=[],
        strip=True,
        strip_comments=True
    ))


# Helper function to return untruncated stripped content
def return_all_content(content):
    return mark_safe(str(content).replace('><', '> <')) if content else None
