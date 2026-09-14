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


def test_list_append_keeps_model_in_params(tmp_path):
    res = _run(tmp_path, {"server.py": LIST_APPEND})
    assert _slot(_unit(res, "query_logs"), "DB", "params").prin == Prin.MODEL


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


def test_local_path_receiver_finds_fs_read(tmp_path):
    res = _run(tmp_path, {"s.py": LOCAL_PATH})
    assert _effects(_unit(res, "scan_project"), "FS_READ")


def test_module_instance_self_field_finds_db(tmp_path):
    res = _run(tmp_path, {"s.py": MODULE_INSTANCE})
    assert _effects(_unit(res, "post_message"), "DB")


def test_intree_return_value_receiver_finds_fs_write(tmp_path):
    res = _run(tmp_path, {"s.py": RETURN_ANNOTATION})
    assert _effects(_unit(res, "submit"), "FS_WRITE")


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


def test_untyped_receiver_by_name_hop_is_opaque(tmp_path):
    """受け手型なしで末尾名だけで降りた経路の効果は **resolved にしない**（D17 の改訂）。

    当初は「降りない」を期待にしていたが、較正対の差分で真の経路が消えることが分かった
    （langroid `LanceDocChatAgent.query_plan` → `VectorStore.compute_from_docs` の
    `eval`、PraisonAI の `acp_*` → `ActionOrchestrator._apply_step` の `subprocess.run`）。
    **効果を落とすと false-clean** なので、降りたうえで `opaque(unresolved)` を合流する。
    """
    res = _run(tmp_path, NAME_ONLY)
    spawns = _effects(_unit(res, "take_screenshot"), "SPAWN")
    assert all(e.resolution.kind == "opaque" and "unresolved" in e.resolution.reasons for e in spawns)


BY_NAME_TRUE_PATH = FASTMCP_HEAD + """\
class VectorStore:
    def compute_from_docs(self, docs, calc: str) -> str:
        return str(eval(calc))

class LanceDB(VectorStore):
    pass

class DocAgent:
    def __init__(self, config):
        self.vecdb = config.make_store()

    def query_plan(self, calc: str) -> str:
        return self.vecdb.compute_from_docs([], calc)

@mcp.tool()
def plan(calc: str) -> str:
    agent = DocAgent(None)
    return agent.query_plan(calc)
"""


def test_untyped_receiver_by_name_hop_keeps_effect(tmp_path):
    """受け手 `self.vecdb` の型が推論できなくても、名前で一意に決まる経路の EXEC は落とさない。"""
    u = _unit(_run(tmp_path, {"s.py": BY_NAME_TRUE_PATH}), "plan")
    execs = _effects(u, "EXEC")
    assert execs, "名前で一意に決まる木内メソッドの EXEC が消えた（false-clean）"
    assert all(e.resolution.kind == "opaque" for e in execs)


BRANCH_APPEND = FASTMCP_HEAD + """\
import subprocess

@mcp.tool()
def rewrite(pattern: str, path: str, dry_run: bool = True) -> str:
    cmd = ["sg", "--pattern", pattern]
    if not dry_run:
        cmd.append("--update-all")
    cmd.append(path)
    return subprocess.run(cmd, capture_output=True, text=True).stdout
"""


def test_branch_join_keeps_argv0_literal(tmp_path):
    """分岐で長さの違う列が合流しても、共通の先頭（argv0 の "sg"）は保つ（A9 で退行した形）。"""
    u = _unit(_run(tmp_path, {"s.py": BRANCH_APPEND}), "rewrite")
    argv0 = _slot(u, "SPAWN", "argv0")
    assert argv0.prin == Prin.OP and argv0.const == "sg"
    assert _slot(u, "SPAWN", "argv[*]").prin == Prin.MODEL


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
        pytest.param(MODULE_CONST, "search", id="module_constant"),
        pytest.param(ENV_MODULE, "issues", id="module_environ"),
        pytest.param(ENV_LOCAL, "token", id="local_environ"),
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


# ---------------------------------------------------------------------------
# 9. 0662b39 のレビューで再現した false-clean（D17 の修正が新たに作ったもの）
# ---------------------------------------------------------------------------

GLOBAL_REBOUND = FASTMCP_HEAD + """\
import subprocess

CMD = "echo hello"
ALLOWED_HOSTS = ["api.example.com"]

@mcp.tool()
def configure(cmd: str, host: str) -> str:
    global CMD
    CMD = cmd
    ALLOWED_HOSTS.append(host)
    return "ok"

@mcp.tool()
def run_it() -> str:
    return subprocess.run(CMD, shell=True, capture_output=True, text=True).stdout

@mcp.tool()
def first_host() -> str:
    import requests
    return requests.get("https://" + ALLOWED_HOSTS[0] + "/v1").text
"""


def test_global_rebound_precondition(tmp_path):
    res = _run(tmp_path, {"s.py": GLOBAL_REBOUND})
    assert _effects(_unit(res, "run_it"), "SPAWN")
    assert _effects(_unit(res, "first_host"), "NET")


def test_module_name_rebound_by_global_is_not_constant(tmp_path):
    """別のツールが `global CMD; CMD = cmd` で書き換える名前を定数（OP / resolved）にしない。

    モジュール直下の代入だけを読むと、MODEL の書き込みを見落として resolved の OP に
    なる（false-clean）。**書き込みのある名前は読まない**（従来の opaque(unresolved) に戻す）。
    """
    u = _unit(_run(tmp_path, {"s.py": GLOBAL_REBOUND}), "run_it")
    cmd = _slot(u, "SPAWN", "shell_string")
    assert not (cmd.prin == Prin.OP and cmd.prov.kind == "resolved")


def test_module_container_mutated_elsewhere_is_not_constant(tmp_path):
    """別のツールが `ALLOWED_HOSTS.append(host)` で変更する列を定数の列にしない。"""
    u = _unit(_run(tmp_path, {"s.py": GLOBAL_REBOUND}), "first_host")
    host = _slot(u, "NET", "url.host")
    assert not (host.prin == Prin.OP and host.prov.kind == "resolved")


URL_TEMPLATE = FASTMCP_HEAD + """\
import requests

@mcp.tool()
def fetch_pct(scheme: str, host: str) -> str:
    return requests.get("%s://%s/api" % (scheme, host)).text

@mcp.tool()
def fetch_fmt(host: str) -> str:
    return requests.get("https://{}/api".format(host)).text
"""


def test_url_template_precondition(tmp_path):
    res = _run(tmp_path, {"s.py": URL_TEMPLATE})
    assert _effects(_unit(res, "fetch_pct"), "NET")
    assert _effects(_unit(res, "fetch_fmt"), "NET")


@pytest.mark.parametrize("tool", ["fetch_pct", "fetch_fmt"])
def test_url_split_does_not_cut_host_from_template_placeholder(tmp_path, tool):
    """書式テンプレートの `%s` / `{}` を host のリテラルとして切り出さない（§2.6 の分割規則は
    **権威部の文字列そのものがリテラル**のときだけ OP にする）。"""
    u = _unit(_run(tmp_path, {"s.py": URL_TEMPLATE}), tool)
    host = _slot(u, "NET", "url.host")
    assert not (host.prin == Prin.OP and host.prov.kind == "resolved" and isinstance(host.const, str)
                and any(ph in host.const for ph in ("%", "{", "}")))


