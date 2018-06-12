import requests
import json
from django.core.management.base import BaseCommand, CommandError
from home.models import HomePage


class Command(BaseCommand):
    """A command for manage.py that updates the home page statistics.
    """

    help = 'Update statistics'

    def get_total_num_activities(self):
        """
            A function that queries the IATI registry that returns a faceted list of activity counts and their frequencies.
            The total number of activities is then calculated as the sum of the product of a count and a frequency.
            E.g. if "30" is the count and the frequency is 2, then the total number of activities is 60.
        """
        activity_url = "https://iatiregistry.org/api/3/action/package_search?q=extras_filetype:activity&facet.field=[%22extras_activity_count%22]&start=0&rows=0&facet.limit=1000000"
        activity_request = requests.get(activity_url)
        if activity_request.status_code == 200:
            activity_json = json.loads(activity_request.content.decode('utf-8'))
            activity_count = 0
            for key in activity_json["result"]["facets"]["extras_activity_count"]:
                activity_count += int(key) * activity_json["result"]["facets"]["extras_activity_count"][key]
            return activity_count
        else:
            raise CommandError('Unable to connect to IATI registry to query activities.')

    def get_total_num_publishers(self):
        """
            A function that queries the IATI registry that returns a faceted list of activities by organisation.
            The total number of organisations is then calculated as the length of the facet object.
        """
        organisation_url = "https://iatiregistry.org/api/3/action/package_search?q=extras_filetype:activity&facet.field=[%22organization%22]&start=0&rows=0&facet.limit=1000000"
        organisation_request = requests.get(organisation_url)
        if organisation_request.status_code == 200:
            organisation_json = json.loads(organisation_request.content.decode('utf-8'))
            organisation_count = len(organisation_json["result"]["search_facets"]["organization"]["items"])
            return organisation_count
        else:
            raise CommandError('Unable to connect to IATI registry to query organisations.')

    def handle(self, *args, **options):
        """The default function Django BaseCommand needs to run."""

        home_page_queryset = HomePage.objects.live()

        activity_count = self.get_total_num_activities()
        home_page_queryset.update(activities=activity_count)

        organisation_count = self.get_total_num_publishers()
        home_page_queryset.update(organisations=organisation_count)

        self.stdout.write(self.style.SUCCESS('Successfully updated home page statistics.'))
