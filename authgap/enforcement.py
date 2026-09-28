"""Def 6 の**執行表**と依存版の確定規則。

執行性規則（D_dom 層の唯一の正当化）: 機械可読な値域制約は、フレームワークが
実行時にそれを執行するなら**宣言ではなく値検証**であり Def 5（M 側）に属する。
執行しないなら untrusted な自己申告であり D に属する。
**同じ構文が登録経路と SDK 版で役割を変える。**

判定は **(1) 登録 API の形状 → (2) 版の確定可否** の順。
**版は二次的な証拠であり単独では使わない。**

版の確定規則:

1. `==X.Y.Z` / `~=X.Y` / 上限付き指定、または lock ファイル
   （`uv.lock` / `poetry.lock` / `Pipfile.lock`）の解決済み版があるときのみ
   「版が確定した」とする。
2. **`>=X.Y` だけの指定は版を確定しない**（`mcp>=1.2.0` は 1.2.0 も 2.2.0 も
   1.30.0 も許す。PyPI の `mcp` 最新は 2.2.0）。
3. 版が確定しない低レベル経路は **API 形状**で決める
   （`@server.call_tool()` は v2 に存在しないので実行時は必ず < 2.0、
   `Server(on_call_tool=)` は必ず ≥ 2.0）。それでも [1.10, 2.0) か < 1.10 かが
   決まらなければ `D_unknown`。
4. **読めないものを既定で「執行あり」とも「執行なし」とも仮定しない。**

**この表は月 3 で凍結し `docs/fingerprint.json` の D パーサ規則に含める。**
確認した版と commit を必ず添える（§9-10）。
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Optional

# --------------------------------------------------------------------------
# 執行表（一次資料で確認。commit を必ず添える）
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class EnforcementRow:
    """執行表の 1 行。"""

    #: 登録経路（木の中の形）。
    path: str
    #: ``enforced``（Def 5 側） / ``not_enforced``（D_dom） / ``version_dependent`` / ``unknown``
    verdict: str
    #: 一次資料（commit を必ず添える）。
    evidence: str
    #: `version_dependent` のときに執行される版の範囲。
    enforced_range: Optional[tuple[str, str]] = None


ENFORCEMENT_TABLE: tuple[EnforcementRow, ...] = (
    EnforcementRow(
        "highlevel_decorator",
        "enforced",
        "v2.0.0b2 `2713b53` の mcpserver/tools/base.py:152 が "
        "fn_metadata.call_fn_with_arg_validation(...)。v2.2.0 `9972c21` では当該 API は "
        "deprecated で経路は base.py:149 validate_arguments + :176 call_fn。"
        "v1.30.0 `8c2fa6e` では fastmcp/tools/base.py:101",
    ),
    EnforcementRow(
        "thirdparty_fastmcp",
        "enforced",
        "`e3fb4af` の fastmcp/tools/function_tool.py:474 "
        "type_adapter.validate_python(arguments, strict=strict)",
    ),
    EnforcementRow(
        "langchain_basetool",
        "enforced",
        "langchain_core/tools/base.py:778 _parse_input -> :834 input_args.model_validate",
    ),
    EnforcementRow(
        "lowlevel_v1_decorator",
        "version_dependent",
        "`v1.10.0` で def call_tool(self, *, validate_input: bool = True) と "
        "jsonschema.validate(...) が導入。**`v1.9.0` / `v1.6.0` は def call_tool(self): で "
        "検証ゼロ。したがって「1.x なら執行される」と書いてはならない**",
        enforced_range=("1.10", "2.0"),
    ),
    EnforcementRow(
        "lowlevel_v2_on_call_tool",
        "not_enforced",
        "`2713b53`(v2.0.0b2) と `9972c21`(v2.2.0) の lowlevel/server.py に jsonschema の "
        "import が無く、src/ 内の使用は client 側の output schema 検証のみ。"
        "**v2 の lowlevel/server.py に def call_tool は存在せず、ハンドラは __init__ の "
        "on_call_tool= で渡される**",
    ),
    EnforcementRow(
        "internal_direct_run",
        "unknown",
        "tool._run(...) を検証経路を通さず直接呼ぶ内部経路。"
        "その呼び出しは OP 起動の経路であり、モデル面の分類を変えない",
    ),
    EnforcementRow(
        "dynamic_schema",
        "unknown",
        "スキーマを動的に組む / 上のどれでもない",
    ),
)

ENFORCEMENT_BY_PATH = {r.path: r for r in ENFORCEMENT_TABLE}

#: ユニットの `entry_kind` / `framework` から登録経路名へ。
PATH_OF_ENTRY = {
    ("mcp", "decorator"): "highlevel_decorator",
    ("fastmcp", "decorator"): "thirdparty_fastmcp",
    ("langchain", "method"): "langchain_basetool",
    ("langchain", "decorator"): "langchain_basetool",
    ("mcp-lowlevel-v1", "lowlevel_v1"): "lowlevel_v1_decorator",
    ("mcp-lowlevel-v2", "lowlevel_v2"): "lowlevel_v2_on_call_tool",
}


# --------------------------------------------------------------------------
# 依存版の読み取り
# --------------------------------------------------------------------------

_REQ_LINE = re.compile(r"^\s*([A-Za-z0-9._-]+)\s*([<>=!~^].*)?$")
_PIN_EXACT = re.compile(r"==\s*([0-9][^,\s]*)")
_PIN_COMPAT = re.compile(r"~=\s*([0-9][^,\s]*)")
_PIN_UPPER = re.compile(r"<\s*=?\s*([0-9][^,\s]*)")
_PIN_LOWER_ONLY = re.compile(r"^\s*>=?\s*[0-9][^,\s]*\s*$")


@dataclass
class DepPin:
    """1 つの依存の版の確定状況。"""

    name: str
    spec: Optional[str]
    #: ``exact`` / ``lockfile`` / ``upper_bounded`` / ``lower_bound_only`` / ``unreadable``
    status: str
    version: Optional[str] = None
    source: str = ""

    @property
    def is_determined(self) -> bool:
        """版が「確定した」と言えるか（規則 1）。"""
        return self.status in ("exact", "lockfile", "upper_bounded")

    def to_json(self) -> dict:
        return {
            "name": self.name,
            "spec": self.spec,
            "status": self.status,
            "version": self.version,
            "source": self.source,
        }


#: 依存の記載を探すファイル。
#: **`requirements*.txt` と lock ファイルを必ず含める**（§9-12。前測のコーパスは
#: これらを 1 件も含まないまま「依存版を読んだ」と書いていた）。
DEP_FILES = (
    "requirements.txt",
    "requirements-dev.txt",
    "requirements_dev.txt",
    "pyproject.toml",
    "setup.py",
    "setup.cfg",
    "uv.lock",
    "poetry.lock",
    "Pipfile.lock",
)

LOCK_FILES = ("uv.lock", "poetry.lock", "Pipfile.lock")


def read_dep_pins(src_root: str, names: tuple[str, ...] = ("mcp", "fastmcp", "mcpserver")) -> dict[str, DepPin]:
    """対象パッケージの依存版の確定状況を読む。

    lock ファイルを最優先する（規則 1）。次に `==` / `~=` / 上限つき。
    `>=` だけの指定は**確定しない**（規則 2）。
    """
    out: dict[str, DepPin] = {}
    found_files: list[str] = []
    for dirpath, dirs, files in os.walk(src_root):
        dirs[:] = sorted(d for d in dirs if not d.startswith("."))
        for fn in sorted(files):
            if fn in DEP_FILES or (fn.startswith("requirements") and fn.endswith(".txt")):
                found_files.append(os.path.join(dirpath, fn))

    # lock ファイル優先
    for path in found_files:
        base = os.path.basename(path)
        if base not in LOCK_FILES:
            continue
        text = _read(path)
        for name in names:
            v = _lock_version(text, name, base)
            if v:
                out[name] = DepPin(name, None, "lockfile", v, os.path.relpath(path, src_root))

    for path in found_files:
        base = os.path.basename(path)
        if base in LOCK_FILES:
            continue
        text = _read(path)
        for name in names:
            if name in out:
                continue
            spec = _spec_for(text, name)
            if spec is None:
                continue
            out[name] = _classify(name, spec, os.path.relpath(path, src_root))
    for name in names:
        out.setdefault(name, DepPin(name, None, "unreadable", None, ""))
    return out


#: `fastmcp` のこの版以上は `mcp>=2.0` を要求する（fastmcp-slim 4.0.10 の METADATA:
#: `Requires-Dist: mcp<3.0.0,>=2.0.0`。D64 / U38）。
FASTMCP_MCP2_MAJOR = 4

_SPEC_CLAUSE = re.compile(r"(===|==|~=|>=|<=|!=|>|<)\s*([0-9][0-9A-Za-z.*+!_-]*)")


def is_dep_file(fn: str) -> bool:
    """依存の記載のファイル名か（:data:`DEP_FILES` と `requirements*.txt`）。"""
    return fn in DEP_FILES or (fn.startswith("requirements") and fn.endswith(".txt"))


def dep_files(src_root: str) -> list[str]:
    """木の中の依存の記載のファイル（`src_root` からの相対パス、決定論的な順序）。

    隠しディレクトリと `srcindex._SKIP_DIRS`（`venv` / `node_modules` など。`.py` の索引も見ない所）は
    見ない（D64 / U38 の ADV-3: 依存記載のあるディレクトリをサブプロジェクトの境界に使うので、索引の外の
    記載で境界を作らない）。境界になるのは、この中で :func:`mcp_major_votes_by_file` の票を持つ記載の
    ディレクトリだけ（D64 / U38 の 3 巡目 RC-1。票の無い記載は境界にしない）。
    """
    from .srcindex import _SKIP_DIRS

    out: list[str] = []
    for dirpath, dirs, files in os.walk(src_root):
        dirs[:] = sorted(d for d in dirs if not d.startswith(".") and d not in _SKIP_DIRS)
        for fn in sorted(files):
            if is_dep_file(fn):
                out.append(os.path.relpath(os.path.join(dirpath, fn), src_root))
    return out


def mcp_major_votes(src_root: str) -> list[tuple[str, str]]:
    """木の中の依存の記載**ファイルごと**に、mcp の主版が 2 以上（``ge2``）か 2 未満（``lt2``）かの票。

    `(出所の説明, 票)` の列。:func:`mcp_major_votes_by_file` から記載のファイルの列を落としたもの。
    """
    return [(label, vote) for _rel, label, vote in mcp_major_votes_by_file(src_root)]


def mcp_major_votes_by_file(src_root: str) -> list[tuple[str, str, str]]:
    """依存の記載ファイルごとの mcp の主版の票 `(記載の相対パス, 出所の説明, "ge2" | "lt2")`（決定論的な順序）。

    **1 つの lock を選ばない**（D64 / U38、fix_outline 条件 (2)）。:func:`read_dep_pins` は
    `os.walk` の順でどれか 1 つの lock を採るので、lock が食い違う monorepo でも版が「確定」して見える。
    ここではすべての記載を票として返し、どの票をどのユニットに効かせるか（サブツリー）と食い違いの扱いは
    呼び出し側（:func:`entries.mcp_version_class`）が決める。

    票になるもの（どれも記載そのものから決まるものだけ。推定で埋めない）:

    * lock ファイルの `mcp` の解決済み版 → 主版で ``ge2`` / ``lt2``
    * 指定 `mcp==X` / `mcp~=X` → X の主版。`mcp>=X` / `mcp>X`（X の主版が 2 以上）→ ``ge2``
      （`>=2.0` は正確な版を決めないが主版 2 以上は決める）。`mcp<X`（X <= 2.0）/ `mcp<=X`（X < 2.0）→ ``lt2``
    * `fastmcp` の lock の版・`==` / `~=` / `>=` の下限が 4 以上 → ``ge2``（:data:`FASTMCP_MCP2_MAJOR`）
    * **`fastmcp` の lock の版が 4 未満、または指定の上限が 4 未満 → ``lt2``**（D64 / U38 の敵対的レビュー ADV-3。
      PyPI の requires_dist で fastmcp 2.3.0 は `mcp<2.0.0,>=1.8.0`、2.12.4 は `mcp<2.0.0,>=1.12.4`、
      3.0.0 / 3.2.0 は `mcp<2.0,>=1.24.0`（レビュー役が確認。この修正では確かめていない）。ge2 の側だけ数えると、
      隣のサブプロジェクトの ge2 の票で木全体が ge2 に倒れ、fastmcp 2 のサーバーの snake_case が宣言になった）

    **依存の指定として書かれた文字列だけを読む**（ADV-4。コメントや description の中の `mcp>=2` を票にしない）:

    * `requirements*.txt`: `#` 以降を落とし、1 行 1 要求として名前を先頭で取る（`-r` などのオプション行は読まない）
    * `pyproject.toml`: `[project]` の `dependencies` と `optional-dependencies` の文字列要素だけ
      （:func:`_pyproject_requirements`）
    * `setup.cfg`: `[options]` の `install_requires` と `[options.extras_require]` の値だけ
    * `setup.py`: `setup(install_requires=..., extras_require=...)` のリテラル（とモジュール直下の名前の束縛）だけ

    1 つの指定の中で ``ge2`` と ``lt2`` の両方が出る（満たせない指定）ときは票にしない。
    """
    votes: list[tuple[str, str, str]] = []
    for rel in dep_files(src_root):
        fn = os.path.basename(rel)
        text = _read(os.path.join(src_root, rel))
        if fn in LOCK_FILES:
            v = _lock_version(text, "mcp", fn)
            if v:
                votes.append((rel, f"lock:{rel}:mcp=={v}", "ge2" if _major(v) >= 2 else "lt2"))
            fv = _lock_version(text, "fastmcp", fn)
            if fv:
                votes.append((rel, f"lock:{rel}:fastmcp=={fv}", "ge2" if _major(fv) >= FASTMCP_MCP2_MAJOR else "lt2"))
            continue
        for req in _requirement_strings(fn, text):
            parsed = _parse_requirement(req)
            if parsed is None:
                continue
            name, spec = parsed
            if name == "mcp":
                vote = _spec_major_vote(spec)
                if vote is not None:
                    votes.append((rel, f"spec:{rel}:mcp{spec}", vote))
            elif name == "fastmcp":
                fvote = _fastmcp_vote(spec)
                if fvote is not None:
                    votes.append((rel, f"spec:{rel}:fastmcp{spec}", fvote))
    return votes


# -- 依存の記載の読み取り（D64 / U38 の ADV-4）--------------------------------

#: PEP 508 の要求の先頭（名前と extras）。名前は PEP 503 で正規化して比べる。
_REQ_HEAD = re.compile(r"^\s*([A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?)\s*(\[[^\]]*\])?\s*(.*)$", re.S)


def _parse_requirement(req: str) -> Optional[tuple[str, str]]:
    """PEP 508 の要求 1 つを `(正規化した名前, 版指定)` にする。URL 指定は版指定を空にする。

    名前の後に版指定・URL・marker でない語が続くもの（自由文）は None。
    """
    m = _REQ_HEAD.match(req)
    if not m:
        return None
    name = re.sub(r"[-_.]+", "-", m.group(1)).lower()
    rest = m.group(3).split(";", 1)[0].strip()
    if rest.startswith("@"):
        return name, ""
    if rest.startswith("(") and rest.endswith(")"):
        rest = rest[1:-1].strip()
    if rest and rest[0] not in "<>=!~":
        return None
    return name, rest


def _requirement_strings(fn: str, text: str) -> list[str]:
    """依存の記載ファイルから、**依存の指定として書かれた**要求の文字列だけを取り出す（lock は除く）。"""
    if fn == "pyproject.toml":
        return _pyproject_requirements(text)
    if fn == "setup.cfg":
        return _setup_cfg_requirements(text)
    if fn == "setup.py":
        return _setup_py_requirements(text)
    out: list[str] = []
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if not line or line.startswith("-"):
            continue
        out.append(line)
    return out


def _pyproject_requirements(text: str) -> list[str]:
    """`[project]` の `dependencies` と `optional-dependencies`（鍵の名前順）の文字列要素。読めない TOML は空。"""
    data = _toml_loads(text)
    if not isinstance(data, dict):
        return []
    proj = data.get("project")
    if not isinstance(proj, dict):
        return []
    out: list[str] = []
    deps = proj.get("dependencies")
    if isinstance(deps, list):
        out += [d for d in deps if type(d) is str]
    opt = proj.get("optional-dependencies")
    if isinstance(opt, dict):
        for key in sorted(k for k in opt if isinstance(k, str)):
            if isinstance(opt[key], list):
                out += [d for d in opt[key] if type(d) is str]
    return out


def _setup_cfg_requirements(text: str) -> list[str]:
    """`setup.cfg` の `[options] install_requires` と `[options.extras_require]` の値（1 行 1 要求）。"""
    import configparser

    cp = configparser.ConfigParser(interpolation=None, strict=False)
    try:
        cp.read_string(text)
    except (configparser.Error, ValueError):
        return []
    values: list[str] = []
    if cp.has_option("options", "install_requires"):
        values.append(cp.get("options", "install_requires"))
    if cp.has_section("options.extras_require"):
        values += [cp.get("options.extras_require", k) for k in sorted(cp.options("options.extras_require"))]
    out: list[str] = []
    for v in values:
        for line in v.splitlines():
            line = line.split("#", 1)[0].strip()
            if line:
                out.append(line)
    return out


def _setup_py_requirements(text: str) -> list[str]:
    """`setup(install_requires=[...], extras_require={...: [...]})` の文字列リテラル。名前はモジュール直下の
    ちょうど 1 つの `NAME = [...]` に解けるときだけ読む。"""
    import ast

    try:
        tree = ast.parse(text.encode("utf-8"))
    except (SyntaxError, ValueError, RecursionError):
        return []
    assigns: dict[str, list[ast.AST]] = {}
    for st in tree.body:
        if isinstance(st, ast.Assign):
            for t in st.targets:
                if isinstance(t, ast.Name):
                    assigns.setdefault(t.id, []).append(st.value)

    def resolve(node: ast.AST) -> ast.AST:
        if isinstance(node, ast.Name) and len(assigns.get(node.id, [])) == 1:
            return assigns[node.id][0]
        return node

    def strs(node: ast.AST) -> list[str]:
        node = resolve(node)
        if isinstance(node, (ast.List, ast.Tuple)):
            return [e.value for e in node.elts if isinstance(e, ast.Constant) and isinstance(e.value, str)]
        return []

    out: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        f = node.func
        fname = f.id if isinstance(f, ast.Name) else (f.attr if isinstance(f, ast.Attribute) else "")
        if fname != "setup":
            continue
        for kw in node.keywords:
            if kw.arg == "install_requires":
                out += strs(kw.value)
            elif kw.arg == "extras_require":
                v = resolve(kw.value)
                if isinstance(v, ast.Dict):
                    for ev in v.values:
                        out += strs(ev)
    return out


# -- TOML（Python 3.10 に tomllib は無い。解析器は標準ライブラリだけを使う §5.0）-----------

try:  # pragma: no cover - 処理系の版による
    import tomllib as _tomllib  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover
    _tomllib = None


def _toml_loads(text: str) -> Optional[dict]:
    """TOML を読む。tomllib（3.11 以上）が無ければ :func:`_toml_subset_loads`。読めなければ None（票にしない）。"""
    if _tomllib is not None:
        try:
            return _tomllib.loads(text)
        except (ValueError, TypeError):
            return None
    try:
        return _toml_subset_loads(text)
    except (ValueError, IndexError, RecursionError):
        return None


class _TomlBare(str):
    """引用符の無い値（数・真偽・日時）。文字列の要素と区別する（tomllib では str にならない）。"""


_TOML_BARE = re.compile(r"[A-Za-z0-9_\-+.:]+")
_TOML_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_TOML_TIME = re.compile(r"^\d{2}:\d{2}")
_TOML_ESCAPES = {"b": "\b", "t": "\t", "n": "\n", "f": "\f", "r": "\r", '"': '"', "\\": "\\"}


def _toml_unescape(s: str, multiline: bool = False) -> str:
    out: list[str] = []
    i = 0
    while i < len(s):
        c = s[i]
        if c != "\\":
            out.append(c)
            i += 1
            continue
        nxt = s[i + 1] if i + 1 < len(s) else ""
        if nxt in _TOML_ESCAPES and nxt:
            out.append(_TOML_ESCAPES[nxt])
            i += 2
        elif nxt in ("u", "U") and nxt:
            width = 4 if nxt == "u" else 8
            out.append(chr(int(s[i + 2 : i + 2 + width], 16)))
            i += 2 + width
        elif multiline and s[i + 1 :].lstrip(" \t").startswith(("\n", "\r\n")):
            i += 1
            while i < len(s) and s[i] in " \t\r\n":
                i += 1
        else:
            raise ValueError("bad escape")
    return "".join(out)


def _toml_tokens(text: str) -> list[tuple[str, Optional[str]]]:
    out: list[tuple[str, Optional[str]]] = []
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if c in " \t\r":
            i += 1
        elif c == "\n":
            out.append(("NL", None))
            i += 1
        elif c == "#":
            j = text.find("\n", i)
            i = n if j < 0 else j
        elif text.startswith('"""', i) or text.startswith("'''", i):
            q = text[i : i + 3]
            j = text.find(q, i + 3)
            if j < 0:
                raise ValueError("unterminated multi-line string")
            extra = 0
            while extra < 2 and j + 3 < n and text[j + 3] == q[0]:
                j += 1  # 閉じの直前の引用符 1〜2 個は中身
                extra += 1
            body = text[i + 3 : j]
            if body.startswith("\r\n"):
                body = body[2:]
            elif body.startswith("\n"):
                body = body[1:]
            out.append(("STR", _toml_unescape(body, multiline=True) if q == '"""' else body))
            i = j + 3
        elif c == '"':
            j = i + 1
            while j < n and text[j] != '"':
                if text[j] == "\n":
                    raise ValueError("newline in string")
                j += 2 if text[j] == "\\" else 1
            if j >= n:
                raise ValueError("unterminated string")
            out.append(("STR", _toml_unescape(text[i + 1 : j])))
            i = j + 1
        elif c == "'":
            j = text.find("'", i + 1)
            if j < 0 or "\n" in text[i + 1 : j]:
                raise ValueError("unterminated literal string")
            out.append(("STR", text[i + 1 : j]))
            i = j + 1
        elif c in "[]{}=,":
            out.append((c, None))
            i += 1
        else:
            m = _TOML_BARE.match(text, i)
            if not m:
                raise ValueError(f"unexpected character {c!r}")
            out.append(("BARE", m.group(0)))
            i = m.end()
    out.append(("NL", None))
    return out


