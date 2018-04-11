from django.core.management.base import BaseCommand, CommandError
from home.models import HomePage
from about.models import AboutPage
from contact.models import ContactPage
from events.models import EventIndexPage
from guidance_and_support.models import GuidanceAndSupportPage
from news.models import NewsIndexPage

from django.conf import settings

class Command(BaseCommand):
    """A command for manage.py that first rectifies some database problems with the HomePage model created by wagtail-modeltranslation and then creates the top-level default pages from the infrastructure architecture.

       The home_page needed a queryset update as well as its individual field update before the HomePage model was allowed to save in the CMS.
       I believe this is because the update method bypasses the validation of the save method and writes directly to the database, but the model then needs to be updated with save.

       TODO: If wagtail-modeltranslation or django-modeltranslation update, this command may no longer need to edit the home page.
    """
    help = 'Create the default pages that constitute the skeleton of the website information architecture'
    def handle(self, *args, **options):
        """The default function Django BaseCommand needs to run"""
        home_page_queryset = HomePage.objects.live()
        home_page = home_page_queryset.first()
        if home_page is not None:
            home_page_queryset.update(url_path_en="/home/", url_path="/home/")
            home_page.title_en = "Home"
            home_page.slug_en = "home"
            home_page.url_path_en = "/home/"
            home_page.title = "Home"
            home_page.slug = "home"
            home_page.url_path = "/home/"

            self.stdout.write(self.style.SUCCESS('Successfully fixed home page...'))

            about_page = AboutPage.objects.live().first()
            if about_page is None:
                self.stdout.write(self.style.WARNING('No about page! Creating about page...'))
                about_page = AboutPage(title_en="About", slug_en="about", title="About", slug="about")
                home_page.add_child(instance=about_page)
                about_page.save_revision().publish()
                about_page.save()

            contact_page = ContactPage.objects.live().first()
            if contact_page is None:
                self.stdout.write(self.style.WARNING('No contact page! Creating page...'))
                contact_page = ContactPage(title_en="Contact", slug_en="contact", title="Contact", slug="contact")
                home_page.add_child(instance=contact_page)
                contact_page.save_revision().publish()
                contact_page.save()

            event_index_page = EventIndexPage.objects.live().first()
            if event_index_page is None:
                self.stdout.write(self.style.WARNING('No event index page! Creating page...'))
                event_index_page = EventIndexPage(title_en="Events", slug_en="events", title="Events", slug="events")
                home_page.add_child(instance=event_index_page)
                event_index_page.save_revision().publish()
                event_index_page.save()

            guidance_and_support_page = GuidanceAndSupportPage.objects.live().first()
            if guidance_and_support_page is None:
                self.stdout.write(self.style.WARNING('No guidance and support page! Creating page...'))
                guidance_and_support_page = GuidanceAndSupportPage(title_en="Guidance and support", slug_en="guidance_and_support", title="Guidance and support", slug="guidance_and_support")
                home_page.add_child(instance=guidance_and_support_page)
                guidance_and_support_page.save_revision().publish()
                guidance_and_support_page.save()

            news_index_page = NewsIndexPage.objects.live().first()
            if news_index_page is None:
                self.stdout.write(self.style.WARNING('No news page! Creating page...'))
                news_index_page = NewsIndexPage(title_en="News", slug_en="news", title="News", slug="news")
                home_page.add_child(instance=news_index_page)
                news_index_page.save_revision().publish()
                news_index_page.save()

            home_page.save()

            self.stdout.write(self.style.SUCCESS('Successfully checked/created default pages.'))
