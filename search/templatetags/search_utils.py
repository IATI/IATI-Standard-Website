import re
from django import template
from wagtail.core.blocks.stream_block import StreamValue
from common.templatetags.string_utils import return_all_content

ALLOWED_BLOCK_TYPES = [
    'case_study',
    'definition_list',
    'infographic',
    'rich_text',
    'section_heading',
    'table',
]

register = template.Library()


@register.filter()
def verbose_name(obj):
    try:
        return obj._meta.verbose_name
    except Exception:
        return ''


@register.filter()
def search_content(obj):
    # TODO: amend to convert line breaks to spaces in rich content
    indexable_text = []
    if hasattr(obj, 'excerpt_field'):
        indexable_text.append(obj.excerpt_field)

    if not hasattr(obj, 'content'):
        return ' '.join(indexable_text)

    content = obj.content

    if isinstance(content, str):
        indexable_text.append(return_all_content(content))
        return re.sub(r' +', ' ', ' '.join(indexable_text)).strip()

    if isinstance(content, StreamValue):
        indexable_text = []
        text = ''
        for block in content:
            text = ''
            if block.block_type in ALLOWED_BLOCK_TYPES:
                text = return_all_content(block.render())
                if text:
                    indexable_text.append(' %s' % text)
        if text:
            return re.sub(r' +', ' ', ' '.join(indexable_text)).strip()

    return ''
