from django.db import models

from wagtail.core.models import Page

class AboutPage(Page):
    pass
    # parent_page_types = ['home.HomePage']
    # subpage_types = ['home.AboutSubpage']

#fffunction notes:

# Model would be something like:
#
# title
# intro (text area)
# content_editor
# The members assembly block in the sidebar is an optional item, the model for which should be something like:
#
# block_title
# block_content
# block_button_text
# block_button_url
# This block appears on several templates
