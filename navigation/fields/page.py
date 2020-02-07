"""Module for a translated page class."""

from wagtail.core.blocks import (
    PageChooserBlock,
    StructBlock,
)
from navigation.values import TransStructValue


class TranslatedPage(StructBlock):
    """Class for a translated page outside of t he Django Modeltranslation framework."""

    class Meta:
        icon = 'link'
        label = 'Page'
        value_class = TransStructValue

    page = PageChooserBlock()
