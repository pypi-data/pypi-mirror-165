from typing import Optional, Sequence, Mapping, Union, Tuple, Iterable

from .align import Align
from .mismatch_error import MismatchError


class AlignTokenLabels(object):
    """
    This class is used to align tokens with the spans
    Each token is assigned one of the following labels
    'B-LABEL', 'I-LABEL', 'O'. For example the text
    360 Longwood Avenue is 2 tokens - [360, Longwood, Avenue]
    and each token would be assigned the following labels
    [B-LOC, I-LOC, I-LOC] (this would also depend on what
    notation we are using). Generally the data after prodigy
    annotation has all the tokens and all the spans.
    We would have tokens:[tok1, tok2, ... tokn]
    and spans:[span1:[tok1, tok2, tok3], span2:[tok7], ... span k]
    This would be used to convert into the format we are using
    which is assign the label to each token based on which span it
    belongs to.
    """

    def __init__(
            self,
            notation: str
    ):
        """
        Initialize variables that will be used to align tokens
        and span labels. Notation is whether we would like to use BIO, IO, BILOU,
        when assigning the label to each token based on which span it belongs to.
        Keep track of the total number of spans etc.

        Args:
            notation (str): NER label notation
        """

        # Keeps track of all the spans (list) in the text (note)
        # Depending on the notation passed, we will return the label for
        # the token accordingly
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
    def __check_begin(token_end: int, span_end) -> Align:
        """
        Given a token, return the position of the token in the span.
        Check if it begins a span or is a single token span.

        Args:
            token_end (int): The end position of the token

        Returns:
            (Align): The position/alignment of the token in the span
        """

        # Set the inside flag to true to indicate that the next token that is checked
        # will be checked to see if it belongs 'inside' the span
        if token_end > span_end:
            raise MismatchError('Span and Token mismatch - Begin Token extends longer than the span')
        # If this token does not cover the entire span then we expect another token
        # to be in the span and that token should be assigned the I-LABEL
        elif token_end < span_end:
            return Align.BEGIN
        # If this token does cover the entire span then we set inside = False
        # to indicate this span is complete and increment the current span
        # to move onto the next span in the text
        elif token_end == span_end:
            return Align.SINGLE

    @staticmethod
    def __check_inside(token_start: int, token_end: int, span_end) -> Align:
        """
        Given a token, return the position of the token in the span.
        Check if it is inside a span or is the ending token of the span.

        Args:
            token_end (int): The end position of the token

        Returns:
            (Align): The position/alignment of the token in the span
        """

        if token_start >= span_end or token_end > span_end:
            raise MismatchError('Span and Token mismatch - Inside Token starts after the span ends. Token positions: '
                                f'{token_start}, {token_end}')
        # If this token does not cover the entire span then we expect another token
        # to be in the span and that token should be assigned the I-LABEL
        elif token_end < span_end:
            return Align.INSIDE
        # If this token does cover the entire span then we set inside = False
        # to indicate this span is complete and increment the current span
        # to move onto the next span in the text
        elif token_end == span_end:
            return Align.END

    def get_alignment(self, token_start: int, token_end: int, span_start: int, span_end: int) -> Align:
        """
        Given a token, return the position/alignment of the token in the span.

        Args:
            token_start (int): The start position of the token
            token_end (int): The end position of the token
            span_start (int): The start position of the span
            span_end (int): The end position of the span

        Returns:
            (Align): The position/alignment of the token in the span
        """

        # Check if the span can be assigned the B-LABEL
        if token_start == span_start:
            return self.__check_begin(
                token_end=token_end,
                span_end=span_end,
            )

        # Check if the span can be assigned the I-LABEL
        elif token_start > span_start and span_start < token_end <= span_end:
            return self.__check_inside(
                token_start=token_start,
                token_end=token_end,
                span_end=span_end,
            )

        # Check if the token is outside a span
        elif token_end <= span_start:
            return Align.OUTSIDE
        else:
            raise MismatchError(
                'Span and Token mismatch - the span and tokens don\'t line up. There might be a tokenization issue '
                f'that needs to be fixed. Token positions: {token_start}, {token_end}'
            )

    def get_label(self, span_label: Optional[str], alignment: Align):
        """
        Get the label for the token in the span based on it's position/alignment.

        Args:
            span_label (Optional[str]): The label of the span.
            alignment (Align): The position/alignment of the token in the span.

        Returns:
            (str): The label for the token in the span.
        """

        if alignment == Align.SINGLE:
            return self._prefix_single + span_label
        elif alignment == Align.BEGIN:
            return self._prefix_begin + span_label
        elif alignment == Align.INSIDE:
            return self._prefix_inside + span_label
        elif alignment == Align.END:
            return self._prefix_end + span_label
        elif alignment == Align.OUTSIDE:
            return self._prefix_outside
        else:
            raise ValueError('Invalid alignment')

    def get_labels(
            self,
            token_positions: Sequence[Tuple[int, int]],
            spans: Sequence[Mapping[str, Union[str, int]]]
    ) -> Iterable[str]:
        """
        Get the labels for every token based on the list of spans.

        Args:
            token_positions (Sequence[Tuple[int, int]]): The start and end positions of all the tokens
            spans (Sequence[Mapping[str, Union[str, int]]]): The spans present in the note/document.

        Returns:
            label (Iterable[str]): An iterable that returns a label for each token.
        """

        # Convert the list of spans into an iterator
        span_iterator = iter(spans)
        # Get the current span
        current_span = next(span_iterator, None)
        # Iterate through the token positions
        for token_start, token_end in token_positions:
            # Current span will be None when we have exhausted all the spans
            # So all tokens post this will get the outside (O) label
            if current_span is None:
                alignment = Align.OUTSIDE
                label = self.get_label(span_label=None, alignment=alignment)
            # Get the position/alignment of the token with respect to the span
            else:
                alignment = self.get_alignment(
                    token_start=token_start,
                    token_end=token_end,
                    span_start=current_span['start'],
                    span_end=current_span['end']
                )
                # Get the label based on the alignment
                label = self.get_label(span_label=current_span['label'], alignment=alignment)
            # Move to the next span when we have covered all the tokens in the current span
            if alignment == Align.SINGLE or alignment == Align.END:
                current_span = next(span_iterator, None)
            yield label
