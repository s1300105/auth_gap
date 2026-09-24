"""O30 / O32 / O33 の直し方（`docs/contradiction_principles.md` §9、D57）。

**期待値はこのテストで、`authgap/` を直す前に書いた**（CLAUDE.md 規則 5 の趣旨）。
規則は `f4d13f9` / `81dc0d4` でコミット済み。各節に**反例**（変えてはいけない形）を入れた。
"""

from __future__ import annotations

import pytest

from authgap.report import manifest_json
from authgap.runner import RunConfig, run

# ---------------------------------------------------------------------------
# O30: テストファイルの定義は、本体からの末尾名の解決の候補にしない
# ---------------------------------------------------------------------------

O30_SERVER = r'''
import logging
import os
from mcp.server.fastmcp import FastMCP
from tests.helpers import explicit_helper

mcp = FastMCP("t")
logger = logging.getLogger(__name__)


class Store:
    def save(self, p):
        open(p, "w").write("x")


@mcp.tool()
async def logs_error(p: str) -> str:
    logger.error("boom %s", p)
    return "x"


@mcp.tool()
async def uses_explicit(p: str) -> str:
    explicit_helper(p)
    return "x"


@mcp.tool()
async def ambiguous_save(obj, p: str) -> str:
    obj.save(p)
    return "x"
'''

O30_TEST_REC = r'''
import os


def scope_records():
    class _Recorder:
        def error(self, msg, *args):
            os.remove("/tmp/authgap_rec")

    return _Recorder()
'''

O30_TEST_HELPERS = r'''
import os


def explicit_helper(p):
    os.remove(p)
'''

O30_TEST_FAKES = r'''
import os


class FakeStore:
    def save(self, p):
        os.remove(p)
'''

O30_TEST_TOOLS = r'''
import os
from mcp.server.fastmcp import FastMCP

mcp2 = FastMCP("t2")


class LocalHelper:
    def cleanup(self, p):
        os.remove(p)


@mcp2.tool()
async def tool_in_test_file(h, p: str) -> str:
    h.cleanup(p)
    return "x"
'''


@pytest.fixture(scope="module")
def o30(tmp_path_factory):
    d = tmp_path_factory.mktemp("o30")
    (d / "server.py").write_text(O30_SERVER, encoding="utf-8")
    (d / "tests").mkdir()
    (d / "tests" / "__init__.py").write_text("", encoding="utf-8")
    (d / "tests" / "test_rec.py").write_text(O30_TEST_REC, encoding="utf-8")
    (d / "tests" / "helpers.py").write_text(O30_TEST_HELPERS, encoding="utf-8")
    (d / "tests" / "fakes.py").write_text(O30_TEST_FAKES, encoding="utf-8")
    (d / "tests" / "test_tools.py").write_text(O30_TEST_TOOLS, encoding="utf-8")
    res = run(RunConfig(src_root=str(d), population="mcp_server", full=True))
    return {u["unit"]["qualname"]: u for u in manifest_json(res, "t")["units"]}


def _effects(u, kind=None):
    return [e for e in u["effects"] if kind is None or e["kind"] == kind]


def test_o30_logger_error_does_not_reach_test_class(o30):
    # 本体の logger.error が tests/ の関数内クラスに結ばれない
    assert not [e for e in _effects(o30["logs_error"]) if e["relpath"].startswith("tests/")]


def test_o30_explicit_import_from_tests_is_kept(o30):
    # 反例: import 表で明示的に結んだ定義には今までどおり降りる
    got = [e for e in _effects(o30["uses_explicit"], "FS_WRITE") if e["relpath"] == "tests/helpers.py"]
    assert got


def test_o30_tool_defined_in_test_file_still_resolves_locally(o30):
    # 反例: テストファイルで定義されたツールからは、同じテストファイルの定義を候補にする
    got = [e for e in _effects(o30["tool_in_test_file"], "FS_WRITE") if e["relpath"] == "tests/test_tools.py"]
    assert got


