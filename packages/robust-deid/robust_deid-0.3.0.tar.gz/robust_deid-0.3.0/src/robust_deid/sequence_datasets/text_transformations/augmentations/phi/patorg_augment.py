import numpy as np

from .augment_type import AugmentType
from .utils import get_casing_probabilities, get_text, get_upper, get_lower, get_acronym_probability


class PatorgAugment(object):

    def __init__(self, fake, patorg_list):
        self._fake = fake
        self._patorg_list = patorg_list

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

        acronym_probability = get_acronym_probability(augment_type=augment_type, original_text=original_text)

        # Generate a company name from faker 80% of the time
        # Generate a company name from the faker company noun and adjective 10% of the time
        # Generate a company acronym 10% of the time
        company = np.random.choice(
            [self.get_company, self.get_company_acronym],
            p=[1 - acronym_probability, acronym_probability]
        )()

        return np.random.choice(
            [get_text, get_upper, get_lower],
            p=[camel_case_probability, upper_case_probability, lower_case_probability]
        )(company).strip()

    def get_company(self):
        if np.random.rand() <= 0.8:
            return str(np.random.choice(self._patorg_list))
        else:
            return self.get_faker_company()

    def get_faker_company(self):
        return self._fake.company()

    def get_company_acronym(self):
        return self._fake.random_company_acronym()
