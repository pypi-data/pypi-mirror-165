import ast
from typing import Any

from ast import *
from enum import IntEnum, auto
import sys
from contextlib import contextmanager, nullcontext
import re
from string import digits, whitespace


punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^`{|}~"""


compound_statements = (
    FunctionDef,
    AsyncFunctionDef,
    ClassDef,
    For,
    AsyncFor,
    While,
    If,
    With,
    AsyncWith,
    Match,
    Try,
)


def has_compound_statement(nodes: list[ast.stmt]) -> bool:
    for node in nodes:
        if isinstance(node, compound_statements):
            return True
    return False


# This code is based on ast.unparse.


class Precedence(IntEnum):
    TUPLE = auto()
    YIELD = auto()           # 'yield', 'yield from'
    TEST = auto()            # 'if'-'else', 'lambda'
    OR = auto()              # 'or'
    AND = auto()             # 'and'
    NOT = auto()             # 'not'
    CMP = auto()             # '<', '>', '==', '>=', '<=', '!=',
                             # 'in', 'not in', 'is', 'is not'
    EXPR = auto()
    BOR = EXPR               # '|'
    BXOR = auto()            # '^'
    BAND = auto()            # '&'
    SHIFT = auto()           # '<<', '>>'
    ARITH = auto()           # '+', '-'
    TERM = auto()            # '*', '@', '/', '%', '//'
    FACTOR = auto()          # unary '+', '-', '~'
    POWER = auto()           # '**'
    AWAIT = auto()           # 'await'
    ATOM = auto()

    def next(self):
        try:
            return self.__class__(self + 1)
        except ValueError:
            return self


INF_STR = "1e" + repr(sys.float_info.max_10_exp + 1)

SINGLE_QUOTES = ("'", '"')
MULTI_QUOTES = ('"""', "'''")
ALL_QUOTES = (*SINGLE_QUOTES, *MULTI_QUOTES)


class Golfer(NodeVisitor):
    """
    Convert the AST into as short a Python code as possible.
    """

    def __init__(self, *, _avoid_backslashes=False, remove_assert=True):
        self._source = []
        self._buffer = []
        self._precedences = {}
        self._type_ignores = {}
        self._indent = 0
        self._avoid_backslashes = _avoid_backslashes
        self._remove_assert = remove_assert
        self._can_omit_nl = False

    def interleave(self, inter, f, seq):
        """Call f on each item in seq, calling inter() in between."""
        seq = iter(seq)
        try:
            f(next(seq))
        except StopIteration:
            pass
        else:
            for x in seq:
                inter()
                f(x)

    def items_view(self, traverser, items):
        """Traverse and separate the given *items* with a comma and append it to
        the buffer. If *items* is a single item sequence, a trailing comma
        will be added."""
        if len(items) == 1:
            traverser(items[0])
            self.write(",")
        else:
            self.interleave(lambda: self.write(","), traverser, items)

    def maybe_newline(self):
        """Adds a newline if it isn't the start of generated source"""
        if self._source:
            self.write("\n")

    def fill(self, *texts):
        """Indent a piece of text and append it, according to the current
        indentation level"""
        if self._can_omit_nl:
            if self._source and self._source[-1][-1] != ":":
                self.write(";")
            self.write(*texts)
        else:
            self.maybe_newline()
            self.write(" " * self._indent, *texts)

    def write(self, *texts):
        """Append a piece of text"""

        for text in texts:
            self._write(text)

    def _write(self, text: str):
        if len(text) == 0:
            return

        if text == " " and len(self._source) >= 1:
            last = self._source[-1][-1]
            if last in punctuation + digits:
                return
        elif text[0] in punctuation:
            tail = "".join(self._source[-2:])
            if len(tail) >= 2:
                if tail[-1] == " " and tail[-2] not in whitespace:
                    last = self._source.pop()
                    if not last == " ":
                        self._source.append(last[:-1])

        self._source.append(text)

    def buffer_writer(self, *texts):
        self._buffer.extend(texts)

    @property
    def buffer(self):
        value = "".join(self._buffer)
        self._buffer.clear()
        return value

    @contextmanager
    def block(self):
        """A context manager for preparing the source for blocks. It adds
        the character':', increases the indentation on enter and decreases
        the indentation on exit.
        """
        self.write(":")
        self._indent += 1
        yield
        self._indent -= 1

    @contextmanager
    def delimit(self, start, end):
        """A context manager for preparing the source for expressions. It adds
        *start* to the buffer and enters, after exit it adds *end*."""

        self.write(start)
        yield
        self.write(end)

    def delimit_if(self, start, end, condition):
        if condition:
            return self.delimit(start, end)
        else:
            return nullcontext()

    def require_parens(self, precedence, node):
        """Shortcut to adding precedence related parens"""
        return self.delimit_if("(", ")", self.get_precedence(node) > precedence)

    def get_precedence(self, node):
        return self._precedences.get(node, Precedence.TEST)

    def set_precedence(self, precedence, *nodes):
        for node in nodes:
            self._precedences[node] = precedence

    def get_raw_docstring(self, node):
        """If a docstring node is found in the body of the *node* parameter,
        return that docstring node, None otherwise.

        Logic mirrored from ``_PyAST_GetDocString``."""
        if not isinstance(
            node, (AsyncFunctionDef, FunctionDef, ClassDef, Module)
        ) or len(node.body) < 1:
            return None
        node = node.body[0]
        if not isinstance(node, Expr):
            return None
        node = node.value
        if isinstance(node, Constant) and isinstance(node.value, str):
            return node

    def get_type_comment(self, node):
        assert False
        comment = self._type_ignores.get(node.lineno) or node.type_comment
        if comment is not None:
            return f" # type: {comment}"

    def traverse(self, node):
        if isinstance(node, list):
            for item in node:
                self.traverse(item)
        else:
            super().visit(node)

    def traverse_body(self, body: list[stmt]):
        if not has_compound_statement(body):
            self._can_omit_nl = True

        with self.block():
            before_source_len = len(self._source)
            self.traverse(body)
            if len(self._source) == before_source_len:
                self.write("1")  # it means pass

        self._can_omit_nl = False

    def traverse_body_with_docstring(self, node):
        if not has_compound_statement(node.body):
            self._can_omit_nl = True

        with self.block():
            before_source_len = len(self._source)
            if (docstring := self.get_raw_docstring(node)):
                self._write_docstring(docstring)
                self.traverse(node.body[1:])
            else:
                self.traverse(node.body)
            if len(self._source) == before_source_len:
                self.write("1")  # it means pass

        self._can_omit_nl = False

    def float_shortest_expression(self, x: float) -> str:
        if x == float("inf"):
            return INF_STR
        elif x == float("nan"):
            return f"({INF_STR}-{INF_STR})"

        candidates = []
        candidates.append(repr(x))

        if x.is_integer():
            candidates.append(repr(int(x)) + ".")
        if x < 1:
            candidates.append("." + repr(x)[2:])

        for exponent in range(-1000, 1000):
            try:
                y = 10.0 ** exponent
            except OverflowError:
                continue

            if y == 0:
                continue

            z = x / y
            if z == float("inf"):
                continue

            if z.is_integer():
                candidates.append(repr(int(z)) + "e" + repr(exponent))
            else:
                candidates.append(repr(z) + "e" + repr(exponent))

        validity_candidates = []

        for c in candidates:
            try:
                if ast.literal_eval(c) == x:
                    validity_candidates.append(c)
            except SyntaxError:
                pass

        return min(validity_candidates, key=len)

    def visit(self, node):
        """Outputs a source code string that, if converted back to an ast
        (using ast.parse) will generate an AST equivalent to *node*"""
        self._source = []
        self.traverse(node)
        return "".join(self._source)

    def _write_docstring_and_traverse_body(self, node):
        if (docstring := self.get_raw_docstring(node)):
            self._write_docstring(docstring)
            self.traverse(node.body[1:])
        else:
            self.traverse(node.body)

    def visit_Module(self, node):
        if not has_compound_statement(node.body):
            self._can_omit_nl = True
        if (docstring := self.get_raw_docstring(node)):
            self._write_docstring(docstring)
            self.traverse(node.body[1:])
        else:
            self.traverse(node.body)
        self._can_omit_nl = False

    def visit_FunctionType(self, node):
        with self.delimit("(", ")"):
            self.interleave(
                lambda: self.write(","), self.traverse, node.argtypes
            )

    def visit_Expr(self, node):
        self.fill()
        self.set_precedence(Precedence.YIELD, node.value)
        self.traverse(node.value)

    def visit_NamedExpr(self, node):
        with self.require_parens(Precedence.TUPLE, node):
            self.set_precedence(Precedence.ATOM, node.target, node.value)
            self.traverse(node.target)
            self.write(":=")
            self.traverse(node.value)

    def visit_Import(self, node):
        self.fill("import ")
        self.interleave(lambda: self.write(","), self.traverse, node.names)

    def visit_ImportFrom(self, node):
        self.fill("from ")
        self.write("." * node.level)
        if node.module:
            self.write(node.module)
        self.write(" ", "import", " ")
        self.interleave(lambda: self.write(","), self.traverse, node.names)

    def visit_Assign(self, node):
        self.fill()
        for target in node.targets:
            self.traverse(target)
            self.write("=")
        self.traverse(node.value)

    def visit_AugAssign(self, node):
        self.fill()
        self.traverse(node.target)
        self.write(self.binop[node.op.__class__.__name__] + "=")
        self.traverse(node.value)

    def visit_AnnAssign(self, node):
        if node.value:
            self.fill()
            with self.delimit_if("(", ")", not node.simple and isinstance(node.target, Name)):
                self.traverse(node.target)
            self.write("=")
            self.traverse(node.value)

    def visit_Return(self, node):
        self.fill("return")
        if node.value:
            self.write(" ")
            self.traverse(node.value)

    def visit_Pass(self, node):
        self.fill("1")  # Pass can be replaced with any Expression

    def visit_Break(self, node):
        self.fill("break")

    def visit_Continue(self, node):
        self.fill("continue")

    def visit_Delete(self, node):
        self.fill("del ")
        self.interleave(lambda: self.write(","), self.traverse, node.targets)

    def visit_Assert(self, node):
        if self._remove_assert:
            pass
        else:
            self.fill("assert ")
            self.traverse(node.test)
            if node.msg:
                self.write(",")
                self.traverse(node.msg)

    def visit_Global(self, node):
        self.fill("global ")
        self.interleave(lambda: self.write(","), self.write, node.names)

    def visit_Nonlocal(self, node):
        self.fill("nonlocal ")
        self.interleave(lambda: self.write(","), self.write, node.names)

    def visit_Await(self, node):
        with self.require_parens(Precedence.AWAIT, node):
            self.write("await")
            if node.value:
                self.write(" ")
                self.set_precedence(Precedence.ATOM, node.value)
                self.traverse(node.value)

    def visit_Yield(self, node):
        with self.require_parens(Precedence.YIELD, node):
            self.write("yield")
            if node.value:
                self.write(" ")
                self.set_precedence(Precedence.ATOM, node.value)
                self.traverse(node.value)

    def visit_YieldFrom(self, node):
        with self.require_parens(Precedence.YIELD, node):
            self.write("yield from ")
            if not node.value:
                raise ValueError("Node can't be used without a value attribute.")
            self.set_precedence(Precedence.ATOM, node.value)
            self.traverse(node.value)

    def visit_Raise(self, node):
        self.fill("raise")
        if not node.exc:
            if node.cause:
                raise ValueError(f"Node can't use cause without an exception.")
            return
        self.write(" ")
        self.traverse(node.exc)
        if node.cause:
            self.write(" ", "from", " ")
            self.traverse(node.cause)

    def visit_Try(self, node):
        self.fill("try")
        self.traverse_body(node.body)
        for ex in node.handlers:
            self.traverse(ex)
        if node.orelse:
            self.fill("else")
            self.traverse_body(node.orelse)
        if node.finalbody:
            self.fill("finally")
            self.traverse_body(node.finalbody)

    def visit_ExceptHandler(self, node):
        self.fill("except")
        if node.type:
            self.write(" ")
            self.traverse(node.type)
        if node.name:
            self.write(" ", "as", " ")
            self.write(node.name)
        self.traverse_body(node.body)

    def visit_ClassDef(self, node):
        for deco in node.decorator_list:
            self.fill("@")
            self.traverse(deco)
        self.fill("class", " " + node.name)
        with self.delimit_if("(", ")", condition = node.bases or node.keywords):
            comma = False
            for e in node.bases:
                if comma:
                    self.write(",")
                else:
                    comma = True
                self.traverse(e)
            for e in node.keywords:
                if comma:
                    self.write(",")
                else:
                    comma = True
                self.traverse(e)

        self.traverse_body_with_docstring(node)

    def visit_FunctionDef(self, node):
        self._function_helper(node, "def")

    def visit_AsyncFunctionDef(self, node):
        self._function_helper(node, "async def")

    def _function_helper(self, node, fill_suffix):
        for deco in node.decorator_list:
            self.fill("@")
            self.traverse(deco)
        def_str = fill_suffix + " " + node.name
        self.fill(def_str)
        with self.delimit("(", ")"):
            self.traverse(node.args)
        self.traverse_body_with_docstring(node)

    def visit_For(self, node):
        self._for_helper("for ", node)

    def visit_AsyncFor(self, node):
        self._for_helper("async for ", node)

    def _for_helper(self, fill, node):
        self.fill(fill)
        self.traverse(node.target)
        self.write(" ", "in", " ")
        self.traverse(node.iter)
        self.traverse_body(node.body)
        if node.orelse:
            self.fill("else")
            self.traverse_body(node.orelse)

    def visit_If(self, node):
        self.fill("if", " ")
        self.traverse(node.test)
        self.traverse_body(node.body)
        # collapse nested ifs into equivalent elifs.
        while node.orelse and len(node.orelse) == 1 and isinstance(node.orelse[0], If):
            node = node.orelse[0]
            self.fill("elif ")
            self.traverse(node.test)
            self.traverse_body(node.body)
        # final else
        if node.orelse:
            self.fill("else")
            self.traverse_body(node.orelse)

    def visit_While(self, node):
        self.fill("while ")
        self.traverse(node.test)
        self.traverse_body(node.body)
        if node.orelse:
            self.fill("else")
            self.traverse_body(node.orelse)

    def visit_With(self, node):
        self.fill("with ")
        self.interleave(lambda: self.write(","), self.traverse, node.items)
        self.traverse_body(node.body)

    def visit_AsyncWith(self, node):
        self.fill("async with ")
        self.interleave(lambda: self.write(","), self.traverse, node.items)
        self.traverse_body(node.body)

    def _str_literal_helper(
        self, string, *, quote_types=ALL_QUOTES, escape_special_whitespace=False
    ):
        """Helper for writing string literals, minimizing escapes.
        Returns the tuple (string literal to write, possible quote types).
        """
        def escape_char(c):
            # \n and \t are non-printable, but we only escape them if
            # escape_special_whitespace is True
            if not escape_special_whitespace and c in "\n\t":
                return c
            # Always escape backslashes and other non-printable characters
            if c == "\\" or not c.isprintable():
                return c.encode("unicode_escape").decode("ascii")
            return c

        escaped_string = "".join(map(escape_char, string))
        possible_quotes = quote_types
        if "\n" in escaped_string:
            possible_quotes = [q for q in possible_quotes if q in MULTI_QUOTES]
        possible_quotes = [q for q in possible_quotes if q not in escaped_string]
        if not possible_quotes:
            # If there aren't any possible_quotes, fallback to using repr
            # on the original string. Try to use a quote from quote_types,
            # e.g., so that we use triple quotes for docstrings.
            string = repr(string)
            quote = next((q for q in quote_types if string[0] in q), string[0])
            return string[1:-1], [quote]
        if escaped_string:
            # Sort so that we prefer '''"''' over """\""""
            possible_quotes.sort(key=lambda q: q[0] == escaped_string[-1])
            # If we're using triple quotes and we'd need to escape a final
            # quote, escape it
            if possible_quotes[0][0] == escaped_string[-1]:
                assert len(possible_quotes[0]) == 3
                escaped_string = escaped_string[:-1] + "\\" + escaped_string[-1]
        return escaped_string, possible_quotes

    def _write_str_avoiding_backslashes(self, string, *, quote_types=ALL_QUOTES):
        """Write string literal value with a best effort attempt to avoid backslashes."""
        string, quote_types = self._str_literal_helper(string, quote_types=quote_types)
        quote_type = quote_types[0]
        self.write(f"{quote_type}{string}{quote_type}")

    def visit_JoinedStr(self, node):
        self.write("f")
        if self._avoid_backslashes:
            self._fstring_JoinedStr(node, self.buffer_writer)
            self._write_str_avoiding_backslashes(self.buffer)
            return

        # If we don't need to avoid backslashes globally (i.e., we only need
        # to avoid them inside FormattedValues), it's cosmetically preferred
        # to use escaped whitespace. That is, it's preferred to use backslashes
        # for cases like: f"{x}\n". To accomplish this, we keep track of what
        # in our buffer corresponds to FormattedValues and what corresponds to
        # Constant parts of the f-string, and allow escapes accordingly.
        buffer = []
        for value in node.values:
            meth = getattr(self, "_fstring_" + type(value).__name__)
            meth(value, self.buffer_writer)
            buffer.append((self.buffer, isinstance(value, Constant)))
        new_buffer = []
        quote_types = ALL_QUOTES
        for value, is_constant in buffer:
            # Repeatedly narrow down the list of possible quote_types
            value, quote_types = self._str_literal_helper(
                value, quote_types=quote_types,
                escape_special_whitespace=is_constant
            )
            new_buffer.append(value)
        value = "".join(new_buffer)
        quote_type = quote_types[0]
        self.write(f"{quote_type}{value}{quote_type}")

    def visit_FormattedValue(self, node):
        self.write("f")
        self._fstring_FormattedValue(node, self.buffer_writer)
        self._write_str_avoiding_backslashes(self.buffer)

    def _fstring_JoinedStr(self, node, write):
        for value in node.values:
            meth = getattr(self, "_fstring_" + type(value).__name__)
            meth(value, write)

    def _fstring_Constant(self, node, write):
        if not isinstance(node.value, str):
            raise ValueError("Constants inside JoinedStr should be a string.")
        value = node.value.replace("{", "{{").replace("}", "}}")
        write(value)

    def _fstring_FormattedValue(self, node, write):
        write("{")
        unparser = type(self)(_avoid_backslashes=True)
        unparser.set_precedence(Precedence.TEST.next(), node.value)
        expr = unparser.visit(node.value)
        if expr.startswith("{"):
            write(" ")  # Separate pair of opening brackets as "{ {"
        if "\\" in expr:
            raise ValueError("Unable to avoid backslash in f-string expression part")
        write(expr)
        if node.conversion != -1:
            conversion = chr(node.conversion)
            if conversion not in "sra":
                raise ValueError("Unknown f-string conversion.")
            write(f"!{conversion}")
        if node.format_spec:
            write(":")
            meth = getattr(self, "_fstring_" + type(node.format_spec).__name__)
            meth(node.format_spec, write)
        write("}")

    def visit_Name(self, node):
        self.write(node.id)

    def _write_docstring(self, node):
        """
        self.fill()
        if node.kind == "u":
            self.write("u")
        self._write_str_avoiding_backslashes(node.value, quote_types=MULTI_QUOTES)
        """

    def _write_constant(self, value):
        if isinstance(value, float):
            self.write(self.float_shortest_expression(value))
        elif isinstance(value, (float, complex)):
            # Substitute overflowing decimal literal for AST infinities,
            # and inf - inf for NaNs.
            self.write(
                repr(value)
                .replace("inf", INF_STR)
                .replace("nan", f"({INF_STR}-{INF_STR})")
            )
        elif self._avoid_backslashes and isinstance(value, str):
            self._write_str_avoiding_backslashes(value)
        else:
            self.write(repr(value))

    def visit_Constant(self, node):
        value = node.value
        if isinstance(value, tuple):
            with self.delimit("(", ")"):
                self.items_view(self._write_constant, value)
        elif value is ...:
            self.write("...")
        else:
            if node.kind == "u":
                self.write("u")
            self._write_constant(node.value)

    def visit_List(self, node):
        with self.delimit("[", "]"):
            self.interleave(lambda: self.write(","), self.traverse, node.elts)

    def visit_ListComp(self, node):
        with self.delimit("[", "]"):
            self.traverse(node.elt)
            for gen in node.generators:
                self.traverse(gen)

    def visit_GeneratorExp(self, node):
        with self.delimit("(", ")"):
            self.traverse(node.elt)
            for gen in node.generators:
                self.traverse(gen)

    def visit_SetComp(self, node):
        with self.delimit("{", "}"):
            self.traverse(node.elt)
            for gen in node.generators:
                self.traverse(gen)

    def visit_DictComp(self, node):
        with self.delimit("{", "}"):
            self.traverse(node.key)
            self.write(":")
            self.traverse(node.value)
            for gen in node.generators:
                self.traverse(gen)

    def visit_comprehension(self, node):
        if node.is_async:
            self.write(" ", "async for", " ")
        else:
            self.write(" ", "for", " ")
        self.set_precedence(Precedence.TUPLE, node.target)
        self.traverse(node.target)
        self.write(" ", "in", " ")
        self.set_precedence(Precedence.TEST.next(), node.iter, *node.ifs)
        self.traverse(node.iter)
        for if_clause in node.ifs:
            self.write(" ", "if", " ")
            self.traverse(if_clause)

    def visit_IfExp(self, node):
        with self.require_parens(Precedence.TEST, node):
            self.set_precedence(Precedence.TEST.next(), node.body, node.test)
            self.traverse(node.body)
            self.write(" ", "if", " ")
            self.traverse(node.test)
            self.write(" ", "else", " ")
            self.set_precedence(Precedence.TEST, node.orelse)
            self.traverse(node.orelse)

    def visit_Set(self, node):
        if node.elts:
            with self.delimit("{", "}"):
                self.interleave(lambda: self.write(","), self.traverse, node.elts)
        else:
            # `{}` would be interpreted as a dictionary literal, and
            # `set` might be shadowed. Thus:
            self.write('{*()}')

    def visit_Dict(self, node):
        def write_key_value_pair(k, v):
            self.traverse(k)
            self.write(":")
            self.traverse(v)

        def write_item(item):
            k, v = item
            if k is None:
                # for dictionary unpacking operator in dicts {**{'y': 2}}
                # see PEP 448 for details
                self.write("**")
                self.set_precedence(Precedence.EXPR, v)
                self.traverse(v)
            else:
                write_key_value_pair(k, v)

        with self.delimit("{", "}"):
            self.interleave(
                lambda: self.write(","), write_item, zip(node.keys, node.values)
            )

    def visit_Tuple(self, node):
        with self.delimit("(", ")"):
            self.items_view(self.traverse, node.elts)

    unop = {"Invert": "~", "Not": "not", "UAdd": "+", "USub": "-"}
    unop_precedence = {
        "not": Precedence.NOT,
        "~": Precedence.FACTOR,
        "+": Precedence.FACTOR,
        "-": Precedence.FACTOR,
    }

    def visit_UnaryOp(self, node):
        operator = self.unop[node.op.__class__.__name__]
        operator_precedence = self.unop_precedence[operator]
        with self.require_parens(operator_precedence, node):
            self.write(operator)
            # factor prefixes (+, -, ~) shouldn't be seperated
            # from the value they belong, (e.g: +1 instead of + 1)
            if operator_precedence is not Precedence.FACTOR:
                self.write(" ")
            self.set_precedence(operator_precedence, node.operand)
            self.traverse(node.operand)

    binop = {
        "Add": "+",
        "Sub": "-",
        "Mult": "*",
        "MatMult": "@",
        "Div": "/",
        "Mod": "%",
        "LShift": "<<",
        "RShift": ">>",
        "BitOr": "|",
        "BitXor": "^",
        "BitAnd": "&",
        "FloorDiv": "//",
        "Pow": "**",
    }

    binop_precedence = {
        "+": Precedence.ARITH,
        "-": Precedence.ARITH,
        "*": Precedence.TERM,
        "@": Precedence.TERM,
        "/": Precedence.TERM,
        "%": Precedence.TERM,
        "<<": Precedence.SHIFT,
        ">>": Precedence.SHIFT,
        "|": Precedence.BOR,
        "^": Precedence.BXOR,
        "&": Precedence.BAND,
        "//": Precedence.TERM,
        "**": Precedence.POWER,
    }

    binop_rassoc = frozenset(("**",))
    def visit_BinOp(self, node):
        operator = self.binop[node.op.__class__.__name__]
        operator_precedence = self.binop_precedence[operator]
        with self.require_parens(operator_precedence, node):
            if operator in self.binop_rassoc:
                left_precedence = operator_precedence.next()
                right_precedence = operator_precedence
            else:
                left_precedence = operator_precedence
                right_precedence = operator_precedence.next()

            self.set_precedence(left_precedence, node.left)
            self.traverse(node.left)
            self.write(f"{operator}")
            self.set_precedence(right_precedence, node.right)
            self.traverse(node.right)

    cmpops = {
        "Eq": "==",
        "NotEq": "!=",
        "Lt": "<",
        "LtE": "<=",
        "Gt": ">",
        "GtE": ">=",
        "Is": "is",
        "IsNot": "is not",
        "In": "in",
        "NotIn": "not in",
    }

    cmpops_only_symbol = {
        "Eq",
        "NotEq",
        "Lt",
        "LtE",
        "Gt",
        "GtE",
    }

    def visit_Compare(self, node):
        with self.require_parens(Precedence.CMP, node):
            self.set_precedence(Precedence.CMP.next(), node.left, *node.comparators)
            self.traverse(node.left)
            for o, e in zip(node.ops, node.comparators):
                with self.delimit_if(" ", " ", o.__class__.__name__ not in self.cmpops_only_symbol):
                    self.write(self.cmpops[o.__class__.__name__])
                self.traverse(e)

    boolops = {"And": "and", "Or": "or"}
    boolop_precedence = {"and": Precedence.AND, "or": Precedence.OR}

    def visit_BoolOp(self, node):
        operator = self.boolops[node.op.__class__.__name__]
        operator_precedence = self.boolop_precedence[operator]

        def increasing_level_traverse(node):
            nonlocal operator_precedence
            operator_precedence = operator_precedence.next()
            self.set_precedence(operator_precedence, node)
            self.traverse(node)

        with self.require_parens(operator_precedence, node):
            s = (" ", operator, " ")
            self.interleave(lambda: self.write(*s), increasing_level_traverse, node.values)

    def visit_Attribute(self, node):
        self.set_precedence(Precedence.ATOM, node.value)
        self.traverse(node.value)
        # Special case: 3.__abs__() is a syntax error, so if node.value
        # is an integer literal then we need to either parenthesize
        # it or add an extra space to get 3 .__abs__().
        if isinstance(node.value, Constant) and isinstance(node.value.value, int):
            self.write(" ")
        self.write(".")
        self.write(node.attr)

    def visit_Call(self, node):
        self.set_precedence(Precedence.ATOM, node.func)
        self.traverse(node.func)
        with self.delimit("(", ")"):
            comma = False
            for e in node.args:
                if comma:
                    self.write(",")
                else:
                    comma = True
                self.traverse(e)
            for e in node.keywords:
                if comma:
                    self.write(",")
                else:
                    comma = True
                self.traverse(e)

    def visit_Subscript(self, node):
        def is_simple_tuple(slice_value):
            # when unparsing a non-empty tuple, the parentheses can be safely
            # omitted if there aren't any elements that explicitly requires
            # parentheses (such as starred expressions).
            return (
                isinstance(slice_value, Tuple)
                and slice_value.elts
                and not any(isinstance(elt, Starred) for elt in slice_value.elts)
            )

        self.set_precedence(Precedence.ATOM, node.value)
        self.traverse(node.value)
        with self.delimit("[", "]"):
            if is_simple_tuple(node.slice):
                self.items_view(self.traverse, node.slice.elts)
            else:
                self.traverse(node.slice)

    def visit_Starred(self, node):
        self.write("*")
        self.set_precedence(Precedence.EXPR, node.value)
        self.traverse(node.value)

    def visit_Ellipsis(self, node):
        self.write("...")

    def visit_Slice(self, node):
        if node.lower:
            self.traverse(node.lower)
        self.write(":")
        if node.upper:
            self.traverse(node.upper)
        if node.step:
            self.write(":")
            self.traverse(node.step)

    def visit_arg(self, node):
        self.write(node.arg)

    def visit_arguments(self, node):
        first = True
        # normal arguments
        all_args = node.posonlyargs + node.args
        defaults = [None] * (len(all_args) - len(node.defaults)) + node.defaults
        for index, elements in enumerate(zip(all_args, defaults), 1):
            a, d = elements
            if first:
                first = False
            else:
                self.write(",")
            self.traverse(a)
            if d:
                self.write("=")
                self.traverse(d)
            if index == len(node.posonlyargs):
                self.write(",/")

        # varargs, or bare '*' if no varargs but keyword-only arguments present
        if node.vararg or node.kwonlyargs:
            if first:
                first = False
            else:
                self.write(",")
            self.write("*")
            if node.vararg:
                self.write(node.vararg.arg)

        # keyword-only arguments
        if node.kwonlyargs:
            for a, d in zip(node.kwonlyargs, node.kw_defaults):
                self.write(",")
                self.traverse(a)
                if d:
                    self.write("=")
                    self.traverse(d)

        # kwargs
        if node.kwarg:
            if first:
                first = False
            else:
                self.write(",")
            self.write("**" + node.kwarg.arg)

    def visit_keyword(self, node):
        if node.arg is None:
            self.write("**")
        else:
            self.write(node.arg)
            self.write("=")
        self.traverse(node.value)

    def visit_Lambda(self, node):
        with self.require_parens(Precedence.TEST, node):
            self.write("lambda ")
            self.traverse(node.args)
            self.write(":")
            self.set_precedence(Precedence.TEST, node.body)
            self.traverse(node.body)

    def visit_alias(self, node):
        self.write(node.name)
        if node.asname:
            self.write(" ", "as", " " + node.asname)

    def visit_withitem(self, node):
        self.traverse(node.context_expr)
        if node.optional_vars:
            self.write(" ", "as", " ")
            self.traverse(node.optional_vars)


def unparse_ast(ast_obj):
    unparser = Golfer()
    return unparser.visit(ast_obj)