@pytest.mark.parametrize("tool", ["fetch_pct", "fetch_fmt"])
def test_url_template_host_is_not_op_resolved(tmp_path, tool):
    """**上のテストは弱すぎた**（プレースホルダの定数だけを見ていた）。host は MODEL なので、
    分割しなくても url.host が OP / resolved であってはならない。`.format` は TRANSFER 表が
    受け手（テンプレート）の主体しか採らず、実引数の MODEL を捨てていた（2 回目のレビュー）。"""
    u = _unit(_run(tmp_path, {"s.py": URL_TEMPLATE}), tool)
    host = _slot(u, "NET", "url.host")
    assert not (host.prin == Prin.OP and host.prov.kind == "resolved")


# ---------------------------------------------------------------------------
# 11. 854f71b（改訂 2）の 2 回目の敵対的レビューで再現した欠陥
# ---------------------------------------------------------------------------

MUTATED_MODULE_OBJECTS = FASTMCP_HEAD + """\
import sqlite3
import requests

conn = sqlite3.connect("app.db")
conn.row_factory = sqlite3.Row
session = requests.Session()
session.headers.update({"Authorization": "Bearer x"})

class Store:
    def __init__(self):
        self._db = sqlite3.connect("store.db")
        self.cache = {}

    def post(self, text):
        self._db.execute(text)

store = Store()

@mcp.tool()
def query_rows(sql: str) -> str:
    return str(conn.execute(sql).fetchall())

@mcp.tool()
def fetch(url: str) -> str:
    return session.get(url).text

@mcp.tool()
def reset_cache() -> str:
    store.cache.clear()
    return "ok"

@mcp.tool()
def post_message(msg: str) -> str:
    store.post(msg)
    return "ok"
"""


def test_mutated_module_objects_precondition(tmp_path):
    res = _run(tmp_path, {"s.py": MUTATED_MODULE_OBJECTS})
    for name in ("query_rows", "fetch", "post_message"):
        _unit(res, name)


@pytest.mark.parametrize(
    "tool,kind",
    [
        ("query_rows", "DB"),
        ("fetch", "NET"),
        ("post_message", "DB"),
    ],
)
def test_mutated_module_object_keeps_effect_rows(tmp_path, tool, kind):
    """属性やメソッドで変更されるモジュール水準のオブジェクトを「読まない」にすると受け手の型が
    消え、**効果行ごと消える**（opaque ではなく drop。false-clean）。型は保ち、確度だけ落とす。"""
    assert _effects(_unit(_run(tmp_path, {"s.py": MUTATED_MODULE_OBJECTS}), tool), kind)


RELATIVE_BASE = {
    "pkg/__init__.py": "",
    "pkg/base.py": "class Resource:\n    pass\n",
    "pkg/tools/__init__.py": "",
    "pkg/tools/base.py": """\
import sqlite3

class BaseTool:
    def __init__(self):
        self.conn = sqlite3.connect("tools.db")

    def run_query(self, sql):
        return self.conn.execute(sql).fetchall()
""",
    "pkg/tools/sqltool.py": """\
from .base import BaseTool

class SqlTool(BaseTool):
    def query(self, sql):
        return self.conn.execute(sql).fetchall()
""",
    "pkg/server.py": FASTMCP_HEAD + """\
from pkg.tools.sqltool import SqlTool

tool = SqlTool()

@mcp.tool()
def own_method(sql: str) -> str:
    return str(tool.query(sql))

@mcp.tool()
def inherited_method(sql: str) -> str:
    return str(tool.run_query(sql))
""",
}


def test_relative_base_precondition(tmp_path):
    res = _run(tmp_path, RELATIVE_BASE)
    _unit(res, "own_method")
    _unit(res, "inherited_method")


@pytest.mark.parametrize("tool", ["own_method", "inherited_method"])
def test_relative_import_base_init_fields_keep_effects(tmp_path, tool):
    """`from .base import BaseTool`（木に別の `pkg/base.py` もある）の基底の `__init__` が作る
    `self.conn` 経由の DB 効果を落とさない。import 表が相対 import の点を捨てるので、厳密化で
    別の `base` モジュールと区別できず基底が解決されなくなった（2 回目のレビュー）。"""
    assert _effects(_unit(_run(tmp_path, RELATIVE_BASE), tool), "DB")


TRANSFER_ARGS = FASTMCP_HEAD + """\
import os
import subprocess
import requests
from urllib.parse import urljoin

@mcp.tool()
def run_fmt_kw(d: str) -> str:
    return subprocess.run("ls {d}".format(d=d), shell=True, capture_output=True).stdout

@mcp.tool()
def read_join(name: str) -> str:
    return open(os.path.join("/data", name)).read()

@mcp.tool()
def fetch_join(url: str) -> str:
    return requests.get(urljoin("https://api.example.com/", url)).text

@mcp.tool()
def fetch_replace(host: str) -> str:
    return requests.get("https://HOST/api".replace("HOST", host)).text
"""


def test_transfer_args_precondition(tmp_path):
    res = _run(tmp_path, {"s.py": TRANSFER_ARGS})
    for name in ("run_fmt_kw", "read_join", "fetch_join", "fetch_replace"):
        _unit(res, name)


@pytest.mark.parametrize(
    "tool,kind,slot",
    [
        pytest.param("run_fmt_kw", "SPAWN", "shell_string", id="str_format_kwarg"),
        pytest.param("read_join", "FS_READ", "path", id="os_path_join_second_arg"),
        pytest.param("fetch_join", "NET", "url.host", id="urljoin_second_arg"),
        pytest.param("fetch_replace", "NET", "url.host", id="str_replace_new"),
    ],
)
def test_transfer_keeps_model_from_non_subject_args(tmp_path, tool, kind, slot):
    """TRANSFER 表の変換は subject 以外の実引数の主体も結果に入れる。捨てると MODEL が OP / resolved に
    なる（`"ls {d}".format(d=d)` が `"ls " + d` と違う結果になる）。"""
    v = _slot(_unit(_run(tmp_path, {"s.py": TRANSFER_ARGS}), tool), kind, slot)
    assert not (v.prin == Prin.OP and v.prov.kind == "resolved")


WRITE_ALIASES = {
    "helper/s.py": FASTMCP_HEAD + """\
import subprocess

SETTINGS = {"cmd": "echo ready"}

def _put(d, k, v):
    d[k] = v

@mcp.tool()
def set_setting(cmd: str) -> str:
    _put(SETTINGS, "cmd", cmd)
    return "ok"

@mcp.tool()
def run_helper_setting() -> str:
    return subprocess.run(SETTINGS["cmd"], shell=True, capture_output=True).stdout
""",
    "alias/s.py": FASTMCP_HEAD + """\
import subprocess

CONFIG = {"cmd": "echo ready"}
CMD = "echo ready"

@mcp.tool()
def set_alias(cmd: str) -> str:
    c = CONFIG
    c["cmd"] = cmd
    globals()["CMD"] = cmd
    return "ok"

@mcp.tool()
def run_alias_setting() -> str:
    return subprocess.run(CONFIG["cmd"], shell=True, capture_output=True).stdout

@mcp.tool()
def run_globals_cmd() -> str:
    return subprocess.run(CMD, shell=True, capture_output=True).stdout
""",
    "envalias/s.py": FASTMCP_HEAD + """\
import os
import subprocess

@mcp.tool()
def set_env_alias(cmd: str) -> str:
    env = os.environ
    env["TOOL_CMD"] = cmd
    return "ok"

@mcp.tool()
def run_env_alias() -> str:
    return subprocess.run(os.environ.get("TOOL_CMD", "true"), shell=True, capture_output=True).stdout
""",
}


