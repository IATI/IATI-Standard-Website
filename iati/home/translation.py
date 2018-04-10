from .models import HomePage
# from wagtail.core.models import Page
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


# @register(Page)
# class PageTR(TranslationOptions):
#     pass
#     # fields = (
#     #     'body',
#     # )

@register(HomePage)
class HomePageTR(TranslationOptions):
    pass
    # fields = (
    #     'body',
    # )
