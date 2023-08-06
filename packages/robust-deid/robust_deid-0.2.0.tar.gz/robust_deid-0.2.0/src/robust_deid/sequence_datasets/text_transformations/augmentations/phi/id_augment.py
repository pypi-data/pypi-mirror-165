import re
import random
import numpy as np

from .augment_type import AugmentType
from .utils import (
    get_casing_probabilities,
    get_text,
    get_upper,
    get_lower,
    get_uppercase_letter,
    get_lowercase_letter,
    get_sep_character,
    get_number,
)


class IDAugment(object):

    def __init__(self, fake, regex_min_length=4, regex_max_length=13):
        self._fake = fake
        self._regex_min_length = regex_min_length
        self._regex_max_length = regex_max_length

    def generate(
            self,
            original_text,
            augment_type
    ):

        original_text = original_text.strip() if original_text is not None else None

        if original_text is None:
            if augment_type != AugmentType.RANDOM:
                raise ValueError('Augment type needs to be random if original text is None')

        camel_case_probability, upper_case_probability, lower_case_probability = get_casing_probabilities(
            original_text=original_text, augment_type=augment_type
        )

        id_text = self.get_id_text(augment_type=augment_type, original_text=original_text)

        # 80% of the time camel case, 10% of the time lowercase, 10% of the time uppercase
        return np.random.choice(
            [get_text, get_upper, get_lower],
            p=[camel_case_probability, upper_case_probability, lower_case_probability]
        )(id_text).strip()

    def get_random_id(self):
        return random.choice([
            self._fake.bban,
            self._fake.iban,
            self._fake.swift,
            self._fake.vat_id,
            self._fake.ean,
            self._fake.gsis,
            self._fake.iana_id,
            self._fake.invalid_ssn,
            self._fake.license_plate,
            self._fake.isbn10,
            self._fake.isbn13,
            self._fake.itin,
            self._fake.pagibig,
            self._fake.ssn,
            self._fake.umid
        ])()

    def get_id_text(self, augment_type, original_text):
        pattern_1 = r'\b[a-zA-Z0-9]+(\W|_)+[a-zA-Z0-9\W_]+\b'
        pattern_2 = r'\b[a-zA-Z0-9]+\b'

        patterns = [pattern_1, pattern_2]
        match = None
        for i, pattern in enumerate(patterns):
            match = re.search(pattern, original_text, flags=re.IGNORECASE)
            if match:
                break
        return self.permute_id_text(augment_type, match.group(0) if match is not None else None)

    def permute_id_text(self, augment_type, text):
        id_text = ''
        if augment_type == AugmentType.RANDOM or text is None:
            return self.get_random_id()

        sep_character = get_sep_character()
        for char in list(text):
            if char.isalpha():
                if char.isupper():
                    if augment_type == AugmentType.MIMIC:
                        p = [1.0, 0.0, 0.0]
                    elif augment_type == AugmentType.MIMIC_PROBABILITY:
                        p = [0.8, 0.1, 0.1]
                    else:
                        raise ValueError('Invalid augment type')
                else:
                    if augment_type == AugmentType.MIMIC:
                        p = [0.0, 1.0, 0.0]
                    elif augment_type == AugmentType.MIMIC_PROBABILITY:
                        p = [0.1, 0.8, 0.1]
                    else:
                        raise ValueError('Invalid augment type')
                id_text += np.random.choice(
                    [get_uppercase_letter, get_lowercase_letter, get_number], p=p
                )()
            elif char.isnumeric():
                if augment_type == AugmentType.MIMIC:
                    p = [0.0, 0.0, 1.0]
                elif augment_type == AugmentType.MIMIC_PROBABILITY:
                    p = [0.1, 0.1, 0.8]
                else:
                    raise ValueError('Invalid augment type')
                id_text += np.random.choice(
                    [get_uppercase_letter, get_lowercase_letter, get_number], p=p
                )()
            else:
                sep = re.search(r'\W|_', char, flags=re.IGNORECASE).group(0)
                if augment_type == AugmentType.MIMIC:
                    p = [1.0, 0.0]
                elif augment_type == AugmentType.MIMIC_PROBABILITY:
                    p = [0.8, 0.2]
                else:
                    raise ValueError('Invalid augment type')
                id_text += np.random.choice([sep, sep_character], p=p)
        # id_text = re.sub(r'(\W)\1+', f'\1', shuffle_word(id_text))
        return id_text
