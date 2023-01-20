import string
import random
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from wagtail.admin.panels import PanelGroup


def random_string(length: int = 6, chars: str = string.ascii_lowercase) -> str:
    """Create and return a random string."""
    return ''.join(random.SystemRandom().choice(chars) for _ in range(length))

def widget_with_script(widget, script):
    return mark_safe('{0}<script>{1}</script>'.format(widget, script))

class CustomisedEditHandler(PanelGroup):
    """Customised edit handler, for use by concrete subclasses."""

    def classes(self):
        """Append an extra class to the list."""
        classes = super().classes()
        classes.append('multi-field')

        return classes

    def render(self):
        """Override the render method."""
        random_id = random_string()
        js = mark_safe(render_to_string(self.js_template, {
            'self': self,
            'id': random_id,
        }))
        fieldset = render_to_string(self.template, {
            'self': self,
            'id': random_id,
        })
        return widget_with_script(fieldset, js)
