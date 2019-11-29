import re

MAP = {
    '"': '«|»|“|”|„|‟|″|‴|⁗|‶|‷',
    "'": '‘|’|‚|‛|′|‵|‹|›',
    '‐': '‑|‒|-|—|―',
    '*': '⁎',
}


def normalise(string):
    normalised = string
    for k, v in MAP.items():
        normalised = re.sub('(%s)' % v, k, normalised)
    return normalised
