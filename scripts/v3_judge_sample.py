#!/usr/bin/env python3
"""母集団 v3 の V2（矛の精度）の判定対象を決める（docs/population_v3.md）。

単位は (木, ユニット, site, kind, 宣言)。D1 / D2 の矛は全件、60 件を超えたら seed 20260924 で 60 件を
抜き取る。D3 / D4 の矛は 30 件まで（同じ seed）。**判定の前に出力をコミットする。**

    .venv/bin/python scripts/v3_judge_sample.py evidence/scan_v2_v3_run1 --out evidence/population_v3/v2_judge_targets.json
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rows = []
    for (tree, qual, site, kind), decls in sorted(load_reasons(a.run_dir).items()):
        for decl, findings in sorted(decls.items()):
            reasons = sorted(r for s, r in findings if s == "contradiction")
            if reasons:
                rows.append({"tree": tree, "unit": qual, "site": site, "kind": kind, "decl": decl, "reasons": reasons})
    main_rows = [r for r in rows if r["decl"] in ("D1", "D2")]
    expl_rows = [r for r in rows if r["decl"] in ("D3", "D4")]
    rng = random.Random(SEED)
    main_pick = sorted(rng.sample(range(len(main_rows)), 60)) if len(main_rows) > 60 else list(range(len(main_rows)))
    rng = random.Random(SEED)
    expl_pick = sorted(rng.sample(range(len(expl_rows)), 30)) if len(expl_rows) > 30 else list(range(len(expl_rows)))
    out = {
        "_note": "docs/population_v3.md V2 の判定対象。判定の前にコミットする。",
        "seed": SEED,
        "n_main": len(main_rows), "n_main_judged": len(main_pick), "main_sampled": len(main_rows) > 60,
        "n_exploratory": len(expl_rows), "n_exploratory_judged": len(expl_pick),
        "targets": [dict(main_rows[i], id=f"M{k:02d}") for k, i in enumerate(main_pick)]
        + [dict(expl_rows[i], id=f"E{k:02d}") for k, i in enumerate(expl_pick)],
    }
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print({k: out[k] for k in out if k.startswith("n_") or k == "main_sampled"})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
