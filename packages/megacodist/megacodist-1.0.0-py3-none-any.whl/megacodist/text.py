from enum import Enum
import string
from typing import Iterator, Sequence, Iterable

from .exceptions import LoopBreakException


# Defining constants...
class Delimiters(Enum):
    WHITE_SPACES = string.whitespace
    NEW_LINE_CHARS = [
        '\n',	    # Line Feed
        '\r',	    # Carriage Return
        '\r\n',	    # Carriage Return + Line Feed
        '\v',	    # Line Tabulation
        '\f',	    # Form Feed
        '\x1c',	    # File Separator
        '\x1d',	    # Group Separator
        '\x1e', 	# Record Separator
        '\x85',	    # Next Line (C1 Control Code)
        '\u2028',	# Line Separator
        '\u2029',]	# Paragraph Separator


def IndexAnyLTR(
        text: str,
        search: str,
        start: int | None = None,
        end: int | None = None,
        /
        ) -> int:
    """Returns the first index of occurrence any of characters of 'search'
    in 'text' from left ('start' defaults to None or 0 index) to right ('end'
    defaults to None or len(text) - 1).

    Exceptions:
    TypeError: there are some invalid parameter types or 'end' is less than
    'start'.
    ValueError: there is no occurrence of 'search' characters from 'start'
    index in the 'text'.
    """
    from functools import partial

    # Checking parameters types...
    if not isinstance(text, str):
        raise TypeError("'text' must be string.")
    if not isinstance(search, str):
        raise TypeError("'search' must be string.")
    if (start is not None) and (not isinstance(start, int)):
        raise TypeError("'start' must be None or integer.")
    if (end is not None) and (not isinstance(end, int)):
        raise TypeError("'end' must be None or integer.")

    def _GetIndexLTR(
            ch: str,
            text: str,
            start: int | None = None,
            end: int | None = None
            ) -> int | None:
        try:
            return text.index(ch, start, end)
        except ValueError:
            return None

    FindAnyLTR = partial(
        _GetIndexLTR,
        text=text,
        start=start,
        end=end)
    try:
        return min(filter(
            lambda a: a is not None,
            map(
                FindAnyLTR,
                search)))
    except ValueError as err:
        err.args = (
            "No occurrence of any of 'search' was found in 'text'",)
        raise err


def IndexAnyRTL(
        text: str,
        search: str,
        start: int | None = None,
        end: int | None = None,
        /
        ) -> int:
    """Returns the first index of occurrence any of characters of 'search'
    in 'text' from right ('end' defaults to None or len(text) - 1) to  left
    ('start' defaults to None or 0 index) .

    Exceptions:
    TypeError: there are some invalid parameter types or 'end' is less than
    'start'.
    ValueError: there is no occurrence of 'search' characters from 'start'
    index in the 'text'.
    """
    from functools import partial

    # Checking parameters types...
    if not isinstance(text, str):
        raise TypeError("'text' must be string.")
    if not isinstance(search, str):
        raise TypeError("'search' must be string.")
    if (start is not None) and (not isinstance(start, int)):
        raise TypeError("'start' must be None or integer.")
    if (end is not None) and (not isinstance(end, int)):
        raise TypeError("'end' must be None or integer.")

    def _GetIndexRTL(
            ch: str,
            text: str,
            start: int | None = None,
            end: int | None = None
            ) -> int | None:
        try:
            return text.rindex(ch, start, end)
        except ValueError:
            return None

    FindAnyRTL = partial(
        _GetIndexRTL,
        text=text,
        start=start,
        end=end)
    try:
        return max(filter(
            lambda a: a is not None,
            map(
                FindAnyRTL,
                search)))
    except ValueError as err:
        err.args = (
            "No occurrence of any of 'search' was found in 'text'",)
        raise err


def SplitAnyIter(
        text: str,
        delimiters: str | Delimiters = Delimiters.WHITE_SPACES,
        minSize: int = 0
        ) -> Iterator[str]:
    """Splits 'text' at any element of 'delimiters' and returns them as
    iterator (not a list). With the specified 'minSize' this slicing
    happens after that number of characters. For delimiters any member
    of Delimiters enumeration in this module can be used, or you can
    assign any string, default is Delimiters.WHITE_SPACES. This function
    'eats' any delimiter at the start of chuncks.
    """
    if isinstance(delimiters, Delimiters):
        delimiters = delimiters.value
    start = 0
    while True:
        # Stripping (eating) leading delimiters at the start of this chunck...
        try:
            while text[start] in delimiters:
                start += 1
        except IndexError:
            # There were only delimiters on the remainder of 'text'...
            # Returning an empty string...
            yield ''
            return

        end = start + minSize
        if minSize:
            if end >= len(text):
                yield text[start:]
                return
            elif text[end] in delimiters:
                yield text[start:end]
                start = end
                continue

        # Finding the nearest delimiter on the right...
        try:
            delimIndex = IndexAnyLTR(
                text,
                delimiters,
                end)
        except ValueError:
            pass
        if delimIndex:
            yield text[start:delimIndex]
            start = delimIndex
        else:
            # No white delimiter was found on the remainder of 'text'
            # Returning the rest of text
            yield text[start:]
            return


