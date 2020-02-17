from modelcluster.fields import ParentalKey
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.core.models import Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from common.utils import ForeignKeyField, WagtailImageField


class BaseRelatedPageItem(models.Model):
    class Meta:
        abstract = True

    page = ForeignKeyField(
        model='wagtailcore.Page',
        required=True,
        on_delete=models.CASCADE,
        help_text='Page link for the item'
    )


class BaseRelatedItem(BaseRelatedPageItem):
    class Meta:
        abstract = True

    title = models.CharField(
        max_length=255,
        help_text='Title for the item',
    )
    description = models.CharField(
        max_length=255,
        help_text='Description for the item',
    )
    image = WagtailImageField(
        required=True,
        help_text='Image for the item'
    )


class GettingStartedItem(BaseRelatedItem):
    class Meta:
        abstract = True

    link_label = models.CharField(
        max_length=255,
        help_text='Link label for the item',
    )


class GettingStartedItems(Orderable, GettingStartedItem):
    item = ParentalKey('HomePage', related_name='getting_started_items')

    title_required = True

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


class BaseRelatedOptionalItem(BaseRelatedPageItem):
    class Meta:
        abstract = True

    title = models.CharField(
        max_length=255,
        blank=True,
        help_text='Optional: title for the item. Defaults to the selected page title if left blank',
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        help_text='Optional: description for the item. Defaults to the selected page excerpt if left blank',
    )


class IATIInActionFeaturedItem(BaseRelatedOptionalItem):
    class Meta:
        abstract = True

    image = WagtailImageField(
        required=False,
        help_text='Optional: image for the item. Defaults to the selected page image if left blank'
    )
    quote = models.CharField(
        max_length=255,
        blank=True,
        help_text='Optional: quote for the item',
    )
    quotee = models.CharField(
        max_length=255,
        blank=True,
        help_text='Optional: the source of the quote',
    )


class IATIInActionFeaturedItems(Orderable, IATIInActionFeaturedItem):
    item = ParentalKey('HomePage', related_name='iati_in_action_featured_item')

    translation_fields = [
        'title',
        'description',
        'quote',
        'quotee',
    ]

    panels = [
        PageChooserPanel('page'),
        ImageChooserPanel('image'),
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('quote'),
        FieldPanel('quotee'),
    ]


class IATIInActionItems(Orderable, BaseRelatedOptionalItem):
    item = ParentalKey('HomePage', related_name='iati_in_action_items')

    translation_fields = [
        'title',
        'description',
    ]

    panels = [
        PageChooserPanel('page'),
        FieldPanel('title'),
        FieldPanel('description'),
    ]
