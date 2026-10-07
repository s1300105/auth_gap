#!/usr/bin/env python3
"""最終評価の集計（段階 8）。`docs/final_evaluation_procedure.md` 第 23 節と、事前登録の下書き
`docs/drafts/prereg_2_12_draft.md` の (f)(g) の計算を、判定し終えた判定表から出す。

**宣言 D1〜D4 ごとに出し、合算しない**（D62）。合算の行は `--v4-judgments` の道具の試験（手順書 6.7）でだけ出す。

    .venv/bin/python scripts/final_aggregate.py \\
        --run evidence/scan_v2_final_run1 \\
        --contradiction-sample evidence/population_final/final_judge_targets.json \\
        --miss-sample evidence/population_final/final_miss_targets.json \\
        --unknown-sample evidence/population_final/final_unknown_targets.json \\
        --contradictions evidence/population_final/sheets/contradiction.csv \\
        --misses evidence/population_final/sheets/miss.csv \\
        --unknowns evidence/population_final/sheets/unknown.csv \\
        --seed <seed ④> --out-json <out>.json --out-md <out>.md

    # 道具の試験（手順書 6.7）: v4 の判定で件数の精度 D1+D2 = 46 / 60 を再現する
    .venv/bin/python scripts/final_aggregate.py --v4-judgments evidence/population_v4/v4_judgments.json \\
        --run evidence/scan_v2_v4_run1 --seed 1 --out-json /tmp/v4_check.json

入力
====

* `--run`: 主の走査の run ディレクトリ（`summary.json` と木ごとの manifest）。ここから宣言ごとに
  - **N** = 宣言 d の矛が出た木の数（組の矛 / 不は `contradiction_by_decl.load_reasons` + `apply_flip(…, None)`。
    `contradiction_by_decl.py` の「矛の木」の列と同じ定義）、
  - **M_d** = 宣言 d を明示したユニットを 1 つ以上持つ走査した木の数（下の `declares()`。解析器の
    `authgap/dparse.py: contradiction_findings` と同じ条件。D73 の 3）、
  - **走査した木の数** = `summary.json` で `status == "ok"` の木（`runlib.run_manifests` と同じ集合）、
  - 不の組の宣言ごと・理由ごとの総数
  を数える。
* `--contradiction-sample` / `--miss-sample` / `--unknown-sample`（任意）: `scripts/final_sample.py` の出力
  （`kind` の欄で取り違えを防ぐ）。判定表の `pair_id` が `targets` と 1 対 1 で、(tree, decl) が同じかを確かめる
  （判定し残し・余分な行は誤り。`--allow-partial` で練習用に許す）。矛の抜き取りの `by_decl.<d>.n_trees`（N）・
  `n_pairs`・`denominators.n_trees_scanned` は `--run` と突き合わせ、食い違えば誤り。`denominators.M_d` の食い違いは
  警告にして両方を残す（下の `declares()` の注）。不の抜き取りの `by_decl.<d>.n_pairs`・`reason_pairs` も突き合わせる。
  `--run` が無ければ、N・M_d・走査した木の数を矛の抜き取りの出力から取る。
* `--contradictions`: 矛の判定表（CSV、1 行 1 組。`scripts/final_sheet.py` の `contradiction.csv` を判定したもの。
  手引きの手順 H の欄。組の id は `pair_id`）。
* `--misses`: 見落としの判定表（`miss.csv`。手引き 18.4 の欄）。
* `--unknowns`: 不の中身の判定表（`unknown.csv`。手引き 18A.3 の欄。`reasons` は空白区切り）。
* `--second-{contradictions,misses,unknowns}`（任意）: 判定の一致を確かめる組の 2 人目（または判定し直し）の
  ラベル（`final_sheet.py --agreement` の `agreement_<種類>.csv` を判定したもの。`pair_id` と `verdict` / `outcome`）。判定の種類ごとに Cohen の κ と一致率を出す（「不明」も 1 つの値）。
* `--resolved-contradictions`（任意）: 話し合いで決めたラベル（`pair_id`・`verdict`）。置き換えたときの主指標を併記する
  （主の結果は置き換えない）。

**語彙の外の値は誤りにする**（黙って落とさない。CLAUDE.md 規則 4）。欄の名前と値の語彙は下の定数（手引きの下書きの
手順 H・14.3・16・17・18.4・18A.3 から写した）。

計算（第 23.2〜23.4 節）
========================

* 木 t の正・誤・不明の数を c_t・w_t・u_t。n = 判定した木の数、k = c_t ≥ 1 の木の数。
* (a) = k / n。K̂ = (k / n) × N（n = N なら K̂ = k）。(c) = K̂ / M_d。(b)（参考）= K̂ / 走査した木の数。
* 木ごとの精度 p_t = c_t / (c_t + w_t)（c_t + w_t = 0 の木は除き、その数を書く）の平均。不明を誤とみなした
  p'_t = c_t / (c_t + w_t + u_t) の平均を併記。
* 区間: 木を単位にした bootstrap。木を名前でソートして並べ、宣言ごと・読み方ごとに `random.Random(seed)` を
  新しく作り、各回 `rng.choices(range(n), k=n)` で n 木を復元抽出する（同じ seed なら (A)(B)(C) は同じ再標本を使う）。
  百分位は線形補間（numpy の既定と同じ）の 2.5% と 97.5%。(b)(c) は各回の (a) × N / 分母。
  **n < 10 の宣言は区間を出さず**、件数と木ごとの内訳の表を出す（D73 の 4）。
* 件数の精度 Σ正 / (Σ正 + Σ誤) と 95% Wilson 区間（z = 1.96）。不明を誤とみなした値も併記。
* 条件の読み方（D68 の 1、第 23.5 節）: (B) は運用者が決める条件（運用者の設定・起動の方法）が 1 つでも入る正を、
  (C) は条件が「なし」でない正を、**誤に置き換えて**主指標を計算し直す。正の件数の (A)(B)(C) も出す。
"""

from __future__ import annotations

import argparse
import collections
import csv
import json
import math
import os
import random
import re
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

DECLS = ("D1", "D2", "D3", "D4")
B_DEFAULT = 10_000
MAX_TREES_PER_DECL = 200
MAX_PAIRS_PER_TREE = 3
MIN_TREES_FOR_INTERVAL = 10

# --- 語彙（手引きの下書きから写す。ここでしか定義しない） --------------------------------------------

VERDICTS = ("正", "誤", "不明")
TERNARY = ("はい", "いいえ", "決められない")
#: 14.3 の条件の種類。順は「弱い」順（手順 G）。
CONDITION_TYPES = ("なし", "引数", "初回", "失敗・期限切れ", "外部の状態", "運用者の設定", "起動の方法")
OPERATOR_CONDITIONS = frozenset({"運用者の設定", "起動の方法"})
#: 16.1 の書き込み先の種類（D1・D2・D4）。
WRITE_TARGETS = ("相手側の状態", "データベース", "利用者のファイル", "ログ", "一時ファイル", "キャッシュ・状態の保存",
                 "プロセスの起動・コードの実行", "その他・不明")
#: 16.3 の通信先の種類（D3）。
COMM_TARGETS = ("定数の外部ホスト", "モデルが決める宛先", "モデルが決めるコード・コマンド", "その他・不明")
#: 17 の誤の原因の分類。欄には「E1: 説明」のように書く（先頭の記号で分類する）。
ERROR_CLASSES = {"E1": "起動時の初期化", "E2": "同じ呼び出しで作った一時ファイル・ロックの後始末",
                 "E3": "名前だけの解決の誤り", "E4": "受け手の型の読み違い（動作の種類まで違う）",
                 "E5": "子プロセスの標準入力・パイプ", "E6": "到達しない（E1 以外）",
                 "E7": "モデルが決められないのに決められるとした", "E8": "宣言に反しない（E2 以外）", "E9": "その他"}
_ERROR_CLASS_RE = re.compile(r"^\s*(E[1-9])(?![0-9])")
#: 18.4 の見落としの結果。「不明（打ち切り）」は 18.3 / 事前登録 (d) の細分で、集計では「不明」に含めて内数を出す。
MISS_OUTCOMES = ("反する動作は無い", "解析器が不として出している", "見落とし", "見落とし（深さ 4 の外）", "不明")
MISS_OUTCOME_SUB = {"不明（打ち切り）": "不明"}
#: 18.2 の 6 の見落としの原因（D76 で「その他（打ち切り）」は無くなり、打ち切りは全部 `不明（打ち切り）`）。
MISS_CAUSES = ("深さ", "呼び出しの解決", "受け手の型", "語彙", "その他")
#: 第 19 節の不明の理由の類（D76。`unknown_reason` の先頭に「類: 説明」の形で書く。1 件に 1 つ）。
UNKNOWN_REASON_CLASSES = ("外の値", "相手の API", "起動・初期化", "動的な呼び出し", "打ち切り", "手引きで決まらない", "その他")
#: 18A.3 の不の中身の結果。
UNKNOWN_OUTCOMES = ("違反", "違反でない", "不明")
AI_USED = ("なし", "あり")
#: 組の id の欄（`scripts/final_sheet.py` の判定表と `scripts/final_sample.py` の targets の `pair_id`）。
ID_COL = "pair_id"


