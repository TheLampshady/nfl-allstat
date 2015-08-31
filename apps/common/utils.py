import logging
from difflib import SequenceMatcher


def best_match(term, choice_list, default=None, threshold=0):
    max_ratio = 0
    value = default

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