import re

MAP = {
    '"': '«|»|“|”|„|‟|″|‴|⁗|‶|‷',
    "'": '‘|’|‚|‛|′|‵|‹|›',
    '‐': '‑|‒|-|—|―',
    '*': '⁎',
}


def normalise(string):
	"""Normalise text following the MAP."""
    normalised = string
    for k, v in MAP.items():
        normalised = re.sub('(%s)' % v, k, normalised)
    return normalised
