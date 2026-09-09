"""G11: 主語不一致（`Gateway.is_allowed` に別の値を渡す）。

期待: NODOM(non_binding_gate)。**前身は DOM = 誤 clear（不健全）。**

ゲートは効果を支配し拒否側も効果へ到達しないが、述語のオペランドが
当該制御位置の値（`name`）ではなく `self.gw.default_tool` なので
`req_val` を引き上げてはならない。
"""

from _prelude import TOOLS, Gateway


class Router:
    def __init__(self):
        self.gw = Gateway()

    def dispatch(self, name, args):
        if not self.gw.is_allowed(self.gw.default_tool):  # WITNESS
            raise PermissionError(name)
        return TOOLS[name](args)  # EFFECT
