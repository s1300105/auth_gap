"""D64 / U23 の敵対的レビューの所見（U23-A1, U23-A2, U23-P1, U23-P2, U23-P3, U23-S1）の反例テスト。

**期待値は authgap/ を直す前に書いた（D64 / U23 の敵対的レビュー）。** 値は所見の expected から導いた。所見の
expected は Python / FastMCP / pydantic / dataclasses の意味と、D64 の U23 行、`evidence/review/triage.json` の U23
fix_outline（「避ける条件」）、D17 改訂 4 / 5（共有される可変オブジェクトの確度は opaque）、§9.3（モデリングして
いない関数を通った値は opaque → 不）に基づく。件数には合わせていない。

- A1（誤 clear）: lifespan_context は別のツールがモデルの値を書き込める共有状態。受け手型の要らない葉（Atom / Str /
  定数）の主体は、直す前と同じく ctx 根の MODEL（確度 opaque、root は ctx の部分パス）のまま。型は受け手の
  オブジェクトにだけ付ける。fix_outline (4)「D1 / D2 の類は 不 → 不 で変わらない」。
- A2（誤 clear）: `_opaque_deep` を深さで打ち切らない。3 段目より深い起動時の定数を resolved で読まない。モジュール
  水準の共有 dict（D17）も同じ関数を通る。
- P1 / P2 / P3 / S1（誤警報）: クラス体の代入で結ばれたフック、pydantic の `Final` の既定値つき（クラス変数）、
  dataclass の既定値の記述子、囲む関数のスコープ・`global` の再束縛で解かれる注釈。どれも実行すると値は OP の
  定数か、別の型になる。今日どおり（不 / pathlib の効果なし）にする。
- `test_keep_*`: 直した後も壊してはいけない対照（所見の対照と could_not_break の形）。
"""

from __future__ import annotations

import pytest

from authgap.ir import RESOLVED, Atom, Map, Obj, Path, Prin, Seq, Str, Unknown, Value
from authgap.report import manifest_json
from authgap.runner import RunConfig, run


def _units(tmp_path_factory, name, files):
    d = tmp_path_factory.mktemp(name)
    for rel, src in files.items():
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(src, encoding="utf-8")
    res = run(RunConfig(src_root=str(d), population="mcp_server", full=True))
    return {u["unit"]["qualname"]: u for u in manifest_json(res, "t")["units"]}


def _effects(u: dict, kind: str) -> list[dict]:
    return [e for e in u["effects"] if e["kind"] == kind]


def _slot(e: dict, name: str) -> dict:
    return (e.get("slots") or {}).get(name) or {}


def _brief(u: dict) -> list:
    out = []
    for e in u["effects"]:
        slots = {k: (v.get("prin"), v.get("prov"), v.get("roots"), (v.get("shape") or {}).get("const"))
                 for k, v in (e.get("slots") or {}).items()}
        out.append((e["kind"], e["site"], e.get("resolution"), e.get("http_method"), slots))
    return out


def _notes(u: dict, kind: str) -> list[str]:
    return [n for r in u["rows"] if r["kind"] == kind for n in r.get("notes", [])]


def _status(u: dict, kind: str, decl: str) -> str:
    rows = [r for r in u["rows"] if r["kind"] == kind]
    assert rows, f"{u['unit']['qualname']}: {kind} の行が無い（効果行が消えている）: {_brief(u)}"
    notes = [n for r in rows for n in r.get("notes", [])]
    hit = any(n == f"contradiction:{decl}" for n in notes)
    unk = any(n.startswith(f"contradiction_unknown:{decl}:") for n in notes)
    assert not (hit and unk), f"{decl} が矛と不の両方: {notes}"
    if hit:
        assert any("CONTRADICTION" in r["verdicts"] for r in rows), "注記が矛なのに CONTRADICTION が無い"
        return "矛"
    return "不" if unk else "内"


def _reasons(u: dict, kind: str, decl: str) -> set[str]:
    out = set()
    for n in _notes(u, kind):
        for pre in (f"contradiction_reason:{decl}:", f"contradiction_unknown:{decl}:"):
            if n.startswith(pre):
                out.add(n[len(pre):])
    return out


