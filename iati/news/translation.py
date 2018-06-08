from home.translation_helper import add_language_content_panels
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from .models import NewsIndexPage, NewsPage, NewsCategory


@register(NewsIndexPage)
class NewsIndexPageTR(TranslationOptions):
    """A class to allow for the news index page translation fields to be autopopulated in the database."""
    fields = NewsIndexPage.translation_fields
add_language_content_panels(NewsIndexPage)


@register(NewsPage)
class NewsPageTR(TranslationOptions):
    """A class to allow for the news page translation fields to be autopopulated in the database."""
    fields = NewsPage.translation_fields
add_language_content_panels(NewsPage)


@register(NewsCategory)
class NewsCategoryTR(TranslationOptions):
    """A class to allow for the news category translation fields to be autopopulated in the database."""
    fields = NewsCategory.translation_fields
