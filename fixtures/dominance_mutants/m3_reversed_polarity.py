"""mutant 3: `if not is_allowed(name): tool.run()`（極性逆）。

期待: **非支配**。効果は拒否側の枝にある。
"""

from _prelude import TOOLS, is_allowed


def dispatch(name, args):
    if not is_allowed(name):  # WITNESS
        return TOOLS[name](args)  # EFFECT
    return ""
