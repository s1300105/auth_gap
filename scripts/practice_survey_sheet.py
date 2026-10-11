#!/usr/bin/env python3
"""実態調査の練習の表（`evidence/practice_survey/survey_practice.csv`）を、名簿と抜き取りの列から作る。

    # 1. 名簿（全 99 木。練習の練習の件を引くため）と、枠の 46 木だけの名簿を作る
    .venv/bin/python scripts/survey_roster.py build --corpus corpus --prefix v4- --out <dir>/roster_all.json
    .venv/bin/python scripts/survey_roster.py build --corpus corpus --prefix v4- \\
        --keep evidence/practice_survey/frame_keep46.json --out <dir>/roster_46.json
    # 2. 抜き取る（使い捨ての seed。_note_practice を除いて survey_practice_targets.json と同じものが出る）
    .venv/bin/python scripts/survey_roster.py sample <dir>/roster_46.json --seed 20261009 --n 10 --out <dir>/targets.json
    # 3. 表を作る
    .venv/bin/python scripts/practice_survey_sheet.py --roster <dir>/roster_all.json --targets <dir>/targets.json \\
        --warmup v4-andrewbolster__mcp.bolster.online:check_availability --skip S-001 --out <dir>/survey_practice.csv
    cmp <dir>/survey_practice.csv evidence/practice_survey/survey_practice.csv

* 1 行目は練習の練習（`W-01`）。無作為の抜き取りではなく手で選んだ件で、行の値は名簿のその木・そのツールの件から写す。
* 続く行は抜き取りの列の順。`--skip` の件を飛ばし、先頭から `--n-timed` 件を `T-01` から振り直す（練習では `unmapped` の
  S-001 を、選び方の規則が未決（O48 (5)）なので飛ばした。本番では飛ばさない。D85 の 3）。
* 欄は練習の表の欄（判定の欄と練習だけの時間の欄は空）。本番の表の道具は段階 B2 で作る（`docs/open_questions.md` O49）。
* 名簿と抜き取りは `survey_roster.py` の決定論に従う（同じ Python で走らせる。練習の抜き取りは 3.10.20）。
"""
from __future__ import annotations

import argparse
import csv
import json
import sys

#: 練習の表の欄（`03_record.md`）。先頭の 9 欄を名簿から書き、ほかは空で配る。
COLUMNS = ("seq", "pair_id", "tree", "tool", "roster_form", "roster_relpath", "roster_lineno", "decl_lineno", "decl",
           "outcome", "write_target", "condition_type", "condition", "depth", "unknown_reason", "evidence", "ai_found",
           "note", "minutes", "ai_used", "ai_model", "ai_log", "stopped_early", "t_start", "t_end", "t_break", "t_noai",
           "t_ai", "t_guide", "t_setup")


def row_of(seq: int, pair_id: str, entry: dict) -> dict:
    return {"seq": seq, "pair_id": pair_id, "tree": entry["tree"], "tool": entry["tool"], "roster_form": entry["form"],
            "roster_relpath": entry["relpath"], "roster_lineno": entry["def_lineno"],
            "decl_lineno": entry["decl_lineno"], "decl": "D1"}


def warmup_entry(roster: dict, tree: str, tool: str) -> dict:
    hits = [dict(e, tree=t["tree"]) for t in roster["trees"] if t["tree"] == tree for e in t["entries"] if e["tool"] == tool]
    if len(hits) != 1:
        raise SystemExit(f"名簿に {tree}:{tool} の件が 1 件でない（{len(hits)} 件）")
    return hits[0]


def build_rows(roster: dict, targets: dict, warmup: str, skip: set[str], n_timed: int) -> list[dict]:
    tree, _, tool = warmup.partition(":")
    rows = [row_of(1, "W-01", warmup_entry(roster, tree, tool))]
    timed = [t for t in targets["targets"] if t["pair_id"] not in skip][:n_timed]
    if len(timed) < n_timed:
        raise SystemExit(f"抜き取りの列に {n_timed} 件が無い（{len(timed)} 件）")
    for k, t in enumerate(timed, start=1):
        rows.append(row_of(k + 1, f"T-{k:02d}", t))
    return rows


def write_sheet(rows: list[dict], path: str) -> None:
    with open(path, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--roster", required=True, help="練習の練習の件を引く名簿（survey_roster.py build の出力）")
    ap.add_argument("--targets", required=True, help="抜き取りの列（survey_roster.py sample の出力）")
    ap.add_argument("--warmup", required=True, help="練習の練習の件の 木:ツール")
    ap.add_argument("--skip", action="append", default=[], help="飛ばす抜き取りの件の pair_id（何度でも）")
    ap.add_argument("--n-timed", type=int, default=3, help="時間を測る件の数（T-01 から）")
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    with open(a.roster, encoding="utf-8") as fh:
        roster = json.load(fh)
    with open(a.targets, encoding="utf-8") as fh:
        targets = json.load(fh)
    rows = build_rows(roster, targets, a.warmup, set(a.skip), a.n_timed)
    write_sheet(rows, a.out)
    print(json.dumps([{k: r[k] for k in ("pair_id", "tree", "tool")} for r in rows], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
