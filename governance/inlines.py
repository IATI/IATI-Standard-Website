from modelcluster.fields import ParentalKey
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.models import Orderable
from common.utils import WagtailImageField


class ChairItem(models.Model):
    """Abstract class for chair item."""

    class Meta:
        abstract = True

    name = models.CharField(
        max_length=255,
        help_text='Name of the chair',
    )
    image = WagtailImageField(
        required=False,
        help_text='Optional: image for the chair'
    )
    bio = models.CharField(
        max_length=255,
        help_text='Short bio for the chair',
    )

    translation_fields = [
        'name',
        'bio',
    ]


class ChairItems(Orderable, ChairItem):
    """Concrete clustrable model class for chair items."""

    item = ParentalKey('MembersAssemblyPage', related_name='chair_items')

    panels = [
        FieldPanel('name'),
        FieldPanel('image'),
        FieldPanel('bio'),
    ]


class ViceChairItems(Orderable, ChairItem):
    """Concrete clustrable model class for vice chair items."""

    item = ParentalKey('MembersAssemblyPage', related_name='vice_chair_items')

    panels = [
        FieldPanel('name'),
        FieldPanel('image'),
        FieldPanel('bio'),
    ]
