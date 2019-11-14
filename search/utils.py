from haystack.utils.highlighting import Highlighter


class CustomHighlighter(Highlighter):

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
