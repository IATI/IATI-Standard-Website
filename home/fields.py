from django.db import models
from common.utils import ForeignKeyField


class HomeFieldsMixin(models.Model):
    class Meta:
        abstract = True

    use_legacy_template = models.BooleanField(
        blank=True,
        default=True,
        help_text='Use the legacy template with hard-coded text for front end display?',
    )
    header_video = models.URLField(
        max_length=255,
        blank=True,
        help_text='Optional: video embed URL for page header',
    )
    testimonial = ForeignKeyField(
        model='testimonials.Testimonial',
        required=True,
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
        help_text='Video embed URL for the about IATI section',
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
    iati_tools_title_description = models.TextField(
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
