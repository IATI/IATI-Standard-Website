"""Module for registering model fields for translation, for use by django-modeltranslation."""

from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

from home.translation_helper import add_language_content_panels
from .models import (
    GuidanceAndSupportPage,
    GuidanceGroupPage,
    GuidancePage,
    # KnowledgebaseIndexPage,
    # KnowledgebasePage,
    CommunityPage,
    SupportPage
)


@register(GuidanceAndSupportPage)
class GuidanceAndSupportPageTR(TranslationOptions):
    """Class declaring which fields of the GuidanceAndSupportPage model to translate."""

    fields = GuidanceAndSupportPage.translation_fields


add_language_content_panels(GuidanceAndSupportPage)


@register(GuidanceGroupPage)
class GuidanceGroupPageTR(TranslationOptions):
    """Class declaring which fields of the GuidanceGroupPage model to translate."""

    fields = GuidanceGroupPage.translation_fields


add_language_content_panels(GuidanceGroupPage)


@register(GuidancePage)
class GuidancePageTR(TranslationOptions):
    """Class declaring which fields of the GuidancePage model to translate."""

    fields = GuidancePage.translation_fields


add_language_content_panels(GuidancePage)


# @register(KnowledgebaseIndexPage)
# class KnowledgebaseIndexPageTR(TranslationOptions):
#     """Class declaring which fields of the KnowledgebaseIndexPage model to translate."""

#     fields = KnowledgebaseIndexPage.translation_fields


# add_language_content_panels(KnowledgebaseIndexPage)


# @register(KnowledgebasePage)
# class KnowledgebasePageTR(TranslationOptions):
#     """Class declaring which fields of the KnowledgebasePage model to translate."""

#     fields = KnowledgebasePage.translation_fields


# add_language_content_panels(KnowledgebasePage)


@register(CommunityPage)
class CommunityPageTR(TranslationOptions):
    """Class declaring which fields of CommunityPage model to translate."""

    fields = CommunityPage.translation_fields


@register(SupportPage)
class SupportPageTR(TranslationOptions):
    """Class declaring which fields of the SupportPage model to translate."""

    fields = SupportPage.translation_fields


add_language_content_panels(SupportPage)
