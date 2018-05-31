import json
from django.utils.text import slugify
from django.core.management.base import BaseCommand, CommandError
from news.models import NewsIndexPage, NewsPage
from wagtail.tests.utils.form_data import streamfield


class Command(BaseCommand):
    """A command for manage.py that imports news from a JSON file.
    """

    help = 'Import news given a JSON file.'

    def add_arguments(self, parser):
        parser.add_argument('json_file', nargs='+', type=str)

    def handle(self, *args, **options):
        """The default function Django BaseCommand needs to run."""

        if not options['json_file']:
            raise CommandError('Please pass the path to a JSON file as the first positional argument.')

        news_index_page = NewsIndexPage.objects.live().first()
        if news_index_page is not None:
            with open(options['json_file']) as json_file:
                json_data = json.loads(json_file)

                for page_data in json_data:
                    news_page = NewsPage(
                        title_en=page_data["title"],
                        slug_en=slugify(page_data["title"]),
                        header_en=page_data["title"],
                        content_editor_en=streamfield([('paragraph', page_data["content"]), ]),
                        title=page_data["title"],
                        slug=slugify(page_data["title"]),
                        header=page_data["title"],
                        content_editor=streamfield([('paragraph', page_data["content"]), ]),
                    )
                    news_index_page.add_child(instance=news_page)
                    news_page.save_revision().publish()

            self.stdout.write(self.style.SUCCESS('Successfully imported news.'))