class VocabularyError(ValueError):
    """判定表の値が語彙の外、または欄の組み合わせが手引きと合わない。"""


# --- 小さな統計 -----------------------------------------------------------------------------------

def wilson(k: int, n: int, z: float = 1.96) -> Optional[tuple[float, float]]:
    """95% Wilson 区間（手順書 23.4 の式）。n = 0 なら None。"""
    if n <= 0:
        return None
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (centre - half, centre + half)


def percentile(sorted_vals: list[float], q: float) -> float:
    """線形補間の百分位（numpy.percentile の既定 'linear' と同じ）。`sorted_vals` は昇順。"""
    if not sorted_vals:
        raise ValueError("空の列の百分位")
    pos = q * (len(sorted_vals) - 1)
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return sorted_vals[lo]
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (pos - lo)


def cohen_kappa(a: list[str], b: list[str]) -> dict:
    """Cohen の κ と一致率。値の集合は 2 人のラベルの和集合（「不明」も 1 つの値）。"""
    if len(a) != len(b):
        raise ValueError("ラベルの数が違う")
    n = len(a)
    if n == 0:
        return {"n": 0, "agree": 0, "percent_agreement": None, "kappa": None, "p_expected": None}
    agree = sum(1 for x, y in zip(a, b, strict=False) if x == y)
    po = agree / n
    ca, cb = collections.Counter(a), collections.Counter(b)
    pe = sum(ca[c] * cb[c] for c in set(ca) | set(cb)) / (n * n)
    kappa = None if pe >= 1 else (po - pe) / (1 - pe)
    return {"n": n, "agree": agree, "disagree": n - agree, "percent_agreement": po, "kappa": kappa,
            "p_expected": pe, "kappa_note": None if kappa is not None else "期待一致が 1（全員が同じ 1 値）で κ は定義されない"}


# --- 判定表の読み込みと検証 ---------------------------------------------------------------------------

@dataclass
class Pair:
    """矛の判定表の 1 行。"""

    id: str
    tree: str
    decl: str
    verdict: str
    conditions: Optional[tuple[str, ...]] = None
    error_class: Optional[str] = None
    write_target: Optional[str] = None
    ai_used: Optional[str] = None
    minutes: Optional[float] = None
    unknown_reason: str = ""
    unknown_class: Optional[str] = None
    target_by_arg: Optional[str] = None


@dataclass
class Miss:
    id: str
    tree: str
    decl: str
    outcome: str
    outcome_raw: str
    cause: Optional[str] = None
    cause_raw: Optional[str] = None
    write_target: Optional[str] = None
    conditions: Optional[tuple[str, ...]] = None
    ai_found: Optional[str] = None
    ai_used: Optional[str] = None
    minutes: Optional[float] = None
    unknown_reason: str = ""
    unknown_class: Optional[str] = None
    output_found: Optional[str] = None


@dataclass
class UnknownPair:
    id: str
    tree: str
    decl: str
    outcome: str
    reasons: tuple[str, ...] = ()
    write_target: Optional[str] = None
    conditions: Optional[tuple[str, ...]] = None
    ai_used: Optional[str] = None
    minutes: Optional[float] = None
    unknown_reason: str = ""
    unknown_class: Optional[str] = None


def _err(where: str, msg: str) -> VocabularyError:
    return VocabularyError(f"{where}: {msg}")


def read_csv(path: str) -> list[dict]:
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return [{(k or "").strip(): (v or "").strip() for k, v in r.items()} for r in csv.DictReader(fh)]


def _require_columns(rows: list[dict], cols: tuple[str, ...], where: str) -> None:
    if not rows:
        return
    missing = [c for c in cols if c not in rows[0]]
    if missing:
        raise _err(where, f"欄が無い: {missing}（あるのは {sorted(rows[0])}）")


def _in(value: str, vocab, where: str, col: str) -> str:
    if value not in vocab:
        raise _err(where, f"{col} = {value!r} は語彙の外（{list(vocab)}）")
    return value


def parse_conditions(value: str, where: str) -> tuple[str, ...]:
    """`condition_type`（`;` で並べる）を語彙で確かめる。「なし」は単独でだけ使える。"""
    parts = tuple(p.strip() for p in value.split(";"))
    if not value or any(not p for p in parts):
        raise _err(where, f"condition_type = {value!r} が空か、`;` の間が空")
    for p in parts:
        _in(p, CONDITION_TYPES, where, "condition_type")
    if "なし" in parts and len(parts) > 1:
        raise _err(where, f"condition_type = {value!r}: 「なし」と条件を同時に書いている")
    if len(set(parts)) != len(parts):
        raise _err(where, f"condition_type = {value!r}: 同じ種類が重なっている")
    return parts


def parse_unknown_reason(value: str, where: str) -> str:
    """`unknown_reason` の先頭の類（第 19 節、D76）。「類」単独か「類: 説明」（`:` / `：`）。"""
    for c in sorted(UNKNOWN_REASON_CLASSES, key=len, reverse=True):
        if value == c or value.startswith(c + ":") or value.startswith(c + "："):
            return c
    raise _err(where, f"unknown_reason = {value!r} の先頭が第 19 節の類（{list(UNKNOWN_REASON_CLASSES)}）でない")


def parse_error_class(value: str, where: str) -> str:
    m = _ERROR_CLASS_RE.match(value)
    if not m:
        raise _err(where, f"error_class = {value!r} が E1〜E9 で始まらない（第 17 節）")
    return m.group(1)


#: D84 の層別。② で「重い」とする書き込み先の種類（D1 の正だけを層別する）。
HEAVY_WRITE_TARGETS = ("利用者のファイル", "データベース", "相手側の状態", "プロセスの起動・コードの実行")
#: D84 の ③ の欄 `target_by_arg` の値。
TARGET_BY_ARG = ("はい", "いいえ", "決められない")


def target_vocab(decl: str) -> tuple[str, ...]:
    return COMM_TARGETS if decl == "D3" else WRITE_TARGETS


def _minutes(value: str, where: str) -> Optional[float]:
    if value == "":
        return None
    try:
        x = float(value)
    except ValueError:
        raise _err(where, f"minutes = {value!r} が数でない") from None
    if x < 0 or math.isnan(x):
        raise _err(where, f"minutes = {value!r} が負か NaN")
    return x


def _ai_used(r: dict, where: str, strict: bool) -> Optional[str]:
    v = r.get("ai_used", "")
    if v == "" and not strict:
        return None
    _in(v, AI_USED, where, "ai_used")
    if v == "あり" and strict and (not r.get("ai_model") or not r.get("ai_log")):
        raise _err(where, "ai_used = あり なのに ai_model か ai_log が空（手順 H）")
    return v


def _check_unique_ids(items, where: str) -> None:
    c = collections.Counter(x.id for x in items)
    dup = sorted(i for i, n in c.items() if n > 1)
    if dup:
        raise _err(where, f"id が重複: {dup[:10]}")


CONTRA_COLUMNS = (ID_COL, "tree", "decl", "verdict", "condition_type", "error_class", "write_target", "unknown_reason",
                  "minutes", "ai_used")
#: 誤の原因のうち「到達しない」側（手引き 14.2・17）。D83 で `reachable` の欄を書かなくなったので、到達しない誤に
#: `condition_type` が付いていないかはこの類で確かめる（D76 の「到達するときだけ書く」）。
UNREACHABLE_ERROR_CLASSES = frozenset({"E1", "E3", "E4", "E6"})


