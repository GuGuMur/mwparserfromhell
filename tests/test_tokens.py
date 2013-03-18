# -*- coding: utf-8  -*-
#
# Copyright (C) 2012-2013 Ben Kurtovic <ben.kurtovic@verizon.net>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import unicode_literals
import unittest

from mwparserfromhell.compat import py3k
from mwparserfromhell.parser import tokens

class TestTokens(unittest.TestCase):
    """Test cases for the Token class and its subclasses."""

    def test_issubclass(self):
        """check that all classes within the tokens module are really Tokens"""
        for name in tokens.__all__:
            klass = getattr(tokens, name)
            self.assertTrue(issubclass(klass, tokens.Token))
            self.assertIsInstance(klass(), klass)
            self.assertIsInstance(klass(), tokens.Token)

    def test_attributes(self):
        """check that Token attributes can be managed properly"""
        token1 = tokens.Token()
        token2 = tokens.Token(foo="bar", baz=123)

        self.assertEquals("bar", token2.foo)
        self.assertEquals(123, token2.baz)
        self.assertRaises(KeyError, lambda: token1.foo)
        self.assertRaises(KeyError, lambda: token2.bar)

        token1.spam = "eggs"
        token2.foo = "ham"
        del token2.baz

        self.assertEquals("eggs", token1.spam)
        self.assertEquals("ham", token2.foo)
        self.assertRaises(KeyError, lambda: token2.baz)
        self.assertRaises(KeyError, delattr, token2, "baz")

    def test_repr(self):
        """check that repr() on a Token works as expected"""
        token1 = tokens.Token()
        token2 = tokens.Token(foo="bar", baz=123)
        token3 = tokens.Text(text="earwig" * 100)
        hundredchars = ("earwig" * 100)[:97] + "..."

        self.assertEquals("Token()", repr(token1))
        if py3k:
            token2repr = "Token(foo='bar', baz=123)"
            token3repr = "Text(text='" + hundredchars + "')"
        else:
            token2repr = "Token(foo=u'bar', baz=123)"
            token3repr = "Text(text=u'" + hundredchars + "')"
        self.assertEquals(token2repr, repr(token2))
        self.assertEquals(token3repr, repr(token3))

    def test_equality(self):
        """check that equivalent tokens are considered equal"""
        token1 = tokens.Token()
        token2 = tokens.Token()
        token3 = tokens.Token(foo="bar", baz=123)
        token4 = tokens.Text(text="asdf")
        token5 = tokens.Text(text="asdf")
        token6 = tokens.TemplateOpen(text="asdf")

        self.assertEquals(token1, token2)
        self.assertEquals(token2, token1)
        self.assertEquals(token4, token5)
        self.assertEquals(token5, token4)
        self.assertNotEquals(token1, token3)
        self.assertNotEquals(token2, token3)
        self.assertNotEquals(token4, token6)
        self.assertNotEquals(token5, token6)

    def test_repr_equality(self):
        "check that eval(repr(token)) == token"
        tests = [
            tokens.Token(),
            tokens.Token(foo="bar", baz=123),
            tokens.Text(text="earwig")
        ]
        for token in tests:
            self.assertEquals(token, eval(repr(token), vars(tokens)))

if __name__ == "__main__":
    unittest.main(verbosity=2)
