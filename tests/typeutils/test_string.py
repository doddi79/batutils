import unittest
from batutils.tpu import string as typeutils_string
import json
import os


class StringTests(unittest.TestCase):
    def test_dequote(self):
        self.assertEqual('foo', typeutils_string.dequote('"foo"'))
        self.assertEqual('foo', typeutils_string.dequote("'foo'"))
        self.assertEqual('foo', typeutils_string.dequote('foo'))

        self.assertEqual('foo bar', typeutils_string.dequote('"foo bar"'))
        self.assertEqual('foo bar', typeutils_string.dequote("'foo bar'"))
        self.assertEqual('foo bar', typeutils_string.dequote('foo bar'))

        self.assertEqual('', typeutils_string.dequote(''))
        self.assertEqual('', typeutils_string.dequote('""'))
        self.assertEqual('', typeutils_string.dequote("''"))

        self.assertEqual('"foo bar', typeutils_string.dequote('"foo bar'))
        self.assertEqual('foo"', typeutils_string.dequote('foo"'))
        self.assertEqual('"foo\'', typeutils_string.dequote('"foo\''))
        self.assertEqual('\'foo"', typeutils_string.dequote('\'foo"'))

        self.assertEqual('foo$bar', typeutils_string.dequote('$foo$bar$', '$'))
        self.assertEqual('foo$bar', typeutils_string.dequote('#foo$bar#', ['$', '#']))
        self.assertEqual('foo#bar', typeutils_string.dequote('#foo#bar#', ['$', '#']))
        self.assertEqual('"foo"', typeutils_string.dequote('"foo"', ['$', '#']))

        self.assertIsNone(typeutils_string.dequote(None))
        self.assertEqual(42, typeutils_string.dequote(42))
