import unittest

from compatibilityer.converter import Converter
from compatibilityer.convert import convert

import ast
from textwrap import dedent


class TestConverter(unittest.TestCase):
    def assertEqualCode(self, actual, expected):
        self.assertEqual(ast.unparse(ast.parse(actual)), ast.unparse(ast.parse(expected)))

    def test_converter(self):
        code = dedent("""\
        from typing import TypeAlias, List

        def test(a: int, b) -> list[int] | None:
            return [a]
        """)
        expected = dedent("""\
        from typing import List

        def test(a: 'int', b) -> 'list[int] | None':
            return [a]
        """)

        self.assertEqualCode(convert(code), expected)

    def test_none_import(self):
        code = dedent("""\
        from typing import Self
        """)
        expected = dedent("""\
        """)  # None

        self.assertEqualCode(convert(code), expected)

    def test_type_alias(self):
        code = dedent("""\
        from typing import TypeAlias
        
        a: TypeAlias = list[int]

        l: a = [1, 2, 3]
        """)
        expected = dedent("""\
        a: 'TypeAlias' = 'list[int]'

        l: 'a' = [1, 2, 3]
        """)

        self.assertEqualCode(convert(code), expected)

    def test_str_annotation(self):
        code = dedent("""\
        a: 'list[int]' = [1, 2, 3]
        """)
        expected = dedent("""\
        a: '\\'list[int]\\'' = [1, 2, 3]
        """)

        self.assertEqualCode(convert(code), expected)

    def test_match(self):
        code = dedent("""\
        a = 3
        match a:
            case 1:
                print(1)
            case 2:
                print(2)
            case x if x <= 5:
                print("o", x)
            case _:
                print("other")
        """)
        expected = dedent("""\
        a = 3
        if (__match_target := a) and False:
            pass
        elif __match_target == 1:
            print(1)
        elif __match_target == 2:
            print(2)
        elif ((x := __match_target) or True) and x <= 5:
            print('o', x)
        elif ((_ := __match_target) or True):
            print('other')
        else:
            pass
        """)

        self.assertEqualCode(convert(code), expected)