def _toml_subset_loads(text: str) -> dict:  # noqa: C901
    """依存の配列を読むのに足りる TOML の部分集合（表・配列の表・点つきの鍵・文字列・配列・インラインの表）。

    tomllib の無い処理系（3.10）で使う**保守的な**読み手。読めない形は ValueError（呼び出し側で票にしない）。
    コメントは読まず、文字列（複数行を含む）の中身は値の文字列としてしか現れないので、自由文の `mcp>=2` を
    依存の指定として読むことはない（ADV-4）。
    """
    toks = _toml_tokens(text)
    root: dict = {}
    defined: set[tuple[str, ...]] = set()
    pos = 0

    def key_path(end: str) -> list[str]:
        nonlocal pos
        path: list[str] = []
        while toks[pos][0] != end:
            kind, val = toks[pos]
            if kind == "BARE":
                path += [p for p in (val or "").split(".") if p]
            elif kind == "STR":
                path.append(val or "")
            else:
                raise ValueError("bad key")
            pos += 1
        if not path:
            raise ValueError("empty key")
        return path

    def descend(base: dict, path: list[str]) -> dict:
        cur = base
        for p in path:
            nxt = cur.setdefault(p, {})
            if isinstance(nxt, list) and nxt and isinstance(nxt[-1], dict):
                nxt = nxt[-1]
            if not isinstance(nxt, dict):
                raise ValueError("key is not a table")
            cur = nxt
        return cur

    def skip_nl() -> None:
        nonlocal pos
        while toks[pos][0] == "NL":
            pos += 1

    def value():
        nonlocal pos
        kind, val = toks[pos]
        pos += 1
        if kind == "STR":
            return val
        if kind == "BARE":
            return _TomlBare(val)
        if kind == "[":
            arr: list = []
            skip_nl()
            while toks[pos][0] != "]":
                arr.append(value())
                skip_nl()
                if toks[pos][0] == ",":
                    pos += 1
                    skip_nl()
                elif toks[pos][0] != "]":
                    raise ValueError("bad array")
            pos += 1
            return arr
        if kind == "{":
            tbl: dict = {}
            while toks[pos][0] != "}":
                path = key_path("=")
                pos += 1
                tgt = descend(tbl, path[:-1])
                if path[-1] in tgt:
                    raise ValueError("duplicate key")
                tgt[path[-1]] = value()
                if toks[pos][0] == ",":
                    pos += 1
                elif toks[pos][0] != "}":
                    raise ValueError("bad inline table")
            pos += 1
            return tbl
        raise ValueError("bad value")

    cur = root
    while pos < len(toks):
        kind = toks[pos][0]
        if kind == "NL":
            pos += 1
            continue
        if kind == "[":
            is_array = toks[pos + 1][0] == "["
            pos += 2 if is_array else 1
            path = key_path("]")
            pos += 1
            if is_array:
                if toks[pos][0] != "]":
                    raise ValueError("bad array-of-tables header")
                pos += 1
                parent = descend(root, path[:-1])
                lst = parent.setdefault(path[-1], [])
                if not isinstance(lst, list):
                    raise ValueError("not an array of tables")
                cur = {}
                lst.append(cur)
            else:
                if tuple(path) in defined:
                    raise ValueError("duplicate table")
                defined.add(tuple(path))
                cur = descend(root, path)
            if toks[pos][0] != "NL":
                raise ValueError("junk after header")
            continue
        path = key_path("=")
        pos += 1
        tgt = descend(cur, path[:-1])
        if path[-1] in tgt:
            raise ValueError("duplicate key")
        val = tgt[path[-1]] = value()
        if (
            toks[pos][0] == "BARE"
            and isinstance(val, _TomlBare)
            and _TOML_DATE.match(val)
            and _TOML_TIME.match(toks[pos][1] or "")
        ):
            pos += 1  # 空白で区切った日時 `1979-05-27 07:32:00Z`
        if toks[pos][0] != "NL":
            raise ValueError("junk after value")  # tomllib と同じく読めない（票にしない）
    return root


