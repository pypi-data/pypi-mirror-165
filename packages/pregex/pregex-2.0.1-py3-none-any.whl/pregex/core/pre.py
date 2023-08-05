import re as _re
import enum as _enum
import pregex.core.exceptions as _ex
from typing import Iterator as _Iterator


__doc__ = """
This module contains two classes, namely :class:`Pregex` which constitutes
the base class for every other class within `pregex`, and :class:`Empty`
which corresponds to the empty string pattern ``''``.

Classes & methods
-------------------------------------------

Below are listed all classes within :py:mod:`pregex.core.pre`
along with any possible methods they may possess.
"""


class _Type(_enum.Enum):
    '''
    This enum represents all possible types of a RegEx pattern.
    '''
    Alternation = 0
    Assertion = 1
    Class = 2
    Empty = 3
    Group = 4
    Other = 5
    Quantifier = 6
    Token = 7


class Pregex():
    '''
    Wraps the provided pattern within an instance of this class.

    :param str pattern: The pattern that is to be wrapped within an instance of this class.
    :param bool escape: Determines whether to escape the provided pattern or not. Defaults to ``True``.

    :raises InvalidArgumentTypeException: Parameter ``pattern`` is not a string.

    :note: This class constitutes the base class for every other class within the `pregex` package.
    '''


    '''
    Determines the groupping rules of each Pregex instance type:

    :schema: __groupping_rules[type] => (on_concat, on_quantify, on_assertion)
    '''
    __groupping_rules: dict[_Type, str] = {
        _Type.Alternation: (True, True, True),
        _Type.Assertion : (False, True, False),
        _Type.Class: (False, False, False),
        _Type.Empty: (False, False, False),
        _Type.Group: (False, False, False),
        _Type.Other: (False, True, False),
        _Type.Quantifier: (False, True, False),
        _Type.Token: (False, False, False),
    }


    '''
    The totality of active flags.
    '''
    __flags: _re.RegexFlag = _re.MULTILINE | _re.DOTALL


    def __init__(self, pattern: str, escape: bool = True) -> 'Pregex':
        '''
        Wraps the provided pattern within an instance of this class.

        :param str pattern: The pattern that is to be wrapped within an instance of this class.
        :param bool escape: Determines whether to escape the provided pattern or not. Defaults to ``True``.

        :raises InvalidArgumentTypeException: Parameter ``pattern`` is not a string.

        :note: This class constitutes the base class for every other class within the `pregex` package.
        '''
        if not isinstance(pattern, str):
            message = "Provided argument \"pattern\" is not a string."
            raise _ex.InvalidArgumentTypeException(message)
        if escape:
            self.__pattern = __class__.__escape(pattern)
        else:
            self.__pattern = pattern
        self.__type, self.__quantifiable = __class__.__infer_type(self.__pattern)
        self.__compiled: _re.Pattern = None


    '''
    Public Methods
    '''
    def print_pattern(self, include_flags: bool = False) -> None:
        '''
        Prints this instance's underlying RegEx pattern.

        :param bool include_falgs: Determines whether to display the RegEx flags \
            along with the pattern. Defaults to ``False``.
        '''
        print(self.get_pattern(include_flags))


    def get_pattern(self, include_flags: bool = False) -> str:
        '''
        Returns this instance's underlying RegEx pattern as a string.

        :param bool include_falgs: Determines whether to display the RegEx flags \
            along with the pattern. Defaults to ``False``.

        :note: This method is to be preferred over str() when one needs to display \
            this instance's underlying Regex pattern.
        '''
        pattern = repr(self)
        return f"/{pattern}/gmsu" if include_flags else pattern


    def get_compiled_pattern(self, discard_after: bool = True) -> _re.Pattern:
        '''
        Returns this instance's underlying RegEx pattern as a ``re.Pattern`` instance.
        
        :param bool discard_after: Determines whether the compiled pattern is to be \
            discarded after this method, or to be retained so that any further attempt \
            at matching a string will use the compiled pattern instead of the regular one. \
            Defaults to ``True``.
        '''
        if self.__compiled is None:
            self.compile()
        compiled = self.__compiled
        if discard_after:
            self.__compiled = None
        return compiled


    def compile(self) -> None:
        '''
        Compiles the underlying RegEx pattern. After invoking this method, any \
        further attempt at matching a string will use the compiled RegEx pattern \
        instead of the regular one.
        '''
        self.__compiled = _re.compile(self.get_pattern(), flags=self.__flags)


    @staticmethod
    def purge() -> None:
        '''
        Clears the regular expression caches.
        '''
        _re.purge()


    def has_match(self, source: str, is_path: bool = False) -> bool:
        '''
        Returns ``True`` if at least one match is found within the provided text.

        :param str source: The text that is to be examined \
            is provided through this parameter.
        :param bool is_path: If set to ``True``, then parameter ``source`` \
            is considered to be a local path pointing to the file from which \
            the text is to be read. Defaults to ``False``.
        '''
        if is_path:
            source = self.__extract_text(source)
        return bool(_re.search(self.__pattern, source) if self.__compiled is None \
            else self.__compiled.search(source))


    def is_exact_match(self, source: str, is_path: bool = False) -> bool:
        '''
        Returns ``True`` only if the provided text matches this pattern exactly.

        :param str source: The text that is to be examined \
            is provided through this parameter.
        :param bool is_path: If set to ``True``, then parameter ``source`` \
            is considered to be a local path pointing to the file from which \
            the text is to be read. Defaults to ``False``.
        '''
        if is_path:
            source = self.__extract_text(source)
        return bool(_re.fullmatch(self.__pattern, source, flags=self.__flags) \
            if self.__compiled is None else self.__compiled.fullmatch(source))


    def iterate_matches(self, source: str, is_path: bool = False) -> _Iterator[str]:
        '''
        Generates any possible matches found within the provided text.

        :param str source: The text that is to be examined \
            is provided through this parameter.
        :param bool is_path: If set to ``True``, then parameter ``source`` \
            is considered to be a local path pointing to the file from which \
            the text is to be read. Defaults to ``False``.
        '''
        for match in self.__iterate_match_objects(source, is_path):
            yield match.group(0)


    def iterate_matches_and_pos(self, source: str, is_path: bool = False) -> _Iterator[tuple[str, int, int]]:
        '''
        Generates any possible matches found within the provided text \
        along with their exact position.

        :param str source: The text that is to be examined \
            is provided through this parameter.
        :param bool is_path: If set to ``True``, then parameter ``source`` \
            is considered to be a local path pointing to the file from which \
            the text is to be read. Defaults to ``False``.
        '''
        for match in self.__iterate_match_objects(source, is_path):
            yield (match.group(0), *match.span())


    def iterate_captures(self, source: str, include_empty: bool = True,
        is_path: bool = False) -> _Iterator[tuple[str]]:
        '''
        Generates tuples, one tuple per match, where each tuple contains \
        all of its corresponding match's captured groups. In case there exists \
        a capturing group within the pattern that has not been captured by a match, \
        then that capture's corresponding value will be ``None``.

        :param str source: The text that is to be examined \
            is provided through this parameter.
        :param bool include_empty: Determines whether to include empty captures into the \
            results. Defaults to ``True``.
        :param bool is_path: If set to ``True``, then parameter ``source`` \
            is considered to be a local path pointing to the file from which \
            the text is to be read. Defaults to ``False``.
        '''
        for match in self.__iterate_match_objects(source, is_path):
            yield match.groups() if include_empty else \
                tuple(group for group in match.groups() if group != '')


    def iterate_captures_and_pos(self, source: str, include_empty: bool = True,
        relative_to_match : bool = False, is_path: bool = False) -> _Iterator[list[tuple[str, int, int]]]:
        '''
        Generates lists of tuples, one list per match, where each tuple contains one \
        of its corresponding match's captured groups along with its exact position \
        within the text. In case there exists a capturing group within the pattern that \
        has not been captured by a match, then that capture's corresponding tuple will be \
        ``(None, -1, -1)``.

        :param str source: The text that is to be examined \
            is provided through this parameter.
        :param bool include_empty: Determines whether to include empty captures into the \
            results. Defaults to ``True``.
        :param bool relative_to_match: If ``True``, then each group's position-indices are calculated \
            relative to the group's corresponding match, not to the whole string. Defaults to ``False``.
        :param bool is_path: If set to ``True``, then parameter ``source`` \
            is considered to be a local path pointing to the file from which \
            the text is to be read. Defaults to ``False``.
        '''
        for match in self.__iterate_match_objects(source, is_path):
            groups, counter = list(), 0
            for group in match.groups():
                counter += 1
                if include_empty or (group != ''):
                    start, end = match.span(counter)
                    if relative_to_match and start > -1:
                        start, end = start - match.start(0), end - match.start(0)
                    groups.append((group, start, end))
            yield groups


    def get_matches(self, source: str, is_path: bool = False) -> list[str]:
        '''
        Returns a list containing any possible matches found within \
        the provided text.

        :param str source: The text that is to be examined \
            is provided through this parameter.
        :param bool is_path: If set to ``True``, then parameter ``source`` \
            is considered to be a local path pointing to the file from which \
            the text is to be read. Defaults to ``False``.
        '''
        return list(match for match in self.iterate_matches(source, is_path))


    def get_matches_and_pos(self, source: str, is_flag: bool = False) -> list[tuple[str, int, int]]:
        '''
        Returns a list containing any possible matches found within the \
        provided text along with their exact position.

        :param str source: The text that is to be examined \
            is provided through this parameter.
        :param bool is_path: If set to ``True``, then parameter ``source`` \
            is considered to be a local path pointing to the file from which \
            the text is to be read. Defaults to ``False``.
        '''
        return list(match for match in self.iterate_matches_and_pos(source, is_flag))


    def get_captures(self, source: str, include_empty: bool = True, is_path: bool = False) -> list[tuple[str]]:
        '''
        Returns a list of tuples, one tuple per match, where each tuple contains \
        all of its corresponding match's captured groups. In case there exists \
        a capturing group within the pattern that has not been captured by a match, \
        then that capture's corresponding value will be ``None``.

        :param str source: The text that is to be examined \
            is provided through this parameter.
        :param bool include_empty: Determines whether to include empty captures into the \
            results. Defaults to ``True``.
        :param bool is_path: If set to ``True``, then parameter ``source`` \
            is considered to be a local path pointing to the file from which \
            the text is to be read. Defaults to ``False``.
        '''
        return list(group for group in self.iterate_captures(source, include_empty, is_path))


    def get_captures_and_pos(self, source: str, include_empty: bool = True,
        relative_to_match: bool = False, is_path: bool = False) -> list[list[tuple[str, int, int]]]:
        '''
        Returns a list containing lists of tuples, one list per match, where each \
        tuple contains one of its corresponding match's captured groups along with \
        its exact position within the text. In case there exists a capturing group \
        within the pattern that has not been captured by a match, then that capture's \
        corresponding tuple will be ``(None, -1, -1)``.

        :param str source: The text that is to be examined \
            is provided through this parameter.
        :param bool include_empty: Determines whether to include empty captures into the \
            results. Defaults to ``True``.
        :param bool relative_to_match: If ``True``, then each group's position-indices are calculated \
            relative to the group's corresponding match, not to the whole string. Defaults to ``False``.
        :param bool is_path: If set to ``True``, then parameter ``source`` \
            is considered to be a local path pointing to the file from which \
            the text is to be read. Defaults to ``False``.
        '''
        return list(tup for tup in self.iterate_captures_and_pos(
            source, include_empty, relative_to_match, is_path))


    def replace(self, source: str, repl: str, count: int = 0, is_path: bool = False) -> str:
        '''
        Substitutes all or some of the occuring matches with ``text`` for ``repl`` \
        and returns the resulting string. If there are no matches, returns \
        parameter ``text`` exactly as provided.

        :param str source: The string that is to be matched and modified.
        :param str repl: The string that is to replace any matches.
        :param int count: The number of matches that are to be replaced, \
            starting from left to right. A value of ``0`` indicates that \
            all matches must be replaced. Defaults to ``0``.
        :param bool is_path: If set to ``True``, then parameter ``source`` \
            is considered to be a local path pointing to the file from which \
            the text is to be read. Defaults to ``False``.

        :raises InvalidArgumentValueException: Parameter ``count`` has a value of less than zero.
        '''
        if count < 0:
            message = "Parameter \"count\" can't be negative."
            raise _ex.InvalidArgumentValueException(message)
        if is_path:
            source = self.__extract_text(source)
        return _re.sub(str(self), repl, source, count, flags=self.__flags)


    def split_by_match(self, source: str, is_path: bool = False) -> list[str]:
        '''
        Splits the provided text based on any matches with this pattern and \
        returns the result as a list containing each individual part of the \
        text after the split.

        :param str source: The piece of text that is to be matched and split.
        :param bool is_path: If set to ``True``, then parameter ``source`` \
            is considered to be a local path pointing to the file from which \
            the text is to be read. Defaults to ``False``.
        '''
        if is_path:
            source = self.__extract_text(source)
        split_list, index = list(), 0
        for _, start, end in self.iterate_matches_and_pos(source):
            if index != start:
                split_list.append(source[index:start])
            index = end
        if index != len(source):
            split_list.append(source[index:])
        return split_list


    def split_by_capture(self, source: str, include_empty: bool = True, is_path: bool = False) -> list[str]:
        '''
        Splits the provided text based on any captured groups that may have \
        occured due to matches with thin pattern, and returns the result as a\
        list containing each individual part of the text after the split.

        :param str source: The piece of text that is to be matched and split.
        :param bool include_empty: Determines whether to include empty groups into the results. \
            Defaults to ``True``.
        :param bool is_path: If set to ``True``, then parameter ``source`` \
            is considered to be a local path pointing to the file from which \
            the text is to be read. Defaults to ``False``.
        '''
        if is_path:
            source = self.__extract_text(source)
        split_list, index = list(), 0
        for groups in self.iterate_captures_and_pos(source, include_empty):
            for group, start, end in groups:
                if group is None:
                    continue
                if index != start:
                    split_list.append(source[index:start])
                index = end
        if index != len(source):
            split_list.append(source[index:])
        return split_list


    '''
    Protected Methods
    '''
    def _get_type(self) -> _Type:
        '''
        Returns this instance's type.
        '''
        return self.__type


    def _is_quantifiable(self):
        '''
        Returns ``True`` if this pattern can be quantified, else returns ``False``.
        '''
        return self.__quantifiable


    def _concat_conditional_group(self) -> str:
        '''
        Returns this instance's pattern wrapped within a non-capturing group
        only if the instance's group-on-concat rule is set to ``True``.
        '''
        return self._non_capturing_group() if self.__get_group_on_concat_rule() else str(self)


    def _quantify_conditional_group(self) -> str:
        '''
        Returns this instance's pattern wrapped within a non-capturing group
        only if the instance's group-on-quantify rule is set to ``True``.
        '''
        return self._non_capturing_group() if self.__get_group_on_quantify_rule() else str(self)


    def _assert_conditional_group(self) -> str:
        '''
        Returns this instance's pattern wrapped within a non-capturing group
        only if the instance's group-on-assertion rule is set to ``True``.
        '''
        return self._non_capturing_group() if self.__get_group_on_assert_rule() else str(self)


    def _to_pregex(pre: 'Pregex' or str) -> 'Pregex':
        '''
        Returns ``pre`` exactly as provided if it is a ``Pregex`` instance, \
        else if it is a string, this method then wraps it within a ``Pregex`` \
        instance while also setting ``escape`` to ``True`` and returns said instance.

        :param Pregex | str: Either a string or a ``Pregex`` instance.

        :raises InvalidArgumentTypeException: Argument ``pre`` is neither a string nor a \
            ``Pregex`` class instance.
        '''
        if isinstance(pre, str):
            return Pregex(pre, escape=True)
        elif issubclass(pre.__class__, __class__):
            return pre
        else:
            message = "Parameter \"pre\" must either be a string or an instance of \"Pregex\"."
            raise _ex.InvalidArgumentTypeException(message)


    ''' 
    Private Methods
    '''
    def __str__(self) -> str:
        '''
        Returns the string representation of this class instance.

        :note: Not to be used for pattern-display purposes.
        '''
        return self.__pattern


    def __repr__(self) -> str:
        '''
        Returns the string representation of this class instance in a printable format.
        '''
        # Replace any quadraple backslashes.
        return _re.sub(r"\\\\", r"\\", repr(self.__pattern)[1:-1])
        

    def __add__(self, pre: str or 'Pregex') -> 'Pregex':
        '''
        Concatenates self with the provided string or ``Pregex`` instance,
        and returns the resulting ``Pregex`` instance.

        :param pre: The string or ``Pregex`` class instance that is to be concatenated with \
            this instance. 
        '''
        return __class__(self._concat(__class__._to_pregex(pre)), escape=False)


    def __radd__(self, pre: str or 'Pregex') -> 'Pregex':
        '''
        Concatenates self with the provided string or ``Pregex`` instance,
        and returns the resulting ``Pregex`` instance.

        :param pre: The string or ``Pregex`` instance that is to be concatenated with \
            this instance. 
        '''
        return __class__(__class__._to_pregex(pre)._concat(self), escape=False)


    def __mul__(self, n: int) -> 'Pregex':
        '''
        Matches ``self`` exactly ``n`` times.

        :param int n: This parameter indicates the number of times that ``self`` \
            is to be matched.

        :raises InvalidArgumentTypeException: Parameter ``n`` is not an integer.
        :raises InvalidArgumentValueException: Parameter ``n`` is less than zero.
        :raises CannotBeQuantifiedException: ``self`` represents an non-quantifiable pattern.
        '''
        if not self._is_quantifiable():
            raise _ex.CannotBeQuantifiedException(self)
        if not isinstance(n, int) or isinstance(n, bool):
            message = "Provided argument \"n\" is not an integer."
            raise _ex.InvalidArgumentTypeException(message)
        if n < 0:
            message = "Using multiplication operator with a negative integer is not allowed."
            raise _ex.InvalidArgumentValueException(message)
        return __class__(self._exactly(n), escape=False)


    def __rmul__(self, n: int) -> 'Pregex':
        '''
        Matches ``self`` exactly ``n`` times.

        :param int n: This parameter indicates the number of times that ``self`` \
            is to be matched.

        :raises InvalidArgumentTypeException: Parameter ``n`` is not an integer.
        :raises InvalidArgumentValueException: Parameter ``n`` is less than zero.
        :raises CannotBeQuantifiedException: ``self`` represents an non-quantifiable pattern.
        '''
        if not self._is_quantifiable():
            raise _ex.CannotBeQuantifiedException(self)
        if not isinstance(n, int) or isinstance(n, bool):
            message = "Provided argument \"n\" is not an integer."
            raise _ex.InvalidArgumentTypeException(message)
        if n < 0:
            message = "Using multiplication operator with a negative integer is not allowed."
            raise _ex.InvalidArgumentValueException(message)
        return __class__(self._exactly(n), escape=False)


    def __get_group_on_concat_rule(self) -> bool:
        '''
        Returns this instance's `group-on-concat` rule.
        '''
        return __class__.__groupping_rules[self.__type][0]


    def __get_group_on_quantify_rule(self) -> bool:
        '''
        Returns this instance's `group-on-quantify` rule.
        '''
        return __class__.__groupping_rules[self.__type][1]


    def __get_group_on_assert_rule(self) -> bool:
        '''
        Returns this instance's `group-on-assert` rule.
        '''
        return __class__.__groupping_rules[self.__type][2]


    def __iterate_match_objects(self, source: str, is_path: bool) -> _Iterator[_re.Match]:
        '''
        Invokes ``re.finditer`` in order to iterate over all matches of this \
        instance's underlying pattern with the provided string ``text`` as \
        instances of type ``re.Match``.

        :param str source: The text that is to be examined \
            is provided through this parameter.
        :param bool is_path: If set to ``True``, then parameter ``source`` \
            is considered to be a local path pointing to the file from which \
            the text is to be read.
        '''
        if is_path:
            source = self.__extract_text(source)
        return _re.finditer(self.__pattern, source, flags=self.__flags) \
            if self.__compiled is None else self.__compiled.finditer(source)


    @staticmethod
    def __escape(pattern: str) -> str:
        '''
        Scans this instance's underlying pattern for any characters that need to be escaped, \
        escapes them if there are any, and returns the resulting string pattern.
        within a new ``Pregex`` class instance.
        '''
        pattern = pattern.replace("\\", "\\\\")
        for c in {'^', '$', '(', ')', '[', ']', '{', '}', '?', '+', '*', '.', '|', '/'}:
            pattern = pattern.replace(c, f"\\{c}")
        return pattern   


    @staticmethod
    def __infer_type(pattern: str) -> tuple[_Type, bool]:
        '''
        Examines the provided RegEx pattern and returns its type,
        as well as a boolean indicating whether said pattern can be
        quantified or not.

        :param str pattern: The RegEx pattern that is to be examined.
        '''
        def remove_groups(pattern: str, repl: str = ''):
            '''
            Removes all groups from the provided pattern, and replaces them with ``repl``.

            :param str pattern: The pattern whose groups are to be removed.
            :param str repl: The string that replaces all groups within the pattern. \
                Defaults to ``''``.
            '''
            left_par, right_par = r"(?:(?<!\\)\()", r"(?:(?<!\\)\))"
            if len(_re.findall(left_par, pattern)) == 0:
                return pattern
            temp = _re.sub(pattern=left_par + r"(?:[^\(\)]|\\(?:\(|\)))+" + right_par,
                repl=repl, string=pattern)
            return temp if temp == repl else remove_groups(temp, repl)

        def __is_group(pattern: str) -> bool:
            '''
            Looks at the underlying pattern of this instance, and returns either \
            ``True`` or ``False``, depending on whether the provided RegEx pattern \
            represents a group or not.

            :param str pattern: The pattern that is to be examined.
            '''
            if pattern.startswith('(') and pattern.endswith(')'):
                n_open = 0
                for i in range(1, len(pattern) - 1):
                    prev_char, curr_char = pattern[i-1], pattern[i]
                    if prev_char != "\\": 
                        if curr_char == ')':
                            if n_open == 0:
                                return False
                            else:
                                n_open -= 1
                        if curr_char == '(':
                            n_open += 1
                return n_open == 0
            return False

        # Replace escaped backslashes with some other character.
        pattern = _re.sub(r"\\{2}", "a", pattern)

        if pattern == "":
            return _Type.Empty, True
        elif _re.fullmatch(r"\\?.", pattern, flags=__class__.__flags) is not None:
            if _re.fullmatch(r"\.|\\(?:w|d|s)", pattern,
                flags=__class__.__flags | _re.IGNORECASE) is not None:
                return _Type.Class, True
            elif _re.fullmatch(r"\.|\\(?:b|B)", pattern,
                flags=__class__.__flags | _re.IGNORECASE) is not None:
                return _Type.Assertion, True
            else:
                return _Type.Token, True

        # Simplify classes by removing extra characters.
        pattern = _re.sub(r"\[.+?(?<!\\)\]", "[a]", pattern)

        if pattern == "[a]":
            return _Type.Class, True
        elif __is_group(pattern):
            return _Type.Group, True

        # Replace every group with a simple character.
        temp = remove_groups(pattern, repl="G")

        if len(_re.split(pattern=r"(?<!\\)\|", string=temp)) > 1:
                return _Type.Alternation, True
        elif _re.fullmatch(r"(?:\^|\\A|\(\?<=.+\)).+|.+(?:\$|\\Z|\(\?=.+\))",
            pattern, flags=__class__.__flags) is not None:
            return _Type.Assertion, False
        elif _re.fullmatch(r"(?:\\b|\\B|\(\?<!.+\)).+|.+(?:\\b|\\B|\(\?!.+\))",
            pattern, flags=__class__.__flags) is not None:
            return _Type.Assertion, True
        elif _re.fullmatch(r"(?:\\.|[^\\])?(?:\?|\*|\+|\{(?:\d+|\d+,|,\d+|\d+,\d+)\})",
            temp, flags=__class__.__flags) is not None:
            return _Type.Quantifier, True
        return _Type.Other, True


    @staticmethod
    def __extract_text(source: str) -> str:
        '''
        Reads and returns the text that is contained within the file \
        to which the provided path points.

        :param str source: The path pointing to the file from which the text \
            is to be extracted.
        '''
        with open(file=source, mode='r', encoding='utf-8') as f:
            text = f.read()
        return text


    '''
    Quantifiers
    '''
    def _optional(self, is_greedy: bool = True)-> str:
        '''
        Applies quantifier ``?`` on this instance's underlying pattern and \
        returns the resulting pattern as a string.

        :param bool is_greedy: Determines whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to ``True``.
        '''
        return f"{self._quantify_conditional_group()}?{'' if is_greedy else '?'}"


    def _indefinite(self, is_greedy: bool = True) -> str:
        '''
        Applies quantifier ``*`` on this instance's underlying pattern and \
        returns the resulting pattern as a string.

        :param bool is_greedy: Determines whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to ``True``.
        '''
        return f"{self._quantify_conditional_group()}*{'' if is_greedy else '?'}"


    def _one_or_more(self, is_greedy: bool = True) -> str:
        '''
        Applies quantifier ``+`` on this instance's underlying pattern and \
        returns the resulting pattern as a string.

        :param bool is_greedy: Determines whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to ``True``.
        '''
        return f"{self._quantify_conditional_group()}+{'' if is_greedy else '?'}"


    def _exactly(self, n: int) -> str:
        '''
        Applies quantifier ``{n}`` on this instance's underlying pattern and \
        returns the resulting pattern as a string.

        :param int n: The exact number of times that the provided pattern is to be matched.
        '''
        if n == 0:
            return str(Empty())
        if n == 1:
            return str(self)
        else:
            return f"{self._quantify_conditional_group()}{{{n}}}"


    def _at_least(self, n: int, is_greedy: bool = True)-> str:
        '''
        Applies quantifier ``{n,}`` on this instance's underlying pattern and \
        returns the resulting pattern as a string.

        :param int n: The minimum number of times that the provided pattern is to be matched.
        :param bool is_greedy: Determines whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to ``True``.
        '''
        if n == 0:
            return self._indefinite(is_greedy)
        elif n == 1:
            return self._one_or_more(is_greedy)
        else:
            return f"{self._quantify_conditional_group()}{{{n},}}{'' if is_greedy else '?'}"


    def _at_most(self, n: int, is_greedy: bool = True) -> str:
        '''
        Applies quantifier ``{,n}`` on this instance's underlying pattern and \
        returns the resulting pattern as a string.

        :param int | None n: The maximum number of times that the provided pattern is to be matched.
        :param bool is_greedy: Determines whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to ``True``.
        '''
        if n == None:
            return self._indefinite(is_greedy)
        elif n == 0:
            return self._exactly(n)
        elif n == 1:
            return self._optional(is_greedy)
        else:
            return f"{self._quantify_conditional_group()}{{,{n}}}{'' if is_greedy else '?'}"


    def _at_least_at_most(self, min: int, max: int, is_greedy: bool = True) -> str:
        '''
        Applies quantifier ``{min,max}`` on this instance's underlying pattern and \
        returns the resulting pattern as a string.

        :param int min: The minimum number of times that the provided pattern is to be matched.
        :param int | None max: The maximum number of times that the provided pattern is to be matched.
        :param bool is_greedy: Determines whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to ``True``.
        '''
        if min == max:
            return self._exactly(min)
        elif min == 0:
            return self._at_most(max, is_greedy)
        elif max is None:
            return self._at_least(min, is_greedy)
        else:
            return f"{self._quantify_conditional_group()}{{{min},{max}}}{'' if is_greedy else '?'}"


    '''
    Operators
    '''
    def _concat(self, pre: 'Pregex') -> str:
        '''
        Concatenates the pattern of this instance with the provided pattern \
        and returns the resulting pattern as a string.

        :param Pregex pre: A ``Pregex`` instance containing the pattern on \
            the right side of the concatenation.
        '''
        return f"{self._concat_conditional_group()}{pre._concat_conditional_group()}"


    def _either(self, pre: 'Pregex') -> str:
        '''
        Applies the "alternation" operator ``|`` on this instance's underlying pattern and \
        the provided pattern, and returns the resulting pattern as a string.

        :param Pregex pre: A ``Pregex`` class instance containing the pattern on the \
            right side of the alternation.
        '''
        if pre._get_type() == _Type.Empty:
            return str(self)
        return f"{self}|{pre}"


    def _enclose(self, pre: 'Pregex') -> str:
        '''
        Concatenates the provided pattern to both the left and right side of \
        this instance's underlying pattern, and returns the resulting pattern \
        as a string.

        :param Pregex pre: A ``Pregex`` instance containing the pattern that is \
            to be concatenated to this instance's underlying pattern.
        '''
        pre = pre._concat_conditional_group()
        return f"{pre}{self._concat_conditional_group()}{pre}"

    '''
    Groups
    '''
    def _capturing_group(self, name: str = None) -> str:
        '''
        Applies a function on this instance's underlying pattern, that does the \
        following based on the nature of the pattern:
            - If pattern is not a group, then wraps it within a capturing group.
            - If pattern is a non-capturing group, then converts it to a capturing group.
            - If pattern is a capturing-group and ``name`` is the empty string, then \
                does nothing.
            - If pattern is an unnamed capturing group and ``name`` is not the empty string, \
                then assigns said name to the capturing group.
            - If pattern is a named capturing group and ``name`` is not the empty string, \
                then changes the capturing group's name to the provided name.

        Finally, returns the resulting pattern as a string.

        :param name: If this parameter is not equal to ``None``, then assigns \
            it as a name to the capturing group. Defaults to ``None``.
        '''
        if self.__type == _Type.Group:
            pattern = self.__pattern.replace('?:', '', 1) if self.__pattern.startswith('(?:') else str(self)
            if name is not None:
                if pattern.startswith('(?P'):
                    pattern = _re.sub('\(\?P<[^>]*>', f'(?P<{name}>', pattern)
                else:
                    pattern = f"(?P<{name}>{pattern[1:-1]})"
        else:
            pattern = f"({f'?P<{name}>' if name != None else ''}{self})"
        return pattern


    def _non_capturing_group(self) -> str:
        '''
        Applies a function on this instance's underlying pattern, that does the \
        following based on the nature of the pattern:
            - If pattern is not a group, then wraps it within a non-capturing group.
            - If pattern is a non-capturing group, then does nothing.
            - If pattern is a capturing-group, then converts it to a non-capturing group.

        Finally, returns the resulting pattern as a string.
        '''
        if self.__type == _Type.Group:
            if self.__pattern.startswith('(?P'):
                pattern = _re.sub('\(\?P<[^>]*>', f'(?:', str(self))
            elif not self.__pattern.startswith('(?:'):
                pattern = self.__pattern.replace('(', '(?:', 1)
            else:
                pattern = str(self)
            return pattern
        return f"(?:{self})"


    '''
    Assertions
    '''
    def _match_at_start(self) -> str:
        '''
        Applies assertion ``\A`` on this instance's underlying pattern and \
        returns the resulting pattern as a string.
        '''
        return f"\\A{self._assert_conditional_group()}"


    def _match_at_end(self) -> str:
        '''
        Applies assertion ``\Z`` on this instance's underlying pattern and \
        returns the resulting pattern as a string.
        '''
        return f"{self._assert_conditional_group()}\\Z"


    def _match_at_line_start(self) -> str:
        '''
        Applies assertion ``^`` on this instance's underlying pattern and \
        returns the resulting pattern as a string.
        '''
        return f"^{self._assert_conditional_group()}"


    def _match_at_line_end(self) -> str:
        '''
        Applies assertion ``$`` on this instance's underlying pattern and \
        returns the resulting pattern as a string.
        '''
        return f"{self._assert_conditional_group()}$"


    def _followed_by(self, pre: 'Pregex') -> str:
        '''
        Applies the "positive lookahead" assertion ``(?=pre)`` on this instance's underlying pattern \
        and returns the resulting pattern as a string.

        :param Pregex pre: The assertion pattern.
        '''
        if pre._get_type() == _Type.Empty:
            return str(self)

        return f"{self._assert_conditional_group()}(?={pre})"


    def _not_followed_by(self, pre: str) -> 'Pregex':
        '''
        Applies the "negative lookahead" assertion ``(?!pre)`` on this instance's underlying \
        pattern and returns the resulting pattern as a string.

        :param Pregex pre: The assertion pattern.
        '''
        if pre._get_type() == _Type.Empty:
            return str(self)
        return f"{self._assert_conditional_group()}(?!{pre})"


    def _preceded_by(self, pre: 'Pregex') -> str:
        '''
        Applies the "positive lookbehind" assertion ``(?<=pre)`` on this instance's underlying pattern \
        and returns the resulting pattern as a string.

        :param Pregex pre: The assertion pattern.
        '''
        if pre._get_type() == _Type.Empty:
            return str(self)
        return f"(?<={pre}){self._assert_conditional_group()}"


    def _not_preceded_by(self, pre: 'Pregex') -> str:
        '''
        Applies the "negative lookbehind" assertion ``(?<!pre)`` on this instance's underlying \
        pattern and returns the resulting pattern as a string.

        :param Pregex pre: The assertion pattern.
        '''
        if pre._get_type() == _Type.Empty:
            return str(self)
        return f"(?<!{pre}){self._assert_conditional_group()}"


    def _enclosed_by(self, pre: 'Pregex') -> str:
        '''
        Applies both the "positive lookbehind" assertion ``(?<=pre)`` and \
        "positive lookahead" assertion ``(?=pre)`` on this instance's underlying \
        pattern and returns the resulting pattern as a string.

        :param Pregex pre: The assertion pattern.
        '''
        if pre._get_type() == _Type.Empty:
            return str(self)
        return f"(?<={pre}){self._assert_conditional_group()}(?={pre})"


    def _not_enclosed_by(self, pre: 'Pregex') -> str:
        '''
        Applies both the "negative lookbehind" assertion ``(?<!pre)`` and \
        "negative lookahead" assertion ``(?!pre)`` on this instance's underlying \
        pattern and returns the resulting pattern as a string.

        :param Pregex pre: The assertion pattern.
        '''
        if pre._get_type() == _Type.Empty:
            return str(self)
        return f"(?<!{pre}){self._assert_conditional_group()}(?!{pre})"


