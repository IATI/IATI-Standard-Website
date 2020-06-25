"""Module of widgets for IATI Standard"""
from django.utils.safestring import mark_safe
from prettyjson import PrettyJSONWidget


class JSONFieldWidget(PrettyJSONWidget):
    """
    Render JSON data from a `JSONField` as a nice interactive widget using
    django-prettyjson.
    For Wagtail pages, specify this widget in the panels definition, e.g:
        content_panels = Page.content_panels + [
            FieldPanel("json", widget=JSONFieldWidget)
        ]
    For standard models, define a custom form based on the admin helper class
    `_PrettyJSONFieldForm` and set the `YourModel.base_form_class` attribute
    to point to it.
    """
    DEFAULT_ATTR = 'parsed'

    def render(self, *args, **kwargs):
        # Discard unsupported `renderer` kwarg
        # TODO Where does `renderer` come from; can we stop it at the source?
        kwargs.pop('renderer', None)

        return mark_safe(super(JSONFieldWidget, self).render(*args, **kwargs))
