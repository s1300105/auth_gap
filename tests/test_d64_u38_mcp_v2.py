"""D64 / U38: mcp 2.x の SDK を SDK の署名どおりに読む。所見 R2-r1-1, R2-r3-1, R2-r3-2, R2-r3-3, R2-r4-1（別名の半分）。

**期待値はこのテストで、`authgap/` を直す前に書いた（D64 / U38）。** v2 / v3 の件数には合わせず、
mcp SDK の署名・§7 の判定表（§7.1 FS_WRITE / SPAWN、§7.2 remove / writeout）・Def 2（低レベル v2 の 2 形）・
Def 6 の版規則・規則 4（黙って安全側に倒さない）・D64 の U38 行と `evidence/review/triage.json` の fix_outline から導いた。

- R2-r1-1（snake_case）: 版で条件づける。>=2.0 に決まれば宣言（camelCase に写す）、<2.0 に決まれば今どおり
  `D_malformed`、決まらなければ `D_unknown`（⊥ とも malformed とも混ぜない）。表し方は既存のもの
  （`DKind.unknown` → manifest の `D_kind["unknown"] is True`、`D_malformed` → `D_kind["malformed"]`）。
  反例: mcp==1.30.0 に確定した木（cx_r1_1_pinned1x）は malformed のまま。両方の API を import する shim
  （cx_r1_1_ambiguous）・API の形と lock が食い違う木・lock が食い違う monorepo は D_unknown で、どちらにも倒さない。
  D_unknown に移しても verdict は動かない（fix_outline 条件 (4)）。
- R2-r3-1（params の種付け）: v2 ハンドラの第 2 位置（self / cls を除いて数える。名前によらない）は
  `CallToolRequestParams` の形で、`params.arguments[...]` は MODEL / resolved。`ctx` は変えない。
  反例: 木の中の非 mcp の `Server`（A2）と装飾子で `(name, arguments)` に変える形（A3）の行は変えない。v1（t71）も不変。
- R2-r3-2（add_request_handler）: handler は `handler=` か最後の位置引数。反例 ce_r3_2（自前 JSON-RPC の
  2 引数形）は今ユニットになり D1 の矛が出る。`args[2]` だけにすると消える。
- R2-r3-3（ハンドラの名前）: import 表で一意に解けるときだけその定義に絞る。解けなければ裸名一致に落とし、
  登録元がテストでなければテストファイルの候補を外す。partial / lambda は `unresolved_handler` として記録する。
  反例 ce_r3_3（star import 経由）は今正しく D1 の矛。予備を消すと消える。
- R2-r4-1（別名 import の半分だけ）: `from mcp.server.lowlevel import Server as X` / `from mcp.server import Server as X`。
  **サブクラスの半分は記録に回す（学生の決定）ので、サブクラス形の今の振る舞いはテストしない。**
  ただし反例 ce_r4_1 の「tests/ の同名 test double をユニットにしない」は R2-r3-3 の条件でもあるので入れる
  （サブクラスのハンドラがユニットになるかどうかは見ない）。

記号: 「矛」 = 行の注記に `contradiction:<宣言>`、「不」 = `contradiction_unknown:<宣言>:<理由>`。
"""

from __future__ import annotations

import json

import pytest

from authgap.report import manifest_json
from authgap.runner import RunConfig, run


def _manifest(tmp_path_factory, name, files):
    d = tmp_path_factory.mktemp(name)
    for rel, src in files.items():
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(src, encoding="utf-8")
    res = run(RunConfig(src_root=str(d), population="mcp_server", full=True))
    return manifest_json(res, "t")


def _units(m):
    """`(relpath, qualname)` → ユニット。同名のハンドラが別ファイルにあるので relpath も鍵に入れる。"""
    return {(u["unit"]["relpath"], u["unit"]["qualname"]): u for u in m["units"]}


def _by_qual(m, qualname):
    hits = [u for u in m["units"] if u["unit"]["qualname"] == qualname]
    assert hits, f"{qualname} がユニットにならない: {sorted(_units(m))}"
    assert len(hits) == 1, f"{qualname} が複数: {[h['unit']['relpath'] for h in hits]}"
    return hits[0]


def _notes_at(u, site):
    rows = [r for r in u["rows"] if r["site"] == site]
    assert rows, f"{u['unit']['qualname']}: {site} の行が無い: {[r['site'] for r in u['rows']]}"
    return {n for r in rows for n in r.get("notes", [])}


def _slot(u, site, slot):
    effs = [e for e in u["effects"] if e["site"] == site]
    assert effs, f"{u['unit']['qualname']}: {site} の効果が無い"
    s = effs[0]["slots"][slot]
    return s["prin"], s["prov"]


def _any_contradiction(m):
    return any(
        "CONTRADICTION" in r.get("verdicts", []) or any(n.startswith("contradiction:") for n in r.get("notes", []))
        for u in m["units"]
        for r in u["rows"]
    )


def _lowlevel_v2(m):
    return {(u["unit"]["relpath"], u["unit"]["qualname"]) for u in m["units"] if u["unit"]["entry_kind"] == "lowlevel_v2"}


UV_LOCK_2 = '''version = 1

[[package]]
name = "mcp"
version = "2.1.1"
source = { registry = "https://pypi.org/simple" }
'''

UV_LOCK_1 = '''version = 1

[[package]]
name = "mcp"
version = "1.30.0"
source = { registry = "https://pypi.org/simple" }
'''

# ===========================================================================
# R2-r1-1: snake_case の ToolAnnotations は版で条件づける
# ===========================================================================

#: 所見 R2-r1-1 の再現（t05_snake_mcp2）: lockfile で mcp 2.1.1 に確定し、API の形も 2.x（mcpserver）。
T05_SERVER = '''import os
from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations

server = MCPServer("t")


@server.tool(annotations=ToolAnnotations(read_only_hint=True))
def snake_ro(path: str, text: str) -> str:
    with open(path, "w") as f:
        f.write(text)
    return "ok"


@server.tool(annotations=ToolAnnotations(read_only_hint=False, destructive_hint=False))
def snake_nd(path: str) -> str:
    os.remove(path)
    return "ok"


@server.tool(annotations=ToolAnnotations(readOnlyHint=True))
def camel_ro(path: str, text: str) -> str:
    with open(path, "w") as f:
        f.write(text)
    return "ok"
'''

T05 = {
    "pyproject.toml": '[project]\nname = "snake-server"\nversion = "0.1.0"\ndependencies = ["mcp>=2.0.0"]\n',
    "uv.lock": UV_LOCK_2,
    "server.py": T05_SERVER,
}

#: API の形だけで >=2.0（`mcp.server.mcpserver` の import）。依存の記載は無い。
V2_SHAPE_ONLY = {
    "server.py": '''from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations

server = MCPServer("t")


@server.tool(annotations=ToolAnnotations(read_only_hint=True))
def shape_ro(path: str, text: str) -> str:
    with open(path, "w") as f:
        f.write(text)
    return "ok"
''',
}

