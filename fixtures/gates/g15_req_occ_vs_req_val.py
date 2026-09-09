"""G15: 最弱等級 / `req_occ` と `req_val` の分離。

期待: `req_occ = OP`（セレクタ allowlist、既定閉のモジュール定数）、
`req_val(argv[*]) = weak(no_dashdash)` -> 規則 W により GAP_INJECT。
**前身は guarded=True = 誤 clear（不健全）。**

**この 2 分割は必須。** 1 つにまとめると、セレクタへの強い検証が
引数位置の INJECT 判定を消す（型エラー）。
"""

from _prelude import ALLOWED_TOOLS
from _tools import git_log


def dispatch(name, argstr):
    if name not in ALLOWED_TOOLS:  # WITNESS
        raise PermissionError(name)
    git_log(argstr)  # EFFECT
