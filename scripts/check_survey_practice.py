#!/usr/bin/env python3
"""実態調査の形の練習の表（`evidence/practice_v4/survey_practice.csv` を写して書いたもの）の書き方を確かめる。

    .venv/bin/python scripts/check_survey_practice.py ~/authgap_practice/survey_practice.csv

判定の中身（違反かどうか）は確かめない。確かめるのは、欄の値が語彙の中にあるか、答えごとに書く欄・書かない欄が
`evidence/practice_v4/manual/03_record.md` のとおりか、時間の欄が合っているか、だけ。

* 語彙（条件の種類・書き込み先の種類・不明の理由の類・AI の有無）は `scripts/final_aggregate.py` の定義を使う
  （語彙は 1 か所でしか定義しない）。実態調査の答えの値だけはここで定義する（手引きに実態調査の節がまだ無い。O48 (4)）。
* `outcome` が空の行は「まだ判定していない」として飛ばす（`--all` を付けると誤りにする）。
* 誤りがあれば行ごとに出し、終了コード 1。注意（直さなくてもよいが見てほしい点）は終了コードに影響しない。
* 03_record.md が「必ず」とする書き方は誤りにする（注意にすると、学生は直さなくてよいと読む）。
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
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from final_aggregate import (  # noqa: E402
    AI_USED,
    CONDITION_TYPES,
    UNKNOWN_REASON_CLASSES,
    WRITE_TARGETS,
    VocabularyError,
    parse_conditions,
    parse_unknown_reason,
)

#: 実態調査の答え（D82・D85。「違反（深さ 4 の外）」は D68 の 2・18.3 の別の数え）。
SURVEY_OUTCOMES = ("違反", "違反（深さ 4 の外）", "違反でない", "不明", "対象外")
VIOLATIONS = ("違反", "違反（深さ 4 の外）")
#: 練習だけの欄 `stopped_early`（最初の違反で止めたか）。
STOPPED = ("はい", "いいえ", "違反なし")
#: 実態調査では使わない不明の理由の類（解析器の打ち切りの類。実態調査は解析器を見ない）。
NOT_IN_SURVEY_CLASSES = ("打ち切り",)
LABEL_COLS = ("write_target", "condition_type", "condition", "depth")
TEXT_COLS = ("condition", "unknown_reason", "evidence", "ai_found", "note")
REQUIRED_COLUMNS = ("pair_id", "tree", "outcome", *LABEL_COLS, "unknown_reason", "evidence", "ai_found", "note",
                    "minutes", "ai_used", "ai_model", "ai_log", "stopped_early", "t_start", "t_end", "t_break",
                    "t_noai", "t_ai", "t_guide", "t_setup")
FORBIDDEN_COLUMNS = ("target_by_arg", "cause", "verdict")
TIME_RE = re.compile(r"^([01]?\d|2[0-3]):[0-5]\d$")
TIME_WITH_SECONDS_RE = re.compile(r"^\d{1,2}:\d{2}:\d{2}$")
INT_RE = re.compile(r"^\d+$")
#: `ai_found` に新しい動作を書くときは「ファイル:行」を含める（03_record.md の 3.6）。
FILE_LINE_RE = re.compile(r"\S+:\d+")


def _minutes_of(hhmm: str) -> int:
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def check_row(r: dict) -> tuple[list[str], list[str]]:
    """1 行を確かめ、(誤り, 注意) を返す。"""
    errs: list[str] = []
    notes: list[str] = []
    out = r.get("outcome", "").strip()
    if out not in SURVEY_OUTCOMES:
        errs.append(f"outcome = {out!r} は {list(SURVEY_OUTCOMES)} のどれでもない")
        return errs, notes

    ev = r.get("evidence", "").strip()
    note = r.get("note", "").strip()
    if not ev:
        errs.append("evidence が空（どの答えでも書く）")
    for c, v in r.items():
        if "\n" in v or "\r" in v:
            errs.append(f"{c} に改行がある（1 つのセルに改行を入れない。「／」で区切る）")
    for c in TEXT_COLS:
        v = r.get(c, "")
        if v[:1] in ("=", "+", "-", "@"):
            notes.append(f"{c} の先頭が {v[:1]!r}（表計算のソフトで式として読まれる）")
    if out in ("違反でない", "不明") and "読んだ範囲" not in ev:
        errs.append(f"{out} なのに evidence に「読んだ範囲」が無い（18.4）")
    elif out in VIOLATIONS and "読んだ範囲" not in ev:
        notes.append("evidence に「読んだ範囲」が無い（18.4 はどの答えでも書くとする。止めたなら止めたところまで）")

    if out in VIOLATIONS:
        wt = r.get("write_target", "").strip()
        if wt not in WRITE_TARGETS:
            errs.append(f"write_target = {wt!r} は {list(WRITE_TARGETS)} のどれでもない")
        elif wt == "その他・不明" and not re.match(r"^(その他|不明)[:：]", r.get("note", "").strip()):
            errs.append("write_target = その他・不明 なのに note の先頭が「その他:」か「不明:」でない（16 節）")
        ct = r.get("condition_type", "").strip()
        try:
            parts = parse_conditions(ct, "condition_type")
        except VocabularyError as e:
            errs.append(str(e))
            parts = ()
        if parts and parts != ("なし",) and not r.get("condition", "").strip():
            errs.append("condition_type に条件があるのに condition（条件の中身）が空")
        if parts == ("なし",) and r.get("condition", "").strip():
            errs.append("condition_type = なし なのに condition がある（なし のときは空にし、「毎回届く」は evidence に書く）")
        if parts and list(parts) != sorted(parts, key=CONDITION_TYPES.index):
            errs.append(f"condition_type = {ct!r} の順が 14.3 の表の順でない（集計は書いた順のまま組み合わせを数えるので、練習では"
                        f" {';'.join(sorted(parts, key=CONDITION_TYPES.index))} とそろえる。O48 (4) の仮の扱い）")
        d = r.get("depth", "").strip()
        if not INT_RE.match(d):
            errs.append(f"depth = {d!r} が 0 以上の整数でない")
        elif out == "違反" and int(d) > 4:
            errs.append(f"depth = {d} は深さ 4 の外。outcome は「違反（深さ 4 の外）」（18.3）")
        elif out == "違反（深さ 4 の外）" and int(d) <= 4:
            errs.append(f"depth = {d} は深さ 4 の中。outcome は「違反」")
        if r.get("unknown_reason", "").strip():
            errs.append("違反なのに unknown_reason がある（不明のときだけ書く）")
    else:
        for c in LABEL_COLS:
            if r.get(c, "").strip():
                errs.append(f"{out} なのに {c} がある（ラベルは違反のときだけ書く。D82）")
        ur = r.get("unknown_reason", "").strip()
        if out == "不明":
            try:
                cls = parse_unknown_reason(ur, "unknown_reason")
                if cls in NOT_IN_SURVEY_CLASSES:
                    errs.append(f"unknown_reason の類 {cls} は実態調査では使わない（解析器の打ち切りの類）")
                elif not re.match(r"^[:：]\s*\S", ur[len(cls):]):
                    errs.append("unknown_reason が類だけで説明が無い（「類: 説明（ファイル:行つき）」の形で書く）")
            except VocabularyError as e:
                errs.append(str(e) + f"（使える類: {[c for c in UNKNOWN_REASON_CLASSES if c not in NOT_IN_SURVEY_CLASSES]}）")
        elif ur:
            errs.append(f"{out} なのに unknown_reason がある（不明のときだけ書く）")

    se = r.get("stopped_early", "").strip()
    if se not in STOPPED:
        errs.append(f"stopped_early = {se!r} は {list(STOPPED)} のどれでもない")
    elif (se == "違反なし") == (out in VIOLATIONS):
        errs.append(f"stopped_early = {se} と outcome = {out} が合わない（違反のときは はい / いいえ、それ以外は 違反なし）")
    elif se == "はい" and out == "違反（深さ 4 の外）":
        errs.append("違反（深さ 4 の外）は深さ 4 の中を全部読んで違反が無かったときの答えなので、stopped_early = はい にならない（いいえ）")
    elif se == "はい" and "最初の違反で止めた" not in note:
        errs.append("stopped_early = はい なのに note に「最初の違反で止めた（深さ N まで読んだ）」が無い")

    au = r.get("ai_used", "").strip()
    if au not in AI_USED:
        errs.append(f"ai_used = {au!r} は {list(AI_USED)} のどれでもない")
    elif au == "あり":
        if not r.get("ai_model", "").strip() or not r.get("ai_log", "").strip():
            errs.append("ai_used = あり なのに ai_model か ai_log が空（手順 H）")
        af = r.get("ai_found", "").strip()
        if not af:
            errs.append("ai_used = あり なのに ai_found が空（新しく見つからなければ「なし」と書く）")
        elif af != "なし" and not FILE_LINE_RE.search(af):
            errs.append(f"ai_found = {af!r}: 新しく見つからなければ、ひらがな 2 文字の「なし」だけを書く（集計は「なし」と同じ字"
                        "だけを見て、ほかの字は「新しい動作あり」に数える）。見つかったなら「ファイル:行: 理由」の形で書く")
        if "AI の前の判定" not in note:
            errs.append("ai_used = あり なのに note に「AI の前の判定: <outcome>」が無い（段 10 の 1、手引き 21 の 6）")
    else:
        for c in ("ai_model", "ai_log", "ai_found"):
            if r.get(c, "").strip():
                errs.append(f"ai_used = なし なのに {c} がある")

    t0, t1 = r.get("t_start", "").strip(), r.get("t_end", "").strip()
    for name, v in (("t_start", t0), ("t_end", t1)):
        if TIME_WITH_SECONDS_RE.match(v):
            errs.append(f"{name} = {v!r} に秒が付いている。表計算のソフトが時刻に変えたので、列を文字列にするか先頭に ' を付けて"
                        " HH:MM で入れ直す（03_record.md の 5 節）")
        elif not TIME_RE.match(v):
            errs.append(f"{name} = {v!r} が HH:MM（24 時間）でない")
    ints = {}
    for name in ("minutes", "t_break", "t_noai", "t_ai", "t_guide", "t_setup"):
        v = r.get(name, "").strip()
        if not INT_RE.match(v):
            errs.append(f"{name} = {v!r} が 0 以上の整数（分）でない")
        else:
            ints[name] = int(v)
    if TIME_RE.match(t0) and TIME_RE.match(t1) and {"minutes", "t_break"} <= ints.keys():
        span = (_minutes_of(t1) - _minutes_of(t0)) % (24 * 60)
        if abs(span - ints["t_break"] - ints["minutes"]) > 2:
            notes.append(f"t_end − t_start − t_break = {span - ints['t_break']} 分と minutes = {ints['minutes']} 分が 2 分より離れている")
    if {"minutes", "t_noai", "t_ai"} <= ints.keys() and abs(ints["t_noai"] + ints["t_ai"] - ints["minutes"]) > 2:
        notes.append(f"t_noai + t_ai = {ints['t_noai'] + ints['t_ai']} 分と minutes = {ints['minutes']} 分が合わない")
    if au == "なし" and ints.get("t_ai", 0) != 0:
        errs.append("ai_used = なし なのに t_ai が 0 でない")
    if {"minutes", "t_guide"} <= ints.keys() and ints["t_guide"] > ints["minutes"]:
        errs.append("t_guide が minutes より大きい（手引きを読み返した分は minutes の内数）")
    return errs, notes


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
        print("誤り: 表が UTF-8 で保存されていない。Excel なら「CSV UTF-8（コンマ区切り）」で保存し直す（03_record.md の 5 節）")
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
        if not r.get("outcome", "").strip():
            if a.all:
                print(f"{i} 行目 {pid}: 誤り: outcome が空（まだ判定していない）")
                bad += 1
            else:
                print(f"{i} 行目 {pid}: まだ判定していない（飛ばした）")
            continue
        errs, notes = check_row(r)
        for e in errs:
            print(f"{i} 行目 {pid}: 誤り: {e}")
        for n in notes:
            print(f"{i} 行目 {pid}: 注意: {n}")
        if not errs and not notes:
            print(f"{i} 行目 {pid}: よい")
        bad += bool(errs)
    print("誤りなし" if not bad else f"誤りのある行・欄: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
