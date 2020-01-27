from django.db import models
from django.utils.functional import cached_property
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.admin.edit_handlers import FieldRowPanel, FieldPanel, InlinePanel, PageChooserPanel, StreamFieldPanel
from wagtail.core.models import Orderable
from common.utils import ForeignKeyField
from dashboard.edit_handlers import MultiFieldPanel, HelpPanel
from navigation.fields import navigation
from navigation.utils import get_localised_field_value


class AbstractLink(models.Model):
    class Meta:
        abstract = True

    label_en = models.CharField(
        max_length=255,
        verbose_name='Label [en]'
    )
    label_fr = models.CharField(
        max_length=255,
        verbose_name='Label [fr]',
        blank=True,
    )
    page = ForeignKeyField(
        model='wagtailcore.Page',
        required=True,
    )
    panels = [
        HelpPanel(
            heading='Primary menu page link',
            content='Top level page for the primary navigation item and associated link label.',
        ),
        PageChooserPanel('page'),
        FieldRowPanel(children=(
            FieldPanel('label_en'),
            FieldPanel('label_fr'),
        )),
    ]


class PrimaryMenuLinks(Orderable, AbstractLink):
    item = ParentalKey('PrimaryMenu', related_name='primary_menu_links')
    meganav = navigation(blank=True)

    panels = AbstractLink.panels + [
        HelpPanel(
            content='Optional: meganav module for the the primary navigation item. Select one of the available module types',
        ),
        StreamFieldPanel('meganav'),
    ]

    @cached_property
    def label(self):
        return get_localised_field_value(self, 'label')


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