def parse_contradiction_rows(rows: list[dict], where: str = "矛の判定表", strict: bool = True) -> list[Pair]:
    """矛の判定表を検証して `Pair` にする。`strict=False` は v4 の判定（欄の少ない旧い形）の読み込みだけに使う。"""
    if strict:
        _require_columns(rows, CONTRA_COLUMNS, where)
    out = []
    for i, r in enumerate(rows):
        w = f"{where} {i + 2} 行目（{ID_COL}={r.get(ID_COL)!r}）"
        if not r.get(ID_COL) or not r.get("tree"):
            raise _err(w, f"{ID_COL} か tree が空")
        decl = _in(r.get("decl", ""), DECLS, w, "decl")
        if r.get("verdict", "") == "":
            raise _err(w, "verdict が空（判定し残し）")
        verdict = _in(r["verdict"], VERDICTS, w, "verdict")
        # D83: `reachable`・`violates`・`condition` は書かない欄になった（verdict と error_class から分かる）。
        # 前の形の表（v4 の判定・練習の表）で書いてあれば、今までどおり 11.2 の表と突き合わせる。
        reach, viol = r.get("reachable", ""), r.get("violates", "")
        old_form = bool(reach or viol)
        if old_form:
            _in(reach, TERNARY, w, "reachable")
            if not (reach in ("いいえ", "決められない") and viol == ""):  # 11.2 の表の「—」
                _in(viol, TERNARY, w, "violates")
            expect = ("正" if reach == "はい" and viol == "はい"
                      else "誤" if reach == "いいえ" or (reach == "はい" and viol == "いいえ") else "不明")
            if verdict != expect:
                raise _err(w, f"verdict = {verdict} が reachable = {reach} / violates = {viol} と合わない（11.2 の表では {expect}）")
        conds = None
        ct = r.get("condition_type", "")
        if ct:
            conds = parse_conditions(ct, w)
            if strict and old_form and reach != "はい":
                raise _err(w, f"reachable = {reach} なのに condition_type がある（到達するときだけ書く。手順 H の既定、D76）")
        elif strict and verdict == "正":
            raise _err(w, "正なのに condition_type が空（14.3）")
        ec_raw = r.get("error_class", "")
        ec = None
        if verdict == "誤":
            if ec_raw:
                ec = parse_error_class(ec_raw, w) if strict else (parse_error_class(ec_raw, w)
                                                                  if _ERROR_CLASS_RE.match(ec_raw) else "未分類")
            elif strict:
                raise _err(w, "誤なのに error_class が空（第 17 節）")
        elif ec_raw and strict:
            raise _err(w, f"{verdict} なのに error_class = {ec_raw!r}（誤のときだけ書く）")
        if strict and old_form and ec in ("E3", "E4") and reach != "いいえ":
            raise _err(w, f"error_class = {ec} なのに reachable = {reach}（E3・E4 は いいえ。手順 H の既定、D76）")
        if strict and old_form and ec == "E5" and viol != "いいえ":
            raise _err(w, f"error_class = E5 なのに violates = {viol}（E5 は いいえ。手順 H の既定、D76）")
        if strict and not old_form and ct and ec in UNREACHABLE_ERROR_CLASSES:
            raise _err(w, f"error_class = {ec}（到達しない誤）なのに condition_type がある（到達するときだけ書く。D76・D83）")
        wt = r.get("write_target", "")
        if wt:
            _in(wt, target_vocab(decl), w, "write_target")
        elif strict and verdict == "正":
            raise _err(w, "正なのに write_target が空（第 16 節）")
        ur_class = None
        if strict and verdict == "不明":
            if not r.get("unknown_reason"):
                raise _err(w, "不明なのに unknown_reason が空（第 19 節）")
            ur_class = parse_unknown_reason(r["unknown_reason"], w)
        # D84: D1 の正には ③「変える場所をツールの引数が決めるか」を書く。ほかの行には書かない。
        tba = r.get("target_by_arg", "")
        if tba:
            _in(tba, TARGET_BY_ARG, w, "target_by_arg")
            if strict and not (decl == "D1" and verdict == "正"):
                raise _err(w, f"target_by_arg = {tba!r} は D1 の正だけに書く（D84）")
        elif strict and decl == "D1" and verdict == "正" and "target_by_arg" in r:
            raise _err(w, "D1 の正なのに target_by_arg が空（D84）")
        out.append(Pair(id=r[ID_COL], tree=r["tree"], decl=decl, verdict=verdict, conditions=conds, error_class=ec,
                        write_target=wt or None, ai_used=_ai_used(r, w, strict), minutes=_minutes(r.get("minutes", ""), w),
                        unknown_reason=r.get("unknown_reason", ""), unknown_class=ur_class,
                        target_by_arg=tba or None))
    _check_unique_ids(out, where)
    return out


MISS_COLUMNS = (ID_COL, "tree", "decl", "outcome", "cause", "write_target", "condition_type", "depth", "ai_found",
                "minutes", "ai_used")


def parse_miss_rows(rows: list[dict], where: str = "見落としの判定表", strict: bool = True) -> list[Miss]:
    if strict:
        _require_columns(rows, MISS_COLUMNS, where)
    out = []
    for i, r in enumerate(rows):
        w = f"{where} {i + 2} 行目（{ID_COL}={r.get(ID_COL)!r}）"
        if not r.get(ID_COL) or not r.get("tree"):
            raise _err(w, f"{ID_COL} か tree が空")
        decl = _in(r.get("decl", ""), ("D1", "D2"), w, "decl")
        raw = r.get("outcome", "")
        if raw == "":
            raise _err(w, "outcome が空（判定し残し）")
        outcome = MISS_OUTCOME_SUB.get(raw, raw)
        _in(outcome, MISS_OUTCOMES, w, "outcome")
        cause_raw = r.get("cause", "") or None
        cause = None
        if cause_raw:
            cause = _in(cause_raw, MISS_CAUSES, w, "cause")
        elif strict and outcome == "見落とし":
            raise _err(w, "見落としなのに cause が空（18.2 の 6）")
        if strict and outcome == "見落とし（深さ 4 の外）" and cause not in (None, "深さ"):
            raise _err(w, f"見落とし（深さ 4 の外）の cause は「深さ」（18.4、D76）。{cause!r} は合わない")
        ur_class = None
        if strict and outcome == "不明":
            if not r.get("unknown_reason"):
                raise _err(w, "不明なのに unknown_reason が空（18.4・第 19 節、D76）")
            ur_class = parse_unknown_reason(r["unknown_reason"], w)
            if (raw == "不明（打ち切り）") != (ur_class == "打ち切り"):
                raise _err(w, f"outcome = {raw} と unknown_reason の類 {ur_class} が合わない（打ち切りは `不明（打ち切り）`）")
        wt = r.get("write_target", "")
        if wt:
            _in(wt, WRITE_TARGETS, w, "write_target")
        elif strict and outcome == "見落とし":
            raise _err(w, "見落としなのに write_target が空（18.2 の 7）")
        ct = r.get("condition_type", "")
        conds = parse_conditions(ct, w) if ct else None
        if strict and outcome == "見落とし" and conds is None:
            raise _err(w, "見落としなのに condition_type が空（18.2 の 7）")
        depth = r.get("depth", "")
        if depth and not re.fullmatch(r"\d+", depth):
            raise _err(w, f"depth = {depth!r} が 0 以上の整数でない")
        if strict and outcome == "見落とし" and depth and int(depth) > 4:
            raise _err(w, f"depth = {depth} は深さ 4 の外。outcome は「見落とし（深さ 4 の外）」（18.3）")
        out.append(Miss(id=r[ID_COL], tree=r["tree"], decl=decl, outcome=outcome, outcome_raw=raw, cause=cause,
                        cause_raw=cause_raw, write_target=wt or None, conditions=conds,
                        ai_found=r.get("ai_found", "") or None, ai_used=_ai_used(r, w, strict),
                        minutes=_minutes(r.get("minutes", ""), w), unknown_reason=r.get("unknown_reason", ""),
                        unknown_class=ur_class, output_found=r.get("output_found", "") or None))
    _check_unique_ids(out, where)
    return out


UNKNOWN_COLUMNS = (ID_COL, "tree", "decl", "reasons", "outcome", "reachable", "violates", "write_target",
                   "condition_type", "unknown_reason", "minutes", "ai_used")


