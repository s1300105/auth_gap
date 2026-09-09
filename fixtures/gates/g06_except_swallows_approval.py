"""G6: 承認の例外が except で握り潰される。

期待: NODOM(deny_reaches_effect)。前身も NODOM（一致。回帰固定として残す）。

**後支配版はこれを DOM と誤採点する。** 本設計が潰すために存在する誤 clear の
方向そのものなので、この fixture を落としてはならない。
"""

from _prelude import ApprovalDenied, TOOLS, require_approval


def dispatch(name, args):
    try:
        require_approval(name)  # WITNESS
    except ApprovalDenied:
        pass
    return TOOLS[name](args)  # EFFECT
