import datetime
from django import forms
from django.db import models
from django.utils.text import slugify
from modelcluster.fields import ParentalManyToManyField, ParentalKey
from wagtail.core.models import Orderable
from wagtail.snippets.models import register_snippet
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from home.models import AbstractIndexPage, AbstractContentPage


class NewsIndexPage(AbstractIndexPage):
    """A model for news index pages, the main news landing page."""
    parent_page_types = ['home.HomePage']
    subpage_types = ['news.NewsPage']

    @property
    def news_categories(self):
        """A function to list all of the news categories"""
        news_categories = NewsCategory.objects.all()
        return news_categories

    def get_context(self, request):
        """Overwriting the default wagtail get_context function to allow for filtering based on params, including pagination.
        Use the functions built into the abstract index page class to dynamically filter the child pages and apply pagination, limiting the results to 3 per page.
        """
        filter_dict = {}
        children = NewsPage.objects.live().descendant_of(self).order_by('-date')

        news_category = request.GET.get('type')
        if news_category:
            filter_dict["news_categories__slug"] = news_category

        filtered_children = self.filter_children(children, filter_dict)
        paginated_children = self.paginate(request, filtered_children, 3)
        context = super(NewsIndexPage, self).get_context(request)
        context['news_posts'] = paginated_children
        return context


class NewsPage(AbstractContentPage):
    """A model for news single pages"""
    parent_page_types = ['news.NewsIndexPage']
    subpage_types = []

    date = models.DateField("News date", default=datetime.date.today)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    news_categories = ParentalManyToManyField('news.NewsCategory', blank=True)

    multilingual_field_panels = [
        FieldPanel('date'),
        FieldPanel('news_categories', widget=forms.CheckboxSelectMultiple),
        ImageChooserPanel('feed_image'),
        InlinePanel('related_news', label="Related news", help_text="Looks best with two related news posts or fewer.")

    ]


@register_snippet
class NewsCategory(models.Model):
    """A snippet model for news categories, to be added in the snippet menu prior to creating news posts for uniformity."""
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        """Display the category name in the CMS rather than the class."""
        return self.name

    class Meta(object):
        """Change verbose name for correct pluralization"""
        verbose_name_plural = "news categories"


    def full_clean(self, *args, **kwargs):
        """Apply fixups that need to happen before per-field validation occurs"""
        base_slug = slugify(self.name, allow_unicode=True)
        if base_slug:
            self.slug = base_slug
        super(NewsCategory, self).full_clean(*args, **kwargs)

    translation_fields = [
        'name',
    ]

    panels = [
        FieldPanel('name'),
    ]


class RelatedNews(Orderable):
    """A model for related news items."""

    page = ParentalKey(NewsPage, related_name='related_news')
    related_post = models.ForeignKey(
        'news.NewsPage',
        on_delete=models.CASCADE,
        related_name='+'
    )

    panels = [
        PageChooserPanel('related_post', 'news.NewsPage'),
    ]
