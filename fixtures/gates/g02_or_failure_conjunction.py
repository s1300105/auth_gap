"""G2: `or` の失敗連言。

期待: DOM(USER)。前身 HEAD は NODOM("`or` disjunct") で誤 FN
（`f7aced6` では DOM だったので v2 での退行）。

`not confirm(name) or name not in ALLOWED_TOOLS` は、どちらの選言肢が真でも
拒否側へ抜ける形。両方の test が効果を支配し、経路上は ⊔ で USER。
"""

from _prelude import ALLOWED_TOOLS, ApprovalDenied, TOOLS, confirm


def dispatch(name, args):
    if not confirm(name) or name not in ALLOWED_TOOLS:  # WITNESS
        raise ApprovalDenied(name)
    return TOOLS[name](args)  # EFFECT
