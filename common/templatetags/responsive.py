from django import template
from wagtail.images.models import SourceImageIOError
from wagtail.images.templatetags.wagtailimages_tags import ImageNode
from django.utils.safestring import mark_safe
from common.templatetags.string_utils import uid

register = template.Library()


@register.tag(name="responsiveimage")
def responsiveimage(parser, token):
    bits = token.split_contents()[1:]
    image_expr = parser.compile_filter(bits[0])
    filter_spec = bits[1]
    remaining_bits = bits[2:]

    if remaining_bits[-2] == 'as':
        attrs = _parse_attrs(remaining_bits[:-2])
        # token is of the form {% responsiveimage self.photo max-320x200 srcset="filter_spec xyzw" [ attr="val" ... ] as img %}
        return ResponsiveImageNode(image_expr, filter_spec, attrs=attrs, output_var_name=remaining_bits[-1])
    else:
        # token is of the form {% responsiveimage self.photo max-320x200 srcset="filter_spec xyzw" [ attr="val" ... ] %}
        # all additional tokens should be kwargs, which become attributes
        attrs = _parse_attrs(remaining_bits)
        return ResponsiveImageNode(image_expr, filter_spec, attrs=attrs)


def _parse_attrs(bits):
    template_syntax_error_message = (
        '"responsiveimage" tag should be of the form '
        '{% responsiveimage self.photo max-320x200 srcset="fill-400x120 400w, fill-600x180 600w" sizes="100vw" [ custom-attr="value" ... ] %} or '
        '{% responsiveimage self.photo max-320x200 srcset="whatever" as img %}'
    )
    attrs = {}
    for bit in bits:
        try:
            name, value = bit.split('=')
        except ValueError:
            raise template.TemplateSyntaxError(template_syntax_error_message)

        if value[0] == value[-1] and value[0] in ('"', "'"):
            # If attribute value is in quotes, strip the quotes and store the attr as a string.
            attrs[name] = value[1:-1]
        else:
            # This attribute isn't in quotes, so it's a variable name. Send a Variable as the attr, so the
            # ResponsiveImageNode can render it based on the context it gets.
            attrs[name] = template.Variable(value)
    return attrs


class ResponsiveImageNode(ImageNode, template.Node):
    def render(self, context):
        try:
            image = self.image_expr.resolve(context)
        except template.VariableDoesNotExist:
            return ''

        if not image:
            return ''

        try:
            rendition = image.get_rendition(self.filter)
        except SourceImageIOError:
            # It's fairly routine for people to pull down remote databases to their
            # local dev versions without retrieving the corresponding image files.
            # In such a case, we would get a SourceImageIOError at the point where we try to
            # create the resized version of a non-existent image. Since this is a
            # bit catastrophic for a missing image, we'll substitute a dummy
            # Rendition object so that we just output a broken link instead.
            Rendition = image.renditions.model  # pick up any custom Image / Rendition classes that may be in use
            rendition = Rendition(image=image, width=0, height=0)
            rendition.file.name = 'not-found'

        # Parse srcset format into array of renditions.
        try:
            try:
                # Assume it's a Variable object, and try to resolve it against the context.
                srcset = self.attrs['srcset'].resolve(context)
            except AttributeError:
                # It's not a Variable, so assume it's a string.
                srcset = self.attrs['srcset']

            # Parse each src from the srcset.
            raw_sources = srcset.replace('"', '').split(',')

            srcset_renditions = []
            widths = []
            newsrcseturls = []

            for source in raw_sources:
                flt = source.strip().split(' ')[0]
                width = source.strip().split(' ')[1]

                '''
                Make retina sizes.
                This section will extract the sizes and widths,
                double them up, and add them to the srcset for retina versions.
                This srcset will also be passed to the responsive css filter, to be used for retina versions
                in the media queries.
                '''
                flt_bits = flt.split('-')
                flt_retina_values = []

                if flt_bits[1].lower().find('x'):
                    flt_values = flt_bits[1].split('x')
                else:
                    flt_values = flt_bits[1]

                for value in flt_values:
                    flt_retina_values.append(str(int(value) * 2))

                flt_retina = '%s-%s' % (flt_bits[0], 'x'.join(flt_retina_values))
                width_retina = '%sw' % (str(int(width.replace('w', '')) * 2))
                '''
                End of retina sizes.
                '''

                # cache widths to be re-appended after filter has been converted to URL
                widths.append(width)
                widths.append(width_retina)

                try:
                    srcset_renditions.append(image.get_rendition(flt))
                    srcset_renditions.append(image.get_rendition(flt_retina))
                except SourceImageIOError:
                    # pick up any custom Image / Rendition classes that may be in use
                    TmpRendition = image.renditions.model
                    tmprend = TmpRendition(image=image, width=0, height=0)
                    tmprend.file.name = 'not-found'

            for index, rend in enumerate(srcset_renditions):
                newsrcseturls.append(' '.join([rend.url, widths[index]]))

        except KeyError:
            newsrcseturls = []
            pass

        if self.output_var_name:
            rendition.srcset = ', '.join(newsrcseturls)

            # return the rendition object in the given variable
            context[self.output_var_name] = rendition
            return ''
        else:
            # render the rendition's image tag now
            resolved_attrs = {}
            for key in self.attrs:
                if key == 'srcset':
                    resolved_attrs[key] = ','.join(newsrcseturls)
                    continue

                try:
                    # Assume it's a Variable object, and try to resolve it against the context.
                    resolved_attrs[key] = self.attrs[key].resolve(context)
                except AttributeError:
                    # It's not a Variable, so assume it's a string.
                    resolved_attrs[key] = self.attrs[key]

            return rendition.img_tag(resolved_attrs)


@register.filter
def responsive_css(image, prefix='ri'):

    if not image or not image.srcset:
        return ''

    srcset = [x for x in image.srcset.split(',')]
    srcset = [[x.strip().split(' ')[0], x.strip().split(' ')[1]] for x in srcset]
    srcset = [[x[0], int(x[1].replace('w', ''))] for x in srcset]
    css = '<style scoped>'

    # create a counter, as we only want to render css every other time
    index = 0

    for size in srcset:
        # increment counter each time
        index += 1

        # skip every second item as they are the retina versions, of which we just want the src
        if index % 2 == 0:
            continue

        # set retina src to the next index in the srcset
        retina = srcset[index]

        # create the kwargs for the css
        kwargs = {
            'size': size[1],
            'prefix': prefix,
            'id': image.uid,
            'url': size[0],
            'url_2x': retina[0]
        }

        # render the css
        css += """
            @media all and (min-width: {size}px) {{
                #{prefix}{id} {{
                    background-image: url({url});
                    background-image: -webkit-image-set(url("{url}") 1x, url("{url_2x}") 2x);
                    background-image: image-set(url("{url}") 1x, url("{url_2x}") 2x);
                    background-position-y: center;
                }}
            }}

        """.format(**kwargs)

    css += '</style>'

    return mark_safe(css)


@register.filter
def responsive_id(image, prefix='ri'):
    if not image:
        return ''
    image.uid = uid()

    html = 'id="%s%s"' % (prefix, image.uid)
    return mark_safe(html)
