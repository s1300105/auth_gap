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
                 depth="2", evidence="a.py:10 → a.py:20 open(p, 'a')／読んだ範囲: a.py:1-30", stopped_early="いいえ",
                 note="最初の違反: 5 分（深さ 2 の a.py:20）")


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
    errs, _ = cs.check_row(row(**{**VIOLATION, "write_target": "その他・不明", "note": "その他: 受け渡しファイル／最初の違反: 5 分（深さ 2 の a.py:20）"}))
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
    errs, _ = cs.check_row(row(**{**VIOLATION, "stopped_early": "はい"}))
    assert any("最初の違反で止めた" in e for e in errs)  # 03_record が「必ず」とする書き方は誤り
    errs, _ = cs.check_row(row(**{**VIOLATION, "stopped_early": "はい", "note": "最初の違反で止めた（深さ 2 まで読んだ）"}))
    assert errs == []
    errs, _ = cs.check_row(row(**{**VIOLATION, "outcome": "違反（深さ 4 の外）", "depth": "6", "stopped_early": "はい",
                                  "note": "最初の違反で止めた（深さ 6 まで読んだ）"}))
    assert any("深さ 4 の外" in e and "いいえ" in e for e in errs)


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


def test_condition_order_and_none_with_text_are_errors():
    errs, _ = cs.check_row(row(**{**VIOLATION, "condition_type": "運用者の設定;失敗・期限切れ"}))
    assert any("失敗・期限切れ;運用者の設定" in e for e in errs)  # 集計は書いた順の組み合わせを数える
    errs, _ = cs.check_row(row(**{**VIOLATION, "condition_type": "なし", "condition": "毎回"}))
    assert any("なし" in e for e in errs)


AI_BASE = {**VIOLATION, "ai_used": "あり", "ai_model": "m 1（Web、記憶なし）", "ai_log": "ai_logs/X-01.md", "t_ai": "0",
           "note": "最初の違反: 5 分（深さ 2 の a.py:20）／AI の前の判定: 違反"}


def test_ai_found_must_be_exactly_nashi_or_name_a_line():
    errs, _ = cs.check_row(row(**{**AI_BASE, "ai_found": "なし"}))
    assert errs == []
    errs, _ = cs.check_row(row(**{**AI_BASE, "ai_found": "src/a.py:40: open(p, 'w') で設定ファイルを書く"}))
    assert errs == []
    # 集計は「なし」と同じ字だけを「無し」と数えるので、ほかの書き方は「新しい動作あり」に数えられてしまう
    for bad in ("無し", "なし。", "特になし", "特に無し", "ない", "None", "N/A", "見つからなかった"):
        errs, _ = cs.check_row(row(**{**AI_BASE, "ai_found": bad}))
        assert any("ひらがな 2 文字" in e for e in errs), bad


def test_ai_used_needs_the_pre_ai_outcome_in_note():
    errs, _ = cs.check_row(row(**{**AI_BASE, "ai_found": "なし", "note": ""}))
    assert any("AI の前の判定" in e for e in errs)


def test_not_stopping_needs_the_first_violation_minute():
    errs, _ = cs.check_row(row(**{**VIOLATION, "note": ""}))
    assert any("最初の違反:" in e for e in errs)


def test_space_before_colon_in_unknown_reason_gets_a_hint():
    errs, _ = cs.check_row(row(outcome="不明", evidence="a.py:3／読んだ範囲: a.py:1-9", unknown_reason="相手の API : a.py:3 の POST"))
    assert any("空白" in e for e in errs)


def test_unknown_reason_needs_an_explanation():
    errs, _ = cs.check_row(row(outcome="不明", evidence="a.py:3／読んだ範囲: a.py:1-9", unknown_reason="相手の API"))
    assert any("説明" in e for e in errs)


def test_time_errors_are_reported_even_with_other_errors():
    errs, _ = cs.check_row(row(**{**VIOLATION, "write_target": "ファイル", "t_ai": "5", "t_guide": "40"}))
    assert any("write_target" in e for e in errs)
    assert any("t_ai" in e for e in errs) and any("t_guide" in e for e in errs)


def test_time_with_seconds_gets_a_hint():
    errs, _ = cs.check_row(row(**{**VIOLATION, "t_start": "10:00:00"}))
    assert any("秒" in e for e in errs)


def test_newline_in_any_cell_is_an_error():
    errs, _ = cs.check_row(row(**{**VIOLATION, "ai_model": "m\nweb"}))
    assert any("ai_model" in e and "改行" in e for e in errs)


def _write(p, lines):
    with open(p, "w", encoding="utf-8-sig", newline="") as f:
        f.write("\r\n".join(lines) + "\r\n")


def test_main_reports_short_and_long_rows_without_crashing(tmp_path, capsys):
    header = ",".join(BASE)
    good = list(row(**VIOLATION).values())
    p = tmp_path / "s.csv"
    _write(p, [header, ",".join(good[:10])])  # 欄が足りない（区切りの , が足りない）
    assert cs.main([str(p)]) == 1
    assert "少ない" in capsys.readouterr().out
    long_row = list(good)
    long_row[list(BASE).index("evidence")] = "a.py:1, b.py:2"
    _write(p, [header, ",".join(long_row)])  # セルの中の , を " で囲んでいない
    assert cs.main([str(p)]) == 1
    assert "多い" in capsys.readouterr().out


def test_main_explains_a_bad_header(tmp_path, capsys):
    p = tmp_path / "s.csv"
    _write(p, ["練習の表", ",".join(BASE), ",".join(row(**VIOLATION).values())])
    assert cs.main([str(p)]) == 1
    assert "1 行目が見出しでない" in capsys.readouterr().out
    _write(p, [";".join(BASE), ";".join(row(**VIOLATION).values())])
    assert cs.main([str(p)]) == 1
    assert "区切りが ;" in capsys.readouterr().out
    _write(p, [",".join(BASE)])
    assert cs.main([str(p)]) == 1
    assert "件の行が無い" in capsys.readouterr().out


def test_violation_without_read_range_is_an_error():
    errs, _ = cs.check_row(row(**{**VIOLATION, "evidence": "a.py:10 → a.py:20 open(p, 'a')"}))
    assert any("読んだ範囲" in e for e in errs)


def test_guide_gap_unknown_needs_a_note():
    base = dict(outcome="不明", evidence="a.py:3／読んだ範囲: a.py:1-9",
                unknown_reason="手引きで決まらない: a.py:3 の遅延 import の一番上の書き込み")
    errs, _ = cs.check_row(row(**base))
    assert any("note" in e for e in errs)
    errs, _ = cs.check_row(row(**{**base, "note": "読めば 違反（初回）"}))
    assert errs == []