def _check(u: dict, kind: str, decl: str, want: str, reason: str | None = None) -> None:
    got = _status(u, kind, decl)
    q = u["unit"]["qualname"]
    assert got == want, f"{q} {kind} {decl}: {got}（期待 {want}）notes={_notes(u, kind)} effects={_brief(u)}"
    if reason is not None:
        assert reason in _reasons(u, kind, decl), f"{q} {decl}: 理由 {_reasons(u, kind, decl)}（期待 {reason}）"


def _not_contra(u: dict, kind: str, decl: str) -> None:
    if not [r for r in u["rows"] if r["kind"] == kind]:
        return
    got = _status(u, kind, decl)
    assert got != "矛", f"{u['unit']['qualname']} {decl}: 矛（誤警報）notes={_notes(u, kind)} effects={_brief(u)}"


def _model_resolved(s: dict) -> bool:
    return s.get("prin") == "MODEL" and s.get("prov") == "resolved"


def _resolved_consts(v: dict) -> set:
    out = set()
    if not v:
        return out
    shape = v.get("shape") or {}
    if v.get("prov") == "resolved" and "const" in shape:
        out.add(shape["const"])
    for it in shape.get("items") or []:
        out |= _resolved_consts(it)
    return out


def _ctx_rooted(s: dict) -> bool:
    roots = s.get("roots") or []
    return bool(roots) and all(r == "ctx" or r.startswith(("ctx[", "ctx.")) for r in roots)


# ===========================================================================
# U23-A1: lifespan の葉は ctx 根の MODEL/opaque のまま（型は受け手オブジェクトにだけ）
# ===========================================================================

LS_SHARED = '''from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import httpx
import psycopg

from mcp.server.fastmcp import Context, FastMCP

DB = psycopg.connect("dbname=app")


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[dict]:
    db = psycopg.connect("dbname=app")
    client = httpx.Client(base_url="https://api.example.com")
    try:
        yield {"db": db, "client": client, "table": "notes", "tag": "default"}
    finally:
        db.close()


mcp = FastMCP("t", lifespan=app_lifespan)


@mcp.tool()
def set_state(table: str, tag: str, key: str, ctx: Context) -> str:
    st = ctx.request_context.lifespan_context
    st["table"] = table
    st["tag"] = tag
    st["other"] = key
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def read_table(ctx: Context) -> str:
    st = ctx.request_context.lifespan_context
    return str(st["db"].execute("SELECT body FROM " + st["table"]).fetchall())


@mcp.tool(annotations={"readOnlyHint": True})
def read_table_moddb(ctx: Context) -> str:
    st = ctx.request_context.lifespan_context
    return str(DB.execute("SELECT body FROM " + st["table"]).fetchall())


@mcp.tool(annotations={"readOnlyHint": True})
def read_other_key(ctx: Context) -> str:
    # yield に無いキー（別のツールが足す）
    st = ctx.request_context.lifespan_context
    return str(DB.execute("SELECT body FROM " + st["other"]).fetchall())


@mcp.tool(annotations={"destructiveHint": False})
def log_tag(ctx: Context) -> str:
    DB.execute("INSERT INTO log(tag) VALUES ('" + ctx.request_context.lifespan_context["tag"] + "')")
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def purge(item_id: str, ctx: Context) -> str:
    # 対照: 受け手型は残る（本体の MODEL を連結した DELETE → 矛）
    ctx.request_context.lifespan_context["db"].execute("DELETE FROM items WHERE id = " + item_id)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def net_delete(item: str, ctx: Context) -> str:
    # 対照: lifespan のクライアントの受け手型
    ctx.request_context.lifespan_context["client"].request("DELETE", "/items/" + item)
    return "ok"
'''

LS_SHARED_DC = '''from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

import psycopg

from mcp.server.fastmcp import Context, FastMCP


@dataclass
class AppContext:
    db: psycopg.Connection
    table: str


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    db = psycopg.connect("dbname=app")
    try:
        yield AppContext(db=db, table="notes")
    finally:
        db.close()


mcp = FastMCP("t", lifespan=app_lifespan)


@mcp.tool()
def set_table(table: str, ctx: Context) -> str:
    ctx.request_context.lifespan_context.table = table
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def read_table_attr(ctx: Context) -> str:
    st = ctx.request_context.lifespan_context
    return str(st.db.execute("SELECT body FROM " + st.table).fetchall())
'''

