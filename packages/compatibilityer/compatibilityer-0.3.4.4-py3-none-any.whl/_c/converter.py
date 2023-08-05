# @converted by compatibilityer.convert.convert

from __future__ import annotations
from typing import cast
import ast

class Converter(ast.NodeTransformer):
    target_version = (3, 8, 0)
    invalid_typing_names = ('Self', 'Unpack', 'TypeAlias', 'Concatenate', 'TypeGuard', 'ParamSpec', 'ParamSpecKwargs', 'is_typeddict', 'Annotated')

    def convert_type_annotation(self, node: 'ast.expr | None') -> 'ast.expr | None':
        if node is None:
            return None
        return cast(ast.expr, ast.Constant(ast.unparse(node)))

    def visit_ImportFrom(self, node: 'ast.ImportFrom') -> 'ast.ImportFrom':
        node = cast(ast.ImportFrom, self.generic_visit(node))
        res = node
        if node.module == 'typing':
            names = []
            for alias in node.names:
                if alias.name in self.invalid_typing_names:
                    continue
                names.append(alias)
            if not names:
                res = None
            else:
                res = ast.ImportFrom('typing', names, node.level)
        return res

    def visit_AnnAssign(self, node: 'ast.AnnAssign') -> 'ast.AnnAssign':
        node = cast(ast.AnnAssign, self.generic_visit(node))
        node.annotation = self.convert_type_annotation(node.annotation)
        if node.annotation.value == 'TypeAlias':
            node.value = self.convert_type_annotation(node.value)
        return node

    def visit_FunctionDef(self, node: 'ast.FunctionDef') -> 'ast.FunctionDef':
        node = cast(ast.FunctionDef, self.generic_visit(node))
        node.returns = self.convert_type_annotation(node.returns)
        return node

    def visit_arg(self, node: 'ast.arg') -> 'ast.arg':
        node = cast(ast.arg, self.generic_visit(node))
        node.annotation = self.convert_type_annotation(node.annotation)
        return node