from __future__ import annotations

from typing import cast

import ast


class Converter(ast.NodeTransformer):
    target_version = (3, 8, 0)
    invalid_typing_names = (
        # 3.11
        "Self",
        "Unpack",
        # 3.10
        "TypeAlias",
        "Concatenate",
        "TypeGuard",
        "ParamSpec",
        "ParamSpecKwargs",
        "is_typeddict",  # function
        # 3.9
        "Annotated",
    )

    def convert_type_annotation(self, node: ast.expr | None) -> ast.expr | None:
        if node is None:
            return None
        return cast(ast.expr, ast.Constant(ast.unparse(node)))

    def visit_ImportFrom(self, node: ast.ImportFrom) -> ast.ImportFrom:
        node = cast(ast.ImportFrom, self.generic_visit(node))

        res = node
        if node.module == "typing":
            names = []
            for alias in node.names:
                if alias.name in self.invalid_typing_names:
                    continue
                names.append(alias)

            if not names:
                res = None
            else:
                res = ast.ImportFrom("typing", names, node.level)

        return res

    def visit_AnnAssign(self, node: ast.AnnAssign) -> ast.AnnAssign:
        node = cast(ast.AnnAssign, self.generic_visit(node))

        node.annotation = self.convert_type_annotation(node.annotation)

        if node.annotation.value == "TypeAlias":
            node.value = self.convert_type_annotation(node.value)

        return node

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        node = cast(ast.FunctionDef, self.generic_visit(node))

        node.returns = self.convert_type_annotation(node.returns)
        return node

    def visit_arg(self, node: ast.arg) -> ast.arg:
        node = cast(ast.arg, self.generic_visit(node))

        node.annotation = self.convert_type_annotation(node.annotation)
        return node

    def visit_Match(self, node: ast.Match) -> ast.If:
        node = cast(ast.Match, self.generic_visit(node))

        target = "__match_target"

        last = ast.If()
        res = ast.If(ast.BoolOp(ast.And(), [
            ast.NamedExpr(ast.Name(target), node.subject),
            ast.Constant(False),
        ]), [ast.Pass()], [last])

        for i, case in enumerate(node.cases):
            test = self.convert_pattern(case.pattern, ast.Name(target))
            if case.guard is not None:
                test = ast.BoolOp(ast.And(), [test, self.visit(case.guard)])
            body = [self.visit(s) for s in case.body]

            last.test = test
            last.body = body

            new_last = ast.If() if i < len(node.cases) - 1 else ast.Pass()
            last.orelse = [new_last]
            last = new_last

        return res

    def convert_pattern(self, node: ast.pattern, target: ast.expr):
        node = self.visit(node)
        func = getattr(self, "convert_" + node.__class__.__name__)
        return func(node, target)

    def convert_MatchValue(self, node: ast.MatchValue, target: ast.expr) -> ast.expr:
        return ast.Compare(
            target,
            [ast.Eq()],
            [node.value],
        )

    def convert_MatchSingleton(self, node: ast.MatchSingleton, target: ast.expr) -> ast.expr:
        return ast.Compare(
            target,
            [ast.Eq()],
            [ast.Constant(node.value)],
        )

    def convert_MatchSequence(self, node: ast.MatchSequence, target: ast.expr) -> ast.expr:
        # ToDo: support MatchSequence
        raise NotImplementedError()

    def convert_MatchStar(self, node: ast.MatchStar, target: ast.expr) -> ast.expr:
        # ToDo: support MatchStar
        raise NotImplementedError()

    def convert_MatchMapping(self, node: ast.MatchMapping, target: ast.expr) -> ast.expr:
        # ToDo: support MatchMapping
        raise NotImplementedError()

    def convert_MatchClass(self, node: ast.MatchClass, target: ast.expr) -> ast.expr:
        # ToDo: support __match_args__
        if node.patterns:
            raise NotImplementedError()

        terms = [ast.Call(
            ast.Name("isinstance"),
            [target, node.cls],
        )]
        for i in range(len(node.kwd_attrs)):
            terms.append(self.convert_pattern(node.kwd_patterns[i], ast.Attribute(target, node.kwd_attrs[i])))
        return ast.BoolOp(ast.And(), terms)

    def convert_MatchAs(self, node: ast.MatchAs, target: ast.expr) -> ast.expr:
        # ToDo: support MatchAs with pattern
        if node.pattern is not None:
            raise NotImplementedError()

        name = node.name if node.name is not None else "_"

        return ast.BoolOp(ast.Or(), [ast.NamedExpr(ast.Name(name), target), ast.Constant(True)])

    def convert_MatchOr(self, node: ast.MatchOr, target: ast.expr) -> ast.expr:
        return ast.BoolOp(ast.Or(), [self.convert_pattern(p, target) for p in node.patterns])
