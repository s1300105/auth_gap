"""G4: walrus を含む test。

期待: DOM(USER)。前身 HEAD は NODOM（`f7aced6` では DOM。v2 での退行）。
"""

from _prelude import ApprovalDenied, TOOLS, confirm


def dispatch(name, args):
    if not (ok := confirm(name)):  # WITNESS
        raise ApprovalDenied(f"{name}:{ok}")
    return TOOLS[name](args)  # EFFECT
