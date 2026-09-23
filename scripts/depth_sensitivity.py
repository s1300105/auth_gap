#!/usr/bin/env python3
"""呼び出しの深さの上限（`MAX_DEPTH`）の感度分析（`docs/open_questions.md` O29）。

`scripts/scan_v2.py --max-depth <d>` で取った full scan を並べ、**費用と増える件数と
消える件数**を出す。先頭の run を基準にする（**同じ条件で同時に走らせた `max_depth=3`
を基準に置く**。所要時間は同時に走らせた本数で変わるので、別の日の run と時間を比べない）。

    .venv/bin/python scripts/depth_sensitivity.py evidence/scan_v2_depth3_sens \\
        evidence/scan_v2_depth4_sens evidence/scan_v2_depth5_sens --md docs/depth_sensitivity.md

数え方（分母を明示する。CLAUDE.md 規則 3）:

* **効果**: manifest の `effects` の件数（重複を含む生の件数。D50 / D51 の「効果」と同じ）。
  消えた / 増えたは 2 つの粒度で集合差を取る。**位置** = (ユニットの鍵, site, kind, relpath,
  lineno)、**経路** = 位置 + (`entry_lineno`, `witness_chain`)。ユニットの鍵は
  `compare_scans.py` と同じ `木|unit_id|qualname|relpath:lineno`。**同じ位置に別の経路で
  届く効果がある**（run10 で位置が同じで経路の違う組が 500 以上）ので、位置だけでは
  経路の消失が見えない。
* **`db_unresolved`**: ユニットごとの記録の合計（D49）。「一意」は (木, relpath, lineno)。
  **未解決率 = `db_unresolved` / (DB 効果 + `db_unresolved`)**（D50 / D51 と同じ定義）。
* **`GAP_INJECT`（一意な位置）**: (木, qualname, site, slot, relpath, lineno)。D50 / D51 と同じ鍵。
* **CONTRADICTION**: (木, qualname, site, kind)。`compare_scans.py` と同じ鍵。
* **深さの上限に当たったユニット**: `cap_hits` に `depth` を持つユニットの数。
  **上げた深さでも当たるなら、その深さでもまだ打ち切られている**という意味。
* **費用**: 木ごとの `elapsed_s`（summary.json）と、tree budget（180 秒）で打ち切られた木。
  ユニットごとの `WALL_CLOCK_CAP` に当たったユニット（`cap_hits` の `wall_clock`）も数える。
"""

from __future__ import annotations

import argparse
import collections
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(run_dir: str) -> dict:
    summary = json.load(open(os.path.join(run_dir, "summary.json"), encoding="utf-8"))
    effects: set[tuple] = set()
    paths: set[tuple] = set()
    n_effects = 0
    kinds: collections.Counter = collections.Counter()
    sub_kinds: collections.Counter = collections.Counter()
    inj: set[tuple] = set()
    contra: set[tuple] = set()
    units: set[str] = set()
    cap_hits: collections.Counter = collections.Counter()
    depth_units = 0
    db_unres = 0
    db_unres_unique: set[tuple] = set()
    verdict_rows: collections.Counter = collections.Counter()
    for fn in sorted(os.listdir(run_dir)):
        if not fn.endswith(".json") or fn in ("summary.json", "contradictions.json"):
            continue
        t = fn[:-5]
        man = json.load(open(os.path.join(run_dir, fn), encoding="utf-8"))
        for u in man.get("units", []):
            un = u["unit"]
            uk = f'{t}|{un["unit_id"]}|{un["qualname"]}|{un.get("relpath")}:{un.get("lineno")}'
            units.add(uk)
            hits = set(u.get("cap_hits") or [])
            for h in hits:
                cap_hits[h] += 1
            if "depth" in hits:
                depth_units += 1
            for e in u.get("effects", []):
                pos = (uk, e["site"], e["kind"], e["relpath"], e["lineno"])
                effects.add(pos)
                paths.add(pos + (e.get("entry_lineno"), tuple(e.get("witness_chain") or ())))
                n_effects += 1
                kinds[e["kind"]] += 1
                sub_kinds[e.get("sub_kind") or "-"] += 1
            for x in u.get("db_unresolved", []) or []:
                db_unres += 1
                db_unres_unique.add((t, x["relpath"], x["lineno"]))
            for r in u.get("rows", []):
                for v in r.get("verdicts", []):
                    verdict_rows[v] += 1
                if "GAP_INJECT" in r.get("verdicts", []):
                    inj.add((t, un["qualname"], r["site"], r.get("slot"), r["relpath"], r["lineno"]))
                if "CONTRADICTION" in r.get("verdicts", []):
                    contra.add((t, un["qualname"], r["site"], r["kind"]))
    trees = {x["tree"]: x for x in summary["trees"]}
    return {"summary": summary, "trees": trees, "effects": effects, "paths": paths,
            "n_effects": n_effects, "kinds": kinds,
            "sub_kinds": sub_kinds, "inj": inj, "contra": contra, "units": units,
            "cap_hits": cap_hits, "depth_units": depth_units, "db_unres": db_unres,
            "db_unres_unique": db_unres_unique, "verdict_rows": verdict_rows}


