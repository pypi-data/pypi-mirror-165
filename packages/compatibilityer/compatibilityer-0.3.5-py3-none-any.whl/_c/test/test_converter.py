# @converted by compatibilityer.convert.convert

import unittest
from compatibilityer.converter import Converter
from compatibilityer.convert import convert
import ast
from textwrap import dedent

class TestConverter(unittest.TestCase):

    def assertEqualCode(self, actual, expected):
        self.assertEqual(ast.unparse(ast.parse(actual)), ast.unparse(ast.parse(expected)))

    def test_converter(self):
        code = dedent('        from typing import TypeAlias, List\n\n        def test(a: int, b) -> list[int] | None:\n            return [a]\n        ')
        expected = dedent("        from typing import List\n\n        def test(a: 'int', b) -> 'list[int] | None':\n            return [a]\n        ")
        self.assertEqualCode(convert(code), expected)

    def test_none_import(self):
        code = dedent('        from typing import Self\n        ')
        expected = dedent('        ')
        self.assertEqualCode(convert(code), expected)

    def test_type_alias(self):
        code = dedent('        from typing import TypeAlias\n        \n        a: TypeAlias = list[int]\n\n        l: a = [1, 2, 3]\n        ')
        expected = dedent("        a: 'TypeAlias' = 'list[int]'\n\n        l: 'a' = [1, 2, 3]\n        ")
        self.assertEqualCode(convert(code), expected)

    def test_str_annotation(self):
        code = dedent("        a: 'list[int]' = [1, 2, 3]\n        ")
        expected = dedent("        a: '\\'list[int]\\'' = [1, 2, 3]\n        ")
        self.assertEqualCode(convert(code), expected)

    def test_match(self):
        pass
