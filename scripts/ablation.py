#!/usr/bin/env python3
"""§3 の 3 腕アブレーションと交差行の測定。

**統一の唯一の証拠は事前登録した交差行数である。**
trig / val / gate は伝播機構を共有しないので、「一つの解析」ではなく
「三つの別々に計算される座標の上の一つの判定」である。それでも統一を主張する
なら、3 座標のうち 2 つを同時に必要とする行が実在しなければならない。

* 腕 A = trig を計算し **val を全位置で OP に固定**
* 腕 B = val を計算し **trig を全て assumed に固定**
* 腕 C = 完全版
* **ゲートは 3 腕とも入っている。3 腕は同一バイナリのフラグ違いである**
  （`authgap/analyze.py` の `arm` 引数。別実装なら不合格）。

行の verdict は集合 `V(row) ⊆ {GAP_SELECT, GAP_INJECT, GAP_DRIFT,
CONTRADICTION, INVENTORY, UNKNOWN}`。行は `(unit id, effect, position)`。

**交差行** = `V_C(row) ≠ V_A(row)` かつ `V_C(row) ≠ V_B(row)`。
Def 7 では SELECT は trig にのみ、INJECT は val にのみ依存するので、
この条件を満たすのは**同一行が SELECT 系と INJECT 系の verdict を同時に持つ場合に
限る**。すなわち「MODEL セレクタから traced で到達されるユニット入口の下に、
MODEL 値が weak validator しか通らない制御位置がある」形である。

数えない行（§3）:

* `OPAQUE` 行（`UNKNOWN` を含む行）
* `Leak`（Def 5-b）だけで説明できる行
* D だけで説明できる行（`INVENTORY` / `CONTRADICTION` / `GAP_DRIFT` のみの行）
* fixture 由来と自作ケーススタディ由来

**閾値**: 交差行 ≥ 3、かつ 3 行が異なるプロジェクト由来
（**PraisonAI 全体を 1 プロジェクトとして数える**）。
1〜2 行なら「統一の証拠は逸話的」と書き、0 なら統一主張を取り下げて
三部品として報告する。**閾値 3 に経験的根拠は無く、事前に固定することだけが
根拠であると本文に明記する。**
"""

from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass, field

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from authgap.report import canonical_json, manifest_json  # noqa: E402
from authgap.runner import RunConfig, run  # noqa: E402

#: 事前登録した閾値。**経験的根拠は無い。事前に固定することだけが根拠。**
INTERSECTION_THRESHOLD = 3

#: SELECT 系 / INJECT 系の verdict。
SELECT_FAMILY = frozenset({"GAP_SELECT"})
INJECT_FAMILY = frozenset({"GAP_INJECT"})
#: D だけで説明できる verdict（交差行に数えない）。
D_ONLY = frozenset({"INVENTORY", "CONTRADICTION", "GAP_DRIFT"})


@dataclass
class TreeArms:
    tree: str
    project: str
    rows: dict[str, dict[str, list[str]]] = field(default_factory=dict)


def row_key(unit_id: str, row: dict) -> str:
    return f"{unit_id}|{row['kind']}@{row['site']}|{row.get('slot')}"


def collect_arm(src_root: str, population: str, arm: str) -> dict[str, list[str]]:
    res = run(RunConfig(src_root=src_root, population=population, full=True, arm=arm))
    man = manifest_json(res, run_id=f"ablation-{arm}", volatile=False)
    out: dict[str, list[str]] = {}
    for u in man["units"]:
        for row in u["rows"]:
            out.setdefault(row_key(u["unit"]["unit_id"], row), []).extend(row["verdicts"])
    return {k: sorted(set(v)) for k, v in out.items()}


def analyse_tree(src_root: str, project: str, population: str, out_dir: str | None) -> TreeArms:
    ta = TreeArms(tree=src_root, project=project)
    for arm in ("A", "B", "C"):
        rows = collect_arm(src_root, population, arm)
        for key, verdicts in rows.items():
            ta.rows.setdefault(key, {})[arm] = verdicts
        if out_dir:
            d = os.path.join(out_dir, arm)
            os.makedirs(d, exist_ok=True)
            name = os.path.basename(os.path.normpath(src_root)) + ".json"
            with open(os.path.join(d, name), "w", encoding="utf-8") as fh:
                fh.write(canonical_json({"tree": src_root, "arm": arm, "rows": rows}))
    return ta


