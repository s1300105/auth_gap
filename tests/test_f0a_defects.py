"""F0a run 1 の事前点検で見つかった欠陥の再現（`docs/decisions.md` D17）。

**期待は仕様の文言から書き、修正より先にコミットする。** 未修正の欠陥は
`xfail(strict=True)` にしてあり、直ったら XPASS で失敗するので、その修正
コミットで印を外す。

各欠陥に**前提テスト**（印なし）を 1 つずつ置く。前提テストは「その fixture が
解析器の当該経路に届いている」ことを確かめる。これが無いと、fixture の書き損じで
ユニットが見つからないだけのテストも xfail として「通って」しまう。

**xfail が予期せず通ったら、点検者の欠陥主張が反証されたということである。**
その場合は印を外すのではなく、`docs/f0a_checks.md` の当該件と突き合わせる。

出所の件番号（OPQ[5] など）は `evidence/f0a/check_sample.json` の標本 index。
"""

from __future__ import annotations

import textwrap

import pytest

from authgap.ir import Prin
from authgap.runner import RunConfig, run

DEFECT = pytest.mark.xfail(strict=True, reason="D17: 未修正の欠陥（修正コミットでこの印を外す）")

FASTMCP_HEAD = """\
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("t")
"""


def _run(tmp_path, files: dict, population: str = "mcp_server"):
    for rel, content in files.items():
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            p.write_bytes(content)
        else:
            p.write_text(textwrap.dedent(content), encoding="utf-8")
    return run(RunConfig(src_root=str(tmp_path), population=population, full=False))


def _unit(res, tool_name: str):
    found = [u for u in res.tree.units if u.unit.tool_name == tool_name]
    assert len(found) == 1, f"{tool_name!r} のユニットが 1 件でない: {[u.unit.tool_name for u in res.tree.units]}"
    return found[0]


def _effects(u, kind: str):
    return [e for e in u.effects if e.kind == kind]


def _slot(u, kind: str, slot: str):
    rows = [e for e in _effects(u, kind) if slot in e.control_slots()]
    assert rows, f"{kind} 効果に slot {slot!r} が無い: {[e.control_slots().keys() for e in u.effects]}"
    return rows[0].control_slots()[slot]


# ---------------------------------------------------------------------------
# 1. list.append を受け手への書き込みとして扱わない（RES[7]。false-clean）
# ---------------------------------------------------------------------------

LIST_APPEND = FASTMCP_HEAD + """\
import sqlite3

@mcp.tool()
def query_logs(run_id: str) -> list:
    conn = sqlite3.connect("logs.db")
    params = []
    params.append(run_id)
    return conn.execute("SELECT * FROM logs WHERE run_id = ?", params).fetchall()

@mcp.tool()
def filter_logs(level: str) -> list:
    conn = sqlite3.connect("logs.db")
    clauses = []
    clauses.append(f"level = '{level}'")
    sql = "SELECT * FROM logs WHERE " + " AND ".join(clauses)
    return conn.execute(sql).fetchall()
"""


def test_list_append_precondition(tmp_path):
    res = _run(tmp_path, {"server.py": LIST_APPEND})
    assert _effects(_unit(res, "query_logs"), "DB")
    assert _effects(_unit(res, "filter_logs"), "DB")


@DEFECT
def test_list_append_keeps_model_in_params(tmp_path):
    res = _run(tmp_path, {"server.py": LIST_APPEND})
    assert _slot(_unit(res, "query_logs"), "DB", "params").prin == Prin.MODEL


@DEFECT
def test_str_join_keeps_model_from_iterable(tmp_path):
    """`" AND ".join(clauses)` の主語は区切り文字だが、値は clauses の中身から来る。"""
    res = _run(tmp_path, {"server.py": LIST_APPEND})
    assert _slot(_unit(res, "filter_logs"), "DB", "sql").prin == Prin.MODEL


# ---------------------------------------------------------------------------
# 2. 受け手型が付かず sink を落とす（NOE[1,4,6,10,11]。false-clean）
# ---------------------------------------------------------------------------

