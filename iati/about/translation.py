from .models import AboutPage, AboutSubPage
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

# from home.translation_helper import add_language_content_panels


@register(AboutPage)
class AboutPageTR(TranslationOptions):
    fields = (
        'heading',
        'excerpt',
        'content_editor',
    )


@register(AboutSubPage)
class AboutSubPageTR(TranslationOptions):
    fields = (
        'heading',
        'excerpt',
        'content_editor',
    )
