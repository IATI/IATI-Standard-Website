from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.admin.edit_handlers import FieldRowPanel, FieldPanel, InlinePanel, PageChooserPanel, StreamFieldPanel
from wagtail.core.models import Orderable
from common.utils import ForeignKeyField
from dashboard.edit_handlers import MultiFieldPanel, HelpPanel
from navigation.fields import navigation


class AbstractLink(models.Model):
    class Meta:
        abstract = True

    label = models.CharField(
        max_length=255,
        verbose_name='Label'
    )
    page = ForeignKeyField(
        model='wagtailcore.Page',
        required=True,
    )
    panels = [
        HelpPanel(
            content='Primary menu item',
            wrapper_class='help-block help-text-section-header',
        ),
        HelpPanel(
            content='<strong>Primary menu link</strong><br>Top level page for the primary menu item and associated link label.',
        ),
        PageChooserPanel('page'),
        FieldRowPanel(children=(
            FieldPanel('label'),
        )),
    ]

    translation_fields = ['label']


class PrimaryMenuLinks(Orderable, AbstractLink):
    item = ParentalKey('PrimaryMenu', related_name='primary_menu_links')
    meganav = navigation(blank=True)

    panels = AbstractLink.panels + [
        HelpPanel(
            content='''
                        <strong>Meganav</strong><br>
                        Optional: meganav module for the the primary menu item.<br><br>
                        Select one of the available module types:<br>
                        <ul class="help-list">
                            <li><strong>Type a</strong>: page lists, nested page lists (max 4 items)</li>
                            <li><strong>Type b</strong>: page list, featured (max 2 items)</li>
                            <li><strong>Type c</strong>: focus items, page lists, secondary highlight (max 7 items)</li>
                        </ul>
                    ''',
        ),
        StreamFieldPanel('meganav'),
    ]

    translation_fields = AbstractLink.translation_fields + ['meganav']


class UtilityMenuLinks(Orderable, AbstractLink):
    item = ParentalKey('UtilityMenu', related_name='utility_menu_links')


class UsefulLinksMenu(Orderable, AbstractLink):
    item = ParentalKey('UsefulLinks', related_name='useful_links')


@register_setting
class PrimaryMenu(ClusterableModel, BaseSetting):

    panels = [
        MultiFieldPanel(
            [
                InlinePanel('primary_menu_links', label='Primary menu item'),
            ],
            heading='Primary menu',
        ),
    ]


@register_setting
class UtilityMenu(ClusterableModel, BaseSetting):

    panels = [
        MultiFieldPanel(
            [
                InlinePanel('utility_menu_links', label='Utility menu link'),
            ],
            heading='Utility menu',
        ),
    ]


@register_setting
class UsefulLinks(ClusterableModel, BaseSetting):

    panels = [
        MultiFieldPanel(
            [
                InlinePanel('useful_links', label='Useful link'),
            ],
            heading='Useful links',
        ),
    ]
