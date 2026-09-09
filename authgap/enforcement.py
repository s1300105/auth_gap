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
