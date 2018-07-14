"""Module for registering model fields for translation, for use by django-modeltranslation."""

from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

from home.translation_helper import add_language_content_panels
from .models import AboutPage, AboutSubPage, CaseStudyIndexPage, CaseStudyPage, HistoryPage, PeoplePage


@register(AboutPage)
class AboutPageTR(TranslationOptions):
    """Class declaring which fields of the AboutPage model to translate."""

    fields = AboutPage.translation_fields


add_language_content_panels(AboutPage)


@register(AboutSubPage)
class AboutSubPageTR(TranslationOptions):
    """Class declaring which fields of the AboutSubPage model to translate."""

    fields = AboutSubPage.translation_fields


add_language_content_panels(AboutSubPage)


@register(CaseStudyIndexPage)
class CaseStudyIndexPageTR(TranslationOptions):
    """Class declaring which fields of the CaseStudyIndexPage model to translate."""

    fields = CaseStudyIndexPage.translation_fields


add_language_content_panels(CaseStudyIndexPage)


@register(CaseStudyPage)
class CaseStudyPageTR(TranslationOptions):
    """Class declaring which fields of the CaseStudyPage model to translate."""

    fields = CaseStudyPage.translation_fields


add_language_content_panels(CaseStudyPage)


@register(HistoryPage)
class HistoryPageTR(TranslationOptions):
    """Class declaring which fields of the HistoryPage model to translate."""

    fields = HistoryPage.translation_fields


add_language_content_panels(HistoryPage)


@register(PeoplePage)
class PeoplePageTR(TranslationOptions):
    """Class declaring which fields of the PeoplePage model to translate."""

    fields = PeoplePage.translation_fields


add_language_content_panels(PeoplePage)
