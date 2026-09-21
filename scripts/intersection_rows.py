#!/usr/bin/env python3
"""§3 の交差行と trig の内訳を、full scan の manifest から数える。

仕様書 §3 は統一の**唯一の証拠**として交差行を事前登録している。

* 交差行 = `V_C(row) != V_A(row)` かつ `V_C(row) != V_B(row)` の行（3 腕アブレーション）。
* §3 はこれを「同一行が SELECT 系と INJECT 系の verdict を**同時に持つ**場合に限る」と
  特徴づけている。**本 script は後者（特徴づけ）で数える。3 腕は回さない。**
  したがって出力は「交差行の候補」であって、腕を回した値ではない（D36 に明記した）。
* 合格条件は **3 行以上、かつ 3 行が異なるプロジェクト由来**。
* 併せて §3 の格下げ条項（`traced` 率 20% 未満なら SELECT は構造的主張に格下げ。
  **撤回しない**と仕様書が書いた条項）の判定に要る trig の内訳も出す。

数える単位は **(ユニット, site, slot)**。効果行は呼び出し経路ごとに複製されるので
（`docs/open_questions.md` O18）、行をそのまま数えると複製で水増しされる。

    .venv/bin/python scripts/intersection_rows.py evidence/scan_v2_run4
    .venv/bin/python scripts/intersection_rows.py evidence/scan_v2_run4 --md docs/intersection_rows.md
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#: §3 の閾値。**経験的根拠は無く、事前に固定したことだけが根拠である**（仕様書の明記事項）。
MIN_ROWS = 3
MIN_PROJECTS = 3
#: §3 の格下げ条項の閾値。
TRACED_GATE = 0.20

SELECT_VERDICTS = frozenset({"GAP_SELECT", "INVENTORY"})
INJECT_VERDICTS = frozenset({"GAP_INJECT", "GAP_DRIFT"})


def scan(evidence_dir: str) -> dict:
    trig: collections.Counter = collections.Counter()
    rows: dict[str, set] = collections.defaultdict(set)
    n_units = 0
    for fn in sorted(os.listdir(evidence_dir)):
        if not fn.endswith(".json") or fn in ("summary.json", "contradictions.json"):
            continue
        with open(os.path.join(evidence_dir, fn), encoding="utf-8") as fh:
            man = json.load(fh)
        tree = fn[:-5]
        for u in man.get("units", []):
            n_units += 1
            trig[(u.get("trig") or {}).get("mode")] += 1
            for r in u.get("rows", []):
                v = set(r.get("verdicts", []))
                # **`Leak` だけで説明できる行と OPAQUE 行、D だけで説明できる行は数えない**
                # （§3）。UNKNOWN と CONTRADICTION しか持たない行はここで落ちる。
                if (v & SELECT_VERDICTS) and (v & INJECT_VERDICTS):
                    rows[tree].add((u["unit"]["qualname"], r["site"], r["slot"]))
    n_rows = sum(len(v) for v in rows.values())
    traced = trig.get("traced", 0)
    return {
        "evidence_dir": os.path.relpath(evidence_dir, ROOT),
        "n_units": n_units,
        "trig": {k: v for k, v in sorted(trig.items(), key=lambda kv: str(kv[0]))},
        "traced_ratio": (traced / n_units) if n_units else None,
        "traced_gate_pass": (traced / n_units >= TRACED_GATE) if n_units else None,
        "n_intersection_rows": n_rows,
        "n_projects": len(rows),
        "pass_rows": n_rows >= MIN_ROWS,
        "pass_projects": len(rows) >= MIN_PROJECTS,
        "by_project": {t: sorted(map(list, v)) for t, v in sorted(rows.items())},
    }


def to_md(res: dict) -> str:
    out: list[str] = []
    out.append("# §3 の交差行（統一の唯一の証拠）と trig の内訳")
    out.append("")
    out.append(f"再現: `python scripts/intersection_rows.py {res['evidence_dir']}`")
    out.append("")
    out.append("**この表は 3 腕アブレーションの値ではない。** §3 が与えた特徴づけ")
    out.append("（同一行が SELECT 系と INJECT 系の verdict を同時に持つ）で数えた**候補**である。")
    out.append("数える単位は (ユニット, site, slot)。効果行は呼び出し経路ごとに複製されるため")
    out.append("（`docs/open_questions.md` O18）、行をそのまま数えない。")
    out.append("")
    out.append("| 項目 | 実測 | §3 の条件 | 判定 |")
    out.append("|---|---|---|---|")
    out.append(f"| 交差行の候補 | {res['n_intersection_rows']} | {MIN_ROWS} 以上 | "
               f"{'○' if res['pass_rows'] else '×'} |")
    out.append(f"| 由来プロジェクト数 | {res['n_projects']} | {MIN_PROJECTS} 以上 | "
               f"{'○' if res['pass_projects'] else '×'} |")
    ratio = res["traced_ratio"]
    out.append(f"| `trig = traced` のユニット | {res['trig'].get('traced', 0)} / {res['n_units']} = "
               f"{100 * ratio:.1f}% | {TRACED_GATE:.0%} 以上 | "
               f"{'○' if res['traced_gate_pass'] else '×'} |")
    out.append("")
    if not res["traced_gate_pass"]:
        out.append("**§3 の格下げ条項が発火している。** 仕様書の文言: 「traced 率が 20% 未満なら")
        out.append("SELECT の野外評価は成立しないので、その時点で SELECT は fixture + ケーススタディのみの")
        out.append("構造的主張に格下げする。**この条項は撤回しない。**」")
        out.append("")
    out.append("## 由来")
    out.append("")
    if not res["by_project"]:
        out.append("交差行の候補なし。")
    for t, items in res["by_project"].items():
        out.append(f"- `{t}`（{len(items)} 行）")
        for q, site, slot in items:
            out.append(f"  - `{q}` / `{site}` / slot `{slot}`")
    out.append("")
    out.append("## 決定")
    out.append("")
    out.append("`docs/decisions.md` D36: 統一主張と等級づけによる判別は主張から降ろし、")
    out.append("「宣言 D と実効 M の照合」1 本を主軸にする。D10 の二択は格下げ分岐を採る。")
    out.append("")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("evidence_dir", help="evidence/scan_v2_<label>（木ごとの manifest がある所）")
    ap.add_argument("--md", help="Markdown をこのパスに書く")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    d = args.evidence_dir if os.path.isabs(args.evidence_dir) else os.path.join(ROOT, args.evidence_dir)
    if not os.path.isdir(d):
        raise SystemExit(f"{d} が無い")
    res = scan(d)

    if args.json:
        json.dump(res, sys.stdout, ensure_ascii=False, indent=1)
        print()
    else:
        print(to_md(res))
    if args.md:
        with open(args.md if os.path.isabs(args.md) else os.path.join(ROOT, args.md), "w", encoding="utf-8") as fh:
            fh.write(to_md(res))
        print(f"\nwrote {args.md}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