def test_o30_remaining_single_production_candidate_is_descended(o30):
    # テストの候補（FakeStore.save）が外れて本体の候補（Store.save）が 1 つだけ残るので、
    # 末尾名で降りて opaque(unresolved) を合流する（D17 改訂の規則のまま）
    effs = [e for e in _effects(o30["ambiguous_save"], "FS_WRITE") if e["relpath"] == "server.py"]
    assert effs
    assert all(e["resolution"] == "opaque" and "unresolved" in e.get("resolution_reasons", []) for e in effs)
    assert not [e for e in _effects(o30["ambiguous_save"]) if e["relpath"].startswith("tests/")]


@pytest.mark.parametrize(
    "path,want",
    [
        ("tests/x.py", True),
        ("a/test/b.py", True),
        ("testing/x.py", True),
        ("pkg/tests/unit/x.py", True),
        ("test_foo.py", True),
        ("src/foo_test.py", True),
        ("conftest.py", True),
        ("src/contest.py", False),
        ("tests_helpers/x.py", False),
        ("latest.py", False),
        ("attest/x.py", False),
        ("src/testify.py", False),
    ],
)
def test_is_test_path(path, want):
    from authgap.srcindex import is_test_path

    assert is_test_path(path) is want


# ---------------------------------------------------------------------------
# O32: 相対 URL の宛先は base_url で決まる
# ---------------------------------------------------------------------------

O32_SRC = r'''
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")


@mcp.tool(annotations={"openWorldHint": False})
async def rel_path(item_id: str) -> str:
    c = httpx.AsyncClient(base_url="https://api.example.com")
    await c.get("/items/" + item_id)
    return "x"


@mcp.tool(annotations={"openWorldHint": False})
async def rel_path_local(item_id: str) -> str:
    c = httpx.AsyncClient(base_url="http://localhost:8080")
    await c.get("/items/" + item_id)
    return "x"


@mcp.tool(annotations={"openWorldHint": False})
async def rel_path_model_base(base: str, item_id: str) -> str:
    c = httpx.AsyncClient(base_url=base)
    await c.get("/items/" + item_id)
    return "x"


@mcp.tool(annotations={"openWorldHint": False})
async def slash_only(item_id: str) -> str:
    c = httpx.AsyncClient(base_url="https://api.example.com")
    await c.get("/" + item_id)
    return "x"


@mcp.tool(annotations={"openWorldHint": False})
async def double_slash(item_id: str) -> str:
    c = httpx.AsyncClient(base_url="https://api.example.com")
    await c.get("//" + item_id)
    return "x"


@mcp.tool(annotations={"openWorldHint": False})
async def full_url_param(url: str) -> str:
    c = httpx.AsyncClient(base_url="https://api.example.com")
    await c.get(url)
    return "x"


@mcp.tool(annotations={"openWorldHint": False})
async def rel_no_base(item_id: str) -> str:
    httpx.get("/items/" + item_id)
    return "x"
'''


@pytest.fixture(scope="module")
def o32(tmp_path_factory):
    d = tmp_path_factory.mktemp("o32")
    (d / "server.py").write_text(O32_SRC, encoding="utf-8")
    res = run(RunConfig(src_root=str(d), population="mcp_server", full=True))
    return {u["unit"]["qualname"]: u for u in manifest_json(res, "t")["units"]}


def _net(u):
    effs = _effects(u, "NET")
    assert effs, f"{u['unit']['qualname']}: NET 効果が無い（前提）"
    return effs


def _d3(u):
    notes = [n for r in u["rows"] if r["kind"] == "NET" for n in r.get("notes", [])]
    if "contradiction:D3" in notes:
        return "矛"
    return "不" if any(n.startswith("contradiction_unknown:D3:") for n in notes) else "内"


def _host(e):
    return e["slots"].get("url.host")


def test_o32_relative_url_host_comes_from_base_url(o32):
    for e in _net(o32["rel_path"]):
        h = _host(e)
        assert h is not None and h["prin"] == "OP"
        assert "api.example.com" in str(h["shape"].get("const", ""))
        assert e["slots"]["url.path"]["prin"] == "MODEL"
    # SSRF の座標（url.host）に GAP_INJECT が立たない。パスの座標には立つ
    rows = [r for r in o32["rel_path"]["rows"] if r["kind"] == "NET"]
    assert not [r for r in rows if r["slot"] == "url.host" and "GAP_INJECT" in r["verdicts"]]
    assert [r for r in rows if r["slot"] == "url.path" and "GAP_INJECT" in r["verdicts"]]
    assert _d3(o32["rel_path"]) == "矛"  # 定数の外部ホスト


