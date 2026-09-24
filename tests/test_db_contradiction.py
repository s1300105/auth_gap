"""DB の書き込みを CONTRADICTION に数える（`docs/contradiction_matrix.md` D1 / D2 の DB 行）。

**期待値はこのテストで、`authgap/` を直す前に書いた**（CLAUDE.md 規則 5 の趣旨）。

表（D41）は次を**すでに決めている**:

* `readOnlyHint: true` × `DB_WRITE`（データの変更）→ **矛盾**
* `destructiveHint: false` × `DB_WRITE`（`INSERT`）→ 宣言内（追記）
* `destructiveHint: false` × `DB_WRITE`（`DELETE` / `DROP` / `UPDATE`）→ **矛盾**

ところが `dparse.contradiction()` は EXEC / SPAWN / FS_WRITE しか見ておらず、DB を
一度も矛盾に数えていなかった（**誤 clear**）。run4 では該当 0 件だったが、D50（DB の受け手型）と
D54（深さ 4）の後の run11 で readOnly × `INSERT` / `UPDATE` 12 位置、destructive=false ×
`UPDATE` / `DELETE` 35 位置が黙っていた（`docs/o23_cells.md`）。

**決めていないマスは報告しない**（O23 #1 の `PRAGMA` など、SQL が定数に解決できないもの）。
"""

from __future__ import annotations

import pytest

from authgap.report import manifest_json
from authgap.runner import RunConfig, run

SRC = '''
import sqlite3
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("t")

def db():
    return sqlite3.connect("x.db")

@mcp.tool(annotations={"readOnlyHint": True})
async def ro_insert(name: str) -> str:
    db().execute("INSERT INTO users (name) VALUES (?)", (name,)); return "x"

@mcp.tool(annotations={"readOnlyHint": True})
async def ro_update(name: str) -> str:
    db().execute("UPDATE users SET seen = 1 WHERE name = ?", (name,)); return "x"

@mcp.tool(annotations={"readOnlyHint": True})
async def ro_create(name: str) -> str:
    db().execute("CREATE TABLE IF NOT EXISTS t (a)"); return "x"

@mcp.tool(annotations={"readOnlyHint": True})
async def ro_select(name: str) -> str:
    db().execute("SELECT * FROM users WHERE name = ?", (name,)); return "x"

@mcp.tool(annotations={"readOnlyHint": True})
async def ro_multiline_select(name: str) -> str:
    db().execute("""
        SELECT *
          FROM users""")
    return "x"

@mcp.tool(annotations={"readOnlyHint": True})
async def ro_pragma(name: str) -> str:
    db().execute("PRAGMA journal_mode=WAL"); return "x"

@mcp.tool(annotations={"readOnlyHint": True})
async def ro_begin(name: str) -> str:
    db().execute("BEGIN"); return "x"

@mcp.tool(annotations={"readOnlyHint": True})
async def ro_dynamic_sql(sql: str) -> str:
    db().execute(sql); return "x"

@mcp.tool(annotations={"destructiveHint": False})
async def nd_insert(name: str) -> str:
    db().execute("INSERT INTO users (name) VALUES (?)", (name,)); return "x"

@mcp.tool(annotations={"destructiveHint": False})
async def nd_create(name: str) -> str:
    db().execute("CREATE TABLE IF NOT EXISTS t (a)"); return "x"

@mcp.tool(annotations={"destructiveHint": False})
async def nd_update(name: str) -> str:
    db().execute("UPDATE users SET seen = 1 WHERE name = ?", (name,)); return "x"

@mcp.tool(annotations={"destructiveHint": False})
async def nd_delete(name: str) -> str:
    db().execute("DELETE FROM users WHERE name = ?", (name,)); return "x"

@mcp.tool(annotations={"destructiveHint": False})
async def nd_drop(name: str) -> str:
    db().execute("DROP TABLE users"); return "x"

@mcp.tool(annotations={"destructiveHint": False})
async def nd_pragma(name: str) -> str:
    db().execute("PRAGMA foreign_keys=ON"); return "x"

@mcp.tool()
async def none_update(name: str) -> str:
    db().execute("UPDATE users SET seen = 1 WHERE name = ?", (name,)); return "x"

@mcp.tool(annotations={"readOnlyHint": False, "destructiveHint": True})
async def permissive_delete(name: str) -> str:
    db().execute("DELETE FROM users WHERE name = ?", (name,)); return "x"
'''


@pytest.fixture(scope="module")
def units(tmp_path_factory):
    d = tmp_path_factory.mktemp("db_contradiction")
    (d / "server.py").write_text(SRC, encoding="utf-8")
    res = run(RunConfig(src_root=str(d), population="mcp_server", full=True))
    return {u["unit"]["qualname"]: u for u in manifest_json(res, "t")["units"]}


def _db_rows(u):
    return [r for r in u["rows"] if r["kind"] == "DB"]


@pytest.mark.parametrize(
    "tool,want",
    [
        # readOnly: データ・スキーマを変える文はすべて矛盾
        ("ro_insert", True),
        ("ro_update", True),
        ("ro_create", True),
        # 読み取り
        ("ro_select", False),
        ("ro_multiline_select", False),
        # O23 #1（接続・トランザクション）は決めていないので報告しない
        ("ro_pragma", False),
        ("ro_begin", False),
        # SQL が定数に解決できない = 不明。矛盾に倒さない（規則 4）
        ("ro_dynamic_sql", False),
        # destructive=false: 追記（INSERT / CREATE）は宣言内
        ("nd_insert", False),
        ("nd_create", False),
        ("nd_update", True),
        ("nd_delete", True),
        ("nd_drop", True),
        ("nd_pragma", False),
        # 宣言が無い / 許容側の宣言は矛盾にならない
        ("none_update", False),
        ("permissive_delete", False),
    ],
)
def test_db_contradiction(units, tool, want):
    u = units[tool]
    rows = _db_rows(u)
    assert rows, f"{tool}: DB 効果の行が無い（前提が崩れている）"
    got = any("CONTRADICTION" in r["verdicts"] for r in rows)
    assert got is want


def test_sql_head_is_recorded(units):
    heads = {e.get("sql_head") for e in units["ro_update"]["effects"] if e["kind"] == "DB"}
    assert heads == {"UPDATE"}
    dyn = [e for e in units["ro_dynamic_sql"]["effects"] if e["kind"] == "DB"]
    assert dyn and all(e.get("sql_head") is None for e in dyn)
