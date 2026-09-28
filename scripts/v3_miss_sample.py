#!/usr/bin/env python3
"""母集団 v3 の V3（見落としの抜き取り）の対象を決める（docs/population_v3.md）。

D1（`readOnlyHint` を明示）か D2（`destructiveHint` を明示し `readOnlyHint` を明示しない）を持ち、その宣言に
対する矛が 1 件も出ていないユニットから、seed 20260924 で 30 件を抜き取る。宣言は解析器の
`D_kind.explicit`。**判定の前に出力をコミットする。**

manifest の集合は summary.json の ok の木で決め、ユニットは relpath と行で区別する（D64 / U50・U52）。
打ち切りの印（`TRUNCATED(...)` の notes）のあるユニットは `truncated` を付け、判定者が「不明（打ち切り）」に
分けられるようにする（D64 / U49、R5-r3-2）。**v3 の対象（2026-09-24 にコミット）はこの修正の前に選んだ。**

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
from runlib import load_manifest, print_warnings, run_manifests, unit_key  # noqa: E402

SEED = 20260924
N = 30


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    contra: set[tuple] = set()
    for key, decls in load_reasons(a.run_dir).items():
        for decl, findings in decls.items():
            if any(s == "contradiction" for s, _ in findings):
                contra.add((*key[:4], decl))
    pool = []
    manifests, warnings = run_manifests(a.run_dir)
    print_warnings(warnings, os.path.basename(a.run_dir.rstrip("/")))
    for tree, path in manifests:
        for u in load_manifest(path)["units"]:
            ex = set((u.get("D_kind") or {}).get("explicit") or [])
            decl = "D1" if "readOnlyHint" in ex else ("D2" if "destructiveHint" in ex else None)
            if decl is None or (*unit_key(tree, u["unit"]), decl) in contra:
                continue
            truncated = sorted(n for n in (u.get("notes") or []) if str(n).startswith("TRUNCATED"))
            pool.append({"tree": tree, "unit": u["unit"]["qualname"], "decl": decl, "relpath": u["unit"].get("relpath"),
                         "lineno": u["unit"].get("lineno"), "n_effects": len(u.get("effects") or []),
                         **({"truncated": truncated} if truncated else {})})
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
