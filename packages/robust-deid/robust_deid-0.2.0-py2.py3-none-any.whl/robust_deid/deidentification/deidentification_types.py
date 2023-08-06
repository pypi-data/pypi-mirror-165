from enum import Enum


class DeidentificationLevel(Enum):
    EXACT = 1
    RELAXED = 2


class DeidentificationStrategy(Enum):
    AUGMENT = 1
    REMOVE = 2
    INFORMATIVE = 3