def parse_unknown_rows(rows: list[dict], where: str = "不の中身の判定表", strict: bool = True) -> list[UnknownPair]:
    if strict:
        _require_columns(rows, UNKNOWN_COLUMNS, where)
    out = []
    for i, r in enumerate(rows):
        w = f"{where} {i + 2} 行目（{ID_COL}={r.get(ID_COL)!r}）"
        if not r.get(ID_COL) or not r.get("tree"):
            raise _err(w, f"{ID_COL} か tree が空")
        decl = _in(r.get("decl", ""), ("D1", "D2"), w, "decl")
        if r.get("outcome", "") == "":
            raise _err(w, "outcome が空（判定し残し）")
        outcome = _in(r["outcome"], UNKNOWN_OUTCOMES, w, "outcome")
        reasons = tuple(sorted({x for x in re.split(r"[;,\s]+", r.get("reasons", "")) if x}))
        for x in reasons:
            if not re.fullmatch(r"[a-z0-9_]+", x):
                raise _err(w, f"reasons の {x!r} が理由コードの形でない")
        wt = r.get("write_target", "")
        if wt:
            _in(wt, WRITE_TARGETS, w, "write_target")
        elif strict and outcome == "違反":
            raise _err(w, "違反なのに write_target が空（18A.2 の 5）")
        ct = r.get("condition_type", "")
        conds = parse_conditions(ct, w) if ct else None
        if strict and outcome == "違反" and conds is None:
            raise _err(w, "違反なのに condition_type が空（18A.2 の 5）")
        if strict and conds is not None and r.get("reachable", "") != "はい":
            raise _err(w, "到達しない・決められないのに condition_type がある（到達するときだけ書く。D76）")
        ur_class = None
        if strict and outcome == "不明":
            if not r.get("unknown_reason"):
                raise _err(w, "不明なのに unknown_reason が空（18A.3・第 19 節）")
            ur_class = parse_unknown_reason(r["unknown_reason"], w)
        if strict:
            reach, viol = r.get("reachable", ""), r.get("violates", "")
            _in(reach, TERNARY, w, "reachable")
            if not (reach in ("いいえ", "決められない") and viol == ""):  # 11.2 の表の「—」
                _in(viol, TERNARY, w, "violates")
            expect = ("違反" if reach == "はい" and viol == "はい"
                      else "違反でない" if reach == "いいえ" or (reach == "はい" and viol == "いいえ") else "不明")
            if outcome != expect:
                raise _err(w, f"outcome = {outcome} が reachable / violates と合わない（{expect}）")
        out.append(UnknownPair(id=r[ID_COL], tree=r["tree"], decl=decl, outcome=outcome, reasons=reasons,
                               write_target=wt or None, conditions=conds, ai_used=_ai_used(r, w, strict),
                               minutes=_minutes(r.get("minutes", ""), w), unknown_reason=r.get("unknown_reason", ""),
                               unknown_class=ur_class))
    _check_unique_ids(out, where)
    return out


def read_v4_judgments(path: str) -> tuple[list[Pair], list[Miss]]:
    """`evidence/population_v4/v4_judgments.json`（D66）を読む（道具の試験だけ。手順書 6.7）。

    v4 の `error_class` は E1〜E9 の前の自由記述、`severity` は D67 の前の定義なので、誤の原因は「未分類」、
    書き込み先・条件の種類は無しとして読む。verdict・outcome・cause は今の語彙で確かめる。
    """
    with open(path, encoding="utf-8") as fh:
        d = json.load(fh)
    crow = [{ID_COL: r["id"], "tree": r["tree"], "decl": r["decl"], "verdict": r["verdict"],
             "error_class": r.get("error_class", "")} for r in d["v2"]]
    mrow = [{ID_COL: r["id"], "tree": r["tree"], "decl": r["decl"], "outcome": r["outcome"],
             "cause": r.get("cause", "")} for r in d["v3"]]
    return (parse_contradiction_rows(crow, "v4 の矛の判定", strict=False),
            parse_miss_rows(mrow, "v4 の見落としの判定", strict=False))


# --- 走査の結果から N・M_d・走査した木の数 -------------------------------------------------------------

def declares(d_kind: dict, decl: str) -> bool:
    """ユニットが宣言 decl を明示したか（事前登録 (f)、D73 の 3）。

    `authgap/dparse.py: contradiction_findings` の分岐と同じ: D1 は `readOnlyHint ∈ explicit`、D2 は
    `destructiveHint ∈ explicit` で `readOnlyHint ∉ explicit`（`elif`）、D3 は `closed_world`、D4 は `idempotent` で
    `readOnlyHint ∉ explicit`。既定値で補ったものは数えない。
    """
    ex = set(d_kind.get("explicit") or [])
    ro = "readOnlyHint" in ex
    if decl == "D1":
        return ro
    if decl == "D2":
        return "destructiveHint" in ex and not ro
    if decl == "D3":
        return bool(d_kind.get("closed_world"))
    if decl == "D4":
        return bool(d_kind.get("idempotent")) and not ro
    raise ValueError(decl)


@dataclass
class RunFacts:
    n_scanned: int
    status_counts: dict
    N: dict  # decl -> 矛の木の数
    trees_with_contradiction: dict  # decl -> sorted list
    n_contradiction_pairs: dict
    M: dict  # decl -> 宣言を明示した木の数
    unknown_pairs: dict  # decl -> 件数
    unknown_reasons: dict  # decl -> {reason: 件数}
    warnings: list = field(default_factory=list)


def run_facts(run_dir: str) -> RunFacts:
    from contradiction_by_decl import apply_flip, load_reasons
    from runlib import load_manifest, run_manifests

    manifests, warnings = run_manifests(run_dir)
    with open(os.path.join(run_dir, "summary.json"), encoding="utf-8") as fh:
        summary = json.load(fh)
    status = collections.Counter(t.get("status") for t in summary.get("trees", []))
    M = {d: 0 for d in DECLS}
    for _tree, path in manifests:
        units = load_manifest(path)["units"]
        for d in DECLS:
            if any(declares(u.get("D_kind") or {}, d) for u in units):
                M[d] += 1
    trees = {d: set() for d in DECLS}
    npairs = collections.Counter()
    unk = collections.Counter()
    unk_reasons = {d: collections.Counter() for d in DECLS}
    for key, per in load_reasons(run_dir).items():
        for d in DECLS:
            fs = per.get(d, set())
            s = apply_flip(fs, d, None)
            if s == "矛":
                trees[d].add(key[0])
                npairs[d] += 1
            elif s == "不":
                unk[d] += 1
                for st, reason in fs:
                    if st == "unknown":
                        unk_reasons[d][reason] += 1
    return RunFacts(n_scanned=len(manifests), status_counts=dict(sorted(status.items())),
                    N={d: len(trees[d]) for d in DECLS}, trees_with_contradiction={d: sorted(trees[d]) for d in DECLS},
                    n_contradiction_pairs={d: npairs[d] for d in DECLS}, M=M,
                    unknown_pairs={d: unk[d] for d in DECLS},
                    unknown_reasons={d: dict(sorted(unk_reasons[d].items())) for d in DECLS}, warnings=warnings)


def load_sample(path: str, kind: str) -> dict:
    """`scripts/final_sample.py <kind>` の出力を読む。`kind` の欄が違えば誤り（取り違えの防止）。"""
    with open(path, encoding="utf-8") as fh:
        s = json.load(fh)
    if s.get("kind") != kind:
        raise ValueError(f"{path}: kind = {s.get('kind')!r}（{kind} の抜き取りの出力を渡す）")
    if not isinstance(s.get("targets"), list):
        raise ValueError(f"{path}: targets が無い")
    return s


def sample_by_decl(sample: dict, decl: str, key: str) -> Optional[int]:
    """抜き取りの出力の `by_decl.<d>.<key>`（`final_sample.py` の形）。無ければ None。"""
    v = ((sample.get("by_decl") or {}).get(decl) or {}).get(key)
    return v if isinstance(v, int) else None


# --- 木の単位の主指標 -----------------------------------------------------------------------------------

#: 1 組の判定を (正 / 誤 / 不明) に写す読み方。(A) は判定のまま、(B)(C) は条件で正を誤に置き換える（23.5）。
Reading = Callable[[Pair], str]


def reading_A(p: Pair) -> str:
    return p.verdict


def reading_B(p: Pair) -> str:
    if p.verdict == "正" and p.conditions is not None and OPERATOR_CONDITIONS & set(p.conditions):
        return "誤"
    return p.verdict


def reading_C(p: Pair) -> str:
    if p.verdict == "正" and p.conditions is not None and p.conditions != ("なし",):
        return "誤"
    return p.verdict


def tree_counts(pairs: list[Pair], reading: Reading = reading_A) -> dict[str, tuple[int, int, int]]:
    acc: dict[str, list[int]] = collections.defaultdict(lambda: [0, 0, 0])
    for p in pairs:
        v = reading(p)
        acc[p.tree][VERDICTS.index(v)] += 1
    return {t: tuple(v) for t, v in sorted(acc.items())}


def _ratio(x: float, y: float) -> Optional[float]:
    return None if not y else x / y


