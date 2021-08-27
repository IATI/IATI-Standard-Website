from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.snippets.models import register_snippet


class SimpleTaxonomy(models.Model):
    """An abstract model for simple taxonomy terms."""

    class Meta:
        abstract = True
        ordering = ['title']

    title = models.CharField(
        max_length=100,
        help_text='The title of the category'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        help_text='The slug must be unique for this category'
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('slug'),
    ]

    def __str__(self):
        """Override magic method to return term title."""
        return self.title


@register_snippet
class Constituency(SimpleTaxonomy):
    """A concrete model for constituency taxonomy terms."""

    class Meta:
        verbose_name = 'Constituency'
        verbose_name_plural = 'Constituencies'
