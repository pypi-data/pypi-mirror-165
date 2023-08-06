import json
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from typing import Union, List, Mapping, Iterable, Dict

from transformers import AutoConfig, PreTrainedTokenizer, PreTrainedTokenizerFast

from .sequence_datasets.sequences import SequenceChunker
from .sequence_datasets.sequences.utils import get_dataset_sentence
from .sequence_datasets.text_tokenizers import HFSubwordTokenizer, SpacyTokenizer
from .sequence_datasets.text_tokenizers.utils import align_token_sub_word_counts
from .model_helpers import ModelHelpers

NOTE_TYPE = Mapping[str, Union[str, List[Mapping[str, Union[str, int]]]]]


class SequenceDataset(object):
    """
    Create a SequenceDataset object to create sequences from long pieces of text (e.g medical notes).
    This class handles the creation of chunks from documents based on the values provided. You would
    use this when you have text that may exceed the 512 sub-word limit of a transformer model. You
    would then use this object to chunk long text sequences to multiple 512 sequences. Each chunk
    is based on a variable striding window, where the window is the current sentence (based on a
    sentencizer). Sequences longer than max_tokens are chunked. Note that we use 500 for
    max_prev_sentence_tokens and max_next_sentence_tokens, so that we have enough context for small
    chunks.
    """

    def __init__(
            self,
            text_tokenizer: SpacyTokenizer,
            hf_tokenizer: Union[PreTrainedTokenizer, PreTrainedTokenizerFast],
            max_tokens: int = 500,
            max_prev_sentence_tokens: int = 500,
            max_next_sentence_tokens: int = 500,
            default_chunk_size: int = 0
    ):
        """
        Initialize the variables.

        Args:
            text_tokenizer (SpacyTokenizer): The SpacyTokenizer object for word tokenization of text.
            hf_tokenizer (Union[PreTrainedTokenizer, PreTrainedTokenizerFast]): The subword tokenizer from HuggingFace
            max_tokens (int, defaults to `500`): The maximum number of tokens in a given chunk
            max_prev_sentence_tokens (int, defaults to `500`): The max chunk size for the previous chunks for a
            given sentence (training/prediction example) in the note can have
            max_next_sentence_tokens (int, defaults to `500`): The max chunk size for the next chunks for a
            given sentence (training/prediction example) in the note can have
            default_chunk_size (int, defaults to `0`): The chunk will always include a chunk of this length
            as part of the previous and next chunks
        """

        # Load the sequence chunker object
        # This class contains the logic for chunking sequences
        self._sequence_chunker = SequenceChunker(
            max_tokens=max_tokens,
            max_prev_sentence_tokens=max_prev_sentence_tokens,
            max_next_sentence_tokens=max_next_sentence_tokens,
            default_chunk_size=default_chunk_size
        )

        # Wrap the spacy and subword tokenizers. These classes have some helper functions.
        self._tokenizer = text_tokenizer
        self._subword_tokenizer = HFSubwordTokenizer(tokenizer=hf_tokenizer)

    def get_sequences(
            self,
            notes: Union[NOTE_TYPE, List[NOTE_TYPE]],
            text_key: str = 'text',
            spans_key: str = 'spans',
            note_id_key: str = 'note_id'
    ) -> Iterable[Dict[str, Union[str, int, List[Dict[str, Union[str, int, bool]]]]]]:
        """
        Given a note - chunk the note into sequences of at most max_tokens. For each chunked
        sequence, get it's local start and end positions, start and end positions with
        respect to the note and the spans that fall within the chunked sequence.

        Args:
            notes (Union[NOTE_TYPE, List[NOTE_TYPE]]): A list of note objects, that contains the note_text, note_id and
            a list of NER spans.
            text_key (str, defaults to `text`): The key value of the note object that contains the note text.
            spans_key (str, defaults to `spans`): The key value of the note object that contains the note text.
            note_id_key (str, defaults to `note_id`): The key value of hte note object that contains the note text.

        Returns:
            (Iterable[Dict[str, Union[str, int, List[Dict[str, Union[str, int, bool]]]]]]): An iterable that iterates
            through the list of chunks generated from the note or list of notes passed to the function.
        """

        # If a string is passed convert it to a list of one element
        if type(notes) != list:
            notes = [notes]

        # Iterate through the list of texts
        for note in notes:

            # Get the tokens in each sentence (as a nested list)
            sentence_tokens = self._tokenizer.get_sentence_tokens(text=note[text_key])

            # Extract thee token texts from the SpaCy token objects
            sentence_tokenized_texts = [
                [token.text for token in sentence_token]
                for sentence_token in sentence_tokens
            ]

            # Get the sub-words from the list of tokens
            sentence_subwords = self._subword_tokenizer.get_sub_words_from_tokens(
                tokenized_texts=sentence_tokenized_texts
            )

            # Create a tuple that where one element contains the word level token and the other
            # contains the number of subwords in that token
            sentence_tokens_subwords = [
                (
                    align_token_sub_word_counts(
                        sentence_token_object=sentence_token,
                        word_ids=sentence_subwords.word_ids(index)
                    )
                )
                for index, sentence_token in enumerate(sentence_tokens)
            ]

            # Get the sequence chunks for the given note. Each chunk will be at most max_tokens.
            sentence_chunks = self._sequence_chunker.get_sentence_chunks(sentence_tokens=sentence_tokens_subwords)

            # Iterate through the sentence chunks and split the note level spans to the
            # chunk level. All note level stuff should map to the chunk level correctly
            for _, sentence_chunk in sentence_chunks:
                # Get the chunk with global and local start and end positions, with the spans that fall
                # within the chunk and any other relative information
                chunk_object = get_dataset_sentence(
                    note_text=note[text_key], note_spans=note[spans_key], sentence_chunk=sentence_chunk
                )

                # Assign the note_id to the chunk
                chunk_object[note_id_key] = note[note_id_key]

                # Delete this object since it can't be JSON serialized, since it contains the
                # SpaCy token objects
                del chunk_object['sentence_chunk']

                # Return the chunk object
                yield chunk_object


