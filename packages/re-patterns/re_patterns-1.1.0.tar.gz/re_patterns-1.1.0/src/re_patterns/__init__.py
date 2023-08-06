#!/usr/bin/env python


"""
Compose regular expression using human-friendly methods
"""


from __future__ import annotations

import re

__pdoc__ = {}


class Rstr(str):
    """
    Subclass of str which adds methods for composing regex patterns
    """

    re = re
    """
    `Rstr` contains a reference to the standard library's `re` module.
    It is not necessary to import `re` separately, you can access it under `Rstr.re`, e.g.
    `Rstr.re.DOTALL`
    """

    def __add__(self, other) -> Rstr:
        """
        Adds `Rstr` or str instances, e.g.:
        ```python
        >>> Rstr("hello") + Rstr(" ") + Rstr("world")
        'hello world'
        >>> Rstr("Hello,") + " Dolly!"
        'Hello, Dolly!'
        ```
        """
        return Rstr(
            "".join(
                (self, other),
            )
        )

    def named(self, name: str, optional: bool = False) -> Rstr:
        """
        Adds the named group syntax around `self`, e.g.:
        ```python
        >>> Rstr(r"\\w+").named("kind_of_cheese") + " cheese"
        '(?P<kind_of_cheese>\\w+) cheese'
        ```
        You can set `optional` to `True` to add the quantifier `?`, e.g.
        ```python
        >>> Rstr("quarterpounder") + \\
        ... Rstr(" with cheese").named("extra", optional=True)
        'quarterpounder(?P<extra> with cheese)?'
        ```
        """
        result = Rstr(r"".join((name.join((r"(?P<", r">")), self, r")")))
        if optional:
            return result.append(r"?")
        return result

    def followed_by(self, following: str) -> Rstr:
        """
        Extends `self` by the _followed-by_ syntax around `following`, e.g.:
        ```python
        >>> Rstr("Isaac ").followed_by("Asimov")
        'Isaac (?=Asimov)'
        ```
        """
        return Rstr("".join((self, following.join((r"(?=", r")")))))

    def not_followed_by(self, following: str) -> Rstr:
        """
        Extends `self` by the _not-followed-by_ syntax around `following`, e.g.:
        ```python
        >>> Rstr("Isaac ").not_followed_by("Asimov")
        'Isaac (?!Asimov)'
        ```
        """
        return Rstr("".join((self, following.join((r"(?!", r")")))))

    def preceded_by(self, precedent: str) -> Rstr:
        """
        Extends `self` by the _preceded-by_ syntax around `precedent`, e.g.:
        ```python
        >>> Rstr("chat").preceded_by("chit")
        '(?<=chit)chat'
        ```
        """
        return Rstr("".join((precedent.join((r"(?<=", r")")), self)))

    def not_preceded_by(self, precedent: str) -> Rstr:
        """
        Extends `self` by the _not-preceded-by_ syntax around `precedent`, e.g.:
        ```python
        >>> Rstr("chat").not_preceded_by("chit")
        '(?<!chit)chat'
        ```
        """
        return Rstr("".join((precedent.join((r"(?<!", r")")), self)))

    def no_capture(self) -> Rstr:
        """
        Surrounds `self` by the _no-capture_ syntax, e.g.:
        ```python
        >>> Rstr("word").no_capture()
        '(?:word)'
        ```
        """
        return Rstr("".join((r"(?:", self, r")")))

    def group(self) -> Rstr:
        """
        Surrounds `self` in group brackets, e.g.:
        ```python
        >>> Rstr("0-9a-f").group()
        '[0-9a-f]'
        ```
        """
        return Rstr("".join((r"[", self, r"]")))

    def unnamed(self, optional: bool = False) -> Rstr:
        """
        Puts `self` in the capture-group brackets, e.g.:
        ```python
        >>> Rstr("pretty").unnamed() + " woman"
        '(pretty) woman'
        ```
        You can set `optional` to `True` to add the quantifier `?`, e.g.
        ```python
        >>> Rstr("quarterpounder") + \\
        ... Rstr(" with cheese").unnamed(optional=True)
        'quarterpounder( with cheese)?'
        ```
        """
        result = Rstr("".join((r"(", self, r")")))
        if optional:
            return result.append(r"?")
        return result

    def comment(self) -> Rstr:
        """
        Surrounds `self` by the _comment_ syntax, e.g.:
        ```python
        >>> Rstr("important note").comment()
        '(?#important note)'
        ```
        """
        return Rstr("".join((r"(?#", self, r")")))

    def append(self, appendix: str) -> Rstr:
        """
        Concatenates an `Rstr` with other following `Rstr` or `str`, e.g.
        ```python
        >>> Rstr("pretty").append(" little").append(Rstr(" angel"))
        'pretty little angel'
        ```
        """
        return Rstr("".join((self, appendix)))

    def prepend(self, prependix: str) -> Rstr:
        """
        Concatenates an `Rstr` with other preceding `Rstr` or `str`, e.g.
        ```python
        >>> Rstr("Party").prepend("Expected ").prepend("A Long-")
        'A Long-Expected Party'
        ```
        """
        return Rstr("".join((prependix, self)))

    def join(self, *args, **kwargs) -> Rstr:
        """
        Convenience function to compose an `Rstr` from multiple parts, e.g.:
        ```python
        >>> Rstr("").join(
        ...     Rstr(r"\\d{1,3}").named("degrees"),
        ...     "°",
        ...     " ",
        ...     Rstr(r"\\d{1,2}").named("minutes"),
        ...     "'",
        ...     " ",
        ...     Rstr(r"\\d{1,2}").named("seconds"),
        ...     '"',
        ...     " ",
        ...     Rstr("NESW").group().named("direction"),
        ... ).named("coordinates")
        '(?P<coordinates>(?P<degrees>\\d{1,3})° (?P<minutes>\\d{1,2})\\' (?P<seconds>\\d{1,2})" (?P<direction>[NESW]))'
        ```
        """
        return Rstr(
            "".join(
                (
                    self,
                    *args,
                ),
                **kwargs,
            )
        )

    def __or__(self, other) -> Rstr:
        """
        Joins an `Rstr` instance with another `Rstr` or `str` using the `|` operator, e.g.
        ```python
        >>> (Rstr("cyan") | "magenta" | "yellow" | "black").named("cmyk")
        '(?P<cmyk>cyan|magenta|yellow|black)'
        ```
        """
        return Rstr(
            "|".join(
                (self, other),
            )
        )

    def compile(self, *args, **kwargs) -> re.Pattern:
        """
        Proxy for `re.compile`
        ```python
        >>> Rstr(r"\\d{4}").compile()
        re.compile('\\\\d{4}')
        ```
        You can forward any additional arguments or keyword arguments, e.g.:
        >>> Rstr.compile("<head>.*</head>", Rstr.re.DOTALL)
        """
        return re.compile(self, *args, **kwargs)

    def match(self, *args, **kwargs) -> re.Match:
        """
        Proxy for `re`'s `re.match`
        ```python
        >>> Rstr(r"\\d{4}").named("year").match("2022-08-30")
        <re.Match object; span=(0, 4), match='2022'>
        >>> Rstr(r"\\d{4}").named("year").match("2022-08-30").group("year")
        '2022'
        ```
        You can also use any additional arguments or keyword arguments, e.g.:
        ```
        >>> text = "MeRrY cHrIStmAS"
        >>> Rstr.match("merry christmas", text, Rstr.re.IGNORECASE)
        <re.Match object; span=(0, 15), match='MeRrY cHrIStmAS'>
        ```
        """
        return re.match(self, *args, **kwargs)

    def search(self, *args, **kwargs) -> re.Match:
        """
        Proxy for `re`'s `re.search`
        ```python
        >>> day = Rstr(r"\\d{2}").named("day").\\
        ...     preceded_by("-").\\
        ...     not_followed_by("-")
        >>> day.search("2022-08-30")
        <re.Match object; span=(8, 10), match='30'>
        >>> day.search("2022-08-30").group("day")
        '30'
        ```
        """
        return re.search(self, *args, **kwargs)

    def finditer(self, *args, **kwargs) -> Iterable[re.Match]:
        """
        Proxy for `re`'s `re.finditer`
        ```python
        >>> utterance = "It is what it is, isn't it?"
        >>> matches = Rstr.finditer("it", utterance, Rstr.re.IGNORECASE)
        >>> next(matches)
        <re.Match object; span=(0, 2), match='It'>
        >>> next(matches)
        <re.Match object; span=(11, 13), match='it'>
        >>> next(matches)
        <re.Match object; span=(24, 26), match='it'>
        ```
        """
        return re.finditer(self, *args, **kwargs)

    def findall(self, *args, **kwargs) -> list[str]:
        """
        Proxy for `re`'s `re.findall`
        ```python
        >>> species = ("felis silvestris",
        ...     "panthera leo",
        ...     "tegenaria silvestris",
        ...     "bubo bubo",
        ...     "pinus sylvestris")
        >>> pattern = Rstr(r"\\w+").named("genus").followed_by(" s[yi]lvestris")
        >>> pattern.findall(", ".join((species)))
        ['felis', 'tegenaria', 'pinus']
        ```
        """
        return re.findall(self.compile(), *args, **kwargs)

    def print_out(self) -> str:
        """
        .. deprecated:: 1.0.1, present for compatibility reasons
        If you need to see a copy-pastable regex string with unescaped backslashes,
        use the built-in `print` function.
        ```python
        >>> artist_duo = Rstr.join(
        ...     Rstr(r"\\w+").named("first"),
        ...     " ",
        ...     Rstr("and|&").named("conjunctor"),
        ...     " ",
        ...     Rstr(r"\\w+").named("second"),
        ... ).named("duo")
        >>> print(artist_duo)
        (?P<duo>(?P<first>\\w+) (?P<conjunctor>and|&) (?P<second>\\w+))
        ```
        """
        return self.compile().pattern.replace("\\\\", "\\")

    as_group = group
    as_comment = comment
    capture_group = unnamed


__pdoc__["Rstr.__add__"] = True
__pdoc__["Rstr.__or__"] = True
