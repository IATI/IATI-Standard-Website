"""Management command that replaces aidtransparency links."""

import json
from django.core.management.base import BaseCommand
from wagtail.core.models import Page


class Command(BaseCommand):
    """Management command that fixed aidtransparency links."""

    help = 'Replace links given a JSON file.'

    def add_arguments(self, parser):
        """Add custom command arguments."""
        parser.add_argument('json_file', nargs='+', type=str)

    def handle(self, *args, **options):
        """Implement the command handler."""
        with open(options['json_file'][0]) as json_file:
            json_data = json.load(json_file)

        for page_data in json_data:
            old_link = page_data["OldLink"]
            new_link = page_data["NewLink"]
            link_location = page_data["NewLocation"]
            link_slug = "/home" + link_location[20:] + "/"
            link_matches = Page.objects.filter(url_path_en=link_slug)
            if link_matches.exists():
                self.stdout.write(self.style.SUCCESS("Found page: " + link_slug))
                link_match = link_matches.first().specific
                old_content = link_match.content_editor[0].value.source
                if old_link in old_content:
                    old_content = old_content.replace(old_link, new_link)
                    link_match.content_editor = json.dumps([{'type': 'paragraph', 'value': old_content}])
                    link_match.save()
                    self.stdout.write(self.style.SUCCESS("Replaced link: " + old_link))
                else:
                    self.stdout.write(self.style.NOTICE("Could not find link: " + old_link))
            else:
                self.stdout.write(self.style.NOTICE("Could not find page: " + link_slug))

        self.stdout.write(self.style.SUCCESS("Done."))