LS_SHARED_LOW = '''from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import psycopg

from mcp.server import Server
from mcp.types import TextContent, Tool, ToolAnnotations


@asynccontextmanager
async def lifespan(server: Server) -> AsyncIterator[dict]:
    db = psycopg.connect("dbname=app")
    try:
        yield {"db": db, "table": "notes"}
    finally:
        db.close()


server = Server("t", lifespan=lifespan)


@server.list_tools()
async def list_tools():
    return [
        Tool(name="read", description="read", inputSchema={}, annotations=ToolAnnotations(readOnlyHint=True)),
    ]


def _remember(table: str) -> None:
    server.request_context.lifespan_context["table"] = table


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "set":
        _remember(arguments["table"])
        return [TextContent(type="text", text="ok")]
    if name == "read":
        st = server.request_context.lifespan_context
        rows = st["db"].execute("SELECT body FROM " + st["table"]).fetchall()
        return [TextContent(type="text", text=str(rows))]
    raise ValueError(name)
'''

LS_SHARED_LOW_INLINE = '''from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import psycopg

from mcp.server import Server
from mcp.types import TextContent, Tool, ToolAnnotations


@asynccontextmanager
async def lifespan(server: Server) -> AsyncIterator[dict]:
    db = psycopg.connect("dbname=app")
    try:
        yield {"db": db, "table": "notes"}
    finally:
        db.close()


server = Server("t", lifespan=lifespan)


@server.list_tools()
async def list_tools():
    return [
        Tool(name="read", description="read", inputSchema={}, annotations=ToolAnnotations(readOnlyHint=True)),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    st = server.request_context.lifespan_context
    if name == "set":
        st["table"] = arguments["table"]
        return [TextContent(type="text", text="ok")]
    if name == "read":
        rows = st["db"].execute("SELECT body FROM " + st["table"]).fetchall()
        return [TextContent(type="text", text=str(rows))]
    raise ValueError(name)
'''


@pytest.fixture(scope="module")
def shared(tmp_path_factory):
    return _units(tmp_path_factory, "u23adv_shared", {"server.py": LS_SHARED})


@pytest.fixture(scope="module")
def shared_dc(tmp_path_factory):
    return _units(tmp_path_factory, "u23adv_shared_dc", {"server.py": LS_SHARED_DC})


@pytest.fixture(scope="module")
def shared_low(tmp_path_factory):
    return _units(tmp_path_factory, "u23adv_shared_low", {"server.py": LS_SHARED_LOW})


@pytest.fixture(scope="module")
def shared_low_inline(tmp_path_factory):
    return _units(tmp_path_factory, "u23adv_shared_low_inline", {"server.py": LS_SHARED_LOW_INLINE})


def test_a1_moddb_select_prefix_stays_unknown(shared):
    """U23-A1: モジュール水準の接続に `"SELECT … " + lifespan_context["table"]`。直す前は ctx 根の MODEL/opaque で
    D1 不（db_sql_model_opaque）。共有状態の値を OP にすると SELECT の接頭辞で READ → 内（誤 clear）。不のまま。"""
    u = shared["read_table_moddb"]
    _check(u, "DB", "D1", "不", "db_sql_model_opaque")
    [e] = _effects(u, "DB")
    s = _slot(e, "sql")
    assert s.get("prin") == "MODEL" and s.get("prov") != "resolved", _brief(u)
    assert _ctx_rooted(s), _brief(u)


def test_a1_lifespan_db_select_prefix_is_unknown(shared):
    """U23-A1: lifespan の接続（受け手型が新しく付く）でも、共有状態のテーブル名を連結した SELECT は 不（内 にしない）。
    葉の主体は ctx 根の MODEL（確度 opaque）。"""
    u = shared["read_table"]
    assert _effects(u, "DB"), _brief(u)
    _check(u, "DB", "D1", "不", "db_sql_model_opaque")
    for e in _effects(u, "DB"):
        s = _slot(e, "sql")
        assert s.get("prin") == "MODEL" and s.get("prov") != "resolved" and _ctx_rooted(s), _brief(u)


def test_a1_unseen_key_is_unknown(shared):
    """U23-A1: yield に無いキー（別のツールが足す）も共有状態の値。OP にせず 不。"""
    _check(shared["read_other_key"], "DB", "D1", "不")


def test_a1_insert_tag_d2_stays_unknown(shared):
    """U23-A1: destructiveHint=False の `INSERT … '" + lifespan_context["tag"] + "'`。直す前は D2 不
    （db_sql_model_opaque）。OP にすると INSERT（additive）→ 内。不のまま。"""
    _check(shared["log_tag"], "DB", "D2", "不", "db_sql_model_opaque")


