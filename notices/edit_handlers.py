from wagtail.admin.panels import FieldPanel, PageChooserPanel
from common.edit_handlers import CustomisedEditHandler

 
class DisplayTypeFieldPanel(CustomisedEditHandler):
    """Customised edit handler, shows and hides the page field depending on display_location selection."""

    template = 'notices/edit_handlers/display_type_field_panel.html'
    js_template = 'notices/edit_handlers/display_type_field_panel.js'

    def __init__(self, children=(), heading='', classname='', help_text='', base_form_class=None):
        """Override the init method."""
        self.children = [
            FieldPanel('display_location'),
            PageChooserPanel('page'),
        ]
        self.heading = heading
        self.classname = classname
        self.help_text = help_text
        self.model = self.instance = self.request = self.form = None
        self.base_form_class = base_form_class
        
