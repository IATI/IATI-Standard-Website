import json
import datetime
import pytz
from django.utils.text import slugify
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from news.models import NewsIndexPage, NewsPage
from events.models import EventIndexPage, EventPage


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
        event_index_page = EventIndexPage.objects.live().first()
        if news_index_page is not None and event_index_page is not None:
            with open(options['json_file'][0]) as json_file:
                json_data = json.load(json_file)

                for page_data in json_data:
                    page_slug = page_data['link'].split("/")[-1]
                    if page_data["type"] == "news":
                        try:
                            news_page = NewsPage(
                                title_en=page_data["title"],
                                slug_en=page_slug,
                                heading_en=page_data["title"],
                                content_editor_en=json.dumps([{'type': 'paragraph', 'value': page_data["content"]}]),
                                title=page_data["title"],
                                slug=page_slug,
                                heading=page_data["title"],
                                content_editor=json.dumps([{'type': 'paragraph', 'value': page_data["content"]}]),
                                date=datetime.datetime.strptime(page_data["date"], "%Y-%m-%d").date()
                            )
                            news_index_page.add_child(instance=news_page)
                            news_page.save_revision().publish()
                            self.stdout.write(self.style.SUCCESS("News: " + page_data["title"]))
                        except ValidationError:
                            self.stdout.write(self.style.NOTICE("News: " + page_data["title"]))
                    else:
                        try:
                            event_page = EventPage(
                                title_en=page_data["title"],
                                slug_en=page_slug,
                                heading_en=page_data["title"],
                                content_editor_en=json.dumps([{'type': 'paragraph', 'value': page_data["content"]}]),
                                title=page_data["title"],
                                slug=page_slug,
                                heading=page_data["title"],
                                content_editor=json.dumps([{'type': 'paragraph', 'value': page_data["content"]}]),
                                date_start=datetime.datetime.strptime(page_data["date"], "%Y-%m-%d").replace(tzinfo=pytz.UTC),
                                date_end=datetime.datetime.strptime(page_data["date"], "%Y-%m-%d").replace(tzinfo=pytz.UTC) 
                            )
                            event_index_page.add_child(instance=event_page)
                            event_page.save_revision().publish()
                            self.stdout.write(self.style.SUCCESS("Event: " + page_data["title"]))
                        except ValidationError:
                            self.stdout.write(self.style.NOTICE("Event: " + page_data["title"]))

            self.stdout.write(self.style.SUCCESS('Successfully imported news and events.'))
