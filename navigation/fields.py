from wagtail.core.fields import StreamField
# from wagtail.images.blocks import ImageChooserBlock
from wagtail.core.blocks import (
    # CharBlock,
    ListBlock,
    StreamBlock,
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
        form_template = 'navigation/block_forms/custom_struct.html'

    page = PageChooserBlock(
        help_text='Highlighted page'
    )
    description_en = TextBlock(
        help_text='Description for the highlight module',
        label='Description [en]',
    )
    description_fr = TextBlock(
        help_text='Description for the highlight module',
        label='Description [fr]',
        required=False,
    )


class PageList(StructBlock):

    class Meta:
        help_text = 'Simple page list.'
        icon = 'list-ul'
        label = 'Page list'
        form_template = 'navigation/block_forms/custom_struct.html'

    pages = ListBlock(
        PageChooserBlock(label='Page')
    )


class TypeA(StructBlock):

    class Meta:
        help_text = 'Primary navigation module type A.'
        icon = 'form'
        label = 'Type A'
        form_template = 'navigation/block_forms/custom_struct_container.html'
        form_classname = 'navigation__meganav'
        template = 'navigation/blocks/type_a.html'

    highlight = Highlight(
        help_text='Highlight block for meganav'
    )
    meganav = ListBlock(
        PageList(label='Page list')
    )


def navigation(blank=False):
    return StreamField(
        StreamBlock(
            [
                ('type_a', TypeA()),
            ],
            max_num=1,
        ),
        blank=blank
    )
