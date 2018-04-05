from .models import Contact
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(Contact)
class ContactTR(TranslationOptions):
    pass
    # fields = (
    #     'body',
    # )
