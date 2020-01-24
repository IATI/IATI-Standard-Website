from wagtail.admin.edit_handlers import MultiFieldPanel as WagtailMultiFieldPanel
from wagtail.admin.edit_handlers import HelpPanel as WagtailHelpPanel


class MultiFieldPanel(WagtailMultiFieldPanel):
    def __init__(self, children=(), *args, **kwargs):
        if kwargs.get('description', None):
            self.description = kwargs.pop('description')
        super().__init__(children, *args, **kwargs)

    def clone(self):
        props = {
            'children': self.children,
            'heading': self.heading,
            'classname': self.classname,
            'help_text': self.help_text,
        }
        if hasattr(self, 'description'):
            props['description'] = self.description
        return self.__class__(**props)


def HelpPanel(content='', template='wagtailadmin/edit_handlers/help_panel.html', heading='', classname=''):
    wrapped_content = '<p class="help-block help-info">%s</p>' % content
    return WagtailHelpPanel(content=wrapped_content, template=template, heading=heading, classname=classname)
