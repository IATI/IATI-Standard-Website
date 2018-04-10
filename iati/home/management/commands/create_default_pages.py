from django.core.management.base import BaseCommand, CommandError
from home.models import HomePage
from about.models import AboutPage
from contact.models import ContactPage
from events.models import EventIndexPage
from guidance_and_support import GuidanceAndSupportPage
from news import NewsIndexPage

class Command(BaseCommand):
    help = 'Create the default pages that constitute the skeleton of the website information architecture'
    def handle(self, *args, **options):
        home_page = HomePage.objects.live().first()
        if home_page is not None:
            home_page.update(url_path_en="/home/",title_en="Home",slug_en="home")
        self.stdout.write(self.style.WARNING('Successfully fixed home page'))
            
        about_page = AboutPage.objects.live().first()
        if about_page is None:
            self.stdout.write(self.style.WARNING('No about page! Creating about page...'))
            about_page = AboutPage(title_en="About",slug_en="about")
            home_page.add_child(about_page)
            about_page.save_revision().publish()
            
        contact_page = ContactPage.objects.live().first()
        if contact_page is None:
            self.stdout.write(self.style.WARNING('No contact page! Creating page...'))
            contact_page = ContactPage(title_en="Contact",slug_en="contact")
            home_page.add_child(contact_page)
            contact_page.save_revision().publish()
            
        event_index_page = EventIndexPage.objects.live().first()
        if event_index_page is None:
            self.stdout.write(self.style.WARNING('No event index page! Creating page...'))
            event_index_page = EventIndexPage(title_en="Events",slug_en="events")
            home_page.add_child(event_index_page)
            event_index_page.save_revision().publish()
            
        guidance_and_support_page = GuidanceAndSupportPage.objects.live().first()
        if guidance_and_support_page is None:
            self.stdout.write(self.style.WARNING('No guidance and support page! Creating page...'))
            guidance_and_support_page = GuidanceAndSupportPage(title_en="Guidance and support",slug_en="guidance_and_support")
            home_page.add_child(guidance_and_support_page)
            guidance_and_support_page.save_revision().publish()
            
        news_index_page = NewsIndexPage.objects.live().first()
        if news_index_page is None:
            self.stdout.write(self.style.WARNING('No news page! Creating page...'))
            news_index_page = NewsIndexPage(title_en="News",slug_en="news")
            home_page.add_child(news_index_page)
            news_index_page.save_revision().publish()
            
        self.stdout.write(self.style.SUCCESS('Successfully checked/created default pages...'))
