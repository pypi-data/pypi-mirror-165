import logging
from typing import Optional, Mapping, Sequence

from transformers import PreTrainedTokenizerFast


class TextTransform(object):

    def __init__(
            self,
            text_tokenizer,
            align_token_labels,
            tokenizer,
            span_fixer,
            ner_augmenter=None,
            character_noise_augmenter=None,
            truncation: bool = True,
            pad_to_max_length: bool = False,
            max_seq_length: Optional[int] = 512,
            label_to_id: Mapping[str, int] = None,
            label_all_tokens: bool = False,
            b_to_i_label: Sequence[int] = None
    ):
        self._text_tokenizer = text_tokenizer
        self._span_fixer = span_fixer
        self._align_token_labels = align_token_labels
        self._tokenizer = tokenizer
        self._ner_augmenter = ner_augmenter
        self._character_noise_augmenter = character_noise_augmenter
        self._truncation = truncation
        self._padding = "max_length" if pad_to_max_length else False
        self._pad_to_max_length = pad_to_max_length
        self._max_seq_length = self._get_max_seq_length(tokenizer=tokenizer, max_seq_length=max_seq_length)
        self._label_to_id = label_to_id
        self._label_all_tokens = label_all_tokens
        self._b_to_i_label = b_to_i_label
        self._ignore_label = -100
        self._token_ignore_label = 'NA'
        self._split = None

    def set_split(self, split):
        self._split = split

    @staticmethod
    def get_token_text(tokens):
        return [token.text for token in tokens]

    @staticmethod
    def __get_whitespaces_back(text, tokens, token_positions):
        previous_end = 0
        whitespaces = list()
        for token, token_position in zip(tokens, token_positions):
            whitespaces.append(text[previous_end:token_position[0]])
            previous_end = token_position[1]
        return whitespaces

    @staticmethod
    def __get_whitespaces_front(text, tokens, token_positions):
        previous_start = len(text)
        whitespaces = list()
        for token, token_position in zip(reversed(tokens), reversed(token_positions)):
            whitespaces.append(text[token_position[1]:previous_start])
            previous_start = token_position[0]
        whitespaces.reverse()
        return whitespaces

    def get_whitespaces(self, text, tokens, token_positions):
        whitespaces_front = self.__get_whitespaces_front(text, tokens, token_positions)
        whitespaces_back = self.__get_whitespaces_back(text, tokens, token_positions)
        return [
            (whitespace_front, whitespace_back)
            for whitespace_front, whitespace_back in zip(whitespaces_front, whitespaces_back)
        ]

    @staticmethod
    def __get_token_positions_dict(tokens):
        """
        Get the start and end positions of all the tokens in the note.
        Args:
            tokens (): The text present in the note
        Returns:
            token_start_positions (Mapping[int, int]): The start positions of all the tokens in the note
            token_end_positions (Mapping[int, int]): The end positions of all the tokens in the note
        """
        token_start_positions = dict()
        token_end_positions = dict()
        for token in tokens:
            start = token.idx
            end = start + len(token)
            token_start_positions[start] = 1
            token_end_positions[end] = 1
        return token_start_positions, token_end_positions

    @staticmethod
    def __get_offset_token_positions_tuple(tokens, offset=0):
        """
        Get the start and end positions of all the tokens in the note.
        Args:
            tokens (): The text present in the note
        Returns:
            token_start_positions (Mapping[int, int]): The start positions of all the tokens in the note
            token_end_positions (Mapping[int, int]): The end positions of all the tokens in the note
        """
        return [(offset + token.idx, offset + token.idx + len(token)) for token in tokens]

    @staticmethod
    def __get_token_positions_tuple(tokens):
        """
        Get the start and end positions of all the tokens in the note.
        Args:
            tokens (): The text present in the note
        Returns:
            token_start_positions (Mapping[int, int]): The start positions of all the tokens in the note
            token_end_positions (Mapping[int, int]): The end positions of all the tokens in the note
        """
        return [(token.idx, token.idx + len(token)) for token in tokens]

    def get_fixed_spans(self, text, spans, tokens):

        if self._span_fixer is None or spans == []:
            return spans

        # 2.1 Get token positions as dict
        # Get token start and end positions for fixing the spans
        token_start_positions, token_end_positions = self.__get_token_positions_dict(tokens)

        return list(
            self._span_fixer.fix_spans(
                text=text,
                spans=spans,
                token_start_positions=token_start_positions,
                token_end_positions=token_end_positions
            )
        )

    def get_labels(self, token_positions, spans):
        # 4.0 Align and get labels
        # Get token positions as tuple
        return list(self._align_token_labels.get_labels(token_positions=token_positions, spans=spans))

    # Function to strip of the context labels and return the labels for
    # the main/current chunk
    def get_context_labels(self, token_positions, labels, current_chunk_start, current_chunk_end):

        return [
            label
            if token_position[0] >= current_chunk_start and token_position[1] <= current_chunk_end
            else self._token_ignore_label for token_position, label in zip(token_positions, labels)
        ]

    def _encode_single(self, text, spans):
        # 2.0 Tokenize the text
        tokens = self._text_tokenizer.get_tokens(text=text.replace('\n', ' '))
        token_positions = self.__get_token_positions_tuple(tokens)
        if spans is not None and spans != []:
            # 3.0 Fix Spans
            spans = self.get_fixed_spans(text=text, tokens=tokens, spans=spans)
            # 4.0 Align and get labels
            # Get token positions as tuple
            labels = self.get_labels(token_positions=token_positions, spans=spans)
        else:
            labels = ['O'] * len(tokens)

        return tokens, labels, token_positions

    def encode_train(self, batch):
        tokens_list = list()
        labels_list = list()
        for text, spans, current_chunk_start, current_chunk_end in zip(
                batch['sentence_text'],
                batch['spans'],
                batch['current_chunk_start'],
                batch['current_chunk_end']
        ):

            tokens, labels, token_positions = self._encode_single(text=text, spans=spans)
            if self._ner_augmenter is not None:
                tokens, labels = self._ner_augmenter.augment(
                    tokens=tokens, token_positions=None, labels=labels
                )
            if self._character_noise_augmenter is not None:
                tokens, labels = self._character_noise_augmenter.augment(
                    tokens=tokens, token_positions=None, labels=labels
                )
            token_texts = self.get_token_text(tokens=tokens)
            tokens_list.append(token_texts)
            labels_list.append(labels)
        return self.tokenize_function(tokens_list=tokens_list, labels_list=labels_list)

    def encode_validation(self, batch):

        tokens_list = list()
        labels_list = list()
        for text, spans, current_chunk_start, current_chunk_end in zip(
                batch['sentence_text'],
                batch['spans'],
                batch['current_chunk_start'],
                batch['current_chunk_end']
        ):

            tokens, labels, token_positions = self._encode_single(text=text, spans=spans)
            labels = self.get_context_labels(
                token_positions=token_positions,
                labels=labels,
                current_chunk_start=current_chunk_start,
                current_chunk_end=current_chunk_end
            )
            token_texts = self.get_token_text(tokens=tokens)
            tokens_list.append(token_texts)
            labels_list.append(labels)
        return self.tokenize_function(tokens_list=tokens_list, labels_list=labels_list)

    def encode_test(self, batch):
        tokens_list = list()
        labels_list = list()
        whitespaces_list = list()
        token_positions_list = list()
        for text, spans, current_chunk_start, current_chunk_end, global_start in zip(
                batch['sentence_text'],
                batch['spans'],
                batch['current_chunk_start'],
                batch['current_chunk_end'],
                batch['global_start']
        ):
            tokens, labels, token_positions = self._encode_single(
                text=text, spans=spans
            )
            labels = self.get_context_labels(
                token_positions=token_positions,
                labels=labels,
                current_chunk_start=current_chunk_start,
                current_chunk_end=current_chunk_end
            )
            token_texts = self.get_token_text(tokens=tokens)
            whitespaces_list.append(self.get_whitespaces(
                text=text, tokens=tokens, token_positions=token_positions
            ))
            token_positions_list.append(self.__get_offset_token_positions_tuple(tokens, offset=global_start))
            tokens_list.append(token_texts)
            labels_list.append(labels)
        tokenized_data = self.tokenize_function(tokens_list=tokens_list, labels_list=labels_list)
        tokenized_data['tokens'] = tokens_list
        tokenized_data['whitespaces'] = whitespaces_list
        tokenized_data['labels_list'] = labels_list
        tokenized_data['token_positions'] = token_positions_list
        return tokenized_data

    def encode_debug(self, batch):
        tokens_list = list()
        labels_list = list()
        augmented_tokens_list = list()
        augmented_labels_list = list()
        whitespaces_list = list()
        token_positions_list = list()

        for text, spans, current_chunk_start, current_chunk_end, global_start in zip(
                batch['sentence_text'],
                batch['spans'],
                batch['current_chunk_start'],
                batch['current_chunk_end'],
                batch['global_start']
        ):

            tokens, labels, token_positions = self._encode_single(text=text, spans=spans)

            token_texts = self.get_token_text(tokens=tokens)
            tokens_list.append(token_texts)

            whitespaces_list.append(self.get_whitespaces(
                text=text, tokens=tokens, token_positions=token_positions
            ))
            token_positions_list.append(self.__get_offset_token_positions_tuple(tokens, offset=global_start))

            if self._ner_augmenter is not None:
                augmented_tokens, augmented_labels = self._ner_augmenter.augment(
                    tokens=tokens, token_positions=None, labels=labels
                )
                augmented_token_texts = self.get_token_text(tokens=augmented_tokens)
                augmented_tokens_list.append(augmented_token_texts)

                # Uncomment this out when debugging "train" i.e debugging with context tokens
                augmented_labels = self.get_context_labels(
                    token_positions=token_positions,
                    labels=augmented_labels,
                    current_chunk_start=current_chunk_start,
                    current_chunk_end=current_chunk_end
                )
                augmented_labels_list.append(augmented_labels)

            # Uncomment this out when debugging "train" i.e debugging with context tokens
            labels = self.get_context_labels(
                token_positions=token_positions,
                labels=labels,
                current_chunk_start=current_chunk_start,
                current_chunk_end=current_chunk_end
            )
            labels_list.append(labels)

        tokenized_data = self.tokenize_function(tokens_list=tokens_list, labels_list=labels_list)
        tokenized_data['tokens'] = tokens_list
        tokenized_data['whitespaces'] = whitespaces_list
        tokenized_data['labels_list'] = labels_list
        tokenized_data['augmented_tokens'] = augmented_tokens_list
        tokenized_data['augmented_labels'] = augmented_labels_list
        tokenized_data['token_positions'] = token_positions_list
        return tokenized_data

    # Local function to tokenize the inputs
    def tokenize_function(self, tokens_list, labels_list):
        # Run the tokenizer on the input text
        tokenized_data = self._tokenizer(
            tokens_list,
            padding=self._padding,
            truncation=self._truncation,
            max_length=self._max_seq_length,
            # We use this argument because the texts in our dataset are lists of words (with a label for each word).
            is_split_into_words=True,
        )

        labels = []
        for i, label in enumerate(labels_list):
            word_ids = tokenized_data.word_ids(batch_index=i)
            previous_word_idx = None
            label_ids = []
            for word_idx in word_ids:
                # Special tokens have a word id that is None. We set the label to -100 so they are automatically
                # ignored in the loss function.
                if word_idx is None:
                    label_ids.append(self._ignore_label)
                # We set the label for the first token of each word.
                elif word_idx != previous_word_idx:
                    if label[word_idx] == self._token_ignore_label:
                        label_ids.append(self._ignore_label)
                    else:
                        label_ids.append(self._label_to_id[label[word_idx]])
                # For the other tokens in a word, we set the label to either the current label or -100, depending on
                # the label_all_tokens flag.
                else:
                    if label[word_idx] == self._token_ignore_label:
                        label_ids.append(self._ignore_label)
                    else:
                        if self._label_all_tokens:
                            label_ids.append(self._b_to_i_label[self._label_to_id[label[word_idx]]])
                        else:
                            label_ids.append(self._ignore_label)
                previous_word_idx = word_idx
            labels.append(label_ids)
        if labels:
            tokenized_data["labels"] = labels
        return tokenized_data

    @staticmethod
    def _get_max_seq_length(
            tokenizer: PreTrainedTokenizerFast,
            max_seq_length: Optional[int] = None
    ) -> int:
        """
        Get the max_seq_length based on the model_max_length specified by the tokenizer.
        Verify that the passed max_seq_length is valid and if not, return and valid max_seq_length
        that can be handled by the model/tokenizer.

        Args:
            tokenizer (PreTrainedTokenizerFast): The tokenizer object
            max_seq_length (Optional[int], defaults to `514`): The maximum total input sequence length after
            tokenization. Sequences longer than this will be truncated.

        Returns:
            max_seq_length (int): The maximum total input sequence length after tokenization.
            Sequences longer than this will be truncated.

        """
        if max_seq_length is None:
            max_seq_length = tokenizer.model_max_length
            if max_seq_length > 1024:
                logging.warning(
                    f"The tokenizer picked seems to have a very large `model_max_length` "
                    f"({tokenizer.model_max_length}). Picking 1024 instead. "
                    f"You can change that default value by passing --max_seq_length xxx. "
                )
                max_seq_length = 1024
        else:
            if max_seq_length > tokenizer.model_max_length:
                logging.warning(
                    f"The max_seq_length passed ({max_seq_length}) is larger than the maximum length for the"
                    f"model ({tokenizer.model_max_length}). Using max_seq_length={tokenizer.model_max_length}."
                )
            max_seq_length = min(max_seq_length, tokenizer.model_max_length)
        return max_seq_length
