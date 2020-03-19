"""Model definitions for the iati_standard app."""

from bs4 import BeautifulSoup

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.functional import cached_property

from wagtail.snippets.models import register_snippet

from home.models import AbstractContentPage, DefaultPageHeaderImageMixin

from iati_standard.panels import ReferenceDataPanel


class IATIStandardPage(DefaultPageHeaderImageMixin, AbstractContentPage):
    """A model for the IATI Standard Page, a landing page for IATI reference."""

    parent_page_types = ['home.HomePage']
    subpage_types = []

    max_count = 1

    repo = models.URLField(
        help_text='Git repo URL',
        blank=True,
        null=True
    )

    live_tag = models.CharField(
        max_length=255,
        help_text='Associated git release tag',
        blank=True,
        null=True
    )

    multilingual_field_panels = DefaultPageHeaderImageMixin.multilingual_field_panels + [ReferenceDataPanel()]


@register_snippet
class ReferenceData(models.Model):
    """A model to act as a temporary holding place for SSOT data."""

    class Meta:
        """Metadata class."""

        ordering = ['ssot_path']
        verbose_name_plural = 'Reference data'
        unique_together = ['ssot_path', 'tag']

    ssot_path = models.TextField(
        null=True,
        blank=True,
        help_text='Folder path of SSOT object'
    )

    tag = models.CharField(
        max_length=255,
        help_text='Associated git release tag',
    )

    language = models.CharField(
        max_length=255,
        help_text='Language',
        default="en"
    )

    ssot_root_slug = models.CharField(
        max_length=255,
        help_text='Slug of the highest parent folder.'
    )

    parent_path = models.TextField(
        null=True,
        blank=True,
        help_text='Parent path of object'
    )

    data = models.TextField(
        null=True,
        blank=True,
        help_text='HTML data for the page'
    )

    @cached_property
    def name(self):
        """Return the last item in the ssot_path as a name."""
        return self.ssot_path.split("/")[-1]

    def __str__(self):
        """Print full path as name."""
        return self.ssot_path

    def save(self, *args, **kwargs):
        """Overwrite save to automatically update parent_path."""
        self.parent_path = "/".join(self.ssot_path.split("/")[:-1])
        self.ssot_root_slug = self.ssot_path.split("/")[0]
        super(ReferenceData, self).save(*args, **kwargs)


class ActivityStandardPage(DefaultPageHeaderImageMixin, AbstractContentPage):
    """A model for reference to the Activity Standard."""

    parent_page_types = ['iati_standard.IATIStandardPage', 'iati_standard.ActivityStandardPage']
    sub_page_types = ['iati_standard.ActivityStandardPage']

    ssot_path = models.TextField(
        null=True,
        blank=True,
        help_text='Folder path of SSOT object'
    )

    tag = models.CharField(
        max_length=255,
        help_text='Associated git release tag',
    )

    data = models.TextField(
        null=True,
        blank=True,
        help_text='HTML data for the page'
    )

    has_been_recursed = models.BooleanField(default=False)

    translation_fields = AbstractContentPage.translation_fields + ["data"]

    @cached_property
    def parent_path(self):
        """Return ssot_path of parent object."""
        return "/".join(self.ssot_path.split("/")[:-1])

    @cached_property
    def name(self):
        """Return the last item in the ssot_path as a name."""
        return self.ssot_path.split("/")[-1]

    @cached_property
    def version(self):
        """Return the first item in the ssot_path as a version."""
        return self.ssot_path.split("/")[0]

    def save(self, *args, **kwargs):
        """Overwrite save to automatically update title."""
        soup = BeautifulSoup(self.data, 'html.parser')
        title = soup.find("h1")
        if title:
            self.title = title.text.replace("¶", "")
            self.heading = title.text.replace("¶", "")
        super(ActivityStandardPage, self).save(*args, **kwargs)


class ReferenceMenu(models.Model):
    """A model for to store the Standard Reference menu."""

    tag = models.CharField(
        max_length=255,
        help_text='Associated git release tag',
    )

    menu_json = JSONField()
