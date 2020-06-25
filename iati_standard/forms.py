"""Module of forms for IATI Standard"""
from django.contrib.postgres.fields import JSONField
from wagtail.admin.forms import WagtailAdminModelForm
from iati_standard.widgets import JSONFieldWidget


class _PrettyJSONFieldForm(WagtailAdminModelForm):
    """
    Render form fields backed by a `JSONField` with a pretty interactive
    widget.
    """

    def __init__(self, *args, **kwargs):
        super(_PrettyJSONFieldForm, self).__init__(*args, **kwargs)
        self.prettify_jsonfields()

    def prettify_jsonfields(self):
        for field_name, field in self.fields.items():
            if isinstance(field, JSONField):
                self.fields[field_name].widget = JSONFieldWidget()
