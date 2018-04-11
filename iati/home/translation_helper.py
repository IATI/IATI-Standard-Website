from django.conf import settings
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList, FieldPanel, MultiFieldPanel, StreamFieldPanel, InlinePanel
from wagtail.core.fields import Creator
from django.utils.translation import gettext_lazy as _
from wagtail.images.edit_handlers import ImageChooserPanel


def add_language_content_panels(page_model, translation_model):
    """A function that dynamically adds tabbed content panels depending on the fields defined in the translation model and the languages in settings

    Args:
        page_model (Page): The page model class which needs tabbed content panels
        translation_model (TranslationOptions): The class from translation.py that contains the fields to be translated

    Returns:
        None: This doesn't return anything, it's modifying the provided page_model.

    TODO:
        Figure out whether using type(Creator) is sustainable. For some reason StreamBlocks are wagtail.core.fields.Creator and all other fiends are django.db.models.query_utils.DeferredAttribute
    """
    edit_handler_contents = []
    promote_panel_contents = []
    promote_panel_fields = ["slug", "seo_title", "search_description"]
    for language_code, language_name in settings.LANGUAGES:
        multi_field_panel_contents = [FieldPanel("title_{}".format(language_code))]
        stream_field_panel_contents = []
        for field_name in translation_model.fields:
            localized_field_name = field_name+"_{}".format(language_code)
            field_object = getattr(page_model, localized_field_name)
            if not isinstance(field_object, Creator):
                multi_field_panel_contents.append(FieldPanel(localized_field_name))
            else:
                stream_field_panel_contents.append(StreamFieldPanel(localized_field_name))
        for field_name in promote_panel_fields:
            promote_panel_contents.append(FieldPanel(field_name+"_{}".format(language_code)))
        local_content_panel = [MultiFieldPanel(multi_field_panel_contents)] + stream_field_panel_contents
        edit_handler_contents.append(ObjectList(local_content_panel, heading=language_name))
    promote_and_settings_panels = [ObjectList([MultiFieldPanel(promote_panel_contents)], heading=_('Promote')), ObjectList(page_model.settings_panels, heading=_('Settings'), classname='settings')]
    if hasattr(translation_model, "image_fields"):
        edit_handler_contents = [ObjectList([ImageChooserPanel(field) for field in translation_model.image_fields], heading=_('Images'))] + edit_handler_contents
    if hasattr(translation_model, "inline_fields"):
        edit_handler_contents = [ObjectList([InlinePanel(field, label=field) for field in translation_model.inline_fields], heading=_('Inlines'))] + edit_handler_contents
    if hasattr(translation_model, "multilingual_fields"):
        edit_handler_contents = [ObjectList([MultiFieldPanel([FieldPanel(field) for field in translation_model.multilingual_fields])], heading=_('Multilingual'))] + edit_handler_contents
    page_model.edit_handler = TabbedInterface(edit_handler_contents + promote_and_settings_panels)
