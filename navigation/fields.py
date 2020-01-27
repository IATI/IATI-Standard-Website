from wagtail.core.fields import StreamField
# from wagtail.images.blocks import ImageChooserBlock
from wagtail.core.blocks import (
    BooleanBlock,
    CharBlock,
    ListBlock,
    PageChooserBlock,
    StreamBlock,
    StructBlock,
    TextBlock,
    # URLBlock,
)
from navigation.values import TransStructValue


class Highlight(StructBlock):

    class Meta:
        icon = 'pick'
        label = 'Highlight'
        form_template = 'navigation/block_forms/custom_struct.html'
        template = 'navigation/blocks/highlight.html'
        value_class = TransStructValue

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
        help_text = '''
                    <strong>List of internal page links.</strong><br>
                    Optional: select the first page link to use as a title, or add a plain text title.<br>
                    Optional: short description.
                    '''
        icon = 'list-ul'
        label = 'Page list'
        form_template = 'navigation/block_forms/custom_struct.html'

    use_first_page_as_title = BooleanBlock(
        help_text='Optional: if checked, the first page in the list will be displayed as a title',
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
        PageChooserBlock(
            label='Page',
            icon='link',
        )
    )


class TypeA(StructBlock):

    class Meta:
        help_text = 'Primary navigation module type A.'
        icon = 'form'
        label = 'Type A'
        form_template = 'navigation/block_forms/custom_struct_container.html'
        form_classname = 'custom-struct-container navigation__meganav'
        template = 'navigation/blocks/type_a.html'

    highlight = Highlight(
        help_text='''
                  <strong>Highlight module.</strong><br>
                  Internal page link and short description.
                  '''
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