def _rate(r: dict) -> float:
    db = r["kinds"]["DB"]
    den = db + r["db_unres"]
    return r["db_unres"] / den if den else 0.0


def to_md(dirs: list[str], runs: list[dict]) -> str:
    names = [os.path.basename(d) for d in dirs]
    base = runs[0]
    o: list[str] = []
    o.append("# 深さの上限の感度分析（O29）")
    o.append("")
    o.append("再現: `python scripts/depth_sensitivity.py " + " ".join(os.path.relpath(d, ROOT) for d in dirs) + "`")
    o.append("")
    o.append("**解析器の `MAX_DEPTH` は 3 のまま**（`authgap/ir.py`）。各 run は `scripts/scan_v2.py --max-depth`"
             " で `Options.max_depth` だけを変えた。基準は先頭の run。")
    o.append("")
    hdr = "| 項目 | " + " | ".join(f"`{n}`" for n in names) + " |"
    sep = "|---|" + "---|" * len(names)

    def row(label: str, vals: list, fmt=str) -> None:
        o.append(f"| {label} | " + " | ".join(fmt(v) for v in vals) + " |")

    o.append("## 件数")
    o.append("")
    o.append(hdr)
    o.append(sep)
    row("`max_depth`", [r["summary"].get("max_depth") for r in runs])
    row("解析器の commit", [str(r["summary"].get("analyzer_commit", ""))[:7] for r in runs])
    row("ユニット", [len(r["units"]) for r in runs])
    row("効果（生の件数）", [r["n_effects"] for r in runs])
    row("効果の位置（一意）", [len(r["effects"]) for r in runs])
    row("効果の経路（一意）", [len(r["paths"]) for r in runs])
    for k in sorted(set().union(*(r["kinds"] for r in runs))):
        row(f"　{k}", [r["kinds"][k] for r in runs])
    row("`db_unresolved`（一意）", [f'{r["db_unres"]}（{len(r["db_unres_unique"])}）' for r in runs])
    row("**DB 未解決率**", [f"{100 * _rate(r):.1f}%" for r in runs])
    row("`GAP_INJECT`（一意な位置）", [len(r["inj"]) for r in runs])
    row("CONTRADICTION（ユニット × site × kind）", [len(r["contra"]) for r in runs])
    for v in sorted(set().union(*(r["verdict_rows"] for r in runs))):
        row(f"`{v}` の行", [r["verdict_rows"][v] for r in runs])
    row("深さの上限に当たったユニット", [r["depth_units"] for r in runs])
    for h in sorted(set().union(*(r["cap_hits"] for r in runs))):
        if h != "depth":
            row(f"`cap_hits` の `{h}`（ユニット）", [r["cap_hits"][h] for r in runs])
    o.append("")

    o.append("## 基準との集合差（**消えた側が回帰**）")
    o.append("")
    o.append("| 比較 | 消えたユニット | 増えたユニット | 消えた効果の位置 | 増えた効果の位置 |"
             " 消えた経路 | 増えた経路 | 消えた `GAP_INJECT` |"
             " 増えた `GAP_INJECT` | 消えた CONTRADICTION | 増えた CONTRADICTION |")
    o.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for n, r in zip(names[1:], runs[1:], strict=True):
        o.append(f"| `{names[0]}` → `{n}` | {len(base['units'] - r['units'])} | {len(r['units'] - base['units'])} | "
                 f"{len(base['effects'] - r['effects'])} | {len(r['effects'] - base['effects'])} | "
                 f"{len(base['paths'] - r['paths'])} | {len(r['paths'] - base['paths'])} | "
                 f"{len(base['inj'] - r['inj'])} | {len(r['inj'] - base['inj'])} | "
                 f"{len(base['contra'] - r['contra'])} | {len(r['contra'] - base['contra'])} |")
    o.append("")
    for n, r in zip(names[1:], runs[1:], strict=True):
        added = sorted(r["contra"] - base["contra"])
        removed = sorted(base["contra"] - r["contra"])
        if added or removed:
            o.append(f"### CONTRADICTION の差（`{names[0]}` → `{n}`）")
            o.append("")
            for t, q, s, k in removed:
                o.append(f"- 消えた: `{t}` / `{q}` / `{k}@{s}`")
            for t, q, s, k in added:
                o.append(f"- 増えた: `{t}` / `{q}` / `{k}@{s}`")
            o.append("")

    o.append("## 費用")
    o.append("")
    o.append(hdr)
    o.append(sep)
    tot = [sum(x.get("elapsed_s", 0) for x in r["trees"].values() if x.get("status") == "ok") for r in runs]
    row("所要時間の合計（秒）", tot, lambda v: f"{v:.1f}")
    row("tree budget で打ち切られた木",
        [", ".join(sorted(t for t, x in r["trees"].items() if x.get("budget_skipped"))) or "なし" for r in runs])
    row("失敗した木", [sum(1 for x in r["trees"].values() if x.get("status") != "ok") for r in runs])
    o.append("")
    o.append("### 所要時間が大きい木（基準の上位と、どれかの run で 30 秒以上）")
    o.append("")
    o.append("| 木 | " + " | ".join(f"`{n}`" for n in names) + " |")
    o.append(sep)
    all_trees = sorted(base["trees"])
    pick = [t for t in all_trees
            if any((r["trees"].get(t) or {}).get("elapsed_s", 0) >= 30 for r in runs)]
    for t in sorted(pick, key=lambda t: -max((r["trees"].get(t) or {}).get("elapsed_s", 0) for r in runs)):
        o.append(f"| `{t}` | " + " | ".join(
            f'{(r["trees"].get(t) or {}).get("elapsed_s", "-")}'
            + ("（打ち切り）" if (r["trees"].get(t) or {}).get("budget_skipped") else "")
            for r in runs) + " |")
    o.append("")

    o.append("## 木ごとの効果の増減（基準との差が大きい順、上位 20）")
    o.append("")
    per: dict[str, list[int]] = collections.defaultdict(lambda: [0] * len(runs))
    for i, r in enumerate(runs):
        for (uk, *_rest) in r["effects"]:
            per[uk.split("|", 1)[0]][i] += 1
    ordered = sorted(per.items(), key=lambda kv: -abs(kv[1][-1] - kv[1][0]))
    o.append("| 木 | " + " | ".join(f"`{n}`" for n in names) + " |")
    o.append(sep)
    for t, vals in ordered[:20]:
        if vals[-1] == vals[0] and all(v == vals[0] for v in vals):
            continue
        o.append(f"| `{t}` | " + " | ".join(str(v) for v in vals) + " |")
    o.append("")
    return "\n".join(o)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("runs", nargs="+", help="先頭が基準")
    ap.add_argument("--md")
    ap.add_argument("--dump", help="基準と最後の run の差（効果の位置・経路・GAP_INJECT）を JSON で書く（抜き取り検証用）")
    args = ap.parse_args(argv)
    runs = [load(d) for d in args.runs]
    md = to_md(args.runs, runs)
    if args.md:
        with open(args.md, "w", encoding="utf-8") as fh:
            fh.write(md + "\n")
    try:
        print(md)
    except BrokenPipeError:
        pass
    if args.dump:
        b, a = runs[0], runs[-1]
        out = {k: {"added": sorted([list(x) for x in a[k] - b[k]], key=str),
                   "removed": sorted([list(x) for x in b[k] - a[k]], key=str)}
               for k in ("effects", "paths", "inj", "contra")}
        with open(args.dump, "w", encoding="utf-8") as fh:
            json.dump(out, fh, ensure_ascii=False, indent=0)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
