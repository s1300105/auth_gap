"""`scripts/check_survey_practice.py`（実態調査の練習の表の書き方の確かめ）の試験。入力は全部合成。

D90: 判定者が書くのは `outcome` と `evidence` だけ。
"""

from __future__ import annotations

import csv
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import check_survey_practice as cs  # noqa: E402

SHEET = os.path.join(ROOT, "evidence", "practice_survey", "survey_practice.csv")


def row(outcome: str, evidence: str) -> dict:
    return {"pair_id": "X-01", "outcome": outcome, "evidence": evidence}


def _write(path, cols, rows):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def _sheet():
    with open(SHEET, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames), list(reader)


def test_good_rows_for_each_outcome():
    assert cs.check_row(row("違反", "a.py:48 f → :38 g: open(p, 'a') に追記")) == []
    assert cs.check_row(row("違反（深さ 4 の外）", "a.py:10 → c.py:90 open(p, 'w')／読んだ範囲: a.py:1-30")) == []
    assert cs.check_row(row("違反でない", "読んだ範囲: a.py:52-55、:19-21")) == []
    assert cs.check_row(row("違反でない", "読んだ範囲: a.py:1-9／https://example.com/api")) == []
    assert cs.check_row(row("不明", "読んだ範囲: a.py:31-41")) == []
    assert cs.check_row(row("対象外", "a.py:12 の辞書は設定の見本で、どのサーバにも登録されない")) == []


def test_outcome_must_be_one_of_the_values():
    for bad in ("違反(深さ4の外)", "違反なし", "OK"):
        assert any("どれでもない" in e for e in cs.check_row(row(bad, "読んだ範囲: a.py:1-9")))


def test_evidence_is_required():
    assert any("evidence が空" in e for e in cs.check_row(row("違反でない", "")))


def test_not_violation_evidence_starts_with_read_range():
    for out in ("違反でない", "不明"):
        assert any("始まっていない" in e for e in cs.check_row(row(out, "特に無い。読んだ範囲 なし")))


def test_violation_evidence_is_the_path_with_file_lines():
    assert any("ファイル:行" in e for e in cs.check_row(row("違反", "open で書いているので違反")))


def test_outside_depth4_needs_path_and_read_range():
    out = "違反（深さ 4 の外）"
    assert any("読んだ範囲" in e for e in cs.check_row(row(out, "a.py:10 → c.py:90 open(p, 'w')")))
    # 読んだ範囲だけで道筋が無い行は、読んだ範囲の a.py:1-30 があっても誤り
    assert any("道筋" in e for e in cs.check_row(row(out, "読んだ範囲: a.py:1-30、b.py:5-20")))


def test_newline_and_formula_prefix_are_errors():
    assert any("改行" in e for e in cs.check_row(row("違反", "a.py:1\na.py:2 open")))
    assert any("式" in e for e in cs.check_row(row("対象外", "=登録されない")))


def test_distributed_sheet_has_only_roster_outcome_evidence_and_is_unjudged(capsys):
    cols, rows = _sheet()
    assert cols == ["seq", "pair_id", "tree", "tool", "roster_form", "roster_relpath", "roster_lineno", "decl_lineno", "decl",
                    "outcome", "evidence"]
    assert [r["pair_id"] for r in rows] == ["W-01", "T-01", "T-02", "T-03"]
    assert cs.main([SHEET]) == 0
    out = capsys.readouterr().out
    assert "まだ判定していない" in out and "誤りなし" in out
    assert cs.main([SHEET, "--all"]) == 1


def test_old_sheet_with_extra_columns_is_still_read(tmp_path, capsys):
    # D90 の前に写した表（時間・ラベル・メモの欄つき）も読み、その欄は見ない
    cols, rows = _sheet()
    cols = cols + ["note", "minutes", "t_start"]
    rows[0].update(outcome="違反でない", evidence="読んだ範囲: app.py:1-9", note="", minutes="", t_start="")
    p = tmp_path / "old.csv"
    _write(p, cols, rows)
    assert cs.main([str(p)]) == 0
    assert "W-01: よい" in capsys.readouterr().out


def test_forbidden_and_missing_columns(tmp_path):
    p = tmp_path / "s.csv"
    _write(p, ["pair_id", "outcome", "evidence", "cause"], [row("違反でない", "読んだ範囲: a.py:1-9")])
    assert cs.main([str(p)]) == 1
    _write(p, ["pair_id", "outcome"], [{"pair_id": "X-01", "outcome": "違反でない"}])
    assert cs.main([str(p)]) == 1


def test_roster_columns_must_match_the_distributed_sheet(tmp_path, capsys):
    cols, rows = _sheet()
    rows[0]["roster_lineno"] = str(int(rows[0]["roster_lineno"]) + 1)  # 判定の前の行でも誤り
    rows.append({**{c: "" for c in cols}, "seq": "9", "pair_id": "EX-1", "tree": "ex-notes"})  # 配った表に無い件は確かめない
    p = tmp_path / "s.csv"
    _write(p, cols, rows)
    assert cs.main([str(p)]) == 1
    out = capsys.readouterr().out
    assert "roster_lineno" in out and out.count("配った表（evidence") == 1 and "EX-1: まだ判定していない" in out


def test_shifted_columns_are_reported_once(tmp_path, capsys):
    cols, rows = _sheet()
    p = tmp_path / "s.csv"
    _write(p, cols, rows)
    text = p.read_text(encoding="utf-8-sig").splitlines()
    text[1] = text[1] + ",違反でない,読んだ範囲: a.py:1-9,extra"
    p.write_text("\n".join(text) + "\n", encoding="utf-8-sig")
    assert cs.main([str(p)]) == 1
    assert "欄の数が見出しより多い" in capsys.readouterr().out
