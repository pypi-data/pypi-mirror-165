from __future__ import annotations

import ast
from pathlib import Path


class Directory(ast.AST):
    def __init__(self, path: Path, children: list[Directory | ast.mod]):
        self.path = path
        self.children = children
        super(Directory, self).__init__(path, children)

    _fields = (
        "path",
        "children",
    )


def build_directory(path: Path) -> Directory:
    children = []
    for child in path.iterdir():
        if child.is_dir():
            children.append(build_directory(child))
        elif child.suffix == ".py":
            children.append(ast.parse(child.read_text()))
    return Directory(path, children)
