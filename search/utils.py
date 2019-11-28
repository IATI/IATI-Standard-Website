import html
from unidecode import unidecode
from haystack.utils.highlighting import Highlighter
from django.utils.html import strip_tags


class CustomHighlighter(Highlighter):

    original_text_block = ""

    def __init__(self, query, **kwargs):
        super().__init__(unidecode(query), **kwargs)

    def find_window(self, highlight_locations):
        if len(self.text_block) <= self.max_length:
            return (0, self.max_length)
        else:
            window = super().find_window(highlight_locations)
            try:
                offset = 30
                if window[0] > offset:
                    return (window[0] - offset, window[1] - offset)
            except Exception:
                return window
            return window

    def highlight(self, text_block):
        self.original_text_block = html.unescape(strip_tags(text_block))
        self.text_block = unidecode(self.original_text_block)

        highlight_locations = self.find_highlightable_words()
        start_offset, end_offset = self.find_window(highlight_locations)
        return self.render_html(highlight_locations, start_offset, end_offset)

    def render_html(self, highlight_locations=None, start_offset=None, end_offset=None):
        # Start by chopping the block down to the proper window.
        text = self.text_block[start_offset:end_offset]
        orig_text = self.original_text_block[start_offset:end_offset]

        # Invert highlight_locations to a location -> term list
        term_list = []

        for term, locations in highlight_locations.items():
            term_list += [(loc - start_offset, term) for loc in locations]

        loc_to_term = sorted(term_list)

        # Prepare the highlight template
        if self.css_class:
            hl_start = '<%s class="%s">' % (self.html_tag, self.css_class)
        else:
            hl_start = "<%s>" % (self.html_tag)

        hl_end = "</%s>" % self.html_tag

        # Copy the part from the start of the string to the first match,
        # and there replace the match with a highlighted version.
        highlighted_chunk = ""
        matched_so_far = 0
        prev = 0
        prev_str = ""

        for cur, cur_str in loc_to_term:
            # This can be in a different case than cur_str
            actual_term = text[cur: cur + len(cur_str)]
            orig_actual_term = orig_text[cur: cur + len(cur_str)]

            # Handle incorrect highlight_locations by first checking for the term
            if actual_term.lower() == cur_str:
                if cur < prev + len(prev_str):
                    continue

                highlighted_chunk += (
                    orig_text[prev + len(prev_str): cur] + hl_start + orig_actual_term + hl_end
                )
                prev = cur
                prev_str = cur_str

                # Keep track of how far we've copied so far, for the last step
                matched_so_far = cur + len(actual_term)

        # Don't forget the chunk after the last term
        highlighted_chunk += text[matched_so_far:]

        if start_offset > 0:
            highlighted_chunk = "...%s" % highlighted_chunk

        if end_offset < len(self.text_block):
            highlighted_chunk = "%s..." % highlighted_chunk

        return highlighted_chunk
