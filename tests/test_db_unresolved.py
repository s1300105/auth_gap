"""受け手型を解決できない `.execute()` を記録する（O28 / D49）。

**期待値はこのテストで、`authgap/` を直す前に書いた**（CLAUDE.md 規則 5 の趣旨）。

仕様書 1118 行目:

> 受け手が Def 3 の proxy カタログの DB 受け手型に**局所代入で解決できる**場合のみ
> DB 効果とする。解決できない `.execute()` は **`db_unresolved` として記録し**、
> **危険効果に数えない**（`effect_fp_audit.db_only_non_db_execute` の分子）。

**「数えない」と「記録する」は別の要求である。** 直す前は前者だけが（しかも
`effects.py` の `if db_rule != "db": return None` ではなく proxy 行の受け手型一致に
よって偶然）満たされ、後者は**どこにも実装されていなかった**。
`.execute()` が 1 つも痕跡を残さずに消えるのは CLAUDE.md 規則 4 に反する。
"""

from __future__ import annotations

import pytest

from authgap.report import manifest_json
from authgap.runner import RunConfig, run

SRC = '''
import sqlite3
from mcp.server.fastmcp import FastMCP
from unknown_orm import get_conn
mcp = FastMCP("t")

@mcp.tool()
async def resolvable(q: str) -> str:
    conn = sqlite3.connect("x.db")
    conn.execute(q)
    return "x"

@mcp.tool()
async def unresolvable(q: str) -> str:
    conn = get_conn()
    conn.execute(q)
    return "x"

@mcp.tool()
async def unresolvable_executemany(q: str) -> str:
    conn = get_conn()
    conn.executemany(q, [])
    return "x"

@mcp.tool()
async def not_a_db_method(q: str) -> str:
    conn = get_conn()
    conn.fetchall()
    return "x"

@mcp.tool()
async def plain_function_call(q: str) -> str:
    execute(q)
    return "x"
'''


@pytest.fixture(scope="module")
def units(tmp_path_factory):
    d = tmp_path_factory.mktemp("db_unresolved")
    (d / "server.py").write_text(SRC, encoding="utf-8")
    res = run(RunConfig(src_root=str(d), population="mcp_server", full=True))
    return {u["unit"]["qualname"]: u for u in manifest_json(res, "t")["units"]}


@pytest.mark.parametrize("tool,method", [
    ("unresolvable", "execute"),
    ("unresolvable_executemany", "executemany"),
])
def test_unresolvable_execute_is_recorded(units, tool, method):
    """**直す前はここが空で、`.execute()` が痕跡なく消えていた。**"""
    rec = units[tool].get("db_unresolved") or []
    assert len(rec) == 1, f"{tool}: {rec}"
    assert rec[0]["method"] == method


@pytest.mark.parametrize("tool", ["unresolvable", "unresolvable_executemany"])
def test_unresolvable_execute_is_not_a_dangerous_effect(units, tool):
    """**記録はするが効果には数えない**（仕様の後半）。"""
    assert [e for e in units[tool].get("effects", []) if e["kind"] == "DB"] == []


def test_resolvable_execute_is_a_db_effect_and_not_recorded(units):
    """解決できた `.execute()` は DB 効果になり、`db_unresolved` には入らない。"""
    u = units["resolvable"]
    assert [e["kind"] for e in u.get("effects", [])] == ["DB"]
    assert u.get("effects")[0].get("db_rule") == "db"
    assert not u.get("db_unresolved")


@pytest.mark.parametrize("tool", ["not_a_db_method", "plain_function_call"])
def test_other_calls_are_not_recorded(units, tool):
    """**`.execute()` 以外を数えない。** 数えると FP 監査の分子が膨らむ。"""
    assert not units[tool].get("db_unresolved")


def test_recording_does_not_create_a_verdict(units):
    """記録は manifest の属性であって verdict ではない。"""
    for tool in ("unresolvable", "unresolvable_executemany"):
        assert units[tool].get("rows", []) == []
