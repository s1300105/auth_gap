"""D64 / U38 の敵対的レビューの所見 U38-ADV-1 / 2 / 3 / 4 / 6 の反例テスト。

**期待値は authgap/ を直す前に書いた（D64 / U38 の敵対的レビュー）。** 再現の木はレビューの木
（scratchpad/d64review/U38/tA・tA2・tB・tD・tF・tG）を最小にしたもの。期待値は所見の expected（Python の意味）と、
D64 の U38 行・`evidence/review/triage.json` の fix_outline・この修正の条件から導いた。件数には合わせない。

- U38-ADV-1（誤 clear）: def の後に実行される `from X import *` は名前を X の定義で上書きする。star import のある
  モジュールでは一意に絞らず、裸名一致に落とす（本物のハンドラのユニットと D1 の矛が残る）。
- U38-ADV-2（誤 clear）: 自前の `(method, handler, X)` の 3 引数形では handler は args[1]。args[1] が mcp の
  `CallToolRequestParams` に解けるときだけ args[-1] を採る。それ以外の 3 引数以上は args[1] と args[-1] の両方を
  候補にし、どちらも関数に解けなければ `unresolved_handler` に数える（規則 4。黙って落とさない）。
- U38-ADV-3（誤警報）: fastmcp 2.x / 3.x は mcp<2 を要求する（PyPI の requires_dist）。fastmcp の lock の版、
  または指定の上限が 4 未満なら lt2 の票。版は木全体で 1 つに決めず、ユニットのファイルから最も近い依存記載の
  あるサブツリーで決める。依存記載が複数のサブプロジェクトに分かれていて、ユニットがどれにも属さなければ unknown。
- U38-ADV-4（誤警報）: requirements のコメントや pyproject の description などの自由文の中の `mcp>=2` は依存の
  指定ではない。requirements*.txt は `#` 以降を落として 1 行 1 要求、pyproject.toml は dependencies /
  optional-dependencies の文字列要素だけを読む。
- U38-ADV-6（誤 clear）: `from pkg import m` は、pkg の `__init__.py` が束縛した属性 m をサブモジュール pkg.m より
  優先する。`__init__.py` が m を束縛していればサブモジュールとみなさない（裸名一致に落とす）。

直さない所見 U38-ADV-5（局所の dict への添字の書き込み。v1 と同じ既存の限界）はテストしない。

記号: 「矛」 = 行の注記に `contradiction:<宣言>`。
"""

from __future__ import annotations

import sys

import pytest

from authgap import enforcement
from authgap.report import manifest_json
from authgap.runner import RunConfig, run


def _write(d, files):
    for rel, src in files.items():
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(src, encoding="utf-8")


def _manifest(tmp_path_factory, name, files):
    d = tmp_path_factory.mktemp(name)
    _write(d, files)
    res = run(RunConfig(src_root=str(d), population="mcp_server", full=True))
    return manifest_json(res, "t")


def _units(m):
    return {(u["unit"]["relpath"], u["unit"]["qualname"]): u for u in m["units"]}


def _lowlevel_v2(m):
    return {(u["unit"]["relpath"], u["unit"]["qualname"]) for u in m["units"] if u["unit"]["entry_kind"] == "lowlevel_v2"}


def _notes_at(u, site):
    rows = [r for r in u["rows"] if r["site"] == site]
    assert rows, f"{u['unit']['qualname']}: {site} の行が無い: {[r['site'] for r in u['rows']]}"
    return {n for r in rows for n in r.get("notes", [])}


def _contradictions(u):
    return sorted(n for r in u["rows"] for n in r.get("notes", []) if n.startswith("contradiction:"))


def _unit(m, relpath, qualname):
    units = _units(m)
    assert (relpath, qualname) in units, f"{relpath}:{qualname} がユニットにならない: {sorted(units)}"
    return units[(relpath, qualname)]


D1_REMOVE = {"contradiction:D1", "contradiction_reason:D1:fs_write"}

