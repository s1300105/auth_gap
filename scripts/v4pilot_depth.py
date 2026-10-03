#!/usr/bin/env python3
"""深さを決める予備調査（D74）: v4 を深さ 3〜8 で走らせた run を並べ、判定の候補を選ぶ。

入力: 深さの順に並べた run の置き場（`evidence/scan_v2_v4pilot_d3` …）。
出力（`--out-dir`、既定 `evidence/v4pilot_depth/`）:

* `depth_table.md` / `depth_table.json` … 深さごとの矛の数、1 段上げて新しく出た矛・消えた矛、深さの上限に当たった
  ユニット、走査の時間、打ち切り
* `contradiction_targets.json` / `contradiction_sheet.csv` … 1 段上げて新しく出た矛（組 = 木・ユニット・site・kind・宣言）
  から、段ごとに最大 15 組を seed 202610031 で選んだもの。判定表の欄は空
* `miss_targets.json` / `miss_sheet.csv` … 深さ 4 の run で D1 か D2 を明示し、その宣言への矛が無いユニットを持つ木から、
  seed 202610032 で 10 木・各 1 ユニット。**判定表（sheet）には解析器の出力を載せない**（見落としは解析器の出力を見る前に
  読む。手引き 18.2）。解析器の情報（効果の数・打ち切りの印）は targets の JSON にだけ残す

矛の組の鍵と見落としの対象の選び方は `scripts/v3_miss_sample.py` と同じ（`load_reasons`、`D_kind.explicit`）。
**判定の前に出力をコミットする。**

    .venv/bin/python scripts/v4pilot_depth.py evidence/scan_v2_v4pilot_d{3,4,5,6,7,8}
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from contradiction_by_decl import load_reasons  # noqa: E402
from runlib import load_manifest, print_warnings, run_manifests, unit_key  # noqa: E402

SEED_CONTRA = 202610031
SEED_MISS = 202610032
N_PER_STEP = 15
N_MISS = 10
MISS_RUN_DEPTH = 4


def contradiction_pairs(run_dir: str) -> set[tuple]:
    """{(木, relpath, 行, qualname, site, kind, 宣言)}: その宣言への矛が出た組。"""
    out = set()
    for key, decls in load_reasons(run_dir).items():
        for decl, findings in decls.items():
            if any(s == "contradiction" for s, _ in findings):
                out.add((*key, decl))
    return out


def run_stats(run_dir: str) -> dict:
    s = json.load(open(os.path.join(run_dir, "summary.json"), encoding="utf-8"))
    trees = s["trees"]
    cap_units = 0
    manifests, warnings = run_manifests(run_dir)
    print_warnings(warnings, os.path.basename(run_dir.rstrip("/")))
    for _, path in manifests:
        for u in load_manifest(path)["units"]:
            if "depth" in (u.get("opaque_reasons") or {}):
                cap_units += 1
    return {
        "max_depth": s["max_depth"], "n_trees": s["n_trees"], "n_units": s["n_units"],
        "n_effects": s["n_effects"], "n_effects_unique": s["n_effects_unique"],
        "elapsed_s": round(sum(t.get("elapsed_s") or 0 for t in trees), 1),
        "max_tree_elapsed_s": max((t.get("elapsed_s") or 0) for t in trees),
        "budget_skipped": sum(t.get("budget_skipped") or 0 for t in trees),
        "trees_not_ok": sum(1 for t in trees if t.get("status") != "ok"),
        "units_hitting_depth_cap": cap_units,
        "fingerprint": s.get("implementation_sha256_combined"),
    }


def effect_detail(run_dir: str, pair: tuple) -> dict:
    """組の効果の位置と、最も短い呼び出しの鎖（witness_chain）。"""
    tree, relpath, lineno, qualname, site, kind, _ = pair
    path = os.path.join(run_dir, f"{tree}.json")
    locs, chains = set(), []
    for u in load_manifest(path)["units"]:
        if unit_key(tree, u["unit"]) != (tree, relpath, lineno, qualname):
            continue
        for r in u.get("rows", []):
            if r["site"] == site and r["kind"] == kind:
                locs.add((r.get("relpath"), r.get("lineno")))
        for e in u.get("effects", []):
            if e.get("site") == site and e.get("kind") == kind:
                chains.append(e.get("witness_chain") or [])
    best = min(chains, key=len) if chains else []
    return {"locations": [f"{a}:{b}" for a, b in sorted(locs, key=lambda x: (str(x[0]), x[1] or 0))],
            "witness_chain": best, "chain_len": len(best)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("runs", nargs="+", help="深さの順に並べた run の置き場")
    ap.add_argument("--out-dir", default=os.path.join(ROOT, "evidence", "v4pilot_depth"))
    a = ap.parse_args()
    os.makedirs(a.out_dir, exist_ok=True)

    stats, pairs = [], []
    for r in a.runs:
        stats.append({"run": os.path.basename(r.rstrip("/")), **run_stats(r)})
        pairs.append(contradiction_pairs(r))
    fps = {s["fingerprint"] for s in stats}
    if len(fps) != 1:
        raise SystemExit(f"run の実装の指紋が揃っていない: {fps}")
    rows = []
    for i, s in enumerate(stats):
        new = pairs[i] - pairs[i - 1] if i else set()
        lost = pairs[i - 1] - pairs[i] if i else set()
        rows.append({**s, "contradiction_pairs": len(pairs[i]), "new_vs_prev": len(new), "lost_vs_prev": len(lost),
                     "contradiction_trees": len({p[0] for p in pairs[i]}),
                     "by_decl": {d: sum(1 for p in pairs[i] if p[-1] == d) for d in ("D1", "D2", "D3", "D4")}})
    json.dump(rows, open(os.path.join(a.out_dir, "depth_table.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    with open(os.path.join(a.out_dir, "depth_table.md"), "w", encoding="utf-8") as fh:
        fh.write("| 深さ | 矛の組 | 新しく出た | 消えた | 矛の出た木 | D1/D2/D3/D4 | 上限に当たったユニット | 走査の時間（木の合計） | 一番長い木 | 打ち切り |\n")
        fh.write("|---|---|---|---|---|---|---|---|---|---|\n")
        for r in rows:
            bd = "/".join(str(r["by_decl"][d]) for d in ("D1", "D2", "D3", "D4"))
            fh.write(f"| {r['max_depth']} | {r['contradiction_pairs']} | {r['new_vs_prev']} | {r['lost_vs_prev']} | "
                     f"{r['contradiction_trees']} | {bd} | {r['units_hitting_depth_cap']} / {r['n_units']} | "
                     f"{r['elapsed_s']} 秒 | {r['max_tree_elapsed_s']} 秒 | {r['budget_skipped']} |\n")

    # 矛: 1 段上げて新しく出た組から、段ごとに最大 15
    rng = random.Random(SEED_CONTRA)
    targets = []
    for i in range(1, len(a.runs)):
        new = sorted(pairs[i] - pairs[i - 1], key=lambda p: tuple(str(x) for x in p))
        pick = sorted(rng.sample(range(len(new)), N_PER_STEP)) if len(new) > N_PER_STEP else list(range(len(new)))
        for j in pick:
            p = new[j]
            targets.append({"id": f"C{stats[i]['max_depth']}-{len([t for t in targets if t['step'] == stats[i]['max_depth']]):02d}",
                            "step": stats[i]["max_depth"], "n_new_in_step": len(new),
                            "tree": p[0], "unit_relpath": p[1], "unit_lineno": p[2], "tool": p[3],
                            "site": p[4], "kind": p[5], "decl": p[6], **effect_detail(a.runs[i], p)})
    json.dump({"_note": "D74 の予備調査。1 段上げて新しく出た矛から段ごとに最大 15 組。判定の前にコミットする。",
               "seed": SEED_CONTRA, "n_per_step": N_PER_STEP, "targets": targets},
              open(os.path.join(a.out_dir, "contradiction_targets.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    with open(os.path.join(a.out_dir, "contradiction_sheet.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "step", "tree", "tool", "unit", "decl", "site", "kind", "locations", "witness_chain",
                    "reach", "violates", "verdict", "condition_type", "condition", "write_target", "error_class",
                    "unknown_reason", "evidence", "minutes", "ai_used", "note"])
        for t in targets:
            w.writerow([t["id"], t["step"], t["tree"], t["tool"], f"{t['unit_relpath']}:{t['unit_lineno']}", t["decl"],
                        t["site"], t["kind"], " ".join(t["locations"]), " > ".join(t["witness_chain"])] + [""] * 12)

    # 見落とし: 深さ 4 の run から 10 木・各 1 ユニット
    k = next(i for i, s in enumerate(stats) if s["max_depth"] == MISS_RUN_DEPTH)
    contra = {(p[0], p[1], p[2], p[3], p[6]) for p in pairs[k]}
    pool: dict[str, list] = {}
    manifests, _ = run_manifests(a.runs[k])
    for tree, path in manifests:
        for u in load_manifest(path)["units"]:
            ex = set((u.get("D_kind") or {}).get("explicit") or [])
            decl = "D1" if "readOnlyHint" in ex else ("D2" if "destructiveHint" in ex else None)
            if decl is None or (*unit_key(tree, u["unit"]), decl) in contra:
                continue
            truncated = sorted(n for n in (u.get("notes") or []) if str(n).startswith("TRUNCATED"))
            pool.setdefault(tree, []).append({"tree": tree, "unit": u["unit"]["qualname"], "decl": decl,
                                              "relpath": u["unit"].get("relpath"), "lineno": u["unit"].get("lineno"),
                                              "n_effects": len(u.get("effects") or []),
                                              **({"truncated": truncated} if truncated else {})})
    rng = random.Random(SEED_MISS)
    trees = sorted(pool)
    chosen = sorted(rng.sample(trees, N_MISS)) if len(trees) > N_MISS else trees
    miss = []
    for n, tree in enumerate(chosen):
        units = sorted(pool[tree], key=lambda x: (str(x["relpath"]), x["lineno"] or 0, x["unit"]))
        miss.append({"id": f"M{n:02d}", **units[rng.randrange(len(units))]})
    json.dump({"_note": "D74 の予備調査。深さ 4 の run から、見落としの候補を 10 木・各 1 ユニット。判定の前にコミットする。"
                        "n_effects と truncated は解析器の情報なので、判定表（miss_sheet.csv）には載せない。",
               "seed": SEED_MISS, "run": stats[k]["run"], "n_pool_trees": len(trees),
               "n_pool_units": sum(len(v) for v in pool.values()), "targets": miss},
              open(os.path.join(a.out_dir, "miss_targets.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    with open(os.path.join(a.out_dir, "miss_sheet.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        depth_cols = [f"d{d}_minutes_cum;d{d}_found" for d in range(0, 11)]
        w.writerow(["id", "tree", "tool", "unit", "decl"] + [c for dc in depth_cols for c in dc.split(";")]
                   + ["deepest_read", "stopped_because", "outcome", "cause", "depth", "write_target", "condition_type",
                      "evidence", "minutes_total", "ai_used", "note"])
        for t in miss:
            w.writerow([t["id"], t["tree"], t["unit"], f"{t['relpath']}:{t['lineno']}", t["decl"]] + [""] * (22 + 11))
    print(open(os.path.join(a.out_dir, "depth_table.md"), encoding="utf-8").read())
    print(f"矛の候補 {len(targets)} 組、見落としの候補 {len(miss)} 件（候補の木 {len(trees)}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