def GetCommonAffix(
        texts: Iterable[Sequence],
        is_suffix: bool = False
        ) -> slice:
    '''Returns the common affix, either prefix or suffix, of two or more
    sequences and returns a slice object specifying the intersection (at
    the start or end). It accepts two or more sequences, aggregated in
    'texts' parameter, if less is provided TypeError exception will be
    raised. The optional 'is_suffix' parameter specifies the affix, either
    prefix or suffix. So to find the common suffix set this parameter
    to true.
    '''

    # Checking parameters...
    try:
        iter(texts)
    except TypeError:
        raise("'texts' parameter must be an ietrable.")

    if len(texts) < 2:
        raise TypeError('At least two sequences must be provided.')

    if is_suffix:
        startIndex = -1
        increment = -1
    else:
        startIndex = 0
        increment = 1

    index = startIndex
    while True:
        try:
            for seqIndex in range(len(texts) - 1):
                if texts[seqIndex][index] != texts[seqIndex + 1][index]:
                    # Stopping comparisons
                    # when the first inequality if found...
                    raise LoopBreakException
        except (IndexError, LoopBreakException):
            # Stopping comparisons when the first sequence is exhausted...
            break

        index += increment

    if is_suffix:
        return slice(index - startIndex, None)
    else:
        return slice(startIndex, index)


def squeeze_text(text, sqz_width, /, break_width=10) -> list:
    '''Accepts a text and returns a list of strings of specified squeezed width.
    
    break_width specifies how many characters must search for word wrap otherwise uses hyphen to break up the last word in each line (each string element in the list return value).'''
    # Checking the correctness of parameters...
    if not isinstance(text, str):
        raise TypeError("'text' argument must be a string")
    if not isinstance(sqz_width, int):
        raise TypeError("'sqz_width' argument must be an integer")
    if sqz_width < 3:
        raise ValueError("'sqz_width' must be greater than 2")
    if not isinstance(break_width, int):
        raise TypeError("'break_width' argument must be an integer")
    if break_width < 1:
        raise ValueError("'sqz_width' must be at least 1")
    
    NEW_LINE = '\n'
    WHITE_SPACE = ' '
    lines = []
    start_index = 0
    next_new_line = text.find(NEW_LINE)
    while True:
        # Ensuring that
        # Firstly NEW_LINE exists (-1 < next_new_line)
        # Secondly lies in the scope of current line, less than sqz_width away (next_new_line < start_index + sqz_width)
        if (-1 < next_new_line < start_index + sqz_width):
            # Then append a slice of text from start_index to next_new_line to the result (including the former & excluding the latter)
            lines.append(text[start_index:next_new_line])
            start_index = next_new_line + 1
            next_new_line = text.find(NEW_LINE, start_index)
        # Else either of the above conditions is not satisfied
        # First of all, checking we are at the end of passed-in string (text)...
        elif (len(text) < start_index + sqz_width):
            # If so, adding the rest of the passed-in string to the result...
            lines.append(text[start_index:])
            break
        # Else
        # Second of all, checking there is a WHITE_SPACE just after this slice...
        elif (text[start_index + sqz_width] == WHITE_SPACE):
            # If it is the case, adding a slice from text with the length of sqz_width to the result & starting next slice just after it...
            lines.append(text[start_index:start_index + sqz_width])
            start_index = start_index + sqz_width + 1
        else:
            # And third of all, checking there is a WHITE_SPACE in the breaking zone of the current slice (in the break_width characters at the end of this slice)...
            ws_index = text.rfind(
                WHITE_SPACE,
                start_index + sqz_width - break_width,
                start_index + sqz_width
            )
            # If there is, breaking up the current line at that position...
            if (ws_index > -1):
                lines.append(text[start_index:ws_index])
                start_index = ws_index + 1
            else:
                # If there is not, move the last character of this slice tothenext slice & replace it with dash (-) character...
                lines.append(text[start_index:start_index + sqz_width - 1] + '-')
                start_index += (sqz_width - 1)
    
    return lines

def squeeze_text_iter(text, sqz_width, /, break_width=10):
    '''Accepts a text and yields a list of strings of specified squeezed width.
    
    break_width specifies how many characters must search for word wrap otherwise uses hyphen to break up the last word in each line (each string element in the list return value).'''
    NEW_LINE = '\n'
    WHITE_SPACE = ' '
    start_index = 0
    next_new_line = text.find(NEW_LINE)
    while True:
        # Ensuring that
        # Firstly NEW_LINE exists (-1 < next_new_line)
        # Secondly lies in the scope of current line, less than sqz_width away (next_new_line < start_index + sqz_width)
        if (-1 < next_new_line < start_index + sqz_width):
            # Then yielding a slice of text from start_index to next_new_line to the result (including the former & excluding the latter)
            yield text[start_index:next_new_line]
            start_index = next_new_line + 1
            next_new_line = text.find(NEW_LINE, start_index)
        # Else either of the above conditions is not satisfied
        # First of all, checking we are at the end of passed-in string (text)...
        elif (len(text) < start_index + sqz_width):
            # If so, yielding the rest of the passed-in string to the result...
            yield text[start_index:]
            break
        # Else
        # Second of all, checking there is a WHITE_SPACE just after this slice...
        elif (text[start_index + sqz_width] == WHITE_SPACE):
            # If it is the case, yielding a slice from text with the length of sqz_width to the result & starting next slice just after it...
            yield text[start_index:start_index + sqz_width]
            start_index = start_index + sqz_width + 1
        else:
            # And third of all, checking there is a WHITE_SPACE in the breaking zone of the current slice (in the break_width characters at the end of this slice)...
            ws_index = text.rfind(
                WHITE_SPACE,
                start_index + sqz_width - break_width,
                start_index + sqz_width
            )
            # If there is, breaking up the current line at that position...
            if (ws_index > -1):
                yield text[start_index:ws_index]
                start_index = ws_index + 1
            else:
                # If there is not, move the last character of this slice to the next slice & replace it with dash (-) character...
                yield text[start_index:start_index + sqz_width - 1] + '-'
                start_index += (sqz_width - 1)