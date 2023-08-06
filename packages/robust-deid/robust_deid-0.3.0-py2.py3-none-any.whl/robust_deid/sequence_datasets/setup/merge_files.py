# Merge two or more input files into a single input file
import json
from argparse import ArgumentParser
from typing import Sequence, Iterable, Dict, Union, List


def main(
        input_files: Sequence[str]
) -> Iterable[Dict[str, Union[str, Dict[str, str], List[Dict[str, Union[str, int]]]]]]:
    """
    Merge all the notes present in the files passed in the list. That is we go through all
    the notes (json objects) present in every file and return a single iterable, so that we
    can merge the data present in these different files into a single file

    Args:
        input_files (Sequence[str]): List that contains different input files that are to be merged,

    Returns:
        (Iterable[Dict[str, Union[str, Dict[str, str], List[Dict[str, Union[str, int]]]]]]): An iterable that iterates
        through each json object in each file.
    """

    for input_file in input_files:
        for line in open(input_file, 'r'):
            note = json.loads(line)
            yield note


if __name__ == '__main__':
    cli_parser = ArgumentParser(description='configuration arguments provided at run time from the CLI')
    cli_parser.add_argument('--input_files', nargs="+", default=None,
                            help='a list of input files that we want to merge')
    cli_parser.add_argument('--output_file', type=str, help='where to store (file location) the merged data')

    args = cli_parser.parse_args()

    # Write the merged dataset to the output file
    notes = main(input_files=args.input_files)
    with open(args.output_file, 'w') as file:
        for _note in notes:
            file.write(json.dumps(_note) + '\n')
