"""DB 効果の受け手型の解決（O29 / D50）。

**期待値はこのテストで、`authgap/` を直す前に書いた**（CLAUDE.md 規則 5 の趣旨）。

直す前、母集団 v2 の `.execute()` の 90.0%（2,078 件）が受け手型を解決できず
DB 効果になっていなかった。抜き取り 20 件中 15 件が本物の SQL だった（D49）。原因は 3 つ:

1. **メソッド呼び出しの型遷移が効かない。** `ATTR_TYPE_TRANSITIONS` は属性アクセス
   （`_ev_Attribute`）でしか引かれず、`conn.cursor()` のような**呼び出し**では使われない。
2. **psycopg 系の CTOR が無い。** `psycopg.Cursor` は DB 型に入っているのに、それを
   作る規則（`psycopg.connect` / `psycopg_pool.ConnectionPool`）が無い。
3. **仮引数の型注釈を使わない。** `session: Session` と書いてあっても型にならない。

**これは解決率を上げる変更なので、反例を正例と同じ重さで固定する**（CLAUDE.md の
敵対的レビュー）。反例を落とすと、DB でないものを DB と数える誤警報になり、
とくに `requests.Session` を SQLAlchemy と取り違えると NET の効果を DB に付け替える。
"""

from __future__ import annotations

import pytest

from authgap.report import manifest_json
from authgap.runner import RunConfig, run

DB_PY = '''
from psycopg_pool import ConnectionPool
pool = ConnectionPool(conninfo="x", open=False)

def conn():
    return pool.connection()
'''

SRC = '''
import os
import sqlite3
import psycopg
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from neo4j import GraphDatabase
from mcp.server.fastmcp import FastMCP
from unknown_lib import get_anything
from .db import conn
mcp = FastMCP("t")

# ---- 正例: 直ったら DB 効果になるべき -------------------------------------
@mcp.tool()
async def p01_cursor_assign(q: str) -> str:
    c = sqlite3.connect("x.db"); cur = c.cursor(); cur.execute(q); return "x"

@mcp.tool()
async def p02_cursor_with(q: str) -> str:
    c = sqlite3.connect("x.db")
    with c.cursor() as cur:
        cur.execute(q)
    return "x"

@mcp.tool()
async def p03_psycopg_cursor(q: str) -> str:
    with psycopg.connect("dbname=x") as c:
        with c.cursor() as cur:
            cur.execute(q)
    return "x"

@mcp.tool()
async def p04_psycopg_conn_execute(q: str) -> str:
    with psycopg.connect("dbname=x") as c:
        c.execute(q)
    return "x"

@mcp.tool()
async def p05_pool(q: str) -> str:
    with conn() as c:
        with c.cursor() as cur:
            cur.execute(q)
    return "x"

def _repo_session(session: Session, q):
    session.execute(q)

@mcp.tool()
async def p06_annot_session(q: str) -> str:
    _repo_session(get_anything(), q); return "x"

async def _repo_async(session: AsyncSession, q):
    await session.execute(q)

@mcp.tool()
async def p07_annot_async(q: str) -> str:
    await _repo_async(get_anything(), q); return "x"

def _repo_opt(session: Optional[Session], q):
    session.execute(q)

@mcp.tool()
async def p08_annot_optional(q: str) -> str:
    _repo_opt(get_anything(), q); return "x"

def _repo_str(session: "Session", q):
    session.execute(q)

@mcp.tool()
async def p09_annot_string(q: str) -> str:
    _repo_str(get_anything(), q); return "x"

def _repo_sqlite(c: sqlite3.Connection, q):
    c.execute(q)

@mcp.tool()
async def p10_annot_sqlite(q: str) -> str:
    _repo_sqlite(get_anything(), q); return "x"

@mcp.tool()
async def p11_engine_connect(q: str) -> str:
    engine = create_engine("sqlite://")
    with engine.connect() as c:
        c.execute(q)
    return "x"

@mcp.tool()
async def p12_neo4j_session(q: str) -> str:
    driver = GraphDatabase.driver("bolt://x")
    with driver.session() as s:
        s.run(q)
    return "x"

# ---- 反例: DB にしてはいけない --------------------------------------------
def _repo_const(session: Session):
    session.execute("SELECT 1")

@mcp.tool()
async def n00_const_sql(unused: str) -> str:
    _repo_const(get_anything()); return "x"
'''

