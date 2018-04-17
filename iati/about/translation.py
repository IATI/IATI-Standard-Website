from .models import AboutPage, AboutSubPage, CaseStudyIndexPage, CaseStudyPage
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

from home.translation_helper import add_language_content_panels


@register(AboutPage)
class AboutPageTR(TranslationOptions):
    fields = AboutPage.translation_fields


add_language_content_panels(AboutPage)


@register(AboutSubPage)
class AboutSubPageTR(TranslationOptions):
    fields = AboutSubPage.translation_fields


add_language_content_panels(AboutSubPage)


@register(CaseStudyIndexPage)
class CaseStudyIndexPageTR(TranslationOptions):
    fields = CaseStudyIndexPage.translation_fields


add_language_content_panels(CaseStudyIndexPage)


@register(CaseStudyPage)
class CaseStudyPageTR(TranslationOptions):
    fields = CaseStudyPage.translation_fields


add_language_content_panels(CaseStudyPage)
