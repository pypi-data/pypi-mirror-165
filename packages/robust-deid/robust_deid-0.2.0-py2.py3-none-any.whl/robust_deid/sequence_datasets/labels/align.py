from enum import Enum


class Align(Enum):
    """
    An Enum that represents the position of a token in a span
    """
    BEGIN = 1
    SINGLE = 2
    INSIDE = 3
    END = 4
    OUTSIDE = 5
