"""Module to define highlight field classes."""

from wagtail.blocks import (
    CharBlock,
    ChoiceBlock,
    PageChooserBlock,
    StructBlock,
    TextBlock,
)
from navigation.values import TransStructValue


class AbstractHighlight(StructBlock):
    """Class for the abstract highlight module."""

    class Meta:
        abstract = True
        icon = 'pick'
        form_template = 'navigation/block_forms/custom_struct.html'
        value_class = TransStructValue

    page = PageChooserBlock(
        help_text='Page for title and link'
    )
    description = TextBlock(
        help_text='Description for the module',
        label='Description',
    )


class Highlight(AbstractHighlight):
    """Class for the highlight module."""

    class Meta:
        help_text = '''
                    <strong>Highlight module</strong><br>
                    Internal page link and short description.
                    '''
        icon = 'pick'
        template = 'navigation/blocks/highlight.html'

    width = ChoiceBlock(
        help_text='Width of the highlight module',
        choices=[
            ('small', 'Regular'),
            ('wide', 'Wide'),
        ],
        default='small',
        required=True,
    )


class SecondaryHighlight(AbstractHighlight):
    """Class for the secondary highlight module."""

    class Meta:
        help_text = '''
                    <strong>Secondary highlight module</strong><br>
                    Internal page link, short description, and link label.
                    '''
        icon = 'pick'
        template = 'navigation/blocks/secondary_highlight.html'

    link_label = CharBlock(
        help_text='Label for the page link button',
        label='Link label',
    )
