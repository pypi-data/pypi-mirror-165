from spacy import tokens
from typing import Dict, List, Tuple, Mapping, Sequence, Union


def get_chunk_positions(sentence_chunk: Dict[str, List[Tuple[tokens.Token, int]]]) -> Tuple[int, int, int, int]:
    """
    Return the global start and end of the chunk. Global means with respect to the
    original note. Also return the start and end positions of the sentence of interest
    within the chunk.

    Args:
        sentence_chunk (Dict[str, List[Tuple[tokens.Token, int]]]): Chunk dictionary that contains the previous chunk,
        current chunk and next chunk objects that contain spacy token objects within them.

    Returns:
        start (int): Global start of the chunk
        end (int): Global end of the chunk
        current_chunk_start (int): Global start of the current chunk
        current_chunk_end (int): Global end of the current chunk
    """

    previous_sentence = sentence_chunk['previous_chunk']
    current_sentence = sentence_chunk['current_chunk']
    next_sentence = sentence_chunk['next_chunk']

    start = current_sentence[0][0].idx if previous_sentence == [] else previous_sentence[0][0].idx
    end = (
            current_sentence[-1][0].idx + len(current_sentence[-1][0])
    ) if next_sentence == [] else (next_sentence[-1][0].idx + len(next_sentence[-1][0]))
    current_chunk_start, current_chunk_end = (
        current_sentence[0][0].idx, current_sentence[-1][0].idx + len(current_sentence[-1][0])
    )
    return start, end, current_chunk_start, current_chunk_end


def get_sentence_spans(
        spans: Sequence[Mapping[str, Union[str, int]]],
        sentence_start: int,
        sentence_end: int
) -> Sequence[Mapping[str, Union[str, int, bool]]]:
    """
    Get the spans the belong or fall within the start and end positions passed

    Args:
        spans (Sequence[Mapping[str, Union[str, int]]]): The annotated NER spans
        sentence_start (int): The start position
        sentence_end (int): The end position

    Returns:
        sentence_spans (Sequence[Mapping[str, Union[str, int]]]): The spans that fall in between the sentence_start
        and sentence_end positions
    """

    sentence_spans = list()
    # Return an empty list if there are no spans
    if len(spans) == 0:
        return sentence_spans
    for index, span in enumerate(spans):
        span_start = span['start']
        span_end = span['end']
        # Break when we have crossed the end position - since spans won't fall within
        if sentence_end < span_start:
            break
        elif sentence_start <= span_start <= sentence_end:
            if span_end > sentence_end:
                overlap = True
                origin = True
            elif span_end <= sentence_end:
                overlap = False
                origin = True
            else:
                raise ValueError('This statement should not be reached - error in code')
        elif span_start < sentence_start <= span_end <= sentence_end:
            overlap = True
            origin = False
        # Ignore span tha appears before the sentence start
        elif sentence_start > span_end:
            continue
        else:
            raise ValueError('This statement should not be reached - error in code')
        # Get the global and local positions of the span
        # Global - with respect to the entire document
        # Local - with respect to the chunk - the sentence_start and sentence_end positions
        span_dict = {
            'global_start': span_start,
            'global_end': span_end,
            'start': max(0, span_start - sentence_start),
            'end': min(sentence_end - sentence_start, span_end - sentence_start),
            'label': span['label'],
            'text': span['text'],
            'origin': origin,
            'overlap': overlap
        }
        sentence_spans.append(span_dict)
    # Return the spans
    return sentence_spans


def get_dataset_sentence(
        note_text: str,
        sentence_chunk: Dict[str, List[Tuple[tokens.Token, int]]],
        note_spans: Sequence[Mapping[str, Union[str, int]]]
) -> Dict[str, Union[str, int, List[tokens.Token], List[Dict[str, Union[str, int, bool]]]]]:
    """

    Args:
        note_text (str): The text present in the document
        sentence_chunk (Dict[str, List[Tuple[tokens.Token, int]]]): The chunk object (subset of document)
        note_spans (Sequence[Mapping[str, Union[str, int]]]): The spans present in the document

    Returns:
        (Dict[str, Union[str, int, List[tokens.Token], List[Dict[str, Union[str, int, bool]]]]]): Additional information
        about the chunk, such as global start and end positions, local start and end positions of the chunk, spans that
        fall within the chunk etc.
    """

    # Get the global start and end of the chunk and the global start and end of the current chunk
    # Global means with respect to the entire document the chunk is a part of
    global_start, global_end, global_current_chunk_start, global_current_chunk_end = get_chunk_positions(
        sentence_chunk=sentence_chunk
    )

    # Get the text of this chunk
    sentence_text = note_text[global_start:global_end]

    # Get the local current chunk start and end positions
    current_chunk_start = max(0, global_current_chunk_start - global_start)
    current_chunk_end = global_current_chunk_end - global_start

    # Get the spans that belong to this chunk
    if note_spans is None:
        sentence_spans = None
    else:
        sentence_spans = get_sentence_spans(
            spans=note_spans,
            sentence_start=global_start,
            sentence_end=global_end
        )

    # Return all the information associated with the chunk (positions, spans etc)
    return {
        'sentence_text': sentence_text,
        'sentence_chunk': sentence_chunk,
        'spans': sentence_spans,
        'global_start': global_start,
        'global_end': global_end,
        'global_current_chunk_start': global_current_chunk_start,
        'global_current_chunk_end': global_current_chunk_end,
        'start': global_start - global_start,
        'end': global_end - global_start,
        'current_chunk_start': current_chunk_start,
        'current_chunk_end': current_chunk_end
    }
