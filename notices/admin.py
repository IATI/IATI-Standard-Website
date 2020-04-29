"""Module for registering admin models for the notices app."""

from django.utils.html import strip_tags
from wagtail.contrib.modeladmin.helpers import PermissionHelper
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register
)
from notices.models import GlobalNotice, PageNotice


class GlobalNoticePermissionHelper(PermissionHelper):
    """Permission helper for global notices."""

    def user_can_create(self, user):
        """Hide the "Add" button when there is already an instance."""
        num_objects = self.model.objects.count()
        if num_objects >= 1:
            return False
        return super().user_can_create(user)


def content(obj):
    """Strip HTML tags for list display."""
    return strip_tags(obj.content.replace('</', ' </'))


class GlobalNoticeAdmin(ModelAdmin):
    """Admin model for global notices."""

    model = GlobalNotice
    menu_icon = 'site'
    menu_order = 100
    menu_label = 'Global notice'
    list_display = (content, 'notice_type', 'uuid', )
    permission_helper_class = GlobalNoticePermissionHelper


class PageNoticeAdmin(ModelAdmin):
    """Admin model for page notices."""

    model = PageNotice
    menu_icon = 'help'
    menu_order = 110
    menu_label = 'Page notices'
    list_display = ('page', 'display_location', 'uuid', 'notice_type', 'allow_dismiss', content, )
    search_fields = ('content', )


class NoticesAdminGroup(ModelAdminGroup):
    """Admin model group for notices."""

    menu_label = 'Notices'
    menu_icon = 'help'
    menu_order = 135
    items = (GlobalNoticeAdmin, PageNoticeAdmin, )


modeladmin_register(NoticesAdminGroup)