LOCAL_PATH = FASTMCP_HEAD + """\
from pathlib import Path

@mcp.tool()
def scan_project(project_path: str) -> int:
    root = Path(project_path)
    total = 0
    for filepath in root.rglob("*.py"):
        total += len(filepath.read_text())
    return total
"""

STORE_CLASS = """\
import sqlite3

class Store:
    def __init__(self):
        self._db = sqlite3.connect("store.db")

    def post(self, text):
        self._db.execute("INSERT INTO messages VALUES (?)", (text,))
"""

MODULE_INSTANCE = FASTMCP_HEAD + STORE_CLASS + """\

store = Store()

@mcp.tool()
def post_message(text: str) -> str:
    store.post(text)
    return "ok"
"""

RETURN_ANNOTATION = FASTMCP_HEAD + """\
from pathlib import Path

def submission_path(name: str) -> Path:
    return Path("/srv/data") / name

@mcp.tool()
def submit(name: str, body: str) -> str:
    p = submission_path(name)
    p.write_text(body)
    return "ok"
"""

CLOSURE_VAR = FASTMCP_HEAD + STORE_CLASS + """\

def register(server, store: Store):
    @server.tool()
    def post(text: str) -> str:
        store.post(text)
        return "ok"

register(mcp, Store())
"""


def test_receiver_precondition(tmp_path):
    res = _run(
        tmp_path,
        {"a/s.py": LOCAL_PATH, "b/s.py": MODULE_INSTANCE, "c/s.py": RETURN_ANNOTATION, "d/s.py": CLOSURE_VAR},
    )
    for name in ("scan_project", "post_message", "submit", "post"):
        _unit(res, name)


@DEFECT
def test_local_path_receiver_finds_fs_read(tmp_path):
    res = _run(tmp_path, {"s.py": LOCAL_PATH})
    assert _effects(_unit(res, "scan_project"), "FS_READ")


@DEFECT
def test_module_instance_self_field_finds_db(tmp_path):
    res = _run(tmp_path, {"s.py": MODULE_INSTANCE})
    assert _effects(_unit(res, "post_message"), "DB")


@DEFECT
def test_intree_return_value_receiver_finds_fs_write(tmp_path):
    res = _run(tmp_path, {"s.py": RETURN_ANNOTATION})
    assert _effects(_unit(res, "submit"), "FS_WRITE")


@DEFECT
def test_closure_variable_receiver_finds_db(tmp_path):
    res = _run(tmp_path, {"s.py": CLOSURE_VAR})
    assert _effects(_unit(res, "post"), "DB")


# ---------------------------------------------------------------------------
# 3. 受け手型なしで末尾名一致の唯一候補へ解決する（EFF[6]。false-alarm）
# ---------------------------------------------------------------------------

NAME_ONLY = {
    "server/app.py": FASTMCP_HEAD + """\
import pyautogui

@mcp.tool()
def take_screenshot(path: str) -> str:
    shot = pyautogui.screenshot()
    shot = shot.convert("RGB")
    return path
""",
    "tools/release.py": """\
import subprocess

class GitHashParamType:
    def convert(self, value, param=None, ctx=None):
        return subprocess.run(["git", "rev-parse", value], capture_output=True).stdout
""",
}


def test_name_only_precondition(tmp_path):
    _unit(_run(tmp_path, NAME_ONLY), "take_screenshot")


@DEFECT
def test_untyped_receiver_does_not_resolve_by_tail_name(tmp_path):
    """Def 4: 木内で解決できない呼び出しは `opaque(unresolved)`。名前だけで他クラスへ飛ばない。"""
    res = _run(tmp_path, NAME_ONLY)
    assert not _effects(_unit(res, "take_screenshot"), "SPAWN")


# ---------------------------------------------------------------------------
# 4. §2.6 の URL slot 分割規則（OPQ 9 件。precision loss）
# ---------------------------------------------------------------------------

URL_SPLIT = FASTMCP_HEAD + """\
import requests

@mcp.tool()
def get_messages(chat_id: str) -> str:
    return requests.get(f"https://graph.example.com/v1.0/chats/{chat_id}/messages").text
"""


