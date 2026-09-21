"""TRANSFER 表・INDIRECT 表・ライブラリ コンストラクタ カタログ。

Def 4 の深さの数え方（**カタログ化ライブラリ呼び出しは深さを消費しない。
間接 target 形は 1 段として数える**）と、§2.6 の canonical-alias 表の定義点。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

# --------------------------------------------------------------------------
# TRANSFER 表: 値を変換するカタログ化ライブラリ呼び出し
#
# 深さを消費しない。呼ぶと値の shape / 属性 / alias_facts が変わる。
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class TransferRow:
    """値変換の 1 行。

    `transform` は canonical-alias 表 `(root, site, transform)` に記録する名前。
    `attrs` はこの変換が立てる :data:`authgap.ir.VALUE_ATTRS` の属性。
    `shape` は結果の形（``str`` / ``seq`` / ``path`` / ``same`` / ``atom``）。
    `canon_class` は正規化子の系統:

    * ``symlink``  symlink 解決子（`realpath` / `Path.resolve`）。Def 5(i) を満たす
    * ``lexical``  字句正規化子（`normpath` / `abspath`）。**単独では (i) を満たさない**
    * ``None``     正規化子ではない
    """

    dotted: str
    transform: str
    shape: str = "same"
    attrs: tuple[str, ...] = ()
    canon_class: Optional[str] = None
    #: 引数のどれが「変換される値」か（既定は第 0 引数、`receiver` は受け手）。
    subject: str = "arg0"
    note: str = ""


TRANSFERS: tuple[TransferRow, ...] = (
    # -- symlink 解決子（Def 5 strong-path (i) を満たす唯一の系統）-----------
    TransferRow("os.path.realpath", "realpath", "path", ("canonicalised",), "symlink"),
    TransferRow("pathlib.Path.resolve", "Path.resolve", "path", ("canonicalised",), "symlink", "receiver"),
    TransferRow("os.realpath", "realpath", "path", ("canonicalised",), "symlink"),
    # -- 字句正規化子（単独では strong-path にしない。weak(no_symlink_resolution)）
    TransferRow("os.path.normpath", "normpath", "path", ("lexical_canon",), "lexical"),
    TransferRow("os.path.abspath", "abspath", "path", ("lexical_canon",), "lexical"),
    TransferRow("os.path.expanduser", "expanduser", "path", (), None),
    TransferRow("os.path.expandvars", "expandvars", "path", (), None),
    # -- パス構築 -----------------------------------------------------------
    TransferRow("os.path.join", "os.path.join", "path", ("joined",), None),
    TransferRow("pathlib.Path", "Path()", "path", (), None, note="正規化ではない（F7 の明記事項）"),
    TransferRow("os.path.basename", "basename", "str", (), None),
    TransferRow("os.path.dirname", "dirname", "path", (), None),
    TransferRow("os.path.relpath", "relpath", "path", (), None),
    # -- URL ----------------------------------------------------------------
    TransferRow("urllib.parse.urlparse", "urlparse", "atom", (), None),
    TransferRow("urllib.parse.urlsplit", "urlparse", "atom", (), None),
    TransferRow("urllib.parse.quote", "quote", "str", ("encoded",), None),
    TransferRow("urllib.parse.urlencode", "urlencode", "str", ("encoded",), None),
    TransferRow("urllib.parse.urljoin", "urljoin", "str", ("joined",), None),
    # -- シェル -------------------------------------------------------------
    TransferRow("shlex.split", "shlex.split", "seq", ("tokenised",), None),
    TransferRow("shlex.quote", "shlex.quote", "str", ("quoted",), None),
    TransferRow("shlex.join", "shlex.join", "str", ("quoted", "joined"), None),
    TransferRow("pipes.quote", "shlex.quote", "str", ("quoted",), None),
    # -- 文字列 -------------------------------------------------------------
    TransferRow("str.split", "str.split", "seq", (), None, subject="receiver"),
    TransferRow("str.rsplit", "str.split", "seq", (), None, subject="receiver"),
    TransferRow("str.strip", "str.strip", "str", (), None, subject="receiver"),
    # bytes との相互変換は内容を変えない（OpenManus `_BashSession.run` の
    # `command.encode() + ...` が stdin に届く。F6。無いと opaque(unresolved) で MODEL が消える）
    TransferRow("str.encode", "str.encode", "str", (), None, subject="receiver"),
    TransferRow("bytes.decode", "bytes.decode", "str", (), None, subject="receiver"),
    TransferRow("str.lower", "str.lower", "str", (), None, subject="receiver"),
    TransferRow("str.upper", "str.upper", "str", (), None, subject="receiver"),
    TransferRow("str.replace", "str.replace", "str", (), None, subject="receiver"),
    TransferRow("str.format", "str.format", "str", ("joined",), None, subject="receiver"),
    TransferRow("str.join", "str.join", "str", ("joined",), None, subject="receiver"),
    TransferRow("json.dumps", "json.dumps", "str", ("encoded",), None),
    # -- SQL 正規化（A13 の条件つき算入がここに依存する）---------------------
    TransferRow(
        "sqlglot.parse_one",
        "sqlglot.parse_one",
        "atom",
        ("canonicalised",),
        None,
        note="A13 を算入するかは D10 の判断。既定では canon_class を付けない",
    ),
    TransferRow("sqlglot.parse", "sqlglot.parse", "atom", ("canonicalised",), None),
)

TRANSFER_BY_NAME: dict[str, TransferRow] = {t.dotted: t for t in TRANSFERS}

#: symlink 解決子の transform 名（Def 5 strong-path (i)）。
SYMLINK_RESOLVERS: frozenset[str] = frozenset(
    t.transform for t in TRANSFERS if t.canon_class == "symlink"
)
#: 字句正規化子の transform 名（**単独では strong-path にしない**）。
LEXICAL_CANONS: frozenset[str] = frozenset(t.transform for t in TRANSFERS if t.canon_class == "lexical")


# --------------------------------------------------------------------------
# INDIRECT 表: 間接 target 形。**1 段として数える**（Def 4）
#
# これが無いと OpenManus PythonExecute（multiprocessing.Process(target=...) 越しに
# exec）が opaque(unresolved) になり、§10 の脈拍の負例期待が外れる。
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class IndirectRow:
    """間接呼び出し形の 1 行。

    `target_ref` は呼ばれる関数を指す引数、`args_ref` はその実引数の列。
    """

    dotted: str
    target_kw: Optional[str] = None
    target_pos: Optional[int] = None
    args_kw: Optional[str] = None
    args_pos: Optional[int] = None
    note: str = ""


INDIRECTS: tuple[IndirectRow, ...] = (
    IndirectRow("multiprocessing.Process", target_kw="target", args_kw="args", note="F5 が依存する"),
    IndirectRow("threading.Thread", target_kw="target", args_kw="args"),
    IndirectRow("functools.partial", target_pos=0, args_pos=1),
    IndirectRow("concurrent.futures.Executor.submit", target_pos=0, args_pos=1),
    IndirectRow("concurrent.futures.ThreadPoolExecutor.submit", target_pos=0, args_pos=1),
    IndirectRow("concurrent.futures.ProcessPoolExecutor.submit", target_pos=0, args_pos=1),
    IndirectRow("asyncio.to_thread", target_pos=0, args_pos=1),
    IndirectRow("asyncio.get_event_loop.run_in_executor", target_pos=1, args_pos=2),
    IndirectRow("loop.run_in_executor", target_pos=1, args_pos=2),
)

INDIRECT_BY_NAME: dict[str, IndirectRow] = {i.dotted: i for i in INDIRECTS}


# --------------------------------------------------------------------------
# ライブラリ コンストラクタ カタログ（月 3 凍結。§2.6）
#
# Obj.fields の束縛を決める。proxy sink の from_ctor がこのフィールド名を参照する。
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class CtorRow:
    """コンストラクタ 1 行。`fields` は「フィールド名 → 引数参照」。

    引数参照は ``"arg<N>"`` または ``"kw:<name>"``、``"const:<値>"``。
    """

    dotted: str
    cls: str
    fields: dict[str, str] = field(default_factory=dict)
    note: str = ""
    required_by: tuple[str, ...] = ()


CTORS: tuple[CtorRow, ...] = (
    CtorRow(
        "git.Repo",
        "git.Repo",
        {"working_dir": "arg0"},
        note="repo.git は git.cmd.Git を返し、working_dir を cwd に運ぶ",
        required_by=("A1", "F1", "F2"),
    ),
    CtorRow("git.cmd.Git", "git.cmd.Git", {"working_dir": "arg0"}),
    CtorRow(
        "subprocess.Popen",
        "subprocess.Popen",
        {"spawn_argv": "arg0", "spawn_shell": "kw:shell", "spawn_cwd": "kw:cwd"},
        note="pipe 形態のハンドル。F6 が依存する",
        required_by=("F6",),
    ),
    CtorRow(
        "asyncio.create_subprocess_shell",
        "asyncio.subprocess.Process",
        {"spawn_argv": "arg0", "spawn_shell": "const:True"},
        required_by=("F6",),
    ),
    CtorRow(
        "asyncio.create_subprocess_exec",
        "asyncio.subprocess.Process",
        {"spawn_argv": "arg0", "spawn_shell": "const:False"},
        required_by=("F6",),
    ),
    CtorRow("sqlite3.connect", "sqlite3.Connection", {"database": "arg0"}),
    CtorRow(
        "httpx.Client",
        "httpx.Client",
        {"base_url": "kw:base_url"},
        note="{ url.base ← b }（Def 3 の明記事項）",
    ),
    CtorRow("httpx.AsyncClient", "httpx.AsyncClient", {"base_url": "kw:base_url"}),
    CtorRow("requests.Session", "requests.Session", {}),
    CtorRow("crawl4ai.AsyncWebCrawler", "crawl4ai.AsyncWebCrawler", {}, required_by=("F8",)),
    CtorRow("neo4j.GraphDatabase.driver", "neo4j.Driver", {"uri": "arg0"}, required_by=("A14", "S2")),
    CtorRow("paramiko.SSHClient", "paramiko.SSHClient", {}),
    CtorRow("sqlalchemy.create_engine", "sqlalchemy.engine.Engine", {"url": "arg0"}),
)

CTOR_BY_NAME: dict[str, CtorRow] = {c.dotted: c for c in CTORS}

#: 属性到達でコンストラクタの型が伝播する規則（`git.Repo(p).git` → `git.cmd.Git`）。
#: キーは `(元の型, 属性名)`、値は `(新しい型, 引き継ぐフィールドの対応)`。
ATTR_TYPE_TRANSITIONS: dict[tuple[str, str], tuple[str, dict[str, str]]] = {
    ("git.Repo", "git"): ("git.cmd.Git", {"working_dir": "working_dir"}),
    ("git.Repo", "index"): ("git.index.base.IndexFile", {"working_dir": "working_dir"}),
    ("subprocess.Popen", "stdin"): ("subprocess.Popen.stdin", {"spawn_argv": "spawn_argv", "spawn_shell": "spawn_shell"}),
    ("asyncio.subprocess.Process", "stdin"): (
        "asyncio.subprocess.Process.stdin",
        {"spawn_argv": "spawn_argv", "spawn_shell": "spawn_shell"},
    ),
    ("sqlite3.Connection", "cursor"): ("sqlite3.Cursor", {"database": "database"}),
    ("neo4j.Driver", "session"): ("neo4j.Session", {"uri": "uri"}),
    ("sqlalchemy.engine.Engine", "connect"): ("sqlalchemy.engine.Connection", {"url": "url"}),
}


#: 受け手を主語とする TRANSFER（メソッド名で引く）。
METHOD_TRANSFERS: dict[str, TransferRow] = {
    t.dotted.rsplit(".", 1)[-1]: t for t in TRANSFERS if t.subject == "receiver"
}


def transfer_for(dotted: str) -> Optional[TransferRow]:
    """dotted 名から TRANSFER 行を引く（完全一致のみ）。

    別名 import は :mod:`authgap.srcindex` が dotted 名に正規化してから渡す。
    ここで末尾一致を許すと `os.path.join` と自作の `join` が衝突するので許さない。
    """
    return TRANSFER_BY_NAME.get(dotted)


def method_transfer_for(method: str) -> Optional[TransferRow]:
    """受け手を主語とするメソッド名（`split` / `resolve` …）から引く。"""
    return METHOD_TRANSFERS.get(method)