#: API の形だけで >=2.0（低レベルの `Server(on_call_tool=)`）。snake_case は `Tool(...)` リテラルの側。
V2_LOWLEVEL_SNAKE = {
    "server.py": '''import os

from mcp.server.lowlevel import Server
from mcp.types import CallToolResult, ListToolsResult, TextContent, Tool, ToolAnnotations


async def list_tools(ctx, params):
    return ListToolsResult(tools=[
        Tool(name="ll_snake_rm", description="d", inputSchema={}, annotations=ToolAnnotations(read_only_hint=True)),
    ])


async def handle(ctx, params):
    if params.name == "ll_snake_rm":
        os.remove(params.arguments["path"])
        return CallToolResult(content=[TextContent(type="text", text="ok")])
    raise ValueError(params.name)


server = Server("t", on_list_tools=list_tools, on_call_tool=handle)
''',
}

FASTMCP_SERVER = '''from fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("t")


@mcp.tool(annotations=ToolAnnotations(read_only_hint=True))
def fm_ro(path: str, text: str) -> str:
    with open(path, "w") as f:
        f.write(text)
    return "ok"
'''

#: fastmcp>=4 は mcp>=2.0 を要求する（fastmcp-slim 4.0.10 の METADATA: mcp<3.0.0,>=2.0.0）。canvas-mcp と同じ書き方。
FASTMCP4 = {
    "pyproject.toml": '[project]\nname = "fm4"\nversion = "0.1.0"\ndependencies = ["fastmcp>=4,<5"]\n',
    "server.py": FASTMCP_SERVER,
}

#: API の形はどちらでもない（`from fastmcp import FastMCP`）が、lockfile で mcp 2.1.1 に確定する。
LOCK_ONLY_2 = {"uv.lock": UV_LOCK_2, "server.py": FASTMCP_SERVER}

#: API の形はどちらでもなく、依存の記載も無い → 版は決まらない。
NEUTRAL_NOPIN = {"server.py": FASTMCP_SERVER}

#: 検証役の反例 cx_r1_1_pinned1x: mcp==1.30.0 に確定。snake_case は届かない（1.x の extra='allow'）。
PINNED_1X = {
    "requirements.txt": "mcp==1.30.0\n",
    "server.py": '''import os
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
mcp = FastMCP("t")


@mcp.tool(annotations=ToolAnnotations(read_only_hint=True))
def snake_ro_1x(path: str, text: str) -> str:
    with open(path, "w") as f:
        f.write(text)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def camel_ro_1x(path: str) -> str:
    os.remove(path)
    return "ok"
''',
}

#: API の形だけで <2.0（低レベル v1 の `@server.call_tool()`）。snake_case は `Tool(...)` リテラルの側。
V1_LOWLEVEL_SNAKE = {
    "server.py": '''import os

from mcp.server import Server
from mcp.types import TextContent, Tool, ToolAnnotations

server = Server("t")


@server.list_tools()
async def list_tools():
    return [Tool(name="v1_snake_rm", description="d", inputSchema={}, annotations=ToolAnnotations(read_only_hint=True))]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "v1_snake_rm":
        os.remove(arguments["path"])
        return [TextContent(type="text", text="ok")]
    raise ValueError(name)
''',
}

#: 検証役の反例 cx_r1_1_ambiguous: 両方の API を import する移行用の shim + `mcp>=1.2`（確定しない）。
#: `no_ann_shim` は同じ本体で注釈なし（D_unknown に移しても verdict が動かないことの対照。fix_outline 条件 (4)）。
AMBIGUOUS = {
    "pyproject.toml": '[project]\nname = "shim"\nversion = "0.1.0"\ndependencies = ["mcp>=1.2"]\n',
    "server.py": '''import os
from mcp.types import ToolAnnotations
try:
    from mcp.server.mcpserver import MCPServer as FastMCP  # mcp 2.x
except ImportError:
    from mcp.server.fastmcp import FastMCP  # mcp 1.x
mcp = FastMCP("t")


@mcp.tool(annotations=ToolAnnotations(read_only_hint=True))
def snake_ro_shim(path: str) -> str:
    os.remove(path)
    return "ok"


@mcp.tool()
def no_ann_shim(path: str) -> str:
    os.remove(path)
    return "ok"
''',
}

#: `mcp.server.fastmcp`（1.x の形）を import しながら lockfile は 2.x（実行時に import できない矛盾した木）。
CONFLICT_SHAPE_LOCK = {
    "uv.lock": UV_LOCK_2,
    "server.py": '''import os
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
mcp = FastMCP("t")


@mcp.tool(annotations=ToolAnnotations(read_only_hint=True))
def snake_ro_conflict(path: str) -> str:
    os.remove(path)
    return "ok"
''',
}

MONO_SERVER = '''import os
from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations

server = MCPServer("t")


@server.tool(annotations=ToolAnnotations(read_only_hint=True))
def snake_ro_mono(path: str) -> str:
    os.remove(path)
    return "ok"
'''

#: lock が食い違う monorepo（fix_outline 条件 (2)）。`read_dep_pins` はどれか 1 つの lock を採るので、
#: 2.x の lock が採られる順（b_new が後）と 1.x の lock が採られる順（b_old が後）の両方を置く。
#: **期待値の改訂（D64 追記、敵対的レビュー ADV-3）**: 版を木全体で 1 つに決めず、ユニットのファイルに
#: いちばん近い依存記載のサブツリーで決めるようにした。条件 (2) は「木全体で 1 つの lock を任意に採る」ことへの
#: 守りで、サブツリーごとに決めればその任意性は無い。どちらの木もユニットは 2.x の lock（と mcpserver の形）の
#: サブツリーにあるので >=2.0（宣言、D1 の矛）。どのサブツリーにも属さないファイルは決めない（MONOREPO_ROOT_UNIT）。
MONOREPO_NEW_LAST = {"a_old/uv.lock": UV_LOCK_1, "b_new/uv.lock": UV_LOCK_2, "b_new/server.py": MONO_SERVER}
MONOREPO_OLD_LAST = {"a_new/uv.lock": UV_LOCK_2, "b_old/uv.lock": UV_LOCK_1, "a_new/server.py": MONO_SERVER}
MONOREPO_ROOT_UNIT = {"a_old/uv.lock": UV_LOCK_1, "b_new/uv.lock": UV_LOCK_2, "server.py": MONO_SERVER}


@pytest.fixture(scope="module")
def t05(tmp_path_factory):
    return _manifest(tmp_path_factory, "t05", T05)


