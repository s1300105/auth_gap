"""Def 3: 効果と sink の 3 形態（直接 / proxy / pipe）。

**この表そのものが研究成果である**（§1.5.3）。権威ある「MCP 効果仕様」は存在しない
ので、表を凍結（月 3 の sink 語彙凍結、月 10 の解析指紋）して再現可能にする。

各行は `required_by` を持ち、「どの pair_id / 仕様節がこの行に依存するか」を記録する。
行を消すと何が壊れるかが表から読めるようにするため。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

# --------------------------------------------------------------------------
# kind と slot の語彙（Def 3。月 3 凍結）
# --------------------------------------------------------------------------

#: 効果 kind と、その kind が持つ制御位置（slot）の語彙。
SLOTS: dict[str, tuple[str, ...]] = {
    "EXEC": ("code_text",),
    "SPAWN": ("argv0", "argv[i]", "argv[*]", "shell_string", "cwd", "env", "stdin"),
    "FS_WRITE": ("path", "content"),
    "FS_READ": ("path",),
    "NET": ("url.scheme", "url.host", "url.path", "url.query", "body", "headers"),
    "DB": ("sql", "params"),
    "DISPATCH": ("callee",),
}

KINDS: tuple[str, ...] = tuple(SLOTS.keys())

#: **パス領域の slot**。Def 5 の strong-path（symlink 解決 + 包含述語）が
#: 保証するのは「値がパスとして root の下にある」ことだけなので、等級が
#: `req_val = OP` を動かせるのはこの位置に限る。`shell_string` / `sql` /
#: `code_text` / `url.*` にパス包含の等級を当てると、コマンド注入・SQLi・eval・
#: SSRF が clear される（D25、`tests/test_d21_adversarial.py` R22〜R25）。
#: `argv[*]` / `argv0` は要素がパスでありうるので含める（較正対 A4 の git_add）。
PATH_DOMAIN_SLOTS: frozenset[str] = frozenset({"path", "cwd", "argv0", "argv[i]", "argv[*]"})

#: 主 slot 7 種（§6 の opaque 率と C2 のラベリングはこれに限定できる）。
PRIMARY_SLOTS: frozenset[str] = frozenset(
    {"code_text", "argv0", "argv[*]", "shell_string", "path", "url.host", "sql"}
)

#: 副 kind（Def 5-b の kind 粒度の前提条件。月 3 の sink 語彙凍結に含む）。
#: `Leak` を verdict に格上げする前に副 kind 一致を要求するために要る。
SUB_KINDS: dict[str, tuple[str, ...]] = {
    "DB": ("DB_READ", "DB_WRITE"),
    "FS_READ": ("FS_READ",),
    "FS_WRITE": ("FS_WRITE",),
    "SPAWN": ("SPAWN_CONST_ARGV", "SPAWN_MODEL_ARGV"),
    "EXEC": ("EXEC",),
    "NET": ("NET",),
    "DISPATCH": ("DISPATCH",),
}

#: 危険効果 kind（P0 が名指しするもの + DB）。
DANGEROUS_KINDS: frozenset[str] = frozenset({"EXEC", "SPAWN", "FS_WRITE", "FS_READ", "NET", "DB"})

#: sink の 3 形態（Def 3）。
FORMS: tuple[str, ...] = ("direct", "proxy", "pipe")


def validate_slot(kind: str, slot: str) -> None:
    """slot 語彙外の位置を作らないことを実装レベルで強制する。"""
    if kind not in SLOTS:
        raise ValueError(f"未知の効果 kind: {kind!r}")
    if slot.startswith("argv[") and slot.endswith("]") and kind == "SPAWN":
        return  # argv[i] の具体化
    if slot not in SLOTS[kind]:
        raise ValueError(f"{kind} に無い slot: {slot!r}")


# --------------------------------------------------------------------------
# 引数参照
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class ArgRef:
    """sink 呼び出しの実引数への参照。

    `proj` は射影:

    * ``value``      その引数の値そのもの
    * ``elem0``      列の先頭要素（argv0）
    * ``all_elems``  列の全要素（argv[*]）
    * ``const``      `const_value` に書いた定数（proxy カタログの固定 argv0 など）
    """

    pos: Optional[int] = None
    kw: Optional[str] = None
    proj: str = "value"
    const_value: Optional[str] = None

    def describe(self) -> str:
        if self.const_value is not None:
            return f"const({self.const_value!r})"
        base = f"arg{self.pos}" if self.pos is not None else f"{self.kw}="
        return base if self.proj == "value" else f"{base}.{self.proj}"


def A(pos: int, proj: str = "value", kw: Optional[str] = None) -> ArgRef:
    """位置 `pos` の実引数。`kw` を与えると、位置に無いときキーワード `kw=` でも引く
    （`crawler.arun(url=u)` のように仮引数名で渡される呼び出し。F8）。"""
    return ArgRef(pos=pos, kw=kw, proj=proj)


def KW(kw: str, proj: str = "value") -> ArgRef:
    return ArgRef(kw=kw, proj=proj)


def CONST(v: str) -> ArgRef:
    return ArgRef(proj="const", const_value=v)


# --------------------------------------------------------------------------
# sink 行
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class SinkRow:
    """sink 表の 1 行。

    `slots` は「実行モードに依存しない」束縛。spawn のようにモードで slot が
    変わるものは `slots_shell` / `slots_argv` に分けて書き、`exec_mode_kw` に
    モードを決めるキーワードを書く。**モードが config-conditional で確定しない
    場合は両方の行を出す**（F3 の受け入れ条件）。
    """

    dotted: str
    kind: str
    slots: dict[str, ArgRef] = field(default_factory=dict)
    exec_mode_kw: Optional[str] = None
    slots_shell: dict[str, ArgRef] = field(default_factory=dict)
    slots_argv: dict[str, ArgRef] = field(default_factory=dict)
    #: FS_READ / FS_WRITE を `mode=` で分ける sink（`open`）のためのキーワード。
    mode_kw: Optional[str] = None
    mode_pos: Optional[int] = None
    #: 副 kind を固定できる場合。
    sub_kind: Optional[str] = None
    #: FS_WRITE の性質（D32 / prereg §5 #7）: True = 削除・上書き型、False = 追記型、
    #: None = mode 依存（`open` 系。mode から `effects._mode_destructive` が決める）。
    #: **kind / slot の語彙ではなく属性。** `destructiveHint==false` の宣言に対する
    #: CONTRADICTION は True（または不明）の行にだけ立てる。
    destructive: Optional[bool] = None
    note: str = ""
    required_by: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for d in (self.slots, self.slots_shell, self.slots_argv):
            for slot in d:
                validate_slot(self.kind, slot)


def _rows(*rows: SinkRow) -> dict[str, tuple[SinkRow, ...]]:
    """dotted 名 → その名前が持つ効果行の列。

    1 つの呼び出しが 2 つの効果を持つことがある（`urllib.request.urlretrieve` は
    NET と FS_WRITE）。**片方を落とさない**ために値は列にする。
    """
    out: dict[str, list[SinkRow]] = {}
    for r in rows:
        out.setdefault(r.dotted, []).append(r)
    return {k: tuple(v) for k, v in sorted(out.items())}


# --------------------------------------------------------------------------
# (a) 直接 sink: 解決済みの dotted callable
# --------------------------------------------------------------------------

DIRECT_SINKS: dict[str, tuple[SinkRow, ...]] = _rows(
    # -- EXEC ---------------------------------------------------------------
    SinkRow("builtins.eval", "EXEC", {"code_text": A(0)}, note="組込み評価器", required_by=("A15", "B1")),
    SinkRow("builtins.exec", "EXEC", {"code_text": A(0)}, note="組込み実行器", required_by=("F5",)),
    SinkRow("builtins.compile", "EXEC", {"code_text": A(0)}, note="ソースからコード生成"),
    SinkRow(
        "pandas.eval",
        "EXEC",
        {"code_text": A(0)},
        note="pandas の式評価器",
        required_by=("Def3-必要ライブラリ",),
    ),
    SinkRow(
        "pandas.DataFrame.query",
        "EXEC",
        {"code_text": A(0)},
        note="pandas の query 式",
        required_by=("Def3-必要ライブラリ",),
    ),
    SinkRow(
        "sympy.sympify",
        "EXEC",
        {"code_text": A(0)},
        note="sympy の文字列パーサ（既定で eval 相当）",
        required_by=("Def3-必要ライブラリ", "A15"),
    ),
    SinkRow(
        "sympy.parsing.sympy_parser.parse_expr",
        "EXEC",
        {"code_text": A(0)},
        note="sympy の式パーサ",
        required_by=("Def3-必要ライブラリ", "A15"),
    ),
    SinkRow(
        "jinja2.Template",
        "EXEC",
        {"code_text": A(0)},
        note="テンプレート文字列からのコード生成（SSTI）",
        required_by=("Def3-必要ライブラリ",),
    ),
    SinkRow(
        "jinja2.Environment.from_string",
        "EXEC",
        {"code_text": A(0)},
        note="同上",
        required_by=("Def3-必要ライブラリ",),
    ),
    # -- SPAWN --------------------------------------------------------------
    SinkRow(
        "os.system",
        "SPAWN",
        {"shell_string": A(0)},
        note="常にシェル経由",
        required_by=("P0",),
    ),
    SinkRow("os.popen", "SPAWN", {"shell_string": A(0)}, note="常にシェル経由"),
    SinkRow(
        "subprocess.run",
        "SPAWN",
        {"cwd": KW("cwd"), "env": KW("env"), "stdin": KW("input")},
        exec_mode_kw="shell",
        slots_shell={"shell_string": A(0)},
        slots_argv={"argv0": A(0, "elem0"), "argv[*]": A(0, "all_elems")},
        note="shell= で slot が変わる。確定しなければ 2 行出す（F3）",
        required_by=("A5", "F3", "F9"),
    ),
    SinkRow(
        "subprocess.call",
        "SPAWN",
        {"cwd": KW("cwd"), "env": KW("env")},
        exec_mode_kw="shell",
        slots_shell={"shell_string": A(0)},
        slots_argv={"argv0": A(0, "elem0"), "argv[*]": A(0, "all_elems")},
    ),
    SinkRow(
        "subprocess.check_call",
        "SPAWN",
        {"cwd": KW("cwd"), "env": KW("env")},
        exec_mode_kw="shell",
        slots_shell={"shell_string": A(0)},
        slots_argv={"argv0": A(0, "elem0"), "argv[*]": A(0, "all_elems")},
    ),
    SinkRow(
        "subprocess.check_output",
        "SPAWN",
        {"cwd": KW("cwd"), "env": KW("env"), "stdin": KW("input")},
        exec_mode_kw="shell",
        slots_shell={"shell_string": A(0)},
        slots_argv={"argv0": A(0, "elem0"), "argv[*]": A(0, "all_elems")},
    ),
    SinkRow(
        "subprocess.Popen",
        "SPAWN",
        {"cwd": KW("cwd"), "env": KW("env")},
        exec_mode_kw="shell",
        slots_shell={"shell_string": A(0)},
        slots_argv={"argv0": A(0, "elem0"), "argv[*]": A(0, "all_elems")},
        note="pipe 形態のハンドルを生む（Def 3(c)）",
        required_by=("F6",),
    ),
    SinkRow(
        "asyncio.create_subprocess_shell",
        "SPAWN",
        {"shell_string": A(0), "cwd": KW("cwd"), "env": KW("env")},
        note="常にシェル経由。pipe ハンドルを生む",
        required_by=("F6",),
    ),
    SinkRow(
        "asyncio.create_subprocess_exec",
        "SPAWN",
        {"argv0": A(0), "argv[*]": ArgRef(proj="varargs"), "cwd": KW("cwd"), "env": KW("env")},
        note="argv 形。pipe ハンドルを生む",
        required_by=("F6",),
    ),
    SinkRow("os.execv", "SPAWN", {"argv0": A(0), "argv[*]": A(1, "all_elems")}),
    SinkRow("os.execvp", "SPAWN", {"argv0": A(0), "argv[*]": A(1, "all_elems")}),
    SinkRow("os.execve", "SPAWN", {"argv0": A(0), "argv[*]": A(1, "all_elems"), "env": A(2)}),
    SinkRow("os.spawnv", "SPAWN", {"argv0": A(1), "argv[*]": A(2, "all_elems")}),
    SinkRow("pty.spawn", "SPAWN", {"argv[*]": A(0, "all_elems"), "argv0": A(0, "elem0")}),
    SinkRow(
        "mcp.StdioServerParameters",
        "SPAWN",
        {"argv0": KW("command"), "argv[*]": KW("args", "all_elems"), "env": KW("env")},
        note="MCP クライアントが子プロセスとして起動するサーバの指定",
        required_by=("B3", "B4", "Def3-必要ライブラリ"),
    ),
    # -- FS_WRITE / FS_READ -------------------------------------------------
    SinkRow(
        "builtins.open",
        "FS_READ",
        {"path": A(0)},
        mode_kw="mode",
        mode_pos=1,
        note="mode で FS_READ / FS_WRITE を分ける。既定 'r'",
        required_by=("P0",),
    ),
    SinkRow(
        "io.open",
        "FS_READ",
        {"path": A(0)},
        mode_kw="mode",
        mode_pos=1,
    ),
    SinkRow(
        "pathlib.Path.open",
        "FS_READ",
        {"path": ArgRef(proj="receiver")},
        mode_kw="mode",
        mode_pos=0,
    ),
    SinkRow("pathlib.Path.write_text", "FS_WRITE", {"path": ArgRef(proj="receiver"), "content": A(0)}, destructive=True,
        required_by=("F7",),
    ),
    SinkRow("pathlib.Path.write_bytes", "FS_WRITE", {"path": ArgRef(proj="receiver"), "content": A(0)}, destructive=True,
        required_by=("F7",),
    ),
    SinkRow("pathlib.Path.read_text", "FS_READ", {"path": ArgRef(proj="receiver")}),
    SinkRow("pathlib.Path.read_bytes", "FS_READ", {"path": ArgRef(proj="receiver")}),
    SinkRow("pathlib.Path.unlink", "FS_WRITE", {"path": ArgRef(proj="receiver")}, destructive=True),
    SinkRow("pathlib.Path.mkdir", "FS_WRITE", {"path": ArgRef(proj="receiver")}, destructive=False),
    SinkRow(
        "pathlib.Path.glob",
        "FS_READ",
        {"path": A(0)},
        note="pattern が制御位置。B2（PraisonAI list_files）が依存する",
        required_by=("B2", "Def3-必要ライブラリ"),
    ),
    SinkRow(
        "pathlib.Path.rglob",
        "FS_READ",
        {"path": A(0)},
        required_by=("B2",),
    ),
    SinkRow("glob.glob", "FS_READ", {"path": A(0)}, required_by=("B2",)),
    SinkRow("glob.iglob", "FS_READ", {"path": A(0)}, required_by=("B2",)),
    SinkRow("os.listdir", "FS_READ", {"path": A(0)}),
    SinkRow("os.walk", "FS_READ", {"path": A(0)}),
    SinkRow("os.remove", "FS_WRITE", {"path": A(0)}, destructive=True),
    SinkRow("os.unlink", "FS_WRITE", {"path": A(0)}, destructive=True),
    SinkRow("os.rmdir", "FS_WRITE", {"path": A(0)}, destructive=True),
    SinkRow("os.makedirs", "FS_WRITE", {"path": A(0)}, destructive=False),
    SinkRow("os.mkdir", "FS_WRITE", {"path": A(0)}, destructive=False),
    SinkRow("os.rename", "FS_WRITE", {"path": A(1)}, destructive=True),
    SinkRow("os.replace", "FS_WRITE", {"path": A(1)}, destructive=True),
    SinkRow("os.chmod", "FS_WRITE", {"path": A(0)}, destructive=True),
    SinkRow("os.symlink", "FS_WRITE", {"path": A(1)}, destructive=False),
    SinkRow("shutil.rmtree", "FS_WRITE", {"path": A(0)}, destructive=True),
    SinkRow("shutil.copy", "FS_WRITE", {"path": A(1), "content": A(0)}, destructive=True),
    SinkRow("shutil.copy2", "FS_WRITE", {"path": A(1), "content": A(0)}, destructive=True),
    SinkRow("shutil.copyfile", "FS_WRITE", {"path": A(1), "content": A(0)}, destructive=True),
    SinkRow("shutil.move", "FS_WRITE", {"path": A(1), "content": A(0)}, destructive=True),
    SinkRow("shutil.unpack_archive", "FS_WRITE", {"path": A(1), "content": A(0)}, destructive=True),
    # -- NET ----------------------------------------------------------------
    SinkRow(
        "requests.get",
        "NET",
        {"url.host": A(0), "url.query": KW("params"), "headers": KW("headers")},
        note="url slot の分割は §2.6 の URL 分割規則が行う",
        required_by=("A16", "F10"),
    ),
    SinkRow(
        "requests.post",
        "NET",
        {"url.host": A(0), "body": KW("data"), "headers": KW("headers")},
        required_by=("A16",),
    ),
    SinkRow("requests.put", "NET", {"url.host": A(0), "body": KW("data")}),
    SinkRow("requests.patch", "NET", {"url.host": A(0), "body": KW("data")}),
    SinkRow("requests.delete", "NET", {"url.host": A(0)}),
    SinkRow("requests.head", "NET", {"url.host": A(0)}),
    SinkRow("requests.request", "NET", {"url.host": A(1), "body": KW("data")}),
    SinkRow("httpx.get", "NET", {"url.host": A(0), "url.query": KW("params")}),
    SinkRow("httpx.post", "NET", {"url.host": A(0), "body": KW("json")}),
    SinkRow("httpx.request", "NET", {"url.host": A(1)}),
    SinkRow("urllib.request.urlopen", "NET", {"url.host": A(0)}),
    SinkRow("urllib.request.urlretrieve", "NET", {"url.host": A(0)}),
    SinkRow(
        "urllib.request.urlretrieve",
        "FS_WRITE",
        {"path": A(1), "content": A(0)},
        note="1 呼び出しで NET と FS_WRITE の 2 行が出る",
    ),
    # -- DB -----------------------------------------------------------------
    SinkRow(
        "sqlalchemy.text",
        "DB",
        {"sql": A(0)},
        note="生 SQL の構築点。実行は proxy 側",
        required_by=("Def3-必要ライブラリ", "A18"),
    ),
)


# --------------------------------------------------------------------------
# (b) proxy sink: 受け手の型がカタログ化された wrapper
#
# **proxy カタログの各行は型だけでなく slot 束縛を持つ**（Def 3）。
# 書式: 受け手到達式 : 受け手型 { slot ← 由来 }
# 由来は受け手を生んだコンストラクタの引数（位置 / キーワード）または定数。
# slot 束縛が無いと較正対 A1（mcp-server-git の封じ込め）が成立しない。
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class ProxyRow:
    """proxy sink の 1 行。

    `recv_types` は受け手の型（`Obj.classes`）。`method` は呼ばれるメソッド名
    （`*` は任意）。`from_ctor` は「受け手を生んだコンストラクタの引数」を
    slot に束縛する規則で、キーは slot、値は ctor のフィールド名。
    """

    recv_types: tuple[str, ...]
    method: str
    kind: str
    slots: dict[str, ArgRef] = field(default_factory=dict)
    from_ctor: dict[str, str] = field(default_factory=dict)
    sub_kind: Optional[str] = None
    note: str = ""
    required_by: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for slot in list(self.slots) + list(self.from_ctor):
            validate_slot(self.kind, slot)


PROXY_SINKS: tuple[ProxyRow, ...] = (
    # GitPython: repo = git.Repo(repo_path) → repo.git.checkout(branch_name)
    # 受け手の型だけを解決しても cwd に repo_path が載らない（Def 3 の明記事項）。
    ProxyRow(
        recv_types=("git.cmd.Git", "git.Git"),
        method="*",
        kind="SPAWN",
        slots={"argv[*]": ArgRef(proj="varargs")},
        from_ctor={"cwd": "working_dir"},
        note="argv0 ← 'git'（定数）。shell=False。§Def3 の A1 行",
        required_by=("A1", "A3", "A4", "F1", "F2"),
    ),
    ProxyRow(
        recv_types=("git.index.base.IndexFile", "git.IndexFile"),
        method="add",
        kind="FS_WRITE",
        slots={"path": A(0)},
        from_ctor={},
        note="git.Repo().index.add。A3 の脆弱側がこの行に依存する",
        required_by=("A3",),
    ),
    # SQLAlchemy / DBAPI カーソル
    ProxyRow(
        recv_types=(
            "sqlalchemy.engine.Connection",
            "sqlalchemy.orm.Session",
            "sqlalchemy.Connection",
            "sqlalchemy.Session",
        ),
        method="execute",
        kind="DB",
        slots={"sql": A(0), "params": A(1)},
        required_by=("A18", "S1'"),
    ),
    ProxyRow(
        recv_types=(
            "sqlalchemy.engine.Connection",
            "sqlalchemy.orm.Session",
            "sqlalchemy.Connection",
            "sqlalchemy.Session",
        ),
        method="exec_driver_sql",
        kind="DB",
        slots={"sql": A(0), "params": A(1)},
        required_by=("A18",),
    ),
    ProxyRow(
        recv_types=("sqlite3.Cursor", "sqlite3.Connection", "psycopg.Cursor", "psycopg2.cursor"),
        method="execute",
        kind="DB",
        slots={"sql": A(0), "params": A(1)},
        required_by=("A18", "S1'"),
    ),
    ProxyRow(
        recv_types=("sqlite3.Cursor", "sqlite3.Connection", "psycopg.Cursor", "psycopg2.cursor"),
        method="executemany",
        kind="DB",
        slots={"sql": A(0), "params": A(1)},
    ),
    ProxyRow(
        recv_types=("sqlite3.Cursor", "sqlite3.Connection"),
        method="executescript",
        kind="DB",
        slots={"sql": A(0)},
    ),
    # httpx / requests のセッション
    ProxyRow(
        recv_types=("httpx.Client", "httpx.AsyncClient", "requests.Session"),
        method="get",
        kind="NET",
        slots={"url.host": A(0), "url.query": KW("params")},
        from_ctor={"url.scheme": "base_url"},
        note="httpx.Client(base_url=b) は { url.base ← b }",
        required_by=("A16",),
    ),
    ProxyRow(
        recv_types=("httpx.Client", "httpx.AsyncClient", "requests.Session"),
        method="post",
        kind="NET",
        slots={"url.host": A(0), "body": KW("json")},
        from_ctor={"url.scheme": "base_url"},
    ),
    ProxyRow(
        recv_types=("httpx.Client", "httpx.AsyncClient", "requests.Session"),
        method="request",
        kind="NET",
        slots={"url.host": A(1), "body": KW("data")},
        from_ctor={"url.scheme": "base_url"},
    ),
    # paramiko
    ProxyRow(
        recv_types=("paramiko.SSHClient",),
        method="exec_command",
        kind="SPAWN",
        slots={"shell_string": A(0)},
        note="遠隔だが SPAWN として数える（Def 3 の明記事項）",
        required_by=("Def3",),
    ),
    # neo4j / arangodb（A14 が依存する）
    ProxyRow(
        recv_types=("neo4j.Session", "neo4j.Driver", "neo4j.AsyncSession"),
        method="run",
        kind="DB",
        slots={"sql": A(0), "params": A(1)},
        required_by=("A14", "S2", "Def3-必要ライブラリ"),
    ),
    ProxyRow(
        recv_types=("neo4j.Driver", "neo4j.AsyncDriver"),
        method="execute_query",
        kind="DB",
        slots={"sql": A(0), "params": A(1)},
        required_by=("A14", "S2"),
    ),
    ProxyRow(
        recv_types=("arango.database.StandardDatabase", "arango.StandardDatabase"),
        method="aql",
        kind="DB",
        slots={"sql": A(0)},
        required_by=("A14",),
    ),
    # crawl4ai（F8 が依存する）
    ProxyRow(
        recv_types=("crawl4ai.AsyncWebCrawler",),
        method="arun",
        kind="NET",
        slots={"url.host": A(0, kw="url")},
        note="OpenManus は `arun(url=url, config=...)` とキーワードで渡す（F8）",
        required_by=("F8",),
    ),
    ProxyRow(
        recv_types=("crawl4ai.AsyncWebCrawler",),
        method="arun_many",
        kind="NET",
        slots={"url.host": A(0, kw="urls")},
        required_by=("F8",),
    ),
)


# --------------------------------------------------------------------------
# (c) pipe sink（新設）
#
# X = subprocess.Popen(...) / asyncio.create_subprocess_* で得たハンドルの
# X.stdin.write(v) / X.communicate(input=v)。
#
# **導入根拠は構造的理由のみで、CVE の裏付けは無い**（Def 3 の明記事項）。
# OpenManus `Bash` は argv0 が定数 "/bin/bash" で、モデル値は spawn 後の
# stdin.write に入るため、直接 / proxy の 2 形態では全 slot が OP になる。
# CVE-2025-2733 が名指しするのは python_execute.py であって bash.py ではない。
# --------------------------------------------------------------------------

#: pipe 形態が EXEC になる argv0（インタプリタ カタログ）。
INTERPRETER_ARGV0: frozenset[str] = frozenset(
    {"/bin/sh", "/bin/bash", "sh", "bash", "python", "python3", "node", "psql", "/usr/bin/psql"}
)


def is_interpreter(argv0: Optional[str]) -> bool:
    """argv0 がインタプリタ カタログに載るか。`python*` は前方一致で見る。"""
    if argv0 is None:
        return False
    base = argv0.rsplit("/", 1)[-1]
    if argv0 in INTERPRETER_ARGV0 or base in INTERPRETER_ARGV0:
        return True
    return base.startswith("python")


@dataclass(frozen=True)
class PipeRow:
    """pipe sink の 1 行。受け手は spawn ハンドル（またはその `.stdin`）。"""

    method: str
    slots: dict[str, ArgRef]
    note: str = ""
    required_by: tuple[str, ...] = ()


PIPE_SINKS: tuple[PipeRow, ...] = (
    PipeRow("stdin.write", {"stdin": A(0)}, required_by=("F6",)),
    PipeRow("communicate", {"stdin": KW("input")}, required_by=("F6",)),
)

#: pipe ハンドルを生む spawn（Def 3(c)）。
PIPE_HANDLE_SOURCES: frozenset[str] = frozenset(
    {
        "subprocess.Popen",
        "asyncio.create_subprocess_shell",
        "asyncio.create_subprocess_exec",
    }
)


# --------------------------------------------------------------------------
# 非 DB の `.execute()` を数えないための機械判定規則（§10）
# --------------------------------------------------------------------------

#: proxy カタログの DB 受け手型（`.execute()` の弁別に使う）。
DB_RECEIVER_TYPES: frozenset[str] = frozenset(
    t for row in PROXY_SINKS if row.kind == "DB" for t in row.recv_types
)


def db_execute_rule(receiver_classes: frozenset[str]) -> str:
    """`.execute()` の受け手が DB かを機械判定する（§10。型環境なしで決める）。

    受け手が proxy カタログの DB 受け手型に**局所代入で解決できる**場合のみ
    DB 効果とする。解決できない `.execute()` は ``db_unresolved`` として記録し、
    **危険効果に数えない**（`effect_fp_audit.db_only_non_db_execute` の分子）。

    :returns: ``"db"`` | ``"db_unresolved"``
    """
    if receiver_classes & DB_RECEIVER_TYPES:
        return "db"
    return "db_unresolved"


# --------------------------------------------------------------------------
# WRITE_POLICY（マニフェスト属性。verdict を持たない）
# --------------------------------------------------------------------------

#: FS_WRITE の path がこれらに解決される場合 `WRITE_POLICY` 属性を立てる。
POLICY_FILE_PATTERNS: tuple[str, ...] = (
    ".claude/settings.json",
    ".claude/settings.local.json",
    "claude_desktop_config.json",
    ".mcp.json",
    "mcp.json",
    "settings.json",
)
