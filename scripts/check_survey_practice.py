#!/usr/bin/env python3
"""実態調査の表（配った表を写して `outcome` と `evidence` を書いたもの）の書き方を確かめる。練習にも本番にも使う。

    .venv/bin/python scripts/check_survey_practice.py practice/survey_practice.csv            # 練習（配った練習の表と照らす）
    .venv/bin/python scripts/check_survey_practice.py <書いた表> --sheet <配った本番の表>       # 本番

判定の中身（違反かどうか）は確かめない。D90（学生: 記録は練習も本番も最低限）で、判定者が書くのは `outcome` と `evidence` だけに
なった。確かめるのは、`outcome` が答えの値のどれかか、`evidence` が答えごとの形（D91・D92。`違反でない` は空で、書いてあっても見ない）
（`survey/PROTOCOL.md` の 7 節。D95 の前は `archive/practice_survey_manual/03_record.md` の 3 節）か、名簿の欄が配った表と同じか、だけ。

* 道筋は 1 本。「ファイル:行 名前」か「名前（外）」を「→」でつなぐ。違反は最後が「ファイル:行: 何をするか」か「名前（外）: 何をするか」。
  不明は最後が呼び出しか「ファイル:行: 何が決められないか」。パスは木の根から（`corpus/` を付けない）。`->` は使わない。
* `--sheet` を付けたとき（本番）は、表の行が配った表の行と 1 対 1 か（消した行・足した行・書き換えた pair_id・重複）も確かめる。
  付けないとき（練習）は、配った練習の表に無い件（素振りの EX-1 など）を確かめない。
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
#: 配った表の名簿の欄（判定者は書き換えない。survey/PROTOCOL.md の 7 節）。写しで書き換わると、別の件を判定した記録になる。
ROSTER_COLS = ("seq", "pair_id", "tree", "tool", "roster_form", "roster_relpath", "roster_lineno", "decl_lineno", "decl")
#: `--sheet` を省いたときに照らす、配った練習の表。
DISTRIBUTED_SHEET = os.path.join(ROOT, "evidence", "practice_survey", "survey_practice.csv")
#: 道筋の 1 つの段（D91）: 木の中の関数「ファイル:行 名前」、木の外の関数「名前（外）」。本体は書かず、呼んだ先から書く（D91 の改訂）。
STEP_RE = re.compile(r"^(\S+:\d+ \S+|[^\s→／:]+（外）)$")
#: 道筋の終わり（D91）: 「ファイル:行: 何をするか」（本体の中の行そのものなら、これだけ）か「名前（外）: 何をするか」。
END_RE = re.compile(r"^(\S+:\d+|[^\s→／:]+（外）): \S")
#: 不明 の終わりの、木の中の呼び出しに何が決められないかを添えた形「ファイル:行 名前: …」（survey/PROTOCOL.md の 7 節）。
UNKNOWN_CALL_END_RE = re.compile(r"^\S+:\d+ [^\s:]+: \S")
#: 段のファイルの部分（「ファイル:行」の「ファイル」）。
STEP_FILE_RE = re.compile(r"^(\S+?):\d+")
#: 添え物の前の半角の「/」（全角の「／」で区切る）。`https://` の中の「/」は除く。
ASCII_SEP_RE = re.compile(r"(?<![:/])/\s*(API 名から|https?://)")
ATTACHMENT_API_NAME = "API 名から"
#: 添え物の URL（`httpx.Client.post（外）` のような道筋を URL と取り違えないよう、`http://`・`https://` で始まるものだけ）。
URL_RE = re.compile(r"^https?://\S+$")


def _path_errors(path: str, out: str) -> list[str]:
    """道筋 1 本の形を確かめる（survey/PROTOCOL.md の 7 節）。"""
    errs: list[str] = []
    if "->" in path:
        errs.append("道筋のつなぎに -> がある（「→」でつなぐ）")
    steps = [x.strip() for x in path.split("→")]
    files = [m.group(1) for m in (STEP_FILE_RE.match(st) for st in steps) if m]
    if any(f.startswith(("/", "./")) or f == "corpus" or f.startswith("corpus/") or "/corpus/" in f for f in files):
        errs.append("パスが木の根からでない（corpus/<木>/・./・/ で始めない）")
    if errs:
        return errs
    head, last = steps[:-1], steps[-1]
    if out in VIOLATIONS:
        if not all(STEP_RE.match(st) for st in head) or not END_RE.match(last):
            errs.append(f"{out} なのに evidence が反する行までの道筋でない（「ファイル:行 名前 → … → ファイル:行: 何をするか」、"
                        "木の外は「名前（外）」。反する行が最後。survey/PROTOCOL.md の 7 節）")
    elif not all(STEP_RE.match(st) for st in head) or not (
            STEP_RE.match(last) or END_RE.match(last) or UNKNOWN_CALL_END_RE.match(last)):
        errs.append("不明 なのに evidence が、決められなかった点までの道筋（「ファイル:行 名前 → … → 名前（外）」、呼び出しでなければ"
                    "「ファイル:行: 何が決められないか」）でない（survey/PROTOCOL.md の 7 節）")
    return errs


def check_row(r: dict) -> list[str]:
    """1 行を確かめ、誤りを返す。"""
    errs: list[str] = []
    out = (r.get("outcome") or "").strip()
    if out not in SURVEY_OUTCOMES:
        return [f"outcome = {out!r} は {list(SURVEY_OUTCOMES)} のどれでもない（字のとおりに書く。survey/PROTOCOL.md の 6 節）"]
    ev = (r.get("evidence") or "").strip()
    for c in ("outcome", "evidence"):
        v = r.get(c) or ""
        if "\n" in v or "\r" in v:
            errs.append(f"{c} に改行がある（1 つのセルに改行を入れない。「／」で区切る）")
        if v[:1] in ("=", "+", "-", "@"):
            errs.append(f"{c} の先頭が {v[:1]!r}（表計算のソフトで式として読まれる）")
    # D92: evidence を書くのは 違反・違反（深さ 4 の外）・不明・対象外。違反でない は空（書いてあっても見ない）
    if out == "違反でない":
        return errs
    if not ev:
        errs.append(f"{out} なのに evidence が空（違反は反する行までの道筋、不明は決められなかった点までの道筋、"
                    "対象外は理由を 1 文。survey/PROTOCOL.md の 7 節）")
        return errs
    if out == "対象外":
        return errs
    # D91: 道筋は 1 本で先頭。URL（公式の文書で決めた）と「API 名から」（名前で決めた）は「／」の後の添え物
    if ASCII_SEP_RE.search(ev):
        errs.append(f"添え物（URL・「{ATTACHMENT_API_NAME}」）の前の区切りが半角の「/」（全角の「／」で区切る。survey/PROTOCOL.md の 7 節）")
        return errs
    segs = [x.strip() for x in ev.split("／") if x.strip()]
    paths = [x for x in segs if not (URL_RE.match(x) or x == ATTACHMENT_API_NAME)]
    if len(paths) != 1 or segs[0] != paths[0]:
        what = "反する行までの道筋" if out in VIOLATIONS else "決められなかった点までの道筋"
        errs.append(f"{out} の evidence は{what} 1 本を先頭に書き、添えるのは「／」の後の URL と「{ATTACHMENT_API_NAME}」だけ"
                    f"（道筋が {len(paths)} 本。survey/PROTOCOL.md の 7 節）")
        return errs
    errs += _path_errors(paths[0], out)
    return errs


def _distributed_roster(path: str = DISTRIBUTED_SHEET) -> dict[str, dict[str, str]]:
    """配った表の名簿の欄を pair_id ごとに返す（無ければ空。配った表に無い件（素振りの EX-1 など）は確かめない）。"""
    try:
        with open(path, encoding="utf-8-sig", newline="") as f:
            return {r["pair_id"].strip(): {c: (r.get(c) or "").strip() for c in ROSTER_COLS} for r in csv.DictReader(f)}
    except (OSError, KeyError):
        return {}


def check_roster(r: dict, roster: dict[str, dict[str, str]], sheet: str = DISTRIBUTED_SHEET) -> list[str]:
    """名簿の欄が配った表と同じかを確かめる（判定の前の行も確かめる）。"""
    want = roster.get((r.get("pair_id") or "").strip())
    if not want:
        return []
    changed = [c for c in ROSTER_COLS if c in r and (r.get(c) or "").strip() != want[c]]
    if not changed:
        return []
    return [f"名簿の欄 {changed} が配った表（{os.path.relpath(sheet, ROOT)}）と違う（名簿の欄は書き換えない。"
            "survey/PROTOCOL.md の 7 節。表計算のソフトで並べ替えた・数を変えたなら、配った表の値に戻す）"]


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
    ap.add_argument("--sheet", help="名簿の欄と行を照らす配った表（本番）。省くと練習の表 "
                                    "evidence/practice_survey/survey_practice.csv の名簿の欄だけを照らす")
    a = ap.parse_args(argv)
    strict = a.sheet is not None
    sheet = a.sheet or DISTRIBUTED_SHEET
    try:
        with open(a.csv, encoding="utf-8-sig", newline="") as f:
            first_line = f.readline()
            f.seek(0)
            reader = csv.DictReader(f)
            rows = list(reader)
            header = [c for c in (reader.fieldnames or []) if c is not None]
    except UnicodeDecodeError:
        print("誤り: 表が UTF-8 で保存されていない。Excel なら「CSV UTF-8（コンマ区切り）」で保存し直す")
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
    roster = _distributed_roster(sheet)
    if not roster:
        print(f"誤り: 配った表 {sheet} を読めない（名簿の欄を照らせない）")
        bad += 1
    seen: set[str] = set()
    for i, raw in enumerate(rows, start=2):
        pid = raw.get("pair_id") or "?"
        key = pid.strip()
        if key in seen:
            print(f"{i} 行目 {pid}: 誤り: 同じ pair_id の行が前にもある（行を写して増やさない）")
            bad += 1
            continue
        seen.add(key)
        if strict and roster and key not in roster:
            print(f"{i} 行目 {pid}: 誤り: 配った表に無い pair_id（pair_id を書き換えた・行を足した。名簿の欄は書き換えない）")
            bad += 1
            continue
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
        roster_errs = check_roster(r, roster, sheet)
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
    if strict and roster:
        lost = [p for p in roster if p not in seen]
        if lost:
            print(f"誤り: 配った表の行が無い: {lost}（行を消さない。まだ判定していない行も残す）")
            bad += 1
    print("誤りなし" if not bad else f"誤りのある行・欄: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
