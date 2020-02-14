from django.db import models
from common.utils import ForeignKeyField


class HomeFieldsMixin(models.Model):
    class Meta:
        abstract = True

    header_video = models.URLField(
        max_length=255,
        blank=True,
        help_text='Optional: video embed URL for page header',
    )
    testimonial = ForeignKeyField(
        model='testimonials.Testimonial',
        required=True,
    )
