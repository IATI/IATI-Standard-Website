from wagtail.core.blocks import (
    PageChooserBlock,
    StructBlock,
)
from navigation.values import TransStructValue


class TranslatedPage(StructBlock):

    class Meta:
        icon = 'link'
        label = 'Page'
        value_class = TransStructValue

    page = PageChooserBlock()
