import ast

import typer


def echo_with_line_ref(filepath: str, section: ast.AST, message: str):
    filepath = filepath if filepath.startswith("/") else f"./{filepath}"
    typer.echo(f"{filepath}:{section.lineno}:{section.col_offset}: {message}")