def test_url_split_precondition(tmp_path):
    assert _effects(_unit(_run(tmp_path, {"s.py": URL_SPLIT}), "get_messages"), "NET")


@DEFECT
def test_url_host_from_literal_authority_is_op(tmp_path):
    """parts[0] がリテラルで `://` の後に `/` を含む → url.host は OP（§2.6）。"""
    u = _unit(_run(tmp_path, {"s.py": URL_SPLIT}), "get_messages")
    host = _slot(u, "NET", "url.host")
    assert host.prin == Prin.OP and host.prov.kind == "resolved"


def test_url_split_does_not_drop_model(tmp_path):
    """分割しても MODEL の部分がどこかの slot に残ること（**false-clean を作らない**）。"""
    u = _unit(_run(tmp_path, {"s.py": URL_SPLIT}), "get_messages")
    slots = [v for e in _effects(u, "NET") for v in e.control_slots().values()]
    assert any(v.prin == Prin.MODEL for v in slots)


# ---------------------------------------------------------------------------
# 5. モジュール大域の名前と os.environ（OPQ 8 + 4 件。precision loss）
# ---------------------------------------------------------------------------

MODULE_CONST = FASTMCP_HEAD + """\
import requests

BASE_URL = "https://api.example.com"

@mcp.tool()
def search(q: str) -> str:
    return requests.get(f"{BASE_URL}/search?q={q}").text
"""

ENV_MODULE = FASTMCP_HEAD + """\
import os
import requests

JIRA_BASE_URL = os.environ.get("JIRA_BASE_URL", "https://jira.example.com")

@mcp.tool()
def issues(jql: str) -> str:
    return requests.get(f"{JIRA_BASE_URL}/rest/api/3/search?jql={jql}").text
"""

ENV_LOCAL = FASTMCP_HEAD + """\
import os
import requests

@mcp.tool()
def token(scope: str) -> str:
    endpoint = os.environ.get("CALM_TOKEN_ENDPOINT", "")
    return requests.post(f"{endpoint}/oauth/token", data={"scope": scope}).text
"""


def test_module_names_precondition(tmp_path):
    res = _run(tmp_path, {"a/s.py": MODULE_CONST, "b/s.py": ENV_MODULE, "c/s.py": ENV_LOCAL})
    for name in ("search", "issues", "token"):
        assert _effects(_unit(res, name), "NET")


@pytest.mark.parametrize(
    "source,tool",
    [
        pytest.param(MODULE_CONST, "search", marks=DEFECT, id="module_constant"),
        pytest.param(ENV_MODULE, "issues", marks=DEFECT, id="module_environ"),
        pytest.param(ENV_LOCAL, "token", marks=DEFECT, id="local_environ"),
    ],
)
def test_url_host_from_config_is_op_resolved(tmp_path, source, tool):
    """モジュール定数と `os.environ` は config atom の源（§2.3）→ OP / resolved。"""
    host = _slot(_unit(_run(tmp_path, {"s.py": source}), tool), "NET", "url.host")
    assert host.prin == Prin.OP and host.prov.kind == "resolved"


# ---------------------------------------------------------------------------
# 6. BOM 付きファイル（parse 失敗 6 件。false-clean）
# ---------------------------------------------------------------------------

BOM_SOURCE = FASTMCP_HEAD + """\
@mcp.tool()
def hello(name: str) -> str:
    return name
"""


def test_bom_precondition(tmp_path):
    res = _run(tmp_path, {"s.py": BOM_SOURCE})
    _unit(res, "hello")
    assert not res.tree.parse_failures


def test_bom_file_is_parsed(tmp_path):
    res = _run(tmp_path, {"s.py": b"\xef\xbb\xbf" + BOM_SOURCE.encode()})  # UTF-8 の BOM
    assert not res.tree.parse_failures
    _unit(res, "hello")


# ---------------------------------------------------------------------------
# 7. annotation の読み取り（r_kind = 0% の一部。Def 6）
# ---------------------------------------------------------------------------

