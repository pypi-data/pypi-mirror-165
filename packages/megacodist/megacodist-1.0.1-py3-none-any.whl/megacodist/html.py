from collections import deque
from html.parser import HTMLParser


_SINGLETON_ELEMS = [
    'area',
    'base',
    'br',
    'col',
    'command',
    'embed',
    'hr',
    'img',
    'input',
    'keygen',
    'link',
    'meta',
    'param',
    'source',
    'track',
    'wbr']


class TagMismatchError(Exception):
    """This exception is raised if the elements of an HTML or XML
    code snippet does not match.
    """
    pass


class HtmlTagsChecker(HTMLParser):
    '''An instance of this class can be used to check thecorrect layout
    of tags in an HTML code. The 'feed' method is the only method
    that should be used.
    '''
    def __init__(self, *, convert_charrefs: bool = True) -> None:
        super().__init__(convert_charrefs=convert_charrefs)

        # Definning instance attributes...
        self._tagsStack: list[str] = []

    def feed(self, data: str) -> bool:
        '''Determines that the provided data (HTML code) has
        well-formed tag structure or not.
        '''
        try:
            super().feed(data)
            if len(self._tagsStack) == 0:
                return True
            else:
                return False
        except TagMismatchError:
            return False

    def handle_decl(self, decl: str) -> None:
        super().handle_decl(decl)

    def handle_starttag(
            self,
            tag: str,
            attrs: list[tuple[str, str | None]]
            ) -> None:

        self._tagsStack.append(tag)

    def handle_endtag(self, tag: str) -> None:
        try:
            while True:
                if (tag == self._tagsStack[-1]):
                    # Its corresponding starting tag is found...
                    self._tagsStack.pop()
                    return
                elif (self._tagsStack[-1] in _SINGLETON_ELEMS):
                    self._tagsStack.pop()
                # So far we have not found a corresponding starting tag for it
                elif tag in _SINGLETON_ELEMS:
                    return
                else:
                    raise TagMismatchError()
        except IndexError:
            # Tags stack is exhausted, so it's an orphan ending tag...
            raise TagMismatchError()


class HtmlTagsOutliner_backup(HTMLParser):
    '''An instance of this class can be used to get a beautiful
    outline of elements (only elements) of tags in an HTML code.
    The 'feed' method is the only method that should be used.
    '''
    def __init__(
            self,
            indent: int = 4,
            *,
            convert_charrefs: bool = True
            ) -> None:

        super().__init__(convert_charrefs=convert_charrefs)

        # Definning instance attributes...
        self._level = 0
        self._tagsStack: deque[str] = deque()
        self._indent = ' ' * indent
        self._output = ''
        self._lastTag = ''
        self._isLastOpen = False

    def feed(self, data: str) -> str:
        '''Returns a beautiful outline of elements (only elements) in the
        provided data (HTML code).
        '''
        super().feed(data)
        if not len(self._tagsStack):
            return self._output
        else:
            raise TagMismatchError()

    def _append_tag(
            self,
            tag: str
            ) -> None:
        pre = ''
        try:
            lastOpenShevron = self._output.rindex('<')
            lastTag = self._output[lastOpenShevron:-1]
            if lastTag != tag:
                pre = '\n' + (self._indent * self._level)
        except ValueError:
            pass
        self._output += (pre + tag)

    def handle_decl(self, decl: str) -> None:
        self._append_tag(f'<!{decl}>')

    def unknown_decl(self, data: str) -> None:
        self._append_tag(f'<?{data}>')

    def handle_starttag(
            self,
            tag: str,
            attrs: list[tuple[str, str | None]]
            ) -> None:

        self._append_tag(f'<{tag}>')
        self._tagsStack.append(tag)
        self._level += 1
        self._lastTag = tag
        self._isLastOpen = True

    def handle_endtag(self, tag: str) -> None:
        try:
            while True:
                if (tag == self._tagsStack[-1]):
                    # Its corresponding starting tag is found...
                    self._append_tag(f'</{tag}>', next_line=False)
                    self._tagsStack.pop()
                    self._level -= 1
                    return
                elif (self._tagsStack[-1] in _SINGLETON_ELEMS):
                    self._append_tag(f'</{tag}>')
                    self._tagsStack.pop()
                    self._level -= 1
                # So far we have not found a corresponding starting tag for it
                elif tag in _SINGLETON_ELEMS:
                    return
                else:
                    raise TagMismatchError()
        except IndexError:
            # Tags stack is exhausted, so it's an orphan ending tag...
            raise TagMismatchError()


class HtmlTagsOutliner(HTMLParser):
    '''An instance of this class can be used to get a beautiful
    outline of elements (only elements) of tags in an HTML code.
    The 'feed' method is the only method that should be used.
    '''
    def __init__(
            self,
            indent: int = 4,
            *,
            convert_charrefs: bool = True
            ) -> None:

        super().__init__(convert_charrefs=convert_charrefs)

        # Definning instance attributes...
        self._level = 0
        self._tagsStack: deque[str] = deque()
        self._indent = ' ' * indent
        self._output = ''
        self._lastTag = ''
        self._isLastOpen = False

    def feed(self, data: str) -> str:
        '''Returns a beautiful outline of elements (only elements) in the
        provided data (HTML code).
        '''
        super().feed(data)
        if not len(self._tagsStack):
            return self._output
        else:
            raise TagMismatchError()

    def _append_tag(
            self,
            tag: str,
            next_line: bool = True
            ) -> None:

        if next_line:
            pre = '\n' + (self._indent * self._level)
        else:
            pre = ''
        self._output += (pre + tag)

    def handle_decl(self, decl: str) -> None:
        self._append_tag(f'<!{decl}>')

    def unknown_decl(self, data: str) -> None:
        self._append_tag(f'<?{data}>')

    def handle_starttag(
            self,
            tag: str,
            attrs: list[tuple[str, str | None]]
            ) -> None:

        self._append_tag(f'<{tag}>', next_line=True)
        self._tagsStack.append(tag)
        self._level += 1
        self._lastTag = tag
        self._isLastOpen = True

    def handle_endtag(self, tag: str) -> None:
        try:
            while True:
                if (tag == self._tagsStack[-1]):
                    # Its corresponding starting tag is found...
                    self._level -= 1
                    if self._isLastOpen and self._lastTag == tag:
                        next_line = False
                    else:
                        next_line = True
                    self._append_tag(f'</{tag}>', next_line=next_line)
                    self._tagsStack.pop()
                    self._lastTag = tag
                    self._isLastOpen = False
                    return
                elif (self._tagsStack[-1] in _SINGLETON_ELEMS):
                    self._append_tag(f'</{tag}>')
                    self._tagsStack.pop()
                    self._level -= 1
                # So far we have not found a corresponding starting tag for it
                elif tag in _SINGLETON_ELEMS:
                    return
                else:
                    raise TagMismatchError()
        except IndexError:
            # Tags stack is exhausted, so it's an orphan ending tag...
            raise TagMismatchError()
