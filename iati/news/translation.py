from .models import NewsIndexPage, NewsPage
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(NewsIndexPage)
class NewsIndexPageTR(TranslationOptions):
    pass
    # fields = (
    #     'body',
    # )

@register(NewsPage)
class NewsPageTR(TranslationOptions):
    pass
    # fields = (
    #     'body',
    # )
