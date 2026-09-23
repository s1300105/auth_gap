"""§3 の交差行の**除外規則**（D46）。

**閾値だけでなく除外規則もテストで固定する。** D46 で、`scripts/intersection_rows.py` の
docstring には「`OPAQUE` 行は数えない」と書いてあるのに実装していない、という食い違いが
見つかった。**書いた規則と実装した規則が違い、しかも向きが主張に有利だった**ため、
あやうく事前登録した判断（D36）を巻き戻すところだった。

仕様書 §3（`AUTHGAP_BRIEF_v3.md` 553 行目）:

> `Leak`（Def 5-b）だけで説明できる行と `OPAQUE` 行は数えない。D だけで説明できる行も除く。
"""

from __future__ import annotations

import json
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from intersection_rows import MIN_PROJECTS, MIN_ROWS, TRACED_GATE, scan  # noqa: E402


def _tree(tmp_path, name, rows):
    """1 ユニット・1 木の最小 manifest を書く。"""
    man = {
        "units": [{
            "unit": {"unit_id": "u1", "qualname": "tool_a"},
            "trig": {"mode": "traced"},
            "rows": [{"site": "s", "slot": f"p{i}", "verdicts": v} for i, v in enumerate(rows)],
        }]
    }
    with open(os.path.join(tmp_path, f"{name}.json"), "w", encoding="utf-8") as fh:
        json.dump(man, fh)


def test_opaque_rows_are_excluded(tmp_path):
    """**SELECT 系と INJECT 系を両方持っても、`UNKNOWN` があれば数えない。**

    D46 以前はここが通らず、`UNKNOWN` 付きの行まで交差行に数えていた。
    **除外を落とすと、解析器が未解決を正直に報告するほど交差行が増える。**
    """
    _tree(tmp_path, "t1", [["GAP_SELECT", "GAP_INJECT", "UNKNOWN"]])
    res = scan(str(tmp_path))
    assert res["n_intersection_rows"] == 0
    assert res["n_excluded_opaque"] == 1


def test_clean_intersection_row_is_counted(tmp_path):
    """`UNKNOWN` が無ければ数える。"""
    _tree(tmp_path, "t1", [["GAP_SELECT", "GAP_INJECT"]])
    res = scan(str(tmp_path))
    assert res["n_intersection_rows"] == 1
    assert res["n_excluded_opaque"] == 0


def test_d_only_rows_are_excluded(tmp_path):
    """D だけで説明できる行（`INVENTORY` / `CONTRADICTION` / `GAP_DRIFT` のみ）は除く。"""
    _tree(tmp_path, "t1", [["INVENTORY", "GAP_DRIFT"]])
    res = scan(str(tmp_path))
    assert res["n_intersection_rows"] == 0
    assert res["n_excluded_d_only"] == 1


@pytest.mark.parametrize("verdicts", [
    ["GAP_SELECT"],            # SELECT だけ
    ["GAP_INJECT"],            # INJECT だけ
    ["CONTRADICTION"],         # D だけ
    ["UNKNOWN"],               # OPAQUE だけ
])
def test_single_coordinate_rows_are_not_intersection_rows(tmp_path, verdicts):
    _tree(tmp_path, "t1", [verdicts])
    assert scan(str(tmp_path))["n_intersection_rows"] == 0


def test_thresholds_are_the_preregistered_ones():
    """**閾値を動かさない。** §3 は「3 行以上、3 プロジェクト以上」「traced 20%」。"""
    assert (MIN_ROWS, MIN_PROJECTS, TRACED_GATE) == (3, 3, 0.20)


def test_projects_are_counted_by_tree(tmp_path):
    """由来プロジェクト数は木ごとに数える。"""
    _tree(tmp_path, "t1", [["GAP_SELECT", "GAP_INJECT"]])
    _tree(tmp_path, "t2", [["GAP_SELECT", "GAP_INJECT"]])
    res = scan(str(tmp_path))
    assert (res["n_intersection_rows"], res["n_projects"]) == (2, 2)
    assert res["pass_rows"] is False and res["pass_projects"] is False
