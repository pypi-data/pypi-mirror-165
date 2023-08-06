from golfer.golfer import unparse_ast

from ast import parse


def golf(source):
    return unparse_ast(parse(source))
