"""mutant 8: ガード偽側の分岐に dispatch がある形。

期待: **非支配**。ゲートは在るが、効果は拒否側の枝にある。
"""

from _prelude import ApprovalDenied, TOOLS, confirm


def dispatch(name, args):
    if confirm(name):  # WITNESS
        raise ApprovalDenied(name)
    return TOOLS[name](args)  # EFFECT