def intersection_rows(ta: TreeArms) -> list[dict]:
    """§3 の交差行を抜き出す。"""
    out: list[dict] = []
    for key in sorted(ta.rows):
        arms = ta.rows[key]
        a, b, c = set(arms.get("A", [])), set(arms.get("B", [])), set(arms.get("C", []))
        if c == a or c == b:
            continue
        if "UNKNOWN" in c:
            continue  # OPAQUE 行は数えない
        if not (c & SELECT_FAMILY and c & INJECT_FAMILY):
            continue  # 定義上ここしか残らないが、明示的に検査する
        if not (c - D_ONLY):
            continue  # D だけで説明できる行は除く
        out.append(
            {
                "row": key,
                "project": ta.project,
                "V_A": sorted(a),
                "V_B": sorted(b),
                "V_C": sorted(c),
            }
        )
    return out


def single_coordinate_rows(ta: TreeArms) -> dict[str, list[str]]:
    """**交差行ではない**が §3 が別表で報告せよと言う「単一座標のゲート寄与」。

    (i) callee の `confirm()` が SELECT を clear する、
    (ii) caller の承認 hook が `req_val` を引き上げる、はそれぞれ腕 B のみ・
    腕 A のみとしか差が出ないので**定義上 0 行**であり、交差行に数えない。
    """
    only_a: list[str] = []
    only_b: list[str] = []
    for key in sorted(ta.rows):
        arms = ta.rows[key]
        a, b, c = set(arms.get("A", [])), set(arms.get("B", [])), set(arms.get("C", []))
        if c != a and c == b:
            only_a.append(key)
        elif c != b and c == a:
            only_b.append(key)
    return {"differs_from_A_only": only_a, "differs_from_B_only": only_b}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "trees",
        nargs="+",
        help="解析対象の木。プロジェクト名は docs/frame.csv の repo 列から引く"
        "（`path:project` で上書き可）",
    )
    ap.add_argument("--population", default="mcp_server")
    ap.add_argument("--evidence", default=os.path.join(ROOT, "evidence", "ablation"))
    ap.add_argument("--md", default=os.path.join(ROOT, "docs", "intersection_rows.md"))
    args = ap.parse_args()

    all_rows: list[dict] = []
    singles: dict[str, dict[str, list[str]]] = {}
    per_tree: list[dict] = []
    frame = _load_frame()
    for spec in args.trees:
        path, _, project = spec.partition(":")
        project = project or _project_of(path, frame)
        if not os.path.isdir(path):
            print(f"SKIP {path}: 木が無い", file=sys.stderr)
            continue
        ta = analyse_tree(path, project, args.population, args.evidence)
        rows = intersection_rows(ta)
        all_rows += rows
        singles[project] = single_coordinate_rows(ta)
        per_tree.append({"tree": path, "project": project, "n_rows": len(ta.rows), "n_intersection": len(rows)})
        print(f"{path}  行 {len(ta.rows)}  交差行 {len(rows)}")

    projects = sorted({r["project"] for r in all_rows})
    n = len(all_rows)
    # **同じリポジトリの別コミットを別プロジェクトとして数えない。**
    ok = n >= INTERSECTION_THRESHOLD and len(projects) >= INTERSECTION_THRESHOLD
    print(f"\n交差行 {n} 行 / {len(projects)} プロジェクト（閾値 {INTERSECTION_THRESHOLD}）: "
          f"{'合格' if ok else '不合格'}")
    if n == 0:
        print("→ 統一主張を取り下げて三部品として報告する（§3）")
    elif n < INTERSECTION_THRESHOLD:
        print("→ 「統一の証拠は逸話的」と書く（§3）")
    elif len(projects) < INTERSECTION_THRESHOLD:
        print(
            f"→ 行数は足りるが**プロジェクトが {len(projects)} 件しかない**。"
            "§3 は「3 行が異なるプロジェクト由来」を要求するので不合格。"
            "別プロジェクトの木を足して測り直すこと"
        )

    os.makedirs(os.path.dirname(args.md), exist_ok=True)
    with open(args.md, "w", encoding="utf-8") as fh:
        fh.write(_markdown(all_rows, projects, per_tree, singles, ok))
    print(f"wrote {args.md}")
    return 0


