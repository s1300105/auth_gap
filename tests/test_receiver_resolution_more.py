"""受け手の型の解決（その 2）: 構築式への直接呼び出し / `@contextmanager` / 戻り値の注釈（O29 / D51）。

**期待値はこのテストで、`authgap/` を直す前に書いた**（CLAUDE.md 規則 5 の趣旨）。

D50 の後も母集団 v2 の `.execute()` の 26.2%（一意 205 か所、抜き取りで 7 割が本物の SQL）が
受け手型を解決できていなかった。最小再現で原因が 3 つ見つかった。

1. **`Cls(...).method(...)` がメソッドに降りない。** `_resolve_in_tree` が
   `dotted_of(node.func)` が `None` なら即座に諦めるので、受け手が呼び出し式だと、
   **受け手の型が分かっていても**降りない。`s = Cls(...); s.method(...)` なら降りる。
   **同じプログラムの書き方の違いで結果が変わる。**しかも kind に依らず、
   `Store("x").run(q)` の中の `os.system(q)` まで落ちる（**DB に限らない誤 clear**）。
2. **`@contextmanager` の `yield` を戻り値にしない。** `_ev_Yield` が無く、
   `yield` は `dynamic` として扱われ、**yield される式そのものが評価されない**。
3. **戻り値の型注釈を使わない**（`def db() -> sqlite3.Connection:`）。

**解決率を上げる変更なので、反例を正例と同じ重さで固定する。**
"""

from __future__ import annotations

import pytest

from authgap.report import manifest_json
from authgap.runner import RunConfig, run

SRC = '''
import os
import sqlite3
import requests
from contextlib import contextmanager, asynccontextmanager
from mcp.server.fastmcp import FastMCP
from unknown_lib import mystery
mcp = FastMCP("t")

class Store:
    def __init__(self, p):
        self.conn = sqlite3.connect(p)
    def via_attr(self, q):
        self.conn.execute(q)
    def via_system(self, q):
        os.system(q)

class Other:                      # 同名メソッドを持つ別クラス（取り違えてはいけない）
    def via_system(self, q):
        return q

@contextmanager
def ctx_conn(p):
    conn = sqlite3.connect(p)
    try:
        yield conn
    finally:
        conn.close()

@asynccontextmanager
async def actx_conn(p):
    conn = sqlite3.connect(p)
    yield conn

@contextmanager
def ctx_http():
    yield requests.Session()

def gen_plain(p):                 # contextmanager ではない普通のジェネレータ
    yield sqlite3.connect(p)

def ret_annot() -> sqlite3.Connection:
    return mystery()

def ret_annot_http() -> requests.Session:
    return mystery()

def ret_annot_but_known() -> sqlite3.Connection:
    return requests.Session()     # 注釈と違う既知の型を返す

def yield_sink(q):
    yield os.system(q)            # yield される式の中の sink

# ---- 1. 構築式への直接呼び出し ----
@mcp.tool()
async def p1_chain_db(q: str) -> str:
    Store("x").via_attr(q); return "x"

@mcp.tool()
async def p1_chain_system(q: str) -> str:
    Store("x").via_system(q); return "x"

@mcp.tool()
async def n1_other_class(q: str) -> str:
    Other().via_system(q); return "x"         # Store.via_system に降りてはいけない

@mcp.tool()
async def n1_untyped_receiver(q: str) -> str:
    mystery().via_system(q); return "x"        # 型の分からない受け手は従来どおり降りない

# ---- 2. @contextmanager ----
@mcp.tool()
async def p2_ctx(q: str) -> str:
    with ctx_conn("x") as c:
        c.execute(q)
    return "x"

@mcp.tool()
async def p2_actx(q: str) -> str:
    async with actx_conn("x") as c:
        c.execute(q)
    return "x"

@mcp.tool()
async def p2_yield_sink(q: str) -> str:
    for _ in yield_sink(q):
        pass
    return "x"

@mcp.tool()
async def n2_ctx_http(q: str) -> str:
    with ctx_http() as s:
        s.execute(q)                           # requests.Session は DB ではない
    return "x"

# ---- 3. 戻り値の注釈 ----
@mcp.tool()
async def p3_ret_annot(q: str) -> str:
    ret_annot().execute(q); return "x"

@mcp.tool()
async def n3_ret_annot_http(q: str) -> str:
    ret_annot_http().execute(q); return "x"    # DB 型でない注釈は使わない

@mcp.tool()
async def n3_ret_annot_but_known(q: str) -> str:
    ret_annot_but_known().execute(q); return "x"   # 既知の型を注釈で上書きしない
'''


@pytest.fixture(scope="module")
def units(tmp_path_factory):
    d = tmp_path_factory.mktemp("recv_more")
    (d / "server.py").write_text(SRC, encoding="utf-8")
    res = run(RunConfig(src_root=str(d), population="mcp_server", full=True))
    return {u["unit"]["qualname"]: u for u in manifest_json(res, "t")["units"]}


def _kinds(u):
    return sorted({e["kind"] for e in u.get("effects", [])})


# ---- 正例 ----
@pytest.mark.parametrize("tool", ["p1_chain_db", "p2_ctx", "p2_actx", "p3_ret_annot"])
def test_positive_db(units, tool):
    """**直す前は DB 効果 0 件だった。**"""
    assert "DB" in _kinds(units[tool]), f"{tool}: {_kinds(units[tool])} / 未解決={units[tool].get('db_unresolved')}"


def test_chain_reaches_non_db_sink(units):
    """**DB に限らない。** `Store("x").via_system(q)` の中の `os.system(q)` を落とさない。"""
    u = units["p1_chain_system"]
    assert "SPAWN" in _kinds(u) or "EXEC" in _kinds(u), f"os.system が落ちた: {_kinds(u)}"
    for e in u["effects"]:
        if e["site"] == "os.system":
            assert e["slots"]["shell_string"]["prin"] == "MODEL"


def test_yielded_expression_is_evaluated(units):
    """`yield os.system(q)` の中の sink を評価する（直す前は yield の式そのものを評価していなかった）。"""
    assert any(e["site"] == "os.system" for e in units["p2_yield_sink"].get("effects", []))


# ---- 反例 ----
def test_negative_other_class(units):
    """**同名メソッドを持つ別クラスに降りない。** `Other().via_system` は `Store.via_system` ではない。"""
    assert not any(e["site"] == "os.system" for e in units["n1_other_class"].get("effects", []))


def test_negative_untyped_receiver_unchanged(units):
    """型の分からない受け手（`mystery().m()`）は従来どおり降りない（この変更の範囲外）。"""
    assert not any(e["site"] == "os.system" for e in units["n1_untyped_receiver"].get("effects", []))


@pytest.mark.parametrize("tool", ["n2_ctx_http", "n3_ret_annot_http", "n3_ret_annot_but_known"])
def test_negative_not_db(units, tool):
    """* n2: contextmanager が DB でないものを yield する
    * n3: DB 型でない戻り値注釈 / **既知の型を注釈で上書きしない**
    """
    assert "DB" not in _kinds(units[tool]), f"{tool}: DB 効果が出た（誤警報）"
