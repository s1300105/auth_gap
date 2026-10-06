#!/usr/bin/env python3
"""最終評価の判定表（CSV）の雛形を作る（`docs/final_evaluation_procedure.md` 6.4・第 10 節、事前登録 §2.12 (d)）。

入力は `scripts/final_sample.py` の出力。種類ごとに 1 枚（`contradiction.csv` / `miss.csv` / `unknown.csv`）を書く。
1 行 1 組で、対象を読む欄（手引き 手順 A・18A.2 の 1）と、空の判定の欄（手順 H・18.4・18A.3）を並べる。

* **行の順は seed ⑤ で並べ替える**（手引き 21 の 1、D73 の 4）。各表ごとに、行を `pair_id` の順に並べてから
  `random.Random(seed).shuffle` する（表ごとに新しい乱数の列。どの表を先に作っても同じ順になる）。`seq` の欄に
  判定の順（1 から）を書く。表計算ソフトで並べ替えても `seq` で戻せる。
* `pair_id` は `final_sample.py` が付けた ID（`C-D1-001` / `M-001` / `U-D2-001`）。並べ替えに依らない。
* **見落としの表には解析器の出力を載せない**（効果の数・理由・位置・site・kind・打ち切りの印。手引き 18.2: 解析器の出力を
  見る前に読む）。載っていないことを書く前に確かめる（`MISS_FORBIDDEN`）。
* `--agreement`（`final_sample.py agreement` の出力）を渡すと、判定の一致を確かめる組だけの空の表
  （`agreement_<種類>.csv`）も書く。行の順は本表の `seq` の順（本表と同じ並べ替えの部分列）。

    .venv/bin/python scripts/final_sheet.py --seed <⑤> --out-dir evidence/population_final/sheets \\
        --contradiction evidence/population_final/final_judge_targets.json \\
        --miss evidence/population_final/final_miss_targets.json \\
        --unknown evidence/population_final/final_unknown_targets.json \\
        [--agreement evidence/population_final/final_agreement_targets.json]
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import random

KINDS = ("contradiction", "miss", "unknown")

#: 対象を読む欄（抜き取りの出力から写す）
TARGET_COLS = {
    # 手引き 手順 A
    "contradiction": ["tree", "unit", "unit_relpath", "unit_lineno", "site", "kind", "decl", "reasons", "locations"],
    # 手引き 18.2 の 1: ツールの本体（relpath:lineno）と、照らす宣言だけ
    "miss": ["tree", "unit", "unit_relpath", "unit_lineno", "decl"],
    # 手引き 18A.2 の 1
    "unknown": ["tree", "unit", "unit_relpath", "unit_lineno", "site", "kind", "decl", "reasons", "locations"],
}

AI_COLS = ["ai_used", "ai_model", "ai_log"]

#: 空の判定の欄
JUDGE_COLS = {
    # 手引き 手順 H（D83: reachable・violates・condition は書かない。verdict と error_class から分かる）
    "contradiction": ["verdict", "condition_type", "write_target", "error_class", "unknown_reason", "evidence", "note",
                      "minutes", *AI_COLS],
    # 手引き 18.4（unknown_reason は 18.4 の表に無いが、第 19 節「不明の理由は集計で内訳として報告する」ために足した）
    "miss": ["outcome", "cause", "write_target", "condition_type", "condition", "depth", "unknown_reason", "evidence",
             "ai_found", "output_found", "note", "minutes", *AI_COLS],  # output_found: 手引き 18.2 の 4・18.4（D76）
    # 手引き 18A.3
    "unknown": ["outcome", "reachable", "violates", "write_target", "condition_type", "condition", "unknown_reason",
                "evidence", "note", "minutes", *AI_COLS],
}

#: 見落としの表に載せてはいけない欄（解析器の出力。手引き 18.2）
MISS_FORBIDDEN = frozenset({"reasons", "locations", "site", "kind", "n_effects", "truncated", "n_units_in_tree",
                            "n_pairs_in_tree", "witness_chain", "verdict", "notes", "cap_hits", "opaque_reasons"})


def columns(kind: str) -> list[str]:
    cols = ["seq", "pair_id", *TARGET_COLS[kind], *JUDGE_COLS[kind]]
    if kind == "miss":
        bad = MISS_FORBIDDEN & set(cols)
        if bad:
            raise AssertionError(f"見落としの表に解析器の出力の欄がある: {sorted(bad)}")
    return cols


def cell(v) -> str:
    if v is None:
        return ""
    if isinstance(v, list):
        return " ".join(str(x) for x in v)
    return str(v)


def ordered(targets: list[dict], seed: int) -> list[dict]:
    rows = sorted(targets, key=lambda t: t["pair_id"])
    random.Random(seed).shuffle(rows)
    return rows


def sheet_rows(kind: str, targets: list[dict], seed: int) -> list[list[str]]:
    cols = columns(kind)
    out = []
    for i, t in enumerate(ordered(targets, seed), start=1):
        src = {"seq": i, **{c: t.get(c) for c in TARGET_COLS[kind]}, "pair_id": t["pair_id"]}
        out.append([cell(src.get(c)) for c in cols])
    return out


def write_csv(path: str, cols: list[str], rows: list[list[str]]) -> None:
    with open(path, "w", encoding="utf-8-sig", newline="") as fh:  # BOM つき: Excel で日本語が化けない
        w = csv.writer(fh)
        w.writerow(cols)
        w.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seed", type=int, required=True, help="seed ⑤（判定表の順序の並べ替え）")
    ap.add_argument("--out-dir", required=True)
    for kind in KINDS:
        ap.add_argument(f"--{kind}", help=f"final_sample.py {kind} の出力")
    ap.add_argument("--agreement", help="final_sample.py agreement の出力（任意）")
    a = ap.parse_args(argv)
    given = {k: getattr(a, k) for k in KINDS if getattr(a, k)}
    if not given:
        ap.error("--contradiction / --miss / --unknown のどれかを渡す")
    os.makedirs(a.out_dir, exist_ok=True)
    sheets: dict[str, list[list[str]]] = {}
    for kind, path in given.items():
        with open(path, encoding="utf-8-sig") as fh:
            s = json.load(fh)
        if s.get("kind") != kind:
            raise SystemExit(f"--{kind} に渡したファイルの kind が {s.get('kind')!r}")
        ids = [t["pair_id"] for t in s["targets"]]
        if len(set(ids)) != len(ids):
            raise SystemExit(f"{kind} の pair_id が重複している")
        sheets[kind] = sheet_rows(kind, s["targets"], a.seed)
        write_csv(os.path.join(a.out_dir, f"{kind}.csv"), columns(kind), sheets[kind])
        print(f"{kind}.csv: {len(sheets[kind])} 行")
    if a.agreement:
        with open(a.agreement, encoding="utf-8-sig") as fh:
            ag = json.load(fh)
        if ag.get("kind") != "agreement":
            raise SystemExit(f"--agreement に渡したファイルの kind が {ag.get('kind')!r}")
        for kind, v in ag["by_kind"].items():
            if kind not in sheets:
                raise SystemExit(f"--agreement の {kind} を書くには --{kind} も渡す")
            want = set(v["pair_ids"])
            pid = columns(kind).index("pair_id")
            rows = [r for r in sheets[kind] if r[pid] in want]
            if len(rows) != len(want):
                raise SystemExit(f"--agreement の {kind} に、本表に無い pair_id がある")
            write_csv(os.path.join(a.out_dir, f"agreement_{kind}.csv"), columns(kind), rows)
            print(f"agreement_{kind}.csv: {len(rows)} 行")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
