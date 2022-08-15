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


def get_selected_or_fallback(selected=[], fallback=[], max_length=3) -> list:
    """Get selected pages from a list, and try to populate with fallbacks if the max length isn't met."""
    if len(selected) >= max_length:
        return list(selected)[:max_length]
    elif len(selected) > 0 and len(fallback) > 0:
        fallback = [fb for fb in fallback if fb.id not in [sel.id for sel in selected]]
        return list(list(selected) + list(fallback))[:max_length]
    else:
        return fallback