#: 本物のハンドラ（readOnlyHint=True の "rm" に os.remove）。
REAL_HANDLER = '''import os

from mcp.types import CallToolResult, TextContent


async def handle(ctx, params):
    if params.name == "rm":
        os.remove(params.arguments["path"])
        return CallToolResult(content=[TextContent(type="text", text="ok")])
    raise ValueError(params.name)
'''

STUB_HANDLER = '''async def handle(ctx, params):
    raise NotImplementedError("stub")
'''

LIST_TOOLS = '''

async def list_tools(ctx, params):
    return ListToolsResult(tools=[
        Tool(name="rm", description="d", inputSchema={}, annotations=ToolAnnotations(readOnlyHint=True)),
    ])
'''

# ===========================================================================
# U38-ADV-1: def の後の star import による上書き
# ===========================================================================

#: レビューの tA: 同じモジュールの既定のスタブを、try の中の star import で被せる。
ADV1_SAME_MODULE = {
    "handlers_impl.py": REAL_HANDLER,
    "server.py": "from mcp.server.lowlevel import Server\nfrom mcp.types import ListToolsResult, Tool, ToolAnnotations\n"
    + LIST_TOOLS
    + '''

async def handle(ctx, params):
    raise NotImplementedError("install the handlers extra")


try:
    from handlers_impl import *  # noqa: F401,F403  (overrides handle)
except ImportError:
    pass

server = Server("t", on_list_tools=list_tools, on_call_tool=handle)
''',
}

#: レビューの tA2: `__init__.py` が `from .base import handle` の後に `from .override import *` を置く。
ADV1_REEXPORT = {
    "handlers/__init__.py": "from .base import handle  # noqa: F401\nfrom .override import *  # noqa: F401,F403\n",
    "handlers/base.py": STUB_HANDLER,
    "handlers/override.py": REAL_HANDLER,
    "server.py": "from handlers import handle\nfrom mcp.server.lowlevel import Server\n"
    "from mcp.types import ListToolsResult, Tool, ToolAnnotations\n"
    + LIST_TOOLS
    + '\n\nserver = Server("t", on_list_tools=list_tools, on_call_tool=handle)\n',
}


def test_adv1_star_import_after_def_keeps_real_handler(tmp_path_factory):
    """U38-ADV-1 の expected: def の後の `from handlers_impl import *` が handle を上書きする。本物のユニットと D1 の矛が残る。"""
    m = _manifest(tmp_path_factory, "adv1_same", ADV1_SAME_MODULE)
    u = _unit(m, "handlers_impl.py", "handle")
    assert u["unit"]["entry_kind"] == "lowlevel_v2"
    assert D1_REMOVE <= _notes_at(u, "os.remove")


def test_adv1_star_reexport_in_package_keeps_real_handler(tmp_path_factory):
    """U38-ADV-1 の expected（tA2）: `__init__.py` の `from .override import *` が base の handle を上書きする。"""
    m = _manifest(tmp_path_factory, "adv1_reexport", ADV1_REEXPORT)
    u = _unit(m, "handlers/override.py", "handle")
    assert u["unit"]["entry_kind"] == "lowlevel_v2"
    assert D1_REMOVE <= _notes_at(u, "os.remove")


def test_adv1_star_fallback_still_excludes_test_doubles(tmp_path_factory):
    """対照（R2-r3-3 の条件、変えない）: star import で裸名一致に落としても、登録元がテストでなければ tests/ の同名は拾わない。"""
    files = dict(ADV1_SAME_MODULE)
    files["tests/test_fake.py"] = STUB_HANDLER
    m = _manifest(tmp_path_factory, "adv1_tests", files)
    assert ("tests/test_fake.py", "handle") not in _lowlevel_v2(m), sorted(_lowlevel_v2(m))
    assert ("handlers_impl.py", "handle") in _lowlevel_v2(m)


