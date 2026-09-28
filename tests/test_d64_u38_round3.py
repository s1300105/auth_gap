"""D64 / U38 の 3 巡目: 2 巡目の直しの再点検の所見 U38-RC-1 / U38-RC-2 の反例テスト。

**期待値は authgap/ を直す前に書いた（D64 / U38 の 3 巡目）。** 再現の木は再点検の木
（scratchpad/d64recheck/U38/tI・tI0・tI3・tG3）をそのまま写したもの。期待値は所見の expected（Python の意味）と
この直しの条件から導いた。件数には合わせない。

- U38-RC-1（誤警報、2 巡目の直しが作った）: mcp / fastmcp の票を 1 つも持たない依存記載のディレクトリ
  （`tools/requirements.txt` に `httpx` だけ）は、独立したサブツリー（版のグループ）にしない。いちばん近い、票を持つ
  祖先のグループに合わせる。tI では tools/notes.py は根の server.py の `app` にツールを登録するので根の環境で動く。
  根は `mcp[cli]>=1.9`（既定の install は 1.x）と extra の `mcp>=2.0`、`mcp.server.fastmcp`（1.x にしか無い）で
  食い違い unknown。したがって snake_case の `read_only_hint` は D_unknown（か malformed）で、矛は出ない。
  あわせて、子のグループ（自分の票を持つ）も、祖先のグループが矛盾で unknown なら unknown を受け継ぐ
  （子は祖先の票を受け継ぐが、祖先の API の形の根拠を受け継がないので、祖先の矛盾が子で消えていた）。
- U38-RC-2（誤 clear、既存の穴）: `import pkg.m as m` は、Python 3.7 以降 `pkg` を import した後に属性 `m` を
  getattr で採る（無いときだけ sys.modules の `pkg.m`）。`pkg/__init__.py` が m を束縛していれば、サブモジュールと
  決めない（ADV-6 と同じ判定。裸名一致に落とす）。mcp 2.2.0 の環境で
  `server.handlers.handle.__module__ == "pkg.impl_v2.tools"` を再点検役が確認。

記号: 「矛」 = 行の注記に `contradiction:<宣言>`。
"""

from __future__ import annotations

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
    return {(u["unit"]["relpath"], u["unit"]["qualname"]): u for u in m["units"]}


def _unit(m, relpath, qualname):
    units = _units(m)
    assert (relpath, qualname) in units, f"{relpath}:{qualname} がユニットにならない: {sorted(units)}"
    return units[(relpath, qualname)]


def _lowlevel_v2(m):
    return {(u["unit"]["relpath"], u["unit"]["qualname"]) for u in m["units"] if u["unit"]["entry_kind"] == "lowlevel_v2"}


def _notes_at(u, site):
    rows = [r for r in u["rows"] if r["site"] == site]
    assert rows, f"{u['unit']['qualname']}: {site} の行が無い: {[r['site'] for r in u['rows']]}"
    return {n for r in rows for n in r.get("notes", [])}


def _contradictions(u):
    return sorted(n for r in u["rows"] for n in r.get("notes", []) if n.startswith("contradiction:"))


D1_REMOVE = {"contradiction:D1", "contradiction_reason:D1:fs_write"}


def _assert_unknown_or_malformed_no_contradiction(u):
    """所見 RC-1 の expected: snake_case は D_unknown か malformed。宣言（explicit / 上界）にせず、矛も出さない。"""
    dk = u["D_kind"]
    assert dk.get("unknown") is True or "read_only_hint" in dk.get("malformed", []), dk
    assert dk["explicit"] == [] and "upper" not in dk, dk
    assert not _contradictions(u), _contradictions(u)
    assert not any("CONTRADICTION" in r["verdicts"] for r in u["rows"]), u["rows"]


def _assert_declared(u):
    dk = u["D_kind"]
    assert dk["explicit"] == ["readOnlyHint"], dk
    assert "read_only_hint" not in dk.get("malformed", []), dk
    assert "contradiction:D1" in _notes_at(u, "builtins.open")


# ===========================================================================
# U38-RC-1: 票の無い依存記載のディレクトリはグループにしない / 祖先の矛盾を受け継ぐ
# ===========================================================================

ROOT_PYPROJECT_OPTIONAL_2 = (
    '[project]\nname = "notes-server"\nversion = "0.1.0"\ndependencies = ["mcp[cli]>=1.9"]\n\n'
    '[project.optional-dependencies]\nnext = ["mcp>=2.0"]\n'
)

ROOT_SERVER_FASTMCP = '''from mcp.server.fastmcp import FastMCP

app = FastMCP("notes")

import tools.notes  # noqa: E402,F401

if __name__ == "__main__":
    app.run()
'''

