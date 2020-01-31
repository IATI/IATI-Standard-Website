from wagtail.core.blocks import (
    PageChooserBlock,
    StructBlock,
    TextBlock,
)


class AbstractHighlight(StructBlock):

    class Meta:
        abstract = True
        icon = 'pick'
        form_template = 'navigation/block_forms/custom_struct.html'

    page = PageChooserBlock(
        help_text='Page for title and link'
    )
    description = TextBlock(
        help_text='Description for the module',
        label='Description',
    )


class Highlight(AbstractHighlight):

    class Meta:
        help_text = '''
                    <strong>Highlight module</strong><br>
                    Internal page link and short description.
                    '''
        icon = 'pick'
        template = 'navigation/blocks/highlight.html'
