#!/usr/bin/env python3
"""F0a の複数 run を並べ、差を「処理系の変更」と「解析器の修正」に分解する（D14 / D16）。

既定の 3 run（標本は `docs/corpus_sample.json`。run3 はアプリ母集団の取り違えを
訂正した後の標本だが、訂正した 1 木はどちらの repo でもユニット 0 件なので率は変わらない）:

* ``run1``       — 解析器 9c2bb11 相当 / Python 3.10（直す前）
* ``run1py312``  — 解析器は run1 と同一 / Python 3.12（処理系だけ替えた）
* ``run3``       — 解析器を D17 と D17 改訂 2 で修正（854f71b）/ Python 3.12

``run1py312 - run1`` が処理系の効果、``run3 - run1py312`` が解析器の修正の効果である。
**どちらか一方の run だけを報告しない**（D14）。

``run2``（0662b39、D17 の最初の修正）は**中間状態として残す**。敵対的レビューで
false-clean 5 系統が見つかった版なので、関門の数字には使わない（D17 改訂 2）。
並べたいときは引数で渡す: ``python scripts/compare_f0a_runs.py run2=evidence/f0a_run2/f0a.json run3=evidence/f0a_run3/f0a.json``

出力: `docs/f0a_runs.md`

使い方::

    python scripts/compare_f0a_runs.py
    python scripts/compare_f0a_runs.py run1=evidence/f0a/f0a.json run2=evidence/f0a_run2/f0a.json
"""

from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "f0a_runs.md")

DEFAULT_RUNS = (
    ("run1", "evidence/f0a/f0a.json"),
    ("run1py312", "evidence/f0a_run1py312/f0a.json"),
    ("run3", "evidence/f0a_run3/f0a.json"),
)

#: §10 の関門（`scripts/f0a.py` と同じ値。**動かさない**）。
GATES = {
    "in_tree_resolution_ratio_sites": (">=", 0.50),
    "validator_holding_ratio": (">=", 0.05),
    "opaque_ratio_primary_slots_sites": ("<=", 0.40),
}

#: 表に出す指標 `(表示名, 取り出し関数, 率か)`。
METRICS = (
    ("解析した木", lambda s: s["n_trees"], False),
    ("ユニット 0 件の木（フレームの雑音 + 取りこぼし）", lambda s: s["n_trees_no_units"], False),
    ("parse 失敗ファイル", lambda s: s["parse_failures"], False),
    ("ユニット", lambda s: s["n_units"], False),
    ("危険効果を持つユニット（偽陽性クラス除外）", lambda s: s["n_units_with_dangerous_effect_fp_excluded"], False),
    ("効果サイト", lambda s: s.get("n_effect_sites"), False),
    ("効果行", lambda s: s.get("n_effect_rows"), False),
    ("in_tree_resolution_ratio（サイト、**関門**）", lambda s: s.get("in_tree_resolution_ratio_sites"), True),
    ("in_tree_resolution_ratio（行、併記）", lambda s: s.get("in_tree_resolution_ratio"), True),
    ("opaque 率 主 slot（サイト、**関門**）", lambda s: s.get("opaque_ratio_primary_slots_sites"), True),
    ("opaque 率 主 slot（行、併記）", lambda s: s.get("opaque_ratio_primary_slots"), True),
    ("remote 率（関門ではない）", lambda s: s.get("remote_ratio"), True),
    ("validator 保有（構文的形状、**関門**）", lambda s: s.get("validator_holding_ratio"), True),
    ("annotation を持つユニット", lambda s: s["D"]["n_annotations_present"], False),
    ("D_unknown", lambda s: s["D"]["n_d_unknown"], False),
    ("r_kind（偽陽性クラス除外）", lambda s: s["D"]["r_kind_fp_excluded"], True),
    ("r_op", lambda s: s["D"]["r_op"], True),
    ("r_D（和集合、偽陽性クラス除外）", lambda s: s["D"]["r_D_fp_excluded"], True),
)


def _fmt(x, rate: bool) -> str:
    if x is None:
        return "—"
    return f"{x:.1%}" if rate else str(x)


