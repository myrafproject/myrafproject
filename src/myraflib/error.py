class NothingToDo(Exception):
    """Raised when there's nothing to do"""


class AlignError(Exception):
    """Raised when cannot align"""


class NumberOfElementError(Exception):
    """Raised when number of elements is a problem"""


class OverCorrection(Exception):
    """Raised when trying to correct a file multiple times"""


class CardNotFound(Exception):
    """Raised when the key not found in the header"""


class Unsolvable(Exception):
    """Raised when the data is not plate solvable"""


class OperatorError(Exception):
    """Raised when an operand is invalid"""