def test_a1_dataclass_attr_leaf_is_unknown(shared_dc):
    """U23-A1: `yield AppContext(db=..., table="notes")` の `.table`（属性の葉）も共有状態（別のツールが代入できる）。
    受け手 `.db` の型は付くが、SELECT の連結は 不。"""
    u = shared_dc["read_table_attr"]
    assert _effects(u, "DB"), _brief(u)
    _check(u, "DB", "D1", "不")


def test_a1_lowlevel_shared_leaf_not_clear(shared_low):
    """U23-A1: 低レベル `server.request_context.lifespan_context` も同じ共有状態（`set` の分岐が補助関数でモデルの値を
    書く）。受け手型は付いても、SELECT の接頭辞 + 共有状態の値を 内 にしない。"""
    u = shared_low["call_tool"]
    assert _effects(u, "DB"), _brief(u)
    _check(u, "DB", "D1", "不")


def test_keep_a1_lowlevel_inline_write_not_clear(shared_low_inline):
    """対照（同じ関数の中で書く形）: 行が無い（今日。分岐の合流で Map の中身が畳まれる既存の限界）か、あっても 内 にしない。"""
    u = shared_low_inline["call_tool"]
    if _effects(u, "DB"):
        assert _status(u, "DB", "D1") != "内", _brief(u)


def test_keep_a1_receiver_types_remain(shared):
    """対照（U23 の修正の目的）: 受け手型は残る。本体の MODEL を連結した DELETE → D1 矛、クライアントの DELETE →
    D1 矛 net_modify。"""
    _check(shared["purge"], "DB", "D1", "矛", "db_modify")
    u = shared["net_delete"]
    assert _effects(u, "NET"), _brief(u)
    _check(u, "NET", "D1", "矛", "net_modify")


def test_keep_a1_ctx_is_model_param(shared):
    """対照（R2-r1-10 は直さない）: ctx は入口の仮引数のまま。"""
    names = [p["name"] for p in shared["read_table"]["unit"]["params"]]
    assert "ctx" in names, names


# ===========================================================================
# U23-A2: 3 段目より深い共有状態の定数を resolved で読まない（_opaque_deep を深さで打ち切らない）
# ===========================================================================

LS_NESTED = '''import sqlite3
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import httpx

from mcp.server.fastmcp import Context, FastMCP

DB = sqlite3.connect("/data/app.db")


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[dict]:
    db = sqlite3.connect("/data/app.db")
    client = httpx.Client(base_url="https://api.example.com")
    yield {
        "db": db,
        "client": client,
        "cfg": {"saved": {"sql": "SELECT 1", "method": "GET"}},
    }


mcp = FastMCP("t", lifespan=app_lifespan)


@mcp.tool()
def set_query(sql: str, method: str, ctx: Context) -> str:
    saved = ctx.request_context.lifespan_context["cfg"]["saved"]
    saved["sql"] = sql
    saved["method"] = method
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def run_saved(ctx: Context) -> str:
    st = ctx.request_context.lifespan_context
    st["db"].execute(st["cfg"]["saved"]["sql"])
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def run_saved_moddb(ctx: Context) -> str:
    st = ctx.request_context.lifespan_context
    DB.execute(st["cfg"]["saved"]["sql"])
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def call_saved(ctx: Context) -> str:
    st = ctx.request_context.lifespan_context
    st["client"].request(st["cfg"]["saved"]["method"], "/items")
    return "ok"
'''

MOD_NESTED = '''import sqlite3

from mcp.server.fastmcp import FastMCP

DB = sqlite3.connect("/data/app.db")
STATE = {"cfg": {"saved": {"sql": "SELECT 1"}}}
mcp = FastMCP("t")


@mcp.tool()
def set_query(sql: str) -> str:
    STATE["cfg"]["saved"]["sql"] = sql
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def run_saved_mod() -> str:
    DB.execute(STATE["cfg"]["saved"]["sql"])
    return "ok"
'''


@pytest.fixture(scope="module")
def nested(tmp_path_factory):
    return _units(tmp_path_factory, "u23adv_nested", {"server.py": LS_NESTED})


@pytest.fixture(scope="module")
def mod_nested(tmp_path_factory):
    return _units(tmp_path_factory, "u23adv_mod_nested", {"server.py": MOD_NESTED})