def main():
    cli_parser = ArgumentParser(
        description='Configuration arguments provided at run time from the CLI',
        formatter_class=ArgumentDefaultsHelpFormatter
    )
    cli_parser.add_argument(
        '--input_file',
        type=str,
        required=True,
        help='The jsonl file that contains the notes'
    )
    cli_parser.add_argument(
        '--max_tokens',
        type=int,
        default=500,
        help='The max tokens that a given sentence/chunk (training/prediction example) in the note can have'
    )
    cli_parser.add_argument(
        '--default_chunk_size',
        type=int,
        default=0,
        help='The default chunk size for the previous and next chunks for a given sentence (training/prediction '
             'example) in the note can have '
    )
    cli_parser.add_argument(
        '--max_prev_sentence_tokens',
        type=int,
        default=500,
        help='The max chunk size for the previous chunks for a given sentence (training/prediction example) in the '
             'note can have '
    )
    cli_parser.add_argument(
        '--max_next_sentence_tokens',
        type=int,
        default=500,
        help='The max chunk size for the next chunks for a given sentence (training/prediction example) in the note '
             'can have '
    )
    cli_parser.add_argument(
        '--spacy_model',
        type=str,
        required=True,
        help='The spacy nlp object that is used to tokenize the text and split documents into sentences'
    )
    cli_parser.add_argument(
        '--hf_tokenizer_name',
        type=str,
        required=True,
        help='The sub-word tokenizer to use for splitting tokens into sub-words'
    )
    cli_parser.add_argument(
        '--text_key',
        type=str,
        default='text',
        help='The key where the note text is present in the json object'
    )
    cli_parser.add_argument(
        '--note_id_key',
        type=str,
        default='note_id',
        help='The key where the note metadata is present in the json object'
    )
    cli_parser.add_argument(
        '--spans_key',
        type=str,
        default='spans',
        help='The key where the note annotates spans are present in the json object'
    )
    cli_parser.add_argument(
        '--output_file',
        type=str,
        help='The file where the sentence/chunk dataset will be stored'
    )
    args = cli_parser.parse_args()

    # Load a helper class to load HuggingFace configs, tokenizers and models
    model_helpers = ModelHelpers()

    # Load the config, to determine model type so that we can check whether to add prefix
    # space to the tokenizer
    config = AutoConfig.from_pretrained(args.hf_tokenizer_name)

    # Load the HuggingFace tokenizer
    hf_tokenizer = model_helpers.get_tokenizer(
        tokenizer_name=args.hf_tokenizer_name,
        model_type=config.model_type,
        cache_dir=None,
        model_revision='main',
        use_auth_token=False
    )

    # Load the SpaCy tokenizer object
    text_tokenizer = model_helpers.get_text_tokenizer(spacy_model=args.spacy_model)

    # Load the sequence dataset object
    sequence_dataset = SequenceDataset(
        text_tokenizer=text_tokenizer,
        hf_tokenizer=hf_tokenizer,
        max_tokens=args.max_tokens,
        max_prev_sentence_tokens=args.max_prev_sentence_tokens,
        max_next_sentence_tokens=args.max_next_sentence_tokens,
        default_chunk_size=args.default_chunk_size
    )

    # Get the chunks from all the notes and write the chunks to a file
    with open(args.output_file, 'w') as file:
        for line in open(args.input_file, 'r'):
            note = json.loads(line)
            for chunk_object in sequence_dataset.get_sequences(
                    note, text_key=args.text_key, spans_key=args.spans_key, note_id_key=args.note_id_key
            ):
                file.write(json.dumps(chunk_object) + '\n')


if __name__ == '__main__':
    main()