def test_o32_relative_url_local_base(o32):
    assert _d3(o32["rel_path_local"]) == "内"


def test_o32_relative_url_model_base(o32):
    # base_url をモデルが選べるなら宛先もモデルが選べる
    assert any((_host(e) or {}).get("prin") == "MODEL" for e in _net(o32["rel_path_model_base"]))
    assert _d3(o32["rel_path_model_base"]) == "矛"


@pytest.mark.parametrize("tool", ["slash_only", "double_slash", "full_url_param"])
def test_o32_not_split_keeps_model_host(o32, tool):
    # 反例: "/" だけ・"//"・URL 全体がモデル由来は、今までどおり宛先がモデル由来
    assert any((_host(e) or {}).get("prin") == "MODEL" for e in _net(o32[tool]))
    rows = [r for r in o32[tool]["rows"] if r["kind"] == "NET"]
    assert [r for r in rows if r["slot"] == "url.host" and "GAP_INJECT" in r["verdicts"]]
    assert _d3(o32[tool]) == "矛"


def test_o32_relative_url_without_base_has_no_host(o32):
    for e in _net(o32["rel_no_base"]):
        assert _host(e) is None
    assert _d3(o32["rel_no_base"]) == "不"


# ---------------------------------------------------------------------------
# O33:「モデルが選べる」は主体 MODEL かつ確度 resolved。SQL は §9.4 の順序
# ---------------------------------------------------------------------------

O33_SRC = r'''
import sqlite3
from mcp.server.fastmcp import FastMCP
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import somelib
from models import User

mcp = FastMCP("t")


def db():
    return sqlite3.connect("x.db")


@mcp.tool(annotations={"readOnlyHint": True})
async def sql_param(sql: str) -> str:
    db().execute(sql); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def sql_through_unmodeled(sql: str) -> str:
    db().execute(somelib.normalize(sql)); return "x"


async def run_query(session: AsyncSession, names):
    return await session.execute(select(User).where(User.name.in_(names)))


@mcp.tool(annotations={"destructiveHint": False})
async def orm_select(names: list) -> str:
    await run_query(somelib.get_session(), names); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def update_prefix_opaque(ids: list) -> str:
    db().execute("UPDATE t SET done = 1 WHERE id IN (" + somelib.join(ids) + ")"); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def select_prefix_chosen(a: str) -> str:
    db().execute("SELECT * FROM t WHERE a = " + a); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def select_prefix_opaque(a: str) -> str:
    db().execute("SELECT * FROM t WHERE a = " + somelib.quote(a)); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def incomplete_prefix(op: str) -> str:
    db().execute("UPD" + op); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def op_config_select(p: str) -> str:
    db().execute("SELECT * FROM " + somelib.TABLE); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def op_config_update(p: str) -> str:
    db().execute("UPDATE " + somelib.TABLE + " SET a = 1"); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def pragma_prefix(mode: str) -> str:
    db().execute("PRAGMA journal_mode=" + mode); return "x"


@mcp.tool(annotations={"destructiveHint": False})
async def path_param(path: str) -> str:
    open(path, "w").write("x"); return "x"


@mcp.tool(annotations={"destructiveHint": False})
async def path_through_unmodeled(path: str) -> str:
    open(somelib.sanitize(path), "w").write("x"); return "x"


@mcp.tool(annotations={"idempotentHint": True})
async def idem_sql_param(sql: str) -> str:
    db().execute(sql); return "x"
'''


@pytest.fixture(scope="module")
def o33(tmp_path_factory):
    d = tmp_path_factory.mktemp("o33")
    (d / "server.py").write_text(O33_SRC, encoding="utf-8")
    res = run(RunConfig(src_root=str(d), population="mcp_server", full=True))
    return {u["unit"]["qualname"]: u for u in manifest_json(res, "t")["units"]}


