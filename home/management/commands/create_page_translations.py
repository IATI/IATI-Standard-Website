from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from wagtail_localize.synctree import PageIndex
from wagtail.models import Locale


class Command(BaseCommand):
    """Management command that attempts to copy default website pages into translations for provided languages in the locales setting."""

    def handle(self, **options):
        """Implement the command handler."""
        source_locale = Locale.objects.get(language_code='en')
        target_locale = Locale.objects.get(language_code='fr')
        page_index = PageIndex.from_database().sort_by_tree_position()
        pages_not_in_locale = page_index.not_translated_into(target_locale)
        for page in pages_not_in_locale:
            model = page.content_type.model_class()
            source_page = model.objects.get(translation_key=page.translation_key, locale=source_locale)
            if target_locale.id not in page.aliased_locales:
                try:
                    source_page.copy_for_translation(target_locale, copy_parents=True, alias=True)
                except ValidationError:
                    print('Cannot create {}. Skipping for now...'.format(source_page))
