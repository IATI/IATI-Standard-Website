"""Module for the Focus Item class."""

from wagtail.blocks import (
    BooleanBlock,
    CharBlock,
    URLBlock,
)
from navigation.fields import (
    AbstractHighlight,
)


class FocusItem(AbstractHighlight):
    """Class to define the focus item in a navigation menu."""

    class Meta:
        help_text = '''
                    <strong>Focus item module</strong><br>
                    Internal page link, short description, and link label.<br>
                    Optional: external url for secondary link, display secondary link as button.
                    '''
        icon = 'pick'
        template = 'navigation/blocks/focus_item.html'

    external_url = URLBlock(
        help_text='Optional: external URL for the secondary link. Defaults to the selected page link',
        required=False,
    )
    link_label = CharBlock(
        help_text='Label for the secondary page link',
        label='Link label',
    )
    use_button_style = BooleanBlock(
        help_text='Optional: if checked, the secondary link will display as a button',
        required=False,
    )