def test_adv1_control_without_star_import_stays_narrowed(tmp_path_factory):
    """対照（could_not_break の形、変えない）: star import が無ければ同じモジュールの def に一意に絞る。
    ほかのモジュールの同名（登録されていない）は入口ではなく、矛も立たない。"""
    files = dict(ADV1_SAME_MODULE)
    files["server.py"] = files["server.py"].replace(
        "try:\n    from handlers_impl import *  # noqa: F401,F403  (overrides handle)\nexcept ImportError:\n    pass\n", ""
    )
    assert "import *" not in files["server.py"]
    m = _manifest(tmp_path_factory, "adv1_control", files)
    assert _lowlevel_v2(m) == {("server.py", "handle")}


# ===========================================================================
# U38-ADV-2: 自前の 3 引数形の add_request_handler
# ===========================================================================

INHOUSE_RPC = '''class JsonRpcServer:
    def __init__(self):
        self.handlers = {}

    def add_request_handler(self, method, handler, params_model=None):
        self.handlers[method] = (handler, params_model)
'''

ADV2_HEAD = '''import os

from mcp.types import CallToolRequestParams, CallToolResult, ListToolsResult, TextContent, Tool, ToolAnnotations

from rpc import JsonRpcServer  # in-house dispatcher


async def list_tools(params):
    return ListToolsResult(tools=[
        Tool(name="rm_three", description="d", inputSchema={}, annotations=ToolAnnotations(readOnlyHint=True)),
    ])


async def handle_three(params):
    if params.name == "rm_three":
        os.remove(params.arguments["path"])
        return CallToolResult(content=[TextContent(type="text", text="ok")])
    raise ValueError(params.name)


rpc = JsonRpcServer()
rpc.add_request_handler("tools/list", list_tools)
'''

#: レビューの tD: `(method, handler, params_model)`。
ADV2_HANDLER_FIRST = {
    "rpc.py": INHOUSE_RPC,
    "server.py": ADV2_HEAD + 'rpc.add_request_handler("tools/call", handle_three, CallToolRequestParams)\n',
}


@pytest.mark.parametrize(
    "third",
    ["CallToolRequestParams", "30", "None", "timeout=30"],
    ids=["type_third", "timeout_positional", "none_third", "keyword_extra"],
)
def test_adv2_inhouse_handler_second_is_an_entry(tmp_path_factory, third):
    """U38-ADV-2 の expected: 自前の `(method, handler, X)` の handler は args[1]。ユニットと D1 の矛が残る。"""
    extra = f", {third}"
    files = {
        "rpc.py": INHOUSE_RPC,
        "server.py": ADV2_HEAD + f'rpc.add_request_handler("tools/call", handle_three{extra})\n',
    }
    m = _manifest(tmp_path_factory, "adv2", files)
    u = _unit(m, "server.py", "handle_three")
    assert u["unit"]["entry_kind"] == "lowlevel_v2"
    assert D1_REMOVE <= _notes_at(u, "os.remove")


def test_adv2_inhouse_model_second_handler_last_is_an_entry(tmp_path_factory):
    """U38-ADV-2（両方を候補に）: args[1] が mcp の型でない `(method, model, handler)` の自前形でも handler（args[-1]）は入口。"""
    files = {
        "rpc.py": INHOUSE_RPC.replace("method, handler, params_model=None", "method, params_model, handler"),
        "models.py": "class CallParams:\n    pass\n",
        "server.py": ADV2_HEAD.replace("from rpc import", "from models import CallParams\nfrom rpc import")
        + 'rpc.add_request_handler("tools/call", CallParams, handle_three)\n',
    }
    m = _manifest(tmp_path_factory, "adv2_model_second", files)
    u = _unit(m, "server.py", "handle_three")
    assert D1_REMOVE <= _notes_at(u, "os.remove")