def test_write_aliases_precondition(tmp_path):
    for sub, tool in (("helper", "run_helper_setting"), ("alias", "run_alias_setting"), ("envalias", "run_env_alias")):
        res = _run(tmp_path / sub, {"s.py": WRITE_ALIASES[f"{sub}/s.py"]})
        assert _effects(_unit(res, tool), "SPAWN")


@pytest.mark.parametrize(
    "sub,tool",
    [
        pytest.param("helper", "run_helper_setting", id="write_via_helper_function"),
        pytest.param("alias", "run_alias_setting", id="write_via_local_alias"),
        pytest.param("alias", "run_globals_cmd", id="write_via_globals"),
        pytest.param("envalias", "run_env_alias", id="environ_write_via_alias"),
    ],
)
def test_writes_through_aliases_are_not_constant(tmp_path, sub, tool):
    """構文上の根の名前だけでは書き込みを見落とす（補助関数の仮引数、局所別名、`globals()`、
    `env = os.environ`）。その名前の値を定数（OP / resolved）にしない。"""
    res = _run(tmp_path / sub, {"s.py": WRITE_ALIASES[f"{sub}/s.py"]})
    v = _slot(_unit(res, tool), "SPAWN", "shell_string")
    assert not (v.prin == Prin.OP and v.prov.kind == "resolved")


def test_deep_unrelated_file_does_not_crash_write_scan(tmp_path):
    """木の無関係なファイルに深い AST（550 項の連結）があっても、書き込み走査の再帰で
    RecursionError を出して木 1 本の出力を全部落とさない。"""
    deep = "BIG = " + " + ".join(['"a"'] * 550) + "\n"
    server = FASTMCP_HEAD + """\
import os
import subprocess

CMD = "ls"

@mcp.tool()
def run_it(arg: str) -> str:
    return subprocess.run([CMD, arg, os.environ.get("X", "")], capture_output=True).stdout.decode()
"""
    res = _run(tmp_path, {"server.py": server, "generated_strings.py": deep})
    assert _effects(_unit(res, "run_it"), "SPAWN")


URL_PREFIX_VAR = FASTMCP_HEAD + """\
import os
import requests

@mcp.tool()
def fetch_host(host: str) -> str:
    prefix = os.environ.get("PREFIX", "https://")
    return requests.get(f"{prefix}{host}/v1").text
"""


def test_url_prefix_var_precondition(tmp_path):
    assert _effects(_unit(_run(tmp_path, {"s.py": URL_PREFIX_VAR}), "fetch_host"), "NET")


def test_url_split_non_literal_first_needs_authority_end(tmp_path):
    """parts[0] が非リテラルでも、その直後が `/` `?` `#` で始まるリテラルでなければ
    権威部の終端が分からないので分割しない（`f"{prefix}{host}/v1"` の host は MODEL）。"""
    u = _unit(_run(tmp_path, {"s.py": URL_PREFIX_VAR}), "fetch_host")
    host = _slot(u, "NET", "url.host")
    assert not (host.prin == Prin.OP and host.prov.kind == "resolved")


ENV_WRITE = FASTMCP_HEAD + """\
import os
import subprocess

@mcp.tool()
def run_subscript(cmd: str) -> str:
    os.environ["USER_CMD"] = cmd
    return subprocess.run(os.environ["USER_CMD"], shell=True, capture_output=True, text=True).stdout

@mcp.tool()
def run_get(cmd: str) -> str:
    os.environ["USER_CMD"] = cmd
    return subprocess.run(os.environ.get("USER_CMD"), shell=True, capture_output=True, text=True).stdout
"""


def test_env_write_precondition(tmp_path):
    res = _run(tmp_path, {"s.py": ENV_WRITE})
    for name in ("run_subscript", "run_get"):
        assert _effects(_unit(res, name), "SPAWN")


@pytest.mark.parametrize("tool", ["run_subscript", "run_get"])
def test_env_read_after_model_write_is_not_config(tmp_path, tool):
    """`os.environ["K"] = cmd` の後の読み戻しを config（OP / resolved）にしない。"""
    u = _unit(_run(tmp_path, {"s.py": ENV_WRITE}), tool)
    cmd = _slot(u, "SPAWN", "shell_string")
    assert not (cmd.prin == Prin.OP and cmd.prov.kind == "resolved")


EXTERNAL_IMPORT_SAME_TAIL = {
    "app/server.py": FASTMCP_HEAD + """\
from requests.sessions import Session

@mcp.tool()
def fetch(url: str) -> str:
    s = Session()
    return url
""",
    "tools/sessions.py": """\
import subprocess

class Session:
    def __init__(self):
        subprocess.run(["rm", "-rf", "/tmp/cache"])
""",
}

EXTERNAL_BASE_SAME_NAME = {
    "app/server.py": FASTMCP_HEAD + """\
from pydantic import BaseModel

class Query(BaseModel):
    text: str

@mcp.tool()
def ask(text: str) -> str:
    q = Query(text)
    return q.text
""",
    "legacy/models.py": """\
import subprocess

class BaseModel:
    def __init__(self, *args):
        subprocess.run(["make", "clean"])
""",
}


def test_external_class_precondition(tmp_path):
    _unit(_run(tmp_path / "a", EXTERNAL_IMPORT_SAME_TAIL), "fetch")
    _unit(_run(tmp_path / "b", EXTERNAL_BASE_SAME_NAME), "ask")


def test_external_import_does_not_construct_intree_class_with_same_module_tail(tmp_path):
    """`from requests.sessions import Session` を木内の `tools/sessions.py` の Session と
    取り違えて `__init__` を実行しない（到達しない SPAWN を出さない）。"""
    u = _unit(_run(tmp_path, EXTERNAL_IMPORT_SAME_TAIL), "fetch")
    assert not _effects(u, "SPAWN")


def test_external_base_does_not_run_intree_init_with_same_name(tmp_path):
    """`class Query(pydantic.BaseModel)` の基底を木内の同名クラスと取り違えて `__init__` を実行しない。"""
    u = _unit(_run(tmp_path, EXTERNAL_BASE_SAME_NAME), "ask")
    assert not _effects(u, "SPAWN")


MODULE_WRITE_VARIANTS = {
    "srv/server.py": FASTMCP_HEAD + """\
import subprocess
import requests
from srv import cfg

COMMAND = "echo ready"
SETTINGS = {"cmd": "echo ready"}

@mcp.tool()
def nested_shadow(cmd: str) -> str:
    COMMAND = cmd
    def inner():
        return subprocess.run(COMMAND, shell=True, capture_output=True).stdout
    return inner()

@mcp.tool()
def set_setting(cmd: str) -> str:
    SETTINGS["cmd"] = cmd
    return "ok"

@mcp.tool()
def run_setting() -> str:
    return subprocess.run(SETTINGS["cmd"], shell=True, capture_output=True).stdout

@mcp.tool()
def set_base(url: str) -> str:
    cfg.BASE_URL = url
    return "ok"

@mcp.tool()
def fetch_base(path: str) -> str:
    return requests.get(cfg.BASE_URL + "/" + path).text
""",
    "srv/cfg.py": """\
BASE_URL = "https://api.example.com"
""",
    "srv/env_setter.py": FASTMCP_HEAD + """\
import os

@mcp.tool()
def set_env(cmd: str) -> str:
    os.environ["TOOL_CMD"] = cmd
    return "ok"
""",
    "srv/env_reader.py": FASTMCP_HEAD + """\
import os
import subprocess

@mcp.tool()
def run_env() -> str:
    return subprocess.run(os.environ.get("TOOL_CMD", "true"), shell=True, capture_output=True).stdout
""",
}