@pytest.mark.parametrize("tool", ["run_saved", "run_saved_moddb"])
def test_a2_nested_saved_sql_is_unknown(nested, tool):
    """U23-A2（ce_lifespan_rebound の入れ子）: `st["cfg"]["saved"]["sql"]` は別のツールが書き換える。起動時の
    "SELECT 1" を resolved で読んで READ → 内 にしない。D1 は 不。"""
    u = nested[tool]
    assert _effects(u, "DB"), _brief(u)
    _check(u, "DB", "D1", "不")
    for e in _effects(u, "DB"):
        assert "SELECT 1" not in _resolved_consts(_slot(e, "sql")), _brief(u)


def test_a2_nested_saved_method_is_unknown(nested):
    """U23-A2: `st["cfg"]["saved"]["method"]` の起動時の "GET" を HTTP_SAFE に読まない。D1 は 不。"""
    u = nested["call_saved"]
    assert _effects(u, "NET"), _brief(u)
    for e in _effects(u, "NET"):
        assert e.get("http_method") not in ("GET", "HEAD", "OPTIONS"), _brief(u)
    _check(u, "NET", "D1", "不")


def test_a2_module_nested_state_not_clear(mod_nested):
    """U23-A2 の同じ穴（D17 のモジュール水準の共有 dict。`_opaque_deep` を共有する）: 3 段目の "SELECT 1" は
    `set_query` が書き換える。resolved で読まず、D1 は 不（直す前から 内 だった既存の誤 clear）。"""
    u = mod_nested["run_saved_mod"]
    assert _effects(u, "DB"), _brief(u)
    for e in _effects(u, "DB"):
        assert "SELECT 1" not in _resolved_consts(_slot(e, "sql")), _brief(u)
    _check(u, "DB", "D1", "不")


def _all_values(v: Value, seen=None):
    seen = set() if seen is None else seen
    if id(v) in seen:
        return
    seen.add(id(v))
    yield v
    s = v.shape
    subs: list = []
    if isinstance(s, (Seq, Str)):
        subs = list(s.elems if isinstance(s, Seq) else s.parts) + ([s.tail] if s.tail is not None else [])
    elif isinstance(s, Map):
        subs = [e for _k, e in s.entries] + ([s.tail] if s.tail is not None else [])
    elif isinstance(s, Obj):
        subs = [e for _k, e in s.fields]
    elif isinstance(s, Path):
        subs = ([s.base] if s.base is not None else []) + list(s.segs) + ([s.tail] if s.tail is not None else [])
    for x in subs:
        yield from _all_values(x, seen)


def test_a2_opaque_deep_has_no_depth_cut():
    """U23-A2: `_opaque_deep` は形の再帰を最後まで降りる。どの深さの要素 / フィールド / パスの部分にも resolved を残さない。"""
    from authgap.val.engine import _opaque_deep

    def c(x):
        return Value(Prin.OP, RESOLVED, Atom(const=x))

    leaf = c("SELECT 1")
    lvl5 = Value(Prin.OP, RESOLVED, Map((("sql", leaf),), None))
    lvl4 = Value(Prin.OP, RESOLVED, Obj(("Saved",), (("q", lvl5), ("p", Value(Prin.OP, RESOLVED, Path(base=c("/srv")))))))
    lvl3 = Value(Prin.OP, RESOLVED, Seq((lvl4, Value(Prin.OP, RESOLVED, Str((c("a"), c("b")), None))), None))
    lvl2 = Value(Prin.OP, RESOLVED, Map((("saved", lvl3),), None))
    top = Value(Prin.OP, RESOLVED, Map((("cfg", lvl2),), None))
    out = _opaque_deep(top)
    vals = list(_all_values(out))
    assert len(vals) >= 10
    bad = [v for v in vals if v.prov.kind == "resolved"]
    assert not bad, bad
    # 形と主体は保つ（受け手型のため）
    assert isinstance(out.shape, Map) and out.prin is Prin.OP


def test_a2_opaque_deep_terminates_on_cycle():
    """U23-A2: 循環する形（凍結したデータクラスを書き換えて作る）でも止まり、止めたところは opaque の Unknown（fail closed）。"""
    from authgap.val.engine import _opaque_deep

    inner = Value(Prin.OP, RESOLVED, Unknown())
    object.__setattr__(inner, "shape", Map((("self", inner),), None))
    out = _opaque_deep(inner)
    assert out.prov.kind != "resolved"
    [(k, v)] = out.shape.entries
    assert k == "self"
    assert v.prov.kind != "resolved"
    assert isinstance(v.shape, (Unknown, Map))