def _fastmcp_vote(spec: str) -> Optional[str]:
    """`fastmcp` の指定から mcp の主版の票。下限が 4 以上 → ``ge2``、上限が 4 未満 → ``lt2``（ADV-3）。"""
    ge = _spec_lower_major(spec) >= FASTMCP_MCP2_MAJOR
    lt = _spec_upper_below(spec, str(FASTMCP_MCP2_MAJOR))
    if ge == lt:
        return None
    return "ge2" if ge else "lt2"


def _spec_upper_below(spec: str, bound: str) -> bool:
    """指定が許す版がすべて `bound` 未満か（`<3` / `<=3.9` / `==2.*` / `==3.2.0` / `~=3.0`）。"""
    for op, ver in _SPEC_CLAUSE.findall(spec):
        v = ver.rstrip(".*")
        if not v:
            continue
        if op in ("==", "===", "~="):
            if _major(v) < _major(bound):
                return True
        elif op == "<":
            if not _ver_gt(v, bound):
                return True
        elif op == "<=":
            if _ver_lt(v, bound):
                return True
    return False


def _major(v: str) -> int:
    return _parts(v)[0] if _parts(v) else 0


def _spec_major_vote(spec: str) -> Optional[str]:
    """1 つの指定（`>=1.2,<2`）から mcp の主版が 2 以上か未満かを決める。決まらなければ None。"""
    out: set[str] = set()
    for op, ver in _SPEC_CLAUSE.findall(spec):
        ver = ver.rstrip(".*")
        if not ver:
            continue
        if op in ("==", "===", "~="):
            out.add("ge2" if _major(ver) >= 2 else "lt2")
        elif op in (">=", ">"):
            if _major(ver) >= 2:
                out.add("ge2")
        elif op == "<":
            if not _ver_gt(ver, "2"):
                out.add("lt2")  # `<2` / `<2.0` / `<1.99`
        elif op == "<=":
            if _major(ver) < 2:
                out.add("lt2")
    return out.pop() if len(out) == 1 else None