def test_module_write_variants_precondition(tmp_path):
    res = _run(tmp_path, MODULE_WRITE_VARIANTS)
    for name in ("run_setting", "run_env"):
        assert _effects(_unit(res, name), "SPAWN")
    assert _effects(_unit(res, "fetch_base"), "NET")
    _unit(res, "nested_shadow")


@pytest.mark.parametrize(
    "tool,kind,slot",
    [
        pytest.param("run_setting", "SPAWN", "shell_string", id="container_written_by_other_tool"),
        # 現状 `cfg.BASE_URL` 自体を解決しない（opaque のまま）ので欠陥ではなく**番人**。
        # モジュール属性を読むようにしたとき、他モジュールからの書き込みを見落とさないため。
        pytest.param("fetch_base", "NET", "url.host", id="module_attr_written_from_other_module"),
        pytest.param("run_env", "SPAWN", "shell_string", id="environ_written_in_other_module"),
    ],
)
def test_written_module_state_is_not_constant(tmp_path, tool, kind, slot):
    """木内のどこかで書き換えられるモジュール水準の状態（コンテナ・モジュール属性・環境変数）を
    読み手のユニットで定数（OP / resolved）にしない（レビューの検証者が見つけた変形）。"""
    v = _slot(_unit(_run(tmp_path, MODULE_WRITE_VARIANTS), tool), kind, slot)
    assert not (v.prin == Prin.OP and v.prov.kind == "resolved")


def test_nested_function_outer_local_shadows_module_constant(tmp_path):
    """入れ子関数が読む `COMMAND` は外側関数の局所変数（MODEL）であり、同名のモジュール定数ではない。"""
    u = _unit(_run(tmp_path, MODULE_WRITE_VARIANTS), "nested_shadow")
    for e in _effects(u, "SPAWN"):
        v = e.control_slots().get("shell_string")
        assert v is None or not (v.prin == Prin.OP and v.prov.kind == "resolved")


# ---------------------------------------------------------------------------
# 10. 末尾名の木全体検索が、同名の関数が別ファイルに増えただけで解決を失う（run 3 で発見）
# ---------------------------------------------------------------------------

SAME_NAME_TWO_MODULES = {
    "api/spotify_api.py": """\
import requests

def get_followed_artists(token, max_artists=50):
    return requests.get("https://api.example.com/me/following", headers={"Authorization": token}).json()

def _token():
    return "t"
""",
    "bot/chatbot_agent.py": FASTMCP_HEAD + """\
import spotify_api as sp

def _helper(q):
    import requests
    return requests.get("https://search.example/?q=" + q).text

@mcp.tool()
def followed(limit: int) -> str:
    return str(sp.get_followed_artists("t", max_artists=limit))

@mcp.tool()
def search(q: str) -> str:
    return _helper(q)
""",
    # 同じ名前の関数を持つ別のファイル（野外では BOM を直して parse できるようになったファイル）
    "bot/mcp_server.py": """\
def get_followed_artists():
    return "local"

def _helper(q):
    return q
""",
}


def test_same_name_two_modules_precondition(tmp_path):
    res = _run(tmp_path, SAME_NAME_TWO_MODULES)
    _unit(res, "followed")
    _unit(res, "search")


def test_module_alias_call_resolves_in_imported_module(tmp_path):
    """`import spotify_api as sp; sp.get_followed_artists(...)` は import 先のモジュールの
    関数である。末尾名だけで木全体を引くと、別ファイルの同名関数と衝突して解決を失い、
    NET 効果が消える（run 3 の w-jitz10__spotify_mcp で 6 ユニット、false-clean）。"""
    assert _effects(_unit(_run(tmp_path, SAME_NAME_TWO_MODULES), "followed"), "NET")


def test_bare_call_prefers_same_module_definition(tmp_path):
    """局所束縛も import も無い素の名前 `_helper(q)` は、同じモジュールの定義を指す。"""
    assert _effects(_unit(_run(tmp_path, SAME_NAME_TWO_MODULES), "search"), "NET")


# ---------------------------------------------------------------------------
# 12. tools_list の入れ子関数を拾うようにしたことで、同じ関数が 2 ユニットに数えられる（run 3 で発見）
# ---------------------------------------------------------------------------

#: 野外（w-giak__mnemo-lite の api/mnemo_mcp/server.py:2098 と :2145）と同じ形。登録した
#: ツール名を**ログの `tools=[...]` キーワード**に並べるので、tools_list 規則がこれを拾う。
REGISTERED_AND_LISTED = FASTMCP_HEAD + """\
import logging
import sqlite3

logger = logging.getLogger(__name__)

def register_indexing_components(server):
    @server.tool()
    async def get_indexing_errors(repository: str, limit: int = 50) -> str:
        conn = sqlite3.connect("idx.db")
        return str(conn.execute("SELECT * FROM errors WHERE repo = ?", (repository,)).fetchall())

    logger.info(
        "mcp.components.indexing.registered",
        tools=["get_indexing_status", "get_indexing_errors", "retry_indexing"],
    )

register_indexing_components(mcp)
"""


def test_registered_and_listed_precondition(tmp_path):
    res = _run(tmp_path, {"server.py": REGISTERED_AND_LISTED})
    assert [u for u in res.tree.units if u.unit.tool_name == "get_indexing_errors"]


def test_function_registered_by_decorator_and_listed_is_one_unit(tmp_path):
    """デコレータで登録されたツール関数が、同じファイルの `tools` の文字列リストにも名前が出るとき、
    **1 つのユニット**として数える。`find_tools_list_units` の既出判定が qualname と末尾名を
    比べていたので、入れ子関数（qualname は `外側.内側`）は既出と判定されず、`mcp` と
    `tools-list` の 2 ユニットになっていた（ユニット数と危険効果ユニット数の過大計上）。"""
    _unit(_run(tmp_path, {"server.py": REGISTERED_AND_LISTED}), "get_indexing_errors")


# ---------------------------------------------------------------------------
# 13. 8f24cbd（改訂 3）の 3 回目の敵対的レビュー: _pinned_function が再定義と入れ子の束縛を見ない
# ---------------------------------------------------------------------------

PIN_OVERLOAD = FASTMCP_HEAD + """\
import subprocess
from typing import overload

@overload
def build_command(cmd: str) -> str: ...
@overload
def build_command(cmd: list) -> str: ...
def build_command(cmd):
    return cmd if isinstance(cmd, str) else " ".join(cmd)

@mcp.tool()
def run_cmd(cmd: str) -> str:
    return subprocess.run(build_command(cmd), shell=True, capture_output=True, text=True).stdout
"""

PIN_REDEFINED = FASTMCP_HEAD + """\
import subprocess

def normalize(cmd):
    return "true"

def normalize(cmd):
    return cmd.strip()

@mcp.tool()
def run_cmd(cmd: str) -> str:
    subprocess.run(normalize(cmd), shell=True)
    return "ok"
"""

PIN_IF_ELSE = FASTMCP_HEAD + """\
import subprocess
import sys

if sys.platform == "win32":
    def normalize(cmd):
        return "cmd /c exit 0"
else:
    def normalize(cmd):
        return cmd.strip()

@mcp.tool()
def run_cmd(cmd: str) -> str:
    subprocess.run(normalize(cmd), shell=True)
    return "ok"
"""

PIN_IMPORT_SHADOWED = {
    "app/__init__.py": "",
    "app/helpers.py": "def normalize(cmd):\n    return \"true\"\n",
    "app/server.py": FASTMCP_HEAD + """\
import subprocess
from .helpers import normalize

def normalize(cmd):
    return cmd.strip()

@mcp.tool()
def run_cmd(cmd: str) -> str:
    subprocess.run(normalize(cmd), shell=True)
    return "ok"
""",
}

