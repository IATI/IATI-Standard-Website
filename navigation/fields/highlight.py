from wagtail.core.blocks import (
    CharBlock,
    PageChooserBlock,
    StructBlock,
    TextBlock,
)
from navigation.values import TransStructValue


class AbstractHighlight(StructBlock):

    class Meta:
        abstract = True
        icon = 'pick'
        form_template = 'navigation/block_forms/custom_struct.html'
        value_class = TransStructValue

    page = PageChooserBlock(
        help_text='Page for title and link'
    )
    description_en = TextBlock(
        help_text='Description for the module',
        label='Description [en]',
    )
    description_fr = TextBlock(
        help_text='Description for the module',
        label='Description [fr]',
        required=False,
    )


class Highlight(AbstractHighlight):

    class Meta:
        help_text = '''
                    <strong>Highlight module</strong><br>
                    Internal page link and short description.
                    '''
        icon = 'pick'
        template = 'navigation/blocks/highlight.html'


class SecondaryHighlight(AbstractHighlight):

    class Meta:
        help_text = '''
                    <strong>Secondary highlight module</strong><br>
                    Internal page link, short description, and link label.
                    '''
        icon = 'pick'
        template = 'navigation/blocks/secondary_highlight.html'

    link_label_en = CharBlock(
        help_text='Label for the page link button',
        label='Link label [en]',
    )
    link_label_fr = CharBlock(
        help_text='Label for the page link button',
        label='Link label [fr]',
        required=False,
    )