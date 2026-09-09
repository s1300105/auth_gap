"""G7: 内包表記の `if` フィルタ。

期待: DOM(OP)。前身は NODOM で誤 FN。
内包表記は合成した無名関数として別 CFG になり、`if` は要素式をゲートする。
"""

from _prelude import TOOLS, is_allowed


def dispatch_all(names, args):
    return [TOOLS[n](args) for n in names if is_allowed(n)]  # EFFECT  # WITNESS
