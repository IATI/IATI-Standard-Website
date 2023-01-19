from modelcluster.fields import ParentalKey
from django.db import models
from wagtail.admin.panels import FieldPanel, PageChooserPanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from common.utils import ForeignKeyField, WagtailImageField


class GetInvolvedItem(models.Model):
    """Abstract class for get involved item."""

    class Meta:
        abstract = True

    title = models.CharField(
        max_length=255,
        help_text='Title for the item',
    )
    image = WagtailImageField(
        required=False,
        help_text='Optional: image for the item'
    )
    description = RichTextField(
        help_text='Description for the item',
        features=['link', 'ul'],
    )
    page = ForeignKeyField(
        model='wagtailcore.Page',
        required=False,
        on_delete=models.CASCADE,
        help_text='Optional: page link for the item'
    )
    link_label = models.CharField(
        blank=True,
        max_length=255,
        help_text='Optional: link label for the item',
    )


class GetInvolvedItems(Orderable, GetInvolvedItem):
    """Concrete clustrable model class for get involved items."""

    item = ParentalKey('GetInvolvedPage', related_name='get_involved_items')

    translation_fields = [
        'title',
        'description',
        'link_label',
    ]

    panels = [
        FieldPanel('title'),
        ImageChooserPanel('image'),
        FieldPanel('description'),
        PageChooserPanel('page'),
        FieldPanel('link_label'),
    ]
