import re
import random
import numpy as np
from collections import namedtuple

from .augment_type import AugmentType
from .utils import get_casing_probabilities, get_text, get_upper, get_lower


class NameAugment(object):

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

        camel_case_probability, upper_case_probability, lower_case_probability = get_casing_probabilities(
            original_text=original_text, augment_type=augment_type
        )

        (
            full_name_probability,
            first_name_probability,
            last_name_probability,
            full_middle_probability,
            one_middle_probability
        ) = self.get_name_format_probability(augment_type=augment_type, original_text=original_text)

        comma_infix_probability = self.get_comma_infix_probability(
            augment_type=augment_type, original_text=original_text
        )

        # Full name - 50% of the time
        # Only first name - 25% of the time
        # Only last name - 25% of the time
        name = np.random.choice(
                [
                    self.get_full_name,
                    self.get_first_name,
                    self.get_last_name
                ], p=[full_name_probability, first_name_probability, last_name_probability]
        )(
            full_middle_probability=full_middle_probability,
            one_middle_probability=one_middle_probability
        )

        # Remove mr, miss etc - we weirdly are generating names with middle names here
        # since we replace the mr with a first or a last name
        name = re.sub(
            r'\b(Mr|Dr|Mrs|Ms|Miss|MD|M\.D|D(\.)?D(\.)?S(\.)?|D(\.)?V(\.)?M(\.)?|P(\.)?h(\.)?D(\.)?)\b\W*',
            '',
            name,
            flags=re.IGNORECASE
        ).strip()

        # Check whether to infix the full name with a space or a comma
        if np.random.rand() < comma_infix_probability:
            if len(name.split(' ')) <= 2:
                # Replace space with comma 20% of the time
                name = name.replace(' ', str(np.random.choice([', ', ','], p=[0.8, 0.2])))
            else:
                comma = str(np.random.choice([', ', ','], p=[0.8, 0.2]))
                if np.random.rand() < 0.5:
                    name = name.replace(' ', comma)
                else:
                    if np.random.rand() < 0.5:
                        name = name.replace(' ', comma, 1)
                    else:
                        name = name[::-1].replace(' ', comma, 1)[::-1]

        # 80% of the time camel case, 10% of the time lowercase, 10% of the time uppercase
        return np.random.choice(
            [get_text, get_upper, get_lower],
            p=[camel_case_probability, upper_case_probability, lower_case_probability]
        )(name).strip()

    def get_full_name(self, full_middle_probability, **kwargs):
        # First name followed by last name
        def get_first_last():
            name_ = self._fake.name()
            if np.random.rand() < full_middle_probability:
                return self.get_middle_name(name=name_)
            else:
                return name_

        # Last name followed by first name
        def get_last_first():
            name_ = ' '.join(reversed(self._fake.name().split(' ')))
            if np.random.rand() < full_middle_probability:
                return self.get_middle_name(name=name_)
            else:
                return name_

        # First name followed by last name 50% of the time
        # Last name followed by first name 50% of the time
        name = np.random.choice([get_first_last, get_last_first], p=[0.5, 0.5])()
        # Return the name
        return name

    def get_first_name(self, one_middle_probability, **kwargs):
        # Get a first name
        name = self._fake.first_name()
        if np.random.rand() < one_middle_probability:
            # Add initial if needed
            return self.get_middle_name(name=name)
        else:
            return name

    def get_last_name(self, one_middle_probability, **kwargs):
        # Get a last name
        name = self._fake.last_name()
        if np.random.rand() < one_middle_probability:
            # Add initial if needed
            return self.get_middle_name(name=name)
        else:
            return name

    def get_middle_name(self, name):
        # Adding a middle name
        middle = np.random.choice(
            [self._fake.random_uppercase_letter,
             self._fake.random_uppercase_letter,
             self._fake.first_name,
             self._fake.last_name]
        )()
        if len(middle) == 1:
            sep = np.random.choice(['', '.'], p=[0.8, 0.2])
        else:
            sep = ''
        if ' ' in name:
            return random.choice(
                [
                    name.replace(' ', f' {middle}{sep} ', 1),
                    name + f' {middle}{sep}',
                    f'{middle}{sep} ' + name
                ]
            )
        else:
            return random.choice(
                [
                    name + f' {middle}{sep}',
                    f'{middle}{sep} ' + name
                ]
            )

    @staticmethod
    def get_name_format_probability(augment_type, original_text):
        NameFormat = namedtuple(
            'NameFormat',
            [
                'full_name_probability',
                'first_name_probability',
                'last_name_probability',
                'full_middle_probability',
                'one_middle_probability'
            ]
        )
        number_of_tokens = len(
            [text for text in re.split(r'\s|,\s*', original_text, flags=re.IGNORECASE) if text != '']
        ) if original_text is not None else None

        if augment_type == AugmentType.RANDOM:
            return NameFormat(0.5, 0.25, 0.25, 0.2, 0.2)

        if number_of_tokens == 1:
            if augment_type == AugmentType.MIMIC:
                return NameFormat(0.0, 0.5, 0.5, 0.0, 0.0)
            elif augment_type == AugmentType.MIMIC_PROBABILITY:
                return NameFormat(0.2, 0.4, 0.4, 0.1, 0.1)
            else:
                raise ValueError('Invalid augment type')
        elif number_of_tokens == 2:
            if augment_type == AugmentType.MIMIC:
                return NameFormat(0.5, 0.25, 0.25, 0.0, 1.0)
            elif augment_type == AugmentType.MIMIC_PROBABILITY:
                return NameFormat(0.5, 0.25, 0.25, 0.2, 0.8)
            else:
                raise ValueError('Invalid augment type')
        elif number_of_tokens == 3:
            if augment_type == AugmentType.MIMIC:
                return NameFormat(1.0, 0.0, 0.0, 1.0, 0.0)
            elif augment_type == AugmentType.MIMIC_PROBABILITY:
                return NameFormat(0.8, 0.1, 0.1, 0.8, 0.8)
            else:
                raise ValueError('Invalid augment type')
        else:
            if augment_type == AugmentType.MIMIC:
                return NameFormat(0.5, 0.25, 0.25, 0.2, 0.2)
            elif augment_type == AugmentType.MIMIC_PROBABILITY:
                return NameFormat(0.5, 0.25, 0.25, 0.2, 0.2)
            else:
                raise ValueError('Invalid augment type')

    @staticmethod
    def get_comma_infix_probability(augment_type, original_text):
        if original_text is not None and re.search(r',', original_text):
            comma = True
        else:
            comma = False
        if augment_type == AugmentType.RANDOM:
            return 0.5
        if comma:
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
