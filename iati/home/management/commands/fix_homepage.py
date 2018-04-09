from django.core.management.base import BaseCommand, CommandError
from home.models import HomePage


class Command(BaseCommand):
    help = 'If run after initial migrate_translation, allows the home page to be edited without throwing an error.'

    def handle(self, *args, **options):
        """A function to force the homepage url_path_en to something not None.
        These particular values were chosen to match the migration 0002_create_homepage.py.
        Without running this function first, the Wagtail function `_update_descendant_url_paths` fails on line 563.
        `_update_descendant_url_paths` queries the length of the field `url_path` without first checking if it's none, because as a constraint no page can exist without a url_path.
        However, since the home page is created before the wagtail-modeltranslation application is applied, url_path_en is by default None.
        At present, the only way I can figure to guarantee an update to the DB without triggering _update_descendant_url_paths after url_path_en is created is by manually running a command after "migrate_translation."
        
        This should only need to be run once at setup.
        """
        HomePage.objects.filter(pk=3).update(url_path_en="/home/",title_en="Home",slug_en="home")
        self.stdout.write(self.style.SUCCESS('Successfully fixed home page'))