TOOLS_NOTES = '''from mcp.types import ToolAnnotations

from server import app


@app.tool(annotations=ToolAnnotations(read_only_hint=True))
def save_note(path: str, text: str) -> str:
    with open(path, "w") as f:
        f.write(text)
    return "ok"
'''

#: 再点検の tI。
RC1_TI = {
    "pyproject.toml": ROOT_PYPROJECT_OPTIONAL_2,
    "server.py": ROOT_SERVER_FASTMCP,
    "tools/requirements.txt": "httpx>=0.27\n",
    "tools/notes.py": TOOLS_NOTES,
}

#: 再点検の tI0（対照: tools/requirements.txt の無い同じ木）。
RC1_TI0 = {k: v for k, v in RC1_TI.items() if k != "tools/requirements.txt"}

#: 再点検の tI3: 根は `mcp>=2.0` だけだが、両方の API を試す shim（形の食い違い）で unknown。tools は票なし。
RC1_TI3 = {
    "pyproject.toml": '[project]\nname = "notes-server"\nversion = "0.1.0"\ndependencies = ["mcp>=2.0"]\n',
    "server.py": '''try:
    from mcp.server.mcpserver import MCPServer as FastMCP
except ImportError:  # mcp 1.x
    from mcp.server.fastmcp import FastMCP

app = FastMCP("notes")

import tools.notes  # noqa: E402,F401
''',
    "tools/requirements.txt": "httpx>=0.27\n",
    "tools/notes.py": TOOLS_NOTES,
}

#: 子のディレクトリが自分の mcp の票（ge2）を持つが、祖先のグループが矛盾で unknown の木（条件の後半）。
RC1_CHILD_VOTES = dict(RC1_TI)
RC1_CHILD_VOTES["tools/requirements.txt"] = "httpx>=0.27\nmcp>=2.0\n"


@pytest.mark.parametrize(
    "tree", [RC1_TI, RC1_TI0, RC1_TI3, RC1_CHILD_VOTES], ids=["tI", "tI0_control", "tI3_shim_root", "child_has_votes"]
)
def test_rc1_subdir_shares_conflicted_root_environment(tmp_path_factory, tree):
    """U38-RC-1 の expected: tools/ は根の app に登録する → 根の環境。根が矛盾で unknown なら tools の snake_case も
    D_unknown（か malformed）で、矛は出ない。tI0 は直す前から通る対照（直した後も壊さない）。"""
    m = _manifest(tmp_path_factory, "rc1", tree)
    _assert_unknown_or_malformed_no_contradiction(_unit(m, "tools/notes.py", "save_note"))


def test_rc1_ti_manifest_does_not_decide_tools_subtree(tmp_path_factory):
    """U38-RC-1: 票の無い tools/ は版のグループにならない（manifest の根拠に `subtree:tools=ge2` を出さない）。"""
    m = _manifest(tmp_path_factory, "rc1_ev", RC1_TI)
    ev = m["mcp_version"]["evidence"]
    assert not any(e.startswith("subtree:tools=") for e in ev), ev
    assert m["mcp_version"]["class"] == "unknown", m["mcp_version"]


#: 対照（直した後も壊さない）: 根が ge2 に決まる木では、票の無い tools/ のファイルも根の版（ge2）で読む。
RC1_CONTROL_ROOT_GE2 = {
    "requirements.txt": "mcp>=2.0\n",
    "server.py": '''from mcp.server.mcpserver import MCPServer

app = MCPServer("notes")

import tools.notes  # noqa: E402,F401
''',
    "tools/requirements.txt": "httpx>=0.27\n",
    "tools/notes.py": TOOLS_NOTES,
}


def test_rc1_control_root_ge2_subdir_without_votes_is_declared(tmp_path_factory):
    """対照: 票の無いディレクトリを祖先に合わせても、祖先が ge2 に決まっていれば snake_case は宣言 → D1 の矛。"""
    m = _manifest(tmp_path_factory, "rc1_ctl_ge2", RC1_CONTROL_ROOT_GE2)
    _assert_declared(_unit(m, "tools/notes.py", "save_note"))


