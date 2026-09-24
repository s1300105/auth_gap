#!/usr/bin/env python3
"""母集団 v3 の V3（見落としの抜き取り）の対象を決める（docs/population_v3.md）。

D1（`readOnlyHint` を明示）か D2（`destructiveHint` を明示し `readOnlyHint` を明示しない）を持ち、その宣言に
対する矛が 1 件も出ていないユニットから、seed 20260924 で 30 件を抜き取る。宣言は解析器の
`D_kind.explicit`。**判定の前に出力をコミットする。**

    .venv/bin/python scripts/v3_miss_sample.py evidence/scan_v2_v3_run1 --out evidence/population_v3/v3_miss_targets.json
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from contradiction_by_decl import load_reasons  # noqa: E402

SEED = 20260924
N = 30


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    contra: set[tuple[str, str, str]] = set()
    for (tree, qual, _site, _kind), decls in load_reasons(a.run_dir).items():
        for decl, findings in decls.items():
            if any(s == "contradiction" for s, _ in findings):
                contra.add((tree, qual, decl))
    pool = []
    for fn in sorted(os.listdir(a.run_dir)):
        if not fn.endswith(".json") or fn in ("summary.json", "contradictions.json") or "-" not in fn:
            continue
        tree = fn[:-5]
        for u in json.load(open(os.path.join(a.run_dir, fn), encoding="utf-8"))["units"]:
            ex = set((u.get("D_kind") or {}).get("explicit") or [])
            qual = u["unit"]["qualname"]
            decl = "D1" if "readOnlyHint" in ex else ("D2" if "destructiveHint" in ex else None)
            if decl is None or (tree, qual, decl) in contra:
                continue
            pool.append({"tree": tree, "unit": qual, "decl": decl, "relpath": u["unit"].get("relpath"),
                         "lineno": u["unit"].get("lineno"), "n_effects": len(u.get("effects") or [])})
    rng = random.Random(SEED)
    pick = sorted(rng.sample(range(len(pool)), N)) if len(pool) > N else list(range(len(pool)))
    out = {"_note": "docs/population_v3.md V3 の対象。判定の前にコミットする。", "seed": SEED,
           "n_pool": len(pool), "n_pool_D1": sum(1 for r in pool if r["decl"] == "D1"),
           "n_pool_D2": sum(1 for r in pool if r["decl"] == "D2"), "n_judged": len(pick),
           "targets": [dict(pool[i], id=f"R{k:02d}") for k, i in enumerate(pick)]}
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print({k: out[k] for k in out if k.startswith("n_")})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
