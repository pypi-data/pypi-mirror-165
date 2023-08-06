import re
import random
import string
import numpy as np

from .augment_type import AugmentType
from .utils import get_casing_probabilities, get_text, get_upper, get_lower


class PhoneAugment(object):

    def __init__(self, fake):
        self._fake = fake

    def generate(self, original_text, augment_type):

        original_text = original_text.strip() if original_text is not None else None

        if original_text is None:
            if augment_type != AugmentType.RANDOM:
                raise ValueError('Augment type needs to be random if original text is None')

        pager_probability = self.get_pager_probability(augment_type=augment_type, original_text=original_text)
        hyphen_replace_probability = self.get_hyphen_replace_probability(
            augment_type=augment_type, original_text=original_text
        )
        camel_case_probability, upper_case_probability, lower_case_probability = get_casing_probabilities(
            original_text=original_text, augment_type=augment_type
        )

        phone = np.random.choice(
            [self.get_phone_number, self.get_pager],
            p=[1 - pager_probability, pager_probability]
        )()

        phone = np.random.choice(
            [get_text, self.replace_hyphen],
            p=[1 - hyphen_replace_probability, hyphen_replace_probability]
        )(text=phone)

        # 80% of the time camel case, 10% of the time lowercase, 10% of the time uppercase
        return np.random.choice(
            [get_text, get_upper, get_lower],
            p=[camel_case_probability, upper_case_probability, lower_case_probability]
        )(phone).strip()

    def get_phone_number(self):
        return np.random.choice([self._fake.phone_number, self._fake.mobile_number], p=[0.5, 0.5])()

    def get_pager(self):
        prefix = random.choice(['p', 'x', 'b', '', ''])
        number_of_digits = np.random.randint(3, 7)
        return (
                prefix +
                random.choice(string.digits) +
                random.choice(['-', '']) +
                str(self._fake.random_number(number_of_digits, fix_len=True))
        )

    @staticmethod
    def replace_hyphen(text):
        if np.random.rand() <= 0.8:
            return text.replace('-', '.')
        else:
            return text.replace('-', random.choice(r'*;^~'))

    @staticmethod
    def get_pager_probability(augment_type, original_text):
        final_regex = r'[pxb](\d{4,}|\d+[-]\d+)'
        if original_text is not None \
                and (re.search(final_regex, original_text, flags=re.IGNORECASE) or len(original_text) <= 5):
            pager = True
        else:
            pager = False
        if augment_type == AugmentType.RANDOM:
            return 0.2

        if pager:
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

    @staticmethod
    def get_hyphen_replace_probability(augment_type, original_text):
        final_regex = r'\d-\d'
        if original_text is not None and re.search(final_regex, original_text, flags=re.IGNORECASE):
            hyphen = True
        else:
            hyphen = False

        if augment_type == AugmentType.RANDOM:
            return 0.2

        if hyphen:
            if augment_type == AugmentType.MIMIC:
                return 0.0
            elif augment_type == AugmentType.MIMIC_PROBABILITY:
                return 0.2
            else:
                raise ValueError('Invalid augment type')
        else:
            if augment_type == AugmentType.MIMIC:
                return 1.0
            elif augment_type == AugmentType.MIMIC_PROBABILITY:
                return 0.8
            else:
                raise ValueError('Invalid augment type')