def _spec_lower_major(spec: str) -> int:
    """指定の下限の主版（`>=4,<5` → 4、`==4.0.1` → 4）。下限が無ければ 0。"""
    lo = 0
    for op, ver in _SPEC_CLAUSE.findall(spec):
        if op in ("==", "===", "~=", ">=", ">"):
            lo = max(lo, _major(ver.rstrip(".*") or "0"))
    return lo


def _ver_gt(a: str, b: str) -> bool:
    return _ver_ge(a, b) and not _ver_ge(b, a)


def _read(path: str) -> str:
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def _spec_for(text: str, name: str) -> Optional[str]:
    pattern = re.compile(rf"['\"]?\b{re.escape(name)}\b['\"]?\s*([<>=!~][^'\",\]\n]*)")
    m = pattern.search(text)
    if m:
        return m.group(1).strip()
    if re.search(rf"^\s*{re.escape(name)}\s*$", text, re.M):
        return ""
    return None


def _classify(name: str, spec: str, source: str) -> DepPin:
    if not spec:
        return DepPin(name, spec, "lower_bound_only", None, source)
    m = _PIN_EXACT.search(spec)
    if m:
        return DepPin(name, spec, "exact", m.group(1), source)
    m = _PIN_COMPAT.search(spec)
    if m:
        return DepPin(name, spec, "exact", m.group(1), source)
    if _PIN_UPPER.search(spec):
        return DepPin(name, spec, "upper_bounded", _PIN_UPPER.search(spec).group(1), source)
    if _PIN_LOWER_ONLY.match(spec):
        return DepPin(name, spec, "lower_bound_only", None, source)
    return DepPin(name, spec, "lower_bound_only", None, source)