def _finding(u, kind, decl):
    rows = [r for r in u["rows"] if r["kind"] == kind]
    assert rows, f"{u['unit']['qualname']}: {kind} の行が無い（前提）"
    notes = [n for r in rows for n in r.get("notes", [])]
    reasons = sorted(n.split(":", 2)[2] for n in notes if n.startswith(f"contradiction_reason:{decl}:"))
    if f"contradiction:{decl}" in notes:
        return ("矛", reasons)
    unk = sorted(n.split(":", 2)[2] for n in notes if n.startswith(f"contradiction_unknown:{decl}:"))
    return ("不", unk) if unk else ("内", [])


@pytest.mark.parametrize(
    "tool,kind,decl,want,reason",
    [
        ("sql_param", "DB", "D1", "矛", "db_model_sql"),
        ("sql_through_unmodeled", "DB", "D1", "不", "db_sql_model_opaque"),
        ("orm_select", "DB", "D2", "不", "db_sql_model_opaque"),
        ("update_prefix_opaque", "DB", "D1", "矛", "db_modify"),
        # 反例: SELECT の接頭辞でも、モデルが選べる連結なら注入で DELETE を書ける
        ("select_prefix_chosen", "DB", "D1", "矛", "db_model_sql"),
        ("select_prefix_opaque", "DB", "D1", "不", "db_sql_model_opaque"),
        ("incomplete_prefix", "DB", "D1", "矛", "db_model_sql"),
        # 主体が MODEL でない連結は接頭辞で決める
        ("op_config_select", "DB", "D1", "内", None),
        ("op_config_update", "DB", "D1", "矛", "db_modify"),
        ("pragma_prefix", "DB", "D1", "矛", "db_model_sql"),
        ("path_param", "FS_WRITE", "D2", "矛", "fs_writeout_model_path"),
        ("path_through_unmodeled", "FS_WRITE", "D2", "不", None),
        # D4 には原理 3 を当てない
        ("idem_sql_param", "DB", "D4", "不", None),
    ],
)
def test_o33(o33, tool, kind, decl, want, reason):
    got, reasons = _finding(o33[tool], kind, decl)
    assert got == want, (tool, got, reasons)
    if reason is not None:
        assert reason in reasons, (tool, reasons)


# ---------------------------------------------------------------------------
# §9.5: 属性の呼び出しをクラス外の関数へ末尾名だけで結ぶ解決は by_name
# ---------------------------------------------------------------------------

S95_SERVER = r'''
from mcp.server.fastmcp import FastMCP
import ladder

mcp = FastMCP("t")


@mcp.tool()
async def method_to_free_fn(obj, q: str) -> str:
    obj.get(q)
    return "x"


@mcp.tool()
async def module_qualified(q: str) -> str:
    ladder.get(q)
    return "x"
'''

S95_LADDER = r'''
import sqlite3


def get(k):
    sqlite3.connect("x.db").execute("SELECT 1")
    return 1
'''


@pytest.fixture(scope="module")
def s95(tmp_path_factory):
    d = tmp_path_factory.mktemp("s95")
    (d / "server.py").write_text(S95_SERVER, encoding="utf-8")
    (d / "ladder.py").write_text(S95_LADDER, encoding="utf-8")
    res = run(RunConfig(src_root=str(d), population="mcp_server", full=True))
    return {u["unit"]["qualname"]: u for u in manifest_json(res, "t")["units"]}


def test_s95_method_call_to_free_function_is_by_name(s95):
    # obj の型は分からない。obj.get を ladder.get（クラス外の関数）に結ぶのは推測なので opaque
    for e in _effects(s95["method_to_free_fn"], "DB"):
        assert e["resolution"] == "opaque" and "unresolved" in e.get("resolution_reasons", []), e


def test_s95_module_qualified_call_stays_resolved(s95):
    # 反例: import したモジュールの関数は import 表で結ばれるので確かな経路
    effs = _effects(s95["module_qualified"], "DB")
    assert effs
    assert all(e["resolution"] == "resolved" for e in effs)