#: 対照（直した後も壊さない。ADV-3 の兄弟のサブプロジェクト）: 票を持つ兄弟のサブツリーは、隣の版に引きずられない。
#: 根に票の無い pyproject（workspace の宣言だけ）を置いても、根はグループにならず結果は変わらない。
FASTMCP2_SERVER = '''from fastmcp import FastMCP
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

RC1_CONTROL_SIBLINGS = {
    "pyproject.toml": '[project]\nname = "ws"\nversion = "0.1.0"\ndependencies = ["httpx"]\n',
    "legacy_server/requirements.txt": "fastmcp>=2.10,<3\n",
    "legacy_server/server.py": FASTMCP2_SERVER,
    "new_server/pyproject.toml": '[project]\nname = "new-server"\nversion = "0.1.0"\ndependencies = ["mcp>=2.0"]\n',
    "new_server/server.py": NEW_SERVER,
}


def test_rc1_control_sibling_subprojects_still_decided_separately(tmp_path_factory):
    """対照: 票を持つ兄弟のサブツリー（ADV-3）は今どおり別々に決まる。legacy は malformed、new は宣言で D1 の矛。"""
    m = _manifest(tmp_path_factory, "rc1_ctl_sib", RC1_CONTROL_SIBLINGS)
    legacy = _unit(m, "legacy_server/server.py", "save_note")
    assert "read_only_hint" in legacy["D_kind"].get("malformed", []), legacy["D_kind"]
    assert not _contradictions(legacy)
    _assert_declared(_unit(m, "new_server/server.py", "new_note"))


# ===========================================================================
# U38-RC-2: `import pkg.m as m` も __init__.py の束縛をサブモジュールより優先する
# ===========================================================================

REAL_HANDLER = '''import os
from mcp.types import CallToolResult, TextContent


async def handle(ctx, params):
    if params.name == "rm":
        os.remove(params.arguments["path"])
        return CallToolResult(content=[TextContent(type="text", text="ok")])
    raise ValueError(params.name)
'''

STUB_HANDLER = '''async def handle(ctx, params):
    raise NotImplementedError("legacy stub")
'''

TG3_SERVER = '''from mcp.server.lowlevel import Server
from mcp.types import ListToolsResult, Tool, ToolAnnotations

import pkg.handlers as handlers


async def list_tools(ctx, params):
    return ListToolsResult(tools=[
        Tool(name="rm", description="d", inputSchema={}, annotations=ToolAnnotations(readOnlyHint=True)),
    ])


server = Server("t", on_list_tools=list_tools, on_call_tool=handlers.handle)
'''

#: 再点検の tG3。
RC2_TG3 = {
    "server.py": TG3_SERVER,
    "pkg/__init__.py": "from . import handlers as _legacy  # noqa: F401\nfrom .impl_v2 import tools as handlers  # noqa: F401\n",
    "pkg/handlers.py": STUB_HANDLER,
    "pkg/impl_v2/__init__.py": "",
    "pkg/impl_v2/tools.py": REAL_HANDLER,
}


def test_rc2_import_as_init_binding_wins_over_submodule(tmp_path_factory):
    """U38-RC-2 の expected: 登録されるのは pkg.impl_v2.tools.handle → そのユニットと D1 の矛が残る。"""
    m = _manifest(tmp_path_factory, "rc2", RC2_TG3)
    u = _unit(m, "pkg/impl_v2/tools.py", "handle")
    assert u["unit"]["entry_kind"] == "lowlevel_v2"
    assert D1_REMOVE <= _notes_at(u, "os.remove")


def test_rc2_import_as_init_star_is_not_a_submodule(tmp_path_factory):
    """U38-RC-2（ADV-6 と同じ理由）: `__init__.py` の star import が handlers を束縛しうるなら、サブモジュールと決めない。"""
    files = dict(RC2_TG3)
    files["pkg/__init__.py"] = "from .impl_v2.exports import *  # noqa: F401,F403\n"
    files["pkg/impl_v2/exports.py"] = "from . import tools as handlers  # noqa: F401\n"
    m = _manifest(tmp_path_factory, "rc2_star", files)
    assert D1_REMOVE <= _notes_at(_unit(m, "pkg/impl_v2/tools.py", "handle"), "os.remove")


def test_rc2_control_import_as_plain_submodule_stays_narrowed(tmp_path_factory):
    """対照（直した後も壊さない）: `__init__.py` が handlers を束縛しなければサブモジュール pkg.handlers に一意に絞る。
    登録されていない同名の関数（impl_v2.tools.handle）は入口にしない。"""
    files = dict(RC2_TG3)
    files["pkg/__init__.py"] = ""
    files["pkg/handlers.py"] = REAL_HANDLER
    files["pkg/impl_v2/tools.py"] = STUB_HANDLER
    m = _manifest(tmp_path_factory, "rc2_ctl", files)
    assert _lowlevel_v2(m) == {("pkg/handlers.py", "handle")}
    assert D1_REMOVE <= _notes_at(_unit(m, "pkg/handlers.py", "handle"), "os.remove")
