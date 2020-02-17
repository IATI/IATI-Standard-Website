"""Module to inject new editor and CSS."""

from django.utils.html import format_html
from wagtail.core import hooks


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

            body#wagtail.page-editor div.locale-picker {{
                # display: none;
            }}

        </style>
        """
    )
