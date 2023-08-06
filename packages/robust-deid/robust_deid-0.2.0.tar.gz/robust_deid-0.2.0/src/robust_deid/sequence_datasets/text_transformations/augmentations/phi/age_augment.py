import re
import random
import string
import numpy as np
from collections import namedtuple

from .augment_type import AugmentType
from .utils import get_casing_probabilities, get_text, get_upper, get_lower


class AgeAugment(object):

    def __init__(self, fake):
        self._fake = fake

    def generate(
            self,
            original_text,
            augment_type
    ):

        original_text = original_text.strip() if original_text is not None else None

        if original_text is None:
            if augment_type != AugmentType.RANDOM:
                raise ValueError('Augment type needs to be random if original text is None')

        (
            one_digit_probability,
            two_digit_probability,
            three_digit_probability,
            prefix,
            suffix,
        ) = self.get_age_digits_probability(augment_type=augment_type, original_text=original_text)

        camel_case_probability, upper_case_probability, lower_case_probability = get_casing_probabilities(
            original_text=original_text, augment_type=augment_type
        )

        age_digits = np.random.choice(
            [self.get_one_age, self.get_two_age, self.get_three_age],
            p=[one_digit_probability, two_digit_probability, three_digit_probability]
        )()
        age = f'{prefix}{age_digits}{suffix}'

        return np.random.choice(
            [get_text, get_upper, get_lower],
            p=[camel_case_probability, upper_case_probability, lower_case_probability]
        )(age).strip()

    @staticmethod
    def get_one_age():
        return random.choice(string.digits.replace('0', ''))

    @staticmethod
    def get_two_age():
        return random.choice(string.digits) + random.choice(string.digits)

    @staticmethod
    def get_three_age():
        return '1' + random.choice(string.digits) + random.choice(string.digits)

    @staticmethod
    def get_age_digits_probability(augment_type, original_text):
        suffix = r'(\d{1,4})((\W*)(s|years|year|yo|yr|yrs|y.o|y/o|f|m|y)(\W*)(old|f|m|o)?)'
        prefix = r'\b((m|f)\W*)(\d{1,4})\b'
        only_num = r'\b(\d{1,4})\b'
        patterns = [suffix, prefix, only_num]
        index = None
        match = None
        for i, pattern in enumerate(patterns):
            match = re.search(pattern, original_text, flags=re.IGNORECASE)
            index = i
            if match:
                break
        AgeDigits = namedtuple(
            'AgeDigits',
            [
                'one_digit_probability',
                'two_digit_probability',
                'three_digit_probability',
                'prefix',
                'suffix'
            ]
        )

        if augment_type == AugmentType.RANDOM or match is None:
            return AgeDigits(0.1, 0.8, 0.1, '', '')

        if index == 0:
            if len(match.group(1)) == 1:
                if augment_type == AugmentType.MIMIC:
                    return AgeDigits(1.0, 0.0, 0.0, '', match.group(2))
                elif augment_type == AugmentType.MIMIC_PROBABILITY:
                    return AgeDigits(0.8, 0.1, 0.1, '', match.group(2))
                else:
                    raise ValueError('Invalid augment type')
            elif len(match.group(1)) == 3:
                if augment_type == AugmentType.MIMIC:
                    return AgeDigits(0.0, 0.0, 1.0, '', match.group(2))
                elif augment_type == AugmentType.MIMIC_PROBABILITY:
                    return AgeDigits(0.1, 0.1, 0.8, '', match.group(2))
                else:
                    raise ValueError('Invalid augment type')
            else:
                if augment_type == AugmentType.MIMIC:
                    return AgeDigits(0.0, 1.0, 0.0, '', match.group(2))
                elif augment_type == AugmentType.MIMIC_PROBABILITY:
                    return AgeDigits(0.1, 0.8, 0.1, '', match.group(2))
                else:
                    raise ValueError('Invalid augment type')
        elif index == 1:
            if len(match.group(3)) == 1:
                if augment_type == AugmentType.MIMIC:
                    return AgeDigits(1.0, 0.0, 0.0, match.group(1), '')
                elif augment_type == AugmentType.MIMIC_PROBABILITY:
                    return AgeDigits(0.8, 0.1, 0.1, match.group(1), '')
                else:
                    raise ValueError('Invalid augment type')
            elif len(match.group(3)) == 3:
                if augment_type == AugmentType.MIMIC:
                    return AgeDigits(0.0, 0.0, 1.0, match.group(1), '')
                elif augment_type == AugmentType.MIMIC_PROBABILITY:
                    return AgeDigits(0.1, 0.1, 0.8, match.group(1), '')
                else:
                    raise ValueError('Invalid augment type')
            else:
                if augment_type == AugmentType.MIMIC:
                    return AgeDigits(0.0, 1.0, 0.0, match.group(1), '')
                elif augment_type == AugmentType.MIMIC_PROBABILITY:
                    return AgeDigits(0.1, 0.8, 0.1, match.group(1), '')
                else:
                    raise ValueError('Invalid augment type')
        elif index == 2:
            if len(match.group(1)) == 1:
                if augment_type == AugmentType.MIMIC:
                    return AgeDigits(1.0, 0.0, 0.0, '', '')
                elif augment_type == AugmentType.MIMIC_PROBABILITY:
                    return AgeDigits(0.8, 0.1, 0.1, '', '')
                else:
                    raise ValueError('Invalid augment type')
            elif len(match.group(1)) == 3:
                if augment_type == AugmentType.MIMIC:
                    return AgeDigits(0.0, 0.0, 1.0, '', '')
                elif augment_type == AugmentType.MIMIC_PROBABILITY:
                    return AgeDigits(0.1, 0.1, 0.8, '', '')
                else:
                    raise ValueError('Invalid augment type')
            else:
                if augment_type == AugmentType.MIMIC:
                    return AgeDigits(0.0, 1.0, 0.0, '', '')
                elif augment_type == AugmentType.MIMIC_PROBABILITY:
                    return AgeDigits(0.1, 0.8, 0.1, '', '')
                else:
                    raise ValueError('Invalid augment type')
