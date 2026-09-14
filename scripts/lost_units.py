#!/usr/bin/env python3
"""2 つの F0a run の間で「危険効果を持つユニット」から外れたユニットを列挙する。

**なぜ要るか。** 解析器を直して率が良くなっても、別のユニットの危険効果が黙って
消えていることがある（run 3 で tool_package の危険効果ユニットが 82 → 76 に減り、
6 件はすべて同名関数の追加で解決を失った false-clean だった。D17 改訂 3）。
母集団の件数だけを見ると、増えた分に隠れて見落とす。

ユニットの同一性は `(木, unit_id, relpath, 入口の行)`。危険効果の判定は
`units.jsonl` の `dangerous_fp_excluded`（偽陽性クラスを除いた危険効果の有無）。

使い方::

    python scripts/lost_units.py evidence/f0a_run1py312 evidence/f0a_run4
    python scripts/lost_units.py evidence/f0a_run3 evidence/f0a_run4 --population tool_package

外れたユニットが 1 件でもあれば終了コード 1（1 件ずつ原ソースで、外れて正しいか
— 誤った解決が直った — を確かめる）。
"""

from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(evidence_dir: str, population: str | None) -> dict[tuple, dict]:
    path = evidence_dir if evidence_dir.endswith(".jsonl") else os.path.join(evidence_dir, "units.jsonl")
    if not os.path.isabs(path):
        path = os.path.join(ROOT, path)
    out: dict[tuple, dict] = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            u = json.loads(line)
            if population and u["population"] != population:
                continue
            key = (u["population"], u["tree"], u["unit_id"], u["relpath"], u["lineno"])
            out[key] = u
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("before")
    ap.add_argument("after")
    ap.add_argument("--population", default=None)
    args = ap.parse_args()

    before = load(args.before, args.population)
    after = load(args.after, args.population)
    lost = [k for k, u in sorted(before.items()) if u["dangerous_fp_excluded"] and not (k in after and after[k]["dangerous_fp_excluded"])]
    gained = [k for k, u in sorted(after.items()) if u["dangerous_fp_excluded"] and not (k in before and before[k]["dangerous_fp_excluded"])]

    by_pop: dict[str, tuple[int, int]] = {}
    for k in lost:
        g = by_pop.get(k[0], (0, 0))
        by_pop[k[0]] = (g[0] + 1, g[1])
    for k in gained:
        g = by_pop.get(k[0], (0, 0))
        by_pop[k[0]] = (g[0], g[1] + 1)
    print(f"{args.before} → {args.after}")
    for pop, (n_lost, n_gained) in sorted(by_pop.items()):
        print(f"  [{pop}] 危険効果から外れた {n_lost} / 新たに危険効果 {n_gained}")

    for k in lost:
        pop, tree, unit_id, relpath, lineno = k
        now = after.get(k)
        state = "ユニット自体が無い" if now is None else f"効果 {len(now['effects'])} 件（危険効果なし）"
        print(f"\n- LOST [{pop}] {tree} {unit_id}  {relpath}:{lineno}  → {state}")
        for e in before[k]["effects"]:
            reasons = ",".join(e.get("resolution_reasons") or [])
            print(f"    前: {e['kind']} {e['relpath']}:{e['lineno']} {e['resolution']}{('(' + reasons + ')') if reasons else ''}")
    return 1 if lost else 0


if __name__ == "__main__":
    sys.exit(main())