# ===========================================================================
# U23-P1 / P2 / P3: フック検出の抜け（誤警報）
# ===========================================================================

PYD_ADV = '''import os
from dataclasses import dataclass, field
from typing import Any, ClassVar, Final

from pydantic import BaseModel, Field, field_validator

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")
FIXED = "/srv/data/report.txt"
DEFAULT_PATH = "/srv/data/default.txt"


def _post(self, __context=None):
    object.__setattr__(self, "path", FIXED)


def fixed(cls, v: str) -> str:
    return FIXED


class Confine:
    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, obj, typ=None):
        return FIXED if obj is None else getattr(obj, self.name, FIXED)

    def __set__(self, obj, value):
        object.__setattr__(obj, self.name, FIXED)


CONF = Confine()


class PostAssign(BaseModel):
    path: str
    model_post_init = _post


@dataclass
class DcPostAssign:
    path: str
    __post_init__ = _post


class UnderReq(BaseModel):
    path: str
    _check: Any = field_validator("path")(fixed)


class CVReq(BaseModel):
    path: str
    check: ClassVar[Any] = field_validator("path")(fixed)


class FinalReq(BaseModel):
    OUT: Final[str] = FIXED
    name: str


@dataclass
class DcDesc:
    path: str = CONF


class PlainReq(BaseModel):
    # 対照: フックの無いモデル（既定値・ClassVar・private・Field は値を変えない）
    path: str
    mode: str = "w"
    tags: list[str] = Field(default_factory=list)
    limit: ClassVar[int] = 3
    _cache: dict = {}


@dataclass
class DcDefaults:
    # 対照: リテラルの既定値・リテラルに束縛された名前の既定値・field(...)
    path: str = DEFAULT_PATH
    mode: str = "w"
    tags: list = field(default_factory=list)


@dataclass
class DcFinal:
    # 対照: dataclasses は Final の既定値つきも init の引数（フィールド）にする
    path: Final[str] = FIXED


def _w(p: str, content: str) -> None:
    with open(p, "w") as f:
        f.write(content)


@mcp.tool(annotations={"destructiveHint": False})
def write_post_assign(req: PostAssign, content: str) -> str:
    with open(req.path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def write_dc_post_assign(req: DcPostAssign, content: str) -> str:
    with open(req.path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def write_under_v(req: UnderReq, content: str) -> str:
    with open(req.path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def write_cv_v(req: CVReq, content: str) -> str:
    with open(req.path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def write_final(req: FinalReq, content: str) -> str:
    with open(req.OUT, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def write_desc(req: DcDesc, content: str) -> str:
    with open(req.path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def write_plain_model(req: PlainReq, content: str) -> str:
    with open(req.path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def write_dc_defaults(req: DcDefaults, content: str) -> str:
    with open(req.path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def write_dc_final(req: DcFinal, content: str) -> str:
    with open(req.path, "w") as f:
        f.write(content)
    return "ok"
'''


@pytest.fixture(scope="module")
def pyd_adv(tmp_path_factory):
    return _units(tmp_path_factory, "u23adv_pyd", {"server.py": PYD_ADV})


@pytest.mark.parametrize(
    "tool",
    [
        "write_post_assign",  # P1 (1): model_post_init = _post
        "write_dc_post_assign",  # P1 (2): __post_init__ = _post
        "write_under_v",  # P1 (3): `_` 始まりの AnnAssign に置いた field_validator(...)(f)
        "write_cv_v",  # P1 (4): ClassVar の AnnAssign に置いた field_validator(...)(f)
        "write_desc",  # P3: dataclass の既定値が名前で参照される記述子
    ],
)
def test_p1_p3_hooks_stay_unknown(pyd_adv, tool):
    """U23-P1 / P3: 実行すると open に渡るのは OP の定数 FIXED。フックとして扱い、今日どおり MODEL に opaque を合流 →
    D2 不（fs_writeout_model_path_opaque）。MODEL/resolved にして矛を出すと誤警報。"""
    u = pyd_adv[tool]
    _check(u, "FS_WRITE", "D2", "不", "fs_writeout_model_path_opaque")
    for e in _effects(u, "FS_WRITE"):
        assert not _model_resolved(_slot(e, "path")), _brief(u)


