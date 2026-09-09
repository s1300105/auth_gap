"""G13: 木内で解決できないレジストリ。

期待: OPAQUE(dynamic_registry) -> UNKNOWN 行。
前身は**誤 clean（不健全）と推定**されていた（§9-13 で実測する）。

`Gateway.plugins` は `importlib.metadata` の entry point を読むので
候補集合が木内で決まらない。**決して drop しない。決して clean にしない。**
"""

from _prelude import Gateway


def dispatch(name, args):
    gw = Gateway()
    handler = gw.plugins.get(name)  # WITNESS
    return handler(args)  # EFFECT