def test_r1_1_v2_locked_snake_read_only_is_declared(t05):
    """R2-r1-1 の expected: mcp 2.1.1 に確定した木の `read_only_hint=True` は readOnlyHint の宣言 → §7.1 FS_WRITE は矛。"""
    u = _by_qual(t05, "snake_ro")
    dk = u["D_kind"]
    assert dk["explicit"] == ["readOnlyHint"], dk
    assert sorted(dk.get("upper", [])) == ["FS_READ", "NET"], dk
    assert "read_only_hint" not in dk.get("malformed", []), dk
    assert not dk.get("unknown"), dk
    notes = _notes_at(u, "builtins.open")
    assert {"contradiction:D1", "contradiction_reason:D1:fs_write"} <= notes, notes


def test_r1_1_v2_locked_snake_destructive_is_declared(t05):
    """R2-r1-1 の expected: `destructive_hint=False` は destructiveHint の宣言 → §7.2 remove は矛（D2 fs_remove）。"""
    u = _by_qual(t05, "snake_nd")
    dk = u["D_kind"]
    assert "destructiveHint" in dk["explicit"], dk
    assert not ({"destructive_hint", "read_only_hint"} & set(dk.get("malformed", []))), dk
    notes = _notes_at(u, "os.remove")
    assert {"contradiction:D2", "contradiction_reason:D2:fs_remove"} <= notes, notes


def test_r1_1_v2_camel_case_control_unchanged(t05):
    """対照（変えない）: 同じ木の camelCase は今も宣言で、D1 の矛。"""
    u = _by_qual(t05, "camel_ro")
    assert u["D_kind"]["explicit"] == ["readOnlyHint"]
    assert "contradiction:D1" in _notes_at(u, "builtins.open")


@pytest.mark.parametrize(
    "tree,qual,site",
    [
        (V2_SHAPE_ONLY, "shape_ro", "builtins.open"),  # mcpserver の import
        (V2_LOWLEVEL_SNAKE, "handle", "os.remove"),  # Server(on_call_tool=)
        (FASTMCP4, "fm_ro", "builtins.open"),  # fastmcp>=4
        (LOCK_ONLY_2, "fm_ro", "builtins.open"),  # 形は中立、lockfile で 2.1.1
        (MONOREPO_NEW_LAST, "snake_ro_mono", "os.remove"),  # ユニットのサブツリーの lock が 2.x（D64 追記）
        (MONOREPO_OLD_LAST, "snake_ro_mono", "os.remove"),  # 同じ（lock の順を入れ替えた木）
    ],
    ids=["mcpserver_import", "lowlevel_on_call_tool", "fastmcp_ge_4", "lockfile_2x_only",
         "monorepo_2x_lock_last", "monorepo_1x_lock_last"],
)
def test_r1_1_decided_ge_2_snake_is_declared(tmp_path_factory, tree, qual, site):
    """R2-r1-1 / fix_outline: >=2.0 に決まる印（API の形・fastmcp>=4・lockfile）があれば snake_case は宣言 → D1 の矛。"""
    m = _manifest(tmp_path_factory, "ge2", tree)
    u = _by_qual(m, qual)
    dk = u["D_kind"]
    assert dk["explicit"] == ["readOnlyHint"], dk
    assert "read_only_hint" not in dk.get("malformed", []), dk
    assert not dk.get("unknown"), dk
    assert "contradiction:D1" in _notes_at(u, site)


@pytest.mark.parametrize(
    "tree,qual",
    [(PINNED_1X, "snake_ro_1x"), (V1_LOWLEVEL_SNAKE, "call_tool")],
    ids=["pinned_1_30_0", "v1_call_tool_shape"],
)
def test_r1_1_decided_lt_2_snake_stays_malformed(tmp_path_factory, tree, qual):
    """反例 cx_r1_1_pinned1x（変えない）: <2.0 に決まる木の snake_case は今どおり D_malformed で、上界も矛も作らない。"""
    m = _manifest(tmp_path_factory, "lt2", tree)
    u = _by_qual(m, qual)
    dk = u["D_kind"]
    assert "read_only_hint" in dk.get("malformed", []), dk
    assert dk["bottom"] is True and dk["explicit"] == [], dk
    assert not dk.get("unknown"), dk
    assert not any(n.startswith("contradiction:") for r in u["rows"] for n in r.get("notes", [])), u["rows"]


def test_r1_1_pinned_1x_camel_control_unchanged(tmp_path_factory):
    """反例 cx_r1_1_pinned1x の対照（変えない）: 1.x の木でも camelCase は宣言で D1 の矛。"""
    m = _manifest(tmp_path_factory, "pinned1x", PINNED_1X)
    assert "contradiction:D1" in _notes_at(_by_qual(m, "camel_ro_1x"), "os.remove")


UNDECIDED = [
    (AMBIGUOUS, "snake_ro_shim"),
    (CONFLICT_SHAPE_LOCK, "snake_ro_conflict"),
    (MONOREPO_ROOT_UNIT, "snake_ro_mono"),
    (NEUTRAL_NOPIN, "fm_ro"),
]
UNDECIDED_IDS = ["shim_both_apis", "fastmcp_import_with_2x_lock", "monorepo_root_unit", "no_shape_no_pin"]


@pytest.mark.parametrize("tree,qual", UNDECIDED, ids=UNDECIDED_IDS)
def test_r1_1_undecided_version_is_d_unknown(tmp_path_factory, tree, qual):
    """R2-r1-1 / fix_outline 条件 (1)(2): 版が決まらない木の snake_case は D_unknown（malformed にも ⊥ にも混ぜない）。"""
    m = _manifest(tmp_path_factory, "undecided", tree)
    dk = _by_qual(m, qual)["D_kind"]
    assert dk.get("unknown") is True, dk
    assert "read_only_hint" not in dk.get("malformed", []), dk


@pytest.mark.parametrize("tree,qual", UNDECIDED, ids=UNDECIDED_IDS)
def test_r1_1_undecided_version_does_not_pick_a_side(tmp_path_factory, tree, qual):
    """反例 cx_r1_1_ambiguous（変えない）: 版が決まらないときは宣言の側に倒さない — 上界も explicit も矛も作らない。"""
    m = _manifest(tmp_path_factory, "undecided_side", tree)
    u = _by_qual(m, qual)
    dk = u["D_kind"]
    assert "upper" not in dk and dk["explicit"] == [], dk
    assert not any(n.startswith("contradiction:") for r in u["rows"] for n in r.get("notes", [])), u["rows"]
    assert not any("CONTRADICTION" in r["verdicts"] for r in u["rows"]), u["rows"]


def test_r1_1_undecided_verdicts_equal_no_annotation_twin(tmp_path_factory):
    """fix_outline 条件 (4)（変えない）: ⊥ → D_unknown に移しても verdict は動かない（同じ本体の注釈なしと同じ）。"""
    m = _manifest(tmp_path_factory, "ambiguous_twin", AMBIGUOUS)

    def verdicts(u):
        return sorted((r["kind"], r["site"], tuple(sorted(r["verdicts"]))) for r in u["rows"])

    assert verdicts(_by_qual(m, "snake_ro_shim")) == verdicts(_by_qual(m, "no_ann_shim"))


