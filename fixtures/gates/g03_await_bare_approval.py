"""G3: `await` した承認割り込みの裸文。

期待: DOM(USER)。前身は NODOM（seen にすら出ない）で誤 FN。
"""

from _prelude import TOOLS, require_approval


async def dispatch(name, args):
    await require_approval(name)  # WITNESS
    return TOOLS[name](args)  # EFFECT
