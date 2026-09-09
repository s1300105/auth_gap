"""G9: `contextlib.suppress` が承認を吸収する。

期待: NODOM(deny_reaches_effect)。前身も NODOM（一致。回帰固定）。

**後支配版はこれを DOM と誤採点する。**
"""

import contextlib

from _prelude import ApprovalDenied, TOOLS, require_approval


def dispatch(name, args):
    with contextlib.suppress(ApprovalDenied):
        require_approval(name)  # WITNESS
    return TOOLS[name](args)  # EFFECT
