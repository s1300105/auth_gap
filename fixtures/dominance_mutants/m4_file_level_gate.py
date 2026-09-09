"""mutant 4: 無関係な関数の `human_in_the_loop=False`（file-level gate の誤検出）。

期待: **非支配**。ゲート語彙がファイル内に出現するだけで、当該ユニットの
連結経路上には無い。
"""

from _prelude import TOOLS


def build_agent():
    return {"human_in_the_loop": False, "requires_confirmation": True}


def dispatch(name, args):
    return TOOLS[name](args)  # EFFECT
