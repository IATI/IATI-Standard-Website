from django.utils.html import format_html
from wagtail.core import hooks


@hooks.register('insert_editor_css')
def editor_css():
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