DECORATOR_ANNOTATIONS = """\
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
mcp = FastMCP("files")

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def read_file(path: str) -> str:
    return open(path).read()

@mcp.tool(annotations={"readOnlyHint": True})
def read_file_dict(path: str) -> str:
    return open(path).read()
"""

EXPLICIT_NONE = FASTMCP_HEAD + """\
from mcp.server.fastmcp.tools import Tool

@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b

def make_tool():
    return Tool(name="add", description="add", parameters={}, fn=add, annotations=None)
"""


def test_annotations_precondition(tmp_path):
    res = _run(tmp_path, {"a/s.py": DECORATOR_ANNOTATIONS, "b/s.py": EXPLICIT_NONE})
    for name in ("read_file", "read_file_dict", "add"):
        _unit(res, name)


@pytest.mark.parametrize("tool", ["read_file", "read_file_dict"])
def test_decorator_annotations_kwarg_is_read(tmp_path, tool):
    """`@mcp.tool(annotations=...)` はエントリ自身の宣言（Def 6 の 3 形）。"""
    u = _unit(_run(tmp_path, {"s.py": DECORATOR_ANNOTATIONS}), tool)
    assert not u.d_kind.is_bottom
    assert u.d_kind.upper == frozenset({"FS_READ", "NET"})


def test_explicit_none_annotations_is_bottom_not_unknown(tmp_path):
    """`annotations=None` は読める明示の「無い」→ `⊥`。読めない形（`D_unknown`）ではない。"""
    u = _unit(_run(tmp_path, {"s.py": EXPLICIT_NONE}), "add")
    assert u.d_kind.is_bottom and not u.d_kind.unknown


# ---------------------------------------------------------------------------
# 8. カタログにある形の取りこぼし（AutoGPT @command の名前 list 形、tools_list の入れ子）
# ---------------------------------------------------------------------------

AUTOGPT = """\
import requests
from forge.command import command
from forge.models.json_schema import JSONSchema

class WebSearchComponent:
    @command(
        "web_search_legacy",
        "Search the web (legacy single-name form).",
        {"query": JSONSchema(type=JSONSchema.Type.STRING, description="q", required=True)},
    )
    def web_search_legacy(self, query: str) -> str:
        return requests.get(f"https://search.example/?q={query}").text

    @command(
        ["web_search", "search"],
        "Search the web.",
        {"query": JSONSchema(type=JSONSchema.Type.STRING, description="q", required=True)},
    )
    def web_search(self, query: str) -> str:
        return requests.get(f"https://search.example/?q={query}").text

    @command(
        names=["todo_add"],
        description="Add a todo item.",
        parameters={"item": JSONSchema(type=JSONSchema.Type.STRING, description="item", required=True)},
    )
    def todo_add(self, item: str) -> str:
        return requests.post("https://todo.example/items", json={"item": item}).text
"""

TOOLS_LIST = """\
import requests

def web_lookup(query: str) -> str:
    return requests.get(f"https://search.example/?q={query}").text

def create_agent(Agent):
    return Agent(tools=[web_lookup])

def create_fallback_agent(Agent):
    def web_research(query: str) -> str:
        return requests.get(f"https://search.example/?q={query}").text
    return Agent(tools=[web_research])
"""


def test_catalog_forms_precondition(tmp_path):
    _unit(_run(tmp_path, {"a/c.py": AUTOGPT}, population="app"), "web_search_legacy")
    _unit(_run(tmp_path, {"b/t.py": TOOLS_LIST}, population="tool_package"), "web_lookup")


def test_autogpt_command_name_list_form(tmp_path):
    """現行 AutoGPT classic は第 1 引数を名前の list で渡す（`["web_search", "search"]`）。"""
    _unit(_run(tmp_path, {"c.py": AUTOGPT}, population="app"), "web_search")


def test_autogpt_command_keyword_form(tmp_path):
    """同じく `@command(names=[...], description=..., parameters={...})`（野外 20 箇所）。"""
    _unit(_run(tmp_path, {"c.py": AUTOGPT}, population="app"), "todo_add")


def test_tools_list_nested_function(tmp_path):
    _unit(_run(tmp_path, {"t.py": TOOLS_LIST}, population="tool_package"), "web_research")
