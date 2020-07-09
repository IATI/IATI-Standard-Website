"""Module for registering admin models for the iati_standard app."""

from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register
)
from iati_standard.models import ReferenceMenu


class ReferenceMenuAdmin(ModelAdmin):
    """Admin model for news pages."""

    model = ReferenceMenu
    menu_icon = 'doc-full'
    menu_order = 145
    menu_label = 'Reference Menu'
    list_display = ('tag', 'menu_type', )
    search_fields = ('tag', )


modeladmin_register(ReferenceMenuAdmin)