def test_p2_pydantic_final_default_is_not_a_field(pyd_adv):
    """U23-P2: pydantic は `OUT: Final[str] = FIXED` をクラス変数として扱う（model_fields に入らない）。値は OP の定数。
    MODEL/resolved にして矛を出さない（不か矛以外）。"""
    u = pyd_adv["write_final"]
    _not_contra(u, "FS_WRITE", "D2")
    for e in _effects(u, "FS_WRITE"):
        assert not _model_resolved(_slot(e, "path")), _brief(u)


@pytest.mark.parametrize("tool", ["write_plain_model", "write_dc_defaults", "write_dc_final"])
def test_keep_p_controls_are_chosen(pyd_adv, tool):
    """対照（U23 の修正の目的）: フックの無いモデル（リテラル・リテラルに束縛された名前・Field / field の既定値、
    ClassVar / `_` のリテラル）と、dataclass の Final フィールドは、モデルが埋めるフィールド → MODEL/resolved → 矛。"""
    u = pyd_adv[tool]
    _check(u, "FS_WRITE", "D2", "矛", "fs_writeout_model_path")
    [e] = _effects(u, "FS_WRITE")
    s = _slot(e, "path")
    assert _model_resolved(s) and s.get("roots") == ["req.path"], _brief(u)


# ===========================================================================
# U23-S1: 注釈を囲む関数のスコープと global の再束縛で解く（誤警報）
# ===========================================================================

S1_SERVER = '''import os
from pathlib import Path

from pydantic import BaseModel, field_validator

from mcp.server.fastmcp import FastMCP

BASE = "/srv/data"
FIXED = "/srv/data/report.txt"


class Req(BaseModel):
    path: str


class PlainReq(BaseModel):
    path: str


def register(mcp: FastMCP) -> None:
    class Req(BaseModel):  # noqa: F811  局所のクラス（注釈はこちらを指す）
        path: str

        @field_validator("path")
        @classmethod
        def _fix(cls, v: str) -> str:
            return FIXED

    from store import Path  # 局所の import（遠隔ストレージのキー）

    @mcp.tool(annotations={"destructiveHint": False})
    def write_local(req: Req, content: str) -> str:
        with open(req.path, "w") as f:
            f.write(content)
        return "ok"

    @mcp.tool(annotations={"readOnlyHint": True})
    def put_local(path: Path, text: str) -> str:
        path.write_text(text)
        return "ok"

    @mcp.tool(annotations={"destructiveHint": False})
    def write_nested_plain(req: PlainReq, content: str) -> str:
        # 対照: 局所で束縛されない注釈はモジュール直下のクラスを指す
        with open(req.path, "w") as f:
            f.write(content)
        return "ok"


mcp = FastMCP("t")
register(mcp)
'''

S1_STORE = '''import requests
from pydantic_core import core_schema


class Path:
    def __init__(self, key: str) -> None:
        self.key = key

    @classmethod
    def __get_pydantic_core_schema__(cls, source, handler):
        return core_schema.no_info_after_validator_function(cls, core_schema.str_schema())

    def write_text(self, text: str) -> None:
        requests.post("https://store.example.com/put", json={"key": self.key, "text": text})
'''

S1_NESTED_PATH_CONTROL = '''from pathlib import Path

from mcp.server.fastmcp import FastMCP


def register(mcp: FastMCP) -> None:
    @mcp.tool(annotations={"readOnlyHint": True})
    def put_nested(path: Path, text: str) -> str:
        path.write_text(text)
        return "ok"


mcp = FastMCP("t")
register(mcp)
'''

S1_GLOBAL = '''from pathlib import Path

from pydantic import BaseModel, field_validator

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")
FIXED = "/srv/data/report.txt"


class Req(BaseModel):
    path: str


def _harden() -> None:
    global Req

    class Req(BaseModel):  # noqa: F811
        path: str

        @field_validator("path")
        @classmethod
        def _fix(cls, v: str) -> str:
            return FIXED


def _swap_path() -> None:
    global Path
    from store import Path


_harden()
_swap_path()


@mcp.tool(annotations={"destructiveHint": False})
def write_global(req: Req, content: str) -> str:
    with open(req.path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def put_global(path: Path, text: str) -> str:
    path.write_text(text)
    return "ok"
'''

