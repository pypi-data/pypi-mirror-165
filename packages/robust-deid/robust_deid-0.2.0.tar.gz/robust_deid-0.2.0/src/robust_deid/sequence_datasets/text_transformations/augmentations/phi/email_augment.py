import numpy as np

from .augment_type import AugmentType
from .utils import get_casing_probabilities, get_text, get_upper, get_lower


class EmailAugment(object):

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

        email = np.random.choice(
            [self._fake.company_email, self._fake.free_email], p=[0.5, 0.5]
        )()

        camel_case_probability, upper_case_probability, lower_case_probability = get_casing_probabilities(
            original_text=original_text, augment_type=augment_type
        )

        return np.random.choice(
            [get_text, get_upper, get_lower],
            p=[camel_case_probability, upper_case_probability, lower_case_probability]
        )(email).strip()
