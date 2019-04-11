from django.contrib.syndication.views import Feed
from django.utils.translation import gettext_lazy as _

from news.models import NewsPage


class LatestEntriesFeed(Feed):
    title = _("IATI - International Aid Transparency Initiative")
    description = _("")
    link = "/en/feed/"

    def items(self):
        return NewsPage.objects.live().order_by('-date')

    def item_title(self, item):
        return item.heading

    def item_description(self, item):
        return item.excerpt

    def item_link(self, item):
        return item.get_url()
