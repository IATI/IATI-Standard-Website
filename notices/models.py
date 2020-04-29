import uuid
from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.html import strip_tags
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.snippets.models import register_snippet
from common.utils import ForeignKeyField
from dashboard.edit_handlers import MultiFieldPanel
from notices.edit_handlers import DisplayTypeFieldPanel

NOTICE_TYPES = [
    ('notice', 'Notice (blue)'),
    ('alert', 'Alert (yellow)'),
    ('warning', 'Warning (red)'),
]

DISPLAY_LOCATIONS = [
    ('all', 'All pages in site'),
    ('selected_page', 'Selected page only'),
    ('selected_page_and_children', 'Selected page and child pages'),
    ('children_only', 'Children of selected page'),
]


class AbstractNotice(models.Model):
    """Abstract class for a notice."""

    class Meta:
        abstract = True

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )
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
        return strip_tags(self.content.replace('</', ' </'))

    @classmethod
    def filter_dismissed_notices(cls, notice, request):
        """Only return notices that aren't set as dismissed in the user's cookies."""
        if request.COOKIES.get(str(notice.uuid)):
            return cls.objects.none()
        return notice


@register_snippet
class GlobalNotice(AbstractNotice):
    """A snippet class for global notices."""

    class Meta:
        verbose_name_plural = 'Global notice'

    panels = [
        FieldPanel('content'),
        FieldPanel(
            'notice_type',
            widget=forms.RadioSelect,
            classname='non-floated-options',
        ),
    ]

    def clean(self):
        """Make sure that no more than one instance of a given model is created."""
        model = self.__class__
        if (model.objects.count() > 0 and self.id != model.objects.get().id):
            raise ValidationError("Can only create 1 %s instance." % model._meta.verbose_name)
        super().clean()

    def has_add_permission(self, request):
        """Hide the "Add" button when there is already an instance."""
        num_objects = self.model.objects.count()
        if num_objects >= 1:
            return False
        return super().has_add_permission(request)

    @classmethod
    def get_notice(cls, request):
        """Class method for getting a global notice."""
        return cls.filter_dismissed_notices(cls.objects.all().first(), request)


@register_snippet
class PageNotice(AbstractNotice):
    """A snippet class for page notices."""

    allow_dismiss = models.BooleanField(
        default=False,
        blank=True,
    )
    display_location = models.CharField(
        max_length=255,
        choices=DISPLAY_LOCATIONS,
        default=DISPLAY_LOCATIONS[1][0]
    )
    page = ForeignKeyField(
        model='wagtailcore.Page',
        required=False,
        on_delete=models.CASCADE,
    )

    panels = [
        FieldPanel('content'),
        FieldPanel(
            'notice_type',
            widget=forms.RadioSelect,
            classname='non-floated-options',
        ),
        MultiFieldPanel(
            [
                FieldPanel('allow_dismiss'),
            ],
            heading='Allow dismiss',
            description='Select to allow visitors to dismiss this message for two weeks.'
        ),
        MultiFieldPanel(
            [
                DisplayTypeFieldPanel(),
            ],
            heading='Display location',
            description='Select the location of this notice. If more than one notice is applicable to a page, the most specific wil be displayed.'
        ),
    ]

    def clean(self):
        """Page field is optional, so raise a validation error when a notice is not global."""
        if self.display_location != DISPLAY_LOCATIONS[0][0] and not self.page:
            raise ValidationError({
                'page': 'This field is required'
            })
        return super().clean()

    @classmethod
    def get_notice(cls, page, request):
        """Class method for finding most specific notice to match a page."""

        # return if no page
        if not page:
            return cls.objects.none()

        # is there a selected page with same id?
        location = DISPLAY_LOCATIONS[1][0]
        notices = cls.objects.all().filter(page=page, display_location=location)
        if notices:
            return cls.filter_dismissed_notices(notices.first(), request)

        # is there a matching selected page and child page?
        location = DISPLAY_LOCATIONS[2][0]
        notices = cls.objects.all().filter(page=page, display_location=location)
        if notices:
            return cls.filter_dismissed_notices(notices.first(), request)

        # get ancestors to check for child pages
        current_page = Page.objects.filter(id=page.id).first()
        ancestors = Page.objects.ancestor_of(current_page).values_list('id', flat=True)

        # is the page a child of a selected page and child page option?
        location = DISPLAY_LOCATIONS[2][0]
        notices = cls.objects.all().filter(page__id__in=[ancestors], display_location=location)
        if notices:
            return cls.filter_dismissed_notices(notices.first(), request)

        # is the page a child of selected page children only option?
        location = DISPLAY_LOCATIONS[3][0]
        notices = cls.objects.all().filter(page__id__in=[ancestors], display_location=location)
        if notices:
            return cls.filter_dismissed_notices(notices.first(), request)

        # is there a global notice?
        location = DISPLAY_LOCATIONS[0][0]
        notices = cls.objects.all().filter(display_location=location)
        if notices:
            return cls.filter_dismissed_notices(notices.last(), request)

        # nothing found, return none
        return cls.objects.none()