def _delta(a, b, rate: bool) -> str:
    if a is None or b is None:
        return "—"
    d = b - a
    if rate:
        return f"{d * 100:+.1f} pt"
    return f"{d:+d}" if isinstance(d, int) else f"{d:+}"


def _gate(key: str, x) -> str:
    op, thr = GATES[key]
    if x is None:
        return "不明"
    ok = x >= thr if op == ">=" else x <= thr
    return "○" if ok else "×"


def main(argv: list[str]) -> int:
    runs = [tuple(a.split("=", 1)) for a in argv] if argv else list(DEFAULT_RUNS)
    loaded: list[tuple[str, dict]] = []
    for label, rel in runs:
        path = rel if os.path.isabs(rel) else os.path.join(ROOT, rel)
        if not os.path.exists(path):
            print(f"{path} が無い（{label} をまだ走らせていない）", file=sys.stderr)
            return 2
        with open(path, encoding="utf-8") as fh:
            loaded.append((label, json.load(fh)))

    samples = {d.get("run_meta", {}).get("sample") for _l, d in loaded}
    lines = [
        "# F0a の run の比較（D14 / D16 / D17）",
        "",
        "再現: `python scripts/compare_f0a_runs.py`",
        "",
        "**同じ標本を同じ手続きで測った run だけを並べる。** 差の分解:",
        "",
        "* `run1py312 − run1` = **処理系の変更**（3.10 → 3.12。解析器は同一）",
        "* `run2 − run1py312` = **解析器の修正**（D17。処理系は同一）",
        "",
        "**どちらか一方の run だけを論文に書かない。** 関門の閾値は §10 の値で固定。",
        "",
        "| run | 解析器 commit | 未コミット変更 | Python | 標本 | 実行日時 |",
        "|---|---|---|---|---|---|",
    ]
    for label, d in loaded:
        m = d.get("run_meta", {})
        commit = (m.get("analyzer_commit") or "")[:9]
        lines.append(
            f"| {label} | `{commit}` | {m.get('analyzer_dirty')} | {m.get('python', '3.10.12（記録なし）')} | "
            f"`{m.get('sample')}` | {m.get('run_at')} |"
        )
    if len(samples) != 1:
        lines += ["", f"**警告: 標本が run 間で違う（{sorted(map(str, samples))}）。差を分解に使えない。**"]

    pops = sorted({p for _l, d in loaded for p in d["populations"]})
    for pop in pops:
        lines += ["", f"## 母集団: {pop}", ""]
        header = "| 指標 | " + " | ".join(label for label, _d in loaded)
        if len(loaded) == 3:
            header += " | Δ 処理系 | Δ 解析器"
        lines.append(header + " |")
        lines.append("|---" * (1 + len(loaded) + (2 if len(loaded) == 3 else 0)) + "|")
        for name, get, rate in METRICS:
            vals = []
            for _label, d in loaded:
                s = d["populations"].get(pop)
                try:
                    vals.append(get(s) if s is not None else None)
                except (KeyError, TypeError):
                    vals.append(None)
            row = f"| {name} | " + " | ".join(_fmt(v, rate) for v in vals)
            if len(loaded) == 3:
                row += f" | {_delta(vals[0], vals[1], rate)} | {_delta(vals[1], vals[2], rate)}"
            lines.append(row + " |")
        lines += ["", "**§10 の関門（run ごと）**", "", "| 関門 | " + " | ".join(lab for lab, _d in loaded) + " |",
                  "|---" * (1 + len(loaded)) + "|"]
        for key, (op, thr) in GATES.items():
            cells = []
            for _label, d in loaded:
                s = d["populations"].get(pop) or {}
                cells.append(_gate(key, s.get(key)))
            lines.append(f"| `{key}` {op} {thr:.0%} | " + " | ".join(cells) + " |")
        branches = [(d["populations"].get(pop) or {}).get("D", {}).get("branch", "—") for _l, d in loaded]
        lines += [
            "",
            "D 規則の分岐: "
            + " / ".join(f"{lab}: {b}" for (lab, _d), b in zip(loaded, branches, strict=True)),
        ]

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
