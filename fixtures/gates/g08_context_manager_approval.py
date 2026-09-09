"""G8: CM 形の承認ゲート（`Gateway.require_approval`、木内解決可）。

期待: DOM(USER)。前身は NODOM で誤 FN。
`ENTER(cm)` の拒否後継は例外辺で、handler が無いので EXC_EXIT に抜ける。
"""

from _prelude import Gateway, TOOLS


def dispatch(name, args):
    gw = Gateway()
    with gw.require_approval(name):  # WITNESS
        return TOOLS[name](args)  # EFFECT
