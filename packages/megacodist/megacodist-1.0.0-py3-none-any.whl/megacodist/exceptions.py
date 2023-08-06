"""This module offers the following complementary exceptions:

⬤ LoopBreakException
⬤ DuplicateError
⬤ InsertionError
⬤ IntervalError
"""

class LoopBreakException(Exception):
    '''This exception is used to break nested loops.'''
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class DuplicateError(Exception):
    '''This exception is used to notify duplicate and redundancy situations.'''
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InsertionError(Exception):
    '''This exception is used to specify a situation where an insertion operation is impossible either logically or technically.'''
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class IntervalError(Exception):
    '''This exception is used to specify an improper interval or an operation which cannot be done in the specified interval.'''
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
