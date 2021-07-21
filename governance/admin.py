"""Module for registering admin models for the governance app."""

from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register
)
from governance.models import Member
from taxonomies.models import Constituency
from governance.resources import MemberResource


class MemberAdmin(ModelAdmin):
    """Admin model for members."""

    model = Member
    menu_icon = 'user'
    menu_order = 100
    menu_label = 'Members'
    list_display = ('name', 'constituency', 'url', 'date_joined', 'active', )
    search_fields = ('name', 'url', )


class ConstituencyAdmin(ModelAdmin):
    """Admin model for constituencies."""

    model = Constituency
    menu_icon = 'tag'
    menu_order = 110
    menu_label = 'Constituencies'
    list_display = ('title', 'slug', )
    search_fields = ('title', 'slug', )


class MembersAdminGroup(ModelAdminGroup):
    """Admin model group for members."""

    menu_label = 'Members'
    menu_icon = 'user'
    menu_order = 120
    items = (MemberAdmin, ConstituencyAdmin, )


modeladmin_register(MembersAdminGroup)


class MemberResourceResourceDjangoAdmin(ImportExportModelAdmin):
    """A Django admin class to represent the resource class."""

    resource_class = MemberResource


admin.site.register(Member, MemberResourceResourceDjangoAdmin)
