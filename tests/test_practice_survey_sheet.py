"""`scripts/practice_survey_sheet.py`（実態調査の練習の表を名簿と抜き取りの列から作る）の試験。

木（corpus）を使わずに、コミット済みの抜き取りの列から時間を測る件の行が作り直せることと、欄の並びが配った表と同じことを
確かめる。名簿から作り直す全体の手順は `evidence/practice_survey/README.md` の「表の作り方と再現」。
"""
from __future__ import annotations

import csv
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import practice_survey_sheet as ps  # noqa: E402

SHEET = os.path.join(ROOT, "evidence", "practice_survey", "survey_practice.csv")
TARGETS = os.path.join(ROOT, "evidence", "practice_survey", "survey_practice_targets.json")


def _committed_rows() -> list[dict]:
    with open(SHEET, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def test_columns_match_the_committed_sheet():
    with open(SHEET, encoding="utf-8-sig", newline="") as fh:
        header = next(csv.reader(fh))
    assert tuple(header) == ps.COLUMNS


def test_timed_rows_come_from_the_committed_targets_in_order():
    with open(TARGETS, encoding="utf-8") as fh:
        targets = json.load(fh)
    committed = _committed_rows()
    w01 = committed[0]
    roster = {"trees": [{"tree": w01["tree"], "entries": [
        {"tool": w01["tool"], "form": w01["roster_form"], "relpath": w01["roster_relpath"],
         "def_lineno": int(w01["roster_lineno"]), "decl_lineno": int(w01["decl_lineno"])}]}]}
    rows = ps.build_rows(roster, targets, f"{w01['tree']}:{w01['tool']}", {"S-001"}, 3)
    assert len(rows) == len(committed)
    for got, want in zip(rows, committed, strict=True):
        assert {k: str(v) for k, v in got.items()} == {k: want[k] for k in got}, want["pair_id"]
    assert [r["pair_id"] for r in rows] == ["W-01", "T-01", "T-02", "T-03"]


def test_skip_and_errors(tmp_path):
    roster = {"trees": [{"tree": "t", "entries": [{"tool": "a", "form": "decorator", "relpath": "a.py", "def_lineno": 2,
                                                   "decl_lineno": 1}]}]}
    targets = {"targets": [{"pair_id": f"S-00{i}", "tree": f"x{i}", "tool": "f", "form": "decorator", "relpath": "m.py",
                            "def_lineno": 10 + i, "decl_lineno": 9 + i} for i in range(1, 5)]}
    rows = ps.build_rows(roster, targets, "t:a", {"S-002"}, 2)
    assert [r["tree"] for r in rows] == ["t", "x1", "x3"]
    out = tmp_path / "s.csv"
    ps.write_sheet(rows, str(out))
    assert out.read_bytes().startswith(b"\xef\xbb\xbf")  # BOM（Excel で開けるように）
    for bad in (lambda: ps.build_rows(roster, targets, "t:missing", set(), 1),
                lambda: ps.build_rows(roster, targets, "t:a", set(), 9)):
        try:
            bad()
        except SystemExit:
            pass
        else:
            raise AssertionError("SystemExit が出ない")
