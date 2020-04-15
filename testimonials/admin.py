"""Module for registering admin models for the testimonials app."""

from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register
)
from testimonials.models import Testimonial


class TestimonialAdmin(ModelAdmin):
    """Admin model for testimonials."""

    model = Testimonial
    menu_icon = 'openquote'
    menu_order = 140
    menu_label = 'Testimonials'
    list_display = ('quote', 'quotee', )
    search_fields = ('quote', 'quotee', )


modeladmin_register(TestimonialAdmin)
