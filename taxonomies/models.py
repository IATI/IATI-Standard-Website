from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.snippets.models import register_snippet
from dashboard.edit_handlers import MultiFieldPanel


class SimpleTaxonomy(models.Model):

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
        help_text='The slug must be unqiue for this category'
    )

    translation_fields = [
        'title',
        'slug',
    ]

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('title'),
                FieldPanel('slug'),
            ],
            heading='Title and slug',
            description='The title and slug of the category.'
        ),
    ]

    def __str__(self):
        return self.title


@register_snippet
class Constituency(SimpleTaxonomy):
    class Meta:
        verbose_name = 'Constituency'
