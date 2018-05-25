import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.core import hooks
from draftjs_exporter.dom import DOM
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineEntityElementHandler
from django.utils.html import format_html_join
from django.conf import settings


@hooks.register('register_rich_text_features')
def register_anchor_feature(features):
    features.default_features.append('anchor')
    """
    Registering the `anchor` feature, which uses the `ANCHOR` Draft.js entity type,
    and is stored as HTML with a `<a href>` tag.
    """
    feature_name = 'anchor'
    type_ = 'ANCHOR'

    control = {
        'type': type_,
        'label': 'A',
        'description': 'Anchor',
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.EntityFeature(control)
    )

    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {'a[href]': AnchorEntityElementHandler(type_)},
        'to_database_format': {'entity_decorators': {type_: anchor_entity_decorator}},
    })


def anchor_entity_decorator(props):
    """
    Draft.js ContentState to database HTML.
    Converts the ANCHOR entities into an a tag.
    """
    return DOM.create_element('a', {
        'href': props['href'],
    }, props['children'])


class AnchorEntityElementHandler(InlineEntityElementHandler):
    """
    Database HTML to Draft.js ContentState.
    Converts the a tag into an ANCHOR entity, with the right data.
    """
    mutability = 'IMMUTABLE'

    def get_attribute_data(self, attrs):
        """
        Take the ``href`` value from the ``href`` HTML attribute.
        """
        return {
            'href': attrs['href'],
        }


@hooks.register('insert_editor_js')
def anchor_editor_js():
    js_files = [
        'wagtailadmin/js/draftail.js',
        'home/js/anchor.js',
    ]
    js_includes = format_html_join('\n', '<script src="{0}{1}"></script>', ((settings.STATIC_URL, filename) for filename in js_files))
    return js_includes
