from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

from home.translation_helper import add_language_content_panels
from .models import GuidanceAndSupportPage, GuidanceGroupPage, GuidancePage, KnowledgebaseIndexPage, KnowledgebasePage


@register(GuidanceAndSupportPage)
class GuidanceAndSupportPageTR(TranslationOptions):
    fields = GuidanceAndSupportPage.translation_fields


add_language_content_panels(GuidanceAndSupportPage)


@register(GuidanceGroupPage)
class GuidanceGroupPageTR(TranslationOptions):
    fields = GuidanceGroupPage.translation_fields


add_language_content_panels(GuidanceGroupPage)


@register(GuidancePage)
class GuidancePageTR(TranslationOptions):
    fields = GuidancePage.translation_fields


add_language_content_panels(GuidancePage)


@register(KnowledgebaseIndexPage)
class KnowledgebaseIndexPageTR(TranslationOptions):
    fields = KnowledgebaseIndexPage.translation_fields


add_language_content_panels(KnowledgebaseIndexPage)


@register(KnowledgebasePage)
class KnowledgebasePageTR(TranslationOptions):
    fields = KnowledgebasePage.translation_fields


add_language_content_panels(KnowledgebasePage)
