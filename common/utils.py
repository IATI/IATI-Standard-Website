"""Module of common utilities."""
from django.db import models


def ForeignKeyField(model=None, required=False, on_delete=models.SET_NULL, related_name='+', **kwargs) -> models.ForeignKey:
    """Define custom field for a non-required foreign key field."""
    if not model:
        raise ValueError('ForeignKeyField requires a valid model string reference')
    required = not required
    return models.ForeignKey(
        model,
        null=True,
        blank=required,
        on_delete=on_delete,
        related_name=related_name,
        **kwargs
    )


def WagtailImageField(required=False, **kwargs) -> models.ForeignKey:
    """Define custom field for a Wagtail-style image."""
    return ForeignKeyField(
        model='wagtailimages.Image',
        required=required,
        **kwargs
    )
