from django.core.management.base import BaseCommand, CommandError
from home.models import HomePage
from about.models import AboutPage
from contact.models import ContactPage
from events.models import EventIndexPage
from guidance_and_support.models import GuidanceAndSupportPage
from news.models import NewsIndexPage


class Command(BaseCommand):
    """A command for manage.py that first rectifies some database problems with the HomePage model created by wagtail-modeltranslation and then creates the top-level default pages from the infrastructure architecture.

       The home_page needed a queryset update before the HomePage model is allowed to save in the CMS.
       The update method bypasses the validation of the save method and writes directly to the database, but the child pages need their URLs updated with save.

       TODO:
       1. If wagtail-modeltranslation or django-modeltranslation update, this command may no longer need to edit the home page.
       2. Check whether home page has a title before changing it.
    """

    help = 'Create the default pages that constitute the skeleton of the website information architecture.'

    def handle(self, *args, **options):
        """The default function Django BaseCommand needs to run."""
        home_page_queryset = HomePage.objects.live()
        home_page_queryset.update(
            slug_en="home",
            slug="home",
            url_path_en="/home/",
            url_path="/home/",
            title_en="Home",
            title="Home"
        )
        home_page = home_page_queryset.first()
        if home_page is not None:
            home_page.save()

            self.stdout.write(self.style.SUCCESS('Successfully fixed home page...'))

            default_pages = [
                {"model": AboutPage, "title": "About", "slug": "about"},
                {"model": ContactPage, "title": "Contact", "slug": "contact"},
                {"model": EventIndexPage, "title": "Events", "slug": "events"},
                {"model": GuidanceAndSupportPage, "title": "Guidance and support", "slug": "guidance_and_support"},
                {"model": NewsIndexPage, "title": "News", "slug": "news"},
            ]

            for default_page in default_pages:
                default_page_instance = default_page["model"].objects.live().first()
                if default_page_instance is None:
                    msg = 'No {} page! Creating about page...'.format(default_page["title"])
                    self.stdout.write(self.style.WARNING(msg))
                    default_page_instance = default_page["model"](
                        title_en=default_page["title"],
                        slug_en=default_page["slug"],
                        title=default_page["title"],
                        slug=default_page["slug"]
                    )
                    home_page.add_child(instance=default_page_instance)
                    default_page_instance.save_revision().publish()

            self.stdout.write(self.style.SUCCESS('Successfully checked/created default pages.'))
