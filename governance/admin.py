from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from import_export.widgets import (
    CharWidget,
    ForeignKeyWidget,
    DateWidget
)
from django.contrib import admin
from governance.models import Member
from taxonomies.models import Constituency
from taxonomies.utils import get_or_create_term


class TextWidget(CharWidget):
    def clean(self, value, row=None):
        value = '' if not value else value

        return super(CharWidget, self).clean(value)


class SingleTermWidget(ForeignKeyWidget):
    def clean(self, value, row=None):
        stripped_value = value.replace('\n', '')
        if stripped_value:
            term = get_or_create_term(self.model, stripped_value)
            return super(ForeignKeyWidget, self).clean(term)

        return None


class SingleTermWidgetFR(ForeignKeyWidget):
    def clean(self, value, row=None):
        stripped_value = value.replace('\n', '')
        stripped_value_en = row[self.field].replace('\n', '')
        if stripped_value and stripped_value_en:
            term = get_or_create_term(self.model, stripped_value_en)
            term.title_fr = stripped_value
            term.save()
            return super(ForeignKeyWidget, self).clean(term)

        return None


class MemberResource(resources.ModelResource):

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


class MemberResourceResourceDjangoAdmin(ImportExportModelAdmin):
    resource_class = MemberResource


admin.site.register(Member, MemberResourceResourceDjangoAdmin)
