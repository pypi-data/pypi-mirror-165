#!/usr/bin/env python


import pytest

from re_patterns import Rstr


def test_add():
    assert Rstr("hello") + Rstr("world") == "helloworld"
    assert Rstr("hello") + "world" == "helloworld"
    assert "hello" + Rstr("world") == "helloworld"


def test_named():
    r = Rstr("this").named("group_name")
    assert r == "(?P<group_name>this)"


def test_named_optional():
    r = Rstr("this").named("group_name", optional=True)
    assert r == "(?P<group_name>this)?"


def test_followed_by():
    r = Rstr("this").followed_by("that")
    assert r == "this(?=that)"


def test_not_followed_by():
    r = Rstr("this").not_followed_by("that")
    assert r == "this(?!that)"


def test_preceded_by():
    r = Rstr("this").preceded_by("that")
    assert r == "(?<=that)this"


def test_not_preceded_by():
    r = Rstr("this").not_preceded_by("that")
    assert r == "(?<!that)this"


def test_no_capture():
    r = Rstr("this").no_capture()
    assert r == "(?:this)"


def test_group():
    r = Rstr("this").group()
    assert r == "[this]"


def test_unnamed():
    r = Rstr("this").unnamed()
    assert r == "(this)"


def test_unnamed_optional():
    r = Rstr("this").unnamed(optional=True)
    assert r == "(this)?"


def test_comment():
    r = Rstr("this").comment()
    assert r == "(?#this)"


def test_append():
    r = Rstr("this").append("that")
    assert r == "thisthat"


def test_prepend():
    r = Rstr("this").prepend("that")
    assert r == "thatthis"


def test_join():
    r = Rstr("this").join("that", "something", "other")
    assert r == "thisthatsomethingother"


def test_or():
    assert "this|that" == Rstr("this") | Rstr("that")
    assert "this|that" == Rstr("this") | "that"
    with pytest.raises(TypeError, match=r"unsupported operand type\(s\)"):
        "this" | Rstr("that")


def test_compile():
    r = Rstr(r"this.\n").compile(Rstr.re.DOTALL | Rstr.re.MULTILINE)
    assert r == Rstr.re.compile(r"this.\n", flags=Rstr.re.DOTALL | Rstr.re.MULTILINE)


def test_match():
    m = Rstr(r"this.\n").match("this\n\n", flags=Rstr.re.DOTALL)
    assert m.span() == (0, 6)
    # Note that even in MULTILINE mode, re.match() will only match
    # at the beginning of the string and not at the beginning of each line
    m = Rstr(r"^this.$").match("this\n\n", flags=Rstr.re.DOTALL | Rstr.re.MULTILINE)
    assert m.span() == (0, 5)
    m = Rstr(r"^this.$").match("\nthis\n\n", flags=Rstr.re.DOTALL | Rstr.re.MULTILINE)
    assert m is None


def test_search():
    m = Rstr(r"^this.$").search("\n\nthis\n\n", flags=Rstr.re.DOTALL | Rstr.re.MULTILINE)
    assert m.span() == (2, 7)


def test_finditer():
    s = "this\nthat\nyon\nit"
    r = Rstr(".*[ai][st]")
    it = r.finditer(s)
    assert next(it).span() == (0, 4)
    assert next(it).span() == (5, 9)
    assert next(it).span() == (14, 16)
    with pytest.raises(StopIteration):
        next(it)


def test_findall():
    s = "this\nthat\nyon\nit"
    r = Rstr(".*[ai][st]")
    r.findall(s) == ["this", "that", "it"]


def test_print_out():
    r = Rstr(r"\\\\nthat\\n")
    pattern = r.print_out()
    assert pattern == r"\\nthat\n"
