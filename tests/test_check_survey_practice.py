"""`scripts/check_survey_practice.py`（実態調査の練習の表の書き方の確かめ）の試験。入力は全部合成。

D90: 判定者が書くのは `outcome` と `evidence` だけ。D91・D92: `evidence` は反する（決められない）行までの道筋で、違反でない は空。
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


# D91 の改訂: 本体は書かず、本体が呼んだ先から書く
V = 'a.py:34 helper → a.py:29 save → a.py:30: open(p, "a") に追記'
U = "a.py:20 Client.sync → httpx.Client.post（外）: POST /items/sync"


def test_good_rows_for_each_outcome():
    # D91: 関数は「ファイル:行 名前」、木の外は「名前（外）」、本体は書かず呼んだ先から。D92: 違反でない は空
    assert cs.check_row(row("違反", V)) == []
    assert cs.check_row(row("違反", "requests.post（外）: 相手に注文を作る")) == []  # 本体が木の外の関数を呼んで反する
    assert cs.check_row(row("違反", "a.py:47: open(p, 'a') に追記")) == []  # 本体の中の行が反する
    assert cs.check_row(row("違反（深さ 4 の外）", V)) == []
    assert cs.check_row(row("不明", U)) == []
    assert cs.check_row(row("不明", "client.sync_items（外）")) == []
    assert cs.check_row(row("違反", "client.create_order（外）: 注文を作る／API 名から")) == []
    assert cs.check_row(row("違反でない", "")) == []
    assert cs.check_row(row("対象外", "a.py:12 の辞書は設定の見本で、どのサーバにも登録されない")) == []


def test_outcome_must_be_one_of_the_values():
    for bad in ("違反(深さ4の外)", "違反なし", "OK"):
        assert any("どれでもない" in e for e in cs.check_row(row(bad, "")))


def test_evidence_is_required_except_not_violation():
    for out in ("違反", "違反（深さ 4 の外）", "不明", "対象外"):
        assert any("evidence が空" in e for e in cs.check_row(row(out, ""))), out


def test_unknown_evidence_is_a_path():
    for bad in ("よく分からない", "Client.sync → post（外）", "読んだ範囲: a.py:1-9"):
        assert any("決められなかった呼び出し" in e for e in cs.check_row(row("不明", bad))), bad


def test_violation_evidence_is_one_path_ending_with_the_line_and_what_it_does():
    for out in ("違反", "違反（深さ 4 の外）"):
        for bad in ("open で書いているので違反", "a.py:34 helper → a.py:29 save", "helper → save → a.py:30: open"):
            assert any("反する行までの道筋" in e for e in cs.check_row(row(out, bad))), (out, bad)


def test_newline_and_formula_prefix_are_errors():
    assert any("改行" in e for e in cs.check_row(row("違反", V.replace(" → a.py:30", "\n→ a.py:30"))))
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
    rows[0].update(outcome="違反でない", evidence="", note="", minutes="", t_start="")
    p = tmp_path / "old.csv"
    _write(p, cols, rows)
    assert cs.main([str(p)]) == 0
    assert "W-01: よい" in capsys.readouterr().out


def test_forbidden_and_missing_columns(tmp_path):
    p = tmp_path / "s.csv"
    _write(p, ["pair_id", "outcome", "evidence", "cause"], [row("違反でない", "")])
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
    text[1] = text[1] + ",違反でない,,extra"
    p.write_text("\n".join(text) + "\n", encoding="utf-8-sig")
    assert cs.main([str(p)]) == 1
    assert "欄の数が見出しより多い" in capsys.readouterr().out
