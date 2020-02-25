"""Module to define featured items from the navigation menu."""

from wagtail.core.blocks import (
    CharBlock,
    PageChooserBlock,
)
from wagtail.images.blocks import ImageChooserBlock
from navigation.fields import (
    AbstractHighlight,
)


class Featured(AbstractHighlight):
    """Class for a featured item."""

    class Meta:
        help_text = '''
                    <strong>Featured module</strong><br>
                    Internal page link and short description.<br>
                    Optional: secondary page link and label.
                    '''
        icon = 'pick'
        template = 'navigation/blocks/featured.html'

    image = ImageChooserBlock(
        help_text='Optional: image for the module. If not selected, the page image will be used, or a fallback if not available',
        required=False,
    )
    secondary_page = PageChooserBlock(
        help_text='Optional: secondary page link',
        required=False,
    )
    link_label_en = CharBlock(
        help_text='Optional: label for the secondary page link',
        label='Link label [en]',
        required=False,
    )
    link_label_fr = CharBlock(
        help_text='Optional: label for the secondary page link',
        label='Link label [fr]',
        required=False,
    )
