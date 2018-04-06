from django.conf import settings
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList, FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField

def add_language_content_panels(page_model,translation_model):
    edit_handler_contents = []
    for language_code, language_name in settings.LANGUAGES:
        multi_field_panel_contents = []
        stream_field_panel_contents = []
        for field_name in translation_model.fields:
            localized_field_name = field_name+"_{}".format(language_code)
            field_object = getattr(page_model,localized_field_name)
            if not isinstance(field_object,StreamField):
                multi_field_panel_contents.append(FieldPanel(localized_field_name))
            else:
                stream_field_panel_contents.append(StreamFieldPanel(localized_field_name))
        local_content_panel = [
            MultiFieldPanel(multi_field_panel_contents)
        ] + stream_field_panel_contents
        edit_handler_contents.append(
            ObjectList(local_content_panel,heading=language_name)
        )
    page_model.edit_handler = TabbedInterface(
        edit_handler_contents +
        ObjectList(Page.promote_panels,heading='Promote'),
        ObjectList(Page.settings_panels,heading='Settings',classname='settings')
    )