class Empty(Pregex):
    '''
    Matches the empty string ``''``.

    :note:
        - Applying a quantifer to ``Empty`` results in ``Empty``.
        - Wrapping ``Empty`` within a group results in ``Empty``.
    '''

    def __init__(self) -> 'Empty':
        '''
        Matches the empty string ``''``.

        :note: 
            - Applying a quantifer to ``Empty`` results in ``Empty``.
            - Wrapping ``Empty`` within a group results in ``Empty``.
        '''
        super().__init__("")


    def __mul__(self, n: int) -> 'Empty':
        '''
        Returns self. \

        :param int n: Does nothing.

        :raises InvalidArgumentTypeException: Parameter ``n`` is not an integer.
        :raises InvalidArgumentValueException: Parameter ``n`` is less than zero.
        '''
        if not isinstance(n, int) or isinstance(n, bool):
            message = "Provided argument \"n\" is not an integer."
            raise _ex.InvalidArgumentTypeException(message)
        if n < 0:
            message = "Using multiplication operator with a negative integer is not allowed."
            raise _ex.InvalidArgumentValueException(message)
        return self


    def __rmul__(self, n: int) -> 'Empty':
        '''
        Returns self. \

        :param int n: Does nothing.

        :raises InvalidArgumentTypeException: Parameter ``n`` is not an integer.
        :raises InvalidArgumentValueException: Parameter ``n`` is less than zero.
        '''
        if not isinstance(n, int) or isinstance(n, bool):
            message = "Provided argument \"n\" is not an integer."
            raise _ex.InvalidArgumentTypeException(message)
        if n < 0:
            message = "Using multiplication operator with a negative integer is not allowed."
            raise _ex.InvalidArgumentValueException(message)
        return self


    def __add__(self, pre: str or Pregex) -> Pregex:
        '''
        Returns the provided string or ``Pregex`` instance as a ``Pregex`` instance.

        :param pre: The string or ``Pregex`` instance that is returned. 
        '''
        return __class__._to_pregex(pre)


    def __radd__(self, pre: str or Pregex) -> Pregex:
        '''
        Returns the provided string or ``Pregex`` instance as a ``Pregex`` instance.

        :param pre: The string or ``Pregex`` instance that is returned. 
        '''
        return __class__._to_pregex(pre)

    
    def _optional(self, is_greedy: bool = True)-> str:
        '''
        Returns self as a string.

        :param bool is_greedy: Does nothing.
        '''
        return str(self)


    def _indefinite(self, is_greedy: bool = True) -> str:
        '''
        Returns self as a string.

        :param bool is_greedy: Does nothing.
        '''
        return str(self)


    def _one_or_more(self, is_greedy: bool = True) -> str:
        '''
        Returns self as a string.

        :param bool is_greedy: Does nothing.
        '''
        return str(self)


    def _exactly(self, n: int) -> str:
        '''
        Returns self as a string.

        :param int n: Does nothing.
        '''
        return str(self)


    def _at_least(self, n: int, is_greedy: bool = True)-> str:
        '''
        Returns self as a string.

        :param int n: Does nothing.
        :param bool is_greedy: Does nothing.
        '''
        return str(self)


    def _at_most(self, n: int, is_greedy: bool = True) -> str:
        '''
        Returns self as a string.

        :param int n: Does nothing.
        :param bool is_greedy: Does nothing.
        '''
        return str(self)


    def _at_least_at_most(self, min: int, max: int, is_greedy: bool = True) -> str:
        '''
        Returns self as a string.

        :param int min: Does nothing.
        :param int max: Does nothing.
        :param bool is_greedy: Does nothing.
        '''
        return str(self)


    def _either(self, pre: 'Pregex') -> str:
        '''
        Returns 'pre' as a string.

        :param Pregex pre: The "Pregex" instance that is returned by this method.
        '''
        return str(pre)


    def _capturing_group(self, name: str = '') -> str:
        '''
        Returns self as a string.

        :param str name: Does nothing.
        '''
        return str(self)


    def _non_capturing_group(self) -> str:
        '''
        Returns self as a string.
        '''
        return str(self)
