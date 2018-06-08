import requests
import json
from django.core.management.base import BaseCommand, CommandError
from home.models import HomePageStatistics


class Command(BaseCommand):
    """A command for manage.py that updates the home page statistics.
    """

    help = 'Update statistics'

    def handle(self, *args, **options):
        """The default function Django BaseCommand needs to run."""

        home_page_stats = HomePageStatistics.objects.first()
        if home_page_stats is None:
            home_page_stats = HomePageStatistics().save()

        activity_url = "https://iatiregistry.org/api/3/action/package_search?q=extras_filetype:activity&facet.field=[%22extras_activity_count%22]&start=0&rows=0&facet.limit=1000000"
        activity_request = requests.get(activity_url)
        if activity_request.status_code == 200:
            activity_json = json.loads(activity_request.content.decode('utf-8'))
            activity_count = 0
            for key in activity_json["result"]["facets"]["extras_activity_count"]:
                activity_count += int(key) * activity_json["result"]["facets"]["extras_activity_count"][key]
            home_page_stats.activities = activity_count
        else:
            raise CommandError('Unable to connect to IATI registry to query activities.')

        organisation_url = "https://iatiregistry.org/api/3/action/package_search?q=extras_filetype:activity&facet.field=[%22organization%22]&start=0&rows=0&facet.limit=1000000"
        organisation_request = requests.get(organisation_url)
        if organisation_request.status_code == 200:
            organisation_json = json.loads(organisation_request.content.decode('utf-8'))
            organisation_count = len(organisation_json["result"]["search_facets"]["organization"]["items"])
            home_page_stats.organisations = organisation_count
        else:
            raise CommandError('Unable to connect to IATI registry to query organisations.')

        home_page_stats.save()

        self.stdout.write(self.style.SUCCESS('Successfully updated home page statistics.'))