def test_adv2_unresolvable_three_arg_form_is_recorded(tmp_path_factory):
    """U38-ADV-2 / 規則 4: どちらの候補も木の中の関数に解けなければ、黙って落とさず `unresolved_handler` に数える。"""
    files = {
        "rpc.py": INHOUSE_RPC,
        "server.py": ADV2_HEAD.replace("from rpc import JsonRpcServer", "from rpc import JsonRpcServer\nimport extlib")
        + 'rpc.add_request_handler("tools/call", extlib.dispatch_tool, CallToolRequestParams)\n',
    }
    m = _manifest(tmp_path_factory, "adv2_unres", files)
    uh = m["unresolved_handler"]
    assert uh["count"] >= 1, uh
    lines = files["server.py"].splitlines()
    lineno = next(i + 1 for i, ln in enumerate(lines) if "extlib.dispatch_tool" in ln)
    assert any(s["relpath"] == "server.py" and s["lineno"] == lineno for s in uh["sites"]), uh


SDK_ARH = '''import os

from mcp.server.lowlevel import Server
from mcp import types
from mcp.types import CallToolResult, TextContent


async def handle(ctx, params):
    if params.name == "rm":
        os.remove(params.arguments["path"])
        return CallToolResult(content=[TextContent(type="text", text="ok")])
    raise ValueError(params.name)


server = Server("t")
server.add_request_handler("tools/call", types.CallToolRequestParams, handle)
'''


def test_adv2_control_sdk_three_arg_form_unchanged(tmp_path_factory):
    """対照（R2-r3-2、変えない）: args[1] が mcp の `CallToolRequestParams` に解ける SDK 形は args[-1] が handler で、
    SDK の呼び出し規約で種付けされる（第 2 位置が params）。解けなかった登録として数えない。"""
    m = _manifest(tmp_path_factory, "adv2_sdk", {"server.py": SDK_ARH})
    u = _unit(m, "server.py", "handle")
    assert u["unit"]["entry_kind"] == "lowlevel_v2"
    assert u["unit"].get("v2_params_arg") == "params"
    assert m["unresolved_handler"]["count"] == 0, m["unresolved_handler"]


def test_adv2_control_two_arg_form_unchanged(tmp_path_factory):
    """対照（ce_r3_2、変えない）: 自前の 2 引数形 `(method, handler)` は今どおり入口。"""
    files = {"rpc.py": INHOUSE_RPC, "server.py": ADV2_HEAD + 'rpc.add_request_handler("tools/call", handle_three)\n'}
    m = _manifest(tmp_path_factory, "adv2_two", files)
    assert D1_REMOVE <= _notes_at(_unit(m, "server.py", "handle_three"), "os.remove")


# ===========================================================================
# U38-ADV-3: fastmcp 2.x / 3.x は lt2 の票。版はサブツリーごとに決める
# ===========================================================================

FASTMCP_SERVER = '''from fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("legacy")


@mcp.tool(annotations=ToolAnnotations(read_only_hint=True))
def save_note(path: str, text: str) -> str:
    with open(path, "w") as f:
        f.write(text)
    return "ok"
'''

NEW_SERVER = '''from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations

server = MCPServer("new")


@server.tool(annotations=ToolAnnotations(read_only_hint=True))
def new_note(path: str, text: str) -> str:
    with open(path, "w") as f:
        f.write(text)
    return "ok"
'''

#: レビューの tB（new_server に snake_case のツールを足したもの）。
ADV3_MONOREPO = {
    "legacy_server/requirements.txt": "fastmcp>=2.10,<3\n",
    "legacy_server/server.py": FASTMCP_SERVER,
    "new_server/pyproject.toml": '[project]\nname = "new-server"\nversion = "0.1.0"\ndependencies = ["mcp>=2.0"]\n',
    "new_server/server.py": NEW_SERVER,
}


def _assert_malformed_no_contradiction(u):
    dk = u["D_kind"]
    assert "read_only_hint" in dk.get("malformed", []), dk
    assert dk["explicit"] == [] and "upper" not in dk, dk
    assert not dk.get("unknown"), dk
    assert not _contradictions(u), _contradictions(u)


