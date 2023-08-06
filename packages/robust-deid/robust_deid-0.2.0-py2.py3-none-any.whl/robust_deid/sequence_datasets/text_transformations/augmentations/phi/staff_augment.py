import re
import string
import random
import numpy as np
from collections import namedtuple

from .augment_type import AugmentType
from .name_augment import NameAugment
from .utils import get_casing_probabilities, get_text, get_upper, get_lower


class StaffAugment(NameAugment):

    def __init__(self, fake):
        super().__init__(fake)

    def generate(
            self,
            original_text,
            augment_type,
    ):

        original_text = original_text.strip() if original_text is not None else None

        if original_text is None:
            if augment_type != AugmentType.RANDOM:
                raise ValueError('Augment type needs to be random if original text is None')

        # id_probability = self.get_id_probability(augment_type=augment_type, original_text=original_text)
        # unknown_probability = self.get_id_probability(augment_type=augment_type, original_text=original_text)

        (
            name_probability,
            unknown_name_probability,
            staff_id_probability,
            two_char_probability,
        ) = self.get_staff_name_format_probability(augment_type=augment_type, original_text=original_text)

        camel_case_probability, upper_case_probability, lower_case_probability = get_casing_probabilities(
            original_text=original_text, augment_type=augment_type
        )

        def get_super_name():
            return super(StaffAugment, self).generate(
                original_text=original_text,
                augment_type=augment_type
            )

        def get_unknown_text():
            return original_text

        name = np.random.choice(
            [
                get_super_name,
                get_unknown_text,
                self.get_staff_id,
                self.get_two_char_id
            ], p=[name_probability, unknown_name_probability, staff_id_probability, two_char_probability]
        )()

        return np.random.choice(
            [get_text, get_upper, get_lower],
            p=[camel_case_probability, upper_case_probability, lower_case_probability]
        )(name).strip()

        # if np.random.rand() <= id_probability:
        #     name = self.get_staff_id()
        #     camel_case_probability, upper_case_probability, lower_case_probability = get_casing_probabilities(
        #         original_text=original_text, augment_type=augment_type
        #     )
        #     # 80% of the time camel case, 10% of the time lowercase, 10% of the time uppercase
        #     return np.random.choice(
        #         [get_text, get_upper, get_lower],
        #         p=[camel_case_probability, upper_case_probability, lower_case_probability]
        #     )(name).strip()
        # else:
        #     if np.random.rand() <= unknown_probability:
        #         return original_text
        #     else:
        #         return super().generate(
        #             original_text=original_text,
        #             augment_type=augment_type
        #         )

    @staticmethod
    def get_staff_id():
        return random.choice(string.ascii_uppercase) + ''.join(
            random.choices(string.ascii_lowercase, k=np.random.randint(1, 3))
        ) + ''.join(random.choices(string.digits, k=np.random.randint(1, 4)))

    @staticmethod
    def get_two_char_id():
        return random.choice(string.ascii_uppercase) + random.choice(string.ascii_lowercase) + \
               np.random.choice(['', random.choice(string.ascii_lowercase)], p=[0.8, 0.2])

    @staticmethod
    def get_staff_name_format_probability(augment_type, original_text):
        NameFormat = namedtuple(
            'NameFormat',
            [
                'name_probability',
                'unknown_name_probability',
                'staff_id_probability',
                'two_char_probability',
            ]
        )
        staff_id_pattern = r'^(\W*)([a-zA-Z]{2,3}\d{1,3})(\W*)$'
        staff_unknown_pattern = r'^(\W*)(\b(unknown)\b)(\W*)(\b(unknown)\b)*(\W*)$'
        staff_two_char_pattern = r'(^[A-Z]{2,3}$)|(^[a-z]{2,3}$)'

        if augment_type == AugmentType.RANDOM:
            return NameFormat(0.8, 0.0, 0.1, 0.1)

        if re.search(staff_id_pattern, original_text):
            if augment_type == AugmentType.MIMIC:
                return NameFormat(0.0, 0.0, 1.0, 0.0)
            elif augment_type == AugmentType.MIMIC_PROBABILITY:
                return NameFormat(0.1, 0.0, 0.8, 0.1)
            else:
                raise ValueError('Invalid augment type')
        elif re.search(staff_unknown_pattern, original_text, flags=re.IGNORECASE):
            if augment_type == AugmentType.MIMIC:
                return NameFormat(0.0, 1.0, 0.0, 0.0)
            elif augment_type == AugmentType.MIMIC_PROBABILITY:
                return NameFormat(0.1, 0.8, 0.05, 0.05)
            else:
                raise ValueError('Invalid augment type')
        elif re.search(staff_two_char_pattern, original_text, flags=re.IGNORECASE):
            if augment_type == AugmentType.MIMIC:
                return NameFormat(0.0, 0.0, 0.0, 1.0)
            elif augment_type == AugmentType.MIMIC_PROBABILITY:
                return NameFormat(0.1, 0.0, 0.1, 0.8)
            else:
                raise ValueError('Invalid augment type')
        else:
            if augment_type == AugmentType.MIMIC:
                return NameFormat(1.0, 0.0, 0.0, 0.0)
            elif augment_type == AugmentType.MIMIC_PROBABILITY:
                return NameFormat(0.8, 0.0, 0.1, 0.1)
            else:
                raise ValueError('Invalid augment type')
