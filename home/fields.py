from django.db import models
from django.utils.functional import cached_property
from common.utils import ForeignKeyField, get_selected_or_fallback


class HomeFieldsMixin(models.Model):
    """Abstract mixin class for the home page db fields."""

    class Meta:
        abstract = True

    header_video = models.URLField(
        max_length=255,
        blank=True,
        help_text='Optional: video embed URL for page header',
    )
    activities_description = models.CharField(
        max_length=255,
        help_text='Description for the activities statistics section',
    )
    organisations_description = models.CharField(
        max_length=255,
        help_text='Description for the organisations statistics section',
    )
    getting_started_title = models.CharField(
        max_length=255,
        help_text='Title for the getting started section',
    )
    about_iati_title = models.CharField(
        max_length=255,
        help_text='Title for the about IATI section',
    )
    about_iati_description = models.TextField(
        help_text='Description for the about IATI section',
    )
    about_iati_video = models.URLField(
        max_length=255,
        blank=True,
        help_text='Optional: video embed URL for the about IATI section',
    )
    about_iati_page = ForeignKeyField(
        model='wagtailcore.Page',
        required=True,
    )
    about_iati_link_label = models.CharField(
        max_length=255,
        help_text='Link label for the about IATI section',
    )
    iati_in_action_title = models.CharField(
        max_length=255,
        help_text='Title for the IATI in action section',
    )
    iati_in_action_description = models.TextField(
        blank=True,
        help_text='Optional: description for the IATI in action section',
    )
    iati_tools_title = models.CharField(
        max_length=255,
        help_text='Title for the IATI tools section',
    )
    iati_tools_description = models.TextField(
        blank=True,
        help_text='Optional: description for the IATI tools section',
    )
    latest_news_title = models.CharField(
        max_length=255,
        help_text='Title for the latest new section',
    )
    latest_news_link_label = models.CharField(
        max_length=255,
        help_text='Label for the view all news button',
    )
    latest_news_tweets_title = models.CharField(
        max_length=255,
        help_text='Title for the latest news Twitter section',
    )

    @cached_property
    def testimonial(self):
        """Get and return a random testomional or none if there is an error."""
        try:
            return self.testimonial_items.all().order_by('?').first().testimonial
        except AttributeError:
            return None

    @cached_property
    def getting_started(self):
        """Create and return a list of getting started items, added to list if the page is live."""
        return [x for x in self.getting_started_items.all() if x.page.live]

    @cached_property
    def iati_in_action_featured(self):
        """Get and return the first IATI in action featured item, if the page is live."""
        featured = self.iati_in_action_featured_item.all().first()
        return featured if featured.page.live else None

    @cached_property
    def iati_in_action(self):
        """Create and return a list of IATI in action items, added to list if the page is live."""
        return [x for x in self.iati_in_action_items.all() if x.page.live]

    @cached_property
    def tools(self):
        """Create and return a list of IATI tools items, added to list if the page is live."""
        return [x.page.specific for x in self.iati_tools_items.all() if x.page.live]

    @cached_property
    def news_index(self):
        """Create and return the first live news index page."""
        from news.models import NewsIndexPage
        return NewsIndexPage.objects.live().first()

    @cached_property
    def selected_news(self):
        """Create and return a list of selected latest news items, added to list if the page is live."""
        return [x.page.specific for x in self.latest_news_items.all() if x.page.live]

    @cached_property
    def news(self):
        """Return a list of news items using get selected or fallback."""
        from news.models import NewsPage
        return get_selected_or_fallback(
            selected=self.selected_news,
            fallback=NewsPage.objects,
            max_length=3,
            order='-date',
        )
