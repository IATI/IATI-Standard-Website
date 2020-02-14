from modelcluster.fields import ParentalKey
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.core.models import Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from common.utils import ForeignKeyField, WagtailImageField


class GettingStartedItem(models.Model):
    class Meta:
        abstract = True

    page = ForeignKeyField(
        model='wagtailcore.Page',
        required=True,
        on_delete=models.CASCADE,
    )
    image = WagtailImageField(
        required=True,
        help_text='Image for the getting started item'
    )
    title = models.CharField(
        max_length=255,
        help_text='Title for the getting started item',
    )
    description = models.CharField(
        max_length=255,
        help_text='Description for the getting started item',
    )
    link_label = models.CharField(
        max_length=255,
        help_text='Link label for the getting started item',
    )


class GettingStartedItems(Orderable, GettingStartedItem):
    item = ParentalKey('HomePage', related_name='getting_started_items')

    translation_fields = [
        'title',
        'description',
        'link_label',
    ]

    panels = [
        PageChooserPanel('page'),
        ImageChooserPanel('image'),
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('link_label'),
    ]
