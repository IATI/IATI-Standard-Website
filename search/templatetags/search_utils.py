import re
from django import template
from wagtail.core.blocks.stream_block import StreamValue
from common.templatetags.string_utils import return_all_content

ALLOWED_BLOCK_TYPES = [
    'h2',
    'h3',
    'h4',
    'intro',
    'paragraph',
    'pullquote',
]

register = template.Library()


@register.filter()
def nice_url(url):
    try:
        if url.endswith('/'):
            url = url[:-1]
        return url.replace('/', ' › ').replace(' ›  › ', '//')
    except Exception:
        return ''


@register.filter()
def verbose_name(obj):
    try:
        return obj._meta.verbose_name
    except Exception:
        return ''


@register.filter()
def search_content(obj):
    indexable_text = []
    if hasattr(obj, 'excerpt'):
        if obj.excerpt:
            indexable_text.append(obj.excerpt)

    if not hasattr(obj, 'content_editor'):
        return ' '.join(indexable_text)

    content = obj.content_editor

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
        if indexable_text:
            return re.sub(r' +', ' ', ' '.join(indexable_text)).strip()

    return ''