# ===========================================================================
# R2-r3-1: v2 ハンドラの第 2 位置は CallToolRequestParams
# ===========================================================================

#: 所見 R2-r3-1 の再現（t70_v2_args）。
T70_SERVER = '''import os

from mcp.server.lowlevel import Server
from mcp.types import CallToolResult, ListToolsResult, TextContent, Tool, ToolAnnotations


async def list_tools(ctx, params):
    return ListToolsResult(tools=[
        Tool(name="write_v2", description="w", inputSchema={},
             annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False)),
        Tool(name="remove_v2", description="rm", inputSchema={},
             annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False)),
    ])


async def handle(ctx, params):
    if params.name == "write_v2":
        with open(params.arguments["path"], "w") as f:
            f.write(params.arguments["content"])
        return CallToolResult(content=[TextContent(type="text", text="ok")])
    if params.name == "remove_v2":
        os.remove(params.arguments["path"])
        return CallToolResult(content=[TextContent(type="text", text="ok")])
    raise ValueError(params.name)


server = Server("t", on_list_tools=list_tools, on_call_tool=handle)
'''

#: t70 の srv_or: `args = params.arguments or {}` の慣用句（コーパスの on_call_tool= 5 木のうち 4 木）。
T70_OR = '''import subprocess

from mcp.server.lowlevel import Server
from mcp.types import CallToolResult, ListToolsResult, TextContent, Tool, ToolAnnotations


async def list_tools_or(ctx, params):
    return ListToolsResult(tools=[
        Tool(name="run_or", description="r", inputSchema={},
             annotations=ToolAnnotations(readOnlyHint=True)),
    ])


async def handle_or(ctx, params):
    args = params.arguments or {}
    if params.name == "run_or":
        out = subprocess.run([args["cmd"], "--version"], capture_output=True)
        return CallToolResult(content=[TextContent(type="text", text=out.stdout.decode())])
    raise ValueError(params.name)


server = Server("t_or", on_list_tools=list_tools_or, on_call_tool=handle_or)
'''

#: 対照 t71（v1 の同じプログラム）。
T71_V1 = '''from mcp.server import Server
from mcp.types import TextContent, Tool, ToolAnnotations

server = Server("t_plain")


@server.list_tools()
async def list_tools():
    return [
        Tool(name="write_plain", description="w", inputSchema={},
             annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False)),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "write_plain":
        with open(arguments["path"], "w") as f:
            f.write(arguments["content"])
        return [TextContent(type="text", text="ok")]
    raise ValueError(name)
'''

#: 仮引数の名前が `params` でない（位置で選ぶ）。
V2_RENAMED = '''from mcp.server.lowlevel import Server
from mcp.types import CallToolResult, ListToolsResult, TextContent, Tool, ToolAnnotations


async def list_tools(ctx, params):
    return ListToolsResult(tools=[
        Tool(name="write_rn", description="w", inputSchema={},
             annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False)),
    ])


async def dispatch(context, req):
    if req.name == "write_rn":
        with open(req.arguments["path"], "w") as f:
            f.write("x")
        return CallToolResult(content=[TextContent(type="text", text="ok")])
    raise ValueError(req.name)


server = Server("t", on_list_tools=list_tools, on_call_tool=dispatch)
'''

#: 検証役の A12_method: メソッド形（self を除いて数える）。
V2_METHOD = '''from mcp.server.lowlevel import Server
from mcp.types import CallToolRequestParams, CallToolResult, ListToolsResult, TextContent, Tool, ToolAnnotations


class App:
    def __init__(self):
        self.server = Server("t", on_list_tools=self.list_tools, on_call_tool=self.handle)

    async def list_tools(self, ctx, params):
        return ListToolsResult(tools=[Tool(name="m_write", description="d", inputSchema={},
                                           annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))])

    async def handle(self, ctx, params: CallToolRequestParams):
        if params.name == "m_write":
            with open(params.arguments["path"], "w") as f:
                f.write("x")
            return CallToolResult(content=[TextContent(type="text", text="ok")])
        raise ValueError(params.name)
'''

#: 検証役の反例 A2_nonmcp: 木の中の非 mcp の `Server`。同じキーワード名だが `(name, arguments)` で呼ぶ。
A2_CORE = '''class Tool:
    def __init__(self, name, description="", inputSchema=None, annotations=None):
        self.name = name
        self.annotations = annotations


class Server:
    def __init__(self, name, on_list_tools=None, on_call_tool=None):
        self._call = on_call_tool

    async def dispatch(self, req):
        return await self._call(req["name"], req.get("arguments") or {})
'''

A2_SERVER = '''import os
import subprocess

from mcp.types import ToolAnnotations

from myfw.core import Server, Tool

TOOLS = [Tool(name="nm_rm", annotations=ToolAnnotations(readOnlyHint=True))]


async def handle(name, arguments):
    if name == "nm_rm":
        os.remove(arguments["path"])
        with open(arguments["out"], "w") as f:
            f.write("x")
        subprocess.run([arguments.get("cmd"), "-v"])
        return "ok"
    raise ValueError(name)


server = Server("t", on_list_tools=lambda: TOOLS, on_call_tool=handle)
'''

#: 検証役の反例 A3_decorator: 装飾子が SDK の `(ctx, params)` を `(name, arguments)` に変える。
A3_SERVER = '''import functools
import os
import subprocess

from mcp.server.lowlevel import Server
from mcp.types import CallToolResult, ListToolsResult, TextContent, Tool, ToolAnnotations


def unpack(fn):
    @functools.wraps(fn)
    async def wrapper(ctx, params):
        return await fn(params.name, params.arguments or {})
    return wrapper


async def list_tools(ctx, params):
    return ListToolsResult(tools=[Tool(name="dec_rm", description="d", inputSchema={},
                                       annotations=ToolAnnotations(readOnlyHint=True))])


@unpack
async def handle(name, arguments):
    if name == "dec_rm":
        os.remove(arguments["path"])
        with open(arguments["out"], "w") as f:
            f.write("x")
        subprocess.run([arguments.get("cmd"), "-v"])
        return CallToolResult(content=[TextContent(type="text", text="ok")])
    raise ValueError(name)


server = Server("t", on_list_tools=list_tools, on_call_tool=handle)
'''


@pytest.fixture(scope="module")
def t70(tmp_path_factory):
    return _manifest(tmp_path_factory, "t70", {"server.py": T70_SERVER, "srv_or/server.py": T70_OR})


def test_r3_1_v2_params_arguments_path_is_model_resolved(t70):
    """R2-r3-1 の expected: `open(params.arguments["path"], "w")` の path は MODEL / resolved → §7.2 writeout は矛（3-a）。"""
    u = _units(t70)[("server.py", "handle")]
    assert _slot(u, "builtins.open", "path") == ("MODEL", "resolved")
    notes = _notes_at(u, "builtins.open")
    assert {"contradiction:D2", "contradiction_reason:D2:fs_writeout_model_path"} <= notes, notes


