import random
import string
import numpy as np


class CharacterNoiseAugment(object):

    def __init__(self, text_tokenizer, noise):
        self._text_tokenizer = text_tokenizer
        self._noise = noise

    def augment(self, tokens, token_positions, labels):
        new_tokens = list()
        for token in tokens:
            token_text = self.get_token_text(token=token, token_positions=token_positions)

            if np.random.rand() <= self._noise:
                noisy_token_text = self.add_noise(text=token_text)
                noisy_token = self._text_tokenizer.get_tokens(noisy_token_text)
                if len(noisy_token) > 1:
                    new_tokens.append(token)
                else:
                    print(noisy_token)
                    new_tokens.extend(noisy_token)
            else:
                new_tokens.append(token)
        return new_tokens, labels

    @staticmethod
    def add_noise(text):

        position = random.choice(range(len(text)))
        original_character = text[position]

        if original_character.isalpha():
            if original_character.isupper():
                new_character = random.choice(string.ascii_uppercase)
            else:
                new_character = random.choice(string.ascii_lowercase)
        elif original_character.isnumeric():
            new_character = random.choice(string.digits)
        else:
            new_character = random.choice(string.punctuation)

        return text[:position] + new_character + text[position + 1:]

    @staticmethod
    def get_token_text(token, token_positions):
        # Assumption is we have spacy token objects - hence the following code
        # will work. Ideally we don't want the code to be coupled to depend
        # on spacy tokens - so we have another else statement that uses
        # token positions.
        if token_positions is None:
            return token.text
        # Here the assumption is that tokens contains the token text
        # and not spacy token object
        else:
            # Reconstruct span text based on token positions and token text
            return token



