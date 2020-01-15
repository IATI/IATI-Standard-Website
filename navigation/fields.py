from wagtail.core.fields import StreamField
# from wagtail.images.blocks import ImageChooserBlock
from wagtail.core.blocks import (
    # CharBlock,
    ListBlock,
    # StreamBlock,
    StructBlock,
    TextBlock,
    # URLBlock,
    PageChooserBlock,
)


class Highlight(StructBlock):

    class Meta:
        help_text = 'Highlight module.'
        icon = 'pick'
        label = 'Highlight'

    page = PageChooserBlock(
        help_text='Highlighted page'
    )
    description = TextBlock(
        help_text='Description for the highlight module'
    )

    translation_fields = [
        'description',
    ]


class PageList(StructBlock):

    class Meta:
        help_text = 'Simple page list.'
        icon = 'list-ul'
        label = 'Page list'

    pages = ListBlock(
        PageChooserBlock(label='Page')
    )


class TypeA(StructBlock):

    class Meta:
        help_text = 'Primary navigation module type A.'
        icon = 'form'
        label = 'Type A'
        template = 'navigation/blocks/type_a.html'

    highlight = Highlight(
        help_text='Highlight block for meganav'
    )
    meganav = ListBlock(
        PageList(label='Page list')
    )


def navigation(blank=False):
    return StreamField([
        ('type_a', TypeA()),
    ], blank=blank)
