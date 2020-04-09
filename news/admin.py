"""Module for registering admin models for the news app."""

from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register
)
from news.models import NewsPage, NewsCategory


def categories(obj):
    return ', '.join([str(x) for x in obj.news_categories.all()])


class NewsPageAdmin(ModelAdmin):
    model = NewsPage
    menu_icon = 'doc-full'
    menu_order = 100
    menu_label = 'News pages'
    list_display = ('title', 'date', categories, )
    search_fields = ('title', 'content_editor', )


class NewsCategoryAdmin(ModelAdmin):
    model = NewsCategory
    menu_icon = 'tag'
    menu_order = 110
    menu_label = 'Categories'
    list_display = ('name', 'slug', )
    search_fields = ('name', 'slug', )


class NewsAdminGroup(ModelAdminGroup):
    menu_label = 'News'
    menu_icon = 'doc-full'
    menu_order = 120
    items = (NewsPageAdmin, NewsCategoryAdmin, )


modeladmin_register(NewsAdminGroup)
