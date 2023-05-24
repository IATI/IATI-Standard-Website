from django.db import models
from django.utils.functional import cached_property
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.admin.panels import FieldRowPanel, FieldPanel, InlinePanel, PageChooserPanel
from wagtail.models import Orderable
from common.utils import ForeignKeyField
from dashboard.edit_handlers import MultiFieldPanel, HelpPanel
from navigation.fields import navigation
from navigation.utils import get_localised_field_value


class AbstractLink(models.Model):
    """Abstract class for a navigation link."""

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
        PageChooserPanel('page'),
        FieldRowPanel(children=(
            FieldPanel('label'),
        )),
    ]

    @cached_property
    def label(self):
        """Define localised menu label."""
        return get_localised_field_value(self, 'label')


class PrimaryMenuLinks(Orderable, AbstractLink):
    """Class for primary menu links."""

    item = ParentalKey('PrimaryMenu', related_name='primary_menu_links')
    meganav = navigation(blank=True)

    pre_panels = [
        HelpPanel(
            content='Primary menu item',
            wrapper_class='help-block help-text-section-header',
        ),
        HelpPanel(
            content='<strong>Primary menu link</strong><br>Top level page for the primary menu item and associated link label.',
        ),
    ]

    panels = pre_panels + AbstractLink.panels + [
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
        FieldPanel('meganav'),
    ]


class UtilityMenuLinks(Orderable, AbstractLink):
    """Class for utility menu links."""

    item = ParentalKey('UtilityMenu', related_name='utility_menu_links')

    pre_panels = [
        HelpPanel(
            content='<strong>Utility menu link</strong><br>Page for the utility menu item and associated link label.',
        ),
    ]

    panels = pre_panels + AbstractLink.panels


class UsefulLinksMenu(Orderable, AbstractLink):
    """Class for useful links menu."""

    item = ParentalKey('UsefulLinks', related_name='useful_links')

    pre_panels = [
        HelpPanel(
            content='<strong>Useful link</strong><br>Page for the useful link item and associated link label.',
        ),
    ]

    panels = pre_panels + AbstractLink.panels


@register_setting
class PrimaryMenu(ClusterableModel, BaseSiteSetting):
    """Class for primary menu settings panel definition."""

    panels = [
        MultiFieldPanel(
            [
                InlinePanel('primary_menu_links', label='Primary menu item'),
            ],
            heading='Primary menu',
        ),
    ]


@register_setting
class UtilityMenu(ClusterableModel, BaseSiteSetting):
    """Class for utility menu settings panel definition."""

    panels = [
        MultiFieldPanel(
            [
                InlinePanel('utility_menu_links', label='Utility menu link'),
            ],
            heading='Utility menu',
        ),
    ]


@register_setting
class UsefulLinks(ClusterableModel, BaseSiteSetting):
    """Class for useful links menu settings panel definition."""

    panels = [
        MultiFieldPanel(
            [
                InlinePanel('useful_links', label='Useful link'),
            ],
            heading='Useful links',
        ),
    ]
