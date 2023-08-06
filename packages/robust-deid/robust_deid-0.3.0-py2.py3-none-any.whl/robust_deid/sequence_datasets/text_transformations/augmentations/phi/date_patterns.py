import re
import random
import holidays
import itertools
import numpy as np
from .augment_type import AugmentType


class DatePatterns(object):

    def __init__(self):
        day_num = r'(\b(([1-9]|0[1-9]|[1-2][0-9]|3[01])((\s*)(st|nd|rd|th))?)\b)'
        day_of_week = r'(\b((mon|monday(s)?)|(tue|tues|tuesday(s)?)|(wed|wednesday(s)?)|(thu|thur(s)?|thursday(' \
                      r's)?)|(fri|friday(s)?)|(sat|saturday(s)?)|(sun|sunday(s)?))\b)'
        self.day = fr'(?P<day>({day_num}|{day_of_week}))'

        month_text = r'\b(jan(uary)?|feb(ruary)?|mar(ch)?|apr(il)?|may|jun(e)?|jul(y)?|aug(ust)?|sep(t)?(ember)?|oct(' \
                     r'ober)?|nov(ember)?|dec(ember)?)\b'
        month_num = r'(\b(0?[0-9]|1[0-2])\b)'
        self.month = fr'(?P<month>({month_text}|{month_num}))'

        year_2 = r'(\b[0-9]{2}\b)'
        year_4 = r'(\b[0-9]{4}\b)'
        self.year = fr'(?P<year>({year_4}|{year_2}))'

        self.season = r'(\b(winter|summer|fall|spring|autumn)\b)'
        self.medicine_days = r'(\b((m|mo|t|tu|w|we|th|f|fr|s|sa|su)((?P<sep_char_1>\W)*(' \
                             r'm|mo|t|tu|w|we|th|f|fr|s|sa|su)*)*)\b)'

        sep_chars = r'([-./,\s\'^]|of)*'
        self.sep_1 = fr'(?P<sep_char_1>{sep_chars})'
        self.sep_2 = fr'(?P<sep_char_2>{sep_chars})'

    def get_m_d_y(self, text, augment_type):
        match_pattern = self.month + self.sep_1 + self.day + self.sep_2 + self.year
        # match_pattern = r'(\b(' + self.month + self.sep_1 + self.day + self.sep_2 + self.year + r')\b)'
        match = re.search(match_pattern, text, flags=re.IGNORECASE)
        if match is None:
            return None
        suffix = self.get_day_suffix(match=match)
        day = self.get_day(match=match, group='day', augment_type=augment_type)
        month = self.get_month(match=match, group='month', augment_type=augment_type)
        year = self.get_year(match=match, group='year', augment_type=augment_type)
        sep_1 = match.group('sep_char_1')
        sep_2 = match.group('sep_char_2')
        return f'{month}{sep_1}{day}{suffix}{sep_2}{year}'

    def get_d_m_y(self, text, augment_type):
        match_pattern = self.day + self.sep_1 + self.month + self.sep_2 + self.year
        # match_pattern = r'(\b(' + self.day + self.sep_1 + self.month + self.sep_2 + self.year + r')\b)'
        match = re.search(match_pattern, text, flags=re.IGNORECASE)
        if match is None:
            return None
        suffix = self.get_day_suffix(match=match)
        day = self.get_day(match=match, group='day', augment_type=augment_type)
        month = self.get_month(match=match, group='month', augment_type=augment_type)
        year = self.get_year(match=match, group='year', augment_type=augment_type)
        sep_1 = match.group('sep_char_1')
        sep_2 = match.group('sep_char_2')
        return f'{day}{suffix}{sep_1}{month}{sep_2}{year}'

    def get_y_m_d(self, text, augment_type):
        match_pattern = self.year + self.sep_1 + self.month + self.sep_2 + self.day
        # match_pattern = r'(\b(' + self.year + self.sep_1 + self.month + self.sep_2 + self.day + r')\b)'
        match = re.search(match_pattern, text, flags=re.IGNORECASE)
        if match is None:
            return None
        suffix = self.get_day_suffix(match=match)
        day = self.get_day(match=match, group='day', augment_type=augment_type)
        month = self.get_month(match=match, group='month', augment_type=augment_type)
        year = self.get_year(match=match, group='year', augment_type=augment_type)
        sep_1 = match.group('sep_char_1')
        sep_2 = match.group('sep_char_2')
        return f'{year}{sep_1}{month}{sep_2}{day}{suffix}'

    def get_m_y_d(self, text, augment_type):
        match_pattern = self.month + self.sep_1 + self.year + self.sep_2 + self.day
        # match_pattern = r'(\b(' + self.month + self.sep_1 + self.year + self.sep_2 + self.day + r')\b)'
        match = re.search(match_pattern, text, flags=re.IGNORECASE)
        if match is None:
            return None
        suffix = self.get_day_suffix(match=match)
        day = self.get_day(match=match, group='day', augment_type=augment_type)
        month = self.get_month(match=match, group='month', augment_type=augment_type)
        year = self.get_year(match=match, group='year', augment_type=augment_type)
        sep_1 = match.group('sep_char_1')
        sep_2 = match.group('sep_char_2')
        return f'{month}{sep_1}{year}{sep_2}{day}{suffix}'

    def get_y_d_m(self, text, augment_type):
        match_pattern = self.year + self.sep_1 + self.day + self.sep_2 + self.month
        # match_pattern = r'(\b(' + self.year + self.sep_1 + self.day + self.sep_2 + self.month + r')\b)'
        match = re.search(match_pattern, text, flags=re.IGNORECASE)
        if match is None:
            return None
        suffix = self.get_day_suffix(match=match)
        day = self.get_day(match=match, group='day', augment_type=augment_type)
        month = self.get_month(match=match, group='month', augment_type=augment_type)
        year = self.get_year(match=match, group='year', augment_type=augment_type)
        sep_1 = match.group('sep_char_1')
        sep_2 = match.group('sep_char_2')
        return f'{year}{sep_1}{day}{suffix}{sep_2}{month}'

    def get_d_y_m(self, text, augment_type):
        match_pattern = self.day + self.sep_1 + self.year + self.sep_2 + self.month
        # match_pattern = r'(\b(' + self.day + self.sep_1 + self.year + self.sep_2 + self.month + r')\b)'
        match = re.search(match_pattern, text, flags=re.IGNORECASE)
        if match is None:
            return None
        suffix = self.get_day_suffix(match=match)
        day = self.get_day(match=match, group='day', augment_type=augment_type)
        month = self.get_month(match=match, group='month', augment_type=augment_type)
        year = self.get_year(match=match, group='year', augment_type=augment_type)
        sep_1 = match.group('sep_char_1')
        sep_2 = match.group('sep_char_2')
        return f'{day}{suffix}{sep_1}{year}{sep_2}{month}'

    def get_m_d(self, text, augment_type):
        match_pattern = self.month + self.sep_1 + self.day
        # match_pattern = r'(\b(' + self.month + self.sep_1 + self.day + r')\b)'
        match = re.search(match_pattern, text, flags=re.IGNORECASE)
        if match is None:
            return None
        suffix = self.get_day_suffix(match=match)
        day = self.get_day(match=match, group='day', augment_type=augment_type)
        month = self.get_month(match=match, group='month', augment_type=augment_type)
        sep_1 = match.group('sep_char_1')
        return f'{month}{sep_1}{day}{suffix}'

    def get_d_m(self, text, augment_type):
        match_pattern = self.day + self.sep_1 + self.month
        # match_pattern = r'(\b(' + self.day + self.sep_1 + self.month + r')\b)'
        match = re.search(match_pattern, text, flags=re.IGNORECASE)
        if match is None:
            return None
        suffix = self.get_day_suffix(match=match)
        day = self.get_day(match=match, group='day', augment_type=augment_type)
        month = self.get_month(match=match, group='month', augment_type=augment_type)
        sep_1 = match.group('sep_char_1')
        return f'{day}{suffix}{sep_1}{month}'

    def get_y_m(self, text, augment_type):
        match_pattern = self.year + self.sep_1 + self.month
        # match_pattern = r'(\b(' + self.year + self.sep_1 + self.month + r')\b)'
        match = re.search(match_pattern, text, flags=re.IGNORECASE)
        if match is None:
            return None
        month = self.get_month(match=match, group='month', augment_type=augment_type)
        year = self.get_year(match=match, group='year', augment_type=augment_type)
        sep_1 = match.group('sep_char_1')
        return f'{year}{sep_1}{month}'

    def get_m_y(self, text, augment_type):
        match_pattern = self.month + self.sep_1 + self.year
        # match_pattern = r'(\b(' + self.month + self.sep_1 + self.year + r')\b)'
        match = re.search(match_pattern, text, flags=re.IGNORECASE)
        if match is None:
            return None
        month = self.get_month(match=match, group='month', augment_type=augment_type)
        year = self.get_year(match=match, group='year', augment_type=augment_type)
        sep_1 = match.group('sep_char_1')
        return f'{month}{sep_1}{year}'

    def get_season_year(self, text, augment_type):
        match_pattern = self.season + self.sep_1 + self.year
        # match_pattern = r'(\b(' + self.season + self.sep_1 + self.year + r')\b)'
        match = re.search(match_pattern, text, flags=re.IGNORECASE)
        if match is None:
            return None
        season = np.random.choice(['Winter', 'Summer', 'Fall', 'Spring', 'Autumn'])
        year = self.get_year(match=match, group='year', augment_type=augment_type)
        sep_1 = match.group('sep_char_1')
        return f'{season}{sep_1}{year}'

    def get_year_range(self, text, augment_type):
        match_pattern = self.year + self.sep_1 + self.year.replace('year', 'year_1')
        # match_pattern = r'(\b(' + self.year + self.sep_1 + self.year.replace('year', 'year_1') + r')\b)'
        match = re.search(match_pattern, text, flags=re.IGNORECASE)
        if match is None:
            return None
        year = self.get_year(match=match, group='year', augment_type=augment_type)
        year_1 = self.get_year(match=match, group='year_1', augment_type=augment_type)
        sep_1 = match.group('sep_char_1')
        return f'{year}{sep_1}{year_1}'

    def get_year_possessive(self, text, augment_type):
        match_pattern = r'\b(' + self.year.replace(r'\b', '') + self.sep_1 + r'(s))\b'
        # match_pattern = r'\b(' + self.year.replace(r'\b', '') + self.sep_1 + r'(s))\b'
        match = re.search(match_pattern, text, flags=re.IGNORECASE)
        if match is None:
            return None
        year = self.get_year(match=match, group='year', augment_type=augment_type)
        sep_1 = match.group('sep_char_1')
        return f'{year}{sep_1}s'

    def get_season(self, text, augment_type):
        match_pattern = self.season
        match = re.search(match_pattern, text, flags=re.IGNORECASE)
        if match is None:
            return None
        season = np.random.choice(['Winter', 'Summer', 'Fall', 'Spring', 'Autumn'])
        return f'{season}'

    def get_month_range(self, text, augment_type):
        match_pattern = self.month + self.sep_1 + self.month.replace('month', 'month_1')
        match = re.search(match_pattern, text, flags=re.IGNORECASE)
        if match is None:
            return None
        month = self.get_month(match=match, group='month', augment_type=augment_type)
        month_1 = self.get_month(match=match, group='month_1', augment_type=augment_type)
        sep_1 = match.group('sep_char_1')
        return f'{month}{sep_1}{month_1}'

    def get_month_day_range(self, text, augment_type):
        match_pattern = self.month + self.sep_1 + self.day + self.sep_2 + self.day.replace('day', 'day_1')
        match = re.search(match_pattern, text, flags=re.IGNORECASE)
        if match is None:
            return None
        suffix = self.get_day_suffix(match=match)
        suffix_1 = self.get_day_suffix(match=match, group='day_1')
        day = self.get_day(match=match, group='day', augment_type=augment_type)
        day_1 = self.get_day(match=match, group='day_1', augment_type=augment_type)
        month = self.get_month(match=match, group='month', augment_type=augment_type)
        sep_1 = match.group('sep_char_1')
        sep_2 = match.group('sep_char_2')
        return f'{month}{sep_1}{day}{suffix}{sep_2}{day_1}{suffix_1}'

    def get_y(self, text, augment_type):
        match_patterns = [self.sep_1 + self.year, self.sep_1 + self.year.replace(r'\b', '')]
        match = None
        for match_pattern in match_patterns:
            match = re.search(match_pattern, text, flags=re.IGNORECASE)
            if match:
                break
        if match is None:
            return None
        year = self.get_year(match=match, group='year', augment_type=augment_type)
        sep_1 = match.group('sep_char_1')
        return f'{sep_1}{year}'

    def get_m(self, text, augment_type):
        match_patterns = [self.month, self.month.replace(r'\b', '')]
        match = None
        for match_pattern in match_patterns:
            match = re.search(match_pattern, text, flags=re.IGNORECASE)
            if match:
                break
        if match is None:
            return None
        month = self.get_month(match=match, group='month', augment_type=augment_type)
        return f'{month}'

    def get_d(self, text, augment_type):
        match_patterns = [self.day, self.day.replace(r'\b', '')]
        match = None
        for match_pattern in match_patterns:
            match = re.search(match_pattern, text, flags=re.IGNORECASE)
            if match:
                break
        if match is None:
            return None
        day = self.get_day(match=match, group='day', augment_type=augment_type)
        return f'{day}'

    def get_medicine_days(self, text, augment_type):
        match_pattern = self.medicine_days
        match = re.search(match_pattern, text, flags=re.IGNORECASE)
        if match is None:
            return None
        count_pattern = r'(m|t|w|f|s)'
        new_match = re.sub(count_pattern, 'X', text, flags=re.IGNORECASE)
        tue = np.random.choice(['T', 'Tu'], p=[0.9, 0.1])
        sat = np.random.choice(['S', 'Sa'], p=[0.9, 0.1])
        choices = [
            np.random.choice(['M', 'Mo'], p=[0.9, 0.1]),
            tue,
            np.random.choice(['W', 'We'], p=[0.9, 0.1]),
            np.random.choice(['T', 'Th'], p=[0.9, 0.1]) if tue == 'Tu' else 'Th',
            np.random.choice(['F', 'Fr'], p=[0.9, 0.1]),
            sat,
            np.random.choice(['S', 'Su'], p=[0.9, 0.1]) if sat == 'Sa' else 'Su'
        ]
        if new_match.count('X') == 1:
            p = np.array([0.16, 0.16, 0.16, 0.16, 0.16, 0.1, 0.1])
            return str(np.random.choice(choices, p=p))
        else:
            medicine_options = list(map(''.join, itertools.combinations(choices, r=new_match.count('X'))))
            return str(np.random.choice(medicine_options))

    def get_number(self, text, augment_type):
        match_pattern = r'\b[0-9\W]+\b'
        match = re.search(match_pattern, text, flags=re.IGNORECASE)
        if match is None:
            return None
        sep_replace = random.choice('--//.')
        text = '2000-01-01'.replace('-', sep_replace)
        match_pattern = self.year + self.sep_1 + self.month + self.sep_2 + self.day
        match = re.search(match_pattern, text, flags=re.IGNORECASE)
        day = self.get_day(match=match, group='day', augment_type=AugmentType.RANDOM)
        month = self.get_month(match=match, group='month', augment_type=AugmentType.RANDOM)
        year = self.get_year(match=match, group='year', augment_type=AugmentType.RANDOM)
        sep_1 = match.group('sep_char_1')
        sep_2 = match.group('sep_char_2')
        pattern = random.choice([
            f'{month}{sep_1}{day}{sep_2}{year}',
            f'{day}{sep_1}{month}{sep_2}{year}',
            f'{year}{sep_1}{month}{sep_2}{day}',
            f'{month}{sep_1}{year}{sep_2}{day}',
            f'{year}{sep_1}{day}{sep_2}{month}',
            f'{day}{sep_1}{year}{sep_2}{month}']
        )
        return pattern

    def get_holidays(self, text, augment_type):
        match_pattern = r'^[\sa-zA-Z\'"-]+$'
        match = re.search(match_pattern, text, flags=re.IGNORECASE)
        if match is None:
            return None
        year = 2014
        countries = list(holidays.utils.list_supported_countries().keys())
        holiday = ''
        pattern = r'^[a-zA-Z\W]+$'
        while not re.search(pattern, holiday):
            country = random.choice(countries)
            holiday_list = [name for _, name in holidays.country_holidays(country=country, years=year).items()]
            holiday = random.choice(holiday_list)
        return holiday.replace('day', random.choice(['day', '']))

    @staticmethod
    def get_day(match, group, augment_type):
        possessive = ''
        if augment_type == AugmentType.RANDOM:
            day_p = [0.25, 0.25, 0.25, 0.25]
        elif re.search(r'\d+', match.group(group)):
            if len(match.group(group)) == 1:
                if augment_type == AugmentType.MIMIC:
                    day_p = [0.0, 1.0, 0.0, 0.0]
                elif augment_type == AugmentType.MIMIC_PROBABILITY:
                    day_p = [0.1, 0.8, 0.05, 0.05]
                else:
                    raise ValueError('Invalid augment type')
            else:
                if augment_type == AugmentType.MIMIC:
                    day_p = [1.0, 0.0, 0.0, 0.0]
                elif augment_type == AugmentType.MIMIC_PROBABILITY:
                    day_p = [0.8, 0.1, 0.05, 0.05]
                else:
                    raise ValueError('Invalid augment type')
        elif len(match.group(group)) <= 4:
            if augment_type == AugmentType.MIMIC:
                day_p = [0.0, 0.0, 1.0, 0.0]
            elif augment_type == AugmentType.MIMIC_PROBABILITY:
                day_p = [0.05, 0.05, 0.8, 0.1]
            else:
                raise ValueError('Invalid augment type')
        else:
            if re.search(r's\s*$', match.group(group)):
                possessive = 's'
            if augment_type == AugmentType.MIMIC:
                day_p = [0.0, 0.0, 0.0, 1.0]
            elif augment_type == AugmentType.MIMIC_PROBABILITY:
                day_p = [0.05, 0.05, 0.1, 0.8]
            else:
                raise ValueError('Invalid augment type')

        return np.random.choice(['%d', '%-d', '%a', '%A' + possessive], p=day_p)

    @staticmethod
    def get_month(match, group, augment_type):
        if augment_type == AugmentType.RANDOM:
            month_p = [0.25, 0.25, 0.25, 0.25]
        elif augment_type == AugmentType.MIMIC:
            if re.search(r'\d+', match.group(group)):
                if len(match.group(group)) == 1:
                    month_p = [0.0, 1.0, 0.0, 0.0]
                else:
                    month_p = [1.0, 0.0, 0.0, 0.0]
            elif len(match.group(group)) <= 3:
                month_p = [0.0, 0.0, 1.0, 0.0]
            else:
                month_p = [0.0, 0.0, 0.0, 1.0]
        elif augment_type == AugmentType.MIMIC_PROBABILITY:
            if re.search(r'\d+', match.group(group)):
                if len(match.group(group)) == 1:
                    month_p = [0.1, 0.8, 0.05, 0.05]
                else:
                    month_p = [0.8, 0.1, 0.05, 0.05]
            elif len(match.group(group)) <= 3:
                month_p = [0.05, 0.05, 0.8, 0.1]
            else:
                month_p = [0.05, 0.05, 0.1, 0.8]
        elif augment_type == AugmentType.CUSTOM:
            raise NotImplementedError('Passing custom probabilities not implemented yet')
        else:
            raise ValueError('Invalid augment type')
        return np.random.choice(['%m', '%-m', '%b', '%B'], p=month_p)

    @staticmethod
    def get_year(match, group, augment_type):
        if augment_type == AugmentType.RANDOM:
            year_p = [0.5, 0.5]
        elif augment_type == AugmentType.MIMIC:
            if len(match.group(group)) <= 2:
                year_p = [0.0, 1.0]
            else:
                year_p = [1.0, 0.0]
        elif augment_type == AugmentType.MIMIC_PROBABILITY:
            if len(match.group(group)) <= 2:
                year_p = [0.2, 0.8]
            else:
                year_p = [0.8, 0.2]
        elif augment_type == AugmentType.CUSTOM:
            raise NotImplementedError('Passing custom probabilities not implemented yet')
        else:
            raise ValueError('Invalid augment type')
        return np.random.choice(['%Y', '%y'], p=year_p)

    @staticmethod
    def get_day_suffix(match, group='day'):
        if re.search(r'(st|nd|rd|th)', match.group(group)):
            return np.random.choice(['st', 'nd', 'rd', 'th'])
        else:
            return ''
