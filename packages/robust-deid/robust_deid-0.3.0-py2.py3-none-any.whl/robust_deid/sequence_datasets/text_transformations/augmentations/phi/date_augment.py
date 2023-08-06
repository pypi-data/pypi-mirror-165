import numpy as np

from .augment_type import AugmentType
from .date_patterns import DatePatterns
from .utils import get_casing_probabilities, get_text, get_upper, get_lower


class DateAugment(object):

    def __init__(self, fake):
        self._fake = fake
        self._date_patterns = DatePatterns()

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

        # We used 1000 years initially - changed to 100
        past_days = np.random.randint(1, np.random.randint(1, 100) * 365)
        future_days = np.random.randint(1, np.random.randint(1, 100) * 365)
        past = self._fake.past_date(f'-{past_days}d')
        future = self._fake.future_date(f'+{future_days}d')

        current = self._fake.date_this_decade()
        fake_date = np.random.choice([past, future, current])

        pattern = self.get_date_pattern(augment_type=augment_type, original_text=original_text)
        date_string = fake_date.strftime(pattern)

        # 80% of the time camel case, 10% of the time lowercase, 10% of the time uppercase
        return np.random.choice(
            [get_text, get_upper, get_lower],
            p=[camel_case_probability, upper_case_probability, lower_case_probability]
        )(date_string).strip()

    def get_date_pattern(self, augment_type, original_text):

        pattern_functions = [
            self._date_patterns.get_m_d_y,
            self._date_patterns.get_d_m_y,
            self._date_patterns.get_y_m_d,
            self._date_patterns.get_m_y_d,
            self._date_patterns.get_y_d_m,
            self._date_patterns.get_d_y_m,
            self._date_patterns.get_m_d,
            self._date_patterns.get_d_m,
            self._date_patterns.get_y_m,
            self._date_patterns.get_m_y,
            self._date_patterns.get_season_year,
            self._date_patterns.get_year_range,
            self._date_patterns.get_year_possessive,
            self._date_patterns.get_season,
            self._date_patterns.get_month_range,
            self._date_patterns.get_month_day_range,
            self._date_patterns.get_y,
            self._date_patterns.get_m,
            self._date_patterns.get_d,
            self._date_patterns.get_medicine_days,
            self._date_patterns.get_number,
            self._date_patterns.get_holidays
        ]
        pattern = None
        for i, pattern_function in enumerate(pattern_functions):
            pattern = pattern_function(text=original_text, augment_type=augment_type)
            if pattern is not None:
                return pattern
        if pattern is None:
            return self._date_patterns.get_number(text=self._fake.date(), augment_type=augment_type)