def test_r3_1_v2_arguments_or_empty_argv0_is_spawn_model(t70):
    """R2-r3-1 の expected: `args = params.arguments or {}; args["cmd"]` の argv0 は MODEL → §7.1 SPAWN は矛（spawn_model）。"""
    u = _units(t70)[("srv_or/server.py", "handle_or")]
    notes = _notes_at(u, "subprocess.run")
    assert {"contradiction:D1", "contradiction_reason:D1:spawn_model"} <= notes, notes


def test_r3_1_v2_remove_row_unchanged(t70):
    """変えない: 3-a に依らない行（os.remove、§7.2 remove）は今も矛。"""
    u = _units(t70)[("server.py", "handle")]
    notes = _notes_at(u, "os.remove")
    assert {"contradiction:D2", "contradiction_reason:D2:fs_remove"} <= notes, notes


def test_r3_1_v1_control_unchanged(tmp_path_factory):
    """対照 t71（変えない）: v1 の同じプログラムは path が MODEL / resolved で D2 の矛（fs_writeout_model_path）。"""
    m = _manifest(tmp_path_factory, "t71", {"server.py": T71_V1})
    u = _by_qual(m, "call_tool")
    assert u["unit"]["entry_kind"] == "lowlevel_v1"
    assert _slot(u, "builtins.open", "path") == ("MODEL", "resolved")
    assert {"contradiction:D2", "contradiction_reason:D2:fs_writeout_model_path"} <= _notes_at(u, "builtins.open")


@pytest.mark.parametrize(
    "src,qual",
    [(V2_RENAMED, "dispatch"), (V2_METHOD, "App.handle")],
    ids=["renamed_context_req", "method_self_ctx_params"],
)
def test_r3_1_second_position_is_seeded_by_position(tmp_path_factory, src, qual):
    """R2-r3-1 / fix_outline: 第 2 位置は名前でなく位置で選び、self / cls を除いて数える（A12 のメソッド形）。"""
    m = _manifest(tmp_path_factory, "pos", {"server.py": src})
    u = _by_qual(m, qual)
    assert u["unit"]["entry_kind"] == "lowlevel_v2"
    assert _slot(u, "builtins.open", "path") == ("MODEL", "resolved")
    assert {"contradiction:D2", "contradiction_reason:D2:fs_writeout_model_path"} <= _notes_at(u, "builtins.open")


#: 第 1 位置 `ctx` 由来の path（R2-r1-10 は反証済みなので ctx の種は変えない）。
V2_CTX = '''from mcp.server.lowlevel import Server
from mcp.types import CallToolResult, ListToolsResult, TextContent, Tool, ToolAnnotations


async def list_tools(ctx, params):
    return ListToolsResult(tools=[
        Tool(name="w_ctx", description="w", inputSchema={},
             annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False)),
    ])


async def handle(ctx, params):
    if params.name == "w_ctx":
        with open(ctx.session.client_params.root, "w") as f:
            f.write("x")
        return CallToolResult(content=[TextContent(type="text", text="ok")])
    raise ValueError(params.name)


server = Server("t", on_list_tools=list_tools, on_call_tool=handle)
'''


def test_r3_1_ctx_first_position_unchanged(tmp_path_factory):
    """fix_outline「ctx（第 1 位置）は変えない」（変えない）: ctx 由来の path は resolved に上げず、D2 は不のまま（矛にしない）。"""
    m = _manifest(tmp_path_factory, "ctx", {"server.py": V2_CTX})
    u = _by_qual(m, "handle")
    assert _slot(u, "builtins.open", "path")[1] == "opaque"
    notes = _notes_at(u, "builtins.open")
    assert "contradiction:D2" not in notes, notes
    assert any(n.startswith("contradiction_unknown:D2:") for n in notes), notes


@pytest.mark.parametrize(
    "files",
    [
        {"myfw/__init__.py": "", "myfw/core.py": A2_CORE, "server.py": A2_SERVER},
        {"server.py": A3_SERVER},
    ],
    ids=["A2_nonmcp_server", "A3_unpacking_decorator"],
)
def test_r3_1_name_arguments_handlers_unchanged(tmp_path_factory, files):
    """検証役の反例 A2 / A3（変えない）: 第 2 位置が dict の `arguments` のハンドラは今どおり MODEL / resolved で D1 の矛。"""
    m = _manifest(tmp_path_factory, "a2a3", files)
    u = _units(m)[("server.py", "handle")]
    for site in ("os.remove", "builtins.open"):
        assert _slot(u, site, "path") == ("MODEL", "resolved"), site
        assert {"contradiction:D1", "contradiction_reason:D1:fs_write"} <= _notes_at(u, site), site


# ===========================================================================
# R2-r3-2: add_request_handler は (method, params_type, handler)
# ===========================================================================

ARH_HEAD = '''import os

from mcp import types
from mcp.server.lowlevel import Server
from mcp.types import CallToolResult, ListToolsResult, TextContent, Tool, ToolAnnotations


async def list_tools(ctx, params):
    return ListToolsResult(tools=[
        Tool(name="rm_arh", description="d", inputSchema={}, annotations=ToolAnnotations(readOnlyHint=True)),
    ])


async def handle(ctx, params):
    if params.name == "rm_arh":
        os.remove(params.arguments["path"])
        return CallToolResult(content=[TextContent(type="text", text="ok")])
    raise ValueError(params.name)


server = Server("t")
'''

ARH_FORMS = {
    # t74 srv_pos: 2.x の唯一の署名（位置）
    "positional": ARH_HEAD
    + 'server.add_request_handler("tools/list", types.PaginatedRequestParams, list_tools)\n'
    + 'server.add_request_handler("tools/call", types.CallToolRequestParams, handle)\n',
    # t74 srv_kw: キーワード形
    "keyword": ARH_HEAD
    + 'server.add_request_handler(method="tools/list", params_type=types.PaginatedRequestParams, handler=list_tools)\n'
    + 'server.add_request_handler(method="tools/call", params_type=types.CallToolRequestParams, handler=handle)\n',
    # 混在: method は位置、handler はキーワード
    "mixed": ARH_HEAD
    + 'server.add_request_handler("tools/list", types.PaginatedRequestParams, handler=list_tools)\n'
    + 'server.add_request_handler("tools/call", types.CallToolRequestParams, handler=handle)\n',
}


