"""低レベル MCP ハンドラと `Tool(...)` 宣言の join（`docs/preregistration.md` §2.9、O5）。

**期待値 `fixtures/dispatch_join/expected.json` は規則から書き、実装より先にコミットした**
（CLAUDE.md 規則 5）。実装で XPASS になったら印を外す。

規則の要点:
* (a) `L.name ∈ u.dispatch_names` で join。名前が非リテラルのリテラルは join しない（件数）。
* (b) 効果は、それを支配する `name == "<t>"` 判定のツールに帰属。どの判定にも支配されない
  効果は join した全ツールに帰属。
* (c) 複数帰属は**最も厳しい宣言**で判定（false-dirty 側。false-clean には倒さない）。
"""

from __future__ import annotations

import json
import os

import pytest

from authgap.runner import RunConfig, run

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURE = os.path.join(ROOT, "fixtures", "dispatch_join")
EXPECTED = json.load(open(os.path.join(FIXTURE, "expected.json"), encoding="utf-8"))["units"]

DEFECT = pytest.mark.xfail(strict=True, reason="prereg §2.9（O5）: 未実装（修正コミットでこの印を外す）")


@pytest.fixture(scope="module")
def units():
    res = run(RunConfig(src_root=FIXTURE, population="mcp_server", full=True))
    return {u.unit.qualname.split(".")[-1]: u for u in res.tree.units}


def _rows_for(u, site: str, kind: str):
    return [r for r in u.rows if r.effect.site == site and r.effect.kind == kind]


# --------------------------------------------------------------------------
# 前提（印なし）: fixture が解析器の当該経路に届いている
# --------------------------------------------------------------------------


def test_precondition_units_exist(units):
    assert "call_tool" in units, sorted(units)
    assert "deco_read" in units, sorted(units)
    assert units["call_tool"].unit.entry_kind.startswith("lowlevel")


def test_precondition_effects_exist(units):
    u = units["call_tool"]
    kinds = sorted((e.site, e.kind) for e in u.effects)
    assert ("os.makedirs", "FS_WRITE") in kinds, kinds
    assert ("builtins.open", "FS_READ") in kinds, kinds
    assert ("builtins.open", "FS_WRITE") in kinds, kinds


def test_precondition_dispatch_names_seen(units):
    names = set(units["call_tool"].unit.dispatch_names)
    assert {"read_note", "write_note"} <= names, names


def test_decorator_form_unchanged(units):
    """(iv) FastMCP デコレータ形は既存経路。**修正で動いてはいけない。**"""
    u = units["deco_read"]
    exp = EXPECTED["deco_read"]
    assert u.d_kind.to_json().get("explicit") == exp["d_kind"]["explicit"]
    assert u.d_kind.to_json().get("upper") == exp["d_kind"]["upper"]
    rows = _rows_for(u, "builtins.open", "FS_READ")
    # trig が assumed の FastMCP 形では SELECT 行は manifest 行で、D の存在は notes に出る（既存挙動）。
    assert rows, "deco_read の FS_READ 行が無い"
    for n in exp["effects"][0]["notes_include"]:
        assert any(n in r.notes for r in rows), [(r.verdicts, r.notes) for r in rows]


# --------------------------------------------------------------------------
# (a) join と未 join の件数
# --------------------------------------------------------------------------


@DEFECT
def test_join_by_dispatch_names(units):
    u = units["call_tool"]
    dj = u.to_json().get("dispatch_join")
    assert dj is not None, "manifest に dispatch_join が無い"
    assert sorted(dj["tools"]) == EXPECTED["call_tool"]["dispatch_join"]["tools"], dj
    assert dj["unjoined_literals"] == EXPECTED["call_tool"]["dispatch_join"]["unjoined_literals"], dj


@DEFECT
def test_d_kind_by_tool(units):
    u = units["call_tool"]
    got = u.to_json().get("D_kind_by_tool")
    assert got is not None, "manifest に D_kind_by_tool が無い"
    exp = EXPECTED["call_tool"]["d_kind_by_tool"]
    assert got["read_note"]["explicit"] == exp["read_note"]["explicit"], got
    assert got["read_note"]["upper"] == exp["read_note"]["upper"], got
    assert got["write_note"]["bottom"] is True, got
    assert got["write_note"]["present_no_bound"] == exp["write_note"]["present_no_bound"], got


# --------------------------------------------------------------------------
# (b)(c) 効果の帰属と判定
# --------------------------------------------------------------------------


@DEFECT
@pytest.mark.parametrize("site,kind", [("os.makedirs", "FS_WRITE"), ("builtins.open", "FS_READ"), ("builtins.open", "FS_WRITE")])
def test_effect_attribution_and_verdicts(units, site, kind):
    u = units["call_tool"]
    exp = next(e for e in EXPECTED["call_tool"]["effects"] if e["site"] == site and e["kind"] == kind)
    rows = _rows_for(u, site, kind)
    assert rows, f"{site}/{kind} の行が無い"
    dj = u.to_json().get("dispatch_join") or {}
    idx = [i for i, e in enumerate(u.effects) if e.site == site and e.kind == kind][0]
    attributed = dj.get("attribution", {}).get(str(idx))
    assert attributed is not None and sorted(attributed) == exp["attributed"], (idx, dj.get("attribution"))
    verdicts = set().union(*(r.verdicts for r in rows))
    for v in exp.get("verdicts_include", []):
        assert v in verdicts, (site, kind, sorted(verdicts))
    for v in exp.get("verdicts_exclude", []):
        assert v not in verdicts, (site, kind, sorted(verdicts))
    if "covered_by" in exp:
        assert any(r.covered_by == exp["covered_by"] for r in rows), [(r.verdicts, r.covered_by) for r in rows]
