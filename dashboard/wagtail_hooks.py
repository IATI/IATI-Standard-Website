"""Module to inject new editor and CSS."""

from django.utils.html import format_html
from wagtail.core import hooks


@hooks.register('construct_main_menu')
def hide_snippets_menu_item(request, menu_items):
    """Hide the default snippets menu item."""
    menu_items[:] = [item for item in menu_items if item.name != 'snippets']


@hooks.register('insert_editor_css')
def editor_css():
    """Inject new editor CSS."""
    return format_html(
        """
        <style>
            .help-block.help-block--snippet-initial {{
                margin-top: -3em;
                margin-bottom: 0;
            }}
            form > div.locale-picker {{
                text-align: left;
                margin: 1.5em 2em 1em !important;
            }}
            @media screen and (min-width: 800px) {{
                form > div.locale-picker {{
                    text-align: left;
                    margin: 1.5em 4em 1em !important;
                }}
            }}
            .non-floated-options label {{
                display: block;
                float: none;
                width: 100%;
            }}
        </style>
        """
    )