def tree_metrics(counts: dict[str, tuple[int, int, int]], N: Optional[int], M: Optional[int],
                 n_scanned: Optional[int], seed: int, reps: int = B_DEFAULT) -> dict:
    """宣言 1 つ分の (a)(b)(c)、木ごとの精度の平均、bootstrap の区間（第 23.2・23.3 節）。"""
    trees = sorted(counts)
    n = len(trees)
    hit = [counts[t][0] >= 1 for t in trees]
    k = sum(hit)
    p_main = [(c / (c + w)) if (c + w) else None for c, w, _u in (counts[t] for t in trees)]
    p_unk = [(c / (c + w + u)) if (c + w + u) else None for c, w, u in (counts[t] for t in trees)]
    defined = [x for x in p_main if x is not None]
    a = _ratio(k, n)
    if N is not None and n:
        k_hat = float(k) if n == N else k / n * N
    else:
        k_hat = None
    out = {
        "n": n, "k": k, "N": N, "M_d": M, "n_scanned": n_scanned,
        "a": a, "K_hat": k_hat,
        "c": _ratio(k_hat, M) if k_hat is not None else None,
        "b": _ratio(k_hat, n_scanned) if k_hat is not None else None,
        "precision_mean": (sum(defined) / len(defined)) if defined else None,
        "n_trees_precision": len(defined), "n_trees_all_unknown": n - len(defined),
        "precision_mean_unknown_as_wrong": (sum(p_unk) / n) if n else None,
        "lower_bound_note": "(a)〜(c) は下限（1 木 3 件までしか判定しない・矛の出なかった木の見落としを数えない）",
        "per_tree": [{"tree": t, "correct": counts[t][0], "wrong": counts[t][1], "unknown": counts[t][2],
                      "precision": p_main[i], "precision_unknown_as_wrong": p_unk[i]} for i, t in enumerate(trees)],
    }
    if N is not None and n > N:
        raise ValueError(f"判定した木の数 n={n} が矛の出た木の数 N={N} を超える")
    if n < MIN_TREES_FOR_INTERVAL:
        out["interval"] = None
        out["interval_note"] = f"n = {n} < {MIN_TREES_FOR_INTERVAL}: 区間を出さない（D73 の 4）。件数と木ごとの内訳を見る"
        return out
    rng = random.Random(seed)
    idx_all = range(n)
    a_reps: list[float] = []
    pm_reps: list[float] = []
    pu_reps: list[float] = []
    undefined = 0
    for _ in range(reps):
        idx = rng.choices(idx_all, k=n)
        a_reps.append(sum(hit[i] for i in idx) / n)
        ps = [p_main[i] for i in idx if p_main[i] is not None]
        if ps:
            pm_reps.append(sum(ps) / len(ps))
        else:
            undefined += 1
        pu_reps.append(sum(p_unk[i] for i in idx) / n)
    for xs in (a_reps, pm_reps, pu_reps):
        xs.sort()

    def ci(xs: list[float], scale: Optional[float] = None) -> Optional[list[float]]:
        if not xs:
            return None
        lo, hi = percentile(xs, 0.025), percentile(xs, 0.975)
        if scale is not None:
            return [lo * scale, hi * scale]
        return [lo, hi]

    out["interval"] = {
        "reps": reps, "seed": seed, "method": "木の復元抽出・百分位（線形補間）2.5% / 97.5%",
        "a": ci(a_reps),
        "c": ci(a_reps, N / M) if (N is not None and M) else None,
        "b": ci(a_reps, N / n_scanned) if (N is not None and n_scanned) else None,
        "precision_mean": ci(pm_reps), "precision_mean_reps_undefined": undefined,
        "precision_mean_unknown_as_wrong": ci(pu_reps),
    }
    return out


def pair_level(pairs: list[Pair], reading: Reading = reading_A) -> dict:
    c = collections.Counter(reading(p) for p in pairs)
    cor, wro, unk = c["正"], c["誤"], c["不明"]
    w = wilson(cor, cor + wro)
    w2 = wilson(cor, cor + wro + unk)
    return {"judged": len(pairs), "correct": cor, "wrong": wro, "unknown": unk,
            "precision": _ratio(cor, cor + wro), "wilson95": list(w) if w else None,
            "precision_unknown_as_wrong": _ratio(cor, cor + wro + unk), "wilson95_unknown_as_wrong": list(w2) if w2 else None}


def condition_breakdown(items) -> dict:
    """条件の種類の内訳（1 件に複数あれば各種類に 1 ずつ）と、組み合わせごとの件数、(A)(B)(C) の数。"""
    per_type = collections.Counter()
    combos = collections.Counter()
    a = b = c = 0
    missing = 0
    for x in items:
        if x.conditions is None:
            missing += 1
            continue
        a += 1
        combos[";".join(x.conditions)] += 1
        for t in x.conditions:
            per_type[t] += 1
        if not (OPERATOR_CONDITIONS & set(x.conditions)):
            b += 1
        if x.conditions == ("なし",):
            c += 1
    return {"per_type": {t: per_type[t] for t in CONDITION_TYPES}, "combinations": dict(sorted(combos.items())),
            "A": a, "B": b, "C": c, "no_condition_recorded": missing}


def _class_counts(classes) -> dict:
    c = collections.Counter(x or "（類なし）" for x in classes)
    out = {k: c[k] for k in UNKNOWN_REASON_CLASSES}
    if c["（類なし）"]:
        out["（類なし）"] = c["（類なし）"]
    return out


def _minutes_summary(items) -> dict:
    ms = sorted(x.minutes for x in items if x.minutes is not None)
    return {"n_with_minutes": len(ms), "total": sum(ms) if ms else None,
            "median": percentile(ms, 0.5) if ms else None}


def impact_strata(ps: list[Pair]) -> dict:
    """D84 の層別（D1 の正だけ）。① D1（クライアントが確認を省く宣言）→ ② 重い書き込み先 → ③ 変える場所を引数が決める。

    組の数と木の数の両方を出す。③ は ② の中で数え、「決められない」と未記入も別に数える（黙って落とさない）。
    """
    correct = [p for p in ps if p.verdict == "正"]
    heavy = [p for p in correct if p.write_target in HEAVY_WRITE_TARGETS]

    def cnt(xs: list[Pair]) -> dict:
        return {"pairs": len(xs), "trees": len({p.tree for p in xs})}

    return {"_note": "D84。① D1 の正 → ② 書き込み先が重い 4 種類 → ③ 変える場所をツールの引数が決める（target_by_arg = はい）",
            "heavy_write_targets": list(HEAVY_WRITE_TARGETS),
            "step1_d1_correct": cnt(correct),
            "step2_heavy_target": cnt(heavy),
            "step3_target_by_arg_yes": cnt([p for p in heavy if p.target_by_arg == "はい"]),
            "step3_breakdown": {v: cnt([p for p in heavy if p.target_by_arg == v])["pairs"] for v in TARGET_BY_ARG}
            | {"（未記入）": sum(1 for p in heavy if not p.target_by_arg)}}


def aggregate_contradictions(pairs: list[Pair], facts: Optional[RunFacts], sample_N: dict, sample_M: dict,
                             sample_scan: Optional[int], seed: int, reps: int, warnings: list,
                             resolved: Optional[dict] = None) -> dict:
    out = {}
    for d in DECLS:
        ps = [p for p in pairs if p.decl == d]
        N = facts.N[d] if facts else sample_N.get(d)
        M = facts.M[d] if facts else sample_M.get(d)
        sc = facts.n_scanned if facts else sample_scan
        per_tree = collections.Counter(p.tree for p in ps)
        over = sorted(t for t, n in per_tree.items() if n > MAX_PAIRS_PER_TREE)
        if over:
            warnings.append(f"{d}: 1 木 {MAX_PAIRS_PER_TREE} 件を超えて判定した木 {len(over)}（{over[:5]}）。抜き取りの規則と合わない")
        if N is not None and ps:
            expect_n = min(N, MAX_TREES_PER_DECL)
            if len(per_tree) != expect_n:
                warnings.append(f"{d}: 判定した木の数 {len(per_tree)} が min(N={N}, {MAX_TREES_PER_DECL}) = {expect_n} と違う")
        if facts and ps:
            extra = sorted(set(per_tree) - set(facts.trees_with_contradiction[d]))
            if extra:
                raise ValueError(f"{d}: 走査で {d} の矛が出ていない木を判定している: {extra[:5]}")
        if pairs and not ps and N:
            warnings.append(f"{d}: 矛の出た木が {N} あるのに、判定した組が無い")
        block: dict = {"judged_pairs": len(ps)}
        if facts:
            block["n_contradiction_pairs_total"] = facts.n_contradiction_pairs[d]
        if not ps:
            block["main"] = None
            block["note"] = "判定した組が無い"
            out[d] = block
            continue
        block["main"] = tree_metrics(tree_counts(ps, reading_A), N, M, sc, seed, reps)
        have_cond = all(p.conditions is not None for p in ps if p.verdict == "正")
        if have_cond:
            block["reading_B"] = tree_metrics(tree_counts(ps, reading_B), N, M, sc, seed, reps)
            block["reading_C"] = tree_metrics(tree_counts(ps, reading_C), N, M, sc, seed, reps)
        else:
            block["reading_B"] = block["reading_C"] = None
            block["reading_note"] = "正に condition_type の無い行があり、(B)(C) を計算しない"
        block["pair_level"] = pair_level(ps)
        block["error_class"] = {e: sum(1 for p in ps if p.error_class == e) for e in (*ERROR_CLASSES, "未分類")
                                if e != "未分類" or any(p.error_class == "未分類" for p in ps)}
        vocab = target_vocab(d)
        block["write_target_of_correct"] = {t: sum(1 for p in ps if p.verdict == "正" and p.write_target == t)
                                            for t in vocab}
        block["write_target_of_correct"]["（未記入）"] = sum(1 for p in ps if p.verdict == "正" and not p.write_target)
        block["conditions_of_correct"] = condition_breakdown([p for p in ps if p.verdict == "正"])
        if d == "D1":
            block["impact_strata"] = impact_strata(ps)
        block["unknown_reasons"] = sorted(p.unknown_reason for p in ps if p.verdict == "不明" and p.unknown_reason)
        block["unknown_reason_classes"] = _class_counts(p.unknown_class for p in ps if p.verdict == "不明")
        block["ai_used"] = dict(collections.Counter(p.ai_used or "（未記入）" for p in ps))
        block["minutes"] = _minutes_summary(ps)
        if resolved:
            rs = [Pair(**{**p.__dict__, "verdict": resolved.get(p.id, p.verdict)}) for p in ps]
            block["resolved"] = {"n_replaced": sum(1 for p in ps if p.id in resolved and resolved[p.id] != p.verdict),
                                 "main": tree_metrics(tree_counts(rs), N, M, sc, seed, reps),
                                 "pair_level": pair_level(rs)}
        out[d] = block
    return out


