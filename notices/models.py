from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.snippets.models import register_snippet
from common.utils import ForeignKeyField
from dashboard.edit_handlers import HelpPanel
from notices.edit_handlers import DisplayTypeFieldPanel

NOTICE_TYPES = [
    ('notice', 'Notice'),
    ('alert', 'Alert'),
    ('warning', 'Warning'),
]

DISPLAY_TYPES = [
    ('all', 'All pages'),
    ('selected_page', 'Selected page only'),
    ('selected_page_and_children', 'Selected page and child pages'),
    ('children_only', 'Children of selected page'),
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

    def __str__(self):
        """Get a string representation of the snippet, the content."""
        return self.content

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
            classname='non-floated-options',
        ),
        FieldPanel('content'),
    ]


@register_snippet
class PageNotice(AbstractNotice):
    """A snippet class for page notices."""

    allow_dismiss = models.BooleanField(
        default=False,
        blank=True,
        help_text='Select to allow visitors to dismiss this message for two weeks'
    )
    display_type = models.CharField(
        max_length=255,
        choices=DISPLAY_TYPES,
        default=DISPLAY_TYPES[1][0]
    )
    page = ForeignKeyField(
        model='wagtailcore.Page',
        required=False,
        on_delete=models.CASCADE,
    )

    panels = [
        HelpPanel(
            content='Available notice types: Notice (green), Alert (yellow), Warning (red).',
        ),
        FieldPanel(
            'notice_type',
            widget=forms.RadioSelect,
            classname='non-floated-options',
        ),
        FieldPanel('allow_dismiss'),
        DisplayTypeFieldPanel(),
        FieldPanel('content'),
    ]

    def clean(self):
        if self.display_type != DISPLAY_TYPES[0][0]:
            raise ValidationError({
                'page': 'This field is required'
            })
        return super().clean()
