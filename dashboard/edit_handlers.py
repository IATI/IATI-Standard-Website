"""Module to define a custom Multifield Panel."""

from wagtail.admin.panels import MultiFieldPanel as WagtailMultiFieldPanel
from wagtail.admin.panels import HelpPanel as WagtailHelpPanel
from wagtail.admin.panels import FieldPanel


class MultiFieldPanel(WagtailMultiFieldPanel):
    """Class for a custom multifield panel with additional descriptions."""

    def __init__(self, children=(), *args, **kwargs):
        """Initialise the class."""
        if kwargs.get('description', None):
            self.description = kwargs.pop('description')
        super().__init__(children, *args, **kwargs)

    def clone(self):
        """Clone the field panel."""
        props = {
            'children': self.children,
            'heading': self.heading,
            'classname': self.classname,
            'help_text': self.help_text,
        }
        if hasattr(self, 'description'):
            props['description'] = self.description
        return self.__class__(**props)


def HelpPanel(
    content='',
    template='wagtailadmin/edit_handlers/help_panel.html',
    heading='',
    classname='',
    wrapper_class='help-block help-info'
):
    """Define a help text panel."""
    wrapped_content = '<div class="%s">%s</div>' % (wrapper_class, content)
    return WagtailHelpPanel(content=wrapped_content, template=template, heading=heading, classname=classname)


class NoEmptyLabelFieldPanel(FieldPanel):
    """Class for a custom field panel that sets empty label to none for required fields."""

    def on_form_bound(self):
        """Override the on_form_bound method."""
        self.form.fields[self.field_name].empty_label = None
        super().on_form_bound()
