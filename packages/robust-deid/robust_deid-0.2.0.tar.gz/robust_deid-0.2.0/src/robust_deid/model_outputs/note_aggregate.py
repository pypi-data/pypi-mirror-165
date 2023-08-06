from collections import defaultdict
from typing import Sequence, Iterable, Tuple, Any


class NoteAggregate(object):
    """
    The input while training the model is at a sequence (sentence) level.
    What happens is we have a bunch of notes (say 20) which we split into
    sentences and tokenize, so we end up with tokenized sentences (say 400).
    Each sentence is then used as a training example. Now this list of sentences
    is shuffled and the model is trained. For evaluation and prediction however
    we want to know which sentence belong to which note since we want go back from
    the sentence to the note level. This class basically aggregates sentence level
    information back to the note level. So that we  can do evaluation at the note
    level and get aggregate predictions for the entire note.
    """

    # Aggregate everything to note_level
    @staticmethod
    def aggregate(
            note_ids: Sequence[str],
            start_positions: Sequence[int],
            *args
    ) -> Iterable[Tuple[str, Sequence[Sequence[Any]]]]:
        """
        Aggregate sequence/sentence level information back to note/document level
        To aggregate we pass the note_id of the sequence and the start position
        of the sequence with respect to the note/document. Everything we want to
        aggregate can be passed via "args".

        Args:
            note_ids (Sequence[str]): The sequence of note_ids in the dataset, where the note_id corresponds to the
            sequence.
            start_positions (Sequence[int]): The sequence of start positions in the dataset, where the start position
            corresponds to the start position of the sequence with respect to the note/document.
            *args: All the information we want to aggregate from sequence/sentence level back to note/document level.

        Returns:
            (Iterable[Tuple[str, Sequence[Sequence[Any]]]]): An iterable that returns a tuple which contains the note_id
            and the aggregated output.
        """

        # For each unique note_id get all the sequence start positions and sequence data (passed via args)
        note_aggregate = defaultdict(list)
        for note_id, chunk_start, *args in zip(note_ids, start_positions, *args):
            note_aggregate[note_id].append([chunk_start, *args])

        # Iterate through the aggregated data above and sort the data according to the sequence
        # start positions.
        for note_id, aggregate_info in note_aggregate.items():
            # Sort the aggregated data
            aggregated_output = list()
            aggregate_info.sort(key=lambda info: info[0])
            # The aggregated data will also contain the start position, we don't return this in the
            # final output
            for index, args in enumerate(zip(*aggregate_info)):
                if index == 0:
                    continue
                # Flatten the aggregated nested list
                aggregated_output.append([element for inner_list in args for element in inner_list])

            # Return the aggregated data
            yield note_id, *aggregated_output
