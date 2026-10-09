"""`scripts/check_survey_practice.py`（実態調査の形の練習の表の書き方の確かめ）の試験。入力は全部合成。"""

from __future__ import annotations

import csv
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import check_survey_practice as cs  # noqa: E402

BASE = {
    "pair_id": "X-01", "tree": "t", "outcome": "", "write_target": "", "condition_type": "", "condition": "",
    "depth": "", "unknown_reason": "", "evidence": "", "ai_found": "", "note": "", "minutes": "20",
    "ai_used": "なし", "ai_model": "", "ai_log": "", "stopped_early": "違反なし", "t_start": "10:00",
    "t_end": "10:25", "t_break": "5", "t_noai": "20", "t_ai": "0", "t_guide": "3", "t_setup": "2",
}


def row(**kw):
    r = dict(BASE)
    r.update(kw)
    return r


VIOLATION = dict(outcome="違反", write_target="ログ", condition_type="引数", condition="引数 save=True のとき",
                 depth="2", evidence="a.py:10 → a.py:20 open(p, 'a')／読んだ範囲: a.py:1-30", stopped_early="いいえ")


def test_good_violation_row_passes():
    errs, notes = cs.check_row(row(**VIOLATION))
    assert errs == [] and notes == []


def test_good_no_violation_row_passes():
    errs, _ = cs.check_row(row(outcome="違反でない", evidence="読んだ範囲: a.py:1-40（深さ 0）。GET だけ。"))
    assert errs == []


def test_no_violation_needs_read_range():
    errs, _ = cs.check_row(row(outcome="違反でない", evidence="書き込みは無い"))
    assert any("読んだ範囲" in e for e in errs)


def test_labels_are_only_for_violations():
    errs, _ = cs.check_row(row(outcome="違反でない", evidence="読んだ範囲: a.py:1-9", write_target="ログ"))
    assert any("write_target" in e for e in errs)


def test_violation_vocab_and_depth():
    errs, _ = cs.check_row(row(**{**VIOLATION, "write_target": "ファイル"}))
    assert any("write_target" in e for e in errs)
    errs, _ = cs.check_row(row(**{**VIOLATION, "condition_type": "なし;引数"}))
    assert any("なし" in e for e in errs)
    errs, _ = cs.check_row(row(**{**VIOLATION, "depth": "5"}))
    assert any("深さ 4 の外" in e for e in errs)
    errs, _ = cs.check_row(row(**{**VIOLATION, "outcome": "違反（深さ 4 の外）", "depth": "3"}))
    assert any("深さ 4 の中" in e for e in errs)


def test_condition_text_required_unless_none():
    errs, _ = cs.check_row(row(**{**VIOLATION, "condition": ""}))
    assert any("condition" in e for e in errs)
    errs, _ = cs.check_row(row(**{**VIOLATION, "condition_type": "なし", "condition": ""}))
    assert errs == []


def test_other_unknown_target_needs_note_prefix():
    errs, _ = cs.check_row(row(**{**VIOLATION, "write_target": "その他・不明"}))
    assert any("その他:" in e for e in errs)
    errs, _ = cs.check_row(row(**{**VIOLATION, "write_target": "その他・不明", "note": "その他: 受け渡しファイル"}))
    assert errs == []


def test_unknown_needs_class_and_rejects_truncation_class():
    errs, _ = cs.check_row(row(outcome="不明", evidence="a.py:3", unknown_reason="よく分からない"))
    assert errs
    errs, _ = cs.check_row(row(outcome="不明", evidence="a.py:3", unknown_reason="打ち切り: 解析器"))
    assert any("打ち切り" in e for e in errs)
    errs, notes = cs.check_row(row(outcome="不明", evidence="a.py:3／読んだ範囲: a.py:1-9",
                                   unknown_reason="相手の API: a.py:3 の POST の意味が文書に無い"))
    assert errs == [] and notes == []
    errs, _ = cs.check_row(row(outcome="不明", evidence="a.py:3", unknown_reason="相手の API: a.py:3 の POST"))
    assert any("読んだ範囲" in e for e in errs)