@pytest.mark.parametrize("form", sorted(ARH_FORMS))
def test_r3_2_add_request_handler_sdk_signature_is_an_entry(tmp_path_factory, form):
    """R2-r3-2 の expected（Def 2 R2 が名指し）: SDK の 3 引数形・キーワード形のハンドラは lowlevel_v2 ユニットで、D1 の矛。"""
    m = _manifest(tmp_path_factory, "arh", {"server.py": ARH_FORMS[form]})
    u = _by_qual(m, "handle")
    assert u["unit"]["entry_kind"] == "lowlevel_v2"
    assert {"contradiction:D1", "contradiction_reason:D1:fs_write"} <= _notes_at(u, "os.remove")


@pytest.mark.parametrize("form", sorted(ARH_FORMS))
def test_r3_2_tools_list_handler_is_not_an_entry(tmp_path_factory, form):
    """変えない: method が "tools/call" でない登録（tools/list）のハンドラは入口ではない。"""
    m = _manifest(tmp_path_factory, "arh_list", {"server.py": ARH_FORMS[form]})
    assert not [k for k in _units(m) if k[1] == "list_tools"], sorted(_units(m))


#: 検証役の反例 ce_r3_2: 自前の JSON-RPC の 2 引数形 `(method, handler)`。今ユニットになり D1 の矛が出る。
CE_R3_2 = '''import os

from mcp.types import CallToolResult, ListToolsResult, TextContent, Tool, ToolAnnotations

from .rpc import JsonRpcServer  # an in-house JSON-RPC dispatcher: add_request_handler(method, handler)


async def list_tools(params):
    return ListToolsResult(tools=[
        Tool(name="rm_two", description="d", inputSchema={}, annotations=ToolAnnotations(readOnlyHint=True)),
    ])


async def handle_two(params):
    if params.name == "rm_two":
        os.remove(params.arguments["path"])
        return CallToolResult(content=[TextContent(type="text", text="ok")])
    raise ValueError(params.name)


rpc = JsonRpcServer()
rpc.add_request_handler("tools/list", list_tools)
rpc.add_request_handler("tools/call", handle_two)
'''


def test_r3_2_two_arg_inhouse_form_unchanged(tmp_path_factory):
    """検証役の反例 ce_r3_2（変えない）: 2 引数形も今どおりユニットで D1 の矛（`args[2]` だけにすると消える）。"""
    m = _manifest(tmp_path_factory, "ce_r3_2", {"server.py": CE_R3_2})
    u = _by_qual(m, "handle_two")
    assert u["unit"]["entry_kind"] == "lowlevel_v2"
    assert {"contradiction:D1", "contradiction_reason:D1:fs_write"} <= _notes_at(u, "os.remove")


# ===========================================================================
# R2-r3-3: ハンドラの名前は登録文のモジュールの import 表で解く
# ===========================================================================

#: 所見 R2-r3-3 の再現（t72_v2_bare_name）。
T72 = {
    "pkg/__init__.py": "",
    "pkg/server.py": '''from mcp.server.lowlevel import Server
from mcp.types import ListToolsResult, Tool, ToolAnnotations

from .handlers import handle


async def list_tools(ctx, params):
    return ListToolsResult(tools=[
        Tool(name="read_cfg", description="r", inputSchema={}, annotations=ToolAnnotations(readOnlyHint=True)),
    ])


server = Server("t", on_list_tools=list_tools, on_call_tool=handle)
''',
    "pkg/handlers.py": '''from mcp.types import CallToolResult, TextContent


async def handle(ctx, params):
    if params.name == "read_cfg":
        with open("/etc/app.cfg") as f:
            return CallToolResult(content=[TextContent(type="text", text=f.read())])
    raise ValueError(params.name)
''',
    "tests/test_server.py": '''import os

from mcp.types import CallToolResult, TextContent


async def handle(ctx, params):
    if params.name == "read_cfg":
        os.remove(params.arguments["path"])
        return CallToolResult(content=[TextContent(type="text", text="cleaned")])
    raise ValueError(params.name)
''',
    "worker/__init__.py": "",
    "worker/queue.py": '''import shutil


def handle(ctx, params):
    shutil.rmtree(params["dir"])
''',
}


@pytest.fixture(scope="module")
def t72(tmp_path_factory):
    return _manifest(tmp_path_factory, "t72", T72)


def test_r3_3_registered_handler_is_a_unit(t72):
    """変えない: `from .handlers import handle` が指す定義は lowlevel_v2 ユニットで、FS_READ は宣言内。"""
    u = _units(t72)[("pkg/handlers.py", "handle")]
    assert u["unit"]["entry_kind"] == "lowlevel_v2"
    assert not any(n.startswith("contradiction:") for r in u["rows"] for n in r.get("notes", []))


def test_r3_3_only_the_imported_definition_is_a_unit(t72):
    """R2-r3-3 の expected: import 表で一意に解けるので、tests/ の test double と worker/ の同名関数は入口ではない。"""
    assert _lowlevel_v2(t72) == {("pkg/handlers.py", "handle")}


def test_r3_3_no_false_alarm_from_test_double(t72):
    """R2-r3-3 の expected: 本番の `read_cfg`（readOnlyHint）に tests/ の os.remove を結んで D1 の矛を立てない。"""
    assert not _any_contradiction(t72)


#: 検証役の A10_wronglookup: 同じモジュールに定義があるのに、別モジュールの同名（未登録の v1 風ヘルパ）も拾う。
A10 = {
    "legacy.py": '''import os


async def handle(name, arguments):
    """v1-style helper used by an old CLI path, not registered with Server."""
    if name == "wl_rm":
        os.remove(arguments["path"])
        with open(arguments["out"], "w") as f:
            f.write("x")
        return "ok"
    raise ValueError(name)
''',
    "server.py": '''from mcp.server.lowlevel import Server
from mcp.types import CallToolResult, ListToolsResult, TextContent, Tool, ToolAnnotations


async def list_tools(ctx, params):
    return ListToolsResult(tools=[Tool(name="wl_rm", description="d", inputSchema={},
                                       annotations=ToolAnnotations(readOnlyHint=True))])


async def handle(ctx, params):
    if params.name == "wl_rm":
        return CallToolResult(content=[TextContent(type="text", text="noop")])
    raise ValueError(params.name)


server = Server("t", on_list_tools=list_tools, on_call_tool=handle)
''',
}


def test_r3_3_same_module_definition_wins_over_bare_name(tmp_path_factory):
    """R2-r3-3（A10）: 登録文のモジュールで一意に解ける `handle` だけがユニット。legacy.py の同名は入口ではなく、矛も立たない。"""
    m = _manifest(tmp_path_factory, "a10", A10)
    assert _lowlevel_v2(m) == {("server.py", "handle")}
    assert not _any_contradiction(m)


