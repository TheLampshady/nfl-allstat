import logging
from difflib import SequenceMatcher


def best_match(term, choice_list, default=None, set_threshold=False):
    max_ratio = 0
    value = default
    if len(term) < 6:
        threshold_delta = 0
    elif len(term) > 16:
        threshold_delta = 5
    else:
        threshold_delta = (len(term)-5) / 2
    threshold = 90 + threshold_delta

    for choice in choice_list:
        check = choice[1] if isinstance(choice, tuple) else choice
        match = int(SequenceMatcher(None, term, check).ratio() * 100)
        if match > max_ratio:
            value = choice
            max_ratio = match

    if max_ratio < threshold:
        logging.info("Hard Match: Ratio %s | Term %s | Choice %s" %
                     (max_ratio, term, value))
        value = default

    return value


def best_match_test(term, choice_list, default='other', threshold=0):
    max_ratio = 0
    value = default

    for choice in choice_list:
        check = choice[1] if isinstance(choice, tuple) else choice
        match = int(SequenceMatcher(None, term, check).ratio() * 100)
        if match > max_ratio:
            value = choice
            max_ratio = match


    return max_ratio, value