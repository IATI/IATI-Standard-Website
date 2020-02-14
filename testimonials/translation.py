"""Module for registering model fields for translation, for use by django-modeltranslation."""

from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from .models import Testimonial


@register(Testimonial)
class TestimonialTR(TranslationOptions):
    """Class declaring which fields of the Testimonial model to translate."""

    fields = Testimonial.translation_fields
