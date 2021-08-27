from modelcluster.fields import ParentalKey
from django.db import models
from django.utils.functional import cached_property
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.core.models import Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from common.utils import ForeignKeyField, WagtailImageField


class TestimonialItem(models.Model):
    """Abstract class for testimonial item."""

    class Meta:
        abstract = True

    testimonial = ForeignKeyField(
        model='testimonials.Testimonial',
        required=True,
        on_delete=models.CASCADE,
    )


class TestimonialItems(Orderable, TestimonialItem):
    """Concrete clustrable model class for testimonial items."""

    item = ParentalKey('HomePage', related_name='testimonial_items')

    panels = [
        SnippetChooserPanel('testimonial'),
    ]


class BaseRelatedPageItem(models.Model):
    """Abstract class for related page."""

    class Meta:
        abstract = True

    page = ForeignKeyField(
        model='wagtailcore.Page',
        required=True,
        on_delete=models.CASCADE,
        help_text='Page link for the item'
    )


class BaseRelatedItem(BaseRelatedPageItem):
    """Abstract class inheriting from BaseRelatedPageItem with extra info."""

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
    """Abstract class inheriting from BaseRelatedItem with extra link label."""

    class Meta:
        abstract = True

    link_label = models.CharField(
        max_length=255,
        help_text='Link label for the item',
    )


class GettingStartedItems(Orderable, GettingStartedItem):
    """Concrete clustrable model class for getting started items."""

    item = ParentalKey('HomePage', related_name='getting_started_items')

    panels = [
        PageChooserPanel('page'),
        ImageChooserPanel('image'),
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('link_label'),
    ]


class BaseRelatedOptionalItem(BaseRelatedPageItem):
    """Abstract class inheriting from BaseRelatedPageItem with optional extra info."""

    class Meta:
        abstract = True

    title = models.CharField(
        max_length=255,
        blank=True,
        help_text='Optional: title for the item. Defaults to the selected page title if left blank',
    )
    description = models.CharField(
        max_length=500,
        blank=True,
        help_text='Optional: description for the item. Defaults to the selected page excerpt if left blank',
    )

    @cached_property
    def get_title(self):
        """Get the title from the instance, or fall back to the selected page heading."""
        title = self.title
        if not title:
            title = self.page.specific.heading

        return title

    @cached_property
    def get_description(self):
        """Get the description from the instance, or fall back to the selected page excerpt."""
        description = self.description
        if not description:
            description = getattr(self.page.specific, 'excerpt', None)

        return description


class IATIInActionFeaturedItem(BaseRelatedOptionalItem):
    """Abstract class inheriting from BaseRelatedOptionalItem with optional image and testimonial fields."""

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

    @cached_property
    def get_image(self):
        """Get the image from the instance, or fall back to the selected page feed or header image."""
        image = self.image
        if not image:
            image = getattr(self.page.specific, 'feed_image', None)
        if not image:
            image = getattr(self.page.specific, 'header_image', None)

        return image


class IATIInActionFeaturedItems(Orderable, IATIInActionFeaturedItem):
    """Concrete clustrable model class for IATI in action featured items."""

    item = ParentalKey('HomePage', related_name='iati_in_action_featured_item')

    panels = [
        PageChooserPanel('page'),
        ImageChooserPanel('image'),
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('quote'),
        FieldPanel('quotee'),
    ]


class IATIInActionItems(Orderable, BaseRelatedOptionalItem):
    """Concrete clustrable model class for IATI in action items."""

    item = ParentalKey('HomePage', related_name='iati_in_action_items')

    panels = [
        PageChooserPanel('page'),
        FieldPanel('title'),
        FieldPanel('description'),
    ]


class IATIToolsItems(Orderable, BaseRelatedPageItem):
    """Concrete clustrable model class for IATI tools items."""

    item = ParentalKey('HomePage', related_name='iati_tools_items')

    panels = [
        PageChooserPanel('page'),
    ]


class LatestNewsItems(Orderable, BaseRelatedPageItem):
    """Concrete clustrable model class for latest news items."""

    item = ParentalKey('HomePage', related_name='latest_news_items')

    panels = [
        PageChooserPanel('page', 'news.NewsPage'),
    ]