def aggregate_misses(misses: list[Miss]) -> dict:
    def block(ms: list[Miss]) -> dict:
        oc = collections.Counter(m.outcome for m in ms)
        trunc = sum(1 for m in ms if m.outcome_raw == "不明（打ち切り）")
        main_miss = oc["見落とし"]
        ai_extra = [m.id for m in ms if m.outcome != "見落とし" and m.ai_found and m.ai_found != "なし"]
        causes = {o: {c: sum(1 for m in ms if m.outcome == o and m.cause == c) for c in MISS_CAUSES}
                  for o in ("見落とし", "見落とし（深さ 4 の外）")}
        return {
            "judged": len(ms),
            "outcomes": {o: oc[o] for o in MISS_OUTCOMES},
            "unknown_truncated_subcount": trunc,
            "miss_main": main_miss,
            "miss_rate_main": _ratio(main_miss, len(ms)),
            "miss_beyond_depth4": oc["見落とし（深さ 4 の外）"],
            "ai_found_checked": sum(1 for m in ms if m.ai_found is not None),
            "ai_found_new": sum(1 for m in ms if m.ai_found and m.ai_found != "なし"),
            "miss_with_ai_added": main_miss + len(ai_extra),
            "ai_added_units": ai_extra,
            "causes": causes,
            "write_target_of_miss": {t: sum(1 for m in ms if m.outcome == "見落とし" and m.write_target == t)
                                     for t in WRITE_TARGETS},
            "conditions_of_miss": condition_breakdown([m for m in ms if m.outcome == "見落とし"]),
            "unknown_reasons": sorted(m.unknown_reason for m in ms if m.outcome == "不明" and m.unknown_reason),
            "unknown_reason_classes": _class_counts(m.unknown_class for m in ms if m.outcome == "不明"),
            "output_found": sum(1 for m in ms if m.output_found),
            "ai_used": dict(collections.Counter(m.ai_used or "（未記入）" for m in ms)),
            "minutes": _minutes_summary(ms),
        }

    per_tree = collections.Counter(m.tree for m in misses)
    out = {"all": block(misses), "by_decl": {d: block([m for m in misses if m.decl == d]) for d in ("D1", "D2")},
           "trees_with_more_than_one_unit": sorted(t for t, n in per_tree.items() if n > 1)}
    return out


def aggregate_unknowns(items: list[UnknownPair], facts: Optional[RunFacts], seed: int, reps: int) -> dict:
    out: dict = {}
    if facts:
        out["totals"] = {d: {"pairs": facts.unknown_pairs[d], "reasons": facts.unknown_reasons[d]} for d in DECLS}
    judged = {}
    for d in ("D1", "D2"):
        xs = [x for x in items if x.decl == d]
        oc = collections.Counter(x.outcome for x in xs)
        # 1 木 1 組なので木の割合は組の割合。木を単位にした bootstrap は主指標と同じ関数で（正 = 違反、誤 = 違反でない）。
        as_pairs = [Pair(id=x.id, tree=x.tree, decl=d, verdict={"違反": "正", "違反でない": "誤", "不明": "不明"}[x.outcome])
                    for x in xs]
        tm = tree_metrics(tree_counts(as_pairs), None, None, None, seed, reps) if xs else None
        by_reason = collections.defaultdict(collections.Counter)
        for x in xs:
            for r in x.reasons or ("（理由なし）",):
                by_reason[r][x.outcome] += 1
        judged[d] = {
            "judged": len(xs), "outcomes": {o: oc[o] for o in UNKNOWN_OUTCOMES},
            # 主: 不明を分母から除く（D70 の 5 と同じ扱い。1 木 1 組なので木の精度の平均 = 決まった木のうち違反の割合）。
            "violation_rate_trees": tm["precision_mean"] if tm else None,
            "violation_rate_trees_interval": (tm["interval"] or {}).get("precision_mean") if tm else None,
            "n_trees_decided": tm["n_trees_precision"] if tm else 0,
            # 併記: 不明を「違反でない」とみなす（分母に入れる）
            "violation_rate_trees_unknown_as_not": tm["precision_mean_unknown_as_wrong"] if tm else None,
            "violation_rate_trees_unknown_as_not_interval":
                (tm["interval"] or {}).get("precision_mean_unknown_as_wrong") if tm else None,
            "by_reason": {r: {o: c[o] for o in UNKNOWN_OUTCOMES} for r, c in sorted(by_reason.items())},
            "write_target_of_violation": {t: sum(1 for x in xs if x.outcome == "違反" and x.write_target == t)
                                          for t in WRITE_TARGETS},
            "conditions_of_violation": condition_breakdown([x for x in xs if x.outcome == "違反"]),
            "unknown_reasons": sorted(x.unknown_reason for x in xs if x.outcome == "不明" and x.unknown_reason),
            "unknown_reason_classes": _class_counts(x.unknown_class for x in xs if x.outcome == "不明"),
            "trees_with_more_than_one_pair": sorted(t for t, n in collections.Counter(x.tree for x in xs).items() if n > 1),
            "interval_note": (tm or {}).get("interval_note"),
        }
    out["judged"] = judged
    return out


def agreement(primary: dict[str, str], second_rows: list[dict], label_col: str, vocab, where: str) -> dict:
    a, b, ids = [], [], []
    for i, r in enumerate(second_rows):
        w = f"{where} {i + 2} 行目（{ID_COL}={r.get(ID_COL)!r}）"
        if r.get(ID_COL) not in primary:
            raise _err(w, f"主の判定表に無い {ID_COL}")
        v = r.get(label_col, "")
        v = MISS_OUTCOME_SUB.get(v, v)
        _in(v, vocab, w, label_col)
        ids.append(r[ID_COL])
        a.append(primary[r[ID_COL]])
        b.append(v)
    if len(set(ids)) != len(ids):
        raise _err(where, "id が重複")
    res = cohen_kappa(a, b)
    res["disagreeing_ids"] = sorted(i for i, x, y in zip(ids, a, b, strict=False) if x != y)
    res["confusion"] = {f"{x}→{y}": n for (x, y), n in sorted(collections.Counter(zip(a, b, strict=False)).items())}
    return res


# --- Markdown -----------------------------------------------------------------------------------------

def _f(x, pct: bool = True) -> str:
    if x is None:
        return "—"
    return f"{x * 100:.1f}%" if pct else (f"{x:.2f}" if isinstance(x, float) else str(x))


def _ci(x) -> str:
    return "—" if not x else f"{x[0] * 100:.1f}〜{x[1] * 100:.1f}%"


