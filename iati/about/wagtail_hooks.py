from django.utils.html import format_html
from django.contrib.staticfiles.templatetags.staticfiles import static

from wagtail.core import hooks


@hooks.register('insert_editor_css')
def editor_css():
    return format_html('<link rel="stylesheet" href="{}">', static('about/admin.css'))
