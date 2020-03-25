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


def get_selected_or_fallback(selected=None, fallback=None, max_length=None, order=None) -> list:
    """Get selected pages from a list, and try to populate with fallbacks if the max length isn't met."""
    if not selected:
        selected = []

    fallbacks = []
    if fallback:
        try:
            fallbacks = fallback
            if selected:
                fallbacks = fallbacks.exclude(
                    id__in=[x.id for x in list(selected)]
                ).live().specific()
            if order:
                fallbacks = fallbacks.order_by(order)
        except AssertionError as e:
            if 'Cannot filter a query once a slice has been taken' in str(e):
                raise Exception('Cannot filter a query once a slice has been taken. \
                             Use the max_length argument if you want to limit the amount returned')

    if not max_length:
        return list(selected) + list(fallbacks)
    else:
        return list(list(selected) + list(fallbacks))[:max_length]
