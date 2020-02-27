from django.db import models
from django.utils.functional import cached_property


class MembersAssemblyFieldsMixin(models.Model):
    """Abstract mixin class for the members assembly page db fields."""

    class Meta:
        abstract = True

    members_title = models.CharField(
        max_length=255,
        help_text='Title for the members section',
    )

    @cached_property
    def chairs(self):
        """Return the chair items."""
        return self.chair_items.all()

    @cached_property
    def vice_chairs(self):
        """Return the vice chair items."""
        return self.vice_chair_items.all()
