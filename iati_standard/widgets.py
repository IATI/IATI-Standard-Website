"""Module of widgets for IATI Standard."""
from django.utils.safestring import mark_safe
from prettyjson import PrettyJSONWidget


class JSONFieldWidget(PrettyJSONWidget):
    """Render JSON data from a `JSONField` as a nice interactive widget using django-prettyjson."""

    DEFAULT_ATTR = 'parsed'

    def render(self, *args, **kwargs):
        """Discard unsupported `renderer` kwarg."""
        kwargs.pop('renderer', None)

        return mark_safe(super(JSONFieldWidget, self).render(*args, **kwargs))