def _lock_version(text: str, name: str, lock_kind: str) -> Optional[str]:
    if lock_kind == "uv.lock" or lock_kind == "poetry.lock":
        pattern = re.compile(rf'name\s*=\s*"{re.escape(name)}"\s*\nversion\s*=\s*"([^"]+)"')
        m = pattern.search(text)
        if m:
            return m.group(1)
    if lock_kind == "Pipfile.lock":
        pattern = re.compile(rf'"{re.escape(name)}":\s*\{{[^}}]*"version":\s*"==([^"]+)"')
        m = pattern.search(text)
        if m:
            return m.group(1)
    return None


# --------------------------------------------------------------------------
# 判定
# --------------------------------------------------------------------------


@dataclass
class EnforcementVerdict:
    """1 ユニットの執行性判定。"""

    path: str
    verdict: str  # enforced | not_enforced | D_unknown
    reason: str
    pin: Optional[DepPin] = None

    def to_json(self) -> dict:
        d = {"path": self.path, "verdict": self.verdict, "reason": self.reason}
        if self.pin is not None:
            d["pin"] = self.pin.to_json()
        return d


def classify_unit(framework: str, entry_kind: str, pins: dict[str, DepPin]) -> EnforcementVerdict:
    """ユニットの登録経路と依存版から執行性を決める。

    **判定は (1) 登録 API の形状 → (2) 版の確定可否 の順。**
    """
    path = PATH_OF_ENTRY.get((framework, entry_kind))
    if path is None:
        return EnforcementVerdict("dynamic_schema", "D_unknown", "登録経路が執行表に無い")
    row = ENFORCEMENT_BY_PATH[path]

    if row.verdict == "enforced":
        return EnforcementVerdict(path, "enforced", row.evidence)
    if row.verdict == "not_enforced":
        # 規則 3: API 形状で決まる（`Server(on_call_tool=)` は必ず >= 2.0）。
        return EnforcementVerdict(path, "not_enforced", row.evidence + " / API 形状で確定")
    if row.verdict == "unknown":
        return EnforcementVerdict(path, "D_unknown", row.evidence)

    # version_dependent: `@server.call_tool()` は v2 に存在しないので実行時は必ず < 2.0。
    # [1.10, 2.0) か < 1.10 かを版で決める。
    pin = pins.get("mcp")
    if pin is None or not pin.is_determined or pin.version is None:
        return EnforcementVerdict(
            path,
            "D_unknown",
            "版が確定しない（`>=` だけの指定は版を確定しない。規則 2）。"
            "**既定で「執行あり」とも「執行なし」とも仮定しない**（規則 4）",
            pin,
        )
    lo, hi = row.enforced_range or ("0", "0")
    if _ver_ge(pin.version, lo) and _ver_lt(pin.version, hi):
        return EnforcementVerdict(path, "enforced", f"版 {pin.version} は [{lo}, {hi}) にある", pin)
    return EnforcementVerdict(path, "not_enforced", f"版 {pin.version} は [{lo}, {hi}) の外", pin)


def _parts(v: str) -> tuple[int, ...]:
    out: list[int] = []
    for chunk in re.split(r"[._-]", v):
        m = re.match(r"^(\d+)", chunk)
        out.append(int(m.group(1)) if m else 0)
    return tuple(out)


def _ver_ge(a: str, b: str) -> bool:
    pa, pb = _parts(a), _parts(b)
    n = max(len(pa), len(pb))
    return pa + (0,) * (n - len(pa)) >= pb + (0,) * (n - len(pb))


def _ver_lt(a: str, b: str) -> bool:
    return not _ver_ge(a, b)
