from django.utils.html import format_html
from wagtail.core import hooks


@hooks.register('insert_editor_css')
def editor_css():

    # For the data-text selector, see https://css-tricks.com/snippets/css/prevent-long-urls-from-breaking-out-of-container/
    # This fixes long URLs breaking the interface
    return format_html(
        """
        <style>

            .navigation__meganav .field-content
            {{
                float: none;
                width: 100%;
            }}

            .navigation__meganav .multiple label,
            .navigation__meganav .sequence-container label,
            .navigation__meganav .custom__itemlist .sequence-container
            {{
                width: 100%;
            }}

            .navigation__meganav .sequence-container .stream-menu-inner ul
            {{
                text-align: center;
            }}

            .navigation__meganav .sequence-container .stream-menu-inner ul li
            {{
                display: inline-block;
                float: none;
            }}

            .navigation__meganav .sequence-container .stream-menu li {{
                width: auto;
            }}

        </style>
        """
    )
