#!/usr/bin/env python3
"""実態調査の練習の表（`evidence/practice_survey/survey_practice.csv` を写して書いたもの）の書き方を確かめる。

    .venv/bin/python scripts/check_survey_practice.py practice/survey_practice.csv

判定の中身（違反かどうか）は確かめない。D90（学生: 記録は練習も本番も最低限）で、判定者が書くのは `outcome` と `evidence` だけに
なった。確かめるのは、`outcome` が答えの値のどれかか、`evidence` が答えごとの形（`evidence/practice_survey/manual/03_record.md` の
3 節）か、名簿の欄が配った表と同じか、だけ。

* `outcome` が空の行は「まだ判定していない」として飛ばす（`--all` を付けると誤りにする）。
* 誤りがあれば行ごとに出し、終了コード 1。
* 前の版の表（時間・ラベル・メモ・AI の欄があるもの）も読める。その欄は見ない。
* 欄の数が見出しと合わない行（セルの中の `,` を `"` で囲んでいない、など）は、欄がずれて値の誤りが連なるので、その行の
  ほかの確かめをせずに欄の数の誤りだけを出す。
"""
from __future__ import annotations

import argparse
import csv
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#: 実態調査の答え（D82・D85。「違反（深さ 4 の外）」は D68 の 2・18.3 の別の数え）。
SURVEY_OUTCOMES = ("違反", "違反（深さ 4 の外）", "違反でない", "不明", "対象外")
VIOLATIONS = ("違反", "違反（深さ 4 の外）")
REQUIRED_COLUMNS = ("pair_id", "outcome", "evidence")
#: 精度・見落としの判定の欄（実態調査には無い。D84・手引き 18.4・13 節）。
FORBIDDEN_COLUMNS = ("target_by_arg", "cause", "verdict", "output_found", "error_class")
#: 配った表の名簿の欄（判定者は書き換えない。03_record.md の 1 節）。写しで書き換わると、別の件を判定した記録になる。
ROSTER_COLS = ("seq", "pair_id", "tree", "tool", "roster_form", "roster_relpath", "roster_lineno", "decl_lineno", "decl")
DISTRIBUTED_SHEET = os.path.join(ROOT, "evidence", "practice_survey", "survey_practice.csv")
#: 道筋の始まり「ファイル:行 名前」と、違反の道筋の終わり「ファイル:行: 何をするか」か「名前（外）: 何をするか」（D91）。
PATH_START_RE = re.compile(r"^\S+:\d+ \S")
VIOLATION_END_RE = re.compile(r"(\S+:\d+|（外）): \S")


def check_row(r: dict) -> list[str]:
    """1 行を確かめ、誤りを返す。"""
    errs: list[str] = []
    out = (r.get("outcome") or "").strip()
    if out not in SURVEY_OUTCOMES:
        return [f"outcome = {out!r} は {list(SURVEY_OUTCOMES)} のどれでもない（字のとおりに書く。03_record.md の 2 節）"]
    ev = (r.get("evidence") or "").strip()
    for c in ("outcome", "evidence"):
        v = r.get(c) or ""
        if "\n" in v or "\r" in v:
            errs.append(f"{c} に改行がある（1 つのセルに改行を入れない。「／」で区切る）")
        if v[:1] in ("=", "+", "-", "@"):
            errs.append(f"{c} の先頭が {v[:1]!r}（表計算のソフトで式として読まれる）")
    if not ev:
        errs.append("evidence が空（どの答えでも書く。03_record.md の 3 節）")
        return errs
    # D91: 道筋は「ファイル:行 名前 → … 」。道筋どうしは「／」。URL と「API 名から」は添え物
    segs = [x.strip() for x in ev.split("／") if x.strip()]
    paths = [x for x in segs if not (x.startswith("http") or x == "API 名から")]
    if out in VIOLATIONS:
        if not paths or not PATH_START_RE.match(paths[0]) or not VIOLATION_END_RE.search(paths[0]):
            errs.append(f"{out} なのに evidence の最初が反する行までの道筋でない（「ファイル:行 名前 → … → ファイル:行: 何をするか」。"
                        "03_record.md の 3 節）")
    if out == "違反（深さ 4 の外）" and not any(PATH_START_RE.match(x) for x in paths[1:]):
        errs.append("違反（深さ 4 の外） なのに「／」の後に、深さ 4 までにたどった道筋が無い（03_record.md の 3 節）")
    if out in ("違反でない", "不明"):
        bad = [x for x in paths if not PATH_START_RE.match(x)]
        if not paths or bad:
            errs.append(f"{out} の evidence が、たどった道筋（「ファイル:行 名前 → …」を「／」で並べたもの）になっていない"
                        f"{'（' + bad[0][:30] + '…）' if bad else ''}（03_record.md の 3 節）")
    return errs


