import re
import numpy as np

from .augment_type import AugmentType
from .utils import get_casing_probabilities, get_text, get_upper, get_lower


class OtherPHIAugment(object):

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

        url_probability = self.get_url_probability(augment_type=augment_type, original_text=original_text)

        other_phi = np.random.choice(
            [self.get_url, self.get_ip], p=[url_probability, 1 - url_probability]
        )()

        return np.random.choice(
            [get_text, get_upper, get_lower],
            p=[camel_case_probability, upper_case_probability, lower_case_probability]
        )(other_phi).strip()

    def get_url(self):
        return np.random.choice(
            [
                self._fake.domain_name,
                self._fake.hostname,
                self._fake.uri
            ]
        )()

    def get_ip(self):
        return np.random.choice(
            [
                self._fake.ipv4,
                self._fake.ipv4_public,
                self._fake.ipv4_private,
                self._fake.ipv6,
                self._fake.mac_address,
            ]
        )()

    @staticmethod
    def get_url_probability(augment_type, original_text):
        url_regex = r'(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))'
        if original_text is not None and re.search(url_regex, original_text, flags=re.IGNORECASE):
            url = True
        else:
            url = False
        if augment_type == AugmentType.RANDOM:
            return 0.8

        if url:
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