def test_stopped_early_matches_outcome():
    errs, _ = cs.check_row(row(**{**VIOLATION, "stopped_early": "違反なし"}))
    assert any("stopped_early" in e for e in errs)
    errs, _ = cs.check_row(row(outcome="違反でない", evidence="読んだ範囲: a.py:1", stopped_early="はい"))
    assert any("stopped_early" in e for e in errs)
    _, notes = cs.check_row(row(**{**VIOLATION, "stopped_early": "はい"}))
    assert any("最初の違反で止めた" in n for n in notes)


def test_ai_fields():
    errs, _ = cs.check_row(row(**{**VIOLATION, "ai_used": "あり"}))
    assert any("ai_model" in e for e in errs) and any("ai_found" in e for e in errs)
    errs, _ = cs.check_row(row(**{**VIOLATION, "ai_found": "なし"}))
    assert any("ai_found" in e for e in errs)
    errs, _ = cs.check_row(row(**{**VIOLATION, "t_ai": "4"}))
    assert any("t_ai" in e for e in errs)


def test_times_and_minutes():
    errs, _ = cs.check_row(row(**{**VIOLATION, "t_start": "25:00"}))
    assert any("t_start" in e for e in errs)
    errs, _ = cs.check_row(row(**{**VIOLATION, "minutes": "20.5"}))
    assert any("minutes" in e for e in errs)
    _, notes = cs.check_row(row(**{**VIOLATION, "t_end": "11:00"}))
    assert any("t_end" in n for n in notes)
    errs, _ = cs.check_row(row(**{**VIOLATION, "t_guide": "30"}))
    assert any("t_guide" in e for e in errs)


def test_newline_in_cell_is_an_error():
    errs, _ = cs.check_row(row(**{**VIOLATION, "evidence": "a.py:1\na.py:2"}))
    assert any("改行" in e for e in errs)


def test_main_skips_unjudged_rows_and_checks_the_practice_sheet_columns(tmp_path, capsys):
    sheet = os.path.join(ROOT, "evidence", "practice_v4", "survey_practice.csv")
    assert cs.main([sheet]) == 0  # 配った表は未記入で、欄がそろっている
    out = capsys.readouterr().out
    assert "まだ判定していない" in out and "誤りなし" in out
    assert cs.main([sheet, "--all"]) == 1

    p = tmp_path / "s.csv"
    cols = list(BASE) + ["target_by_arg"]
    with open(p, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerow({**row(**VIOLATION), "target_by_arg": ""})
    assert cs.main([str(p)]) == 1
    assert "使わない欄" in capsys.readouterr().out


def test_condition_order_and_none_with_text_are_notes():
    _, notes = cs.check_row(row(**{**VIOLATION, "condition_type": "運用者の設定;失敗・期限切れ"}))
    assert any("失敗・期限切れ;運用者の設定" in n for n in notes)
    _, notes = cs.check_row(row(**{**VIOLATION, "condition_type": "なし", "condition": "毎回"}))
    assert any("なし" in n for n in notes)


def test_ai_found_must_be_exactly_nashi():
    base = {**VIOLATION, "ai_used": "あり", "ai_model": "m 1（Web、記憶なし）", "ai_log": "ai_logs/X-01.md", "t_ai": "0"}
    errs, _ = cs.check_row(row(**{**base, "ai_found": "なし"}))
    assert errs == []
    for bad in ("無し", "なし。", "特になし"):
        errs, _ = cs.check_row(row(**{**base, "ai_found": bad}))
        assert any("ひらがな 2 文字" in e for e in errs), bad


def test_violation_without_read_range_is_a_note():
    _, notes = cs.check_row(row(**{**VIOLATION, "evidence": "a.py:10 → a.py:20 open(p, 'a')"}))
    assert any("読んだ範囲" in n for n in notes)
