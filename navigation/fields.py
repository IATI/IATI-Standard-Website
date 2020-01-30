from django.utils.safestring import mark_safe
from wagtail.core.fields import StreamField
# from wagtail.images.blocks import ImageChooserBlock
from wagtail.core.blocks import (
    BooleanBlock,
    CharBlock,
    ListBlock,
    PageChooserBlock,
    StaticBlock,
    StreamBlock,
    StructBlock,
    TextBlock,
    # URLBlock,
)
from navigation.values import ModuleStructValue, TransStructValue


class Highlight(StructBlock):

    class Meta:
        help_text = '''
                    <strong>Highlight module</strong><br>
                    Internal page link and short description.
                    '''
        icon = 'pick'
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


class TranslatedPage(StructBlock):

    class Meta:
        icon = 'link'
        label = 'Page'
        value_class = TransStructValue

    page = PageChooserBlock()


class NestedPageGroup(StructBlock):

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
        TranslatedPage(),
        label='Pages',
    )


class NestedPageList(StructBlock):

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


class AbstractModuleType(StructBlock):

    class Meta:
        abstract = True
        icon = 'form'
        form_template = 'navigation/block_forms/custom_struct_container.html'
        form_classname = 'custom-struct-container navigation__meganav struct-block'
        value_class = ModuleStructValue

    highlight = Highlight()

    columns_label = StaticBlock(
        admin_text=mark_safe(
            '''
            <div class="help-block help-info">
                <p>
                    <strong>Columns</strong><br>
                    Column elements for the meganav module.<br>
                    Maximum number of columns: 4
                </p>
            </div>
            '''
        )
    )


class TypeA(AbstractModuleType):

    class Meta:
        help_text = 'Meganav module type a'
        template = 'navigation/blocks/type_a.html'

    columns = StreamBlock(
        [
            ('page_list', PageList()),
            ('nested_page_list', NestedPageList()),
        ],
        min_num=0,
        max_num=4,
        required=False,
    )


def navigation(blank=False):
    required = not blank
    return StreamField(
        StreamBlock(
            [
                ('type_a', TypeA()),
                # ('type_b', TypeB()),
            ],
            max_num=1,
            required=required,
        ),
        blank=blank
    )
