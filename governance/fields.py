from django.db import models
from django.utils.functional import cached_property
from taxonomies.models import Constituency


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

    @cached_property
    def constituencies(self):
        """Return the constituency items."""
        return Constituency.objects.all().order_by('title')

    @cached_property
    def members(self):
        """Return the member items."""
        from governance.models import Member
        return Member.objects.all().order_by('name')
