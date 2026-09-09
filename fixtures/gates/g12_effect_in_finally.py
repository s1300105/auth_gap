"""G12: 効果が `finally` 側にある。

期待: NODOM。前身も NODOM（一致。回帰固定）。

`finally` は正常終了・例外・return・break・continue のどの脱出経路でも
実行される。1 ノードで表すと支配関係が経路ごとに矛盾するので、
**finalbody は脱出種別ごとに複製し、効果の verdict は全複製の ⊓ を採る。**
例外複製は承認にゲートされていないので最弱は NODOM。
"""

from _prelude import TOOLS, require_approval


def dispatch(name, args):
    result = None
    try:
        require_approval(name)  # WITNESS
    finally:
        result = TOOLS[name](args)  # EFFECT
    return result
