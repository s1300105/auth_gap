import ast


def literal_only(x):
    return ast.literal_eval(x)
