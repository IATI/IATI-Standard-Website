"""Model definitions for the using_data app."""

from about.models import AboutSubPage, AboutPage
from home.models import AbstractContentPage
from wagtail.core.fields import StreamField
from wagtail.core.blocks import RichTextBlock, StreamBlock


class UsingDataPage(AboutPage):
    """A page model for the Using IATI data page. Inherits all from AbstractContentPage."""

    subpage_types = ['using_data.ToolsIndexPage', 'about.AboutSubPage']

    def get_context(self, request, *args, **kwargs):
        """Overwrite the default wagtail get_context function to add all subpages of UsingDataPage."""
        context = super(UsingDataPage, self).get_context(request)

        context['subpages'] = AboutSubPage.objects.child_of(self)
        context['toolsindex'] = ToolsIndexPage.objects.child_of(self).first()
        return context


class ToolBoxBlock(StreamBlock):
    """A block for holding a list of tool pages."""

    tool_box_text = RichTextBlock(required=False)


class ToolsIndexPage(AbstractContentPage):
    """A page model for the Tools & Resources page. Inherits all from AboutSubPage."""

    parent_page_types = ['using_data.UsingDataPage']
    subpage_types = ['using_data.ToolsPage']

    tool_box_editor = StreamField(ToolBoxBlock, null=True, blank=True)

    translation_fields = AbstractContentPage.translation_fields + ['tool_box_editor']


class ToolsPage(AboutSubPage):
    """A page model for single Tools & Resources pages. Inherits all from AboutSubPage."""

    parent_page_types = ['using_data.ToolsIndexPage']
