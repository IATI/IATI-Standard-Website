from modelcluster.fields import ParentalKey
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.core.models import Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from common.utils import ForeignKeyField, WagtailImageField


class DynamicOptionalFieldPanel(FieldPanel):
    '''
    By default, this field will be required.
    If the concrete class field should be optional, then add the following to the class definition:
    [field]_required = False
    '''

    def on_form_bound(self):
        name = self.field_name
        required = getattr(self.model, '%s_required' % name, True)
        self.form.fields[name].required = required
        super().on_form_bound()


class DynamicOptionalImageChooserPanel(ImageChooserPanel):
    '''
    By default, this field will be required.
    If the concrete class field should be optional, then add the following to the class definition:
    [field]_required = False
    '''

    def on_form_bound(self):
        name = self.field_name
        required = getattr(self.model, '%s_required' % name, True)
        self.form.fields[name].required = required
        super().on_form_bound()


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


class BaseRelatedImageItem(BaseRelatedItem):
    class Meta:
        abstract = True

    image = WagtailImageField(
        required=True,
        help_text='Image for the item'
    )


class GettingStartedItem(BaseRelatedImageItem):
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
        DynamicOptionalFieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('link_label'),
    ]


class IATIInActionFeaturedItem(BaseRelatedImageItem):
    class Meta:
        abstract = True

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

    title_required = False
    description_required = False
    image_required = False

    translation_fields = [
        'title',
        'description',
        'quote',
        'quotee',
    ]

    panels = [
        PageChooserPanel('page'),
        ImageChooserPanel('image'),
        DynamicOptionalFieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('quote'),
        FieldPanel('quotee'),
    ]