S1_GLOBAL_CTX = '''import sqlite3
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from mcp.server.fastmcp import Context, FastMCP


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[dict]:
    db = sqlite3.connect("/data/app.db")
    try:
        yield {"db": db}
    finally:
        db.close()


def _swap_context() -> None:
    global Context
    from mylib import Context


_swap_context()
mcp = FastMCP("t", lifespan=app_lifespan)


@mcp.tool(annotations={"readOnlyHint": True})
def purge(item_id: str, ctx: Context) -> str:
    ctx.request_context.lifespan_context["db"].execute("DELETE FROM items WHERE id = " + item_id)
    return "ok"
'''


@pytest.fixture(scope="module")
def s1(tmp_path_factory):
    return _units(tmp_path_factory, "u23adv_s1", {"server.py": S1_SERVER, "store.py": S1_STORE})


@pytest.fixture(scope="module")
def s1_ctl(tmp_path_factory):
    return _units(tmp_path_factory, "u23adv_s1_ctl", {"server.py": S1_NESTED_PATH_CONTROL})


@pytest.fixture(scope="module")
def s1_global(tmp_path_factory):
    return _units(tmp_path_factory, "u23adv_s1_global", {"server.py": S1_GLOBAL, "store.py": S1_STORE})


@pytest.fixture(scope="module")
def s1_global_ctx(tmp_path_factory):
    return _units(tmp_path_factory, "u23adv_s1_global_ctx", {"server.py": S1_GLOBAL_CTX})


def _no_pathlib_write(u: dict) -> None:
    effs = [e for e in u["effects"] if e["kind"] == "FS_WRITE" and str(e["site"]).startswith("pathlib.")]
    assert not effs, _brief(u)
    _not_contra(u, "FS_WRITE", "D1")


def test_s1_local_class_shadows_module_class(s1):
    """U23-S1: `register()` の中の `write_local(req: Req)` の `Req` は局所のクラス（field_validator が FIXED を返す）。
    モジュール直下の `Req` で解いてフィールドを resolved にしない → 今日どおり D2 不。"""
    u = s1["register.write_local"]
    _check(u, "FS_WRITE", "D2", "不", "fs_writeout_model_path_opaque")
    for e in _effects(u, "FS_WRITE"):
        assert not _model_resolved(_slot(e, "path")), _brief(u)


def test_s1_local_import_shadows_pathlib(s1):
    """U23-S1: `put_local(path: Path)` の `Path` は局所の `from store import Path`（write_text は HTTP POST）。
    pathlib の FS_WRITE を足さない（D1 の矛を作らない）。"""
    _no_pathlib_write(s1["register.put_local"])


def test_s1_global_rebinding_class(s1_global):
    """U23-S1: `_harden()` の `global Req` がモジュールの `Req` を検証子つきのクラスに差し替える。モジュール直下で
    1 回束縛とは数えない → 今日どおり D2 不。"""
    u = s1_global["write_global"]
    _check(u, "FS_WRITE", "D2", "不", "fs_writeout_model_path_opaque")
    for e in _effects(u, "FS_WRITE"):
        assert not _model_resolved(_slot(e, "path")), _brief(u)


def test_s1_global_rebinding_path(s1_global):
    """U23-S1: `global Path` で `store.Path` に差し替わる注釈に pathlib の効果を足さない。"""
    _no_pathlib_write(s1_global["put_global"])


def test_s1_global_rebinding_context(s1_global_ctx):
    """U23-S1（lifespan の Context の解決にも同じ守り）: `global Context` で利用者の Context に差し替わる注釈には
    lifespan の値を種付けしない（今日どおり DB 行 0）。"""
    u = s1_global_ctx["purge"]
    assert not _effects(u, "DB"), _brief(u)


def test_keep_s1_nested_plain_model_is_chosen(s1):
    """対照: `register()` の中の入口でも、局所で束縛されない注釈（`PlainReq`）はモジュール直下のクラス → 矛。"""
    _check(s1["register.write_nested_plain"], "FS_WRITE", "D2", "矛", "fs_writeout_model_path")


def test_keep_s1_nested_pathlib_is_typed(s1_ctl):
    """対照: `register()` の中の入口で、モジュール直下の `from pathlib import Path` を指す注釈は Path 形 → D1 矛。"""
    u = s1_ctl["register.put_nested"]
    assert [e for e in _effects(u, "FS_WRITE") if e["site"] == "pathlib.Path.write_text"], _brief(u)
    _check(u, "FS_WRITE", "D1", "矛", "fs_write")
