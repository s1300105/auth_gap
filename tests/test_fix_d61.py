"""D61 の一般的な修正（G1〜G5。`docs/decisions.md` D61）。

**期待値はこのテストで、`authgap/` を直す前に書いた。** v3 の事例ではなく、言語の意味・ライブラリの仕様から
決まる形だけを入れる（D61 の基準）。「変えない」側を反例として入れる。
"""

from __future__ import annotations

import pytest

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


def _kinds(u):
    return sorted({(e["kind"], e["site"]) for e in u["effects"]})


def _contra(u, decl):
    return any(n == f"contradiction:{decl}" for r in u["rows"] for n in r.get("notes", []))


# ---------------------------------------------------------------------------
# G1: 子プロセスの標準入力はファイルではない
# ---------------------------------------------------------------------------

G1_SRC = r'''
import asyncio
import subprocess

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")


@mcp.tool(annotations={"readOnlyHint": True})
async def run_cmd_no_input(cmd: str) -> str:
    proc = await asyncio.create_subprocess_exec("helm", "history", cmd, stdout=asyncio.subprocess.PIPE)
    out, _ = await proc.communicate(input=None)
    return out.decode()


@mcp.tool(annotations={"readOnlyHint": True})
async def run_cmd_with_input(data: str) -> str:
    proc = subprocess.Popen(["sort"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, _ = proc.communicate(input=data.encode())
    return out.decode()


@mcp.tool()
async def run_interpreter(code: str) -> str:
    proc = subprocess.Popen(["python3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, _ = proc.communicate(input=code.encode())
    return out.decode()
'''


@pytest.fixture(scope="module")
def g1(tmp_path_factory):
    return _units(tmp_path_factory, "g1", {"server.py": G1_SRC})


@pytest.mark.parametrize("tool", ["run_cmd_no_input", "run_cmd_with_input"])
def test_g1_pipe_to_non_interpreter_is_not_fs_write(g1, tool):
    assert not [k for k in _kinds(g1[tool]) if k[1].startswith("pipe:")], _kinds(g1[tool])
    assert not [r for r in g1[tool]["rows"] if r["site"].startswith("pipe:") and "CONTRADICTION" in r["verdicts"]]


@pytest.mark.parametrize("tool", ["run_cmd_no_input", "run_cmd_with_input"])
def test_g1_spawn_itself_is_kept(g1, tool):
    # 反例（変えない）: 子プロセスの起動そのものは SPAWN として残る
    assert [k for k in _kinds(g1[tool]) if k[0] == "SPAWN"], _kinds(g1[tool])


def test_g1_interpreter_pipe_is_still_exec(g1):
    # 反例（変えない）: インタプリタへのコード投入は EXEC@pipe
    assert ("EXEC", "pipe:communicate") in _kinds(g1["run_interpreter"]), _kinds(g1["run_interpreter"])


# ---------------------------------------------------------------------------
# G2: 組込み型の値のメソッドを木の中の同名メソッドに結ばない
# ---------------------------------------------------------------------------

G2_AUDIT = r'''
from pathlib import Path


class AuditLog:
    def append(self, x):
        Path("/tmp/audit").write_text(str(x))

    def update(self, x):
        Path("/tmp/audit2").write_text(str(x))
'''

G2_SRC = r'''
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")


@mcp.tool(annotations={"readOnlyHint": True})
def with_bytearray(p: str) -> str:
    rows = bytearray()
    rows.append(0)
    return "x"


@mcp.tool(annotations={"readOnlyHint": True})
def with_list_ctor(p: str) -> str:
    xs = list()
    xs.append(p)
    return "x"


@mcp.tool(annotations={"readOnlyHint": True})
def with_dict_ctor(p: str) -> str:
    d = dict()
    d.update(a=p)
    return "x"


@mcp.tool(annotations={"readOnlyHint": True})
def with_str_value(p: str) -> str:
    s = "a" + p
    s.update(1)
    return "x"


@mcp.tool(annotations={"readOnlyHint": True})
def with_unknown_receiver(log, p: str) -> str:
    log.append(p)
    return "x"


@mcp.tool(annotations={"readOnlyHint": True})
def with_shadowed_list(p: str) -> str:
    from pkg.audit import AuditLog as list  # noqa: A001
    xs = list()
    xs.append(p)
    return "x"
'''


@pytest.fixture(scope="module")
def g2(tmp_path_factory):
    return _units(tmp_path_factory, "g2", {"pkg/__init__.py": "", "pkg/audit.py": G2_AUDIT, "server.py": G2_SRC})


@pytest.mark.parametrize("tool", ["with_bytearray", "with_list_ctor", "with_dict_ctor", "with_str_value"])
def test_g2_builtin_receiver_not_bound_to_tree_method(g2, tool):
    assert not [e for e in g2[tool]["effects"] if "AuditLog" in " ".join(e.get("witness_chain") or [])], _kinds(g2[tool])
    assert not _contra(g2[tool], "D1")


def test_g2_unknown_receiver_still_by_name(g2):
    # 反例（変えない）: 型の分からない受け手は今までどおり末尾名で降りる（確度 opaque(unresolved)）
    effs = [e for e in g2["with_unknown_receiver"]["effects"] if e["kind"] == "FS_WRITE"]
    assert effs and all("unresolved" in (e.get("resolution_reasons") or []) for e in effs)


