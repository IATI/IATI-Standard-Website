"""Management command that replaces soft-links in content editors and creates redirects."""

import json

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from wagtail.core.models import Page
from wagtail.contrib.redirects.models import Redirect

from wagtail_modeltranslation.contextlib import use_language

from home.models import HomePage


class Command(BaseCommand):
    """Management command that replaces soft-links in content editors and creates redirects."""

    help = 'Replace soft-links in content editors and creates redirects.'

    def add_arguments(self, parser):
        """Add custom command arguments."""
        parser.add_argument('old_pk', nargs='?', type=int)
        parser.add_argument('new_pk', nargs='?', type=int)

    def handle(self, *args, **options):
        """Implement the command handler."""
        if not options['old_pk']:
            raise CommandError('Please pass the old primary key as first positional argument.')
        if not options['new_pk']:
            raise CommandError('Please pass the new primary key as second positional argument.')

        home_page = HomePage.objects.first()

        old_link_str = '<a id=\\"{}\\" linktype=\\"page\\">'.format(options['old_pk'])
        new_link_str = '<a id=\\"{}\\" linktype=\\"page\\">'.format(options['new_pk'])

        for page in Page.objects.all():
            specific_page = page.specific
            for language_code, language_name in settings.ACTIVE_LANGUAGES:
                content_field_name = "content_editor_{}".format(language_code)
                if hasattr(specific_page, content_field_name):
                    content_field = getattr(specific_page, content_field_name)
                    content_str = json.dumps(content_field.stream_data)
                    if old_link_str in content_str:
                        self.stdout.write(self.style.SUCCESS('Replacing soft-link in page: {}'.format(specific_page.title)))
                        edited_content_str = content_str.replace(old_link_str, new_link_str)
                        setattr(specific_page, content_field_name, edited_content_str)
                        if specific_page.live:
                            specific_page.save_revision().publish()
                        else:
                            specific_page.save_revision()

        for language_code, language_name in settings.ACTIVE_LANGUAGES:
            with use_language(language_code):
                old_page = Page.objects.get(pk=options['old_pk'])
                new_page = Page.objects.get(pk=options['new_pk'])
                redirect, created = Redirect.objects.get_or_create(
                    site=home_page.get_site(),
                    old_path=old_page.url
                )
                redirect.redirect_page = new_page
                redirect.save()

        self.stdout.write(self.style.SUCCESS('Successfully replaced {} with {}'.format(options['old_pk'], options['new_pk'])))