def _distributed_roster() -> dict[str, dict[str, str]]:
    """配った表の名簿の欄を pair_id ごとに返す（無ければ空。素振りの EX-1 などは配った表に無いので確かめない）。"""
    try:
        with open(DISTRIBUTED_SHEET, encoding="utf-8-sig", newline="") as f:
            return {r["pair_id"].strip(): {c: (r.get(c) or "").strip() for c in ROSTER_COLS} for r in csv.DictReader(f)}
    except (OSError, KeyError):
        return {}


def check_roster(r: dict, roster: dict[str, dict[str, str]]) -> list[str]:
    """名簿の欄が配った表と同じかを確かめる（判定の前の行も確かめる）。"""
    want = roster.get((r.get("pair_id") or "").strip())
    if not want:
        return []
    changed = [c for c in ROSTER_COLS if c in r and (r.get(c) or "").strip() != want[c]]
    if not changed:
        return []
    return [f"名簿の欄 {changed} が配った表（evidence/practice_survey/survey_practice.csv）と違う（名簿の欄は書き換えない。"
            "03_record.md の 1 節。表計算のソフトで並べ替えた・数を変えたなら、配った表の値に戻す）"]


def _header_hint(first_line: str) -> str:
    """見出しの欄が足りないときに、よくある原因を 1 つ当てる。"""
    if "pair_id" not in first_line:
        return "（1 行目が見出しでない。表の上に行を足していないか、見出しの行を消していないか）"
    if first_line.count(";") > first_line.count(","):
        return "（区切りが ; になっている。コンマ区切りの CSV で保存し直す）"
    if first_line.count("\t") > first_line.count(","):
        return "（区切りがタブになっている。コンマ区切りの CSV で保存し直す）"
    return ""


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("csv")
    ap.add_argument("--all", action="store_true", help="outcome が空の行も誤りにする")
    a = ap.parse_args(argv)
    try:
        with open(a.csv, encoding="utf-8-sig", newline="") as f:
            first_line = f.readline()
            f.seek(0)
            reader = csv.DictReader(f)
            rows = list(reader)
            header = [c for c in (reader.fieldnames or []) if c is not None]
    except UnicodeDecodeError:
        print("誤り: 表が UTF-8 で保存されていない。Excel なら「CSV UTF-8（コンマ区切り）」で保存し直す（03_record.md の 4 節）")
        return 1
    bad = 0
    missing = [c for c in REQUIRED_COLUMNS if c not in header]
    extra = [c for c in FORBIDDEN_COLUMNS if c in header]
    if missing:
        print(f"誤り: 欄が無い: {missing}{_header_hint(first_line)}")
        print(f"誤りのある行・欄: {bad + 1}")
        return 1
    if extra:
        print(f"誤り: 実態調査では使わない欄がある: {extra}")
        bad += 1
    if not rows:
        print("誤り: 見出しの行だけで、件の行が無い")
        return 1
    roster = _distributed_roster()
    for i, raw in enumerate(rows, start=2):
        pid = raw.get("pair_id") or "?"
        if None in raw:
            print(f"{i} 行目 {pid}: 誤り: 欄の数が見出しより多い（セルの中の , を \" で囲んでいない。表計算のソフトで開いて"
                  " 保存し直すか、テキストエディタなら \"…\" で囲む）")
            bad += 1
            continue
        if any(v is None for v in raw.values()):
            print(f"{i} 行目 {pid}: 誤り: 欄の数が見出しより少ない（区切りの , が足りない。表計算のソフトで開いて保存し直す）")
            bad += 1
            continue
        r = dict(raw)
        roster_errs = check_roster(r, roster)
        for e in roster_errs:
            print(f"{i} 行目 {pid}: 誤り: {e}")
        if not r.get("outcome", "").strip():
            if a.all:
                print(f"{i} 行目 {pid}: 誤り: outcome が空（まだ判定していない）")
                bad += 1
            else:
                print(f"{i} 行目 {pid}: まだ判定していない（飛ばした）")
                bad += bool(roster_errs)
            continue
        errs = check_row(r)
        for e in errs:
            print(f"{i} 行目 {pid}: 誤り: {e}")
        if not errs and not roster_errs:
            print(f"{i} 行目 {pid}: よい")
        bad += bool(errs or roster_errs)
    print("誤りなし" if not bad else f"誤りのある行・欄: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
