"""Model definitions for the governance app."""

from home.models import AbstractContentPage
from governance.fields import MembersAssemblyFieldsMixin


class MembersAssemblyPage(MembersAssemblyFieldsMixin, AbstractContentPage):
    """A model for the members assembly page."""

    parent_page_types = ['about.AboutSubPage']
    subpage_types = []

    local_translation_fields = [
        'chairs_title',
        'chairs_description',
        'members_title',
    ]
    optional_local_translation_fields = [
        'chairs_description',
    ]
    translation_fields = AbstractContentPage.translation_fields + local_translation_fields
    required_languages = {'en': list(set(local_translation_fields) - set(optional_local_translation_fields))}

    multilingual_field_panels = [
    ]
