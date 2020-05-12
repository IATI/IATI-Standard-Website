from modelcluster.fields import ParentalKey
from django.db import models

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Orderable


class StandardGuidanceTypes(Orderable):
    """Concrete clustrable model class for guidance type items."""

    page = ParentalKey('StandardGuidancePage', related_name='guidance_types')
    guidance_type = models.CharField(max_length=100)

    panels = [
        FieldPanel('guidance_type'),
    ]
