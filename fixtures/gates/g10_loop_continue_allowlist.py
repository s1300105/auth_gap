"""G10: ループ内 `continue` の allowlist。

期待: DOM(OP, config-conditional 既定閉)。前身も DOM（一致。回帰固定）。

**`CFG∖{g}` の除去が無いと `continue -> header -> 次の反復 -> 効果` が
拒否辺からの到達路に見え、正しいループ allowlist を誤って NODOM にする。**
"""

from _prelude import ALLOWED_TOOLS, TOOLS


def dispatch_all(names, args):
    out = []
    for name in names:
        if name not in ALLOWED_TOOLS:  # WITNESS
            continue
        out.append(TOOLS[name](args))  # EFFECT
    return out