def _assert_not_declared(u):
    dk = u["D_kind"]
    assert dk["explicit"] == [] and "upper" not in dk, dk
    assert not _contradictions(u), _contradictions(u)


def _assert_declared(u):
    dk = u["D_kind"]
    assert dk["explicit"] == ["readOnlyHint"], dk
    assert "read_only_hint" not in dk.get("malformed", []), dk
    assert "contradiction:D1" in _notes_at(u, "builtins.open")


@pytest.fixture(scope="module")
def adv3_mono(tmp_path_factory):
    return _manifest(tmp_path_factory, "adv3_mono", ADV3_MONOREPO)


def test_adv3_legacy_fastmcp2_subtree_stays_malformed(adv3_mono):
    """U38-ADV-3 の expected: fastmcp<3 のサブツリーは mcp 1.x で動く → snake_case は ⊥ + malformed のまま、矛は出ない。"""
    _assert_malformed_no_contradiction(_unit(adv3_mono, "legacy_server/server.py", "save_note"))


def test_adv3_new_subtree_decided_by_its_own_dependencies(adv3_mono):
    """U38-ADV-3（サブツリーごと）: mcp>=2.0 の new_server の snake_case は、隣の legacy_server に引きずられず宣言 → D1 の矛。"""
    _assert_declared(_unit(adv3_mono, "new_server/server.py", "new_note"))


@pytest.mark.parametrize(
    "req",
    ["fastmcp>=2.10,<3", "fastmcp==2.*", "fastmcp~=3.0", "fastmcp<4", "fastmcp==3.2.0", "fastmcp<=3.9"],
)
def test_adv3_fastmcp_upper_below_4_is_lt2(tmp_path_factory, req):
    """U38-ADV-3 (1): fastmcp の指定の上限が 4 未満なら mcp<2 → snake_case は malformed、矛は出ない。"""
    m = _manifest(tmp_path_factory, "adv3_upper", {"requirements.txt": req + "\n", "server.py": FASTMCP_SERVER})
    _assert_malformed_no_contradiction(_unit(m, "server.py", "save_note"))


def test_adv3_fastmcp_lock_below_4_is_lt2(tmp_path_factory):
    """U38-ADV-3 (1): fastmcp の lock の版が 4 未満（2.12.4 は mcp<2.0.0,>=1.12.4 を要求）なら lt2。"""
    lock = 'version = 1\n\n[[package]]\nname = "fastmcp"\nversion = "2.12.4"\nsource = { registry = "https://pypi.org/simple" }\n'
    m = _manifest(tmp_path_factory, "adv3_lock", {"uv.lock": lock, "server.py": FASTMCP_SERVER})
    _assert_malformed_no_contradiction(_unit(m, "server.py", "save_note"))


@pytest.mark.parametrize("req", ["fastmcp>=2.10", "fastmcp<=4", "fastmcp<4.1", "fastmcp"])
def test_adv3_fastmcp_without_upper_below_4_is_undecided(tmp_path_factory, req):
    """対照: 上限が 4 未満と言えない fastmcp の指定（4.x を許す）は票にならない → D_unknown で、宣言にも malformed にもしない。"""
    m = _manifest(tmp_path_factory, "adv3_open", {"requirements.txt": req + "\n", "server.py": FASTMCP_SERVER})
    u = _unit(m, "server.py", "save_note")
    assert u["D_kind"].get("unknown") is True, u["D_kind"]
    assert "read_only_hint" not in u["D_kind"].get("malformed", [])
    _assert_not_declared(u)


def test_adv3_control_fastmcp_ge_4_still_ge2(tmp_path_factory):
    """対照（変えない）: fastmcp>=4 は mcp>=2 を要求する → snake_case は宣言。"""
    m = _manifest(tmp_path_factory, "adv3_fm4", {"requirements.txt": "fastmcp>=4,<5\n", "server.py": FASTMCP_SERVER})
    _assert_declared(_unit(m, "server.py", "save_note"))


