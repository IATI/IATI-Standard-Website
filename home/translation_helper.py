"""Module providing helper functions for use with django-modeltranslation."""

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import TabbedInterface, ObjectList, FieldPanel, MultiFieldPanel
from wagtail.fields import Creator


def add_language_content_panels(page_model):
    """Dynamically add tabbed content panels depending on the fields defined in the page model and the languages in settings.

    Args:
        page_model (Page): The page model class which needs tabbed content panels. Should have the array translation_fields defined in the page model.

    Returns:
        None: This doesn't return anything, it's modifying the provided page_model.

    TODO:
        Figure out whether using type(Creator) is sustainable. For some reason StreamBlocks are wagtail.core.fields.Creator and all other fiends are django.db.models.query_utils.DeferredAttribute

    """
    edit_handler_contents = []
    promote_panel_contents = []
    promote_panel_translation_fields = [
        FieldPanel('slug'),
        FieldPanel('seo_title'),
        FieldPanel('search_description'),
    ]
    promote_panel_non_translation_fields = [
        FieldPanel('social_media_image'),
    ]
    for language_code, language_name in settings.LANGUAGES:
        multi_field_panel_contents = [FieldPanel("title_{}".format(language_code))]
        stream_field_panel_contents = []
        for field_name in page_model.translation_fields:
            localized_field_name = field_name + "_{}".format(language_code)
            field_object = getattr(page_model, localized_field_name)
            if not isinstance(field_object, Creator):
                multi_field_panel_contents.append(FieldPanel(localized_field_name))
            else:
                stream_field_panel_contents.append(StreamFieldPanel(localized_field_name))
        for field in promote_panel_translation_fields:
            promote_panel_contents.append(FieldPanel(field.field_name + "_{}".format(language_code)))

        local_content_panel = [MultiFieldPanel(multi_field_panel_contents)] + stream_field_panel_contents
        edit_handler_contents.append(ObjectList(local_content_panel, heading=language_name))

    for field in promote_panel_non_translation_fields:
        promote_panel_contents.append(field)
    promote_and_settings_panels = [ObjectList([MultiFieldPanel(promote_panel_contents)], heading=_('Promote')), ObjectList(page_model.settings_panels, heading=_('Settings'), classname='settings')]
    if hasattr(page_model, "multilingual_field_panels"):
        edit_handler_contents = [ObjectList([field for field in page_model.multilingual_field_panels], heading=_('Multilingual'))] + edit_handler_contents
    page_model.edit_handler = TabbedInterface(edit_handler_contents + promote_and_settings_panels)
