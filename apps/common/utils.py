import logging
from difflib import SequenceMatcher


def best_match(term, choices, default='other', threshold=0):
    max_ratio = 0
    value = default

    for choice in choices:
        match = (SequenceMatcher(None, term, choice).ratio() * 100)
        if match > max_ratio:
            value = choice
            max_ratio = match

    if max_ratio < threshold:
        value = default

    if max_ratio < 75:
        logging.info("Hard Match: Ratio %s | Term %s | Choice %s" % \
              (max_ratio, term, value))
    return value