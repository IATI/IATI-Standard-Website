"""Module for Django Import Export resources."""

from import_export import resources
from import_export.fields import Field
from import_export.widgets import (
    CharWidget,
    ForeignKeyWidget,
    DateWidget
)
from wagtail.images import get_image_model
from common.helpers import get_or_create_image
from django.apps import apps
from taxonomies.models import Constituency
from taxonomies.utils import get_or_create_term

Member = apps.get_model('governance', 'Member')


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

    def export(self, queryset=None, *args, **kwargs):
        """Override export method to filter by active."""
        queryset = queryset and queryset.filter(active=True)
        return super(MemberResource, self).export(queryset, *args, **kwargs)

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
