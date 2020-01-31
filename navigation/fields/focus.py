from wagtail.core.blocks import (
    CharBlock,
    URLBlock,
)
from navigation.fields import (
    AbstractHighlight,
)


class FocusItem(AbstractHighlight):

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
    link_label_en = CharBlock(
        help_text='Label for the secondary page link',
        label='Link label [en]',
    )
    link_label_fr = CharBlock(
        help_text='Label for the secondary page link',
        label='Link label [fr]',
        required=False,
    )