def test_adv3_unit_outside_every_subproject_is_unknown(tmp_path_factory):
    """U38-ADV-3 (2): 依存記載が複数のサブプロジェクトに分かれ、ユニットがどれにも属さなければ版は決まらない（D_unknown）。"""
    files = {
        "a/requirements.txt": "mcp>=2.0\n",
        "b/requirements.txt": "mcp>=2.1\n",
        "tools/server.py": FASTMCP_SERVER,
    }
    m = _manifest(tmp_path_factory, "adv3_outside", files)
    u = _unit(m, "tools/server.py", "save_note")
    assert u["D_kind"].get("unknown") is True, u["D_kind"]
    _assert_not_declared(u)


def test_adv3_workspace_root_lock_conflicting_with_member_shape_is_unknown(tmp_path_factory):
    """対照（fix_outline 条件 (1)、変えない）: ルートの lock（mcp 1.30.0）と、メンバーの `mcp.server.mcpserver`（2.x の形）が
    食い違う木では、メンバーの snake_case を宣言にしない。"""
    lock = 'version = 1\n\n[[package]]\nname = "mcp"\nversion = "1.30.0"\nsource = { registry = "https://pypi.org/simple" }\n'
    files = {
        "uv.lock": lock,
        "pyproject.toml": '[project]\nname = "ws"\nversion = "0.1.0"\n\n[tool.uv.workspace]\nmembers = ["member"]\n',
        "member/pyproject.toml": '[project]\nname = "member"\nversion = "0.1.0"\ndependencies = ["mcp"]\n',
        "member/server.py": NEW_SERVER,
    }
    m = _manifest(tmp_path_factory, "adv3_ws", files)
    _assert_not_declared(_unit(m, "member/server.py", "new_note"))


# ===========================================================================
# U38-ADV-4: コメント・自由文の中の `mcp>=2` は依存の指定ではない
# ===========================================================================

ADV4_FREE_TEXT = {
    "requirements_comment_line": {
        "requirements.txt": "fastmcp>=2.10\n# TODO: move to mcp>=2 (MCPServer) once we drop fastmcp\n",
    },
    "requirements_inline_comment": {"requirements.txt": "fastmcp>=2.10  # switch to mcp>=2 later\n"},
    "pyproject_description": {
        "pyproject.toml": '[project]\nname = "x"\nversion = "0.1.0"\ndescription = "works with mcp>=2 soon"\n'
        'dependencies = ["fastmcp>=2.10"]\n',
    },
    "pyproject_comment": {
        "pyproject.toml": '[project]\nname = "x"\nversion = "0.1.0"\n# pin mcp>=2 once fastmcp 4 is out\n'
        'dependencies = [\n    "fastmcp>=2.10",  # mcp>=2 breaks us\n]\n',
    },
    "pyproject_other_table": {
        "pyproject.toml": '[project]\nname = "x"\nversion = "0.1.0"\ndependencies = ["fastmcp>=2.10"]\n\n'
        '[tool.notes]\nmigration = "mcp>=2.0"\n',
    },
}


@pytest.mark.parametrize("key", sorted(ADV4_FREE_TEXT))
def test_adv4_free_text_is_not_a_version_vote(tmp_path_factory, key):
    """U38-ADV-4 の expected: コメント・description などの `mcp>=2` は票にならない → 版は決まらず（D_unknown）、矛は出ない。"""
    files = dict(ADV4_FREE_TEXT[key])
    files["server.py"] = FASTMCP_SERVER
    m = _manifest(tmp_path_factory, "adv4", files)
    u = _unit(m, "server.py", "save_note")
    assert u["D_kind"].get("unknown") is True, (u["D_kind"], m.get("mcp_version"))
    _assert_not_declared(u)


