import re
import nltk
import numpy as np
from scipy.special import softmax
from collections import namedtuple
from nltk.corpus import wordnet as wn

from .augment_type import AugmentType
from .utils import get_casing_probabilities, get_text, get_upper, get_lower


class HospitalAugment(object):

    def __init__(
            self,
            fake,
            id_augment,
            location_augment,
            acronyms,
            assisted_living,
            locations,
            location_ids,
            ids,
            pharmacies,
            hospitals,
            randomize=False
    ):
        self._fake = fake
        self._id_augment = id_augment
        self._location_augment = location_augment

        self._acronyms_list = self.get_list(acronyms)
        self._acronyms_probabilities = self.get_probabilities(acronyms)

        self._assisted_living_list = self.get_list(assisted_living)
        self._assisted_living_probabilities = self.get_probabilities(assisted_living)

        self._locations_list = self.get_list(locations)
        self._locations_probabilities = self.get_probabilities(locations)

        self._location_ids_list = self.get_list(location_ids)
        self._location_ids_probabilities = self.get_probabilities(location_ids)

        self._ids_list = self.get_list(ids)
        self._ids_probabilities = self.get_probabilities(ids)

        self._pharmacies_list = self.get_list(pharmacies)
        self._pharmacies_probabilities = self.get_probabilities(pharmacies)

        self._hospitals_list = self.get_list(hospitals)
        self._hospitals_probabilities = self.get_probabilities(hospitals)

        self._randomize = randomize

    def generate(
            self,
            original_text,
            augment_type,
    ):
        original_text = original_text.strip() if original_text is not None else None

        if original_text is None:
            if augment_type != AugmentType.RANDOM:
                raise ValueError('Augment type needs to be random if original text is None')

        camel_case_probability, upper_case_probability, lower_case_probability = get_casing_probabilities(
            original_text=original_text, augment_type=augment_type
        )

        (
            acronym_probability,
            assisted_living_probability,
            location_probability,
            location_id_probability,
            id_probability,
            pharmacy_probability,
            hospital_probability
        ) = self.get_hospital_format_probability(
            augment_type=augment_type, original_text=original_text
        )

        hospital = np.random.choice(
            [
                self.get_acronym,
                self.get_assisted_living,
                self.get_location,
                self.get_location_id,
                self.get_id,
                self.get_pharmacy,
                self.get_hospital
            ],
            p=[
                acronym_probability,
                assisted_living_probability,
                location_probability,
                location_id_probability,
                id_probability,
                pharmacy_probability,
                hospital_probability
            ]
        )(original_text=original_text, augment_type=augment_type)

        hospital = str(hospital)

        return np.random.choice(
            [get_text, get_upper, get_lower],
            p=[camel_case_probability, upper_case_probability, lower_case_probability]
        )(hospital).strip()

    @staticmethod
    def check_location(text):
        locations = '(room|floor|lab|unit|bed|blake|north|south|east|west)'
        pattern = fr'(((\W|\d)+{locations}))|(({locations}(\W|\d)+))'
        if re.search(pattern, text, flags=re.IGNORECASE):
            return True
        else:
            return False

    @staticmethod
    def check_location_boundary(text):
        locations = '(room|floor|lab|unit|bed|blake|north|south|east|west)'
        pattern = fr'(\b((\W|\d)+{locations})\b)|(\b({locations}(\W|\d)+)\b)'
        if re.search(pattern, text, flags=re.IGNORECASE):
            return True
        else:
            return False

    @staticmethod
    def check_pharmacy(text):
        pattern = r'(cvs|walgreen(s)?|pharma(cy)?|walmart|eaton|rite\W*aid|kroger|costco|apoth(' \
                  r'a|e)cary|amerisourcebergen|amerisource|albertson(s)?|Mmckesson|sears|pharmerica|shopko|wegman(' \
                  r's)?|kinney|conroy(\')?(s)?)|heb|meijer'
        if re.search(pattern, text, flags=re.IGNORECASE):
            return True
        else:
            return False

    @staticmethod
    def get_list(json_object):
        return [key for key, value in json_object.items()]

    @staticmethod
    def get_probabilities(json_object, use_softmax=False):
        if use_softmax:
            return softmax([value for key, value in json_object.items()]).tolist()
        else:
            total_count = sum([value for key, value in json_object.items()])
            return [value / total_count for key, value in json_object.items()]

    @staticmethod
    def get_vowel_count(text):
        count = 0
        vowel = set("aeiouAEIOU")
        for char in text:
            if char in vowel:
                count += 1
        return count

    def get_acronym(self, original_text=None, augment_type=None):
        if self._randomize:
            return self._id_augment.permute_id_text(augment_type=augment_type, text=original_text)
        else:
            return np.random.choice(self._acronyms_list, p=self._acronyms_probabilities)

    def get_assisted_living(self, original_text=None, augment_type=None):
        if self._randomize:
            return self._location_augment.get_assisted_living()
        else:
            return np.random.choice(self._assisted_living_list, p=self._assisted_living_probabilities)

    def get_location(self, original_text=None, augment_type=None):
        if self._randomize:
            fixed = r'(room|floor|lab|unit|\brm\b|bed|blake|north|south|east|west|wacc|cwn|drift|\bu\b|yawkey)\W*'
            match = re.search(fixed, original_text, flags=re.IGNORECASE)
            fix = '' if match is None else match.group(0)
            text = re.sub(fixed, '', original_text, flags=re.IGNORECASE)
            return fix + self._id_augment.permute_id_text(augment_type=augment_type, text=text)
        else:
            return np.random.choice(self._locations_list, p=self._locations_probabilities)

    def get_location_id(self, original_text=None, augment_type=None):
        if self._randomize:
            return self._id_augment.permute_id_text(augment_type=augment_type, text=original_text)
        else:
            return np.random.choice(self._location_ids_list, p=self._location_ids_probabilities)

    def get_id(self, original_text=None, augment_type=None):
        if self._randomize:
            return self._id_augment.permute_id_text(augment_type=augment_type, text=original_text)
        else:
            return np.random.choice(self._ids_list, p=self._ids_probabilities)

    def get_pharmacy(self, original_text=None, augment_type=None):
        return np.random.choice(self._pharmacies_list, p=self._pharmacies_probabilities)

    def get_hospital(self, original_text=None, augment_type=None):
        return np.random.choice(self._hospitals_list, p=self._hospitals_probabilities)

    def get_hospital_format_probability(self, augment_type, original_text):
        HospitalFormat = namedtuple(
            'HospitalFormat',
            [
                'acronym_probability',
                'assisted_living_probability',
                'location_probability',
                'location_id_probability',
                'id_probability',
                'pharmacy_probability',
                'hospital_probability'
            ]
        )
        hospital_pattern = r'\b(hosp(ital)?)\b|\b(health(care)?)\b|community.*clinic'
        if original_text is not None:
            original_text = re.sub(r'\s+', ' ', original_text)
            number_of_tokens = len([text for text in re.split(r'\s', original_text, flags=re.IGNORECASE) if text != ''])
        else:
            number_of_tokens = None

        if augment_type == AugmentType.RANDOM:
            return HospitalFormat(0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.8)

        if (
                self._location_augment.check_assisted_living(original_text) and
                not re.search(hospital_pattern, original_text, flags=re.IGNORECASE)
        ):
            return HospitalFormat(0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0)

        elif self.check_pharmacy(original_text):
            return HospitalFormat(0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        elif re.search(r'\d', original_text, flags=re.IGNORECASE):
            number_digits = sum(char.isdigit() for char in original_text)
            if number_of_tokens == 1 and not re.search(r'\W', original_text, flags=re.IGNORECASE):
                if (
                        not self.check_location_boundary(original_text) and
                        (
                                (len(original_text) > 6 and number_digits <= 4) or
                                (len(original_text) > 4 and number_digits <= 2)
                        )
                ):
                    if (
                            re.search(r'(\d+[a-z]+$)', original_text, flags=re.IGNORECASE) or
                            self.check_location(original_text)
                    ):
                        return HospitalFormat(0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0)
                    else:
                        return HospitalFormat(0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0)

                else:
                    return HospitalFormat(0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0)

            elif number_of_tokens <= 2:
                return HospitalFormat(0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0)

            else:
                tokens = nltk.word_tokenize(original_text)
                noun_flag = False
                for token in tokens:
                    if re.search(r'^\w+$', token, flags=re.IGNORECASE):
                        if wn.synsets(token):
                            noun_flag = True
                            break
                if noun_flag:
                    return HospitalFormat(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0)
                else:
                    return HospitalFormat(0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0)

        else:
            tokens = nltk.word_tokenize(original_text.replace('-', ' '))
            noun_flag = False
            for token in tokens:
                if re.search(r'^\w+$', token, flags=re.IGNORECASE) and len(token) > 3:
                    if wn.synsets(token):
                        noun_flag = True
                        break
            if (
                    noun_flag or
                    number_of_tokens >= 2 or
                    (re.search(r'\W', original_text, flags=re.IGNORECASE) and len(re.sub(r'', '', original_text)) > 3)
            ):
                return HospitalFormat(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0)
            else:
                vowel_count = self.get_vowel_count(
                    re.sub(r'(a)\1+|(e)\2+|(i)\3+|(o)\4+|(u)\5+', r'\1\2\3\4\5', original_text, flags=re.IGNORECASE)
                )
                if len(re.sub(r'', '', original_text)) in range(1, 5):
                    return HospitalFormat(1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
                elif (
                        original_text.isupper() and
                        (
                                (len(original_text) >= 8 and vowel_count <= 2) or
                                (len(original_text) >= 10 and vowel_count <= 3)
                        )
                ):
                    return HospitalFormat(0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0)
                else:
                    return HospitalFormat(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0)
