from django.db import models


class MembersAssemblyFieldsMixin(models.Model):
    """Abstract mixin class for the members assembly page db fields."""

    class Meta:
        abstract = True

    members_title = models.CharField(
        max_length=255,
        help_text='Title for the members section',
    )
