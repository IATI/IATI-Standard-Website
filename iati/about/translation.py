from .models import AboutPage, AboutSubPage, CaseStudiesIndexPage, CaseStudyPage
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

from wagtail.admin.edit_handlers import InlinePanel

from home.translation_helper import add_language_content_panels


@register(AboutPage)
class AboutPageTR(TranslationOptions):
    fields = (
        'heading',
        'excerpt',
        'content_editor',
    )


add_language_content_panels(AboutPage, AboutPageTR)


@register(AboutSubPage)
class AboutSubPageTR(TranslationOptions):
    fields = (
        'heading',
        'excerpt',
        'content_editor',
    )


add_language_content_panels(AboutSubPage, AboutSubPageTR)


@register(CaseStudiesIndexPage)
class CaseStudiesIndexPageTR(TranslationOptions):
    fields = (
        'heading',
        'excerpt',
    )


add_language_content_panels(CaseStudiesIndexPage, CaseStudiesIndexPageTR)


@register(CaseStudyPage)
class CaseStudyPageTR(TranslationOptions):
    fields = (
        'heading',
        'excerpt',
        'content_editor',
    )
    multilingual_field_panels = (
        InlinePanel('case_study_documents', label='Case study attachments'),
    )


add_language_content_panels(CaseStudyPage, CaseStudyPageTR)
