from __future__ import annotations

import abc
import ast
import typing as t

from pyaphid.helpers import echo_with_line_ref


class ImportFrom(t.NamedTuple):
    value: ast.ImportFrom
    import_string: str
    alias: str | None


class Import(t.NamedTuple):
    value: ast.Import
    import_string: str
    alias: str | None


class CallMatch(t.NamedTuple):
    call: ast.Call
    match: str


def get_call_signature(call: ast.Call) -> tuple[str, str]:
    basename = ""
    path = ""
    if isinstance(call.func, ast.Attribute):
        basename = call.func.attr
        call_func = call.func.value
        while isinstance(call_func, ast.Attribute):
            path = f".{call_func.attr}{path}"
            call_func = call_func.value

        if isinstance(call_func, ast.Name):
            path = call_func.id + path
        elif isinstance(call_func, ast.Call):
            sub_path, sub_basename = get_call_signature(call_func)
            path = f"{sub_path}.{sub_basename}(){path}"

    elif isinstance(call.func, ast.Name):
        basename = call.func.id

    return (path, basename)


def replace_alias(import_: ImportFrom | Import, path: str):
    if import_.alias and (path == import_.alias or path.startswith(import_.alias)):
        return path.replace(import_.alias, import_.import_string, 1)
    return path


def expand_call(call: ast.Call, imports: list[Import], import_froms: list[ImportFrom]):
    """
    Expand call with the matching import string.
    If the call does not match an import and is not a built-in function, None is returned
    """
    (path, basename) = get_call_signature(call)
    if "(" in path or ")" in path:
        return None
    work_path = path
    if path:
        for import_ in reversed(imports):
            work_path = replace_alias(import_, work_path)
            if work_path == import_.import_string or work_path.startswith(
                f"{import_.import_string}."
            ):
                return f"{work_path}.{basename}"
            work_path = path
    for import_from in reversed(import_froms):
        imported_name: str = import_from.import_string.rsplit(".", 1)[1]
        if path:
            work_path = replace_alias(import_from, work_path)
            if work_path == imported_name or work_path.startswith(f"{imported_name}."):
                return f"{work_path.replace(imported_name, import_from.import_string, 1)}.{basename}"  # noqa: E501
        elif (
            import_from.alias
            and basename == import_from.alias
            or imported_name == basename
        ):
            return import_from.import_string
    return basename if not path and basename in __builtins__ else None  # type: ignore


_FuncDef = t.TypeVar(
    "_FuncDef", bound="ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef"
)


class ImportsTracker(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        self.import_froms: list[ImportFrom] = []
        self.imports: list[Import] = []

    @abc.abstractmethod
    def generic_visit(self, node: ast.AST) -> t.Any:
        pass

    def new_import_context(self, node: _FuncDef) -> _FuncDef:
        old_imports = self.imports.copy()
        old_import_froms = self.import_froms.copy()
        self.generic_visit(node)
        self.imports = old_imports
        self.import_froms = old_import_froms
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        return self.new_import_context(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        return self.new_import_context(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        return self.new_import_context(node)

    def visit_Import(self, node: ast.Import):
        for name in node.names:
            self.imports.append(Import(node, name.name, name.asname))
        return node

    def visit_ImportFrom(self, node: ast.ImportFrom) -> ast.ImportFrom:
        for name in node.names:
            self.import_froms.append(
                ImportFrom(node, f"{node.module}.{name.name}", name.asname)
            )
        return node


class ExpandedCallCollector(ast.NodeVisitor, ImportsTracker):
    def __init__(self, *args, **kw) -> None:
        self.calls: list[CallMatch] = []
        return super().__init__()

    def visit_Call(self, node: ast.Call) -> None:
        expanded_call_signature = expand_call(node, self.imports, self.import_froms)
        if expanded_call_signature and expanded_call_signature not in map(
            lambda call: call.match, self.calls
        ):
            self.calls.append(CallMatch(node, expanded_call_signature))


class VisitorMixIn(ImportsTracker):
    def __init__(self, filepath: str, forbidden: list[str]) -> None:
        self.filepath = filepath
        self.forbidden = forbidden
        self.ignored_forbidden: list[list[str]] = []
        self.matches: list[CallMatch] = []
        return super().__init__()

    def is_forbidden(self, signature: str):
        for pattern in self.forbidden:
            if pattern.endswith(".*") and signature.startswith(
                pattern.rsplit(".", 1)[0]
            ):
                return True
            elif signature == pattern:
                return True
        return False

    def _ignore_forbidden_assignment(self, target: ast.Name):
        self.forbidden.remove(target.id)
        if self.ignored_forbidden:
            self.ignored_forbidden[-1].append(target.id)
        echo_with_line_ref(
            self.filepath,
            target,
            f"Assignment of {target.id} collides with forbidden built-in. Calls to it will be ignored within its scope",  # noqa: E501
        )

    def visit_Assign(self, node: ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id in self.forbidden:
                self._ignore_forbidden_assignment(target)

        return node

    def visit_AnnAssign(self, node: ast.AnnAssign):
        if isinstance(node.target, ast.Name) and node.target.id in self.forbidden:
            self._ignore_forbidden_assignment(node.target)

        return node

    def new_import_context(self, node: _FuncDef) -> _FuncDef:
        if node.name in self.forbidden:
            self.forbidden.remove(node.name)
            echo_with_line_ref(
                self.filepath,
                node,
                f"Local definition  of {node.name} collides with forbidden built-in. {node.name} calls will be ignored for the rest of the file",  # noqa: E501
            )
        return super().new_import_context(node)

    def visit_Call(self, node: ast.Call) -> ast.Call | None:
        expanded_call_signature = expand_call(node, self.imports, self.import_froms)
        if expanded_call_signature and self.is_forbidden(expanded_call_signature):
            self.matches.append(CallMatch(node, expanded_call_signature))
            return None
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        self.ignored_forbidden.append([])
        super().visit_FunctionDef(node)
        self.forbidden += self.ignored_forbidden.pop()
        return node

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.ignored_forbidden.append([])
        super().visit_AsyncFunctionDef(node)
        self.forbidden += self.ignored_forbidden.pop()
        return node


class Visitor(ast.NodeVisitor, VisitorMixIn):
    pass


class Transformer(ast.NodeTransformer, VisitorMixIn):
    pass
