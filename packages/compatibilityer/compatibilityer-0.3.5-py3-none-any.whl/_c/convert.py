# @converted by compatibilityer.convert.convert

from typing import Type
from compatibilityer.converter import Converter
import ast
from pathlib import Path
HEAD = '# @converted by compatibilityer.convert.convert\n\n'

def convert_ast(node: 'ast.AST', converter: 'Type[Converter]'=Converter) -> 'ast.AST':
    return converter().visit(node)

def convert(code: 'str', converter: 'Type[Converter]'=Converter) -> 'str':
    node = ast.parse(code)
    return ast.unparse(convert_ast(node, converter))

def convert_file(code: 'str', converter: 'Type[Converter]'=Converter, head: 'str'=HEAD) -> 'str':
    return head + convert(code, converter)

def convert_dir(dir_: 'Path', converter: 'Type[Converter]'=Converter, head: 'str'=HEAD) -> 'None':
    assert dir_.is_dir()
    for file in dir_.glob('**/*.py'):
        with open(file, 'r') as f:
            c = f.read()
        with open(file, 'w') as f:
            nc = convert_file(c, converter, head)
            f.write(nc)