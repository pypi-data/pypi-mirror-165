import re
from collections import namedtuple

from seqeval.metrics.sequence_labeling import get_entities

from .deidentification_types import DeidentificationLevel, DeidentificationStrategy


class TextDeidentification(object):

    def __init__(self, ner_augmenter):

        self._ner_augmenter = ner_augmenter

    @staticmethod
    def __get_relaxed_predictions(predictions):
        return ['I-' + prediction[2:] if prediction != 'O' else prediction for prediction in predictions]

    def get_ner_spans(self, tokens, predictions, token_positions, whitespaces, deidentification_level):
        offset = token_positions[0][0]
        Entity = namedtuple('Entity', ['tag', 'start', 'end'])
        if deidentification_level == DeidentificationLevel.RELAXED:
            predictions = self.__get_relaxed_predictions(predictions)
        elif deidentification_level == DeidentificationLevel.EXACT:
            predictions = predictions
        else:
            raise ValueError('Invalid deidentification level')

        for entity_ in get_entities(predictions):
            entity = Entity(entity_[0], entity_[1], entity_[2] + 1)
            text = self._ner_augmenter.reconstruct_text_from_whitespaces(
                tokens[entity.start:entity.end],
                whitespaces[entity.start:entity.end],
                token_positions[entity.start:entity.end]
            )
            position = (token_positions[entity.start][0], token_positions[entity.end - 1][1])
            if self._ner_augmenter.check_only_special(text=text):
                continue
            else:
                yield {
                    'start': position[0] - offset,
                    'end': position[1] - offset,
                    'text': text.strip(),
                    'label': entity.tag
                }

    def get_text(self, tokens, whitespaces, token_positions):
        return self._ner_augmenter.reconstruct_text_from_whitespaces(
            tokens,
            whitespaces,
            token_positions
        ).strip()

    def de_identify_text(self, text, entities, deidentification_strategy):
        entity_start = 0
        entity_offset = 0
        de_identified_text = ''
        previous_location = None
        previous_location_index = 0
        Entity = namedtuple('Entity', ['tag', 'start', 'end'])
        spans = list()

        for entity_ in entities:
            check_special = False
            entity = Entity(entity_['label'], entity_['start'], entity_['end'])

            if entity.tag != 'LOC' or previous_location == 'zipcode':
                previous_location = None
            elif entity.tag == 'LOC' and entity.start - previous_location_index >= 5 and previous_location is not None:
                previous_location = None

            start = entity.start
            de_identified_text += text[entity_start:start]

            entity_text = text[entity.start:entity.end]

            if self._ner_augmenter.check_only_special(text=entity_text):
                augmented_text = entity_text
                check_special = True
            elif entity.tag == 'PATIENT':
                augmented_text = self.de_identify_patient(
                    text=entity_text, deidentification_strategy=deidentification_strategy
                )
            elif entity.tag == 'STAFF':
                augmented_text = self.de_identify_staff(
                    text=entity_text, deidentification_strategy=deidentification_strategy
                )
            elif entity.tag == 'AGE':
                augmented_text = self.de_identify_age(
                    text=entity_text, deidentification_strategy=deidentification_strategy
                )
            elif entity.tag == 'PHONE':
                augmented_text = self.de_identify_phone(
                    text=entity_text, deidentification_strategy=deidentification_strategy
                )
            elif entity.tag == 'PATORG':
                augmented_text = self.de_identify_patorg(
                    text=entity_text, deidentification_strategy=deidentification_strategy
                )
            elif entity.tag == 'EMAIL':
                augmented_text = self.de_identify_email(
                    text=entity_text, deidentification_strategy=deidentification_strategy
                )
            elif entity.tag == 'HOSP':
                augmented_text = self.de_identify_hospital(
                    text=entity_text, deidentification_strategy=deidentification_strategy
                )
            elif entity.tag == 'ID':
                augmented_text = self.de_identify_id(
                    text=entity_text, deidentification_strategy=deidentification_strategy
                )
            elif entity.tag == 'OTHERPHI':
                augmented_text = self.de_identify_other_phi(
                    text=entity_text, deidentification_strategy=deidentification_strategy
                )
            elif entity.tag == 'LOC':
                location_text, location_type = self.de_identify_location(
                    text=entity_text,
                    deidentification_strategy=deidentification_strategy,
                    previous_location=previous_location
                )
                augmented_text = location_text
                previous_location = location_type
                previous_location_index = entity.end
            elif entity.tag == 'DATE':
                augmented_text = self.de_identify_date(
                    text=entity_text, deidentification_strategy=deidentification_strategy
                )
            else:
                raise NotImplementedError('Augmentation for this entity type is not implemented')

            de_identified_text += augmented_text
            entity_start = entity.end

            if not check_special and deidentification_strategy == DeidentificationStrategy.AUGMENT:
                de_id_entity_start = start + entity_offset
                de_id_entity_end = de_id_entity_start + len(augmented_text)
                entity_offset = de_id_entity_end - entity.end
                de_id_span = {
                    'start': de_id_entity_start,
                    'end': de_id_entity_end,
                    'text': augmented_text,
                    'label': entity.tag
                }
                spans.append(de_id_span)

        de_identified_text += text[entity_start:]
        return de_identified_text, spans

    def de_identify_patient(self, text, deidentification_strategy):
        if deidentification_strategy == DeidentificationStrategy.AUGMENT:
            # Get the augmented patient tokens
            return self._ner_augmenter.patient_augment.generate(
                original_text=re.sub(r'\s+', ' ', text),
                augment_type=self._ner_augmenter.augment_type
            )
        elif deidentification_strategy == DeidentificationStrategy.INFORMATIVE:
            return f'<<PATIENT:{text}>>'
        elif deidentification_strategy == DeidentificationStrategy.REMOVE:
            return ''

    def de_identify_staff(self, text, deidentification_strategy):
        if deidentification_strategy == DeidentificationStrategy.AUGMENT:
            # Get the augmented patient tokens
            return self._ner_augmenter.staff_augment.generate(
                original_text=re.sub(r'\s+', ' ', text),
                augment_type=self._ner_augmenter.augment_type
            )
        elif deidentification_strategy == DeidentificationStrategy.INFORMATIVE:
            return f'<<STAFF:{text}>>'
        elif deidentification_strategy == DeidentificationStrategy.REMOVE:
            return ''

    def de_identify_age(self, text, deidentification_strategy):
        if deidentification_strategy == DeidentificationStrategy.AUGMENT:
            # Get the augmented patient tokens
            return self._ner_augmenter.age_augment.generate(
                original_text=re.sub(r'\s+', ' ', text),
                augment_type=self._ner_augmenter.augment_type
            )
        elif deidentification_strategy == DeidentificationStrategy.INFORMATIVE:
            return f'<<AGE:{text}>>'
        elif deidentification_strategy == DeidentificationStrategy.REMOVE:
            return ''

    def de_identify_phone(self, text, deidentification_strategy):
        if deidentification_strategy == DeidentificationStrategy.AUGMENT:
            # Get the augmented patient tokens
            return self._ner_augmenter.phone_augment.generate(
                original_text=re.sub(r'\s+', ' ', text),
                augment_type=self._ner_augmenter.augment_type
            )
        elif deidentification_strategy == DeidentificationStrategy.INFORMATIVE:
            return f'<<PHONE:{text}>>'
        elif deidentification_strategy == DeidentificationStrategy.REMOVE:
            return ''

    def de_identify_patorg(self, text, deidentification_strategy):
        if deidentification_strategy == DeidentificationStrategy.AUGMENT:
            # Get the augmented patient tokens
            return self._ner_augmenter.patorg_augment.generate(
                original_text=re.sub(r'\s+', ' ', text),
                augment_type=self._ner_augmenter.augment_type
            )
        elif deidentification_strategy == DeidentificationStrategy.INFORMATIVE:
            return f'<<PATORG:{text}>>'
        elif deidentification_strategy == DeidentificationStrategy.REMOVE:
            return ''

    def de_identify_email(self, text, deidentification_strategy):
        if deidentification_strategy == DeidentificationStrategy.AUGMENT:
            # Get the augmented patient tokens
            return self._ner_augmenter.email_augment.generate(
                original_text=re.sub(r'\s+', ' ', text),
                augment_type=self._ner_augmenter.augment_type
            )
        elif deidentification_strategy == DeidentificationStrategy.INFORMATIVE:
            return f'<<EMAIL:{text}>>'
        elif deidentification_strategy == DeidentificationStrategy.REMOVE:
            return ''

    def de_identify_hospital(self, text, deidentification_strategy):
        if deidentification_strategy == DeidentificationStrategy.AUGMENT:
            # Get the augmented patient tokens
            return self._ner_augmenter.hospital_augment.generate(
                original_text=re.sub(r'\s+', ' ', text),
                augment_type=self._ner_augmenter.augment_type,
            )
        elif deidentification_strategy == DeidentificationStrategy.INFORMATIVE:
            return f'<<HOSPITAL:{text}>>'
        elif deidentification_strategy == DeidentificationStrategy.REMOVE:
            return ''

    def de_identify_id(self, text, deidentification_strategy):
        if deidentification_strategy == DeidentificationStrategy.AUGMENT:
            # Get the augmented patient tokens
            return self._ner_augmenter.id_augment.generate(
                original_text=re.sub(r'\s+', ' ', text),
                augment_type=self._ner_augmenter.augment_type
            )
        elif deidentification_strategy == DeidentificationStrategy.INFORMATIVE:
            return f'<<ID:{text}>>'
        elif deidentification_strategy == DeidentificationStrategy.REMOVE:
            return ''

    def de_identify_other_phi(self, text, deidentification_strategy):
        if deidentification_strategy == DeidentificationStrategy.AUGMENT:
            # Get the augmented patient tokens
            return self._ner_augmenter.other_phi_augment.generate(
                original_text=re.sub(r'\s+', ' ', text),
                augment_type=self._ner_augmenter.augment_type
            )
        elif deidentification_strategy == DeidentificationStrategy.INFORMATIVE:
            return f'<<URL:{text}>>'
        elif deidentification_strategy == DeidentificationStrategy.REMOVE:
            return ''

    def de_identify_location(self, text, deidentification_strategy, previous_location):
        if deidentification_strategy == DeidentificationStrategy.AUGMENT:
            # Get the augmented patient tokens
            return self._ner_augmenter.location_augment.generate(
                original_text=re.sub(r'\s+', ' ', text),
                augment_type=self._ner_augmenter.augment_type,
                previous_location=previous_location
            )
        elif deidentification_strategy == DeidentificationStrategy.INFORMATIVE:
            return f'<<LOCATION:{text}>>', None
        elif deidentification_strategy == DeidentificationStrategy.REMOVE:
            return '', None

    def de_identify_date(self, text, deidentification_strategy):
        if deidentification_strategy == DeidentificationStrategy.AUGMENT:
            # Get the augmented patient tokens
            return self._ner_augmenter.date_augment.generate(
                original_text=re.sub(r'\s+', ' ', text),
                augment_type=self._ner_augmenter.augment_type
            )
        elif deidentification_strategy == DeidentificationStrategy.INFORMATIVE:
            return f'<<DATE:{text}>>'
        elif deidentification_strategy == DeidentificationStrategy.REMOVE:
            return ''
