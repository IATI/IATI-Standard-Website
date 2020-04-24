from django import forms
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.snippets.models import register_snippet
from dashboard.edit_handlers import HelpPanel

NOTICE_TYPES = [
    ('notice', 'Notice'),
    ('alert', 'Alert'),
    ('warning', 'Warning'),
]


class AbstractNotice(models.Model):
    """Abstract class for a notice."""

    class Meta:
        abstract = True

    notice_type = models.CharField(
        max_length=255,
        choices=NOTICE_TYPES,
        default=NOTICE_TYPES[0][0]
    )
    content = RichTextField(
        help_text='Content for the notice',
        features=['h2', 'link', 'bold'],
    )

    translation_fields = [
        'content',
    ]

    # panels = [
    #     PageChooserPanel('page'),
    # ]


@register_snippet
class GlobalNotice(AbstractNotice):
    """A snippet class for global notices."""

    panels = [
        HelpPanel(
            content='Available notice types: Notice (blue), Alert (yellow), Warning (red).',
        ),
        FieldPanel(
            'notice_type',
            widget=forms.RadioSelect,
            classname='non-floated-options',),
        FieldPanel('content'),
    ]

    def __str__(self):
        """Get a string representation of the snippet, the content."""
        return self.content
