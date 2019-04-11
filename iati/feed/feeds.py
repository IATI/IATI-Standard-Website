from django.contrib.syndication.views import Feed
from django.utils.translation import gettext_lazy as _

from news.models import NewsPage


class LatestEntriesFeed(Feed):
    """Class for the RSS news feed."""

    title = _("IATI - International Aid Transparency Initiative")
    description = _("")
    link = "/en/feed/"

    def items(self):
        """Return an iterable of feed items."""
        return NewsPage.objects.live().order_by('-date')

    def item_title(self, item):
        """Return the feed item title."""
        return item.heading

    def item_description(self, item):
        """Return the feed item description."""
        return item.excerpt

    def item_link(self, item):
        """Return the link to the feed item."""
        return item.get_url()
