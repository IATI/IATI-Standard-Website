from wagtail.core.blocks import StructValue
from navigation.utils import get_localised_field_value, get_default_lang_slug


class TransStructValue(StructValue):

    def description(self):
        return get_localised_field_value(
            self,
            'description',
            use_get=True,
        )

    def default_slug(self):
        return get_default_lang_slug(self.get('page'))