PIN_NESTED_HANDLER = """\
import subprocess
from mcp.server import Server

def prepare(cmd):
    return "echo ready"

async def serve():
    server = Server("x")

    def prepare(cmd):
        return cmd

    @server.call_tool()
    async def call_tool(name, arguments):
        subprocess.run(prepare(arguments["cmd"]), shell=True)
        return []
"""


def _pin_files(form: str) -> dict:
    return {
        "overload": {"s.py": PIN_OVERLOAD},
        "redefined": {"s.py": PIN_REDEFINED},
        "if_else": {"s.py": PIN_IF_ELSE},
        "import_shadowed": PIN_IMPORT_SHADOWED,
    }[form]


def test_pin_forms_precondition(tmp_path):
    for form in ("overload", "redefined", "if_else", "import_shadowed"):
        assert _effects(_unit(_run(tmp_path / form, _pin_files(form)), "run_cmd"), "SPAWN")
    res = _run(tmp_path / "nested", {"server.py": PIN_NESTED_HANDLER})
    handlers = [u for u in res.tree.units if u.unit.qualname == "serve.call_tool"]
    assert handlers and _effects(handlers[0], "SPAWN")


@pytest.mark.parametrize(
    "form",
    [
        "overload",
        "redefined",
        "if_else",
        "import_shadowed",
    ],
)
def test_pinned_call_does_not_pick_one_of_several_definitions(tmp_path, form):
    """同じモジュールに同名の定義が複数ある（`@overload` のスタブ、単純な再定義、if / else の def、
    import を上書きするローカル def）とき、最初の 1 つに決め打ちしない。索引は module 付きの引きで
    最初の定義しか返さないので、「一意」の判定が空回りしていた（3 回目のレビュー）。"""
    u = _unit(_run(tmp_path, _pin_files(form)), "run_cmd")
    v = _slot(u, "SPAWN", "shell_string")
    assert not (v.prin == Prin.OP and v.prov.kind == "resolved")


def test_pinned_bare_name_respects_enclosing_function_definition(tmp_path):
    """`serve()` の中の低レベル MCP ハンドラが呼ぶ `prepare(...)` は `serve.prepare` であって、
    モジュール直下の同名の `prepare` ではない（Python のスコープ規則）。"""
    res = _run(tmp_path, {"server.py": PIN_NESTED_HANDLER})
    u = [u for u in res.tree.units if u.unit.qualname == "serve.call_tool"][0]
    v = _slot(u, "SPAWN", "shell_string")
    assert not (v.prin == Prin.OP and v.prov.kind == "resolved")


MODULE_OBJECTS_WITH_EXEC = FASTMCP_HEAD + """\
import sqlite3
import httpx

client = httpx.Client()
conn = sqlite3.connect("app.db")

@mcp.tool()
def fetch(url: str) -> str:
    return client.get(url).text

@mcp.tool()
def query(sql: str) -> str:
    return str(conn.execute(sql).fetchall())

@mcp.tool()
def run_python(code: str) -> str:
    exec(code)
    return "ok"

def show_config():
    return str(globals().get("VERSION"))
"""


def test_module_objects_with_exec_precondition(tmp_path):
    res = _run(tmp_path, {"s.py": MODULE_OBJECTS_WITH_EXEC})
    for name in ("fetch", "query", "run_python"):
        _unit(res, name)


@pytest.mark.parametrize("tool,kind", [("fetch", "NET"), ("query", "DB")])
def test_dynamic_namespace_module_keeps_object_effect_rows(tmp_path, tool, kind):
    """`exec` / `globals()` を含むモジュールでも、モジュール水準のオブジェクトを受け手にする効果行を
    落とさない。改訂 3 の `"*"`（どの名前も再束縛されうる）が名前を読まない側に倒したので、受け手の型が
    消えて DB / NET の行ごと消えていた（3 回目のレビュー、2 観点が独立に指摘）。"""
    assert _effects(_unit(_run(tmp_path, {"s.py": MODULE_OBJECTS_WITH_EXEC}), tool), kind)


def test_deep_expression_read_by_tool_does_not_crash_tree(tmp_path):
    """tool が 550 項の連結式を読んでも、val エンジンの `_eval` の再帰で RecursionError を出して
    木 1 本の出力（無関係な tool の行を含む）を全部落とさない。"""
    deep = "BIG = " + " + ".join(['"a"'] * 550) + "\n"
    server = FASTMCP_HEAD + """\
import subprocess
from generated_strings import BIG

@mcp.tool()
def run_big(cmd: str) -> str:
    return subprocess.run(BIG + cmd, shell=True).stdout

@mcp.tool()
def other(cmd: str) -> str:
    return subprocess.run(cmd, shell=True).stdout
"""
    res = _run(tmp_path, {"server.py": server, "generated_strings.py": deep})
    assert _effects(_unit(res, "other"), "SPAWN")
    assert _effects(_unit(res, "run_big"), "SPAWN")


FORMAT_CONSTANT_HOST = FASTMCP_HEAD + """\
import requests

@mcp.tool()
def fmt(owner: str, repo: str):
    return requests.get("https://api.github.com/repos/{}/{}".format(owner, repo))

@mcp.tool()
def fmtkw(city: str):
    return requests.get("https://api.weather.com/v1/{city}".format(city=city))
"""


def test_format_constant_host_precondition(tmp_path):
    res = _run(tmp_path, {"s.py": FORMAT_CONSTANT_HOST})
    assert _effects(_unit(res, "fmt"), "NET")
    assert _effects(_unit(res, "fmtkw"), "NET")


@pytest.mark.parametrize(
    "tool,host",
    [("fmt", "api.github.com"), ("fmtkw", "api.weather.com")],
)
def test_format_template_with_literal_authority_splits_host(tmp_path, tool, host):
    """権威部の終端が最初のプレースホルダより前のリテラルにある `.format` テンプレートは、f 文字列と
    同じく url.host = OP の定数に分割し、MODEL は url.path に残す（§2.6 の分割規則。改訂 3 が形を
    丸ごと捨てたので host が MODEL になっていた。3 回目のレビュー、精度の損失）。"""
    u = _unit(_run(tmp_path, {"s.py": FORMAT_CONSTANT_HOST}), tool)
    h = _slot(u, "NET", "url.host")
    assert h.prin == Prin.OP and h.const == host
    assert _slot(u, "NET", "url.path").prin == Prin.MODEL


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


# ---------------------------------------------------------------------------
# 14. ea35672（改訂 4）の 4 回目の敵対的レビュー:
#     (a) opaque に落としたモジュール値の定数を、効果側がリテラルとして読む（false-clean）
#     (b) 同名の定義が複数あると被呼び出しへ降りず、helper の中の効果行が消える（行の消失）
# ---------------------------------------------------------------------------

_REBOUND_URL_HEAD = FASTMCP_HEAD + """\
import requests

BASE_URL = "https://api.example.com/v1"
TEMPLATE = "https://api.github.com/repos/{}"
"""

_REBOUND_URL_SETTER = """
@mcp.tool()
def set_base(url: str, template: str) -> str:
    global BASE_URL, TEMPLATE
    BASE_URL = url
    TEMPLATE = template
    return "ok"
"""

