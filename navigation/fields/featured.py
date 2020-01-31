from wagtail.core.blocks import (
    CharBlock,
    PageChooserBlock,
)
from navigation.fields import (
    AbstractHighlight,
)


class Featured(AbstractHighlight):

    class Meta:
        help_text = '''
                    <strong>Featured module</strong><br>
                    Internal page link and short description.<br>
                    Optional: secondary page link and label.
                    '''
        icon = 'pick'
        template = 'navigation/blocks/featured.html'

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
