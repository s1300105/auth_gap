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

DEFECT = pytest.mark.xfail(strict=True, reason="D32 / prereg §5 #7: 未実装（修正コミットでこの印を外す）")


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


@DEFECT
@pytest.mark.parametrize("tool", sorted(EXPECTED))
def test_destructive_attribute(units, tool):
    e = _effect(units[tool], EXPECTED[tool]["site"])
    assert getattr(e, "destructive", "missing") == EXPECTED[tool]["destructive"], e.to_json()


#: 現行の規則で既に期待どおりのもの（宣言なし / readOnly）には印を付けない。
#: 追記型を矛盾に数えている nd_mkdir / nd_append だけが未達。
_VERDICT_DEFECTS = {"nd_mkdir", "nd_append"}


@pytest.mark.parametrize(
    "tool", [pytest.param(t, marks=[DEFECT] if t in _VERDICT_DEFECTS else [], id=t) for t in sorted(EXPECTED)]
)
def test_contradiction_verdict(units, tool):
    u = units[tool]
    site = EXPECTED[tool]["site"]
    rows = [r for r in u.rows if r.effect.site == site and r.effect.kind == "FS_WRITE"]
    assert rows, f"{tool}: {site} の行が無い"
    has = any("CONTRADICTION" in r.verdicts for r in rows)
    assert has == EXPECTED[tool]["contradiction"], [(r.effect.site, sorted(r.verdicts)) for r in rows]