_REBOUND_URL_READERS = """
@mcp.tool()
def fetch_whole() -> str:
    return requests.get(BASE_URL).text

@mcp.tool()
def fetch_concat(path: str) -> str:
    return requests.get(BASE_URL + "/items/" + path).text

@mcp.tool()
def fetch_fstr(path: str) -> str:
    return requests.get(f"{BASE_URL}/items/{path}").text

@mcp.tool()
def fetch_fmt(repo: str) -> str:
    return requests.get(TEMPLATE.format(repo)).text
"""

_REBOUND_STAR_HEAD = FASTMCP_HEAD + """\
import requests

API = "https://api.example.com/v1/"

@mcp.tool()
def get_item(path: str) -> str:
    return requests.get(API + path).text
"""

_REBOUND_STAR_EXEC = """
@mcp.tool()
def run_python(code: str) -> str:
    exec(code, globals())
    return "ok"
"""

_REBOUND_IMPORT_SERVER_HEAD = FASTMCP_HEAD + """\
import requests
from .config import BASE

@mcp.tool()
def get_item(path: str) -> str:
    return requests.get(BASE + path).text
"""

_REBOUND_IMPORT_SETTER = """
@mcp.tool()
def set_base(base: str) -> str:
    global BASE
    BASE = base
    return "ok"
"""


_REBOUND_PARTS_HEAD = FASTMCP_HEAD + """\
import requests

HOST = "https://api.example.com"
VERSION = "/v1"
BASE = HOST + VERSION
FBASE = f"{HOST}/v2"
"""

_REBOUND_PARTS_SETTER = """
@mcp.tool()
def set_base(url: str) -> str:
    global BASE, FBASE
    BASE = url
    FBASE = url
    return "ok"
"""

_REBOUND_PARTS_READERS = """
@mcp.tool()
def get_concat(path: str) -> str:
    return requests.get(BASE + "/" + path).text

@mcp.tool()
def get_fstr(path: str) -> str:
    return requests.get(FBASE + "/" + path).text
"""


def _rebound_url_files(form: str, rebound: bool) -> tuple[dict, tuple[str, ...]]:
    """`(ファイル, NET を読む tool)`。`rebound=False` は書き換えの無い対照。"""
    if form == "global":
        body = _REBOUND_URL_HEAD + (_REBOUND_URL_SETTER if rebound else "") + _REBOUND_URL_READERS
        return {"s.py": body}, ("fetch_whole", "fetch_concat", "fetch_fstr", "fetch_fmt")
    if form == "parts":
        # 再束縛される名前の値が、別のモジュール定数を連結した Str（part ごとに確度を持つ）である形
        body = _REBOUND_PARTS_HEAD + (_REBOUND_PARTS_SETTER if rebound else "") + _REBOUND_PARTS_READERS
        return {"s.py": body}, ("get_concat", "get_fstr")
    if form == "star":
        return {"s.py": _REBOUND_STAR_HEAD + (_REBOUND_STAR_EXEC if rebound else "")}, ("get_item",)
    return {
        "app/__init__.py": "",
        "app/config.py": 'BASE = "https://api.example.com/"\n',
        "app/server.py": _REBOUND_IMPORT_SERVER_HEAD + (_REBOUND_IMPORT_SETTER if rebound else ""),
    }, ("get_item",)


def test_rebound_url_precondition(tmp_path):
    """書き換えが無ければ、どの形も url.host を OP の定数に分割する（分割の経路に届いている）。
    書き換えのある fixture でも NET 行は出る（ユニットと sink は見つかっている）。"""
    for form in ("global", "parts", "star", "import"):
        files, tools = _rebound_url_files(form, rebound=False)
        res = _run(tmp_path / form / "control", files)
        for tool in tools:
            h = _slot(_unit(res, tool), "NET", "url.host")
            assert h.prin == Prin.OP and h.prov.kind == "resolved" and h.const, (form, tool)
        files, tools = _rebound_url_files(form, rebound=True)
        res = _run(tmp_path / form / "rebound", files)
        for tool in tools:
            assert _effects(_unit(res, tool), "NET"), (form, tool)


@pytest.mark.parametrize(
    "form,tool",
    [
        ("global", "fetch_whole"),
        ("global", "fetch_concat"),
        ("global", "fetch_fstr"),
        ("global", "fetch_fmt"),
        ("parts", "get_concat"),
        ("parts", "get_fstr"),
        ("star", "get_item"),
        ("import", "get_item"),
    ],
)
def test_rebound_module_url_is_not_split_into_op_resolved_host(tmp_path, form, tool):
    """MODEL が `global` / `exec(..., globals())` / 読む側の再束縛で書き換えるベース URL から、
    §2.6 の分割で url.host = OP / resolved の定数を切り出さない。改訂 4 は再束縛される名前を
    「型と主体を保ったまま opaque」で読むようにしたが、`_opaque_deep` が定数を残し、`_split_url` が
    その定数から確度を捨てて RESOLVED の host を作っていた（4 回目のレビュー、2 観点が独立に指摘）。"""
    files, _tools = _rebound_url_files(form, rebound=True)
    u = _unit(_run(tmp_path, files), tool)
    rows = _effects(u, "NET")
    assert rows
    for e in rows:
        h = e.control_slots().get("url.host")
        assert h is not None
        assert not (h.prin == Prin.OP and h.prov.kind == "resolved")
        assert e.resolution.kind != "resolved"


REBOUND_MODES = FASTMCP_HEAD + """\
import subprocess

USE_SHELL = False
MODE = "r"

@mcp.tool()
def configure(use_shell: bool, mode: str) -> str:
    global USE_SHELL, MODE
    USE_SHELL = use_shell
    MODE = mode
    return "ok"

@mcp.tool()
def run_cmd(cmd: str) -> str:
    return subprocess.run(cmd, shell=USE_SHELL, capture_output=True, text=True).stdout

@mcp.tool()
def touch(path: str) -> str:
    with open(path, MODE) as f:
        return "ok"
"""


def test_rebound_modes_precondition(tmp_path):
    res = _run(tmp_path, {"s.py": REBOUND_MODES})
    assert _effects(_unit(res, "run_cmd"), "SPAWN")
    assert _effects(_unit(res, "touch"), "FS_READ")


def test_rebound_shell_flag_keeps_shell_string_row(tmp_path):
    """`shell=USE_SHELL` の USE_SHELL を MODEL が書き換えるなら、shell=True 側の行（shell_string）を
    落とさない。opaque に落とした値の定数 False を `_exec_mode` がリテラルとして読み、SPAWN 行の
    片側が消えていた（4 回目のレビュー、false-clean）。"""
    rows = _effects(_unit(_run(tmp_path, {"s.py": REBOUND_MODES}), "run_cmd"), "SPAWN")
    assert any("shell_string" in e.control_slots() for e in rows)


def test_rebound_open_mode_keeps_fs_write_row(tmp_path):
    """`open(path, MODE)` の MODE を MODEL が書き換えるなら、FS_WRITE の行を落とさない
    （`_mode_is_write` が opaque の定数 "r" を読んでいた。4 回目のレビュー、false-clean）。"""
    assert _effects(_unit(_run(tmp_path, {"s.py": REBOUND_MODES}), "touch"), "FS_WRITE")


_PIN_SINK_HELPER = """\
import subprocess

def run_command(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout
"""

_PIN_SINK_TOOL = """
@mcp.tool()
def shell(cmd: str) -> str:
    return run_command(cmd)
"""

_PIN_UNRELATED_NESTED = """
def build_cli():
    def run_command(args):
        return args
    return run_command
"""