def _load_frame() -> dict[str, str]:
    """`docs/frame.csv` の `path -> repo` 表。

    **プロジェクトの同定は repo 単位で行う。** 同じリポジトリの別コミットを
    別プロジェクトとして数えると「≥ 3 プロジェクト」が自明に満たされ、
    §3 の条件が意味を失う（仕様書が「PraisonAI 全体を 1 プロジェクトとして
    数える」と明記しているのと同じ趣旨）。
    """
    import csv

    path = os.path.join(ROOT, "docs", "frame.csv")
    out: dict[str, str] = {}
    if not os.path.exists(path):
        return out
    with open(path, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            out[os.path.normpath(row["path"])] = row["repo"]
    return out


def _project_of(path: str, frame: dict[str, str]) -> str:
    rel = os.path.normpath(os.path.relpath(os.path.abspath(path), ROOT))
    if rel in frame:
        return frame[rel]
    return os.path.basename(os.path.normpath(path))


def _markdown(rows, projects, per_tree, singles, ok) -> str:
    lines = [
        "# 交差行（§3 の 3 腕アブレーション）",
        "",
        "**統一の唯一の証拠。** trig / val / gate は伝播機構を共有しないので、",
        "3 座標のうち 2 つを同時に必要とする行が実在しなければ「一つの解析」とは",
        "書けない。3 腕は `authgap/analyze.py` の `arm` 引数によるフラグ違いであり、",
        "**別実装ではない**（§3 の要求）。",
        "",
        "再現: `python scripts/ablation.py <木> [<木> ...]`",
        "",
        f"- 交差行 **{len(rows)}** 行 / **{len(projects)}** プロジェクト",
        f"- 事前登録した閾値 **{INTERSECTION_THRESHOLD}**（**経験的根拠は無い。"
        "事前に固定することだけが根拠である**）",
        f"- 判定: **{'合格' if ok else '不合格'}**",
        "",
        "数えない行: `UNKNOWN` を含む行（OPAQUE 行）、`Leak` だけで説明できる行、",
        "D だけで説明できる行（INVENTORY / CONTRADICTION / GAP_DRIFT のみ）、",
        "fixture 由来と自作ケーススタディ由来。",
        "",
        "## 木ごとの内訳",
        "",
        "| 木 | プロジェクト | 行数 | 交差行 |",
        "|---|---|---|---|",
    ]
    for t in per_tree:
        lines.append(f"| `{t['tree']}` | {t['project']} | {t['n_rows']} | {t['n_intersection']} |")
    lines += ["", "## 交差行", ""]
    if not rows:
        lines.append("交差行は 0 行。**統一主張を取り下げて三部品として報告する**（§3）。")
    else:
        lines += ["| 行 | プロジェクト | V_A | V_B | V_C |", "|---|---|---|---|---|"]
        for r in rows:
            lines.append(
                f"| `{r['row']}` | {r['project']} | {','.join(r['V_A']) or '-'} | "
                f"{','.join(r['V_B']) or '-'} | {','.join(r['V_C'])} |"
            )
    lines += [
        "",
        "## 単一座標のゲート寄与（**交差行ではない。別表**）",
        "",
        "§3 が明記するとおり、(i) callee の `confirm()` が SELECT を clear する / ",
        "(ii) caller の承認 hook が `req_val` を引き上げる、はそれぞれ腕 B のみ・",
        "腕 A のみとしか差が出ないので**定義上 0 行**であり交差行に数えない。",
        "ここには「腕 A とだけ差が出た行 / 腕 B とだけ差が出た行」の件数を出す。",
        "",
        "| プロジェクト | 腕 A とだけ差 | 腕 B とだけ差 |",
        "|---|---|---|",
    ]
    for proj in sorted(singles):
        s = singles[proj]
        lines.append(f"| {proj} | {len(s['differs_from_A_only'])} | {len(s['differs_from_B_only'])} |")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
