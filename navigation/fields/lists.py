"""Module of lists available as part of the navigation menu."""

from wagtail.blocks import (
    BooleanBlock,
    CharBlock,
    ListBlock,
    PageChooserBlock,
    StructBlock,
)
from navigation.fields import TranslatedPage
from navigation.values import TransStructValue


class NestedPageGroup(StructBlock):
    """Class for a nested page group."""

    class Meta:
        icon = 'list-ul'
        label = 'Page group'
        value_class = TransStructValue

    page = PageChooserBlock(
        help_text='Optional: top level page for the group',
        required=False,
        label='Top level page',
    )
    title_en = CharBlock(
        help_text='Optional: plain text title for the page group',
        label='Title [en]',
        required=False,
    )
    title_fr = CharBlock(
        help_text='Optional: plain text title for the page group',
        label='Title [fr]',
        required=False,
    )
    page_group = ListBlock(
        TranslatedPage(),
        required=False,
        help_text='Optional: group of sub pages, displayed as an indented list',
    )


class PageList(StructBlock):
    """Class for a page list."""

    class Meta:
        help_text = '''
                    <strong>List of internal page links.</strong><br>
                    Optional: select the first page link to use as a title, or add a plain text title.<br>
                    Optional: short description.
                    '''
        icon = 'list-ul'
        label = 'Page list'
        form_template = 'navigation/block_forms/custom_struct.html'
        template = 'navigation/blocks/page_list.html'
        value_class = TransStructValue

    use_first_page_as_title = BooleanBlock(
        help_text='Optional: if checked, the first page in the list will be displayed as a title, overriding any plain text title below',
        required=False,
    )
    title_en = CharBlock(
        help_text='Optional: plain text title for the page list',
        label='Title [en]',
        required=False,
    )
    title_fr = CharBlock(
        help_text='Optional: plain text title for the page list',
        label='Title [fr]',
        required=False,
    )
    description_en = CharBlock(
        help_text='Optional: description for the page list',
        label='Description [en]',
        required=False,
    )
    description_fr = CharBlock(
        help_text='Optional: description for the page list',
        label='Description [fr]',
        required=False,
    )
    page_list = ListBlock(
        TranslatedPage(),
        label='Pages',
    )


class NestedPageList(StructBlock):
    """Class for a nested page list."""

    class Meta:
        help_text = '''
                    <strong>List of internal page links, with optional page link sub-groups.</strong><br>
                    Optional: plain text title for sub-groups<br>
                    '''
        icon = 'list-ul'
        label = 'Nested page list'
        form_template = 'navigation/block_forms/custom_struct.html'
        template = 'navigation/blocks/nested_page_list.html'
        value_class = TransStructValue

    groups = ListBlock(
        NestedPageGroup()
    )
