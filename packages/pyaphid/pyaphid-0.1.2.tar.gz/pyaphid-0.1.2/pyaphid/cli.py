from __future__ import annotations

import ast
import os
import typing as t

import tomli
import typer

from pyaphid.analyzer import ExpandedCallCollector, Transformer, Visitor
from pyaphid.helpers import echo_with_line_ref


def pyproject():
    with open("pyproject.toml", "rb") as f:
        return tomli.load(f)


def get_pyaphid_toml_section() -> dict[str, t.Any] | None:
    pyproject_toml = pyproject()
    if "tool" in pyproject_toml:
        if "pyaphid" in pyproject_toml["tool"]:
            return pyproject_toml["tool"]["pyaphid"]
    return None


def get_forbidden_calls() -> list[str]:
    """Ger forbidden calls from pyproject.toml"""
    aphid_section = get_pyaphid_toml_section()
    if aphid_section and "forbidden" in aphid_section:
        return aphid_section["forbidden"]

    return []


def collect_python_files(files_and_dirs: list[str]):
    files: list[str] = []
    for file_or_dir in files_and_dirs:
        path = os.path.abspath(file_or_dir)
        if os.path.isfile(path) and path.endswith(".py"):
            files.append(file_or_dir)
        elif os.path.isdir(path):
            for dirpath, _, filenames in os.walk(file_or_dir, followlinks=False):
                for filename in filenames:
                    if filename.endswith(".py"):
                        files.append(f"{dirpath}/{filename}")

    return files


def main(
    files_and_dirs: list[str] = typer.Argument(
        None, show_default=False, help="Multiple files and/or directories to work with"
    ),
    # omit: bool = typer.Option(
    #    False,
    #   "--omit",
    #   "-o",
    #  rich_help_panel="Pyaphid options",
    # show_default=False,
    # help="Remove calls from falls (might destroy formatting)",
    # ),
    print_names_only: bool = typer.Option(
        False,
        "--names",
        "-n",
        rich_help_panel="Pyaphid options",
        show_default=False,
        help="Print only the expandend names of calls in files",
    ),
):
    files = collect_python_files(files_and_dirs)
    forbidden = get_forbidden_calls()
    omit = False
    exit_code = 0
    cls: type[Transformer] | type[Visitor] | type[ExpandedCallCollector]
    if print_names_only:
        cls = ExpandedCallCollector
    elif omit:
        cls = Transformer
    else:
        cls = Visitor

    for filepath in files:
        with open(filepath, "rb") as f:
            tree = ast.parse(f.read())
        visitor = cls(filepath=filepath, forbidden=forbidden)
        visitor.visit(tree)
        if isinstance(visitor, ExpandedCallCollector):
            names = visitor.calls
        else:
            names = visitor.matches
        exit_code += len(names)
        for match, expanded_call_name in names:
            echo_with_line_ref(filepath, match, expanded_call_name)

        # if omit and names:
        #    with open(filepath, "w") as f:
        #        f.write(ast.unparse(tree))

    raise typer.Exit(exit_code if not print_names_only else 0)


def run():
    typer.run(main)
