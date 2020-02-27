"""Model definitions for the governance app."""

from wagtail.admin.edit_handlers import InlinePanel
from home.models import AbstractContentPage
from governance.fields import MembersAssemblyFieldsMixin
from governance.inlines import *  # noqa


class MembersAssemblyPage(MembersAssemblyFieldsMixin, AbstractContentPage):
    """A model for the members assembly page."""

    parent_page_types = ['about.AboutSubPage']
    subpage_types = []

    local_translation_fields = [
        'members_title',
    ]
    optional_local_translation_fields = [
    ]

    translation_fields = AbstractContentPage.translation_fields + local_translation_fields
    required_languages = {'en': list(set(local_translation_fields) - set(optional_local_translation_fields))}

    multilingual_field_panels = [
        InlinePanel(
            'chair_items',
            heading='Chair items',
            label='Chair item',
            max_num=1,
        ),
        InlinePanel(
            'vice_chair_items',
            heading='Vice chair items',
            label='Vice chair item',
        ),
    ]
