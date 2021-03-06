# Generated by Django 2.2.9 on 2020-04-03 14:41

from django.db import migrations, transaction
from importlib import import_module

DATA = {
    'title': 'Search iatistandard.org',
    'slug': 'search',
    'heading': 'Search iatistandard.org',
    'heading_en': 'Search iatistandard.org',
    'heading_fr': 'Recherche iatistandard.org',
}


class Migration(migrations.Migration):

    def add_search_page(apps, schema_editor):
        """Add a new search page with minimal data"""
        # if the models no longer exists, return directly
        try:
            HomePage = import_module('home.models').HomePage
            SearchPage = import_module('search.models').SearchPage
            NewsIndexPage = import_module('news.models').NewsIndexPage
        except Exception:
            return

        # test for the existance of a news index page
        # an empty database won't have this, but it needs wrapping in an atomic transaction so we can back out successfully
        # https://docs.djangoproject.com/en/2.2/topics/db/transactions/#controlling-transactions-explicitly
        news_index_page_count = 0
        try:
            with transaction.atomic():
                news_index_page_count = NewsIndexPage.objects.all().count()
        except Exception:
            return

        # only proceed if we have a news indes page (e.g. not an empty database)
        if news_index_page_count:

            # return if we already have a search page
            if SearchPage.objects.all().first():
                return

            parent = HomePage.objects.all().first()
            new_page = SearchPage()
            for field, value in DATA.items():
                setattr(new_page, field, value)

            parent.add_child(instance=new_page)
            new_page.save_revision().publish()

    dependencies = [
        ('search', '0003_add_search_page'),
    ]

    operations = [
        migrations.RunPython(add_search_page),
    ]
