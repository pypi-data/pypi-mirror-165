from collections import deque
from typing import Deque, List, Sequence, Iterable, Optional, NoReturn, Dict, Tuple, Any


class SequenceChunker(object):
    """
    When we mention previous sentence and next sentence, we don't mean exactly one sentence
    but rather a previous chunk and a next chunk. This can include one or more sentences and
    it does not mean that the sentence has to be complete (it can be cutoff in between) - hence a chunk
    This class is used to build a dataset at the sentence level. It takes as input all the tokenized
    sentences in the note. So the input is a list of lists where the outer list represents the sentences
    in the note and the inner list is a list of tokens in the sentence. It then returns a dataset where
    each element in the list contains the tokens that form the previous chunk, the current chunk
    and the next chunk. This is done so that when we build a model we can use the previous and next chunks
    to add context to the sentence/model. We could have different sizes of previous and next chunks
    depending on the position of the sentence etc. Essentially we build a sentence level dataset
    where we can also provide context to the sentence by including the previous and next chunks
    """

    def __init__(
            self,
            max_tokens: int,
            max_prev_sentence_tokens: int,
            max_next_sentence_tokens: int,
            default_chunk_size: int,
    ) -> NoReturn:
        """
        Set the maximum token length a given training example (sentence level) can have.
        That is the total length of the current sentence + previous chunk + next chunk
        We also set the the maximum length of the previous and next chunks. That is how many
        tokens can be in these chunks. However if the total length exceeds, tokens in the
        previous and next chunks will be dropped to ensure that the total length is < max_tokens
        The default chunk size ensures that the length of the chunks will be a minimum number of
        tokens based on the value passed. For example is default_chunk_size=10, the length
        of the previous chunks and next chunks will be at least 10 tokens.

        Args:
            max_tokens (int): The maximum token length a given training example (sentence level) can have.
            max_prev_sentence_tokens (int): The max chunk size for the previous chunks for a given sentence
            (training/prediction example) in the note can have.
            max_next_sentence_tokens (int): The max chunk size for the next chunks for a given sentence
            (training/prediction example) in the note can have.
            default_chunk_size (int): the training example will always include a chunk of this length
            as part of the previous and next chunks.
        """

        self._id_num = None
        self._max_tokens = max_tokens
        self._max_prev_sentence_tokens = max_prev_sentence_tokens
        self._max_next_sentence_tokens = max_next_sentence_tokens
        self._default_chunk_size = default_chunk_size

    @staticmethod
    def _get_chunks(
            seq: List[Tuple[Any, int]],
            size: int
    ) -> Iterable[List[Tuple[Any, int]]]:
        """
        Return chunks of the sequence. The size of each chunk will be based
        on the value passed to the size argument.

        Args:
            seq (List[Tuple[Any, int]]): The sequence to be chunked.
            size (int): The max chunk size for the chunks.

        Returns:
            (Iterable[List[Tuple[Any, int]]]): Iterable that iterates through fixed size chunks of
            the input sequence chunked version of the sequence.
        """

        count = 0
        chunked_seq = list()
        for token in seq:
            # Append when the size of the chunk is less than maximum size
            if count + token[1] <= size:
                count += token[1]
                chunked_seq.append(token)
            # Return the chunk when it has reached the maximum size
            else:
                yield chunked_seq
                chunked_seq = list()
                count = token[1]
                chunked_seq.append(token)
        # Return the final chunk
        if len(chunked_seq) != 0:
            yield chunked_seq

    @staticmethod
    def _get_sentence_length(sentence: Sequence[Tuple[Any, int]]) -> int:
        """
        Get the number of subwords in the sentence.

        Args:
            sentence (Sequence[Tuple[Any, int]]): A list of tuples that contains token object, and how many
            subwords the token contains.

        Returns:
            (int): The total number of subwords in the sequence
        """

        count = 0
        for token in sentence:
            # The token is a tuple where the second element contains the number of
            # subwords for that token
            count += token[1]
        return count

    def get_previous_sentences(
            self,
            sent_tokens: Sequence[Sequence[Tuple[Any, int]]]
    ) -> List[Deque]:
        """
        Go through all the sentences in the medical note and create a list of
        previous sentences. The output of this function will be a list of chunks
        where each index of the list contains the sentences (chunks) - (tokens) present before
        the sentence at that index in the medical note. For example prev_sent[0] will
        be empty since there is no sentence before the first sentence in the note
        prev_sent[1] will be equal to sent[0], that is the previous sentence of the
        second sentence will be the first sentence. We make use of deque, where we
        start to deque elements when it start to exceed max_prev_sentence_token. This
        list of previous sentences will be used to define the previous chunks

        Args:
            sent_tokens (Sequence[Sequence[Tuple[Any, int]]]): Sentences in the note and each element of the list
            contains a list of tokens in that sentence.

        Returns:
            previous_sentences (List[deque]): A list of deque objects where each index contains a list (queue) of
            previous tokens (chunk) with respect to the sentence represented by that index in the note.
        """

        previous_sentences = list()

        # Create a queue and specify the capacity of the queue
        # Tokens will be popped from the queue when the capacity is exceeded
        prev_sentence = deque(maxlen=self._max_prev_sentence_tokens)

        # The first previous chunk is empty since the first sentence in the note does not have
        # anything before it
        previous_sentences.append(prev_sentence.copy())

        # As we iterate through the list of sentences in the not, we add the tokens from the previous chunks
        # to the the queue. Since we have a queue, as soon as the capacity is exceeded we pop tokens from
        # the queue
        for sent_token in sent_tokens[:-1]:
            for token in sent_token:
                prev_sentence.append(token)
            # As soon as each sentence in the list is processed
            # We add a copy of the current queue to a list - this list keeps track of the
            # previous chunks for a sentence
            previous_sentences.append(prev_sentence.copy())

        return previous_sentences

    def get_next_sentences(
            self,
            sent_tokens: Sequence[Sequence[Tuple[Any, int]]]
    ) -> List[Deque]:
        """
        Go through all the sentences in the medical note and create a list of
        next sentences. The output of this function will be a list of lists
        where each index of the list contains the list of sentences present after
        the sentence at that index in the medical note. For example next_sent[-] will
        be empty since there is no sentence after the last sentence in the note
        next_sent[0] will be equal to sent[1:], that is the next sentence of the
        first sentence will be the subsequent sentences. We make use of deque, where we
        start to deque elements when it start to exceed max_next_sentence_token. This
        list of previous sentences will be used to define the previous chunks

        Args:
            sent_tokens (Sequence[Sequence[Tuple[Any, int]]]): Sentences in the note and each element of the list
            contains a list of tokens in that sentence

        Returns:
            next_sentences (List[deque]): A list of deque objects where each index contains a list (queue) of
            next tokens (chunk) with respect to the sentence represented by that index in the note
        """

        # A list of next sentences is first created and reversed
        next_sentences = list()

        # Create a queue and specify the capacity of the queue
        # Tokens will be popped from the queue when the capacity is exceeded
        next_sentence = deque(maxlen=self._max_next_sentence_tokens)

        # The first (which becomes the last chunk when we reverse this list) next chunk is empty since
        # the last sentence in the note does not have
        # anything after it
        next_sentences.append(next_sentence.copy())
        for sent_token in reversed(sent_tokens[1:]):
            for token in reversed(sent_token):
                next_sentence.appendleft(token)
            next_sentences.append(next_sentence.copy())

        # The list is reversed - since we went through the sentences in the reverse order in
        # the earlier steps
        return [next_sent for next_sent in reversed(next_sentences)]

    def get_sentence_chunks(
            self,
            sentence_tokens: List[List[Tuple[Any, int]]],
            start_chunk: Optional[List[Tuple[Any, int]]] = None,
            end_chunk: Optional[List[Tuple[Any, int]]] = None,
            sub: bool = False
    ) -> Iterable[Tuple[str, Dict[str, List[Tuple[Any, int]]]]]:
        """
        When we mention previous sentence and next sentence, we don't mean exactly one sentence
        but rather a previous chunk and a next chunk. This can include one or more sentences and
        it does not mean that the sentence has to be complete (it can be cutoff in between) - hence a chunk
        We iterate through all the tokenized sentences in the note. So the input is
        a list of lists where the outer list represents the sentences in the note and the inner list
        is a list of tokens in the sentence. It then returns a dataset where each sentence is
        concatenated with the previous and the next sentence. This is done so that when we build a model
        we can use the previous and next sentence to add context to the model. The weights and loss etc
        will be computed and updated based on the current sentence. The previous and next sentence will
        only be used to add context. We could have different sizes of previous and next chunks
        depending on the position of the sentence etc. Since we split a note in several sentences which are
        then used as training data.
        ignore_label is used to differentiate between the current sentence and the previous and next
        chunks. The chunks will have the label NA so that and the current sentence
        will have the label (DATE, AGE etc) so that they can be distinguished.
        If however we are building a dataset for predictions
        the current sentence will have the default label O, but the next and previous chunks will still
        have the label NA. However if the total length exceeds, tokens in the
        previous and next chunks will be dropped to ensure that the total length is < max_tokens
        The default chunk size ensures that the length of the chunks will be a minimum number of
        tokens based on the value passed. For example is default_chunk_size=10, the length
        of the previous chunks and next chunks will be at least 10 tokens. If the total length > max tokens
        even after decreasing the sizes of the previous and next chunks, then we split this long
        sentence into sub sentences and repeat the process described above.

        Args:
            sentence_tokens (List[List[Tuple[Any, int]]]): Sentences in the note and each sentence contain
            the tokens (dict) in that sentence the token dict object contains the token text, start, end etc.
            start_chunk (Optional[List[Tuple[Any, int]]]): Prefix the first sentence of with some
            pre-defined chunk
            end_chunk (Optional[List[Tuple[Any, int]]]): Suffix the last sentence of with some
            pre-defined chunk
            sub (bool): Whether the function is called to process sub-sentences (used when we are splitting
            long sentences into smaller sub sentences to keep sentence length < max_tokens

        Returns:
            (Iterable[Tuple[str, Dict[str, List[Tuple[Any, int]]]]]): Iterate through the returned sentences, where
            each sentence has the previous chunks and next chunks attached to it.
        """

        # Id num keeps track of the id of the sentence - that is the position the sentence occurs in
        # the note. We keep the id of sub sentences the same as the sentence, so that the user
        # knows that these sub sentences are chunked from a longer sentence.
        # <SENT 0> <SENT 1>. Say length of sent 0 with the previous and next chunks is less than max_tokens
        # we return sent 0 with id 0. For sent 1, say the length is longer, we split it into sub
        # sentences - <SUB 1><SUB 2> - we return SUB 1, and SUB 2 with id 1 - so we know that it belongs
        # to <SENT 1> in the note.
        if not sub:
            self._id_num = -1

        # Initialize the object that will take all the sentences in the note and return
        # a dataset where each row represents a sentence in the note. The sentence in each
        # row will also contain a previous chunk and next chunk (tokens) that will act as context
        # when training the mode
        # [ps1, ps 2, ps 3...ps-i], [cs1, cs2, ... cs-j], [ns, ns, ... ns-k] - as you can see the current sentence
        # which is the sentence we train on (or predict on) will be in the middle - the surrounding tokens will
        # provide context to the current sentence
        # Get the previous sentences (chunks) for each sentence in the note
        previous_chunks_tokens = self.get_previous_sentences(sentence_tokens)
        # Get the next sentences (chunks) for each sentence in the note
        next_chunks_tokens = self.get_next_sentences(sentence_tokens)

        # For the note we are going to iterate through all the sentences in the note and
        # concatenate each sentence with the previous and next chunks. (This forms the data that
        # will be used for training/predictions) Each sentence with the concatenated chunks will be
        # a training sample. We would do the same thing for getting predictions on a sentence as well
        # The only difference would be the labels that are used. We would use the default label O for
        # prediction and the annotated labels for prediction
        if len(sentence_tokens) != len(previous_chunks_tokens) or len(sentence_tokens) != len(next_chunks_tokens):
            raise ValueError('Sentence length mismatch')
        for index, (previous_chunk_tokens, current_sentence_tokens, next_chunk_tokens) in enumerate(
                zip(previous_chunks_tokens, sentence_tokens, next_chunks_tokens)
        ):
            # We check if the number of tokens in teh current sentence + previous chunk
            # + next chunk exceeds max tokens. If it does we start popping tokens from the previous and next chunks
            # until the number of tokens is equal to max tokens
            previous_chunk_length = self._get_sentence_length(previous_chunk_tokens)
            current_sentence_length = self._get_sentence_length(current_sentence_tokens)
            next_sentence_length = self._get_sentence_length(next_chunk_tokens)
            total_length = previous_chunk_length + current_sentence_length + next_sentence_length

            # If the length of the current sentence plus the length of the previous and next
            # chunks exceeds the max_tokens, start popping tokens from the previous and next
            # chunks until either total length < max_tokens or the number of tokens in the previous and
            # next chunks goes below the default chunk size
            while (
                    total_length > self._max_tokens and
                    (next_sentence_length > self._default_chunk_size or
                     previous_chunk_length > self._default_chunk_size)
            ):
                if next_sentence_length >= previous_chunk_length:
                    _, length = next_chunk_tokens.pop()
                    next_sentence_length -= length
                    total_length -= length
                elif previous_chunk_length > next_sentence_length:
                    _, length = previous_chunk_tokens.popleft()
                    previous_chunk_length -= length
                    total_length -= length

            # If this is not a sub sentence, increment the ID to
            # indicate the processing of the next sentence of the note
            # If it is a sub sentence, keep the ID the same, to indicate
            # it belongs to a larger sentence
            if not sub:
                self._id_num += 1

            # If total length < max_tokens - process the sentence with the current sentence
            # and add on the previous and next chunks and return
            if total_length <= self._max_tokens:
                # Check if we want to add a pre-defined chunk for the first sentence in the note
                if index == 0 and start_chunk is not None:
                    previous_chunk = start_chunk + list(previous_chunk_tokens)
                else:
                    previous_chunk = list(previous_chunk_tokens)
                # Check if we want to add a pre-defined chunk for the last sentence in the note
                if index == len(sentence_tokens) - 1 and end_chunk is not None:
                    next_chunk = list(next_chunk_tokens) + end_chunk
                else:
                    next_chunk = list(next_chunk_tokens)
                # Return processed sentences
                yield (
                    self._id_num,
                    {
                        'previous_chunk': previous_chunk,
                        'current_chunk': current_sentence_tokens,
                        'next_chunk': next_chunk
                    }
                )

            # Process the sub sentences - we take a long sentence
            # and split it into smaller chunks - and we recursively call the function on this list
            # of smaller chunks - as mentioned before the smaller chunks (sub sentences) will have the
            # same ID as the original sentence
            else:
                # Store the smaller chunks - say <SENT1> is too long
                # <PREV CHUNK><SENT1><NEXT CHUNK>
                # We get chunk sent 1 - to <SUB1><SUB2><SUB3> and we pass this [<SUB1><SUB2><SUB3>] to the function
                # as a recursive call. This list is now processed as a smaller note that essentially belongs
                # to a sentence. But as you can see we did not pass <PREV CHUNK> & <NEXT CHUNK>, because
                # these are chunks that are not part of the current sentence, but they still need to be
                # included in the final output - and the work around is mentioned below
                # So that we have a previous chunk for <SUB1> and next chunk for <SUB3>
                # we include the previous_sent_tokens and next_sent_tokens as the start chunk
                # and the next chunk in the function call below
                # <PREV CHUNK><SUB1><NEXT SUB1>, id = x
                # <PREV SUB2><SUB2><NEXT SUB2>, id = x
                # <PREV SUB3><SUB3><NEXT CHUNK>, id = x
                sub_sentences = list()
                # Prefix the first sentence in these smaller chunks
                previous_chunk = list(previous_chunk_tokens)
                # Suffix the last sentence in these smaller chunks
                next_chunk = list(next_chunk_tokens)
                # Get chunks
                for chunk in self._get_chunks(
                        current_sentence_tokens, self._max_tokens - (2 * self._default_chunk_size)
                ):
                    sub_sentences.append(chunk)

                # Process list of smaller chunks
                for sub_sent in self.get_sentence_chunks(
                        sub_sentences,
                        start_chunk=previous_chunk,
                        end_chunk=next_chunk,
                        sub=True
                ):
                    yield sub_sent
