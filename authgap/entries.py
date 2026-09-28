"""Def 2 の R1 / R2: MODEL 導入点の発見と、ユニット（解析単位）の切り出し。

**解析開始点は callee 内である。** 呼び出し元集合の完全性は要求しない。
完全性の要求は「R1/R2 のユニット入口カタログ」へ移るだけであり、
カタログ外の呼び出し元からのみ到達する効果は取り落とす（§Def 4 の残余仮定）。

unit id は `framework:qualified_name:schema_hash`（§5.2）。
`schema_hash` は静的に得られる入力スキーマの正規化 JSON の sha256 先頭 12 桁。
**ファイル移動には安定。rename とスキーマ変更は diff で delete+add として現れる。**
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
from dataclasses import dataclass, field
from typing import Any, Optional

from .catalog.entries import (
    ENTRY_RULES,
    LLM_CALLS,
    LOWLEVEL_V2_KWARGS,
    LOWLEVEL_V2_REQUEST,
    R2_EXCEPTIONS,
    SPEC_OBJECT_ORIGINS,
    TOOLMESSAGE_META_FIELDS,
    EntryRule,
    find_entry_rule,
)
from .srcindex import FuncDef, Scope, SourceIndex, dotted_of

#: `match` 文は Python 3.10 以降にしか無い。
_MATCH_CASE = getattr(ast, "match_case", None)


@dataclass
class Param:
    """ツールエントリの仮引数 1 つ。"""

    name: str
    index: int
    annotation: Optional[str] = None
    default_repr: Optional[str] = None
    #: `val = MODEL` としない（Def 2 の R2 例外）。
    excluded: bool = False
    excluded_reason: Optional[str] = None

    def to_json(self) -> dict:
        d: dict[str, Any] = {"name": self.name, "index": self.index}
        if self.annotation:
            d["annotation"] = self.annotation
        if self.default_repr is not None:
            d["default"] = self.default_repr
        if self.excluded:
            d["excluded"] = self.excluded_reason
        return d


@dataclass
class Unit:
    """R2 のツールエントリ 1 つ。解析と labelling の単位は**ツール**である。"""

    framework: str
    entry_kind: str
    module: str
    qualname: str
    relpath: str
    node: ast.AST
    params: list[Param] = field(default_factory=list)
    #: 宣言されたツール名（デコレータの `name=` またはメソッド名）。
    tool_name: Optional[str] = None
    #: `Tool(...)` リテラルから join した MCP annotations（D_kind の源）。
    annotations: Optional[dict] = None
    #: annotations の読み取りで扱えなかった形。
    annotation_form: Optional[str] = None
    #: **snake_case 表記の注釈キー**（`read_only_hint` 等）。仕様書 322 行目は
    #: 「`ToolAnnotations` に deserialize されず protocol に届かないので
    #: `D_malformed` として別行で報告する」と定める。**記録だけで上界は動かさない。**
    #: 動かすと「書いただけで宣言したことになる」= 誤 clear になる（O27 / D48）。
    malformed_fields: tuple[str, ...] = ()
    #: 低レベル経路のとき、ハンドラ内の name 分岐から得た候補名。
    dispatch_names: tuple[str, ...] = ()
    #: 低レベル経路のとき、`dispatch_names` で join した `Tool(...)` リテラルの
    #: 宣言（ツール名 → `(annotations, form)`）。`docs/preregistration.md` §2.9 (a)。
    dispatch_annotations: dict[str, tuple[Optional[dict], str]] = field(default_factory=dict)
    #: 同じファイルにあって名前が文字列リテラルでないため join できなかったリテラル数（§2.9 (d)）。
    dispatch_unjoined: int = 0
    is_async: bool = False
    #: `toolmessage_handler` 形のとき、MODEL 値を運ぶ仮引数の名前（`msg`）。
    message_param: Optional[str] = None
    #: 同じく、`ToolMessage` 派生クラスの `(フィールド名, 注釈)`。
    message_fields: tuple[tuple[str, Optional[str]], ...] = ()
    #: 同じく、`ToolMessage` 派生クラス名。
    message_class: Optional[str] = None
    #: 呼び出し形の登録（`x.tool(...)(fn)` / `x.add_tool(fn)`）と `spec_object` のとき、登録文の
    #: `{"form", "relpath", "lineno"}`（D64 / U40）。ユニットの位置（`relpath` / `lineno`）は関数の定義。
    registration: Optional[dict] = None

    @property
    def schema_hash(self) -> str:
        payload = {
            "params": [
                {"name": p.name, "annotation": p.annotation, "default": p.default_repr}
                for p in self.params
            ]
        }
        blob = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:12]

    @property
    def unit_id(self) -> str:
        return f"{self.framework}:{self.qualname}:{self.schema_hash}"

    @property
    def model_params(self) -> list[Param]:
        """R2 が MODEL ラベルを付ける引数（例外に当たるものを除く）。"""
        return [p for p in self.params if not p.excluded]

    def to_json(self) -> dict:
        d: dict[str, Any] = {
            "unit_id": self.unit_id,
            "framework": self.framework,
            "entry_kind": self.entry_kind,
            "module": self.module,
            "qualname": self.qualname,
            "relpath": self.relpath,
            "lineno": getattr(self.node, "lineno", None),
            "tool_name": self.tool_name,
            "params": [p.to_json() for p in self.params],
            "schema_hash": self.schema_hash,
            "is_async": self.is_async,
        }
        if self.annotations is not None:
            d["annotations"] = self.annotations
        if self.annotation_form:
            d["annotation_form"] = self.annotation_form
        if self.malformed_fields:
            d["malformed_fields"] = list(self.malformed_fields)
        if self.dispatch_names:
            d["dispatch_names"] = list(self.dispatch_names)
        if self.dispatch_annotations:
            d["dispatch_annotations"] = {
                k: {"annotations": a, "form": f} for k, (a, f) in sorted(self.dispatch_annotations.items())
            }
            d["dispatch_unjoined"] = self.dispatch_unjoined
        if self.message_param:
            d["message_param"] = self.message_param
            d["message_class"] = self.message_class
            d["message_fields"] = [[n, a] for n, a in self.message_fields]
        if self.registration:
            d["registration"] = dict(self.registration)
        return d


# --------------------------------------------------------------------------
# R1: LLM 呼び出し
# --------------------------------------------------------------------------


def is_llm_call(call: ast.Call) -> bool:
    """カタログ化した LLM 呼び出しか（dotted 名の**末尾一致**で照合する）。"""
    name = dotted_of(call.func)
    if name is None:
        return False
    for pat in LLM_CALLS:
        if name == pat or name.endswith("." + pat):
            return True
    return False


def llm_calls_in(fn: ast.AST) -> list[ast.Call]:
    return [n for n in ast.walk(fn) if isinstance(n, ast.Call) and is_llm_call(n)]


# --------------------------------------------------------------------------
# R2: ツールエントリ
# --------------------------------------------------------------------------


def _annotation_str(node: Optional[ast.AST]) -> Optional[str]:
    """注釈を**文字列として読むだけ**。型環境は構築しない（§2.6）。"""
    if node is None:
        return None
    try:
        return ast.unparse(node)
    except Exception:  # pragma: no cover - 3.10 未満では来ない
        return None


def _r2_excluded(annotation: Optional[ast.AST]) -> tuple[bool, Optional[str]]:
    """Def 2 の R2 例外に当たるか。

    フレームワークが実行時に「このパラメータをモデルに見せない」ことを執行する
    機械可読な指定がある引数は `val = MODEL` としない。
    """
    if annotation is None:
        return False, None
    text = _annotation_str(annotation) or ""
    for exc in R2_EXCEPTIONS:
        if exc.marker_key in text and repr(exc.marker_value) in text.replace("'", ""):
            return True, f"{exc.framework}:{exc.marker_key}"
        if exc.marker_key in text and str(exc.marker_value) in text:
            return True, f"{exc.framework}:{exc.marker_key}"
    return False, None


def params_of(fn: ast.AST, exclude: tuple[str, ...] = ("self", "cls")) -> list[Param]:
    args = getattr(fn, "args", None)
    if args is None:
        return []
    out: list[Param] = []
    positional = list(args.posonlyargs) + list(args.args)
    defaults = list(args.defaults)
    pad = len(positional) - len(defaults)
    for i, a in enumerate(positional):
        if a.arg in exclude:
            continue
        default = None
        if i >= pad:
            try:
                default = ast.unparse(defaults[i - pad])
            except Exception:  # pragma: no cover
                default = "<unparseable>"
        excluded, reason = _r2_excluded(a.annotation)
        out.append(Param(a.arg, i, _annotation_str(a.annotation), default, excluded, reason))
    for j, a in enumerate(args.kwonlyargs):
        if a.arg in exclude:
            continue
        d = args.kw_defaults[j]
        default = None
        if d is not None:
            try:
                default = ast.unparse(d)
            except Exception:  # pragma: no cover
                default = "<unparseable>"
        excluded, reason = _r2_excluded(a.annotation)
        out.append(Param(a.arg, len(positional) + j, _annotation_str(a.annotation), default, excluded, reason))
    return out


def _decorator_calls(fn: ast.AST) -> list[tuple[str, Optional[ast.Call], ast.AST]]:
    """`(dotted 名, 呼び出しなら Call, デコレータ式)` の列。"""
    out: list[tuple[str, Optional[ast.Call], ast.AST]] = []
    for d in getattr(fn, "decorator_list", []):
        if isinstance(d, ast.Call):
            name = dotted_of(d.func)
            if name:
                out.append((name, d, d))
        else:
            name = dotted_of(d)
            if name:
                out.append((name, None, d))
    return out


def _match_decorator(name: str) -> Optional[EntryRule]:
    """デコレータ名を R2 の規則に照合する。**末尾成分で照合する。**"""
    last = name.split(".")[-1]
    for rule in ENTRY_RULES:
        if rule.kind != "decorator":
            continue
        for pat in rule.names:
            if name == pat or last == pat.split(".")[-1]:
                return rule
    return None


def _kwarg_str(call: Optional[ast.Call], key: str) -> Optional[str]:
    if call is None:
        return None
    for kw in call.keywords:
        if kw.arg == key and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
            return kw.value.value
    return None


def _positional_str(call: Optional[ast.Call], idx: Optional[int]) -> Optional[str]:
    if call is None or idx is None or idx >= len(call.args):
        return None
    a = call.args[idx]
    return a.value if isinstance(a, ast.Constant) and isinstance(a.value, str) else None


def _kwarg_node(call: Optional[ast.Call], key: str) -> Optional[ast.AST]:
    if call is None:
        return None
    for kw in call.keywords:
        if kw.arg == key:
            return kw.value
    return None


def _is_name_decl(node: ast.AST) -> bool:
    """名前の宣言として読める形: 定数、または文字列定数 / 名前だけを要素に持つ list / tuple。"""
    if isinstance(node, ast.Constant):
        return True
    if isinstance(node, (ast.List, ast.Tuple)) and node.elts:
        return all(
            isinstance(e, ast.Name) or (isinstance(e, ast.Constant) and isinstance(e.value, str))
            for e in node.elts
        )
    return False


def _has_catalog_signature(call: Optional[ast.Call], rule: EntryRule) -> bool:
    """`require_positional` を持つ規則（AutoGPT `@command`）の呼び出し形か。

    * 位置形: `@command("name", "desc", {...})` / `@command(["a", "b"], "desc", {...})`
    * キーワード形: `@command(names=[...], description=..., parameters={...})`
    """
    if call is None:
        return False
    if len(call.args) >= (rule.require_positional or 0) and call.args:
        if _is_name_decl(call.args[rule.name_arg or 0]):
            return True
    if rule.names_kwarg and rule.schema_kwarg:
        names = _kwarg_node(call, rule.names_kwarg)
        schema = _kwarg_node(call, rule.schema_kwarg)
        if names is not None and schema is not None and _is_name_decl(names):
            return True
    return False


def _first_listed_name(call: Optional[ast.Call], rule: EntryRule) -> Optional[str]:
    """名前の list（位置 `name_arg` か `names_kwarg`）の最初の文字列定数。"""
    if call is None:
        return None
    nodes: list[ast.AST] = []
    if rule.name_arg is not None and rule.name_arg < len(call.args):
        nodes.append(call.args[rule.name_arg])
    if rule.names_kwarg:
        kw = _kwarg_node(call, rule.names_kwarg)
        if kw is not None:
            nodes.append(kw)
    for n in nodes:
        if isinstance(n, (ast.List, ast.Tuple)):
            for e in n.elts:
                if isinstance(e, ast.Constant) and isinstance(e.value, str):
                    return e.value
    return None


def _dict_keys(node: Optional[ast.AST]) -> Optional[frozenset[str]]:
    if not isinstance(node, ast.Dict):
        return None
    out = {k.value for k in node.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)}
    return frozenset(out) if out else None


def _schema_keys(call: Optional[ast.Call], idx: Optional[int]) -> Optional[frozenset[str]]:
    """デコレータのスキーマ辞書のキー（= モデルが埋める引数名）。

    読めなければ `None` を返す。**読めないことを「全部 MODEL」とも
    「全部除外」とも解釈しない**（`None` は「宣言が無い」として扱い、
    呼び出し側が既定の全引数 MODEL に落とす）。
    """
    if call is None or idx is None:
        return None
    node = call.args[idx] if idx < len(call.args) else None
    if not isinstance(node, ast.Dict):
        return None
    out: set[str] = set()
    for k in node.keys:
        if isinstance(k, ast.Constant) and isinstance(k.value, str):
            out.add(k.value)
    return frozenset(out) if out else None


def _class_bases(index: SourceIndex, classname: str, module: Optional[str]) -> frozenset[str]:
    """クラスの基底名（1 段だけ。多重継承の連鎖は追わない）。"""
    cd = index.get_class(classname, module)
    if cd is None:
        return frozenset()
    out = set(cd.bases)
    for b in list(cd.bases):
        parent = index.get_class(b.split(".")[-1])
        if parent is not None:
            out |= set(parent.bases)
    return frozenset({b.split(".")[-1] for b in out})


def find_units(index: SourceIndex) -> list[Unit]:
    """木全体から R2 のユニットを取り出す（決定論的な順序）。"""
    units: list[Unit] = []
    for fd in index.functions():
        path = index.resolve_module_path(fd.module)
        if path is None:
            continue
        # -- デコレータ形 --------------------------------------------------
        matched = False
        for name, call, _node in _decorator_calls(fd.node):
            rule = _match_decorator(name)
            if rule is None:
                continue
            if rule.require_positional and not _has_catalog_signature(call, rule):
                # **末尾名が同じ別のデコレータと取り違えない。**
                # `@click.command()` は位置引数も `names=` / `parameters=` も取らないので落ちる。
                continue
            units.append(_decorator_unit(fd, rule, call))
            matched = True
            break
        if matched:
            continue

        # -- メソッド形 ----------------------------------------------------
        if fd.classname is None:
            continue
        bases = _class_bases(index, fd.classname, fd.module)
        method = fd.qualname.split(".")[-1]
        for rule in ENTRY_RULES:
            if rule.kind != "method":
                continue
            if not (set(rule.bases) & bases):
                continue
            if "*" not in rule.names and method not in rule.names:
                continue
            if method.startswith("__"):
                continue
            units.append(
                Unit(
                    framework=rule.framework,
                    entry_kind="method",
                    module=fd.module,
                    qualname=fd.qualname,
                    relpath=fd.relpath,
                    node=fd.node,
                    params=params_of(fd.node, rule.exclude_params),
                    tool_name=method,
                    is_async=fd.is_async,
                )
            )
            break

    units += find_lowlevel_units(index)
    units += find_toolmessage_units(index)
    # **呼び出し形の登録と spec_object は tools_list より前に置き、registered で二重登録を防ぐ**（D64 / U40）。
    # デコレータ形・メソッド形・低レベル形ですでにユニットになった関数は 2 つ目のユニットにしない。
    registered = {(u.module, u.qualname) for u in units}
    units += find_registration_units(index, registered)
    units += find_tools_list_units(index, {u.qualname for u in units}, {(u.module, u.qualname) for u in units})
    units.sort(key=lambda u: (u.relpath, u.qualname, u.framework))
    return units


def _decorator_unit(
    fd: FuncDef,
    rule: EntryRule,
    call: Optional[ast.Call],
    registration: Optional[dict] = None,
) -> Unit:
    """デコレータ規則に当たった関数のユニット。`call` はデコレータ（呼び出し形なら外側の登録呼び出し）。"""
    tool_name = (
        _kwarg_str(call, "name")
        or _positional_str(call, rule.name_arg)
        or _first_listed_name(call, rule)
        or fd.qualname.split(".")[-1]
    )
    params = params_of(fd.node, rule.exclude_params)
    declared = _schema_keys(call, rule.schema_arg)
    if declared is None and rule.schema_kwarg:
        declared = _dict_keys(_kwarg_node(call, rule.schema_kwarg))
    # **デコレータの `annotations=` はエントリ自身の宣言**（Def 6 の 3 形）。
    # 読まないと `@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))` が
    # `⊥` になり r_kind を過小に数える（D17）。
    ann_node = _kwarg_node(call, "annotations")
    ann: Optional[dict] = None
    ann_form: Optional[str] = None
    malformed: tuple[str, ...] = ()
    if ann_node is not None:
        # **3 つ目の戻り値（snake_case）を捨てない。** 捨てていたため
        # `D_malformed` が構造的に常に空だった（母集団 v2 に 574 箇所。O27 / D48）。
        ann, ann_form, malformed = _read_annotations(ann_node)
    if declared is not None:
        # **スキーマ辞書に無い仮引数は MODEL としない。**
        # 実行文脈（`agent` など）を MODEL に数えると、フレームワークが
        # 渡すオブジェクトがモデル由来の値として伝播する。
        for pm in params:
            if pm.name not in declared:
                pm.excluded = True
                pm.excluded_reason = f"{rule.framework}:not_in_tool_schema"
    return Unit(
        framework=rule.framework,
        entry_kind="decorator",
        module=fd.module,
        qualname=fd.qualname,
        relpath=fd.relpath,
        node=fd.node,
        params=params,
        tool_name=tool_name,
        annotations=ann,
        annotation_form=ann_form,
        malformed_fields=malformed,
        is_async=fd.is_async,
        registration=registration,
    )


# --------------------------------------------------------------------------
# 呼び出し形の登録と spec_object（D64 / U40）
#
# `x.tool(...)(fn)` / `x.tool(fn)` / `x.add_tool(fn, ...)` と `ToolSpec(execute=fn)` の `fn` を入口にする。
# **`fn` は登録文のスコープ（囲む関数 → モジュール → import 先）で Python の意味どおりに厳密に解く。**
# 末尾名の索引（`lookup_function(name)`）で引くと、木外の関数の登録で木内の同名の無関係な関数が偽の
# ユニットになり、宣言に対する誤警報を作る（検証役の反例 cx_r1_2_extern）。解けないもの（束縛が 2 つ以上、
# 呼び出し式・lambda・partial・ループ変数、`global` / `nonlocal` / `globals()` / `exec` / `import *` で動的に
# 書き換えうる名前）は採らない（数え落としのまま。誤警報は作らない）。
# --------------------------------------------------------------------------

_FUNC_NODES = (ast.FunctionDef, ast.AsyncFunctionDef)
_COMP_NODES = (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)
#: 属性を名前で書き換える組込み。
_SETATTR = ("setattr", "delattr")
#: 関数の値ではなく記述子を返すデコレータ（`self.m` が関数にならない）。
_NON_FUNCTION_DECORATORS = frozenset({"property", "cached_property", "setter", "getter", "deleter"})
#: import 先をたどる回数の上限（再公開の連鎖）。
_IMPORT_HOPS = 4


@dataclass(frozen=True)
class _Ref:
    """式が指すもの。`kind` は ``func`` / ``class`` / ``module``（木内）/ ``extern``（木外の dotted 名）。"""

    kind: str
    name: str
    fd: Optional[FuncDef] = None


@dataclass
class _ModInfo:
    """1 モジュールの、名前の解決に要る事実（`find_registration_units` の 1 回の走査で集める）。"""

    path: str
    tree: ast.Module
    is_pkg: bool
    #: どこかの関数で `global` / `nonlocal` と宣言された名前。
    declared: set[str] = field(default_factory=set)
    #: モジュールの名前空間を名前で書き換えうる（`globals()` / 引数なしの `vars()` を読む以外に使う、
    #: 既定の名前空間の `exec` / `eval`、`sys.modules[...]` への `setattr`）。モジュール水準の名前をどれも確定しない。
    dynamic: bool = False
    #: `alias.NAME = ...` / `del alias.NAME` / `setattr(alias, "NAME", v)` の `(alias, NAME)`（名前が定数でなければ `"*"`）。
    attr_pairs: set[tuple[str, str]] = field(default_factory=set)
    #: import で束縛される名前 → import 文（モジュール直下でも関数の中でも）。
    imports: dict[str, list[ast.AST]] = field(default_factory=dict)
    #: 受け手を問わず書き換えられる属性名と、名前が定数でない `setattr` / `delattr` があるか。
    stored_attrs: set[str] = field(default_factory=set)
    any_setattr: bool = False


#: `globals()` / `vars()` の結果を読むだけの属性（名前空間を書き換えない）。
_READ_ONLY_NS_ATTRS = frozenset({"get", "items", "keys", "values", "copy", "__contains__", "__getitem__"})


def _is_namespace_call(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and (node.func.id == "globals" or (node.func.id == "vars" and not node.args and not node.keywords))
    )


def _namespace_read_only(parent: ast.AST, call: ast.AST) -> bool:
    """`globals()` / `vars()` の呼び出し `call` を、親 `parent` が読むだけに使うか
    （`k in globals()`、`globals()[k]`、`globals().get(k)`）。それ以外（代入先・引数・別名への束縛）は書き換えうる。"""
    if isinstance(parent, ast.Compare):
        return any(c is call for c in parent.comparators) and all(isinstance(o, (ast.In, ast.NotIn)) for o in parent.ops)
    if isinstance(parent, ast.Subscript):
        return parent.value is call and isinstance(parent.ctx, ast.Load)
    if isinstance(parent, ast.Attribute):
        return parent.value is call and parent.attr in _READ_ONLY_NS_ATTRS
    return False


def _note_facts(node: ast.AST, parent: ast.AST, info: _ModInfo) -> None:
    """走査中のノード 1 つ（親は `parent`）から `_ModInfo` の事実を足す（`_scan_module_writes` / `_attr_stores`
    と同じ趣旨）。"""
    if isinstance(node, (ast.Global, ast.Nonlocal)):
        info.declared.update(node.names)
    elif isinstance(node, (ast.Import, ast.ImportFrom)):
        for al in node.names:
            if al.name != "*":
                info.imports.setdefault(al.asname or al.name.split(".")[0], []).append(node)
    elif isinstance(node, ast.Attribute) and isinstance(node.ctx, (ast.Store, ast.Del)):
        info.stored_attrs.add(node.attr)
        if isinstance(node.value, ast.Name):
            info.attr_pairs.add((node.value.id, node.attr))
    elif isinstance(node, ast.Call):
        fid = node.func.id if isinstance(node.func, ast.Name) else None
        if _is_namespace_call(node) and not _namespace_read_only(parent, node):
            info.dynamic = True
        if fid in ("exec", "eval") and len(node.args) + len(node.keywords) < 2:
            info.dynamic = True  # 既定の名前空間（呼び出し位置のグローバル）で実行する
        if _last_name(node) in _SETATTR and len(node.args) >= 2:
            a = node.args[1]
            const = a.value if isinstance(a, ast.Constant) and isinstance(a.value, str) else None
            if const is not None:
                info.stored_attrs.add(const)
            else:
                info.any_setattr = True
            if isinstance(node.args[0], ast.Name):
                info.attr_pairs.add((node.args[0].id, const or "*"))
            elif any(isinstance(m, ast.Attribute) and m.attr == "modules" for m in ast.walk(node.args[0])):
                info.dynamic = True  # `setattr(sys.modules[__name__], name, fn)`


def _arg_nodes(args: ast.arguments) -> list[ast.arg]:
    out = list(args.posonlyargs) + list(args.args) + list(args.kwonlyargs)
    if args.vararg is not None:
        out.append(args.vararg)
    if args.kwarg is not None:
        out.append(args.kwarg)
    return out


def _target_names(t: ast.AST) -> list[ast.Name]:
    return [n for n in ast.walk(t) if isinstance(n, ast.Name) and isinstance(n.ctx, (ast.Store, ast.Del))]


def _scope_bindings(scope: ast.AST, name: str) -> tuple[list[ast.AST], bool]:
    """`scope`（モジュール / クラス本体 / 関数 / lambda / 内包）の中で `name` を束縛するもの。

    入れ子の関数・クラス・lambda の本体は別のスコープなので見ない（その名前と、外側で評価される
    デコレータ・既定値・基底は見る）。内包の中の `:=` は外側を束縛するので数える。**取りこぼすと
    外側のスコープの別の定義に解いてしまう**（偽のユニット）ので、疑わしいものは束縛として数える。

    :returns: `(束縛するノードの列, global / nonlocal / import * で動的に決まるか)`
    """
    binds: list[ast.AST] = []
    dynamic = False
    if isinstance(scope, _COMP_NODES):
        for gen in scope.generators:
            binds += [n for n in _target_names(gen.target) if n.id == name]
        return binds, False
    stack: list[ast.AST] = []
    if isinstance(scope, (*_FUNC_NODES, ast.Lambda)):
        binds += [a for a in _arg_nodes(scope.args) if a.arg == name]
        body = scope.body if isinstance(scope.body, list) else [scope.body]
        stack += list(body)
    else:
        stack += list(getattr(scope, "body", []))
    while stack:
        node = stack.pop()
        if isinstance(node, (*_FUNC_NODES, ast.ClassDef)):
            if node.name == name:
                binds.append(node)
            stack += list(node.decorator_list)
            if isinstance(node, ast.ClassDef):
                stack += list(node.bases) + [k.value for k in node.keywords]
            else:
                stack += [d for d in node.args.defaults] + [d for d in node.args.kw_defaults if d is not None]
            continue
        if isinstance(node, ast.Lambda):
            stack += [d for d in node.args.defaults] + [d for d in node.args.kw_defaults if d is not None]
            continue
        if isinstance(node, _COMP_NODES):
            binds += [
                n
                for n in ast.walk(node)
                if isinstance(n, ast.NamedExpr) and isinstance(n.target, ast.Name) and n.target.id == name
            ]
            continue
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for a in node.names:
                if a.name == "*":
                    dynamic = True
                elif (a.asname or a.name.split(".")[0]) == name:
                    binds.append(node)
            continue
        if isinstance(node, (ast.Global, ast.Nonlocal)):
            if name in node.names:
                dynamic = True
            continue
        if isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Store, ast.Del)) and node.id == name:
            binds.append(node)
        elif isinstance(node, ast.ExceptHandler) and node.name == name:
            binds.append(node)
        elif isinstance(node, ast.alias):
            continue
        elif type(node).__name__ in ("MatchAs", "MatchStar") and getattr(node, "name", None) == name:
            binds.append(node)
        elif type(node).__name__ == "MatchMapping" and getattr(node, "rest", None) == name:
            binds.append(node)
        stack += list(ast.iter_child_nodes(node))
    return binds, dynamic


def _qual_prefix(chain: tuple[ast.AST, ...]) -> str:
    """スコープの列（外 → 内）の中で定義される関数の qualname の接頭辞（`SourceIndex._index_body` と同じ）。"""
    parts = [n.name for n in chain if isinstance(n, (*_FUNC_NODES, ast.ClassDef))]
    return "".join(p + "." for p in parts)


def _last_name(node: ast.AST) -> Optional[str]:
    d = dotted_of(node.func if isinstance(node, ast.Call) else node)
    return d.split(".")[-1] if d else None


class _Resolver:
    """登録文のスコープから、関数・クラス・モジュールへの参照を厳密に解く（D64 / U40）。"""

    def __init__(self, index: SourceIndex) -> None:
        self.index = index
        self._modules: Optional[frozenset[str]] = None
        #: パス → そのファイルの事実。`add_file` で走査しながら埋める（**全ファイルを入れてから解決する**）。
        self._by_path: dict[str, _ModInfo] = {}
        self._info: dict[str, Optional[_ModInfo]] = {}
        self._attr_writes: Optional[frozenset[tuple[str, str]]] = None
        self._mbinds: dict[tuple[str, str], tuple[list[ast.AST], bool]] = {}
        self._stored_attrs: Optional[tuple[frozenset[str], bool]] = None

    def add_file(self, path: str, tree: ast.Module) -> _ModInfo:
        info = _ModInfo(path, tree, os.path.basename(path) == "__init__.py")
        self._by_path[os.path.abspath(path)] = info
        return info

    # -- モジュール --------------------------------------------------------

    def module_bindings(self, module: str, name: str) -> tuple[list[ast.AST], bool]:
        key = (module, name)
        if key not in self._mbinds:
            info = self.info(module)
            self._mbinds[key] = _scope_bindings(info.tree, name) if info is not None else ([], False)
        return self._mbinds[key]

    def stored_attrs(self) -> tuple[frozenset[str], bool]:
        """木のどこかで `x.NAME = ...` / `del x.NAME` / `setattr(x, "NAME", v)` と書き換えられる属性名と、
        名前が定数でない `setattr` / `delattr` があるか。"""
        if self._stored_attrs is None:
            names: set[str] = set()
            any_name = False
            for info in self._by_path.values():
                names |= info.stored_attrs
                any_name = any_name or info.any_setattr
            self._stored_attrs = (frozenset(names), any_name)
        return self._stored_attrs

    def modules(self) -> frozenset[str]:
        if self._modules is None:
            self._modules = frozenset(self.index.module_name(p) for p in self.index.py_files())
        return self._modules

    def abs_module(self, dotted: Optional[str]) -> tuple[str, Optional[str]]:
        """絶対 import の dotted 名を木内モジュールへ。`("tree", 名)` / `("extern", None)` / `("ambiguous", None)`。

        完全一致を先に採り、なければ `.<dotted>` で終わる木内モジュールが**ちょうど 1 つ**のときだけ採る
        （src レイアウト）。2 つ以上なら決めない（`resolve_module_path` の setdefault のように最初の 1 つを
        採ると、別のパッケージの同名モジュールに解く）。
        """
        if not dotted:
            return "ambiguous", None
        mods = self.modules()
        if dotted in mods:
            return "tree", dotted
        hits = [m for m in mods if m.endswith("." + dotted)]
        if len(hits) == 1:
            return "tree", hits[0]
        return ("ambiguous", None) if hits else ("extern", None)

    def info(self, module: str) -> Optional[_ModInfo]:
        if module in self._info:
            return self._info[module]
        out: Optional[_ModInfo] = None
        if module in self.modules():
            path = self.index.resolve_module_path(module)
            if path is not None and self.index.module_name(path) == module:
                out = self._by_path.get(os.path.abspath(path))
        self._info[module] = out
        return out

    def attr_writes(self) -> frozenset[tuple[str, str]]:
        """木のどこかで**モジュール属性として**書き換えられる `(module, NAME)`（`NAME` が `"*"` なら全部）。

        `mod.NAME = ...` / `del mod.NAME` / `setattr(mod, "NAME", v)`。`mod` はそのファイルの import
        （モジュール直下でも関数の中でも）で木内モジュールに解けるもの。
        """
        if self._attr_writes is None:
            # 集める間は書き換えの確認を外して import をたどる（再帰を止める）。集めた後の解決では確認する。
            self._attr_writes = frozenset()
            out: set[tuple[str, str]] = set()
            for path in sorted(self._by_path):
                info = self._by_path[path]
                mod = self.index.module_name(path)
                for alias, attr in sorted(info.attr_pairs):
                    for imp in info.imports.get(alias, ()):
                        ref = self._from_import(mod, imp, alias, _IMPORT_HOPS)
                        if ref is not None and ref.kind == "module":
                            out.add((ref.name, attr))
            self._attr_writes = frozenset(out)
        return self._attr_writes

    def in_module(self, module: str, name: str, hops: int = _IMPORT_HOPS) -> Optional[_Ref]:
        """モジュール水準の `name`。束縛が**ちょうど 1 つ**で、動的に書き換えられないときだけ解く。"""
        info = self.info(module)
        if info is None or hops < 0:
            return None
        if info.dynamic or name in info.declared:
            return None
        binds, dynamic = self.module_bindings(module, name)
        if dynamic or len(binds) != 1:
            return None
        writes = self.attr_writes()
        if (module, name) in writes or (module, "*") in writes:
            return None
        return self._from_binding(module, binds[0], name, (info.tree,), hops)

    def _from_binding(
        self, module: str, b: ast.AST, name: str, chain: tuple[ast.AST, ...], hops: int
    ) -> Optional[_Ref]:
        """唯一の束縛 `b` から参照を作る。`chain` は `b` を持つスコープまでの列（外 → 内）。"""
        if isinstance(b, _FUNC_NODES):
            qual = _qual_prefix(chain) + name
            fds = [
                f
                for f in self.index.lookup_function(qual, module)
                if f.module == module and f.qualname == qual and f.node is b
            ]
            return _Ref("func", qual, fds[0]) if len(fds) == 1 else None
        if isinstance(b, ast.ClassDef):
            return _Ref("class", f"{module}.{_qual_prefix(chain)}{name}")
        if isinstance(b, (ast.Import, ast.ImportFrom)):
            return self._from_import(module, b, name, hops)
        return None

    def _from_import(self, module: str, node: ast.AST, local: str, hops: int) -> Optional[_Ref]:
        aliases = [a for a in node.names if a.name != "*" and (a.asname or a.name.split(".")[0]) == local]
        if len(aliases) != 1:
            return None
        alias = aliases[0]
        if isinstance(node, ast.Import):
            dotted = alias.name if alias.asname else alias.name.split(".")[0]
            status, mod = self.abs_module(dotted)
            if status == "tree":
                return _Ref("module", mod)
            return _Ref("extern", dotted) if status == "extern" else None
        assert isinstance(node, ast.ImportFrom)
        if node.level > 0:
            # **相対 import は `level` で解く**（import 表は相対の点を捨てるので使わない。D61 の改訂 G3）。
            # 基準は `__init__.py` ならパッケージ自身、ほかは親パッケージ。
            info = self.info(module)
            if info is None:
                return None
            base = module if info.is_pkg else module.rpartition(".")[0]
            for _ in range(node.level - 1):
                base = base.rpartition(".")[0]
            if not base:
                return None
            target = f"{base}.{node.module}" if node.module else base
            if node.module and target not in self.modules():
                return None  # 相対 import が木の中で解けない（木外ではありえない）
        else:
            status, target = self.abs_module(node.module)
            if status == "extern":
                return _Ref("extern", f"{node.module}.{alias.name}")
            if status != "tree" or target is None:
                return None
        return self.member(target, alias.name, hops - 1)

    def member(self, module: str, attr: str, hops: int) -> Optional[_Ref]:
        """木内モジュール（パッケージ）`module` の属性 `attr`。

        パッケージの本体が `attr` を束縛し、かつ同名のサブモジュールもあるときは決めない（import の順で
        どちらにもなる）。
        """
        sub = f"{module}.{attr}"
        sub_exists = sub in self.modules()
        info = self.info(module)
        bound = bool(info is not None and self.module_bindings(module, attr)[0])
        if sub_exists and bound:
            return None
        if sub_exists:
            return _Ref("module", sub)
        if bound:
            return self.in_module(module, attr, hops)
        return None

    # -- 登録文のスコープ ----------------------------------------------------

    def _binding_scope(
        self, module: str, chain: tuple[ast.AST, ...], name: str
    ) -> tuple[str, Optional[int], list[ast.AST]]:
        """`name` を束縛する最も内側のスコープ。

        :returns: `("local", chain の位置, 束縛)` / `("module", None, [])` / `("dynamic", None, [])`。
            クラス本体は、参照がその本体に直接あるときだけ見える（Python のスコープ規則）。
        """
        info = self.info(module)
        if info is None or name in info.declared:
            return "dynamic", None, []
        for i in range(len(chain) - 1, 0, -1):
            scope = chain[i]
            if isinstance(scope, ast.ClassDef) and i != len(chain) - 1:
                continue
            binds, dynamic = _scope_bindings(scope, name)
            if dynamic:
                return "dynamic", None, []
            if binds:
                return "local", i, binds
        return "module", None, []

    def name(self, module: str, chain: tuple[ast.AST, ...], name: str) -> Optional[_Ref]:
        where, i, binds = self._binding_scope(module, chain, name)
        if where == "dynamic":
            return None
        if where == "module":
            return self.in_module(module, name)
        if len(binds) != 1 or i is None:
            return None
        return self._from_binding(module, binds[0], name, chain[: i + 1], _IMPORT_HOPS)

    def expr(self, module: str, chain: tuple[ast.AST, ...], node: ast.AST) -> Optional[_Ref]:
        """式 `node`（Name / Attribute の連鎖 / `self.<m>`）が指すもの。それ以外の式は解かない。"""
        if isinstance(node, ast.Name):
            return self.name(module, chain, node.id)
        if not isinstance(node, ast.Attribute):
            return None
        if isinstance(node.value, ast.Name):
            handled, ref = self._self_method(module, chain, node.value.id, node.attr)
            if handled:
                return ref
        base = self.expr(module, chain, node.value)
        if base is None:
            return None
        if base.kind == "module":
            return self.member(base.name, node.attr, _IMPORT_HOPS)
        if base.kind == "extern":
            return _Ref("extern", f"{base.name}.{node.attr}")
        return None

    def _self_method(
        self, module: str, chain: tuple[ast.AST, ...], head: str, attr: str
    ) -> tuple[bool, Optional[_Ref]]:
        """`self.<attr>` を**囲むクラスの中だけ**で解く（D64 / U40 条件 (2)）。

        `head` が、クラス本体に直接ある（staticmethod / classmethod でない）メソッドの第 1 仮引数で、
        そのメソッドの中で束縛し直されないときだけ扱う。クラス本体で `attr` を束縛するのがちょうど 1 つの
        def で、インスタンス属性・クラス属性として書き換えられず、木内のサブクラスが上書きしないときだけ採る。
        別クラスの同名メソッドや木外の基底から来るメソッドは採らない。

        :returns: `(self 形として扱ったか, 参照)`。扱わないなら一般の解決に回す。
        """
        where, i, binds = self._binding_scope(module, chain, head)
        if where != "local" or i is None:
            return False, None
        meth = chain[i]
        if not isinstance(meth, _FUNC_NODES) or i < 1 or not isinstance(chain[i - 1], ast.ClassDef):
            return False, None
        positional = list(meth.args.posonlyargs) + list(meth.args.args)
        if not positional or positional[0].arg != head:
            return False, None
        if len(binds) != 1 or binds[0] is not positional[0]:
            return True, None  # self を束縛し直している
        if any(_last_name(d) in ("staticmethod", "classmethod") for d in meth.decorator_list):
            return True, None
        cls = chain[i - 1]
        cbinds, cdyn = _scope_bindings(cls, attr)
        if cdyn or len(cbinds) != 1 or not isinstance(cbinds[0], _FUNC_NODES):
            return True, None
        target = cbinds[0]
        if any(_last_name(d) in _NON_FUNCTION_DECORATORS for d in target.decorator_list):
            return True, None
        # インスタンス属性・クラス属性としての書き換え（`self.m = ...` / `C.m = ...` / `setattr(x, "m", v)`）。
        # 受け手の型は見ず、木のどこかで同じ名前の属性が書き換えられるなら採らない。
        stored, any_setattr = self.stored_attrs()
        if attr in stored or any_setattr:
            return True, None
        # 木内のサブクラス（何段下でも）か、その MRO で `cls` より前に来うるミックスインが同名で上書きする
        # （`self.m` は動的に束縛される）。
        if self._overridden_below(cls.name, attr):
            return True, None
        ref = self._from_binding(module, target, attr, chain[:i], _IMPORT_HOPS)
        return True, ref

    def _overridden_below(self, cls_name: str, attr: str) -> bool:
        """`cls_name` の木内のサブクラス（推移的）と、それらから `cls_name` を通らずにたどれる基底のどれかが
        `attr` を束縛するか。クラスは基底の末尾名で結ぶ（同名のクラスが複数あれば全部を見る。見過ぎる側）。"""
        classes = list(self.index.classes())

        def bases_of(cd) -> set[str]:
            return {b.split(".")[-1] for b in cd.bases}

        subs: set[str] = set()
        frontier = [cls_name]
        while frontier:
            cur = frontier.pop()
            for cd in classes:
                if cur in bases_of(cd) and cd.name != cls_name and cd.name not in subs:
                    subs.add(cd.name)
                    frontier.append(cd.name)
        if not subs:
            return False
        check = set(subs)
        frontier = list(subs)
        while frontier:
            cur = frontier.pop()
            for cd in classes:
                if cd.name != cur:
                    continue
                for b in bases_of(cd):
                    if b != cls_name and b not in check:
                        check.add(b)
                        frontier.append(b)
        return any(cd.name in check and _scope_bindings(cd.node, attr)[0] for cd in classes)


def _walk_scoped(tree: ast.Module):
    """`(node, 親, スコープの列（外 → 内、先頭はモジュール）)` を再帰せずに列挙する。

    デコレータ・既定値・基底・注釈は外側のスコープで評価されるので、外側の列で出す。
    """
    top: tuple[ast.AST, ...] = (tree,)
    stack: list[tuple[ast.AST, ast.AST, tuple[ast.AST, ...]]] = [(c, tree, top) for c in reversed(tree.body)]
    while stack:
        node, parent, outer = stack.pop()
        yield node, parent, outer
        if isinstance(node, (*_FUNC_NODES, ast.Lambda)):
            inner = outer + (node,)
            body = node.body if isinstance(node.body, list) else [node.body]
            stack += [(c, node, inner) for c in reversed(body)]
            if not isinstance(node, ast.Lambda):
                stack += [(d, node, outer) for d in node.decorator_list]
                if node.returns is not None:
                    stack.append((node.returns, node, outer))
            stack += [(c, node, outer) for c in ast.iter_child_nodes(node.args)]
        elif isinstance(node, ast.ClassDef):
            inner = outer + (node,)
            stack += [(c, node, inner) for c in reversed(node.body)]
            stack += [(c, node, outer) for c in node.decorator_list + node.bases + [k.value for k in node.keywords]]
        elif isinstance(node, _COMP_NODES):
            inner = outer + (node,)
            stack += [(c, node, inner) for c in ast.iter_child_nodes(node)]
        else:
            stack += [(c, node, outer) for c in ast.iter_child_nodes(node)]


def _registration_of(call: ast.Call) -> Optional[tuple[EntryRule, ast.Call, ast.AST]]:
    """呼び出し形の登録なら `(規則, 宣言を読む呼び出し, 登録される式)`。

    * `d(...)(fn)`: `@d(...) def fn` の糖衣を外した形（PEP 318）。宣言は内側の `d(...)` から読む。
      `require_positional` の規則は同じ構造条件で見る（`click.command()(main)` は落ちる）。
    * `d(fn, ...)`: `@d def fn` の糖衣を外した形と `add_tool(fn, annotations=...)`。宣言はこの呼び出しから読む。
      `require_positional` の規則は裸のデコレータ形と同じく採らない。
    """
    if not call.args:
        return None
    f = call.func
    if isinstance(f, ast.Call):
        name = dotted_of(f.func)
        rule = _match_decorator(name) if name else None
        if rule is not None and (not rule.require_positional or _has_catalog_signature(f, rule)):
            return rule, f, call.args[0]
        return None
    name = dotted_of(f)
    rule = _match_decorator(name) if name else None
    if rule is not None and not rule.require_positional:
        return rule, call, call.args[0]
    return None


def _spec_origin(ref: Optional[_Ref], origins: tuple[str, ...]) -> bool:
    """構築子の参照が `SPEC_OBJECT_ORIGINS` の import 元に当たるか。木内の定義は `.<元>` で終わるものも採る。"""
    if ref is None:
        return False
    if ref.kind == "extern":
        return ref.name in origins
    if ref.kind == "class":
        return any(ref.name == o or ref.name.endswith("." + o) for o in origins)
    return False


def find_registration_units(
    index: SourceIndex, registered: set[tuple[str, str]] | frozenset[tuple[str, str]] = frozenset()
) -> list[Unit]:
    """呼び出し形の登録（`x.tool(...)(fn)` / `x.tool(fn)` / `x.add_tool(fn, ...)`）と `spec_object`
    （`ToolSpec(name=..., execute=fn)`）の `fn` を入口にする（D64 / U40）。

    **`fn` は登録文のスコープで厳密に解く**（`_Resolver`）。`registered` にある関数（すでに別の形で
    ユニットになったもの）と、この中で先に登録された関数は 2 つ目のユニットにしない。
    """
    resolver = _Resolver(index)
    seen: set[tuple[str, str]] = set(registered)
    out: list[Unit] = []
    spec_rules: list[tuple[EntryRule, tuple[str, ...], str]] = []
    for fw, (origins, kwarg) in sorted(SPEC_OBJECT_ORIGINS.items()):
        rule = find_entry_rule("spec_object", origins[0].split(".")[-1])
        if rule is not None and rule.framework == fw:
            spec_rules.append((rule, origins, kwarg))
    spec_kwargs = {kwarg for _r, _o, kwarg in spec_rules}
    # 1 回目の走査: 候補の呼び出しと、名前の解決に要るモジュールの事実を**全ファイルについて**集める
    # （あるファイルの解決は、別のファイルの書き換え・再公開を見る）。
    files: list[tuple[str, str, list[tuple[ast.Call, tuple[ast.AST, ...]]]]] = []
    for path in index.py_files():
        tree = index.parse(path)
        if tree is None:
            continue
        info = resolver.add_file(path, tree)
        cands: list[tuple[ast.Call, tuple[ast.AST, ...]]] = []
        for node, parent, chain in _walk_scoped(tree):
            _note_facts(node, parent, info)
            if isinstance(node, ast.Call) and (
                _registration_of(node) is not None or any(k.arg in spec_kwargs for k in node.keywords)
            ):
                cands.append((node, chain))
        if cands:
            files.append((index.module_name(path), index.relpath(path), cands))
    # 2 回目: 候補を解く。
    for module, rel, cands in files:
        found: list[tuple[int, int, Unit]] = []
        for node, chain in cands:
            reg = _registration_of(node)
            if reg is not None:
                rule, decl_call, target = reg
                ref = resolver.expr(module, chain, target)
                if ref is not None and ref.kind == "func" and ref.fd is not None:
                    where = {"form": "call", "relpath": rel, "lineno": getattr(node, "lineno", 0)}
                    found.append((node.lineno, node.col_offset, _decorator_unit(ref.fd, rule, decl_call, where)))
                continue
            for rule, origins, kwarg in spec_rules:
                value = _kwarg_node(node, kwarg)
                if value is None:
                    continue
                if not _spec_origin(resolver.expr(module, chain, node.func), origins):
                    continue
                ref = resolver.expr(module, chain, value)
                if ref is None or ref.kind != "func" or ref.fd is None:
                    continue  # `execute=create_mcp_execute_function(...)` などの呼び出し式は採らない
                fd = ref.fd
                found.append(
                    (
                        node.lineno,
                        node.col_offset,
                        Unit(
                            framework=rule.framework,
                            entry_kind="spec_object",
                            module=fd.module,
                            qualname=fd.qualname,
                            relpath=fd.relpath,
                            node=fd.node,
                            # **仮引数は全部 MODEL**（`confirm` も。R2 例外の語彙は月 3 凍結で、足していない）。
                            params=params_of(fd.node, rule.exclude_params),
                            tool_name=_kwarg_str(node, "name")
                            or _positional_str(node, 0)
                            or fd.qualname.split(".")[-1],
                            is_async=fd.is_async,
                            registration={"form": "spec_object", "relpath": rel, "lineno": node.lineno},
                        ),
                    )
                )
                break
        found.sort(key=lambda t: (t[0], t[1]))
        for _l, _c, unit in found:
            key = (unit.module, unit.qualname)
            if key in seen:
                continue  # 二重登録（デコレータ形 + 呼び出し形、呼び出し形 2 回）は 1 ユニット
            seen.add(key)
            out.append(unit)
    return out


# --------------------------------------------------------------------------
# `tools=[...]` 形（フレームワーク横断）
# --------------------------------------------------------------------------


def find_tools_list_units(
    index: SourceIndex,
    already: frozenset[str] | set[str] = frozenset(),
    registered: frozenset[tuple[str, str]] | set[tuple[str, str]] = frozenset(),
) -> list[Unit]:
    """`Agent(tools=[f, g])` / `tools = [f, g]` の要素を入口にする。

    **木内のユーザ定義関数に一意に解決できる要素だけを採る。** 名前だけで
    拾うと同名の無関係な関数まで入口になり、母集団が膨らむ。
    """
    #: 名前 → それを参照しているファイル（同名が複数あるときの絞り込みに使う）。
    names: dict[str, set[str]] = {}
    for path in index.py_files():
        tree = index.parse(path)
        if tree is None:
            continue
        rel = index.relpath(path)
        for node in ast.walk(tree):
            elts: list = []
            if isinstance(node, ast.Call):
                for kw in node.keywords:
                    if kw.arg == "tools" and isinstance(kw.value, (ast.List, ast.Tuple)):
                        elts += list(kw.value.elts)
            elif isinstance(node, ast.Assign) and isinstance(node.value, (ast.List, ast.Tuple)):
                for t in node.targets:
                    if isinstance(t, ast.Name) and t.id in ("tools", "TOOLS", "AGENT_TOOLS"):
                        elts += list(node.value.elts)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # `def get_ast_grep_tools(): return [f, g, h]` 形。
                if node.name.endswith("_tools") or node.name.endswith("_toolset"):
                    for sub in ast.walk(node):
                        if isinstance(sub, ast.Return) and isinstance(
                            sub.value, (ast.List, ast.Tuple)
                        ):
                            elts += list(sub.value.elts)
            for e in elts:
                n = dotted_of(e)
                if n:
                    names.setdefault(n.split(".")[-1], set()).add(rel)
                elif isinstance(e, ast.Constant) and isinstance(e.value, str):
                    # `tools=["ast_grep_search", "ast_grep_rewrite"]` の文字列形。
                    names.setdefault(e.value, set()).add(rel)

    out: list[Unit] = []
    seen: set[str] = set()
    for name in sorted(names):
        if name in already:
            continue
        # **入れ子関数も採る**（qualname は `外側.内側` なので完全一致では落ちる。D17）。
        # メソッドは採らない（従来どおり）。
        fds = [
            f
            for f in index.lookup_function(name)
            if f.qualname.split(".")[-1] == name and f.classname is None
        ]
        if len(fds) > 1:
            # 同名が複数あれば、その名前を tools に並べているファイルの定義に絞る。
            fds = [f for f in fds if f.relpath in names[name]]
        if len(fds) != 1:
            continue  # 一意に解決できないものは採らない
        fd = fds[0]
        if (fd.module, fd.qualname) in registered:
            # **ほかの規則ですでにユニットになった関数を 2 つ目のユニットにしない**（D17 改訂 4）。
            # `@mcp.tool()` で登録した入れ子関数の名前をログの `tools=[...]` に並べる形で、同じ関数が
            # mcp と tools-list の 2 ユニットに数えられていた（ユニット数と危険効果ユニット数の過大計上）。
            continue
        if fd.key in seen:
            continue
        seen.add(fd.key)
        out.append(
            Unit(
                framework="tools-list",
                entry_kind="tools_list",
                module=fd.module,
                qualname=fd.qualname,
                relpath=fd.relpath,
                node=fd.node,
                params=params_of(fd.node),
                tool_name=name,
                is_async=fd.is_async,
            )
        )
    return out


# --------------------------------------------------------------------------
# langroid の `ToolMessage` 派生 + 同名ハンドラ
# --------------------------------------------------------------------------


def find_toolmessage_units(index: SourceIndex) -> list[Unit]:
    """`ToolMessage` 派生クラスの `request` 値と同名のメソッドを入口にする。

    **MODEL 値はメソッドの仮引数ではなくクラスのフィールドである。**
    `def run_query(self, msg: RunQueryTool)` の `msg` は 1 つの引数だが、
    モデルが決めるのは `RunQueryTool.query` などのフィールドなので、
    仮引数だけを見ると MODEL 値が 1 つも見つからない。
    """
    out: list[Unit] = []
    messages: dict[str, tuple[str, tuple[tuple[str, Optional[str]], ...]]] = {}
    for cd in index.classes():
        bases = {b.split(".")[-1] for b in cd.bases}
        if "ToolMessage" not in bases:
            continue
        request = None
        fields: list[tuple[str, Optional[str]]] = []
        for node in cd.node.body:
            if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                name = node.target.id
                ann = _annotation_str(node.annotation)
                if name == "request" and isinstance(node.value, ast.Constant):
                    if isinstance(node.value.value, str):
                        request = node.value.value
                    continue
                if name in TOOLMESSAGE_META_FIELDS or name.startswith("_"):
                    continue
                fields.append((name, ann))
        if request:
            messages[request] = (cd.name, tuple(fields))

    if not messages:
        return out
    for fd in index.functions():
        method = fd.qualname.split(".")[-1]
        if fd.classname is None or method not in messages:
            continue
        cls, fields = messages[method]
        params = params_of(fd.node)
        msg_param = None
        for p in params:
            if p.annotation and p.annotation.split(".")[-1] == cls:
                msg_param = p.name
                break
        if msg_param is None and params:
            msg_param = params[0].name
        if msg_param is None:
            continue
        out.append(
            Unit(
                framework="langroid",
                entry_kind="toolmessage_handler",
                module=fd.module,
                qualname=fd.qualname,
                relpath=fd.relpath,
                node=fd.node,
                params=[p for p in params if p.name != msg_param],
                tool_name=method,
                is_async=fd.is_async,
                message_param=msg_param,
                message_fields=fields,
                message_class=cls,
            )
        )
    return out


# --------------------------------------------------------------------------
# 低レベル MCP の 2 形（Def 2 が名指しで要求する）
# --------------------------------------------------------------------------


def find_lowlevel_units(index: SourceIndex) -> list[Unit]:  # noqa: C901
    """`@server.call_tool()` デコレータ形（v1）と `Server(on_call_tool=...)` 形（v2）。

    低レベル経路ではハンドラが 1 つで、その中の `name` 分岐が DISPATCH になる。
    ハンドラ本体を 1 ユニットとし、分岐から得た候補名を `dispatch_names` に持つ。
    """
    out: list[Unit] = []
    seen: set[str] = set()
    enums = enum_string_members(index)

    for fd in index.functions():
        for name, _call, _node in _decorator_calls(fd.node):
            last = name.split(".")[-1]
            if last != "call_tool":
                continue
            key = f"{fd.module}:{fd.qualname}"
            if key in seen:
                continue
            seen.add(key)
            out.append(
                Unit(
                    framework="mcp-lowlevel-v1",
                    entry_kind="lowlevel_v1",
                    module=fd.module,
                    qualname=fd.qualname,
                    relpath=fd.relpath,
                    node=fd.node,
                    params=params_of(fd.node),
                    tool_name=None,
                    dispatch_names=dispatch_name_candidates(fd.node, enums),
                    is_async=fd.is_async,
                )
            )

    # v2: `Server(on_call_tool=handler)` / `add_request_handler("tools/call", handler)`
    for path in index.py_files():
        tree = index.parse(path)
        if tree is None:
            continue
        scope = index.module_scope(path)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            handler: Optional[ast.AST] = None
            fname = dotted_of(node.func) or ""
            if fname.split(".")[-1] == "Server":
                for kw in node.keywords:
                    if kw.arg in LOWLEVEL_V2_KWARGS:
                        handler = kw.value
            elif fname.split(".")[-1] == "add_request_handler":
                if node.args and isinstance(node.args[0], ast.Constant):
                    if node.args[0].value == LOWLEVEL_V2_REQUEST and len(node.args) > 1:
                        handler = node.args[1]
            if handler is None:
                continue
            hname = dotted_of(handler)
            if hname is None:
                continue
            for fd in index.lookup_function(hname.split(".")[-1]):
                key = f"{fd.module}:{fd.qualname}"
                if key in seen:
                    continue
                seen.add(key)
                out.append(
                    Unit(
                        framework="mcp-lowlevel-v2",
                        entry_kind="lowlevel_v2",
                        module=fd.module,
                        qualname=fd.qualname,
                        relpath=fd.relpath,
                        node=fd.node,
                        params=params_of(fd.node),
                        tool_name=None,
                        dispatch_names=dispatch_name_candidates(fd.node, enums),
                        is_async=fd.is_async,
                    )
                )
        del scope
    return out


def enum_string_members(index: SourceIndex) -> dict[str, str]:
    """`class GitTools(str, Enum): STATUS = "git_status"` を `GitTools.STATUS` →
    `"git_status"` の表にする。

    低レベルハンドラの `match name: case GitTools.STATUS:` から候補名を読むために
    要る。**読めない形は表に入れない**（推定で名前を作らない）。
    """
    out: dict[str, str] = {}
    for cd in index.classes():
        if not any("Enum" in b or "str" in b for b in cd.bases):
            continue
        for node in cd.node.body:
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant):
                if not isinstance(node.value.value, str):
                    continue
                for t in node.targets:
                    if isinstance(t, ast.Name):
                        out[f"{cd.name}.{t.id}"] = node.value.value
                        out[t.id] = node.value.value
    return out


def dispatch_name_candidates(fn: ast.AST, enums: Optional[dict[str, str]] = None) -> tuple[str, ...]:
    """低レベルハンドラ内の `name` 分岐から候補名を集める。

    `if name == "x"` / `elif name in (...)` / `match name: case "x"` /
    定数辞書リテラルの添字、の 4 形だけを読む。**読めない形は候補にしない**
    （`OPAQUE(dynamic_registry)` の側で扱う）。
    """
    names: set[str] = set()
    for node in ast.walk(fn):
        if isinstance(node, ast.Compare):
            for op, comp in zip(node.ops, node.comparators, strict=False):
                if isinstance(op, ast.Eq) and isinstance(comp, ast.Constant) and isinstance(comp.value, str):
                    names.add(comp.value)
                elif isinstance(op, ast.In) and isinstance(comp, (ast.Tuple, ast.List, ast.Set)):
                    for e in comp.elts:
                        if isinstance(e, ast.Constant) and isinstance(e.value, str):
                            names.add(e.value)
        elif isinstance(node, ast.Dict):
            for k in node.keys:
                if isinstance(k, ast.Constant) and isinstance(k.value, str):
                    names.add(k.value)
        elif _MATCH_CASE is not None and isinstance(node, _MATCH_CASE):
            for pat in _flatten_patterns(node.pattern):
                if not isinstance(pat, ast.MatchValue):
                    continue
                v = pat.value
                if isinstance(v, ast.Constant) and isinstance(v.value, str):
                    names.add(v.value)
                elif enums is not None:
                    dotted = dotted_of(v)
                    if dotted and dotted in enums:
                        names.add(enums[dotted])
    return tuple(sorted(names))


def _flatten_patterns(pattern: ast.AST) -> list[ast.AST]:
    mo = getattr(ast, "MatchOr", None)
    if mo is not None and isinstance(pattern, mo):
        out: list[ast.AST] = []
        for p in pattern.patterns:
            out += _flatten_patterns(p)
        return out
    return [pattern]


# --------------------------------------------------------------------------
# MCP annotations の join（D_kind の源。Def 6）
# --------------------------------------------------------------------------

#: 仕様の camelCase 表記のみ。snake_case は `D_malformed` として別行で報告する。
ANNOTATION_FIELDS = ("title", "readOnlyHint", "destructiveHint", "idempotentHint", "openWorldHint")
SNAKE_ALIASES = {
    "read_only_hint": "readOnlyHint",
    "destructive_hint": "destructiveHint",
    "idempotent_hint": "idempotentHint",
    "open_world_hint": "openWorldHint",
}


@dataclass
class ToolLiteral:
    """`Tool(...)` / `types.Tool(...)` リテラル 1 つ。"""

    name: Optional[str]
    annotations: Optional[dict]
    #: 読み取った形（`ToolAnnotations` / `dict` / `unpack` / `unreadable`）。
    form: str
    malformed_fields: tuple[str, ...] = ()
    relpath: str = ""
    lineno: int = 0


def find_tool_literals(index: SourceIndex) -> list[ToolLiteral]:
    """パッケージ内の全 `Tool(...)` / `types.Tool(...)` リテラルを集める。

    パーサは `annotations=ToolAnnotations(...)` / `ToolAnnotations(**{...})` /
    辞書リテラル `{...}` の 3 形を扱う（前測でエントリ基準 1125 件中 727 件 =
    64.6% が後 2 形だった）。**読めない形は `D_unknown` とし `⊥` と混ぜない。**
    """
    out: list[ToolLiteral] = []
    for path in index.py_files():
        tree = index.parse(path)
        if tree is None:
            continue
        rel = index.relpath(path)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            fname = dotted_of(node.func) or ""
            if fname.split(".")[-1] != "Tool":
                continue
            name = _kwarg_str(node, "name")
            ann_node = None
            for kw in node.keywords:
                if kw.arg == "annotations":
                    ann_node = kw.value
            ann, form, malformed = _read_annotations(ann_node)
            out.append(ToolLiteral(name, ann, form, malformed, rel, getattr(node, "lineno", 0)))
    out.sort(key=lambda t: (t.relpath, t.lineno))
    return out


def _read_annotations(node: Optional[ast.AST]) -> tuple[Optional[dict], str, tuple[str, ...]]:
    if node is None:
        return None, "absent", ()
    if isinstance(node, ast.Constant) and node.value is None:
        # **`annotations=None` は読める明示の「無い」**であり `⊥`。読めない形
        # （`D_unknown`）ではない。unreadable にすると同名ツールの `D_unknown` を
        # 過大に数える（野外 run 1 で 5 件）。
        return None, "absent", ()
    malformed: list[str] = []
    values: dict[str, Any] = {}

    def take(key: Optional[str], value_node: ast.AST) -> None:
        if key is None:
            return
        if key in SNAKE_ALIASES:
            malformed.append(key)
            return
        if key not in ANNOTATION_FIELDS:
            return  # 仕様外のフィールド（`category` 等）は D ではない
        try:
            values[key] = ast.literal_eval(value_node)
        except (ValueError, TypeError, SyntaxError):
            pass

    if isinstance(node, ast.Call):
        fname = dotted_of(node.func) or ""
        if fname.split(".")[-1] != "ToolAnnotations":
            return None, "unreadable", ()
        form = "ToolAnnotations"
        for kw in node.keywords:
            if kw.arg is None:  # ToolAnnotations(**{...})
                form = "unpack"
                if isinstance(kw.value, ast.Dict):
                    for k, v in zip(kw.value.keys, kw.value.values, strict=False):
                        if isinstance(k, ast.Constant) and isinstance(k.value, str):
                            take(k.value, v)
                else:
                    return None, "unreadable", ()
            else:
                take(kw.arg, kw.value)
        return values, form, tuple(sorted(set(malformed)))
    if isinstance(node, ast.Dict):
        for k, v in zip(node.keys, node.values, strict=False):
            if isinstance(k, ast.Constant) and isinstance(k.value, str):
                take(k.value, v)
        return values, "dict", tuple(sorted(set(malformed)))
    return None, "unreadable", ()


def join_annotations(units: list[Unit], literals: list[ToolLiteral]) -> tuple[int, int]:
    """`Tool(...)` リテラルとユニットを**ツール名文字列の完全一致**で join する。

    join できない行は「未 join 行」として報告し D にも CONTRADICTION にも
    寄与させない（Def 6）。

    :returns: `(join できた数, 未 join のリテラル数)`
    """
    by_name: dict[str, ToolLiteral] = {}
    for lit in literals:
        if lit.name:
            by_name.setdefault(lit.name, lit)
    joined = 0
    used: set[str] = set()
    for u in units:
        key = u.tool_name
        if u.annotation_form is not None:
            # **エントリ自身（デコレータの `annotations=`）が宣言している。**
            # 木内の同名 `Tool(...)` リテラルで上書きしない。
            continue
        if key and key in by_name:
            lit = by_name[key]
            u.annotations = lit.annotations
            u.annotation_form = lit.form
            u.malformed_fields = lit.malformed_fields
            joined += 1
            used.add(key)
            continue
        if key is None and u.dispatch_names:
            # §2.9 (a): 低レベルハンドラは `dispatch_names`（本体の `name == "<literal>"`
            # 分岐から得た候補名）でリテラルを join する。ハンドラの `annotations` は
            # 立てない（1 ユニットが複数ツールを持つ）。効果ごとの帰属は
            # `analyze.py` が支配判定で行う（§2.9 (b)）。
            hit = {n: (by_name[n].annotations, by_name[n].form) for n in u.dispatch_names if n in by_name}
            if hit:
                u.dispatch_annotations = hit
                # **join した全リテラルの snake_case の和**（1 ユニットが複数ツールを持つ）。
                u.malformed_fields = tuple(sorted(
                    {m for n in hit for m in by_name[n].malformed_fields}
                ))
                used |= set(hit)
                joined += 1
            # §2.9 (d): 同じファイルの、名前が非リテラルのリテラルは join できない。件数を持つ。
            u.dispatch_unjoined = sum(1 for lit in literals if not lit.name and lit.relpath == u.relpath)
    unjoined = len([lit for lit in literals if not lit.name or lit.name not in used])
    return joined, unjoined


def scope_for(index: SourceIndex, unit: Unit) -> Optional[Scope]:
    path = index.resolve_module_path(unit.module)
    if path is None:
        return None
    return index.function_scope(path, unit.node)