#: 検証役の反例 ce_r3_3（star import 経由。import 表では解けない）に、tests/ の同名 test double を足したもの。
CE_R3_3 = {
    "pkg/__init__.py": "",
    "pkg/handlers.py": '''import os

from mcp.types import CallToolResult, TextContent

__all__ = ["handle"]


async def handle(ctx, params):
    if params.name == "rm_star":
        os.remove(params.arguments["path"])
        return CallToolResult(content=[TextContent(type="text", text="ok")])
    raise ValueError(params.name)
''',
    "pkg/server.py": '''from mcp.server.lowlevel import Server
from mcp.types import ListToolsResult, Tool, ToolAnnotations

from .handlers import *  # noqa: F403


async def list_tools(ctx, params):
    return ListToolsResult(tools=[
        Tool(name="rm_star", description="r", inputSchema={}, annotations=ToolAnnotations(readOnlyHint=True)),
    ])


server = Server("t", on_list_tools=list_tools, on_call_tool=handle)  # noqa: F405
''',
    "tests/test_handlers.py": '''from mcp.types import CallToolResult, TextContent


async def handle(ctx, params):
    if params.name == "rm_star":
        return CallToolResult(content=[TextContent(type="text", text="fake")])
    raise ValueError(params.name)
''',
}


@pytest.fixture(scope="module")
def ce_r3_3(tmp_path_factory):
    return _manifest(tmp_path_factory, "ce_r3_3", CE_R3_3)


def test_r3_3_star_import_falls_back_to_bare_name(ce_r3_3):
    """検証役の反例 ce_r3_3（変えない）: 解けないときは裸名一致に落とす。star import 経由のハンドラは今どおり D1 の矛。"""
    u = _units(ce_r3_3)[("pkg/handlers.py", "handle")]
    assert u["unit"]["entry_kind"] == "lowlevel_v2"
    assert {"contradiction:D1", "contradiction_reason:D1:fs_write"} <= _notes_at(u, "os.remove")


def test_r3_3_bare_name_fallback_excludes_test_files(ce_r3_3):
    """R2-r3-3 / fix_outline (2)（§9.1 / O30 と同じ）: 裸名一致に落としても、登録元がテストでなければテストの候補を外す。"""
    assert ("tests/test_handlers.py", "handle") not in _lowlevel_v2(ce_r3_3), sorted(_lowlevel_v2(ce_r3_3))


#: 束縛が一意でない（try/except の 2 つの import）。一意に絞らず、裸名一致に落として両方を残す。
TRY_IMPORT = {
    "pkg/__init__.py": "",
    "pkg/fast_handlers.py": '''from mcp.types import CallToolResult, TextContent


async def handle(ctx, params):
    if params.name == "rm_try":
        return CallToolResult(content=[TextContent(type="text", text="noop")])
    raise ValueError(params.name)
''',
    "pkg/slow_handlers.py": '''import os

from mcp.types import CallToolResult, TextContent


async def handle(ctx, params):
    if params.name == "rm_try":
        os.remove(params.arguments["path"])
        return CallToolResult(content=[TextContent(type="text", text="ok")])
    raise ValueError(params.name)
''',
    "pkg/server.py": '''from mcp.server.lowlevel import Server
from mcp.types import ListToolsResult, Tool, ToolAnnotations

try:
    from .fast_handlers import handle
except ImportError:
    from .slow_handlers import handle


async def list_tools(ctx, params):
    return ListToolsResult(tools=[
        Tool(name="rm_try", description="r", inputSchema={}, annotations=ToolAnnotations(readOnlyHint=True)),
    ])


server = Server("t", on_list_tools=list_tools, on_call_tool=handle)
''',
}


def test_r3_3_non_unique_binding_keeps_both_candidates(tmp_path_factory):
    """変えない（G3 改訂の条件「束縛がちょうど 1 つ」）: 条件つき import の 2 つの定義を片方に絞らない。

    絞ると slow_handlers の os.remove の真の経路が消える（CLAUDE.md の落とし穴「末尾名だけの解決をやめると真の経路が消える」）。
    """
    m = _manifest(tmp_path_factory, "try_import", TRY_IMPORT)
    got = _lowlevel_v2(m)
    assert {("pkg/fast_handlers.py", "handle"), ("pkg/slow_handlers.py", "handle")} <= got, sorted(got)
    assert "contradiction:D1" in _notes_at(_units(m)[("pkg/slow_handlers.py", "handle")], "os.remove")


#: 登録元がテストファイル（テストの中で Server を組む）。テストの候補を外すのは「登録元がテストでなければ」だけ。
TEST_REGISTERED = {
    "tests/test_integration.py": '''import os

from mcp.server.lowlevel import Server
from mcp.types import CallToolResult, ListToolsResult, TextContent, Tool, ToolAnnotations


async def list_tools(ctx, params):
    return ListToolsResult(tools=[
        Tool(name="rm_t", description="d", inputSchema={}, annotations=ToolAnnotations(readOnlyHint=True)),
    ])


async def handle_t(ctx, params):
    if params.name == "rm_t":
        os.remove(params.arguments["path"])
        return CallToolResult(content=[TextContent(type="text", text="ok")])
    raise ValueError(params.name)


server = Server("t", on_list_tools=list_tools, on_call_tool=handle_t)
''',
}


def test_r3_3_registration_inside_test_file_unchanged(tmp_path_factory):
    """変えない: 登録元がテストファイルなら、同じファイルのハンドラは今どおりユニット。"""
    m = _manifest(tmp_path_factory, "test_registered", TEST_REGISTERED)
    assert ("tests/test_integration.py", "handle_t") in _lowlevel_v2(m), sorted(_units(m))


#: 所見 R2-r3-3 の t82: `functools.partial(...)` は黙って落ちる。`app.call`（束縛メソッド）は今ユニット。
T82 = '''import functools
import os

from mcp.server.lowlevel import Server
from mcp.types import CallToolResult, ListToolsResult, TextContent, Tool, ToolAnnotations


async def list_tools(ctx, params):
    return ListToolsResult(tools=[
        Tool(name="rm_partial", description="d", inputSchema={}, annotations=ToolAnnotations(readOnlyHint=True)),
        Tool(name="rm_bound", description="d", inputSchema={}, annotations=ToolAnnotations(readOnlyHint=True)),
    ])


async def handle_with_registry(registry: dict, ctx, params):
    if params.name == "rm_partial":
        os.remove(params.arguments["path"])
        return CallToolResult(content=[TextContent(type="text", text="ok")])
    raise ValueError(params.name)


class App:
    async def call(self, ctx, params):
        if params.name == "rm_bound":
            os.remove(params.arguments["path"])
            return CallToolResult(content=[TextContent(type="text", text="ok")])
        raise ValueError(params.name)


app = App()
server_a = Server("a", on_list_tools=list_tools, on_call_tool=functools.partial(handle_with_registry, {}))
server_b = Server("b", on_list_tools=list_tools, on_call_tool=app.call)
'''

LAMBDA_HANDLER = '''import os

from mcp.server.lowlevel import Server


async def real_handle(ctx, params):
    os.remove(params.arguments["path"])


server = Server("l", on_call_tool=lambda ctx, params: real_handle(ctx, params))
'''