def test_g2_shadowed_builtin_name_is_not_builtin(g2):
    # 反例（変えない）: `list` が木の中のクラスに束縛し直されていれば、組込みとして扱わない
    assert [e for e in g2["with_shadowed_list"]["effects"] if e["kind"] == "FS_WRITE"], _kinds(g2["with_shadowed_list"])


# ---------------------------------------------------------------------------
# G3: パッケージの __init__.py の再公開を追う
# ---------------------------------------------------------------------------

G3_FILES = {
    "app/__init__.py": "",
    "app/tools/__init__.py": "from .impl import do_write\n",
    "app/tools/impl.py": "from pathlib import Path\n\n\ndef do_write(p):\n    Path(p).write_text('x')\n",
    "other/__init__.py": "",
    "other/copy.py": "def do_write(p):\n    return p\n",
    "app/main.py": r'''
from mcp.server.fastmcp import FastMCP

from .tools import do_write
from .tools import do_write as do_write_tool

mcp = FastMCP("t")


@mcp.tool(annotations={"readOnlyHint": True})
def reexport_plain(p: str) -> str:
    do_write(p)
    return "x"


@mcp.tool(annotations={"readOnlyHint": True})
def reexport_alias(p: str) -> str:
    def do_write(q):  # 読む側の同名の入れ子 def は別名 do_write_tool を上書きしない
        return q

    do_write_tool(p)
    return "x"
''',
}


@pytest.fixture(scope="module")
def g3(tmp_path_factory):
    return _units(tmp_path_factory, "g3", G3_FILES)


@pytest.mark.parametrize("tool", ["reexport_plain", "reexport_alias"])
def test_g3_reexport_is_followed(g3, tool):
    assert ("FS_WRITE", "pathlib.Path.write_text") in _kinds(g3[tool]), _kinds(g3[tool])
    assert _contra(g3[tool], "D1")


# ---------------------------------------------------------------------------
# G4: 注釈で型を付ける受け手は sink 表の proxy の型から導く
# ---------------------------------------------------------------------------

G4_SRC = r'''
from typing import Any

import httpx
from mcp.server.fastmcp import Context, FastMCP

mcp = FastMCP("t")


def _client(ctx: Context) -> httpx.AsyncClient:
    return ctx.request_context.lifespan_context["v2"]


def _other(ctx: Context) -> dict:
    return ctx.request_context.lifespan_context["v2"]


async def _send(c: httpx.AsyncClient, key: str) -> Any:
    return await c.post(f"/issue/{key}", json={"k": key})


@mcp.tool(annotations={"readOnlyHint": True})
async def via_return_annotation(ctx: Context, key: str) -> str:
    c = _client(ctx)
    await c.post(f"/issue/{key}/transitions", json={"k": key})
    return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def via_param_annotation(ctx: Context, key: str) -> str:
    await _send(ctx.request_context.lifespan_context["v2"], key)
    return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def via_non_proxy_annotation(ctx: Context, key: str) -> str:
    c = _other(ctx)
    await c.post(f"/issue/{key}", json={"k": key})
    return "x"
'''


@pytest.fixture(scope="module")
def g4(tmp_path_factory):
    return _units(tmp_path_factory, "g4", {"server.py": G4_SRC})


@pytest.mark.parametrize("tool", ["via_return_annotation", "via_param_annotation"])
def test_g4_proxy_receiver_from_annotation(g4, tool):
    assert [k for k in _kinds(g4[tool]) if k[0] == "NET" and k[1].endswith(".post")], _kinds(g4[tool])


def test_g4_non_proxy_annotation_does_not_type(g4):
    # 反例（変えない）: sink 表に無い型（dict）の注釈は受け手の型にしない
    assert not [k for k in _kinds(g4["via_non_proxy_annotation"]) if k[0] == "NET"], _kinds(g4["via_non_proxy_annotation"])


# ---------------------------------------------------------------------------
# G5: 解決できなかった木の中の呼び出しを数えて出す（判定は変えない）
# ---------------------------------------------------------------------------

G5_FILES = {
    "a/__init__.py": "",
    "a/one.py": "def helper(p):\n    return p\n",
    "b/__init__.py": "",
    "b/two.py": "def helper(p):\n    return p\n",
    "server.py": r'''
import json

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")


def local_ok(p):
    return p


@mcp.tool(annotations={"readOnlyHint": True})
def ambiguous_tree_call(obj, p: str) -> str:
    obj.helper(p)
    return "x"


@mcp.tool(annotations={"readOnlyHint": True})
def resolved_only(p: str) -> str:
    local_ok(p)
    return json.dumps(p)
''',
}


@pytest.fixture(scope="module")
def g5(tmp_path_factory):
    return _units(tmp_path_factory, "g5", G5_FILES)


def test_g5_counts_unresolved_tree_call(g5):
    u = g5["ambiguous_tree_call"]
    assert u.get("unresolved_in_tree_calls"), u.get("unresolved_in_tree_calls")
    assert u["unresolved_in_tree_calls"][0]["name"] == "helper"


def test_g5_zero_when_all_resolved_or_external(g5):
    # 反例: 木の中の呼び出しが解決でき、ほかは外部ライブラリ（json.dumps）だけなら 0
    assert g5["resolved_only"].get("unresolved_in_tree_calls") == []
