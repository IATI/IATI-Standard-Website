import string
import random
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from wagtail.admin.edit_handlers import BaseCompositeEditHandler
from wagtail.admin.edit_handlers import widget_with_script


def random_string(length: int = 6, chars: str = string.ascii_lowercase) -> str:
    return ''.join(random.SystemRandom().choice(chars) for _ in range(length))


class CustomisedEditHandler(BaseCompositeEditHandler):

    def classes(self):
        classes = super().classes()
        classes.append('multi-field')

        return classes

    def render(self):
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
