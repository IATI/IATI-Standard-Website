"""Customise the formatting options shown to the editor when inserting images in the RichTextField editor."""

from wagtail.images.formats import Format, register_image_format, unregister_image_format

unregister_image_format("fullwidth")
unregister_image_format("left")
unregister_image_format("right")

register_image_format(Format('right', 'Align right', 'alignright', 'max-300x300'))
register_image_format(Format('left', 'Align left', 'alignleft', 'max-300x300'))
register_image_format(Format('fullwidth', 'Full width', 'full', 'max-1280x1280'))
