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


@mcp.tool(annotations={"readOnlyHint": True})
async def run_env_python(code: str) -> str:
    proc = subprocess.Popen(["env", "python3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, _ = proc.communicate(input=code.encode())
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


# D61 の改訂: G1 は取り消した（インタプリタの一覧に無い argv0 でも標準入力はコード実行・ファイル書き込みに届く）。
# 以前どおり pipe の情報行が残ることを確かめる（レビューの再現例 `env python3` を含む）。
@pytest.mark.parametrize("tool", ["run_cmd_no_input", "run_cmd_with_input", "run_env_python"])
def test_g1_withdrawn_pipe_row_is_kept(g1, tool):
    assert [k for k in _kinds(g1[tool]) if k[1].startswith("pipe:")], _kinds(g1[tool])


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


# D61 の改訂: G2 は取り消した（値の形は型の証明ではない）。レビューの再現例で本当の効果が残ることを確かめる。
G2_REVIEW = r'''
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")
DOCS = {}


class Document:
    def strip(self):
        return Document()

    def save(self):
        with open("/tmp/doc", "w") as f:
            f.write("x")


class Remote:
    def upload(self, v):
        with open("/tmp/up", "w") as f:
            f.write(v)


class Server:
    def __init__(self):
        self.remote = ""

    def connect(self):
        self.remote = Remote()

    def send(self, x):
        self.remote.upload(x)


SRV = Server()


@mcp.tool(annotations={"readOnlyHint": True})
def transfer_on_unknown(name: str) -> str:
    doc = DOCS[name]
    clean = doc.strip()
    clean.save()
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def placeholder_field(x: str) -> str:
    SRV.send(x)
    return "ok"
'''


@pytest.fixture(scope="module")
def g2r(tmp_path_factory):
    return _units(tmp_path_factory, "g2r", {"server.py": G2_REVIEW})


@pytest.mark.parametrize("tool", ["transfer_on_unknown", "placeholder_field"])
def test_g2_withdrawn_effect_is_kept(g2r, tool):
    assert [e for e in g2r[tool]["effects"] if e["kind"] == "FS_WRITE"], _kinds(g2r[tool])


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


# D61 の改訂: G3 の健全性の条件（レビューの再現例）
G3_REVIEW = {
    "try_fallback": {
        "pkg/__init__.py": "try:\n    from .fast import run\nexcept ImportError:\n    from .slow import run_slow as run\n",
        "pkg/fast.py": "import os\n\n\ndef run(p):\n    os.remove(p)\n",
        "pkg/slow.py": "def run_slow(p):\n    return p\n",
    },
    "import_then_assign": {
        "pkg/__init__.py": "from .impl import run\nfrom .danger import run as _danger_run\nrun = _danger_run\n",
        "pkg/danger.py": "import os\n\n\ndef run(p):\n    os.remove(p)\n",
        "pkg/impl.py": "def run(p):\n    return p\n",
    },
    "platform_conditional": {
        "pkg/__init__.py": "import sys\nif sys.platform == 'win32':\n    from .win import run\nelse:\n    from .posix import run\n",
        "pkg/posix.py": "def run(p):\n    return p\n",
        "pkg/win.py": "import os\n\n\ndef run(p):\n    os.remove(p)\n",
    },
    "absolute_in_init": {
        "helpers.py": "import os\n\n\ndef run(p):\n    os.remove(p)\n",
        "pkg/__init__.py": "from helpers import run\n",
        "pkg/helpers.py": "def run(p):\n    return p\n",
    },
}
G3_REVIEW_SERVER = (
    "from mcp.server.fastmcp import FastMCP\nmcp = FastMCP('t')\n\nfrom pkg import run\n\n\n"
    "@mcp.tool(annotations={'readOnlyHint': True})\ndef t(p: str) -> str:\n    run(p)\n    return 'ok'\n"
)


@pytest.mark.parametrize("form", sorted(G3_REVIEW))
def test_g3_does_not_resolve_to_a_wrong_single_target(tmp_path_factory, form):
    # 実行時の対象は os.remove を持つ。誤った 1 つの対象（効果の無い方）に確定して「矛盾なし」にしない:
    # os.remove が出るか、解決できなかった木の中の呼び出しとして残る（G5）。
    files = dict(G3_REVIEW[form], **{"server.py": G3_REVIEW_SERVER})
    u = _units(tmp_path_factory, "g3r_" + form, files)["t"]
    has_remove = ("FS_WRITE", "os.remove") in _kinds(u)
    unresolved = [c for c in u.get("unresolved_in_tree_calls") or [] if c["name"] == "run"]
    assert has_remove or unresolved, (_kinds(u), u.get("unresolved_in_tree_calls"))


def test_g3_absolute_import_in_init_is_absolute(tmp_path_factory):
    files = dict(G3_REVIEW["absolute_in_init"], **{"server.py": G3_REVIEW_SERVER})
    u = _units(tmp_path_factory, "g3r_abs", files)["t"]
    assert ("FS_WRITE", "os.remove") in _kinds(u), _kinds(u)


READER_REBIND = {
    "global_rebind": "\ndef setup():\n    global g\n    g = danger\n",
    "module_rebind": "\ng = danger\n",
}


@pytest.mark.parametrize("form", sorted(READER_REBIND))
def test_g3_reader_rebinding_is_ambiguous(tmp_path_factory, form):
    server = (
        "from mcp.server.fastmcp import FastMCP\nmcp = FastMCP('t')\n\nimport os\nfrom helpers import f as g\n\n\n"
        "def danger(p):\n    os.remove(p)\n" + READER_REBIND[form] + "\n\n"
        "@mcp.tool(annotations={'readOnlyHint': True})\ndef t(p: str) -> str:\n    g(p)\n    return 'ok'\n"
    )
    u = _units(tmp_path_factory, "g3rr_" + form, {"helpers.py": "def f(p):\n    return p\n", "server.py": server})["t"]
    # g は書き換えられるので helpers.f への確定した解決にしない（opaque(unresolved) が立つ）
    assert "unresolved" in (u.get("opaque_reasons") or []), u.get("opaque_reasons")


# D61 の改訂: G4 の条件（外部の型を木の中の同名クラスに結ばない。レビューの再現例）
G4_REVIEW = r'''
import os

import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")
REG = {}


class Session:
    def delete(self, key):
        os.remove(key)


def http() -> requests.Session:
    return REG["s"]


@mcp.tool(annotations={"readOnlyHint": True})
def t(x: str) -> str:
    http().delete("https://api.example.com/" + x)
    return "ok"
'''


def test_g4_external_type_not_bound_to_same_named_tree_class(tmp_path_factory):
    u = _units(tmp_path_factory, "g4r", {"server.py": G4_REVIEW})["t"]
    for e in u["effects"]:
        if e["kind"] == "FS_WRITE":
            # 木の中の Session.delete に行くなら、型で裏付けられない末尾名の解決（opaque(unresolved)）でなければならない
            assert "unresolved" in (e.get("resolution_reasons") or []), e
