import re
import random
import string
from collections import namedtuple

from .augment_type import AugmentType


def get_casing_probabilities(augment_type, original_text):
    Casing = namedtuple(
        'Casing', ['camel_case_probability', 'upper_case_probability', 'lower_case_probability']
    )

    if augment_type == AugmentType.RANDOM:
        return Casing(0.5, 0.25, 0.25)
    if original_text.isupper():
        if augment_type == AugmentType.MIMIC:
            return Casing(0.0, 1.0, 0.0)
        elif augment_type == AugmentType.MIMIC_PROBABILITY:
            return Casing(0.1, 0.8, 0.1)
        else:
            raise ValueError('Invalid augment type')
    elif original_text.islower():
        if augment_type == AugmentType.MIMIC:
            return Casing(0.0, 0.0, 1.0)
        elif augment_type == AugmentType.MIMIC_PROBABILITY:
            return Casing(0.1, 0.1, 0.8)
        else:
            raise ValueError('Invalid augment type')
    else:
        if augment_type == AugmentType.MIMIC:
            return Casing(1.0, 0.0, 0.0)
        elif augment_type == AugmentType.MIMIC_PROBABILITY:
            return Casing(0.8, 0.1, 0.1)
        else:
            raise ValueError('Invalid augment type')


def get_acronym_probability(augment_type, original_text):
    acronym_regex = r'^[A-Z][a-zA-Z\.]*[A-Z]\.?$'
    if original_text is not None and re.search(acronym_regex, original_text):
        acronym = True
    else:
        acronym = False
    if augment_type == AugmentType.RANDOM:
        return 0.2
    if acronym:
        if augment_type == AugmentType.MIMIC:
            return 1.0
        elif augment_type == AugmentType.MIMIC_PROBABILITY:
            return 0.8
        else:
            raise ValueError('Invalid augment type')
    else:
        if augment_type == AugmentType.MIMIC:
            return 0.0
        elif augment_type == AugmentType.MIMIC_PROBABILITY:
            return 0.2
        else:
            raise ValueError('Invalid augment type')


def get_text(text):
    return text


def get_upper(text):
    return text.upper()


def get_lower(text):
    return text.lower()


def get_uppercase_letter():
    return random.choice(string.ascii_uppercase)


def get_lowercase_letter():
    return random.choice(string.ascii_lowercase)


def get_number():
    return random.choice(string.digits)


def get_sep_character():
    return random.choice(r'#*./;:^~|_-')


def shuffle_word(word):
    word = list(word)
    random.shuffle(word)
    return ''.join(word)