PIN_SINK_IF_ELSE = FASTMCP_HEAD + """\
import subprocess
import sys

if sys.platform == "win32":
    def run_command(cmd):
        return subprocess.run(["cmd", "/c", cmd]).stdout
else:
    def run_command(cmd):
        return subprocess.run(cmd, shell=True).stdout

@mcp.tool()
def shell(cmd: str) -> str:
    return run_command(cmd)
"""

PIN_SINK_IF_ONLY = FASTMCP_HEAD + """\
import subprocess

def run_command(cmd):
    return subprocess.run(cmd, shell=True).stdout

@mcp.tool()
def shell(cmd: str) -> str:
    return run_command(cmd)
"""


def _pin_sink_files(form: str, control: bool) -> dict:
    """helper の中に sink がある形。`control=True` は同名の余分な定義を除いた対照。"""
    extra = "" if control else _PIN_UNRELATED_NESTED
    if form == "nested_unrelated":
        return {"server.py": FASTMCP_HEAD + _PIN_SINK_HELPER + _PIN_SINK_TOOL + extra}
    if form == "if_else":
        return {"server.py": PIN_SINK_IF_ONLY if control else PIN_SINK_IF_ELSE}
    if form == "import_nested_unrelated":
        return {
            "helpers.py": _PIN_SINK_HELPER,
            "server.py": FASTMCP_HEAD + "from helpers import run_command\n" + _PIN_SINK_TOOL + extra,
        }
    # module_attr_nested: `helpers.run_command(...)` と、helpers.py の別の関数の中の同名 def
    helper_extra = "" if control else "\ndef make_runner():\n    def run_command(cmd):\n        return cmd\n    return run_command\n"
    return {
        "helpers.py": _PIN_SINK_HELPER + helper_extra,
        "server.py": FASTMCP_HEAD + """\
import helpers

@mcp.tool()
def shell(cmd: str) -> str:
    return helpers.run_command(cmd)
""",
    }


_PIN_SINK_FORMS = ["nested_unrelated", "if_else", "import_nested_unrelated", "module_attr_nested"]


def test_pin_sink_forms_precondition(tmp_path):
    """余分な同名の定義が無ければ、helper の中の shell=True の SPAWN 行が出る。"""
    for form in _PIN_SINK_FORMS:
        u = _unit(_run(tmp_path / form, _pin_sink_files(form, control=True)), "shell")
        assert any("shell_string" in e.control_slots() for e in _effects(u, "SPAWN")), form


@pytest.mark.parametrize("form", _PIN_SINK_FORMS)
def test_same_name_definitions_do_not_drop_helper_effect_rows(tmp_path, form):
    """呼び出し側から見えない同名の入れ子 def（別の関数の中）、if / else の 2 つの def、import した名前と
    読む側の無関係な入れ子 def、モジュール属性越しの呼び出しと helper 側の入れ子 def。どの形でも
    helper の中の shell=True の SPAWN 行を落とさない。改訂 4 の `_pinned_function` はモジュール内の
    同名の def を入れ子まで数えて pin をやめ、末尾名の木全体検索も 2 候補で降りなかった
    （4 回目のレビュー、8f24cbd では出ていた行が消えた）。"""
    u = _unit(_run(tmp_path, _pin_sink_files(form, control=False)), "shell")
    assert any("shell_string" in e.control_slots() for e in _effects(u, "SPAWN"))


def test_if_else_definitions_keep_rows_of_both_branches_as_opaque(tmp_path):
    """どちらの def が効くかを決めない（flow-insensitive）。両方の分岐の SPAWN 行を出し、
    どれを採ったかが名前だけで決まらないので行の確度は resolved にしない。"""
    u = _unit(_run(tmp_path, _pin_sink_files("if_else", control=False)), "shell")
    rows = _effects(u, "SPAWN")
    assert any("shell_string" in e.control_slots() for e in rows)
    argv0 = [e.control_slots()["argv0"] for e in rows if "argv0" in e.control_slots()]
    assert any(v.shape.const == "cmd" for v in argv0 if hasattr(v.shape, "const"))
    assert all(e.resolution.kind != "resolved" for e in rows)


CONTAINER_TEMPLATE_URL = FASTMCP_HEAD + """\
import requests

ENDPOINTS = {"weather": "https://api.weather.com/v1/{}", "search": "https://api.search.com/v1/"}

@mcp.tool()
def register(name: str, tmpl: str) -> str:
    ENDPOINTS[name] = tmpl
    return "ok"

@mcp.tool()
def call_fmt(q: str) -> str:
    return requests.get(ENDPOINTS["weather"].format(q)).text

@mcp.tool()
def call_plus(q: str) -> str:
    return requests.get(ENDPOINTS["search"] + q).text
"""


def test_container_template_url_precondition(tmp_path):
    res = _run(tmp_path, {"s.py": CONTAINER_TEMPLATE_URL})
    for tool in ("call_fmt", "call_plus"):
        assert _slot(_unit(res, tool), "NET", "url.host") is not None


@pytest.mark.parametrize("tool", ["call_fmt", "call_plus"])
def test_mutable_container_url_template_is_not_split_into_op_resolved_host(tmp_path, tool):
    """tool が `ENDPOINTS[name] = tmpl` で差し替えるモジュール水準の dict の要素は opaque（改訂 3 / 4 の
    `_opaque_deep`）。その定数から url.host = OP / resolved を切り出さない。`.format` の形は改訂 4 の
    テンプレート先頭の part（確度を捨てて RESOLVED で作る）で入った退行、`+` の形は 8f24cbd の時点から
    ある同じ根（分割が part の確度を見ない）の欠陥（4 回目のレビュー、精度の観点が false-clean として指摘）。"""
    u = _unit(_run(tmp_path, {"s.py": CONTAINER_TEMPLATE_URL}), tool)
    for e in _effects(u, "NET"):
        h = e.control_slots().get("url.host")
        assert h is not None
        assert not (h.prin == Prin.OP and h.prov.kind == "resolved")


# ---------------------------------------------------------------------------
# 15. 150e06a（改訂 5）の 5 回目（最後）の敵対的レビューで確認された既知の欠陥（D19(3)）
#     **直さない。** レビューと修正の繰り返しを止め、向きと件数つきで報告する
#     （`docs/decisions.md` D19 の「結果」）。F0a 標本の 98 木には、どの形も構文上の候補が 0 件。
#     印は、将来直したときに XPASS で知らせるためのもの。
# ---------------------------------------------------------------------------

KNOWN = pytest.mark.xfail(
    strict=True, reason="D19: 5 回目のレビューで確認した既知の欠陥（直さずに報告する。直したら印を外す）"
)

PIPE_ARGV0_FROM_MODULE_LIST = FASTMCP_HEAD + """\
import subprocess

PYTHON_REPL = ["python3", "-i", "-q"]

@mcp.tool()
def run_python(code: str) -> str:
    proc = subprocess.Popen(PYTHON_REPL, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, _ = proc.communicate(input=code.encode())
    return out.decode()

@mcp.tool()
def run_python_literal(code: str) -> str:
    proc = subprocess.Popen(["python3", "-i", "-q"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, _ = proc.communicate(input=code.encode())
    return out.decode()
"""

PIPE_SHELL_FROM_REBOUND_NAME = FASTMCP_HEAD + """\
import subprocess

USE_SHELL = True

@mcp.tool()
def configure(flag: bool) -> str:
    global USE_SHELL
    USE_SHELL = flag
    return "ok"

@mcp.tool()
def run_script(script: str) -> str:
    proc = subprocess.Popen("cat", shell=USE_SHELL, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, _ = proc.communicate(input=script.encode())
    return out.decode()

@mcp.tool()
def run_script_literal(script: str) -> str:
    proc = subprocess.Popen("cat", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, _ = proc.communicate(input=script.encode())
    return out.decode()
"""


