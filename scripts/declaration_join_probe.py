#!/usr/bin/env python3
"""**探索的**: 低レベル MCP ハンドラの `dispatch_names` で `Tool(...)` リテラルを join したら
r_D の分子がどれだけ動くかを見る（`docs/preregistration.md` §2.8 段 A の補助。
**O5（Def 6 に規則が無い）の影響の大きさを測るだけで、r_D の定義は変えない**）。

    .venv/bin/python scripts/declaration_join_probe.py --run evidence/f0a_run6 --out evidence/decl_census_run6/join_probe.json

木ごとに:
  n_units / n_units_lowlevel（tool_name が None でハンドラ形）
  n_literals / n_literals_explicit（readOnlyHint==True / destructiveHint==False / openWorldHint==True のいずれか）
  joined_current（現行規則 = tool_name の完全一致 + デコレータ annotations）
  joinable_dispatch（探索: リテラル名 ∈ unit.dispatch_names）
  units_explicit_current / units_explicit_dispatch（宣言が明示的なユニット数。r_D の分子に相当）
"""

from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from authgap.entries import find_tool_literals, find_units, join_annotations  # noqa: E402
from authgap.srcindex import SourceIndex  # noqa: E402


def explicit(ann) -> bool:
    """dparse.py:102-124 と同じ規則（明示 = 上界を宣言している）。"""
    if not isinstance(ann, dict):
        return False
    return ann.get("readOnlyHint") is True or ann.get("destructiveHint") is False or ann.get("openWorldHint") is True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", default="evidence/f0a_run6")
    ap.add_argument("--corpus", default="corpus")
    ap.add_argument("--out", default="evidence/decl_census_run6/join_probe.json")
    args = ap.parse_args()
    trees = [json.loads(line) for line in open(os.path.join(ROOT, args.run, "trees.jsonl"), encoding="utf-8") if line.strip()]
    rows = []
    tot = {"n_units": 0, "n_dangerous_unknown": 0, "n_literals": 0, "n_literals_explicit": 0, "joined_current": 0,
           "joinable_dispatch": 0, "units_explicit_current": 0, "units_explicit_dispatch": 0, "n_trees": 0}
    for t in trees:
        d = os.path.join(ROOT, args.corpus, t["tree"])
        if not os.path.isdir(d):
            rows.append({"tree": t["tree"], "status": "missing"})
            continue
        try:
            index = SourceIndex(d)
            index.build()
            units = find_units(index)
            lits = find_tool_literals(index)
            joined, unjoined = join_annotations(units, lits)
        except Exception as exc:  # 1 本で全体を落とさない
            rows.append({"tree": t["tree"], "status": f"failed: {type(exc).__name__}: {exc}"[:200]})
            continue
        lit_by_name = {}
        for L in lits:
            if L.name:
                lit_by_name.setdefault(L.name, L)
        n_expl_lits = sum(1 for L in lits if explicit(L.annotations))
        units_expl_cur = sum(1 for u in units if explicit(u.annotations))
        joinable = 0
        units_expl_disp = 0
        lowlevel = 0
        for u in units:
            if u.tool_name is None and u.dispatch_names:
                lowlevel += 1
                hit = [lit_by_name[n] for n in u.dispatch_names if n in lit_by_name]
                if hit:
                    joinable += 1
                    if any(explicit(L.annotations) for L in hit):
                        units_expl_disp += 1
            elif explicit(u.annotations):
                units_expl_disp += 1
        row = {"tree": t["tree"], "population": t["population"], "status": "ok", "n_units": len(units),
               "n_units_lowlevel_dispatch": lowlevel, "n_literals": len(lits), "n_literals_explicit": n_expl_lits,
               "joined_current": joined, "unjoined_current": unjoined, "joinable_dispatch": joinable,
               "units_explicit_current": units_expl_cur, "units_explicit_dispatch": units_expl_disp}
        rows.append(row)
        tot["n_trees"] += 1
        for k in ("n_units", "n_literals", "n_literals_explicit", "joined_current", "joinable_dispatch",
                  "units_explicit_current", "units_explicit_dispatch"):
            tot[k] += row[k]
        if lits or units_expl_cur:
            print(f"  {t['tree']:44s} units={len(units):3d} low={lowlevel:2d} lits={len(lits):3d} expl_lits={n_expl_lits:3d} "
                  f"joined={joined:2d} joinable_dispatch={joinable:2d} units_expl cur={units_expl_cur} disp={units_expl_disp}")
    out = {"_note": "探索的（r_D の定義は変えない）。docs/preregistration.md §2.8、O5。", "totals": tot, "trees": rows}
    with open(os.path.join(ROOT, args.out), "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write("\n")
    print("\ntotals:", tot)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
