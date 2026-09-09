"""mutant 2: `if trusted or confirm(name):`（`or` の極性）。

期待: **非支配**。`trusted` が真なら短絡して `confirm` は評価されないので、
`confirm` は効果を支配しない。

G2（`or` の失敗連言、DOM 期待）と対になる。**両方を正しく分けられることが、
`or` を一律に非支配へ倒した前身 v2 との差である。**
"""

from _prelude import TOOLS, confirm


def dispatch(name, args, trusted):
    if trusted or confirm(name):  # WITNESS
        return TOOLS[name](args)  # EFFECT
    return ""