def test_adv4_review_tree_tf(tmp_path_factory):
    """U38-ADV-4 の再現（tF）: fastmcp<3 とコメントの `mcp>=2` → lt2（malformed）で、矛は出ない。"""
    files = {
        "requirements.txt": "fastmcp>=2.10,<3\n# TODO: move to mcp>=2 (MCPServer) once we drop fastmcp\n",
        "server.py": FASTMCP_SERVER,
    }
    m = _manifest(tmp_path_factory, "adv4_tf", files)
    _assert_malformed_no_contradiction(_unit(m, "server.py", "save_note"))


ADV4_REAL_SPECS = {
    "requirements_extras_marker": {"requirements.txt": 'mcp[cli]>=2.0 ; python_version >= "3.10"\n'},
    "requirements_dev": {"requirements-dev.txt": "-r requirements.txt\nmcp>=2.1  # new SDK\n"},
    "pyproject_multiline": {
        "pyproject.toml": '[project]\nname = "x"\nversion = "0.1.0"\ndescription = "d"\ndependencies = [\n'
        '    "httpx>=0.27",\n    "mcp>=2.0",  # the SDK\n]\n',
    },
    "pyproject_optional": {
        "pyproject.toml": '[project]\nname = "x"\nversion = "0.1.0"\ndependencies = []\n\n'
        '[project.optional-dependencies]\nserver = ["mcp[cli]>=2.0"]\n',
    },
    "setup_cfg": {"setup.cfg": "[metadata]\nname = x\n\n[options]\ninstall_requires =\n    httpx\n    mcp>=2.0\n"},
}


@pytest.mark.parametrize("key", sorted(ADV4_REAL_SPECS))
def test_adv4_control_real_specs_still_vote_ge2(tmp_path_factory, key):
    """対照（変えない）: 依存の指定としての `mcp>=2`（extras・marker・複数行の配列・optional・setup.cfg）は今どおり ge2 の票。"""
    files = dict(ADV4_REAL_SPECS[key])
    files["server.py"] = FASTMCP_SERVER
    m = _manifest(tmp_path_factory, "adv4_real", files)
    _assert_declared(_unit(m, "server.py", "save_note"))


PYPROJECT_CASES = {
    # description の中の `mcp>=2` は票にならない
    "description": (
        '[project]\nname = "x"\ndescription = "works with mcp>=2 soon"\ndependencies = ["fastmcp>=2.10"]\n',
        [],
    ),
    # 複数行の文字列の中は読まない。`mcp-types>=2` は mcp ではない
    "multiline_string": (
        '[project]\nname = "x"\ndescription = """\nmcp>=2\n"""\ndependencies = [\n  "mcp>=2.0",\n  "mcp-types>=2",\n]\n',
        ["ge2"],
    ),
    # optional-dependencies も依存の指定
    "optional": (
        '[project]\nname = "x"\ndependencies = ["mcp>=1.2,<2"]\n[project.optional-dependencies]\ncli = ["mcp[cli]>=2"]\n',
        ["ge2", "lt2"],
    ),
    # コメントと、依存の表でない所の文字列は読まない
    "comment_and_non_list": (
        '[project]\nname = "x"\n# mcp>=2\ndependencies = []\n[tool.x]\ndependencies = "mcp>=2"\n',
        [],
    ),
}


@pytest.mark.parametrize("key", sorted(PYPROJECT_CASES))
def test_adv4_pyproject_line_parser_matches_toml_parser(tmp_path, monkeypatch, key):
    """ADV-4（Python 3.10 には tomllib が無い）: 保守的な行パーサは TOML パーサと同じ票を出す（処理系で結果が変わらない）。

    参照の TOML パーサは 3.11 以上の tomllib、3.10 ではテストの依存の tomli（解析器は標準ライブラリだけを使う）。
    """
    text, expected = PYPROJECT_CASES[key]
    ref = pytest.importorskip("tomllib") if sys.version_info >= (3, 11) else pytest.importorskip("tomli")
    (tmp_path / "pyproject.toml").write_text(text, encoding="utf-8")
    monkeypatch.setattr(enforcement, "_tomllib", ref)
    with_toml = enforcement.mcp_major_votes(str(tmp_path))
    monkeypatch.setattr(enforcement, "_tomllib", None)
    without_toml = enforcement.mcp_major_votes(str(tmp_path))
    assert with_toml == without_toml
    assert sorted(v for _label, v in without_toml) == expected, without_toml