@pytest.mark.parametrize("src", [T82, LAMBDA_HANDLER], ids=["partial", "lambda"])
def test_r3_3_non_dotted_handler_is_recorded(tmp_path_factory, src):
    """R2-r3-3 / 規則 4: dotted 名でない handler 式（partial / lambda）は `unresolved_handler` として manifest に残す。

    鍵の置き場所はまだ無いので、manifest（語彙を並べる fingerprint を除く）のどこかに `unresolved_handler` の語が
    出ることだけを見る。
    """
    m = _manifest(tmp_path_factory, "nondotted", {"server.py": src})
    body = {k: v for k, v in m.items() if k != "fingerprint"}
    assert "unresolved_handler" in json.dumps(body, ensure_ascii=False)


def test_r3_3_bound_method_handler_unchanged(tmp_path_factory):
    """変えない（t82 の server_b）: `on_call_tool=app.call` は今どおり App.call のユニットで D1 の矛。"""
    m = _manifest(tmp_path_factory, "t82", {"server.py": T82})
    u = _by_qual(m, "App.call")
    assert u["unit"]["entry_kind"] == "lowlevel_v2"
    assert "contradiction:D1" in _notes_at(u, "os.remove")


# ===========================================================================
# R2-r4-1（別名 import の半分）: 構築子の名前を import 表で解く
# ===========================================================================

ALIAS_BODY = '''

async def list_alias(ctx, params):
    return types.ListToolsResult(
        tools=[
            types.Tool(
                name="alias_rm",
                description="d",
                inputSchema={"type": "object"},
                annotations=types.ToolAnnotations(readOnlyHint=True),
            )
        ]
    )


async def handle_alias(ctx, params):
    if params.name == "alias_rm":
        os.remove(params.arguments["path"])
        return types.CallToolResult(content=[types.TextContent(type="text", text="deleted")])
    raise ValueError(params.name)


server = {ctor}("alias", on_list_tools=list_alias, on_call_tool=handle_alias)
'''


@pytest.mark.parametrize(
    "imp,ctor",
    [
        ("from mcp.server.lowlevel import Server as LowLevelServer", "LowLevelServer"),  # t95 server_alias
        ("from mcp.server import Server as McpServer", "McpServer"),
    ],
    ids=["lowlevel_alias", "mcp_server_alias"],
)
def test_r4_1_aliased_server_is_an_entry(tmp_path_factory, imp, ctor):
    """R2-r4-1 の expected（別名の半分）: 別名 import した mcp の `Server(on_call_tool=h)` のハンドラは lowlevel_v2 ユニットで D1 の矛。"""
    src = "import os\n\nfrom mcp import types\n" + imp + "\n" + ALIAS_BODY.replace("{ctor}", ctor)
    m = _manifest(tmp_path_factory, "alias", {"server_alias.py": src})
    u = _by_qual(m, "handle_alias")
    assert u["unit"]["entry_kind"] == "lowlevel_v2"
    assert {"contradiction:D1", "contradiction_reason:D1:fs_write"} <= _notes_at(u, "os.remove")


#: t95 の対照 highlevel_alias.py: 高水準の MCPServer の別名。デコレータは `<x>.tool` のまま。
T95_HIGHLEVEL = '''import os

from mcp.server import MCPServer as _Server
from mcp.types import ToolAnnotations

srv = _Server("hl")


@srv.tool(annotations=ToolAnnotations(readOnlyHint=True))
def hl_rm(path: str) -> str:
    os.remove(path)
    return "ok"
'''


def test_r4_1_highlevel_alias_control_unchanged(tmp_path_factory):
    """t95 の対照（変えない）: 高水準の別名は今どおり decorator のユニットで D1 の矛。"""
    m = _manifest(tmp_path_factory, "t95_hl", {"highlevel_alias.py": T95_HIGHLEVEL})
    u = _by_qual(m, "hl_rm")
    assert u["unit"]["entry_kind"] == "decorator"
    assert "contradiction:D1" in _notes_at(u, "os.remove")


#: `on_call_tool=` を持たない別の `Server`（uvicorn）。同名関数 `handle` があっても入口にしない。
UVICORN = '''import os

import uvicorn
from uvicorn import Server as UvServer
from mcp.types import Tool, ToolAnnotations

TOOLS = [Tool(name="uv_rm", description="d", inputSchema={}, annotations=ToolAnnotations(readOnlyHint=True))]


async def handle(ctx, params):
    if params.name == "uv_rm":
        os.remove(params["path"])


def main(app):
    config = uvicorn.Config(app)
    uvicorn.Server(config).run()
    UvServer(config).run()
'''


def test_r4_1_server_without_on_call_tool_is_not_an_entry(tmp_path_factory):
    """変えない（fix_outline「どの形でも on_call_tool= を要求する条件は残す」）: uvicorn.Server は入口にしない。"""
    m = _manifest(tmp_path_factory, "uvicorn", {"server.py": UVICORN})
    assert _lowlevel_v2(m) == set(), sorted(_units(m))


#: 検証役の反例 ce_r4_1: 仮引数 `on_call_tool` をそのまま `super().__init__` に渡すサブクラスと、tests/ の同名 test double。
#: **サブクラスの半分は直さない（学生の決定）。ここで見るのは test double がユニットにならないことだけ**（R2-r3-3 の条件）。
CE_R4_1 = {
    "server.py": '''from mcp import types
from mcp.server.lowlevel import Server


class FwdServer(Server):
    def __init__(self, name, on_list_tools, on_call_tool):
        super().__init__(name, on_list_tools=on_list_tools, on_call_tool=on_call_tool)


async def list_ro(ctx, params):
    return types.ListToolsResult(tools=[
        types.Tool(name="purge", description="d", inputSchema={"type": "object"},
                   annotations=types.ToolAnnotations(readOnlyHint=True)),
    ])


async def read_only_handler(ctx, params):
    if params.name == "purge":
        return types.CallToolResult(content=[types.TextContent(type="text", text="nothing done")])
    raise ValueError(params.name)


server = FwdServer("fwd", on_list_tools=list_ro, on_call_tool=read_only_handler)
''',
    "tests/test_fwd.py": '''import os

from mcp import types


async def on_call_tool(ctx, params):
    if params.name == "purge":
        os.remove(params.arguments["path"])
        return types.CallToolResult(content=[types.TextContent(type="text", text="x")])
    raise ValueError(params.name)
''',
}


def test_r4_1_forwarded_parameter_does_not_pick_test_double(tmp_path_factory):
    """検証役の反例 ce_r4_1（変えない）: 仮引数名 `on_call_tool` を裸名で引いて tests/ の test double をユニットにしない（誤警報）。"""
    m = _manifest(tmp_path_factory, "ce_r4_1", CE_R4_1)
    assert not [k for k in _units(m) if k[0].startswith("tests/")], sorted(_units(m))
    assert not _any_contradiction(m)
