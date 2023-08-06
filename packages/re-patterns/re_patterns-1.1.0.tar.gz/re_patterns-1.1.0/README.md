# re_patterns

python regular expressions for humans

## Description

This module helps you build complex regular expressions.

## Usage

Example:
```
>>> from re_patterns import Rstr

>>> regex = Rstr("Isaac").not_followed_by("Newton").named("non_newtonians")
>>> regex
'(?P<non-newtonians>Isaac(?!Newton))'
>>> match = regex.search("Isaac Lobkowicz, Isaac Newton")
>>> match.span()
(0, 5)
>>> match.group("non_newtonians")
'Isaac'
```

For further uses please look at the methods of the `Rstr` class in `__init__.py`.
