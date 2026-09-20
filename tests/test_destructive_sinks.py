"""CONTRADICTION の規則（D32、prereg §5 #7）: `destructiveHint==false` には削除・上書き型だけ。

**期待値 `fixtures/destructive_sinks/expected.json` は規則から書き、実装より先にコミットした。**
"""

from __future__ import annotations

import json
import os

import pytest

from authgap.runner import RunConfig, run

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURE = os.path.join(ROOT, "fixtures", "destructive_sinks")
EXPECTED = json.load(open(os.path.join(FIXTURE, "expected.json"), encoding="utf-8"))["tools"]

#: 564c81d で xfail(strict) の DEFECT として置き、実装で 10 件すべてが XPASS になったので印を外した。


@pytest.fixture(scope="module")
def units():
    res = run(RunConfig(src_root=FIXTURE, population="mcp_server", full=True))
    return {u.unit.tool_name: u for u in res.tree.units}


def _effect(u, site):
    es = [e for e in u.effects if e.site == site and e.kind == "FS_WRITE"]
    assert es, f"{u.unit.tool_name}: {site} の FS_WRITE 効果が無い: {[(e.site, e.kind) for e in u.effects]}"
    return es[0]


@pytest.mark.parametrize("tool", sorted(EXPECTED))
def test_precondition_effect_exists(units, tool):
    assert tool in units, sorted(units)
    _effect(units[tool], EXPECTED[tool]["site"])


@pytest.mark.parametrize("tool", sorted(EXPECTED))
def test_destructive_attribute(units, tool):
    e = _effect(units[tool], EXPECTED[tool]["site"])
    assert getattr(e, "destructive", "missing") == EXPECTED[tool]["destructive"], e.to_json()


@pytest.mark.parametrize(
    "tool", [pytest.param(t, id=t) for t in sorted(EXPECTED)]
)
def test_contradiction_verdict(units, tool):
    u = units[tool]
    site = EXPECTED[tool]["site"]
    rows = [r for r in u.rows if r.effect.site == site and r.effect.kind == "FS_WRITE"]
    assert rows, f"{tool}: {site} の行が無い"
    has = any("CONTRADICTION" in r.verdicts for r in rows)
    assert has == EXPECTED[tool]["contradiction"], [(r.effect.site, sorted(r.verdicts)) for r in rows]


#: 混在ユニット（rmtree + makedirs）: 行ごとの判定。ebac5cb で xfail として置き、実装で XPASS になったので印を外した。
def test_mixed_unit_rows_are_judged_per_effect(units):
    u = units["nd_mixed"]
    exp = EXPECTED["nd_mixed"]
    for spec in [exp] + exp["other_rows"]:
        rows = [r for r in u.rows if r.effect.site == spec["site"] and r.effect.kind == "FS_WRITE"]
        assert rows, spec["site"]
        has = any("CONTRADICTION" in r.verdicts for r in rows)
        assert has == spec["contradiction"], (spec["site"], [(r.effect.site, sorted(r.verdicts)) for r in rows])
