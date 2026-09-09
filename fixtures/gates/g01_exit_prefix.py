"""G1: exit 前に 1 文（前身の `_is_exit_body` の全 exit 要求を突く）。

期待: DOM(OP)。前身は NODOM("non-exit body") で誤 FN。
"""

import logging

from _prelude import TOOLS, is_allowed

logger = logging.getLogger(__name__)


def dispatch(name, args):
    if not is_allowed(name):  # WITNESS
        logger.warning("denied %s", name)
        return ""
    return TOOLS[name](args)  # EFFECT
