from django.utils.safestring import mark_safe
from wagtail.core.blocks import (
    StaticBlock,
    StreamBlock,
    StructBlock,
)
from navigation.fields import (
    Featured,
    FocusItem,
    Highlight,
    NestedPageList,
    PageList,
)
from navigation.values import ModuleStructValue


class AbstractModuleType(StructBlock):

    class Meta:
        abstract = True
        icon = 'form'
        form_template = 'navigation/block_forms/custom_struct_container.html'
        form_classname = 'custom-struct-container navigation__meganav struct-block'
        value_class = ModuleStructValue

    highlight = Highlight()


class TypeA(AbstractModuleType):

    class Meta:
        help_text = 'Meganav module type a'
        template = 'navigation/blocks/type_a.html'

    columns_label = StaticBlock(
        admin_text=mark_safe(
            '''
            <div class="help-block help-info">
                <p>
                    <strong>Columns</strong><br>
                    Column elements for the meganav module.<br>
                    Maximum number of items: 4
                </p>
            </div>
            '''
        )
    )
    columns = StreamBlock(
        [
            ('page_list', PageList()),
            ('nested_page_list', NestedPageList()),
        ],
        min_num=0,
        max_num=4,
        required=False,
    )


class TypeB(AbstractModuleType):

    class Meta:
        help_text = 'Meganav module type b'
        template = 'navigation/blocks/type_b.html'

    columns_label = StaticBlock(
        admin_text=mark_safe(
            '''
            <div class="help-block help-info">
                <p>
                    <strong>Columns</strong><br>
                    Column elements for the meganav module.<br>
                    Maximum number of items: 2
                </p>
            </div>
            '''
        )
    )
    columns = StreamBlock(
        [
            ('page_list', PageList()),
            ('featured', Featured()),
        ],
        min_num=0,
        max_num=2,
        required=False,
        block_counts={
            'page_list': {
                'max_num': 1
            },
            'featured': {
                'max_num': 1
            }
        },
    )


class TypeC(AbstractModuleType):

    class Meta:
        help_text = 'Meganav module type c'
        template = 'navigation/blocks/type_c.html'

    columns_label = StaticBlock(
        admin_text=mark_safe(
            '''
            <div class="help-block help-info">
                <p>
                    <strong>Columns</strong><br>
                    Column elements for the meganav module.<br>
                    Maximum number of items: 7
                </p>
            </div>
            '''
        )
    )
    columns = StreamBlock(
        [
            ('focus_item', FocusItem()),
            ('page_list', PageList()),
        ],
        min_num=0,
        max_num=2,
        required=False,
    )