def test_known_pipe_precondition(tmp_path):
    """argv0 / shell が resolved のリテラルなら pipe 書き込みは EXEC(code_text) になり、opaque の形でも
    pipe の行（FS_WRITE）までは出る（pipe の経路に届いている）。"""
    res = _run(tmp_path / "argv0", {"s.py": PIPE_ARGV0_FROM_MODULE_LIST})
    assert _effects(_unit(res, "run_python_literal"), "EXEC")
    assert _effects(_unit(res, "run_python"), "FS_WRITE")
    res = _run(tmp_path / "shell", {"s.py": PIPE_SHELL_FROM_REBOUND_NAME})
    assert _effects(_unit(res, "run_script_literal"), "EXEC")
    assert _effects(_unit(res, "run_script"), "FS_WRITE")


@KNOWN
@pytest.mark.parametrize("fixture,tool", [("argv0", "run_python"), ("shell", "run_script")])
def test_known_pipe_with_undecidable_spawn_keeps_exec_row(tmp_path, fixture, tool):
    """spawn の argv0 / shell が opaque の値（改訂 4 から常に opaque のモジュール水準のリスト、`global` で
    書き換えられる名前）だと、`_pipe` は判定できないのに FS_WRITE の側だけを出し、EXEC(code_text) 行が
    消える（**効果行の消失**、改訂 5 の退行: 170a7b2 は opaque の定数を読んで EXEC を出していた）。
    `_exec_mode` / `_mode_is_write` と違い、判定できないときに両方の行を出す分岐が無い。"""
    src = PIPE_ARGV0_FROM_MODULE_LIST if fixture == "argv0" else PIPE_SHELL_FROM_REBOUND_NAME
    assert _effects(_unit(_run(tmp_path, {"s.py": src}), tool), "EXEC")


KNOWN_SCOPE_FORMS = {
    "global_nested_def": {
        "server.py": FASTMCP_HEAD + """\
import subprocess

def run_command(cmd):
    return subprocess.run(["echo", "disabled"], capture_output=True).stdout

def enable_shell():
    global run_command
    def run_command(cmd):
        return subprocess.run(cmd, shell=True, capture_output=True).stdout

@mcp.tool()
def enable() -> str:
    enable_shell()
    return "ok"

@mcp.tool()
def shell(cmd: str) -> str:
    return run_command(cmd)
"""
    },
    "global_assign": {
        "server.py": FASTMCP_HEAD + """\
import subprocess

def _shell_runner(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True).stdout

def run_command(cmd):
    return subprocess.run(["echo", "disabled"], capture_output=True).stdout

@mcp.tool()
def enable() -> str:
    global run_command
    run_command = _shell_runner
    return "ok"

@mcp.tool()
def shell(cmd: str) -> str:
    return run_command(cmd)
"""
    },
    "method_nested_def": {
        "server.py": """\
import subprocess
from mcp.server import Server

def run_command(cmd):
    return subprocess.run(["echo", cmd], capture_output=True).stdout

class App:
    def __init__(self):
        self.server = Server("t")

    def register(self):
        def run_command(cmd):
            return subprocess.run(cmd, shell=True, capture_output=True).stdout

        @self.server.call_tool()
        async def call_tool(name, arguments):
            return run_command(arguments["cmd"])
"""
    },
    "enclosing_import": {
        "helpers_shell.py": (
            "import subprocess\n\ndef run_command(cmd):\n"
            "    return subprocess.run(cmd, shell=True, capture_output=True).stdout\n"
        ),
        "server.py": """\
import subprocess
from mcp.server import Server

def run_command(cmd):
    return subprocess.run(["echo", cmd], capture_output=True).stdout

async def serve():
    from helpers_shell import run_command
    server = Server("t")

    @server.call_tool()
    async def call_tool(name, arguments):
        return run_command(arguments["cmd"])
""",
    },
}


def _known_scope_unit(res, form: str):
    if form in ("global_nested_def", "global_assign"):
        return _unit(res, "shell")
    qual = "App.register.call_tool" if form == "method_nested_def" else "serve.call_tool"
    found = [u for u in res.tree.units if u.unit.qualname == qual]
    assert len(found) == 1, [u.unit.qualname for u in res.tree.units]
    return found[0]


def test_known_scope_forms_precondition(tmp_path):
    """ユニットが見つかり、呼び出しはどれかの run_command へ降りている（SPAWN 行が出る）。"""
    for form, files in KNOWN_SCOPE_FORMS.items():
        assert _effects(_known_scope_unit(_run(tmp_path / form, files), form), "SPAWN"), form


@KNOWN
@pytest.mark.parametrize("form", sorted(KNOWN_SCOPE_FORMS))
def test_known_scope_rebinding_does_not_pin_resolved_safe_def(tmp_path, form):
    """呼び出し名がモジュール直下の def 以外でも束縛される形で、モジュール直下の安全な def に resolved で
    決め打ちしない（shell=True 側の行を出すか、少なくとも残る行を resolved にしない）。いまは shell=True 側を
    落とし、echo 側の行を resolved で出す（**false-clean**）:

    - global_nested_def: 関数内の `global run_command` と入れ子 def（改訂 5 の退行。170a7b2 は同名の入れ子 def で
      pin をやめて降りず、行 0 / opaque(unresolved) だった）
    - global_assign: 関数内の `global run_command; run_command = _shell_runner`（改訂 5 より前から）
    - method_nested_def: メソッドの中の入れ子 def（classname が付くので候補から外れる。改訂 5 より前から）
    - enclosing_import: 囲む関数の局所 import（改訂 5 より前から）

    `_pinned_candidates` は、`_scan_module_writes` が集めている `global` 宣言も、囲む関数の局所 import も、
    メソッドの中の入れ子 def も競合として見ない。"""
    u = _known_scope_unit(_run(tmp_path, KNOWN_SCOPE_FORMS[form]), form)
    rows = _effects(u, "SPAWN")
    assert rows
    assert any("shell_string" in e.control_slots() for e in rows) or all(
        e.resolution.kind != "resolved" for e in rows
    )


DEEP_MODULE_DICT_URL = FASTMCP_HEAD + """\
import requests

SERVICES = {"weather": {"api": {"url": "https://api.weather.example.com/v1/"}}}

@mcp.tool()
def register(url: str) -> str:
    SERVICES["weather"]["api"]["url"] = url
    return "ok"

@mcp.tool()
def forecast(city: str) -> str:
    return requests.get(SERVICES["weather"]["api"]["url"] + city).text
"""


def test_known_deep_dict_precondition(tmp_path):
    assert _slot(_unit(_run(tmp_path, {"s.py": DEEP_MODULE_DICT_URL}), "forecast"), "NET", "url.host") is not None


@KNOWN
def test_known_deep_module_dict_url_is_not_op_resolved(tmp_path):
    """3 段入れ子のモジュール水準 dict の要素は `_opaque_deep` の深さ上限（2）を超えるので確度が resolved の
    まま残り、tool が MODEL の URL を書き込むのに url.host = OP / resolved の定数になる（**false-clean**、
    改訂 5 より前から。改訂 3 / 4 の `_opaque_deep` の限界）。"""
    h = _slot(_unit(_run(tmp_path, {"s.py": DEEP_MODULE_DICT_URL}), "forecast"), "NET", "url.host")
    assert not (h.prin == Prin.OP and h.prov.kind == "resolved")