# ===========================================================================
# U38-ADV-6: `from pkg import m` は __init__.py の束縛をサブモジュールより優先する
# ===========================================================================

SERVER_HEAD = "from mcp.server.lowlevel import Server\nfrom mcp.types import ListToolsResult, Tool, ToolAnnotations\n"

#: レビューの tG。
ADV6_ABS = {
    "pkg/__init__.py": "from .impl_v2 import tools as handlers  # noqa: F401\n",
    "pkg/handlers.py": STUB_HANDLER,
    "pkg/impl_v2/__init__.py": "",
    "pkg/impl_v2/tools.py": REAL_HANDLER,
    "server.py": SERVER_HEAD
    + "\nfrom pkg import handlers\n"
    + LIST_TOOLS
    + '\n\nserver = Server("t", on_list_tools=list_tools, on_call_tool=handlers.handle)\n',
}

#: 同じ形の相対 import（`from . import handlers`、allow_package の枝）。
ADV6_REL = {
    "pkg/__init__.py": "from .impl_v2 import tools as handlers  # noqa: F401\n",
    "pkg/handlers.py": STUB_HANDLER,
    "pkg/impl_v2/__init__.py": "",
    "pkg/impl_v2/tools.py": REAL_HANDLER,
    "pkg/server.py": SERVER_HEAD
    + "\nfrom . import handlers\n"
    + LIST_TOOLS
    + '\n\nserver = Server("t", on_list_tools=list_tools, on_call_tool=handlers.handle)\n',
}


@pytest.mark.parametrize("tree", [ADV6_ABS, ADV6_REL], ids=["absolute", "relative"])
def test_adv6_init_binding_wins_over_submodule(tmp_path_factory, tree):
    """U38-ADV-6 の expected: `__init__.py` が handlers を impl_v2.tools に束縛する → 登録されるのは tools.handle。
    そのユニットと D1 の矛が残る。"""
    m = _manifest(tmp_path_factory, "adv6", tree)
    u = _unit(m, "pkg/impl_v2/tools.py", "handle")
    assert u["unit"]["entry_kind"] == "lowlevel_v2"
    assert D1_REMOVE <= _notes_at(u, "os.remove")


def test_adv6_init_star_import_is_not_a_submodule(tmp_path_factory):
    """U38-ADV-6（同じ理由）: `__init__.py` の star import が handlers を束縛しうるなら、サブモジュールと決めない。"""
    files = dict(ADV6_ABS)
    files["pkg/__init__.py"] = "from .impl_v2.exports import *  # noqa: F401,F403\n"
    files["pkg/impl_v2/exports.py"] = "from . import tools as handlers  # noqa: F401\n"
    m = _manifest(tmp_path_factory, "adv6_star", files)
    u = _unit(m, "pkg/impl_v2/tools.py", "handle")
    assert D1_REMOVE <= _notes_at(u, "os.remove")


def test_adv6_control_plain_submodule_stays_narrowed(tmp_path_factory):
    """対照（R2-r3-3、変えない）: `__init__.py` が handlers を束縛しなければサブモジュール pkg.handlers に一意に絞る。
    ほかの同名の関数（登録されていない）は入口ではない。"""
    files = dict(ADV6_ABS)
    files["pkg/__init__.py"] = ""
    files["pkg/handlers.py"] = REAL_HANDLER
    files["pkg/impl_v2/tools.py"] = STUB_HANDLER
    m = _manifest(tmp_path_factory, "adv6_control", files)
    assert _lowlevel_v2(m) == {("pkg/handlers.py", "handle")}
    assert D1_REMOVE <= _notes_at(_unit(m, "pkg/handlers.py", "handle"), "os.remove")