NEG_SRC = '''
import requests
import sqlalchemy.orm                 # n05 の注釈を**解決できる**ようにする（下の注記）
from requests import Session
from mcp.server.fastmcp import FastMCP
from unknown_lib import get_anything, build_service, make_redis
mcp = FastMCP("n")

def _http(s: Session, q):
    s.execute(q)                       # requests.Session は DB ではない

@mcp.tool()
async def n01_requests_session(q: str) -> str:
    _http(get_anything(), q); return "x"

class LocalSession:                    # 木内の同名に近いクラス
    def execute(self, q):
        return q

def _local(s: LocalSession, q):
    s.execute(q)

@mcp.tool()
async def n02_in_tree_class(q: str) -> str:
    _local(LocalSession(), q); return "x"

@mcp.tool()
async def n03_google_api(q: str) -> str:
    svc = build_service()
    svc.files().get(fileId=q).execute(); return "x"

@mcp.tool()
async def n04_redis(q: str) -> str:
    pipe = make_redis().pipeline()
    pipe.set(q, 1); pipe.execute(); return "x"

def _override(s: "sqlalchemy.orm.Session", q):
    s.execute(q)

@mcp.tool()
async def n05_actual_type_wins(q: str) -> str:
    _override(requests.Session(), q); return "x"   # 実引数の型が既知なら注釈で上書きしない
'''


def _run(tmp_path_factory, name, files):
    d = tmp_path_factory.mktemp(name)
    pkg = d / "pkg"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("", encoding="utf-8")
    for fn, text in files.items():
        (pkg / fn).write_text(text, encoding="utf-8")
    res = run(RunConfig(src_root=str(d), population="mcp_server", full=True))
    return {u["unit"]["qualname"]: u for u in manifest_json(res, "t")["units"]}


@pytest.fixture(scope="module")
def pos(tmp_path_factory):
    return _run(tmp_path_factory, "db_pos", {"server.py": SRC, "db.py": DB_PY})


@pytest.fixture(scope="module")
def neg(tmp_path_factory):
    return _run(tmp_path_factory, "db_neg", {"server.py": NEG_SRC})


def _db(u):
    return [e for e in u.get("effects", []) if e["kind"] == "DB"]


POSITIVE = [
    "p01_cursor_assign", "p02_cursor_with", "p03_psycopg_cursor", "p04_psycopg_conn_execute",
    "p05_pool", "p06_annot_session", "p07_annot_async", "p08_annot_optional",
    "p09_annot_string", "p10_annot_sqlite", "p11_engine_connect", "p12_neo4j_session",
]


@pytest.mark.parametrize("tool", POSITIVE)
def test_positive_becomes_db_effect(pos, tool):
    """**直す前はすべて DB 効果 0 件で `db_unresolved` に入っていた。**"""
    assert _db(pos[tool]), f"{tool}: DB 効果が出ない / 未解決={pos[tool].get('db_unresolved')}"
    assert not pos[tool].get("db_unresolved"), f"{tool}: まだ未解決に残っている"


@pytest.mark.parametrize("tool", POSITIVE)
def test_positive_keeps_the_sql_principal(pos, tool):
    """**受け手を型付けしても SQL の主体は変えない。** q はツール引数なので MODEL。"""
    for e in _db(pos[tool]):
        slot = (e.get("slots") or {}).get("sql") or (e.get("slots") or {}).get("query")
        if slot is not None:
            assert slot["prin"] == "MODEL", f"{tool}: sql の主体が {slot['prin']}"


def test_constant_sql_stays_op(pos):
    """定数 SQL は OP のまま（受け手の型付けで主体を持ち上げない）。"""
    effs = _db(pos["n00_const_sql"])
    assert effs, "定数 SQL でも DB 効果は出る"
    for e in effs:
        assert e["slots"]["sql"]["prin"] == "OP"


# ---- 反例 -------------------------------------------------------------------
@pytest.mark.parametrize("tool", ["n01_requests_session", "n02_in_tree_class", "n03_google_api",
                                  "n04_redis", "n05_actual_type_wins"])
def test_negative_does_not_become_db(neg, tool):
    """**ここを DB にすると誤警報。**

    * n01: `from requests import Session` を SQLAlchemy と取り違えない（import で解決する）
    * n02: 木内のクラスは木内の定義に降りる
    * n03 / n04: Google API / Redis の `.execute()` は DB ではない
    * n05: **実引数の型が既知なら、仮引数の注釈で上書きしない**。
      初版は `sqlalchemy` を import しておらず、注釈が**解決できないせいで**通っていた
      （試したい規則を試していなかった）。実装の前に `import sqlalchemy.orm` を足した
    """
    assert not _db(neg[tool]), f"{tool}: DB 効果が出た（誤警報）"
