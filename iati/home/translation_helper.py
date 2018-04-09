from django.conf import settings
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList, FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.core.fields import Creator
from django.utils.translation import gettext as _


def add_language_content_panels(page_model, translation_model):
    """A function that dynamically adds tabbed content panels depending on the fields defined in the translation model and the languages in settings

    Args:
        page_model (Page): The page model class which needs tabbed content panels
        translation_model (TranslationOptions): The class from translation.py that contains the fields to be translated

    Returns:
        None: This doesn't return anything, it's modifying the provided page_model.

    TODO:
        Figure out whether using type(Creator) is sustainable. For some reason StreamBlocks are wagtail.core.fields.Creator and all other fiends are django.db.models.query_utils.DeferredAttribute
        Start a standard way of adding to the TabbedInferface. I can't find a way to create a new tabbed interface without overwriting page_model.edit_handler so it would be nice to start using a variable inside of our classes that use this. Something like `additional_panels` that could be picked up and added to edit_handler_contents before overwriting page_model.edit_handler
    """
    edit_handler_contents = []
    for language_code, language_name in settings.LANGUAGES:
        localized_title_field = FieldPanel("title_{}".format(language_code))
        multi_field_panel_contents = [localized_title_field]
        stream_field_panel_contents = []
        for field_name in translation_model.fields:
            localized_field_name = field_name+"_{}".format(language_code)
            field_object = getattr(page_model, localized_field_name)
            if not isinstance(field_object, Creator):
                multi_field_panel_contents.append(FieldPanel(localized_field_name))
            else:
                stream_field_panel_contents.append(StreamFieldPanel(localized_field_name))

        local_content_panel = [MultiFieldPanel(multi_field_panel_contents)] + stream_field_panel_contents
        edit_handler_contents.append(ObjectList(local_content_panel, heading=language_name))
        # Can you add a better variable name if this one isn't good enough?
        page_model_panels = [ObjectList(page_model.promote_panels, heading=_('Promote')), ObjectList(page_model.settings_panels, heading=_('Settings'), classname='settings')]

    page_model.edit_handler = TabbedInterface(edit_handler_contents + page_model_panels)