def to_markdown(res: dict) -> str:
    o = ["# 最終評価の集計", "", f"seed（bootstrap）= {res['seed']}、反復 {res['reps']}。宣言ごとに読み、**合算しない**。",
         "(a)〜(c) はどれも**下限**（1 木 3 件までしか判定しない・矛の出なかった木の見落としを数えない）。",
         "(B)(C) は条件つきの位置で正が見つかれば読むのを止めてよいので、これも**下限**（D76）。", ""]
    if res.get("run"):
        r = res["run"]
        o += [f"走査した木（ok）: {r['n_scanned']}。状態: {r['status_counts']}", ""]
    o += ["## 主指標（木の単位）", "",
          "| 宣言 | 読み方 | n | k | N | M_d | (a) k/n | 区間 | K̂ | (c) K̂/M_d | 区間 | (b) K̂/走査 | 区間 | 木ごとの精度 | 区間 | 全部不明の木 | 不明=誤 |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for d, blk in res["contradictions"].items():
        for name in ("main", "reading_B", "reading_C"):
            m = blk.get(name)
            if not m:
                continue
            iv = m.get("interval") or {}
            o.append(f"| {d} | {dict(main='(A) 主', reading_B='(B)', reading_C='(C)')[name]} | {m['n']} | {m['k']} | "
                     f"{_f(m['N'], False)} | {_f(m['M_d'], False)} | {_f(m['a'])} | {_ci(iv.get('a'))} | "
                     f"{_f(m['K_hat'], False)} | {_f(m['c'])} | {_ci(iv.get('c'))} | {_f(m['b'])} | {_ci(iv.get('b'))} | "
                     f"{_f(m['precision_mean'])} | {_ci(iv.get('precision_mean'))} | {m['n_trees_all_unknown']} | "
                     f"{_f(m['precision_mean_unknown_as_wrong'])} |")
    o.append("")
    for d, blk in res["contradictions"].items():
        m = blk.get("main")
        if m and m.get("interval") is None:
            o += [f"### {d}: 木ごとの内訳（n = {m['n']} < {MIN_TREES_FOR_INTERVAL}。区間を出さない）", "",
                  "| 木 | 正 | 誤 | 不明 | 精度 |", "|---|---|---|---|---|"]
            o += [f"| {t['tree']} | {t['correct']} | {t['wrong']} | {t['unknown']} | {_f(t['precision'])} |" for t in m["per_tree"]]
            o.append("")
    o += ["## 参考: 件数の精度（Wilson 95%）", "",
          "| 宣言 | 判定 | 正 | 誤 | 不明 | 精度 | Wilson | 不明=誤 | Wilson |", "|---|---|---|---|---|---|---|---|---|"]
    for d, blk in res["contradictions"].items():
        p = blk.get("pair_level")
        if p:
            o.append(f"| {d} | {p['judged']} | {p['correct']} | {p['wrong']} | {p['unknown']} | {_f(p['precision'])} | "
                     f"{_ci(p['wilson95'])} | {_f(p['precision_unknown_as_wrong'])} | {_ci(p['wilson95_unknown_as_wrong'])} |")
    if res.get("tool_check_v4"):
        t = res["tool_check_v4"]
        o += ["", f"**道具の試験（v4、手順書 6.7。主指標ではない）**: D1+D2 の件数の精度 {t['correct']} / {t['decided']} = "
                  f"{_f(t['precision'])}（Wilson {_ci(t['wilson95'])}）。期待 46 / 60: {'一致' if t['matches_expected'] else '**不一致**'}"]
    o += ["", "## 誤の原因・書き込み先・条件", ""]
    for d, blk in res["contradictions"].items():
        if not blk.get("pair_level"):
            continue
        o.append(f"- {d} 誤の原因: " + ", ".join(f"{k} {v}" for k, v in blk["error_class"].items()))
        o.append(f"- {d} 正の{'通信先' if d == 'D3' else '書き込み先'}: "
                 + ", ".join(f"{k} {v}" for k, v in blk["write_target_of_correct"].items()))
        cb = blk["conditions_of_correct"]
        o.append(f"- {d} 正の条件: " + ", ".join(f"{k} {v}" for k, v in cb["per_type"].items())
                 + f"。(A) {cb['A']} / (B) {cb['B']} / (C) {cb['C']}（条件の記入なし {cb['no_condition_recorded']}）")
        if blk.get("impact_strata"):
            st = blk["impact_strata"]
            o.append(f"- {d} の層別（D84）: ① 正 {st['step1_d1_correct']['pairs']} 組・{st['step1_d1_correct']['trees']} 木"
                     f" → ② 重い書き込み先 {st['step2_heavy_target']['pairs']} 組・{st['step2_heavy_target']['trees']} 木"
                     f" → ③ 場所を引数が決める {st['step3_target_by_arg_yes']['pairs']} 組・{st['step3_target_by_arg_yes']['trees']} 木"
                     f"（③ の内訳: " + ", ".join(f"{k} {v}" for k, v in st["step3_breakdown"].items()) + "）")
    if res.get("misses"):
        a = res["misses"]["all"]
        o += ["", "## 見落とし", "", f"判定 {a['judged']}。" + ", ".join(f"{k} {v}" for k, v in a["outcomes"].items())
              + f"（不明のうち打ち切り {a['unknown_truncated_subcount']}）", "",
              f"- 主の見落とし: {a['miss_main']}（{_f(a['miss_rate_main'])}）。深さ 4 の外（主に入れない）: {a['miss_beyond_depth4']}",
              f"- AI の点検を足した見落とし: {a['miss_with_ai_added']}（ai_found の新しい動作 {a['ai_found_new']}、点検した {a['ai_found_checked']}）",
              "- 見落としの原因: " + ", ".join(f"{k} {v}" for k, v in a["causes"]["見落とし"].items())]
        for d, b in res["misses"]["by_decl"].items():
            o.append(f"- {d}: 判定 {b['judged']}、" + ", ".join(f"{k} {v}" for k, v in b["outcomes"].items()))
    if res.get("unknowns"):
        u = res["unknowns"]
        o += ["", "## 不", ""]
        for d, t in (u.get("totals") or {}).items():
            o.append(f"- {d} 不の組 {t['pairs']}: " + ", ".join(f"`{k}` {v}" for k, v in t["reasons"].items()))
        for d, j in u["judged"].items():
            o.append(f"- {d} 判定した不 {j['judged']}: " + ", ".join(f"{k} {v}" for k, v in j["outcomes"].items())
                     + f"。違反だった木の割合（不明を除く、{j['n_trees_decided']} 木）{_f(j['violation_rate_trees'])}"
                     f"（区間 {_ci(j['violation_rate_trees_interval'])}）、不明を違反でないとみなすと "
                     f"{_f(j['violation_rate_trees_unknown_as_not'])}")
    if res.get("agreement"):
        o += ["", "## 判定の一致", "", "| 種類 | 件数 | 一致率 | κ | 食い違い |", "|---|---|---|---|---|"]
        for kind, g in res["agreement"].items():
            o.append(f"| {kind} | {g['n']} | {_f(g['percent_agreement'])} | {_f(g['kappa'], False)} | {g.get('disagree', 0)} |")
    if res.get("warnings"):
        o += ["", "## 警告", ""] + [f"- {w}" for w in res["warnings"]]
    return "\n".join(o) + "\n"


# --- main ------------------------------------------------------------------------------------------------

def check_against_sample(sample: dict, items, kind: str, allow_partial: bool, warnings: list) -> None:
    """判定表の行と抜き取りの targets が `pair_id` で 1 対 1 で、(tree, decl) が同じか。"""
    tid = {t[ID_COL]: t for t in sample["targets"] if ID_COL in t}
    if len(tid) != len(sample["targets"]):
        raise ValueError(f"{kind} の抜き取り: {ID_COL} の無い target か重複がある")
    judged = {p.id: p for p in items}
    extra = sorted(set(judged) - set(tid))
    missing = sorted(set(tid) - set(judged))
    if extra:
        raise ValueError(f"{kind}: 抜き取りに無い {ID_COL} を判定している: {extra[:10]}")
    for i, p in judged.items():
        t = tid[i]
        if t.get("tree") != p.tree or t.get("decl") != p.decl:
            raise ValueError(f"{kind} {i}: 判定表の (tree, decl) = ({p.tree}, {p.decl}) が抜き取り "
                             f"({t.get('tree')}, {t.get('decl')}) と違う")
    if missing:
        msg = f"{kind}: 抜き取りの {len(missing)} 組が判定表に無い（判定し残し）: {missing[:10]}"
        if not allow_partial:
            raise ValueError(msg)
        warnings.append(msg + "（--allow-partial。主の結果に使わない）")


def reconcile_contradiction_sample(sample: dict, facts: Optional[RunFacts], warnings: list) -> tuple[dict, dict, Optional[int]]:
    """矛の抜き取りの件数を走査と突き合わせ、`(N, M_d, 走査した木の数)` を返す（走査が無ければ抜き取りの値）。

    N（`by_decl.<d>.n_trees`）・矛の組の数（`n_pairs`）・走査した木の数（`denominators.n_trees_scanned`）の食い違いは誤り。
    M_d（`denominators.M_d`）の食い違いは、両方を出力に残して警告にする（この script の `declares()` は解析器の
    `contradiction_findings` と同じ `elif` / `not read_only` を当てる。`final_sample.py: declared` は当てない）。
    """
    N = {d: sample_by_decl(sample, d, "n_trees") for d in DECLS}
    den = sample.get("denominators") or {}
    sM = den.get("M_d") or {}
    sScan = den.get("n_trees_scanned")
    if facts is None:
        missing = [d for d in DECLS if N[d] is None]
        if missing:
            raise ValueError(f"--run が無く、矛の抜き取りにも by_decl.<d>.n_trees が無い: {missing}")
        warnings.append("--run が無い。N・M_d・走査した木の数を矛の抜き取りの出力から取った（M_d は final_sample.py の定義）")
        return N, {d: sM.get(d) for d in DECLS}, sScan
    for d in DECLS:
        if N[d] is not None and N[d] != facts.N[d]:
            raise ValueError(f"{d}: 抜き取りの矛の木の数 {N[d]} が走査の N = {facts.N[d]} と違う")
        sp = sample_by_decl(sample, d, "n_pairs")
        if sp is not None and sp != facts.n_contradiction_pairs[d]:
            raise ValueError(f"{d}: 抜き取りの矛の組の数 {sp} が走査の {facts.n_contradiction_pairs[d]} と違う")
        if d in sM and sM[d] != facts.M[d]:
            warnings.append(f"{d}: M_d が食い違う（この script {facts.M[d]}、抜き取りの出力 {sM[d]}）。"
                            "主は解析器と同じ条件のこの script の値。両方を run.M_d_sample に残す")
    if sScan is not None and sScan != facts.n_scanned:
        raise ValueError(f"走査した木の数が食い違う（走査 {facts.n_scanned}、抜き取り {sScan}）")
    return facts.N, facts.M, facts.n_scanned


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", help="主の走査の run ディレクトリ（N・M_d・走査した木の数・不の総数）")
    ap.add_argument("--contradiction-sample", help="final_sample.py contradiction の出力（pair_id の突き合わせと N の照合）")
    ap.add_argument("--miss-sample", help="final_sample.py miss の出力（pair_id の突き合わせと対象の総数）")
    ap.add_argument("--unknown-sample", help="final_sample.py unknown の出力（pair_id の突き合わせと不の総数の照合）")
    ap.add_argument("--contradictions", help="矛の判定表（CSV）")
    ap.add_argument("--misses", help="見落としの判定表（CSV）")
    ap.add_argument("--unknowns", help="不の中身の判定表（CSV）")
    ap.add_argument("--second-contradictions")
    ap.add_argument("--second-misses")
    ap.add_argument("--second-unknowns")
    ap.add_argument("--resolved-contradictions", help="話し合いで決めたラベル（pair_id, verdict）")
    ap.add_argument("--v4-judgments", help="道具の試験: evidence/population_v4/v4_judgments.json を読む（手順書 6.7）")
    ap.add_argument("--seed", type=int, required=True, help="seed ④（bootstrap）")
    ap.add_argument("--reps", type=int, default=B_DEFAULT)
    ap.add_argument("--allow-partial", action="store_true", help="判定し残しを許す（練習用。結果に印が付く）")
    ap.add_argument("--out-json")
    ap.add_argument("--out-md")
    a = ap.parse_args(argv)

    warnings: list[str] = []
    if a.v4_judgments and (a.contradictions or a.misses):
        ap.error("--v4-judgments と判定表は同時に使わない")
    facts = run_facts(a.run) if a.run else None
    if facts:
        warnings += facts.warnings
    csample = load_sample(a.contradiction_sample, "contradiction") if a.contradiction_sample else None
    msample = load_sample(a.miss_sample, "miss") if a.miss_sample else None
    usample = load_sample(a.unknown_sample, "unknown") if a.unknown_sample else None
    sample_N: dict = {}
    sample_M: dict = {}
    sample_scan = None
    if csample is not None:
        sample_N, sample_M, sample_scan = reconcile_contradiction_sample(csample, facts, warnings)
    if usample is not None and facts is not None:
        for d in DECLS:
            sp = sample_by_decl(usample, d, "n_pairs")
            if sp is not None and sp != facts.unknown_pairs[d]:
                raise ValueError(f"{d}: 不の抜き取りの組の数 {sp} が走査の不の組 {facts.unknown_pairs[d]} と違う")
            rp = ((usample.get("by_decl") or {}).get(d) or {}).get("reason_pairs")
            if isinstance(rp, dict) and rp != facts.unknown_reasons[d]:
                raise ValueError(f"{d}: 不の抜き取りの理由ごとの数が走査と違う（{rp} / {facts.unknown_reasons[d]}）")

    pairs: list[Pair] = []
    misses: list[Miss] = []
    if a.v4_judgments:
        pairs, misses = read_v4_judgments(a.v4_judgments)
        warnings.append("v4 の判定（D66）を読んだ。抜き取りの規則が違う（1 木 3 件の上限なし）ので木の単位の値は比べられない"
                        "（手順書 6.7）。誤の原因は「未分類」、書き込み先・条件の種類は無い")
    if a.contradictions:
        pairs = parse_contradiction_rows(read_csv(a.contradictions))
    if a.misses:
        misses = parse_miss_rows(read_csv(a.misses))
    unknowns = parse_unknown_rows(read_csv(a.unknowns)) if a.unknowns else []
    if not facts and not sample_N and pairs:
        raise ValueError("N が決まらない: --run か --contradiction-sample を渡す")
    for smp, items, kind, given in ((csample, pairs, "contradiction", a.contradictions),
                                    (msample, misses, "miss", a.misses), (usample, unknowns, "unknown", a.unknowns)):
        if smp is not None and given:
            check_against_sample(smp, items, kind, a.allow_partial, warnings)

    resolved = None
    if a.resolved_contradictions:
        rrows = read_csv(a.resolved_contradictions)
        ids = {p.id for p in pairs}
        resolved = {}
        for i, r in enumerate(rrows):
            w = f"話し合いのラベル {i + 2} 行目"
            if r.get(ID_COL) not in ids:
                raise _err(w, f"主の判定表に無い {ID_COL} {r.get(ID_COL)!r}")
            resolved[r[ID_COL]] = _in(r.get("verdict", ""), VERDICTS, w, "verdict")

    res: dict = {"_note": "scripts/final_aggregate.py の出力（第 23 節、事前登録 (f)(g)）。宣言ごと、合算しない。",
                 "seed": a.seed, "reps": a.reps, "partial": bool(a.allow_partial),
                 "inputs": {k: v for k, v in vars(a).items() if v and k not in ("seed", "reps")}}
    if facts:
        res["run"] = {"n_scanned": facts.n_scanned, "status_counts": facts.status_counts, "N": facts.N, "M_d": facts.M,
                      "n_contradiction_pairs": facts.n_contradiction_pairs,
                      **({"M_d_sample": (csample.get("denominators") or {}).get("M_d")} if csample is not None else {})}
    elif csample is not None:
        res["run"] = {"n_scanned": sample_scan, "status_counts": None, "N": sample_N, "M_d": sample_M,
                      "source": "矛の抜き取りの出力（--run なし）"}
    res["contradictions"] = aggregate_contradictions(pairs, facts, sample_N, sample_M, sample_scan, a.seed, a.reps,
                                                     warnings, resolved)
    if a.v4_judgments:
        d12 = [p for p in pairs if p.decl in ("D1", "D2")]
        pl = pair_level(d12)
        res["tool_check_v4"] = {"note": "道具の試験だけ（手順書 6.7）。D1 と D2 を合わせた件数の精度で、主指標ではない",
                                "correct": pl["correct"], "decided": pl["correct"] + pl["wrong"],
                                "precision": pl["precision"], "wilson95": pl["wilson95"],
                                "matches_expected": (pl["correct"], pl["correct"] + pl["wrong"]) == (46, 60)}
    if misses:
        res["misses"] = aggregate_misses(misses)
        if msample is not None:
            res["misses"]["pool"] = msample.get("pool")
    if unknowns or facts or usample is not None:
        res["unknowns"] = aggregate_unknowns(unknowns, facts, a.seed, a.reps)
        if facts is None and usample is not None:
            res["unknowns"]["totals"] = {d: {"pairs": sample_by_decl(usample, d, "n_pairs"),
                                             "reasons": ((usample.get("by_decl") or {}).get(d) or {}).get("reason_pairs")}
                                         for d in DECLS}
    agr = {}
    if a.second_contradictions:
        agr["矛"] = agreement({p.id: p.verdict for p in pairs}, read_csv(a.second_contradictions), "verdict", VERDICTS,
                             "2 人目（矛）")
    if a.second_misses:
        agr["見落とし"] = agreement({m.id: m.outcome for m in misses}, read_csv(a.second_misses), "outcome",
                                MISS_OUTCOMES, "2 人目（見落とし）")
    if a.second_unknowns:
        agr["不の中身"] = agreement({x.id: x.outcome for x in unknowns}, read_csv(a.second_unknowns), "outcome",
                                UNKNOWN_OUTCOMES, "2 人目（不の中身）")
    if agr:
        res["agreement"] = agr
    res["warnings"] = warnings
    for w in warnings:
        print(f"警告: {w}", file=sys.stderr)
    if a.out_json:
        with open(a.out_json, "w", encoding="utf-8") as fh:
            json.dump(res, fh, ensure_ascii=False, indent=1, sort_keys=False)
            fh.write("\n")
    md = to_markdown(res)
    if a.out_md:
        with open(a.out_md, "w", encoding="utf-8") as fh:
            fh.write(md)
    print(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
