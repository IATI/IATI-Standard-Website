from django.core.management.base import BaseCommand, CommandError
from home.models import HomePageStatistics


class Command(BaseCommand):
    """A command for manage.py that updates the home page statistics.
    """

    help = 'Update statistics'

    def add_arguments(self, parser):
        parser.add_argument(
            '--activities',
            dest='activities',
            default=None,
            help='Number of activities',
        )
        parser.add_argument(
            '--organisations',
            dest='organisations',
            default=None,
            help='Number of organisations',
        )

    def handle(self, *args, **options):
        """The default function Django BaseCommand needs to run."""

        if not options['activities'] and not options['organisations']:
            raise CommandError('Please pass at least one statistic to update.')

        home_page_stats = HomePageStatistics.objects.first()
        if home_page_stats is None:
            home_page_stats = HomePageStatistics().save()

        if options['activities']:
            home_page_stats.activities = int(options['activities'])

        if options['organisations']:
            home_page_stats.organisations = int(options['organisations'])

        home_page_stats.save()

        self.stdout.write(self.style.SUCCESS('Successfully updated home page statistics.'))
