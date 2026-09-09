#!/usr/bin/env python3
"""mutant 7（CFG ノード cap）を再生成する。

CFG ノード cap（`authgap.ir.CFG_NODE_CAP` = 2000）を超え、かつ
file 単位の AST ノード cap（`AST_NODE_CAP` = 20000）は超えないようにする。
**両方に当たると、どちらの cap を試験しているのか分からなくなる。**
"""

import ast
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(ROOT, "fixtures", "dominance_mutants", "m7_cfg_cap.py")
N = 2100

HEADER = '''"""mutant 7: node/深さ cap 到達での黙示 clear。

期待: **非支配**に加えて `TRUNCATED` 行と `OPAQUE(cfg_cap)` が出力されること。
行が出なければ不合格（支配規則ではなくハーネスの性質を突く）。

生成規則: `dispatch` の本体に `x{{i}} = 1` を {n} 行置く。
authgap.ir.CFG_NODE_CAP = 2000 を超えるので cfg_cap に当たる。
AST ノード数は AST_NODE_CAP = 20000 の下に収める（**別の cap に当てない**
ため。file 単位の cap に当たると CFG cap を試験できない）。
再生成: scripts/gen_mutant7.py
"""

from _prelude import TOOLS


def dispatch(name, args):
'''


def main() -> None:
    body = "\n".join(f"    x{i} = 1" for i in range(N))
    src = HEADER.format(n=N) + body + "\n    return TOOLS[name](args)  # EFFECT\n"
    with open(DEST, "w", encoding="utf-8") as fh:
        fh.write(src)
    nodes = sum(1 for _ in ast.walk(ast.parse(src)))
    print(f"wrote {DEST}: {N} statements, {nodes} AST nodes")
    assert nodes < 20000, "AST_NODE_CAP に当たってしまう"


if __name__ == "__main__":
    main()
