from django.db import models


class MembersAssemblyFieldsMixin(models.Model):
    """Abstract mixin class for the members assembly page db fields."""

    class Meta:
        abstract = True

    chairs_title = models.CharField(
        max_length=255,
        help_text='Title for the chairs and vice chairs section',
    )
    chairs_description = models.TextField(
        blank=True,
        help_text='Optional: description for the chairs and vice chairs section',
    )
    members_title = models.CharField(
        max_length=255,
        help_text='Title for the members section',
    )
