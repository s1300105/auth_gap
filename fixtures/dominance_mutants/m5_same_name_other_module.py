"""mutant 5: 別モジュールの同名クラスにゲートがあり、当該ユニットの
連結経路上には無い形。

期待: **非支配**。前身は呼出元を上向きに辿ってクラス名だけで一致させ誤って
clear した。AuthGap は入口から sink へ**下向き**に辿るので「呼出元一致」という
概念自体を持たない。この mutant は下向き走査が同名クラスに引きずられないことを試す。
"""

from _prelude import TOOLS
from m5_other import Router as GatedRouter


class Router:
    """こちらにはゲートが無い。名前だけが `m5_other.Router` と一致する。"""

    def dispatch(self, name, args):
        return TOOLS[name](args)  # EFFECT


def build_gated():
    return GatedRouter()
