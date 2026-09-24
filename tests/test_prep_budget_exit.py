"""前処理の後で tree budget を確かめる（`RunConfig.prep_budget_exit`）。

**期待値はこのテストで、`authgap/runner.py` を直す前に書いた**（CLAUDE.md 規則 5 の趣旨）。

`meta-skill-evloving` は前処理（索引 225 秒 + ユニット発見 60 秒）だけで tree budget の
180 秒を超え、**716 ユニットを 1 つも解析しないまま**残りの前処理（ツール定義の照合 25 秒 +
trig 索引 126 秒 ほか）に時間を使っていた。budget の判定がユニットの間にしか無いためである。

守ること:

1. **打ち切ったユニットの数は変えない**（分母に効く。`budget_skipped` は同じ値）。
2. **省いた前処理の値は 0 ではなく「無い」と記録する。** dispatch の位置や `d_op` を
   空で出すだけだと「dispatch が 0 件の木」と区別できないので、
   `TRUNCATED(tree_budget_prep)` を truncations に残す（CLAUDE.md 規則 4）。
3. **既定は無効。** F0a（`scripts/f0a.py`）は木全体の値（ツール定義の数・dispatch）を
   数えるので、既定で省くと事前登録した測定が変わる。
4. **budget 内の木では何も変えない**（manifest が一致する）。
"""

from __future__ import annotations

import json

import pytest

from authgap.report import manifest_json
from authgap.runner import RunConfig, run

SRC = '''
import os
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("t")

TOOLS = {"a": None}

def dispatch(name, arg):
    return TOOLS[name](arg)

@mcp.tool(annotations={"readOnlyHint": True})
async def one(p: str) -> str:
    os.makedirs(p); return "x"

@mcp.tool()
async def two(p: str) -> str:
    os.system(p); return "x"
'''


@pytest.fixture(scope="module")
def tree(tmp_path_factory):
    d = tmp_path_factory.mktemp("prep_budget")
    (d / "server.py").write_text(SRC, encoding="utf-8")
    return str(d)


def _run(tree, **kw):
    return run(RunConfig(src_root=tree, population="mcp_server", full=True, **kw))


def _strip(man: dict) -> str:
    man = dict(man)
    man.pop("run_meta", None)
    return json.dumps(man, sort_keys=True)


def test_budget_exceeded_in_prep_keeps_skip_count(tree):
    old = _run(tree, max_tree_seconds=1e-9)
    new = _run(tree, max_tree_seconds=1e-9, prep_budget_exit=True)
    assert old.tree_budget_skipped == 2
    assert new.tree_budget_skipped == old.tree_budget_skipped
    assert new.tree.units == [] and old.tree.units == []


def test_skipped_prep_is_recorded_not_zero(tree):
    new = _run(tree, max_tree_seconds=1e-9, prep_budget_exit=True)
    man = manifest_json(new, "t")
    caps = [t.get("cap") for t in man["truncations"]]
    assert "tree_budget_prep" in caps
    # 省いた値は「無い」（None）であって 0 件ではない
    assert new.tree.trig_index is None
    assert new.tree.d_op is None


def test_default_is_off(tree):
    res = _run(tree, max_tree_seconds=1e-9)
    assert res.tree.trig_index is not None
    caps = [t.get("cap") for t in manifest_json(res, "t")["truncations"]]
    assert "tree_budget_prep" not in caps


def test_within_budget_identical(tree):
    a = manifest_json(_run(tree, max_tree_seconds=600.0), "t")
    b = manifest_json(_run(tree, max_tree_seconds=600.0, prep_budget_exit=True), "t")
    assert len(a["units"]) == 2
    assert _strip(a) == _strip(b)
