import re
import random
import numpy as np
from collections import namedtuple

from .augment_type import AugmentType
from .utils import get_casing_probabilities, get_text, get_upper, get_lower


class LocationAugment(object):

    def __init__(self, fake):
        self._fake = fake
        self._countries = ['United States', 'Afghanistan', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua And Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia And Herzegowina', 'Botswana', 'Bouvet Island', 'Brazil', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Central African Rep', 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos Islands', 'Colombia', 'Comoros', 'Congo', 'Cook Islands', 'Costa Rica', 'Cote D`ivoire', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'East Timor', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'French S. Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guinea', 'Guinea-bissau', 'Guyana', 'Haiti', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Korea (North)', 'Korea (South)', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macau', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'Netherlands Antilles', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Reunion', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Kitts And Nevis', 'Saint Lucia', 'St Vincent/Grenadines', 'Samoa', 'San Marino', 'Sao Tome', 'Saudi Arabia', 'Senegal', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'Spain', 'Sri Lanka', 'St. Helena', 'St.Pierre', 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Togo', 'Tokelau', 'Tonga', 'Trinidad And Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican City State', 'Venezuela', 'Vietnam', 'Virgin Islands', 'Virgin Islands', 'Western Sahara', 'Yemen', 'Yugoslavia', 'Zaire', 'Zambia', 'Zimbabwe', 'United States of America']
        self._nationalities = ('Afghan', 'Albanian', 'Algerian', 'American', 'Andorran', 'Angolan', 'Antiguans', 'Argentinean', 'Armenian', 'Australian', 'Austrian', 'Azerbaijani', 'Bahamian', 'Bahraini', 'Bangladeshi', 'Barbadian', 'Barbudans', 'Batswana', 'Belarusian', 'Belgian', 'Belizean', 'Beninese', 'Bhutanese', 'Bolivian', 'Bosnian', 'Brazilian', 'British', 'Bruneian', 'Bulgarian', 'Burkinabe', 'Burmese', 'Burundian', 'Cambodian', 'Cameroonian', 'Canadian', 'Cantonese', 'Cape Verdean', 'Central African', 'Chadian', 'Chilean', 'Chinese', 'Colombian', 'Comoran',  'Congolese', 'Costa Rican', 'Croatian', 'Cuban', 'Cypriot', 'Czech', 'Danish', 'Djibouti', 'Dominican', 'Dutch', 'Dutchman', 'Dutchwoman', 'East Timorese', 'Ecuadorean', 'Egyptian', 'Emirian', 'Equatorial Guinean', 'Eritrean', 'Estonian', 'Ethiopian', 'Fijian', 'Filipino', 'Finnish', 'French', 'Gabonese', 'Gambian', 'Georgian', 'German', 'Ghanaian', 'Greek', 'Grenadian', 'Guatemalan', 'Guinea-Bissauan', 'Guinean', 'Guyanese', 'Haitian', 'Herzegovinian', 'Hispanic5', 'Honduran', 'Hungarian', 'I-Kiribati', 'Icelander', 'Indian', 'Indonesian', 'Iranian', 'Iraqi', 'Irish', 'Israeli', 'Italian', 'Ivorian', 'Jamaican', 'Japanese', 'Jordanian', 'Kazakhstani', 'Kenyan', 'Kittian', 'Nevisian', 'Kuwaiti', 'Kyrgyz', 'Laotian', 'Latino', 'Latvian', 'Lebanese', 'Liberian', 'Libyan', 'Liechtensteiner', 'Lithuanian', 'Luxembourger', 'Macedonian', 'Malagasy', 'Malawian', 'Malaysian', 'Maldivan', 'Malian', 'Maltese', 'Marshallese', 'Mauritanian', 'Mauritian', 'Mexican', 'Micronesian', 'Moldovan', 'Monacan', 'Mongolian', 'Moroccan', 'Mosotho', 'Motswana', 'Mozambican', 'Namibian', 'Nauruan', 'Nepalese', 'Netherlander', 'New Zealander', 'Ni-Vanuatu', 'Nicaraguan', 'Nigerian', 'Nigerien', 'North Korean', 'Northern Irish', 'Norwegian', 'Omani', 'Pakistani', 'Palauan', 'Panamanian', 'Papua New Guinean', 'Paraguayan', 'Peruvian', 'Polish', 'Portuguese', 'Qatari', 'Romanian', 'Russian', 'Rwandan', 'Saint Lucian', 'Salvadoran', 'Samoan', 'San Marinese', 'Sao Tomean', 'Saudi', 'Scottish', 'Senegalese', 'Serbian', 'Seychellois', 'Sierra Leonean', 'Singaporean', 'Slovakian', 'Slovenian', 'Solomon Islander', 'Somali', 'South African', 'South Korean', 'Spanish', 'Sri Lankan', 'Sudanese', 'Surinamer', 'Swazi', 'Swedish', 'Swiss', 'Syrian', 'Taiwanese', 'Tajik', 'Tanzanian', 'Thai', 'Togolese', 'Tongan', 'Trinidadian', 'Tobagonian', 'Toishwanese', 'Tunisian', 'Turkish', 'Tuvaluan', 'Ugandan', 'Ukrainian', 'Uruguayan', 'Uzbekistani', 'Venezuelan', 'Vietnamese', 'Welsh', 'Yemenite', 'Zambian', 'Zimbabwean')
        self._nationalities_pattern = r'^\W*(' + '|'.join(self._nationalities) + r')\W*$'
        self._countries_pattern = r'^\W*(' + '|'.join(self._countries) + r')\W*$'

    def generate(
            self,
            original_text,
            augment_type,
            previous_location
    ):

        original_text = original_text.strip() if original_text is not None else None

        if original_text is None:
            if augment_type != AugmentType.RANDOM:
                raise ValueError('Augment type needs to be random if original text is None')

        (
            street_probability,
            apartment_probability,
            city_probability,
            state_probability,
            country_probability,
            zipcode_probability,
        ) = self.get_location_format_probability(
            augment_type=augment_type, original_text=original_text, previous_location=previous_location
        )

        abbreviated_probability = self.get_abbreviated_probability(
            augment_type=augment_type, original_text=original_text
        )

        camel_case_probability, upper_case_probability, lower_case_probability = get_casing_probabilities(
            original_text=original_text, augment_type=augment_type
        )

        if self.check_nationality(original_text):
            location = random.choice(self._nationalities)
            location_type = None
        elif self.check_country(original_text):
            location = self._fake.country()
            location_type = 'country'
        elif self.check_assisted_living(original_text) \
                and (previous_location is None or previous_location in ['country', 'zipcode']):
            location = self.get_assisted_living()
            location_type = None
        else:
            location, location_type = np.random.choice(
                [
                    self.get_street,
                    self.get_apartment,
                    self.get_city,
                    np.random.choice(
                        [self.get_state, self.get_state_abbreviated],
                        p=[1 - abbreviated_probability, abbreviated_probability]
                    ),
                    np.random.choice(
                        [self.get_country, self.get_country_abbreviated],
                        p=[1 - abbreviated_probability, abbreviated_probability]
                    ),
                    self.get_zip_code
                ],
                p=[
                    street_probability,
                    apartment_probability,
                    city_probability,
                    state_probability,
                    country_probability,
                    zipcode_probability
                ]
            )()

        return np.random.choice(
            [get_text, get_upper, get_lower],
            p=[camel_case_probability, upper_case_probability, lower_case_probability]
        )(location).strip(), location_type

    def check_nationality(self, original_text):
        if re.search(self._nationalities_pattern, original_text, flags=re.IGNORECASE):
            return True
        else:
            return False

    def check_country(self, original_text):
        if re.search(self._countries_pattern, original_text, flags=re.IGNORECASE):
            return True
        else:
            return False

    @staticmethod
    def check_assisted_living(original_text):
        pattern = r'\b(living|assisted|community|building|((nursing|group)\W*home)|home|nursing|rehab)\b'
        if re.search(pattern, original_text, flags=re.IGNORECASE):
            return True
        else:
            return False

    def get_street(self):
        street_address = self._fake.street_address()
        street_address = re.sub(
            r'\b(apt|#|unit|building|apartment|suite|center|ste|no|number|floor|room)\b.*$',
            '',
            street_address,
            flags=re.IGNORECASE
        ).strip()
        # Return some street address representation
        return street_address, 'street'

    def get_apartment(self):
        second_prefix = str(
            np.random.choice(['', 'no', 'number', '#', 'No', 'Number'], p=[0.8, 0.02, 0.02, 0.12, 0.02, 0.02])
        )
        prefix = random.choice(
            [
                'Apt' + second_prefix,
                '#',
                'Unit' + second_prefix,
                'Building' + second_prefix,
                'Suite' + second_prefix,
                'Apartment' + second_prefix,
                'Ste',
                'Center',
                'No',
                'Number',
            ]
        )
        sep = random.choice(['- ', ': ', ' ', ' ', ' ', '-', '. '])
        if prefix == '#' or second_prefix == '#':
            sep = ''
        number = self._fake.building_number()
        letter = str(np.random.choice([self._fake.random_letter(), ''], p=[0.2, 0.8]))

        return prefix + sep + number + letter, 'apartment'

    def get_city(self):
        # Return some city representation
        return np.random.choice(
            [self._fake.city,
             self._get_new_city,
             self._fake.province_lgu
             ], p=[0.5, 0.25, 0.25]
        )(), 'city'

    def get_state(self):
        # Return some state representation
        return np.random.choice(
            [
                self._fake.state,
                self._fake.administrative_unit,
            ]
        )(), 'state'

    def get_state_abbreviated(self):
        # Return some state representation
        return np.random.choice(
            [
                self._fake.state_abbr,
                self._get_random_letters,
            ]
        )(), 'state'

    def get_country(self):
        # Return some country representation 20% of the time
        return self._fake.country(), 'country'

    def get_country_abbreviated(self):
        # Return some country representation 20% of the time
        return np.random.choice(
            [
                self._fake.country_code,
                self._get_random_letters,
            ]
        )(), 'country'

    def get_zip_code(self):
        # Return some zipcode representation
        return np.random.choice(
            [
                self._fake.zipcode,
                self._fake.zipcode_plus4,
                self._fake.postalcode,
                self._fake.postalcode_plus4,
                self._fake.postcode,
                np.random.choice(
                    [
                        self._fake.luzon_province_postcode,
                        self._fake.visayas_province_postcode,
                        self._fake.mindanao_province_postcode
                    ]
                )
            ]
        )(), 'zipcode'

    def _get_random_letters(self):
        return self._fake.random_uppercase_letter() + self._fake.random_uppercase_letter()

    def _get_new_city(self):

        def get_city():
            return self._fake.city_prefix() + ' ' + self._fake.last_name() + self._fake.city_suffix()

        def get_prefix_city():
            return self._fake.city_prefix() + ' ' + self._fake.last_name()

        def get_suffix_city():
            return self._fake.last_name() + self._fake.city_suffix()

        return np.random.choice([get_city, get_prefix_city, get_suffix_city])()

    def get_assisted_living(self):
        return self._fake.random_object_name() + random.choice(
            [
                random.choice(['Assisted Living', 'Assisted living', 'assisted living']),
                random.choice(['Living', 'living']),
                random.choice(['Building', 'building']),
                random.choice(['Community', 'community']),
                random.choice(['Rehab', 'rehab']),
                random.choice(['Home', 'home']),
                random.choice(['Center', 'center']),
                random.choice(['Nursing Home', 'Nursing home', 'nursing home']),
                random.choice(['Group Home', 'Group home', 'group home'])
            ]
        )

    @staticmethod
    def get_location_format_probability(augment_type, original_text, previous_location):
        LocationFormat = namedtuple(
            'LocationFormat',
            [
                'street_probability',
                'apartment_probability',
                'city_probability',
                'state_probability',
                'country_probability',
                'zipcode_probability'
            ]
        )

        apartment = False
        digits = False
        zipcode = False

        number_of_tokens = len(
            [text for text in re.split(r'\s|-\s*|,\s*|the\s*', original_text, flags=re.IGNORECASE) if text != '']
        ) if original_text is not None else None

        if re.search(r'\b(\d+)\b', original_text, flags=re.IGNORECASE):
            digits = True

        if re.search(r'^\W*(\d+[-]*\d+)\W*$', original_text, flags=re.IGNORECASE):
            zipcode = True

        if re.search(
                r'\b(apt|#|unit|building|apartment|suite|center|ste|no|number|floor|room)\b',
                original_text,
                flags=re.IGNORECASE
        ):
            apartment = True

        if augment_type == AugmentType.RANDOM:
            return LocationFormat(0.25, 0.0, 0.25, 0.25, 0.15, 0.1)

        if previous_location is None or previous_location == 'zipcode':
            if number_of_tokens >= 3 or (number_of_tokens > 1 and digits and not zipcode and not apartment):
                if augment_type == AugmentType.MIMIC:
                    return LocationFormat(1.0, 0.0, 0.0, 0.0, 0.0, 0.0)
                elif augment_type == AugmentType.MIMIC_PROBABILITY:
                    return LocationFormat(0.8, 0.0, 0.05, 0.05, 0.05, 0.05)
                else:
                    raise ValueError('Invalid augment type')
            elif apartment:
                if augment_type == AugmentType.MIMIC:
                    return LocationFormat(0.0, 1.0, 0.0, 0.0, 0.0, 0.0)
                elif augment_type == AugmentType.MIMIC_PROBABILITY:
                    return LocationFormat(0.05, 0.8, 0.05, 0.05, 0.05, 0.0)
                else:
                    raise ValueError('Invalid augment type')
            elif zipcode:
                if augment_type == AugmentType.MIMIC:
                    return LocationFormat(0.0, 0.0, 0.0, 0.0, 0.0, 1.0)
                elif augment_type == AugmentType.MIMIC_PROBABILITY:
                    return LocationFormat(0.05, 0.0, 0.05, 0.05, 0.05, 0.8)
                else:
                    raise ValueError('Invalid augment type')
            else:
                if augment_type == AugmentType.MIMIC:
                    return LocationFormat(0.0, 0.0, 0.5, 0.5, 0.0, 0.0)
                elif augment_type == AugmentType.MIMIC_PROBABILITY:
                    return LocationFormat(0.05, 0.05, 0.4, 0.4, 0.05, 0.05)
                else:
                    raise ValueError('Invalid augment type')

        elif previous_location == 'street':
            if zipcode:
                if augment_type == AugmentType.MIMIC:
                    return LocationFormat(0.0, 0.0, 0.0, 0.0, 0.0, 1.0)
                elif augment_type == AugmentType.MIMIC_PROBABILITY:
                    return LocationFormat(0.05, 0.0, 0.05, 0.05, 0.05, 0.8)
                else:
                    raise ValueError('Invalid augment type')
            elif apartment or digits:
                if augment_type == AugmentType.MIMIC:
                    return LocationFormat(0.0, 1.0, 0.0, 0.0, 0.0, 0.0)
                elif augment_type == AugmentType.MIMIC_PROBABILITY:
                    return LocationFormat(0.05, 0.8, 0.05, 0.05, 0.05, 0.0)
                else:
                    raise ValueError('Invalid augment type')
            else:
                if augment_type == AugmentType.MIMIC:
                    return LocationFormat(0.0, 0.0, 1.0, 0.0, 0.0, 0.0)
                elif augment_type == AugmentType.MIMIC_PROBABILITY:
                    return LocationFormat(0.05, 0.0, 0.8, 0.05, 0.05, 0.05)
                else:
                    raise ValueError('Invalid augment type')

        elif previous_location == 'apartment':
            if zipcode:
                if augment_type == AugmentType.MIMIC:
                    return LocationFormat(0.0, 0.0, 0.0, 0.0, 0.0, 1.0)
                elif augment_type == AugmentType.MIMIC_PROBABILITY:
                    return LocationFormat(0.05, 0.0, 0.05, 0.05, 0.05, 0.8)
                else:
                    raise ValueError('Invalid augment type')
            else:
                if augment_type == AugmentType.MIMIC:
                    return LocationFormat(0.0, 0.0, 1.0, 0.0, 0.0, 0.0)
                elif augment_type == AugmentType.MIMIC_PROBABILITY:
                    return LocationFormat(0.05, 0.0, 0.8, 0.05, 0.05, 0.05)
                else:
                    raise ValueError('Invalid augment type')

        elif previous_location == 'city':
            if zipcode:
                if augment_type == AugmentType.MIMIC:
                    return LocationFormat(0.0, 0.0, 0.0, 0.0, 0.0, 1.0)
                elif augment_type == AugmentType.MIMIC_PROBABILITY:
                    return LocationFormat(0.05, 0.0, 0.05, 0.05, 0.05, 0.8)
                else:
                    raise ValueError('Invalid augment type')
            elif apartment:
                if augment_type == AugmentType.MIMIC:
                    return LocationFormat(0.0, 1.0, 0.0, 0.0, 0.0, 0.0)
                elif augment_type == AugmentType.MIMIC_PROBABILITY:
                    return LocationFormat(0.05, 0.8, 0.05, 0.05, 0.05, 0.0)
                else:
                    raise ValueError('Invalid augment type')
            else:
                if augment_type == AugmentType.MIMIC:
                    return LocationFormat(0.0, 0.0, 0.0, 1.0, 0.0, 0.0)
                elif augment_type == AugmentType.MIMIC_PROBABILITY:
                    return LocationFormat(0.05, 0.0, 0.05, 0.8, 0.05, 0.05)
                else:
                    raise ValueError('Invalid augment type')

        elif previous_location == 'state':
            if zipcode:
                if augment_type == AugmentType.MIMIC:
                    return LocationFormat(0.0, 0.0, 0.0, 0.0, 0.0, 1.0)
                elif augment_type == AugmentType.MIMIC_PROBABILITY:
                    return LocationFormat(0.05, 0.0, 0.05, 0.05, 0.05, 0.8)
                else:
                    raise ValueError('Invalid augment type')
            elif apartment:
                if augment_type == AugmentType.MIMIC:
                    return LocationFormat(0.0, 1.0, 0.0, 0.0, 0.0, 0.0)
                elif augment_type == AugmentType.MIMIC_PROBABILITY:
                    return LocationFormat(0.05, 0.8, 0.05, 0.05, 0.05, 0.0)
                else:
                    raise ValueError('Invalid augment type')
            else:
                if augment_type == AugmentType.MIMIC:
                    return LocationFormat(0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
                elif augment_type == AugmentType.MIMIC_PROBABILITY:
                    return LocationFormat(0.05, 0.0, 0.05, 0.05, 0.8, 0.05)
                else:
                    raise ValueError('Invalid augment type')

        elif previous_location == 'country':
            if zipcode:
                if augment_type == AugmentType.MIMIC:
                    return LocationFormat(0.0, 0.0, 0.0, 0.0, 0.0, 1.0)
                elif augment_type == AugmentType.MIMIC_PROBABILITY:
                    return LocationFormat(0.05, 0.0, 0.05, 0.05, 0.05, 0.8)
                else:
                    raise ValueError('Invalid augment type')
            elif apartment:
                if augment_type == AugmentType.MIMIC:
                    return LocationFormat(0.0, 1.0, 0.0, 0.0, 0.0, 0.0)
                elif augment_type == AugmentType.MIMIC_PROBABILITY:
                    return LocationFormat(0.05, 0.8, 0.05, 0.05, 0.05, 0.0)
                else:
                    raise ValueError('Invalid augment type')
            else:
                if re.search(r'(\b\w+\b)', original_text, flags=re.IGNORECASE):
                    if augment_type == AugmentType.MIMIC:
                        return LocationFormat(0.0, 0.0, 0.0, 0.5, 0.5, 0.0)
                    elif augment_type == AugmentType.MIMIC_PROBABILITY:
                        return LocationFormat(0.05, 0.05, 0.05, 0.4, 0.4, 0.05)
                    else:
                        raise ValueError('Invalid augment type')
                else:
                    return LocationFormat(0.1, 0.0, 0.15, 0.25, 0.25, 0.25)
        else:
            LocationFormat(0.25, 0.0, 0.25, 0.25, 0.15, 0.1)

    @staticmethod
    def get_abbreviated_probability(augment_type, original_text):
        acronym_regex = r'(\b[A-Z][A-Z]\b)|(\bU(\.)?S(\.)?(A(\.)?)?\b)|(^[a-z][a-z]$)'
        if original_text is not None and re.search(acronym_regex, original_text, flags=re.IGNORECASE):
            abbreviated = True
        else:
            abbreviated = False
        if augment_type == AugmentType.RANDOM:
            return 0.8
        elif augment_type == AugmentType.MIMIC:
            if abbreviated:
                return 1.0
            else:
                return 0.0
        elif augment_type == AugmentType.MIMIC_PROBABILITY:
            if abbreviated:
                return 0.8
            else:
                return 0.2
        elif augment_type == AugmentType.CUSTOM:
            raise NotImplementedError('Passing custom probabilities not implemented yet')
        else:
            raise ValueError('Invalid augment type')
