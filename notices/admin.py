"""Module for registering admin models for the notices app."""

from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register
)
from notices.models import GlobalNotice, PageNotice


class GlobalNoticeAdmin(ModelAdmin):
    """Admin model for global notices."""

    model = GlobalNotice
    menu_icon = 'site'
    menu_order = 100
    menu_label = 'Global notices'
    list_display = ('content', )
    search_fields = ('content', )


class PageNoticeAdmin(ModelAdmin):
    """Admin model for page notices."""

    model = PageNotice
    menu_icon = 'help'
    menu_order = 110
    menu_label = 'Page notices'
    list_display = ('content', )
    search_fields = ('content', )


class NoticesAdminGroup(ModelAdminGroup):
    """Admin model group for notices."""

    menu_label = 'Notices'
    menu_icon = 'help'
    menu_order = 135
    items = (GlobalNoticeAdmin, PageNoticeAdmin, )


modeladmin_register(NoticesAdminGroup)
