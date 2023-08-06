from __future__ import annotations

import ast
from typing import Any

from ast import *
from enum import IntEnum, auto
import sys
from contextlib import contextmanager, nullcontext
from abc import ABC
import builtins
from collections import Counter
from collections.abc import Iterable


def flatten(it):
    for x in it:
        if isinstance(x, Iterable):
            yield from flatten(x)
        else:
            yield x


class Variable:
    _instances: dict[str, Variable] = {}

    def __new__(cls, name: str):
        if name in cls._instances:
            return cls._instances[name]
        else:
            return super().__new__(cls)

    def __init__(self, name: str):
        self.name = name

    def __hash__(self):
        return hash(self.name)


class Function:
    def __init__(self, name: str):
        self.name = name
        self.variables_uses_num: Counter[Variable] = Counter()
        self.local_variables: set[Variable] = set()
        self.global_variables: set[Variable] = set()  # global or nonlocal


class VariableSearcher(NodeVisitor):
    def __init__(self, excluded_names: set[str], builtin_names: set[str] = None):
        if builtin_names is None:
            builtin_names = set(builtins.__dict__.keys())

        self.excluded_names = excluded_names
        self.builtin_names = builtin_names

        self.all_funcs: list[Function] = []
        self.func_stack: list[Function] = []

        self.toplevel_variables: Counter[Variable] = Counter()

    def visit_FunctionDef(self, node: FunctionDef) -> None:
        func = Function(node.name)
        self.all_funcs.append(func)
        self.func_stack.append(func)
        super().visit_FunctionDef(node)
        assert self.func_stack.pop() is func
        self.func_stack.pop()

    def _assign(self, target: str):
        v = Variable(target)
        if not self.func_stack:
            self.toplevel_variables[v] += 1
        else:
            self.func_stack[-1].variables_uses_num[v] += 1
            self.func_stack[-1].local_variables.add(v)

    def _use(self, target: str):
        v = Variable(target)
        if not self.func_stack:
            self.toplevel_variables[v] += 1
        else:
            self.func_stack[-1].variables_uses_num[v] += 1

    def visit_Name(self, node: Name) -> None:
        if isinstance(node.ctx, Load):
            self._use(node.id)
        elif isinstance(node.ctx, Store):
            self._assign(node.id)


VariableSearcher(set())
