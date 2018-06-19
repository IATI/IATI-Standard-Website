"""A module for the IATI Standard page model."""
from django.db import models
from home.models import AbstractContentPage


class IATIStandardPage(AbstractContentPage):
    """A model for the IATI Standard Page, a landing page for IATI reference."""
    parent_page_types = ['home.HomePage']
    subpage_types = []
    translation_fields = AbstractContentPage.translation_fields
