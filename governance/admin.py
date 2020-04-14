"""Module for registering admin models for the governance app."""

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from import_export.widgets import (
    CharWidget,
    ForeignKeyWidget,
    DateWidget
)
from django.contrib import admin
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register
)
from wagtail.images import get_image_model
from common.helpers import get_or_create_image
from governance.models import Member
from taxonomies.models import Constituency
from taxonomies.utils import get_or_create_term


class MemberAdmin(ModelAdmin):
    model = Member
    menu_icon = 'user'
    menu_order = 100
    menu_label = 'Members'
    list_display = ('name', 'constituency', 'url', 'date_joined', 'active', )
    search_fields = ('name', 'url', )


class ConstituencyAdmin(ModelAdmin):
    model = Constituency
    menu_icon = 'tag'
    menu_order = 110
    menu_label = 'Constituencies'
    list_display = ('title', 'slug', )
    search_fields = ('title', 'slug', )


class MembersAdminGroup(ModelAdminGroup):
    menu_label = 'Members'
    menu_icon = 'user'
    menu_order = 120
    items = (MemberAdmin, ConstituencyAdmin, )


modeladmin_register(MembersAdminGroup)


class TextWidget(CharWidget):
    """An overriden widget for text import."""

    def clean(self, value, row=None):
        """Override the clean method."""
        value = '' if not value else value

        return super(CharWidget, self).clean(value)


class SingleTermWidget(ForeignKeyWidget):
    """An overriden widget for foreign key import."""

    def clean(self, value, row=None):
        """Override the clean method."""
        stripped_value = value.replace('\n', '')
        if stripped_value:
            term = get_or_create_term(self.model, stripped_value)
            return super(ForeignKeyWidget, self).clean(term)

        return None


class SingleTermWidgetFR(ForeignKeyWidget):
    """An overriden widget for French foreign key import."""

    def clean(self, value, row=None):
        """Override the clean method."""
        stripped_value = value.replace('\n', '')
        stripped_value_en = row[self.field].replace('\n', '')
        if stripped_value and stripped_value_en:
            term = get_or_create_term(self.model, stripped_value_en)
            term.title_fr = stripped_value
            term.save()
            return super(ForeignKeyWidget, self).clean(term)

        return None


class ImageWidget(ForeignKeyWidget):
    """An overriden widget for foreign key import."""

    def clean(self, value, row=None):
        """Override the clean method."""
        stripped_value = value.replace('\n', '')
        image_type = 'flag' if 'country' in row['constituency'].lower() else 'logo'
        title = '%s %s' % (row['name'], image_type)
        if stripped_value:
            base_url = 'https://dev.iatistandard.org/media/member-logos/'
            url = '%s%s' % (base_url, stripped_value)
            image = get_or_create_image(url, title)
            return super(ForeignKeyWidget, self).clean(image)

        return None


class MemberResource(resources.ModelResource):
    """A resource class for importing data to the Member class."""

    class Meta:
        import_id_fields = ['id']
        model = Member

    name = Field(
        attribute='name',
        column_name='name',
        widget=TextWidget(),
    )
    name_fr = Field(
        attribute='name_fr',
        column_name='name_fr',
        widget=TextWidget(),
    )
    url = Field(
        attribute='url',
        column_name='url',
        widget=TextWidget(),
    )
    date_joined = Field(
        attribute='date_joined',
        column_name='date_joined',
        widget=DateWidget(format='%Y'),
    )
    constituency = Field(
        attribute='constituency',
        column_name='constituency',
        widget=SingleTermWidget(
            Constituency
        ),
    )
    constituency_fr = Field(
        attribute='constituency_fr',
        column_name='constituency_fr',
        widget=SingleTermWidgetFR(
            Constituency,
            'constituency'
        ),
    )
    image = Field(
        attribute='image',
        column_name='image',
        widget=ImageWidget(
            get_image_model()
        ),
    )


class MemberResourceResourceDjangoAdmin(ImportExportModelAdmin):
    """A Django admin class to represent the resource class."""

    resource_class = MemberResource


admin.site.register(Member, MemberResourceResourceDjangoAdmin)
