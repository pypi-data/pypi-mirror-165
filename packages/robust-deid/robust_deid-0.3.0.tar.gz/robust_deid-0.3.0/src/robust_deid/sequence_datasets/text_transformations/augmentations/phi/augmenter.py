import re
from collections import namedtuple

from typing import Union, Type

from seqeval.metrics.sequence_labeling import get_entities
from seqeval.scheme import IOBES, IOB2, BILOU, IOB1, Entities


class PHIAugmenter(object):

    def __init__(
            self,
            text_tokenizer,
            notation,
            augment_type,
            patient_augment,
            staff_augment,
            age_augment,
            phone_augment,
            patorg_augment,
            email_augment,
            hospital_augment,
            id_augment,
            location_augment,
            other_phi_augment,
            date_augment
    ):
        self._text_tokenizer = text_tokenizer
        self._scheme = self.__get_scheme(notation=notation)
        self.augment_type = augment_type
        self.patient_augment = patient_augment
        self.staff_augment = staff_augment
        self.age_augment = age_augment
        self.phone_augment = phone_augment
        self.patorg_augment = patorg_augment
        self.email_augment = email_augment
        self.hospital_augment = hospital_augment
        self.id_augment = id_augment
        self.location_augment = location_augment
        self.other_phi_augment = other_phi_augment
        self.date_augment = date_augment
        if notation == 'BIO':
            self._prefix_single = 'B-'
            self._prefix_begin = 'B-'
            self._prefix_inside = 'I-'
            self._prefix_end = 'I-'
            self._prefix_outside = 'O'
        elif notation == 'BIOES':
            self._prefix_single = 'S-'
            self._prefix_begin = 'B-'
            self._prefix_inside = 'I-'
            self._prefix_end = 'E-'
            self._prefix_outside = 'O'
        elif notation == 'BILOU':
            self._prefix_single = 'U-'
            self._prefix_begin = 'B-'
            self._prefix_inside = 'I-'
            self._prefix_end = 'L-'
            self._prefix_outside = 'O'
        elif notation == 'IO':
            self._prefix_single = 'I-'
            self._prefix_begin = 'I-'
            self._prefix_inside = 'I-'
            self._prefix_end = 'I-'
            self._prefix_outside = 'O'

    @staticmethod
    def __get_scheme(notation: str) -> Union[Type[IOB2], Type[IOBES], Type[BILOU], Type[IOB1]]:
        """
        Get the seqeval scheme based on the notation
        Args:
            notation (str): The NER notation
        Returns:
            (Union[IOB2, IOBES, BILOU, IOB1]): The seqeval scheme
        """
        if notation == 'BIO':
            return IOB2
        elif notation == 'BIOES':
            return IOBES
        elif notation == 'BILOU':
            return BILOU
        elif notation == 'IO':
            return IOB1
        else:
            raise ValueError('Invalid Notation')

    # @staticmethod
    # def reconstruct_text_from_whitespaces(tokens, whitespaces):
    #     return ''.join([whitespace + token for token, whitespace in zip(tokens, whitespaces)])

    @staticmethod
    def reconstruct_text_from_whitespaces(tokens, whitespaces, token_positions):
        text = ''
        previous_whitespace = ''
        start = 0
        for token, whitespace, token_position in zip(tokens, whitespaces, token_positions):
            if previous_whitespace == '':
                if whitespace[1] == '':
                    text += (' ' * (token_position[0] - start) + token + whitespace[0])
                else:
                    text += whitespace[1] + token + whitespace[0]
            else:
                text += token + whitespace[0]
            start = token_position[1]
            previous_whitespace = whitespace[0]
        return text

    @staticmethod
    def reconstruct_text(tokens, token_positions):
        # Assumption is we have spacy token objects - hence the following code
        # will work. Ideally we don't want the code to be coupled to depend
        # on spacy tokens - so we have another else statement that uses
        # token positions.
        if token_positions is None:
            return ''.join([token.text + token.whitespace_ for token in tokens])
        # Here the assumption is that tokens contains the token text
        # and not spacy token object
        else:
            # Reconstruct span text based on token positions and token text
            text = ''
            start = 0
            for token, token_position in zip(tokens, token_positions):
                # Add spaces between the consecutive tokens
                text += (' ' * min(1, token_position[0] - start)) + token
                start = token_position[1]
            return text

    def augment(self, tokens, token_positions, labels):
        new_tokens = list()
        new_labels = list()
        Entity = namedtuple('Entity', ['tag', 'start', 'end'])
        # Get the entities
        entity_start = 0
        previous_location = None
        previous_location_index = 0
        # Strict version:
        # entities = Entities(sequences=[labels], scheme=self._scheme, suffix=False)
        # for entity in entities.entities[0]:
        for entity_ in get_entities(labels):
            entity = Entity(entity_[0], entity_[1], entity_[2] + 1)
            # if entity.tag != 'LOC' or previous_location == 'zipcode':
            if entity.tag != 'LOC':
                previous_location = None
            elif entity.tag == 'LOC' and entity.start - previous_location_index >= 5 and previous_location is not None:
                previous_location = None
            start = entity.start
            # Add any tokens and labels not part of an entity/span
            new_tokens.extend(tokens[entity_start:start])
            new_labels.extend(labels[entity_start:start])
            # When augmenting we use the current text - the line below extracts
            # the text present in the staff span
            text = self.reconstruct_text(
                tokens[entity.start:entity.end],
                token_positions[entity.start:entity.end] if token_positions else None
            ).strip()
            # There is text that contains only special characters but are annotated as
            # some spans - we remove these annotations
            if self.check_only_special(text=text):
                special_char_tokens = self._text_tokenizer.get_tokens(text)
                new_tokens.extend(special_char_tokens)
                new_labels.extend(['O'] * len(special_char_tokens))
            elif entity.tag == 'PATIENT':
                # Get the augmented patient tokens
                patient_tokens = self.augment_patient_tokens(original_text=text)
                # Add the augmented patient tokens
                new_tokens.extend(patient_tokens)
                # Update the labels based on the augmented patient tokens
                new_labels.extend(self.augment_labels(entity.tag, len(patient_tokens)))
            # Augment the staff tokens
            elif entity.tag == 'STAFF':
                # Get the augmented staff tokens
                staff_tokens = self.augment_staff_tokens(original_text=text)
                # Add the augmented staff tokens
                new_tokens.extend(staff_tokens)
                # Update the labels based on the augmented staff tokens
                new_labels.extend(self.augment_labels(entity.tag, len(staff_tokens)))
            elif entity.tag == 'AGE':
                # Get the augmented age tokens
                age_tokens = self.augment_age_tokens(original_text=text)
                # Add the augmented age tokens
                new_tokens.extend(age_tokens)
                # Update the labels based on the augmented age tokens
                new_labels.extend(self.augment_labels(entity.tag, len(age_tokens)))
            elif entity.tag == 'PHONE':
                # Get the augmented phone tokens
                phone_tokens = self.augment_phone_tokens(original_text=text)
                # Add the augmented phone tokens
                new_tokens.extend(phone_tokens)
                # Update the labels based on the augmented phone tokens
                new_labels.extend(self.augment_labels(entity.tag, len(phone_tokens)))
            elif entity.tag == 'PATORG':
                # Get the augmented patorg tokens
                patorg_tokens = self.augment_patorg_tokens(original_text=text)
                # Add the augmented patorg tokens
                new_tokens.extend(patorg_tokens)
                # Update the labels based on the augmented patorg tokens
                new_labels.extend(self.augment_labels(entity.tag, len(patorg_tokens)))
            elif entity.tag == 'EMAIL':
                # Get the augmented email tokens
                email_tokens = self.augment_email_tokens(original_text=text)
                # Add the augmented email tokens
                new_tokens.extend(email_tokens)
                # Update the labels based on the augmented email tokens
                new_labels.extend(self.augment_labels(entity.tag, len(email_tokens)))
            elif entity.tag == 'HOSP':
                # Get the augmented hospital tokens
                hosp_tokens = self.augment_hospital_tokens(original_text=text)
                # Add the augmented hospital tokens
                new_tokens.extend(hosp_tokens)
                # Update the labels based on the augmented hospital tokens
                new_labels.extend(self.augment_labels(entity.tag, len(hosp_tokens)))
            elif entity.tag == 'ID':
                # Get the augmented id tokens
                id_tokens = self.augment_id_tokens(original_text=text)
                # Add the augmented id tokens
                new_tokens.extend(id_tokens)
                # Update the labels based on the augmented id tokens
                new_labels.extend(self.augment_labels(entity.tag, len(id_tokens)))
            elif entity.tag == 'OTHERPHI':
                # Get the augmented other phi tokens
                other_phi_tokens = self.augment_other_phi_tokens(original_text=text)
                # Add the augmented other phi tokens
                new_tokens.extend(other_phi_tokens)
                # Update the labels based on the augmented other phi tokens
                new_labels.extend(self.augment_labels(entity.tag, len(other_phi_tokens)))
            elif entity.tag == 'LOC':
                # We have them separately because we annotate each location component independently
                location_tokens, location_type = self.augment_location_tokens(
                    original_text=text, previous_location=previous_location
                )
                previous_location = location_type
                # Add the augmented other phi tokens
                new_tokens.extend(location_tokens)
                # Update the labels based on the augmented other phi tokens
                new_labels.extend(self.augment_labels(entity.tag, len(location_tokens)))
                previous_location_index = entity.end
            elif entity.tag == 'DATE':
                date_tokens = self.augment_date_tokens(original_text=text)
                new_labels.extend(self.augment_labels(entity.tag, len(date_tokens)))
                new_tokens.extend(date_tokens)
            else:
                raise NotImplementedError('Augmentation for this entity type is not implemented')
            entity_start = entity.end
        new_tokens.extend(tokens[entity_start:])
        new_labels.extend(labels[entity_start:])
        return new_tokens, new_labels

    @staticmethod
    def check_only_special(text):
        if re.search(r'^\W+$', text):
            return True
        else:
            return False

    def augment_labels(self, entity_tag, tokens_length):
        # Return a list of labels that align with the tokens
        # This function returns the token level labels for the
        # augmented tokens
        labels = list()
        # If there is only one augmented token, the label is the entity type
        # prefixed with the single label
        if tokens_length == 1:
            labels.append(self._prefix_single + entity_tag)
        # If there is more than one augmented token
        if tokens_length > 1:
            for i in range(tokens_length):
                # Prefix with begin label for the first token
                if i == 0:
                    labels.append(self._prefix_begin + entity_tag)
                # Prefix with end label for the last token
                elif i == tokens_length - 1:
                    labels.append(self._prefix_end + entity_tag)
                # Prefix with the inside label otherwise
                else:
                    labels.append(self._prefix_inside + entity_tag)
        # Return the labels for the tokens
        return labels

    def augment_patient_tokens(self, original_text):
        # Get the augmented text and then return the tokenized augmented text
        augmented_text = self.patient_augment.generate(
            original_text=original_text, augment_type=self.augment_type
        )
        return self._text_tokenizer.get_tokens(augmented_text)

    def augment_staff_tokens(self, original_text):
        # Get the augmented text and then return the tokenized augmented text
        augmented_text = self.staff_augment.generate(
            original_text=original_text, augment_type=self.augment_type
        )
        return self._text_tokenizer.get_tokens(augmented_text)

    def augment_age_tokens(self, original_text):
        # Get the augmented text and then return the tokenized augmented text
        augmented_text = self.age_augment.generate(
            original_text=original_text, augment_type=self.augment_type
        )
        return self._text_tokenizer.get_tokens(augmented_text)

    def augment_phone_tokens(self, original_text):
        # Get the augmented text and then return the tokenized augmented text
        augmented_text = self.phone_augment.generate(
            original_text=original_text, augment_type=self.augment_type
        )
        return self._text_tokenizer.get_tokens(augmented_text)

    def augment_patorg_tokens(self, original_text):
        # Get the augmented text and then return the tokenized augmented text
        augmented_text = self.patorg_augment.generate(
            original_text=original_text, augment_type=self.augment_type
        )
        # print('Original Text: ', original_text)
        # print('Augmented Text: ', augmented_text)
        return self._text_tokenizer.get_tokens(augmented_text)

    def augment_email_tokens(self, original_text):
        # Get the augmented text and then return the tokenized augmented text
        augmented_text = self.email_augment.generate(
            original_text=original_text, augment_type=self.augment_type
        )
        return self._text_tokenizer.get_tokens(augmented_text)

    def augment_hospital_tokens(self, original_text):
        # Get the augmented text and then return the tokenized augmented text
        augmented_text = self.hospital_augment.generate(
            original_text=original_text, augment_type=self.augment_type
        )
        return self._text_tokenizer.get_tokens(augmented_text)

    def augment_id_tokens(self, original_text):
        # Get the augmented text and then return the tokenized augmented text
        augmented_text = self.id_augment.generate(
            original_text=original_text, augment_type=self.augment_type
        )
        return self._text_tokenizer.get_tokens(augmented_text)

    def augment_other_phi_tokens(self, original_text):
        # Get the augmented text and then return the tokenized augmented text
        augmented_text = self.other_phi_augment.generate(
            original_text=original_text, augment_type=self.augment_type
        )
        return self._text_tokenizer.get_tokens(augmented_text)

    def augment_location_tokens(self, original_text, previous_location):
        # Get the augmented text and then return the tokenized augmented text
        augmented_text, location_type = self.location_augment.generate(
            original_text=original_text, augment_type=self.augment_type, previous_location=previous_location
        )
        return self._text_tokenizer.get_tokens(augmented_text), location_type

    def augment_date_tokens(self, original_text):
        # Get the augmented text and then return the tokenized augmented text
        augmented_text = self.date_augment.generate(
            original_text=original_text, augment_type=self.augment_type
        )
        return self._text_tokenizer.get_tokens(augmented_text)
