"""Module to update wagtail hooks with bespoke JavaScript and urls."""
from django.conf.urls import include, url
from django.utils.html import format_html_join
from django.templatetags.static import static
from wagtail.core import hooks
from iati_standard import urls


@hooks.register('register_admin_urls')
def register_admin_urls():
    """Register bespoke URLs."""
    return [
        url(r'^iati_standard/', include(urls, namespace='iati_standard')),
    ]


@hooks.register('insert_editor_js')
def editor_js():
    """Inject bespoke JavaScript."""
    js_files = [
        'iati_standard/js/reference-utils.js',
    ]
    js_includes = format_html_join('\n', '<script src="{0}"></script>', ((static(filename),) for filename in js_files))
    return js_includes
