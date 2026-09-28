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


def mcp_major_votes(src_root: str) -> list[tuple[str, str]]:
    """木の中の依存の記載**ファイルごと**に、mcp の主版が 2 以上（``ge2``）か 2 未満（``lt2``）かの票。

    **1 つの lock を選ばない**（D64 / U38、fix_outline 条件 (2)）。:func:`read_dep_pins` は
    `os.walk` の順でどれか 1 つの lock を採るので、lock が食い違う monorepo でも版が「確定」して見える。
    ここではすべての記載を票として返し、食い違いは呼び出し側が「決まらない」にする。

    票になるもの（どれも記載そのものから決まるものだけ。推定で埋めない）:

    * lock ファイルの `mcp` の解決済み版 → 主版で ``ge2`` / ``lt2``
    * 記載の指定 `mcp==X` / `mcp~=X` → X の主版。`mcp>=X` / `mcp>X`（X の主版が 2 以上）→ ``ge2``
      （`>=2.0` は正確な版を決めないが主版 2 以上は決める）。`mcp<X`（X <= 2.0）/ `mcp<=X`（X < 2.0）→ ``lt2``
    * `fastmcp` の lock の版・`==` / `~=` / `>=` の下限が 4 以上 → ``ge2``（:data:`FASTMCP_MCP2_MAJOR`）

    1 つの指定の中で ``ge2`` と ``lt2`` の両方が出る（満たせない指定）ときは票にしない。
    :returns: `(出所の説明, "ge2" | "lt2")` の列（決定論的な順序）
    """
    votes: list[tuple[str, str]] = []
    for dirpath, dirs, files in os.walk(src_root):
        dirs[:] = sorted(d for d in dirs if not d.startswith("."))
        for fn in sorted(files):
            if not (fn in DEP_FILES or (fn.startswith("requirements") and fn.endswith(".txt"))):
                continue
            path = os.path.join(dirpath, fn)
            rel = os.path.relpath(path, src_root)
            text = _read(path)
            if fn in LOCK_FILES:
                v = _lock_version(text, "mcp", fn)
                if v:
                    votes.append((f"lock:{rel}:mcp=={v}", "ge2" if _major(v) >= 2 else "lt2"))
                fv = _lock_version(text, "fastmcp", fn)
                if fv and _major(fv) >= FASTMCP_MCP2_MAJOR:
                    votes.append((f"lock:{rel}:fastmcp=={fv}", "ge2"))
                continue
            for spec in _requirement_specs(text, "mcp"):
                vote = _spec_major_vote(spec)
                if vote is not None:
                    votes.append((f"spec:{rel}:mcp{spec}", vote))
            for fspec in _requirement_specs(text, "fastmcp"):
                if _spec_lower_major(fspec) >= FASTMCP_MCP2_MAJOR:
                    votes.append((f"spec:{rel}:fastmcp{fspec}", "ge2"))
    return votes


def _requirement_specs(text: str, name: str) -> list[str]:
    """記載の中の `name` の版指定（PEP 508 の extras `mcp[cli]>=2` を含む。`,` で続く句も含める）。

    :func:`_spec_for` は `mcp[cli]` を読まず、`fastapi-mcp==0.3` の末尾を `mcp==0.3` と読む。票は宣言の読み方を
    変えるので、名前の前後が名前の文字（英数字・`-`・`_`・`.`）でないものだけを採る。
    """
    pat = re.compile(
        rf"(?<![\w.-]){re.escape(name)}(?![\w.-])(?:\[[^\]]*\])?\s*((?:===|==|~=|>=|<=|!=|>|<)\s*[0-9][^'\"\n;#\]]*)"
    )
    return [m.group(1).strip() for m in pat.finditer(text)]


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
