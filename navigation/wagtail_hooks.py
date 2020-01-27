from django.utils.html import format_html
from wagtail.core import hooks


@hooks.register('insert_editor_css')
def editor_css():

    # For the data-text selector, see https://css-tricks.com/snippets/css/prevent-long-urls-from-breaking-out-of-container/
    # This fixes long URLs breaking the interface
    return format_html(
        """
        <style>

            .custom-struct-container label
            {{
                float: none;
                width: 100%;
                display: inline-block;
            }}

            .struct-container-help-text {{
                background-color: #d9d9d9;
            }}

        </style>
        """
    )
