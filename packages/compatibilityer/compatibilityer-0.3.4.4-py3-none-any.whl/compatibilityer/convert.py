from typing import Type

from compatibilityer.converter import Converter

import ast
from pathlib import Path
import subprocess


HEAD = """\
# @converted by compatibilityer

"""


def convert_ast(node: ast.AST, converter: Type[Converter] = Converter) -> ast.AST:
    return converter().visit(node)


def convert(code: str, converter: Type[Converter] = Converter) -> str:
    node = ast.parse(code)
    return ast.unparse(convert_ast(node, converter))


def convert_file(code: str, converter: Type[Converter] = Converter, head: str = HEAD) -> str:
    return head + convert(code, converter)


def convert_dir(dir_: Path, converter: Type[Converter] = Converter, head: str = HEAD) -> None:
    assert dir_.is_dir()
    for file in dir_.glob('**/*.py'):
        with open(file, "r") as f:
            c = f.read()
        with open(file, "w") as f:
            nc = convert_file(c, converter, head)
            f.write(nc)


def convert_dir_with_copy(dir_: Path, output_dir: Path, converter: Type[Converter] = Converter, head: str = HEAD) -> None:
    excludes = []

    if output_dir in dir_.glob("**/*"):
        excludes.append(output_dir)

    excludes = ["--exclude", *map(str, excludes)] if excludes else []

    subprocess.run(["rsync", "-a", dir_, output_dir, *excludes], check=True)
    convert_dir(output_dir, converter, head)
