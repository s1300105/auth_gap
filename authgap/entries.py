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
from .srcindex import (
    FuncDef,
    Scope,
    SourceIndex,
    _local_bindings,
    dotted_of,
    idents_of,
    is_test_path,
    resolve_call_name,
)

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
    #: **mcp の版が決まらないため読み方が決まらない snake_case のキー**（D64 / U38、R2-r1-1）。
    #: mcp>=2.0 では `ToolAnnotations` の属性名そのもので camelCase の別名で protocol に届き、
    #: <2.0 では届かない（`D_malformed`）。版が決まらない木では**どちらにも倒さず `D_unknown`**（⊥ とも
    #: malformed とも混ぜない。Def 6 の版規則 (4)）。上界にも `explicit` にも入れない。
    undetermined_fields: tuple[str, ...] = ()
    #: 低レベル経路のとき、ハンドラ内の name 分岐から得た候補名。
    dispatch_names: tuple[str, ...] = ()
    #: 低レベル経路のとき、`dispatch_names` で join した `Tool(...)` リテラルの
    #: 宣言（ツール名 → `(annotations, form)`）。`docs/preregistration.md` §2.9 (a)。
    dispatch_annotations: dict[str, tuple[Optional[dict], str]] = field(default_factory=dict)
    #: 同じく、join したツールごとの :attr:`undetermined_fields`（空のツールは載せない）。
    dispatch_undetermined: dict[str, tuple[str, ...]] = field(default_factory=dict)
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
    #: `lowlevel_v2` のとき、mcp SDK が `CallToolRequestParams` を渡す仮引数の名前（第 2 位置。self / cls を
    #: 除いて数える。D64 / U38、R2-r3-1）。**登録が SDK の形だと裏付けられるときだけ**立てる
    #: （:func:`find_lowlevel_units`）。`analyze._seed` がこの仮引数に `CallToolRequestParams` の形を種付ける。
    v2_params_arg: Optional[str] = None

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
        if self.undetermined_fields:
            d["undetermined_fields"] = list(self.undetermined_fields)
        if self.v2_params_arg:
            d["v2_params_arg"] = self.v2_params_arg
        if self.dispatch_names:
            d["dispatch_names"] = list(self.dispatch_names)
        if self.dispatch_annotations:
            d["dispatch_annotations"] = {
                k: {"annotations": a, "form": f} for k, (a, f) in sorted(self.dispatch_annotations.items())
            }
            d["dispatch_unjoined"] = self.dispatch_unjoined
        if self.dispatch_undetermined:
            d["dispatch_undetermined"] = {k: list(v) for k, v in sorted(self.dispatch_undetermined.items())}
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
            # snake_case の注釈の読み方を決める mcp の主版は、ユニットのファイルのサブツリーで決める
            # （D64 / U38、R2-r1-1 と敵対的レビュー ADV-3）。
            units.append(_decorator_unit(fd, rule, call, snake=mcp_version_for(index, fd.relpath)))
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
    # tools_list の `already`（名前の集合）には、呼び出し形・spec_object のユニットの qualname を入れない
    # （D64 / U40-R8）。入れると、別モジュールの無関係な同名関数の tools-list ユニットが名前だけで消える
    # （数え落とし）。同じ関数の二重登録は `(module, qualname)` の registered で防ぐ。
    already = {u.qualname for u in units}
    units += find_registration_units(index, registered)
    units += find_tools_list_units(index, already, {(u.module, u.qualname) for u in units})
    units.sort(key=lambda u: (u.relpath, u.qualname, u.framework))
    return units


def _decorator_unit(
    fd: FuncDef,
    rule: EntryRule,
    call: Optional[ast.Call],
    registration: Optional[dict] = None,
    *,
    snake: str,
) -> Unit:
    """デコレータ規則に当たった関数のユニット。`call` はデコレータ（呼び出し形なら外側の登録呼び出し）。

    `snake` は snake_case の注釈の読み方を決める mcp の主版（:func:`mcp_version_class`、D64 / U38）。
    """
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
    undetermined: tuple[str, ...] = ()
    if ann_node is not None:
        # **3 つ目の戻り値（snake_case）を捨てない。** 捨てていたため
        # `D_malformed` が構造的に常に空だった（母集団 v2 に 574 箇所。O27 / D48）。
        ann, ann_form, malformed, undetermined = _read_annotations(ann_node, snake)
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
        undetermined_fields=undetermined,
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
    #: `R.NAME = ...` / `del R.NAME` / `setattr(R, "NAME", v)` / `R.__setattr__("NAME", v)` /
    #: `R.__dict__["NAME"] = v` / `vars(R)["NAME"] = v` の `(受け手の式 R, R を評価するスコープの列, NAME)`
    #: （名前が定数でなければ `"*"`）。**受け手は Name に限らない**（`import pkg.impl; pkg.impl.f = x` を
    #: 落とすと、書き換えられたモジュール属性を解いてしまう。D64 / U40-R4）。
    attr_pairs: list[tuple[ast.AST, tuple[ast.AST, ...], str]] = field(default_factory=list)
    #: import で束縛される名前 → import 文（モジュール直下でも関数の中でも）。
    imports: dict[str, list[ast.AST]] = field(default_factory=dict)
    #: 受け手を問わず書き換えられる属性名と、名前が定数でない `setattr` / `delattr` があるか。
    stored_attrs: set[str] = field(default_factory=set)
    any_setattr: bool = False
    #: このファイルのクラス定義と、それを評価するスコープの列（外 → 内。基底はこの列で解く）。
    classes: list[tuple[ast.ClassDef, tuple[ast.AST, ...]]] = field(default_factory=list)
    #: 単一の Name への代入 `X = <式>` の、代入先の Name ノード → 右辺（基底の別名をたどるのに使う）。
    alias_values: dict[ast.AST, ast.AST] = field(default_factory=dict)
    #: 本体で `locals()` / 引数なしの `vars()` を読む以外に使うクラス（クラスの名前空間を名前で書き換えうる）。
    ns_classes: list[ast.ClassDef] = field(default_factory=list)


#: `globals()` / `vars()` の結果を読むだけの属性（名前空間を書き換えない）。
_READ_ONLY_NS_ATTRS = frozenset({"get", "items", "keys", "values", "copy", "__contains__", "__getitem__"})


def _is_namespace_call(node: ast.AST) -> bool:
    """`globals()` / 引数なしの `vars()` / `locals()`（呼び出し位置の名前空間の辞書を返す）。

    `locals()` はモジュール直下では `globals()` と同じ辞書、クラス本体ではクラスの名前空間そのもので、
    書き込みがそのまま名前を束縛し直す（D64 / U40-R3）。関数の中の `locals()` は写しなので書き込んでも
    名前は変わらない（呼び出し側の `_note_facts` がスコープで分ける）。
    """
    if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)):
        return False
    fid = node.func.id
    return fid == "globals" or (fid in ("vars", "locals") and not node.args and not node.keywords)


#: 辞書を書き換える（読むだけでない）メソッド。`X.__dict__.update(...)` / `vars(X).setdefault(...)` など。
_DICT_WRITERS = frozenset({"update", "setdefault", "pop", "popitem", "clear", "__setitem__", "__delitem__"})


def _ns_dict_receiver(node: ast.AST) -> Optional[ast.AST]:
    """`R.__dict__` / `vars(R)` なら属性の名前空間の持ち主 `R`。"""
    if isinstance(node, ast.Attribute) and node.attr == "__dict__":
        return node.value
    if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "vars"
        and len(node.args) == 1
        and not node.keywords
    ):
        return node.args[0]
    return None


def _str_const(node: Optional[ast.AST]) -> Optional[str]:
    return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else None


def _mentions_sys_modules(node: ast.AST) -> bool:
    return any(isinstance(m, ast.Attribute) and m.attr == "modules" for m in ast.walk(node))


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


def _note_facts(node: ast.AST, parent: ast.AST, info: _ModInfo, chain: tuple[ast.AST, ...] = ()) -> None:
    """走査中のノード 1 つ（親は `parent`、評価するスコープの列は `chain`）から `_ModInfo` の事実を足す
    （`_scan_module_writes` / `_attr_stores` と同じ趣旨）。"""
    if isinstance(node, (ast.Global, ast.Nonlocal)):
        info.declared.update(node.names)
    elif isinstance(node, (ast.Import, ast.ImportFrom)):
        for al in node.names:
            if al.name != "*":
                info.imports.setdefault(al.asname or al.name.split(".")[0], []).append(node)
    elif isinstance(node, ast.ClassDef):
        info.classes.append((node, chain))
    elif isinstance(node, ast.Assign):
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            info.alias_values[node.targets[0]] = node.value
    elif isinstance(node, ast.Attribute) and isinstance(node.ctx, (ast.Store, ast.Del)):
        info.stored_attrs.add(node.attr)
        info.attr_pairs.append((node.value, chain, node.attr))
        if node.attr == "__dict__":
            # `R.__dict__ |= {...}` / `R.__dict__ = {...}` / `del R.__dict__` は R の属性の書き換え（D64 / U40-RC4）。
            # 右辺が定数キーだけの dict ならそのキー、そうでなければどの名前でもありうる。
            keys = _const_dict_keys(_assigned_value(parent, node))
            for k in keys if keys is not None else [None]:
                _note_attr_write(info, node.value, chain, k)
    elif isinstance(node, ast.Subscript) and isinstance(node.ctx, (ast.Store, ast.Del)):
        # `R.__dict__["NAME"] = v` / `vars(R)["NAME"] = v` は属性 NAME の書き換え（D64 / U40-R2）。
        owner = _ns_dict_receiver(node.value)
        if owner is not None:
            _note_attr_write(info, owner, chain, _str_const(node.slice))
    elif isinstance(node, ast.Call):
        _note_call_facts(node, parent, info, chain)


def _assigned_value(parent: ast.AST, target: ast.AST) -> Optional[ast.AST]:
    """`parent` が `target` への代入（`=` の唯一の代入先 / `op=` / 注釈つき）なら右辺。それ以外は None。"""
    if isinstance(parent, ast.Assign) and len(parent.targets) == 1 and parent.targets[0] is target:
        return parent.value
    if isinstance(parent, (ast.AugAssign, ast.AnnAssign)) and parent.target is target:
        return parent.value
    return None


def _const_dict_keys(node: Optional[ast.AST]) -> Optional[list[str]]:
    """`{"a": x, "b": y}`（キーがすべて文字列定数、`**` の展開なし）ならキーの列。それ以外は None。"""
    if not isinstance(node, ast.Dict):
        return None
    keys = [_str_const(k) for k in node.keys]
    return None if any(k is None for k in keys) else [k for k in keys if k is not None]


def _note_attr_write(
    info: _ModInfo, owner: Optional[ast.AST], chain: tuple[ast.AST, ...], name: Optional[str]
) -> None:
    """受け手 `owner`（`super()` のように式として持てないなら None）の属性 `name`（定数でなければ None）の
    書き換えを記録する。"""
    if name is not None:
        info.stored_attrs.add(name)
    else:
        info.any_setattr = True
    if owner is None:
        return
    info.attr_pairs.append((owner, chain, name or "*"))
    if _mentions_sys_modules(owner):
        info.dynamic = True  # `setattr(sys.modules[__name__], name, fn)` / `sys.modules[__name__].__dict__[k] = v`


def _note_call_facts(node: ast.Call, parent: ast.AST, info: _ModInfo, chain: tuple[ast.AST, ...]) -> None:
    fid = node.func.id if isinstance(node.func, ast.Name) else None
    if _is_namespace_call(node) and not _namespace_read_only(parent, node):
        # 名前空間の持ち主は、内包を除いた最も内側のスコープ（D64 / U40-R3）。
        owner = next((c for c in reversed(chain) if not isinstance(c, _COMP_NODES)), None)
        if fid != "locals" or owner is None or isinstance(owner, ast.Module):
            # globals() と引数なしの vars() は従来どおりどこにあっても。locals() はモジュール直下だけ
            # （globals() と同じ辞書）。関数の中の locals() は写しで、書き込んでも名前は変わらない。
            info.dynamic = True
        if isinstance(owner, ast.ClassDef) and fid in ("vars", "locals"):
            info.ns_classes.append(owner)  # クラス本体の locals() / vars() はクラスの名前空間そのもの
    if fid in ("exec", "eval") and len(node.args) + len(node.keywords) < 2:
        info.dynamic = True  # 既定の名前空間（呼び出し位置のグローバル）で実行する
    if _last_name(node) in _SETATTR and len(node.args) >= 2:
        _note_attr_write(info, node.args[0], chain, _str_const(node.args[1]))
    f = node.func
    if isinstance(f, ast.Attribute) and f.attr in ("__setattr__", "__delattr__"):
        # D64 / U40-R2。`object.__setattr__(self, "NAME", v)` / `type.__setattr__(C, "NAME", v)` は非束縛形
        # （名前は args[1]）、`self.__setattr__("NAME", v)` / `super().__setattr__("NAME", v)` は束縛形
        # （名前は args[0]）。`super()` の受け手は式として持てない（インスタンスなのでモジュールではない）。
        unbound = isinstance(f.value, ast.Name) and f.value.id in ("object", "type")
        bound_owner = None if unbound or isinstance(f.value, ast.Call) else f.value
        if unbound and len(node.args) >= 2:
            _note_attr_write(info, node.args[0], chain, _str_const(node.args[1]))
        elif not unbound and node.args and _str_const(node.args[0]) is not None:
            _note_attr_write(info, bound_owner, chain, _str_const(node.args[0]))
        else:
            # 形を決められない（`Base.__setattr__(self, name, v)` / `self.__setattr__(name, v)`）。見過ぎる側に
            # 倒し、名前が定数でない書き換えとして、ありうる受け手の両方に記録する。
            _note_attr_write(info, bound_owner, chain, None)
            if node.args and _str_const(node.args[0]) is None:
                _note_attr_write(info, node.args[0], chain, None)
    elif isinstance(f, ast.Attribute) and f.attr in _DICT_WRITERS:
        owner = _ns_dict_receiver(f.value)
        if owner is not None:
            _note_attr_write(info, owner, chain, None)  # `R.__dict__.update(...)` / `vars(R).setdefault(...)`


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

    **スコープごとに 1 回だけ歩いて全部の名前の表を作る**（:func:`_scope_binding_table`）。以前は（スコープ, 名前）の
    組ごとに歩き直し、run21 で xagent の `find_units` が 12.7 → 61.9 秒になって木の時間上限でユニットが落ちた。
    名前ごとの束縛の列（順を含む）と動的かどうかは、名前ごとに歩いていたとき（:func:`_scope_bindings_uncached`、
    テストの突き合わせ用に残す）と同じ。

    :returns: `(束縛するノードの列, global / nonlocal / import * で動的に決まるか)`
    """
    table, star, declared, comp = _scope_binding_table(scope)
    binds = list(table.get(name, ()))
    if comp:
        return binds, False
    return binds, star or name in declared


def _scope_binding_table(scope: ast.AST) -> tuple[dict[str, list[ast.AST]], bool, frozenset[str], bool]:
    """`(名前 → 束縛するノードの列, import * があるか, global / nonlocal の名前, 内包のスコープか)`。スコープの AST に置く。"""
    cached = scope.__dict__.get("_authgap_scope_table")
    if cached is not None:
        return cached
    table: dict[str, list[ast.AST]] = {}

    def add(n: str, node: ast.AST) -> None:
        table.setdefault(n, []).append(node)

    if isinstance(scope, _COMP_NODES):
        for gen in scope.generators:
            for n in _target_names(gen.target):
                add(n.id, n)
        out = (table, False, frozenset(), True)
        scope.__dict__["_authgap_scope_table"] = out
        return out
    star = False
    declared: set[str] = set()
    stack: list[ast.AST] = []
    if isinstance(scope, (*_FUNC_NODES, ast.Lambda)):
        for a in _arg_nodes(scope.args):
            add(a.arg, a)
        body = scope.body if isinstance(scope.body, list) else [scope.body]
        stack += list(body)
    else:
        stack += list(getattr(scope, "body", []))
    while stack:
        node = stack.pop()
        if isinstance(node, (*_FUNC_NODES, ast.ClassDef)):
            add(node.name, node)
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
            for n in ast.walk(node):
                if isinstance(n, ast.NamedExpr) and isinstance(n.target, ast.Name):
                    add(n.target.id, n)
            continue
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for a in node.names:
                if a.name == "*":
                    star = True
                else:
                    add(a.asname or a.name.split(".")[0], node)
            continue
        if isinstance(node, (ast.Global, ast.Nonlocal)):
            declared.update(node.names)
            continue
        if isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Store, ast.Del)):
            add(node.id, node)
        elif isinstance(node, ast.ExceptHandler) and node.name:
            add(node.name, node)
        elif isinstance(node, ast.alias):
            continue
        elif type(node).__name__ in ("MatchAs", "MatchStar") and getattr(node, "name", None):
            add(node.name, node)  # type: ignore[attr-defined]
        elif type(node).__name__ == "MatchMapping" and getattr(node, "rest", None):
            add(node.rest, node)  # type: ignore[attr-defined]
        stack += list(ast.iter_child_nodes(node))
    out = (table, star, frozenset(declared), False)
    scope.__dict__["_authgap_scope_table"] = out
    return out


def _scope_bindings_uncached(scope: ast.AST, name: str) -> tuple[list[ast.AST], bool]:
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


def _stmt_index(body: list, node: ast.AST) -> Optional[int]:
    """`body`（文の列）のうち `node` を含む文の位置（デコレータも文に含める）。見つからなければ None。"""
    for k, stmt in enumerate(body):
        if stmt is node:
            return k
    if not hasattr(node, "lineno"):
        return None
    at = (node.lineno, node.col_offset)
    end = (getattr(node, "end_lineno", None) or node.lineno, getattr(node, "end_col_offset", None) or node.col_offset)
    for k, stmt in enumerate(body):
        starts = [(stmt.lineno, stmt.col_offset)]
        starts += [(d.lineno, d.col_offset) for d in getattr(stmt, "decorator_list", [])]
        s_end = (stmt.end_lineno or stmt.lineno, stmt.end_col_offset or 0)
        if min(starts) <= at and end <= s_end:
            return k
    return None


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
        self._graph: Optional[list[tuple[str, ast.ClassDef, tuple[tuple[str, str], ...]]]] = None
        self._ns_classes: Optional[list[ast.ClassDef]] = None
        #: `attr_writes` / `_class_graph` を作っている途中か（その間の `_overridden_below` は見過ぎる側で真）。
        self._building = False

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
        """木のどこかで `x.NAME = ...` / `del x.NAME` / `setattr(x, "NAME", v)` / `x.__setattr__("NAME", v)` /
        `x.__dict__["NAME"] = v` と書き換えられる属性名と、名前が定数でない書き換えがあるか。"""
        if self._stored_attrs is None:
            names: set[str] = set()
            any_name = False
            for info in self._by_path.values():
                names |= info.stored_attrs
                any_name = any_name or info.any_setattr
            self._stored_attrs = (frozenset(names), any_name)
        return self._stored_attrs

    def ns_class(self, cls: ast.ClassDef) -> bool:
        """クラス本体が `locals()` / `vars()` でクラスの名前空間を書き換えうるか（D64 / U40-R3）。"""
        if self._ns_classes is None:
            self._ns_classes = [c for info in self._by_path.values() for c in info.ns_classes]
        return any(c is cls for c in self._ns_classes)

    def modules(self) -> frozenset[str]:
        if self._modules is None:
            self._modules = frozenset(self.index.module_name(p) for p in self.index.py_files())
        return self._modules

    def abs_module(self, dotted: Optional[str], importer: Optional[str] = None) -> tuple[str, Optional[str]]:
        """絶対 import の dotted 名を木内モジュールへ。`("tree", 名)` / `("extern", None)` / `("ambiguous", None)`。

        完全一致を先に採り、なければ `.<dotted>` で終わる木内モジュールが**ちょうど 1 つ**のときだけ採る
        （src レイアウト）。2 つ以上なら決めない（`resolve_module_path` の setdefault のように最初の 1 つを
        採ると、別のパッケージの同名モジュールに解く）。

        **import する側（`importer`）と同じディレクトリに `<先頭>.py` / `<先頭>/__init__.py` があり、それが
        選んだ木内モジュールと違うなら決めない**（D64 / U40-R6）。スクリプトとして動かすと `sys.path[0]` は
        スクリプトのディレクトリなので兄弟が先に当たり、パッケージとして動かすと根の方が当たる。どちらで
        動かすかは木からは決まらない。
        """
        if not dotted:
            return "ambiguous", None
        mods = self.modules()
        chosen: Optional[str]
        if dotted in mods:
            chosen = dotted
        else:
            # 末尾一致の候補は dotted ごとに覚える（木の全モジュールを毎回なめていた。結果は同じ）
            memo = self.__dict__.setdefault("_abs_hits", {})
            hits = memo.get(dotted)
            if hits is None:
                hits = memo[dotted] = [m for m in mods if m.endswith("." + dotted)]
            if not hits:
                return "extern", None
            chosen = hits[0] if len(hits) == 1 else None
        sibling = self._sibling_module(importer, dotted)
        if chosen is None or (sibling is not None and sibling != chosen):
            return "ambiguous", None
        return "tree", chosen

    def _sibling_module(self, importer: Optional[str], dotted: str) -> Optional[str]:
        """`importer` のファイルと同じディレクトリにある `<先頭>.py` / `<先頭>/__init__.py` から見た `dotted` の
        木内モジュール名（兄弟が無ければ None）。"""
        info = self.info(importer) if importer else None
        if info is None:
            return None
        head, _, rest = dotted.partition(".")
        d = os.path.dirname(os.path.abspath(info.path))
        for cand in (os.path.join(d, head, "__init__.py"), os.path.join(d, head + ".py")):
            if os.path.isfile(cand):
                base = self.index.module_name(cand)
                return f"{base}.{rest}" if rest else base
        if rest and os.path.isdir(os.path.join(d, head)):
            # `<先頭>/` が `__init__.py` の無い名前空間パッケージ（D64 / U40-RC3）。その部分は `sys.path` の順に
            # 並ぶので、残りの dotted のファイルが兄弟の下にあれば、スクリプトとして動かすとそちらが当たる。
            sub = os.path.join(d, head, *rest.split("."))
            for cand in (os.path.join(sub, "__init__.py"), sub + ".py"):
                if os.path.isfile(cand):
                    return self.index.module_name(cand)
        return None

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
        """木のどこかで**モジュール属性として**書き換えられうる `(module, NAME)`（`NAME` が `"*"` なら全部）。

        `R.NAME = ...` / `del R.NAME` / `setattr(R, "NAME", v)` など。受け手 `R` は、そのファイルのそのスコープで
        `expr` によって解く（`import pkg.impl; pkg.impl.f = x` の連鎖形も。D64 / U40-R4）。

        * 木内モジュールに解ければ `(そのモジュール, NAME)`。
        * **解けない受け手**（`sys.modules["m"]`、`import_module("m")`、ローカル変数）は、どのモジュールでも
          ありうるので `("*", NAME)`（見過ぎる側。`self.m` で `stored_attrs` を使うのと同じ方針）。ただし
          名前が定数でないものは全部の名前になるので記録しない（限界。`setattr(obj, k, v)` の汎用の書き方で
          木の全部の解決を止めないため）。
        * メソッドの第 1 仮引数（インスタンス / クラス）と、関数・クラス・木外に解ける受け手はモジュールでは
          ないので数えない。
        """
        if self._attr_writes is None:
            # 集める間は書き換えの確認を外して import をたどる（再帰を止める）。集めた後の解決では確認する。
            self._attr_writes = frozenset()
            out: set[tuple[str, str]] = set()
            building, self._building = self._building, True
            try:
                for path in sorted(self._by_path):
                    info = self._by_path[path]
                    mod = self.index.module_name(path)
                    for recv, chain, attr in info.attr_pairs:
                        if isinstance(recv, ast.Name) and self._instance_param(mod, chain, recv):
                            continue
                        ref = self.expr(mod, chain, recv)
                        if ref is not None and ref.kind == "module":
                            out.add((ref.name, attr))
                        elif ref is None and attr != "*":
                            out.add(("*", attr))
            finally:
                self._building = building
            self._attr_writes = frozenset(out)
        return self._attr_writes

    def _written(self, module: str, name: str) -> bool:
        return bool({(module, name), (module, "*"), ("*", name)} & self.attr_writes())

    def _stable_module_binding(self, module: str, name: str, hops: int = _IMPORT_HOPS) -> Optional[ast.AST]:
        """モジュール水準の `name` の唯一の束縛（動的に書き換えられうるなら None）。"""
        info = self.info(module)
        if info is None or hops < 0:
            return None
        if info.dynamic or name in info.declared:
            return None
        binds, dynamic = self.module_bindings(module, name)
        if dynamic or len(binds) != 1:
            return None
        if self._written(module, name):
            return None
        return binds[0]

    def in_module(self, module: str, name: str, hops: int = _IMPORT_HOPS) -> Optional[_Ref]:
        """モジュール水準の `name`。束縛が**ちょうど 1 つ**で、動的に書き換えられないときだけ解く。"""
        b = self._stable_module_binding(module, name, hops)
        info = self.info(module)
        if b is None or info is None:
            return None
        return self._from_binding(module, b, name, (info.tree,), hops)

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
            status, mod = self.abs_module(dotted, module)
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
            status, target = self.abs_module(node.module, module)
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
        self, module: str, chain: tuple[ast.AST, ...], name: str, ref: Optional[ast.AST] = None
    ) -> tuple[str, Optional[int], list[ast.AST]]:
        """`name`（参照のノードは `ref`）を束縛する最も内側のスコープ。

        :returns: `("local", chain の位置, 束縛)` / `("module", None, [])` / `("dynamic", None, [])`。
            クラス本体は、参照がその本体に直接あるときだけ見える（Python のスコープ規則）。
            クラス本体の扱いは :meth:`_class_body_binding`（D64 / U40-R5）。
        """
        info = self.info(module)
        if info is None or name in info.declared:
            return "dynamic", None, []
        for i in range(len(chain) - 1, 0, -1):
            scope = chain[i]
            if isinstance(scope, ast.ClassDef):
                if i != len(chain) - 1:
                    continue
                got = self._class_body_binding(scope, name, ref)
                if got is None:
                    continue
                if isinstance(got, str):
                    return got, None, []
                return "local", i, [got]
            binds, dynamic = _scope_bindings(scope, name)
            if dynamic:
                return "dynamic", None, []
            if binds:
                return "local", i, binds
        return "module", None, []

    def _class_body_binding(self, cls: ast.ClassDef, name: str, ref: Optional[ast.AST]):
        """クラス本体に直接ある参照 `ref` から見た `name`（D64 / U40-R5）。

        **クラス本体の名前は LOAD_NAME で引かれる。** クラスのローカルな束縛が参照を含む文より後にしか
        無ければ、参照の時点ではまだ束縛されておらず、グローバルに落ちる（囲む関数のスコープは飛ばす）。
        束縛が参照より前にあるときは、それがクラス本体に直接ある文（`if` / `try` の中でない）で、ほかに
        束縛が無いときだけ採る。それ以外（条件つきの束縛、参照と同じ文の中、`locals()` による書き換え）は
        決めない。

        :returns: None（束縛なし。外のスコープへ）/ ``"module"``（グローバルへ）/ ``"dynamic"``（決めない）/
            束縛のノード。
        """
        if self.ns_class(cls):
            return "dynamic"
        binds, dynamic = _scope_bindings(cls, name)
        if dynamic:
            return "dynamic"
        if not binds:
            return None
        pos = _stmt_index(cls.body, ref) if ref is not None else None
        if pos is None:
            return "dynamic"
        idx = [_stmt_index(cls.body, b) for b in binds]
        if any(k is None or k == pos for k in idx):
            return "dynamic"
        if all(k is not None and k > pos for k in idx):
            return "module"
        if len(binds) != 1 or not any(s is binds[0] for s in cls.body):
            return "dynamic"
        return binds[0]

    def name(
        self, module: str, chain: tuple[ast.AST, ...], name: str, ref: Optional[ast.AST] = None
    ) -> Optional[_Ref]:
        where, i, binds = self._binding_scope(module, chain, name, ref)
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
            return self.name(module, chain, node.id, node)
        if not isinstance(node, ast.Attribute):
            return None
        if isinstance(node.value, ast.Name):
            handled, ref = self._self_method(module, chain, node.value, node.attr)
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

    def _method_of_param(
        self, module: str, chain: tuple[ast.AST, ...], head: ast.Name
    ) -> Optional[tuple[int, ast.AST, list[ast.AST]]]:
        """`head` を束縛する最も内側のスコープが、クラス本体に直接あるメソッドで、`head` がその第 1 仮引数の名前なら
        `(chain の位置, メソッド, そのメソッドの中の束縛)`。"""
        where, i, binds = self._binding_scope(module, chain, head.id, head)
        if where != "local" or i is None:
            return None
        meth = chain[i]
        if not isinstance(meth, _FUNC_NODES) or i < 1 or not isinstance(chain[i - 1], ast.ClassDef):
            return None
        positional = list(meth.args.posonlyargs) + list(meth.args.args)
        if not positional or positional[0].arg != head.id:
            return None
        return i, meth, binds

    def _instance_param(self, module: str, chain: tuple[ast.AST, ...], head: ast.Name) -> bool:
        """`head` がメソッドの第 1 仮引数（インスタンスかクラス。staticmethod でない）のままか。"""
        hit = self._method_of_param(module, chain, head)
        if hit is None:
            return False
        _i, meth, binds = hit
        positional = list(meth.args.posonlyargs) + list(meth.args.args)
        if len(binds) != 1 or binds[0] is not positional[0]:
            return False
        return not any(_last_name(d) == "staticmethod" for d in meth.decorator_list)

    def _self_method(
        self, module: str, chain: tuple[ast.AST, ...], head: ast.Name, attr: str
    ) -> tuple[bool, Optional[_Ref]]:
        """`self.<attr>` を**囲むクラスの中だけ**で解く（D64 / U40 条件 (2)）。

        `head` が、クラス本体に直接ある（staticmethod / classmethod でない）メソッドの第 1 仮引数で、
        そのメソッドの中で束縛し直されないときだけ扱う。クラス本体で `attr` を束縛するのがちょうど 1 つの
        def で、インスタンス属性・クラス属性として書き換えられず、木内のサブクラスが上書きしないときだけ採る。
        別クラスの同名メソッドや木外の基底から来るメソッドは採らない。

        :returns: `(self 形として扱ったか, 参照)`。扱わないなら一般の解決に回す。
        """
        hit = self._method_of_param(module, chain, head)
        if hit is None:
            return False, None
        i, meth, binds = hit
        positional = list(meth.args.posonlyargs) + list(meth.args.args)
        if len(binds) != 1 or binds[0] is not positional[0]:
            return True, None  # self を束縛し直している
        if any(_last_name(d) in ("staticmethod", "classmethod") for d in meth.decorator_list):
            return True, None
        cls = chain[i - 1]
        assert isinstance(cls, ast.ClassDef)
        if self.ns_class(cls):
            return True, None  # クラス本体の locals() / vars() で名前空間を書き換えうる（U40-R3）
        cbinds, cdyn = _scope_bindings(cls, attr)
        if cdyn or len(cbinds) != 1 or not isinstance(cbinds[0], _FUNC_NODES):
            return True, None
        target = cbinds[0]
        if any(_last_name(d) in _NON_FUNCTION_DECORATORS for d in target.decorator_list):
            return True, None
        # インスタンス属性・クラス属性としての書き換え（`self.m = ...` / `C.m = ...` / `setattr(x, "m", v)` /
        # `object.__setattr__(self, "m", v)` / `self.__dict__["m"] = v`。U40-R2）。受け手の型は見ず、木のどこかで
        # 同じ名前の属性が書き換えられるなら採らない。
        stored, any_setattr = self.stored_attrs()
        if attr in stored or any_setattr:
            return True, None
        # 木内のサブクラス（何段下でも）か、その MRO で `cls` より前に来うるミックスインが同名で上書きする
        # （`self.m` は動的に束縛される）。
        if self._overridden_below(module, chain[: i - 1], cls, attr):
            return True, None
        ref = self._from_binding(module, target, attr, chain[:i], _IMPORT_HOPS)
        return True, ref

    # -- クラスの継承 --------------------------------------------------------

    def _base_ref(
        self, module: str, chain: tuple[ast.AST, ...], node: Optional[ast.AST], depth: int = _IMPORT_HOPS
    ) -> Optional[_Ref]:
        """クラスの基底の式 `node` が指すもの（D64 / U40-R1）。

        Subscript（`Server[str]`、`Generic[T]`）は value を見る。import の別名は `expr` がたどる。単一の Name
        への代入 `Base = s.Server` は右辺をたどる（モジュール水準は書き換えられないときだけ）。どこにも
        束縛されない名前は組込み（`object` / `Exception`）。それ以外（呼び出し式、解けない名前）は None。
        """
        while isinstance(node, ast.Subscript):
            node = node.value
        if not isinstance(node, (ast.Name, ast.Attribute)) or depth < 0:
            return None
        ref = self.expr(module, chain, node)
        if ref is not None:
            return ref
        info = self.info(module)
        if info is None:
            return None
        if isinstance(node, ast.Name):
            where, i, binds = self._binding_scope(module, chain, node.id, node)
            if where == "module":
                if info.dynamic or node.id in info.declared:
                    return None
                mbinds, dyn = self.module_bindings(module, node.id)
                if dyn:
                    return None
                if not mbinds:
                    return _Ref("extern", "builtins." + node.id)
                b = self._stable_module_binding(module, node.id)
                val = info.alias_values.get(b) if b is not None else None
                return self._base_ref(module, (info.tree,), val, depth - 1)
            if where == "local" and i is not None and len(binds) == 1:
                return self._base_ref(module, chain[: i + 1], info.alias_values.get(binds[0]), depth - 1)
            return None
        base = self.expr(module, chain, node.value)
        if base is None or base.kind != "module" or f"{base.name}.{node.attr}" in self.modules():
            return None
        tinfo = self.info(base.name)
        if tinfo is None:
            return None
        return self._base_ref(base.name, (tinfo.tree,), ast.Name(id=node.attr, ctx=ast.Load()), depth - 1)

    def _class_graph(self) -> list[tuple[str, ast.ClassDef, tuple[tuple[str, str], ...]]]:
        """木内の全クラス `(識別名, 定義, 基底)`。基底は `("class", 識別名)` / `("extern", dotted)` /
        `("unknown", "")`（解けない）。識別名は `_from_binding` のクラス参照と同じ形。"""
        if self._graph is None:
            self.attr_writes()  # 基底の名前も、書き換えの確認を済ませてから解く
            graph = []
            building, self._building = self._building, True
            try:
                for path in sorted(self._by_path):
                    info = self._by_path[path]
                    mod = self.index.module_name(path)
                    for node, chain in info.classes:
                        bases: list[tuple[str, str]] = []
                        for b in node.bases:
                            ref = self._base_ref(mod, chain, b)
                            if ref is not None and ref.kind in ("class", "extern"):
                                bases.append((ref.kind, ref.name))
                            else:
                                bases.append(("unknown", ""))
                        graph.append((f"{mod}.{_qual_prefix(chain)}{node.name}", node, tuple(bases)))
            finally:
                self._building = building
            self._graph = graph
        return self._graph

    def _overridden_below(self, module: str, outer: tuple[ast.AST, ...], cls: ast.ClassDef, attr: str) -> bool:
        """`cls` の木内のサブクラス（推移的）と、それらから `cls` を通らずにたどれる基底のどれかが
        `attr` を束縛するか（D64 / U40-R1）。

        **基底は末尾名で結ばず `_base_ref` で解く**（別名の import、`Base = s.Server`、`Server[str]` を
        落とさない）。**解けない基底を持つクラスは、どのクラスのサブクラスでもありうる**ものとして扱う
        （見過ぎる側）: それ自身かその下のクラスが `attr` を束縛すれば採らない。

        D64 / U40 の 3 巡目:

        * RC1: **確かなサブクラス**（`("class", ...)` の辺だけで `cls` に結ばれる）と、そこから `cls` を通らずに
          たどれる基底（`cls` 自身の祖先は除く。C3 で `cls` より後に来る）が**解けない基底**を持つなら、その
          基底（try/except の import、呼び出し式のミックスイン）が `attr` を束縛しうるので採らない。確かな
          サブクラスの外のクラスの解けない基底では採るのをやめない（木の全部の `self.m` を失わないため）。
        * RC2: 木外（extern）と判定した基底でも、dotted 名の末尾が木内のクラス名（`cls`、サブクラス、`attr` を
          束縛するクラス）と一致するなら解けない基底として扱う（走査の根がパッケージそのもので
          `from proj.s import Server` が木外に落ちる）。
        """
        if self._building:
            return True  # 書き換え・継承の表を作っている途中（受け手の `self.x.y` など）は決めない側に倒す
        target = f"{module}.{_qual_prefix(outer)}{cls.name}"
        graph = self._class_graph()
        binds_attr = {
            ident
            for ident, node, _b in graph
            if node is not cls and (bool(_scope_bindings(node, attr)[0]) or self.ns_class(node))
        }
        names = {cls.name} | {node.name for ident, node, _b in graph if ident in binds_attr}

        def kind(k: str, n: str) -> str:
            return "unknown" if k == "extern" and n.rsplit(".", 1)[-1] in names else k

        subs: set[str] = set()
        definite: set[str] = set()
        changed = True
        while changed:
            changed = False
            for ident, node, bases in graph:
                if node is cls or ident in definite:
                    continue
                ks = [(kind(k, n), n) for k, n in bases]
                if any(k == "class" and (n == target or n in definite) for k, n in ks):
                    definite.add(ident)
                elif ident in subs or not any(k == "unknown" or (k == "class" and n in subs) for k, n in ks):
                    continue
                subs.add(ident)
                names.add(node.name)
                changed = True
        if not subs:
            return False

        def reach(start: set[str], skip: set[str]) -> set[str]:
            out = set(start)
            frontier = list(start)
            while frontier:
                cur = frontier.pop()
                for ident, _node, bases in graph:
                    if ident != cur:
                        continue
                    for k, n in bases:
                        if k == "class" and n not in skip and n not in out:
                            out.add(n)
                            frontier.append(n)
            return out

        # RC1: 確かなサブクラスとそこからたどれる基底（`cls` の祖先は除く）の解けない基底。
        ancestors = reach({target}, set())
        dcheck = reach(definite, ancestors)
        if any(
            ident in dcheck and node is not cls and any(kind(k, n) == "unknown" for k, n in bases)
            for ident, node, bases in graph
        ):
            return True
        # サブクラスと、そこから `cls` を通らずにたどれる基底（MRO で `cls` より前に来うるミックスイン）。
        check = reach(subs, {target})
        return bool(check & binds_attr)

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
            _note_facts(node, parent, info, chain)
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
                    found.append((node.lineno, node.col_offset, _decorator_unit(
                        ref.fd, rule, decl_call, where,
                        # snake_case の読み方は登録文のファイルのサブツリーの版（D64 / U38 の ADV-3）
                        snake=mcp_version_for(index, where["relpath"]),
                    )))
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

    # v2: `Server(on_call_tool=handler)` / `add_request_handler("tools/call", ..., handler)`
    v2: dict[str, tuple[FuncDef, bool]] = {}
    for reg in lowlevel_v2_registrations(index):
        if reg.handler_name is None:
            continue  # partial / lambda など。`unresolved_handler` として manifest に残る（規則 4）
        cands, pinned = _resolve_v2_handler(index, reg)
        for fd in cands:
            key = f"{fd.module}:{fd.qualname}"
            if key in seen:
                continue
            prev = v2.get(key)
            # **種付けは、そのハンドラの登録がすべて SDK の形で、定義が handler 式の形と合うときだけ**
            # （1 つでも外れれば種付けしない。今までどおり裸の Atom）。
            sdk = reg.sdk and (pinned or _handler_form_matches(reg, fd))
            v2[key] = (fd, sdk if prev is None else (prev[1] and sdk))
    for key in sorted(v2):
        fd, sdk = v2[key]
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
                v2_params_arg=_v2_params_arg(fd.node) if sdk else None,
            )
        )
    return out


# --------------------------------------------------------------------------
# 低レベル v2 の登録点（D64 / U38: R2-r3-2 / R2-r3-3 / R2-r4-1）
# --------------------------------------------------------------------------

#: import 表で解いた mcp SDK の低レベル `Server` の名前（R2-r4-1 の別名 import。`from mcp.server.lowlevel
#: import Server as X` / `from mcp.server import Server as X`）。mcp 2.2.0 の `mcp/server/__init__.py` と
#: `mcp/server/lowlevel/__init__.py` が再公開する名前。
MCP_LOWLEVEL_SERVER_NAMES: frozenset[str] = frozenset(
    {"mcp.server.lowlevel.Server", "mcp.server.lowlevel.server.Server", "mcp.server.Server"}
)

#: SDK の `add_request_handler(method, params_type, handler)` の `params_type` として SDK 形の裏付けになる型
#: （import 表で解いた名前の、先頭のパッケージと末尾名）。mcp 2.2.0 は型を `mcp_types` に分けて `mcp.types` から再公開する。
_SDK_TYPE_PACKAGES: frozenset[str] = frozenset({"mcp", "mcp_types"})
_CALL_TOOL_PARAMS = "CallToolRequestParams"


@dataclass
class V2Registration:
    """`Server(on_call_tool=h)` / `add_request_handler("tools/call", ..., h)` の登録点 1 つ。"""

    relpath: str
    module: str
    lineno: int
    #: `on_call_tool` / `add_request_handler`。
    form: str
    #: handler 式。
    handler: ast.AST
    #: handler 式の dotted 名。dotted でない式（partial / lambda / 添字）は None。
    handler_name: Optional[str]
    #: 登録が mcp SDK の形だと裏付けられるか（`Server` が import 表で mcp の `Server` に解ける、または
    #: `add_request_handler` の `params_type` が mcp の `CallToolRequestParams` に解ける）。
    sdk: bool
    #: 登録を囲む定義（外側から。関数・クラス・lambda）。
    enclosing: tuple[ast.AST, ...] = ()
    #: 登録の呼び出しの列（同じ行の別の登録と区別する。1 つの登録点が handler の候補を複数持つとき、
    #: それらは `(relpath, lineno, col, form)` が同じ）。
    col: int = 0
    #: 同じ登録点の handler の候補の式（自前の 3 引数形の `args[1]` と `args[-1]`。ADV-2）。1 つなら自分だけ。
    alternatives: tuple[ast.AST, ...] = ()

    def site(self) -> tuple[str, int, int, str]:
        return (self.relpath, self.lineno, self.col, self.form)

    def unresolved_json(self) -> dict:
        h = self.handler
        callee = dotted_of(h.func) if isinstance(h, ast.Call) else None
        d: dict[str, Any] = {
            "relpath": self.relpath,
            "lineno": self.lineno,
            "form": self.form,
            "expr": type(h).__name__,
        }
        if callee:
            d["callee"] = callee
        # dotted 名でない式（partial / lambda）か、dotted 名だが木の中の関数の定義に 1 つも当たらないか
        d["reason"] = "not_dotted" if self.handler_name is None else "no_definition"
        if len(self.alternatives) > 1:
            d["candidates"] = [dotted_of(a) or type(a).__name__ for a in self.alternatives]
        return d


def _calls_with_enclosing(tree: ast.AST):
    """`(Call, 囲む定義の列)` を決定論的な順序で返す。"""
    stack: list[tuple[ast.AST, tuple[ast.AST, ...]]] = [(tree, ())]
    while stack:
        node, encl = stack.pop()
        if isinstance(node, ast.Call):
            yield node, encl
        inner = encl + (node,) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)) else encl
        stack.extend((c, inner) for c in reversed(list(ast.iter_child_nodes(node))))


def _kw(node: ast.Call, name: str) -> Optional[ast.AST]:
    for kw in node.keywords:
        if kw.arg == name:
            return kw.value
    return None


def lowlevel_v2_registrations(index: SourceIndex) -> list[V2Registration]:
    """木の中の低レベル v2 の登録点（索引ごとに記憶化）。

    * `Server(...)`: 被呼び出し名の末尾が `Server`、**または import 表で mcp の `Server` に解ける**
      （別名 import。R2-r4-1）。どの形でも `on_call_tool=` キーワードを要求する（`uvicorn.Server` を拾わない）。
    * `add_request_handler(...)`: method は `args[0]` か `method=` で `"tools/call"`。handler は `handler=`。
      無ければ位置引数から取る（R2-r3-2。SDK は `(method, params_type, handler)` の 3 引数で、`args[1]` は
      `params_type`。`args[2]` だけにすると自前の JSON-RPC の 2 引数形 `(method, handler)` が消える）:

      - 2 引数: `args[1]`。
      - 3 引数以上で **`args[1]` が mcp の `CallToolRequestParams` に解ける**（SDK の形と裏付けられる）: `args[-1]`。
      - それ以外の 3 引数以上: **`args[1]` と `args[-1]` の両方を候補**にする（D64 / U38 の敵対的レビュー ADV-2。
        自前の `(method, handler, params_model)` で `args[-1]` の型を handler と取り違えると、本物のハンドラの
        ユニットが消え、型名は関数に当たらないので記録にも残らなかった）。同じ登録点の候補は 1 つずつ
        登録として返し、`alternatives` に候補の式の列を持つ。どれも関数に解けなければ
        :func:`unresolved_handlers` に数える。
    """
    cache = index.__dict__.setdefault("_authgap_v2_registrations", {})
    if "all" in cache:
        return cache["all"]
    out: list[V2Registration] = []
    for path in index.py_files():
        tree = index.parse(path)
        if tree is None:
            continue
        ids = idents_of(tree)
        if "add_request_handler" not in ids and not any(k in ids for k in LOWLEVEL_V2_KWARGS):
            # 登録点は、名前の末尾が `add_request_handler` の呼び出しか `on_call_tool=` を持つ呼び出しだけ。
            # どちらの識別子も無いファイルは全ノードを歩かない（run21 の速度の退行。結果は同じ）
            continue
        rel = index.relpath(path)
        mod = index.module_name(path)
        mscope = index.module_scope(path)
        for node, encl in _calls_with_enclosing(tree):
            fname = dotted_of(node.func) or ""
            last = fname.split(".")[-1]
            handlers: list[ast.AST] = []
            sdk = False
            form = ""
            if last == "add_request_handler":
                method = node.args[0] if node.args else _kw(node, "method")
                if not (isinstance(method, ast.Constant) and method.value == LOWLEVEL_V2_REQUEST):
                    continue
                scope = _scope_at(index, path, mscope, encl)
                hkw = _kw(node, "handler")
                ptype = _kw(node, "params_type")
                if hkw is not None:
                    handlers = [hkw]
                    if ptype is None and len(node.args) >= 2:
                        ptype = node.args[1]
                elif len(node.args) >= 3:
                    if _is_sdk_call_tool_params(index, node.args[1], scope):
                        handlers = [node.args[-1]]  # SDK の (method, params_type, handler)
                        ptype = ptype if ptype is not None else node.args[1]
                    else:
                        handlers = [node.args[1], node.args[-1]]  # 自前の形。どちらが handler か決めない（ADV-2）
                elif len(node.args) == 2:
                    handlers = [node.args[1]]
                sdk = ptype is not None and _is_sdk_call_tool_params(index, ptype, scope)
                form = "add_request_handler"
            else:
                handler = None
                for kw in node.keywords:
                    if kw.arg in LOWLEVEL_V2_KWARGS:
                        handler = kw.value
                if handler is None:
                    continue
                resolved = resolve_call_name(node.func, _scope_at(index, path, mscope, encl))
                sdk = resolved in MCP_LOWLEVEL_SERVER_NAMES and _outside_tree(index, resolved)
                if last != "Server" and not sdk:
                    continue
                form = "on_call_tool"
                handlers = [handler]
            for h in handlers:
                out.append(
                    V2Registration(
                        relpath=rel,
                        module=mod,
                        lineno=getattr(node, "lineno", 0),
                        form=form,
                        handler=h,
                        handler_name=dotted_of(h),
                        sdk=sdk,
                        enclosing=encl,
                        col=getattr(node, "col_offset", 0),
                        alternatives=tuple(handlers),
                    )
                )
    out.sort(key=lambda r: (r.relpath, r.lineno, r.col, r.form))
    cache["all"] = out
    return out


def unresolved_handlers(index: SourceIndex) -> list[dict]:
    """handler が木の中の関数に解けない登録点（R2-r3-3、規則 4）。

    * dotted 名でない handler 式（`functools.partial(...)` / `lambda` など）。どの定義が呼ばれるかを名前で
      決められない。
    * dotted 名だが、import 表でも裸名一致でも関数の定義に 1 つも当たらないもの（D64 / U38 の敵対的レビュー
      ADV-2。自前の 3 引数形で候補の `args[1]` と `args[-1]` のどちらも当たらないときなど）。

    登録点ごとに、候補の**どれか 1 つでも**関数に解ければ数えない。ユニットにはならないので、**黙って落とさず**
    件数と位置を manifest の `unresolved_handler` に残す。判定は変えない。
    """
    order: list[tuple[str, int, int, str]] = []
    first: dict[tuple[str, int, int, str], V2Registration] = {}
    resolved: set[tuple[str, int, int, str]] = set()
    for r in lowlevel_v2_registrations(index):
        key = r.site()
        if key not in first:
            first[key] = r
            order.append(key)
        if r.handler_name is not None and _resolve_v2_handler(index, r)[0]:
            resolved.add(key)
    return [first[k].unresolved_json() for k in order if k not in resolved]


def _scope_at(index: SourceIndex, path: str, mscope: Scope, encl: tuple[ast.AST, ...]) -> Scope:
    """登録点で見える import 表（いちばん内側の関数の局所 import とモジュールの import）。"""
    for fn in reversed(encl):
        if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return index.function_scope(path, fn)
    return mscope


def _is_sdk_call_tool_params(index: SourceIndex, node: ast.AST, scope: Scope) -> bool:
    name = resolve_call_name(node, scope)
    if not name:
        return False
    return (
        name.split(".")[0] in _SDK_TYPE_PACKAGES
        and name.split(".")[-1] == _CALL_TOOL_PARAMS
        and _outside_tree(index, name)
    )


def _outside_tree(index: SourceIndex, dotted: str) -> bool:
    """dotted 名のモジュール部分が木の中に無い（外部のパッケージ = SDK そのもの）か。

    木の中に同じ名前のモジュール（`mcp/server/lowlevel.py` を持つ別物・SDK の fork）があれば、それが SDK と
    同じ呼び出し規約だとは言えないので SDK の裏付けにしない（種付けしない向き。D61 の改訂 G4 と同じ考え方）。
    """
    return index.resolve_module_strict(dotted.rpartition(".")[0]) is None


def _v2_params_arg(fn: ast.AST) -> Optional[str]:
    """SDK が `CallToolRequestParams` を渡す仮引数（第 2 位置。self / cls を除いて数える。名前によらない）。

    **デコレータ付きの定義には種付けしない。** 登録されるのはデコレータが返す関数で、定義の仮引数の並びは
    SDK の呼び出し規約と一致するとは限らない（検証役の反例 A3: `(ctx, params)` を `(name, arguments)` に
    変える装飾子）。位置引数が 2 つに満たないときも種付けしない。
    """
    if getattr(fn, "decorator_list", None):
        return None
    args = getattr(fn, "args", None)
    if args is None:
        return None
    positional = [a.arg for a in list(args.posonlyargs) + list(args.args) if a.arg not in ("self", "cls")]
    return positional[1] if len(positional) >= 2 else None


def _binds_locally(container: ast.AST, name: str) -> bool:
    """囲む関数の中で `name` が束縛されるか（関数の局所束縛・入れ子 def・lambda の仮引数）。"""
    if isinstance(container, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return name in _local_bindings(container)
    if isinstance(container, ast.Lambda):
        a = container.args
        return name in {x.arg for x in list(a.posonlyargs) + list(a.args) + list(a.kwonlyargs)} | {
            x.arg for x in (a.vararg, a.kwarg) if x is not None
        }
    return False


def _resolve_v2_handler(index: SourceIndex, reg: V2Registration) -> tuple[list[FuncDef], bool]:
    """登録された handler の定義（R2-r3-3）。

    1. **登録文のモジュールの import 表で一意に解けるとき**（D61 の改訂 G3 と同じ条件: モジュール直下の束縛が
       ちょうど 1 つで、関数の中で書き換えられない。import は `level` で厳密に解く）だけ、その定義 1 つに絞る。
       `from .handlers import handle` / 同じモジュールの `def handle` / `handlers.handle`（モジュールの別名）。
    2. 解けなければ**今までの裸名一致に落とす**（star import・条件つき import・関数の中の束縛など。落とさないと
       真の登録が消える。CLAUDE.md の落とし穴）。ただし §9.1 / O30 と同じく、**登録元がテストでなければ
       テストファイルの候補を外す**（どの Server にも登録されていない同名の test double を入口にしない）。

    :returns: `(候補, import 表で一意に解けたか)`
    """
    name = reg.handler_name or ""
    pinned = _pin_v2_handler(index, reg, name)
    if pinned is not None:
        return [pinned], True
    cands = index.lookup_function(name.split(".")[-1])
    if not is_test_path(reg.relpath):
        cands = [c for c in cands if not is_test_path(c.relpath)]
    return cands, False


def _is_direct_method(fd: FuncDef) -> bool:
    """クラス本体に直接書かれたメソッドか（メソッドの中の入れ子関数は含めない）。"""
    return fd.classname is not None and fd.qualname.rpartition(".")[0].split(".")[-1] == fd.classname


def _handler_form_matches(reg: V2Registration, fd: FuncDef) -> bool:
    """裸名一致で拾った定義が handler 式の形と合うか（種付けの条件。D64 / U38）。

    裸の名前 `h` がクラス本体のメソッドを指すことは無く、`x.h` は関数の中の入れ子 def を指さない。合わない
    定義は裸名一致の取り違え（別の同名の定義）なので、SDK の呼び出し規約を当てはめない（ユニットには今までどおりなる）。
    """
    if "." in (reg.handler_name or ""):
        return _is_direct_method(fd)
    return not _is_direct_method(fd)


def _pin_v2_handler(index: SourceIndex, reg: V2Registration, name: str) -> Optional[FuncDef]:
    from .val.engine import _module_bindings, _scan_module_writes

    parts = name.split(".")
    if len(parts) > 2 or not parts[0]:
        return None
    head = parts[0]
    for i, c in enumerate(reg.enclosing):
        if isinstance(c, ast.ClassDef):
            if i == len(reg.enclosing) - 1:
                return None  # クラス本体の名前空間は追わない（名前で決めない）
            continue  # メソッドの中からクラス本体の名前は見えない
        if _binds_locally(c, head):
            return None  # 関数の仮引数・局所変数・入れ子 def（名前だけでは決めない）
    path = index.resolve_module_path(reg.module)
    tree = index.parse(path) if path is not None else None
    if tree is None or index.module_name(path) != reg.module:
        return None
    if _has_star_import(tree):
        return None  # star import はどの名前も上書きしうる（敵対的レビュー ADV-1）
    binds = _module_bindings(tree, head)
    writes = _scan_module_writes(tree)
    if len(binds) != 1 or head in writes or "*" in writes:
        return None
    b = binds[0]
    if len(parts) == 1:
        if isinstance(b, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return _unique_module_def(index, reg.module, head)
        if isinstance(b, ast.ImportFrom) and b in tree.body:
            alias = next(a for a in b.names if (a.asname or a.name) == head)
            target = _import_from_base(index, reg.module, path, b)
            if target is None:
                return None
            return _pin_in_module(index, target, alias.name)
        return None
    # `m.h`: `m` がモジュールを指す import（`import pkg.m as m` / `from pkg import m`）のときだけ
    if b not in tree.body:
        return None
    target: Optional[str] = None
    if isinstance(b, ast.Import):
        alias = next(a for a in b.names if (a.asname or a.name.split(".")[0]) == head)
        if alias.asname is None and alias.name != head:
            return None  # `import pkg.m` は `pkg` を束縛する（2 段の名前は扱わない）
        target = _unique_module(index, alias.name)
        # `import pkg.m as m` も、pkg を import した後に属性 m を getattr で採る（無いときだけ sys.modules の
        # pkg.m。Python 3.7 以降の IMPORT_FROM）。`__init__.py` が m を束縛していればサブモジュールと決めない
        # （D64 / U38 の 3 巡目 RC-2。ADV-6 と同じ判定。絞るとスタブだけが残り本物のハンドラが消える誤 clear）。
        if target is not None and not _package_leaves_submodule(index, target, ignore=b):
            return None
    elif isinstance(b, ast.ImportFrom):
        alias = next(a for a in b.names if (a.asname or a.name) == head)
        if b.level == 0:
            target = _unique_module(index, f"{b.module}.{alias.name}" if b.module else alias.name)
        else:
            base = _import_from_base(index, reg.module, path, b, allow_package=True)
            if base is None:
                return None
            cand = f"{base}.{alias.name}"
            cpath = index.resolve_module_path(cand)
            target = cand if cpath is not None and index.module_name(cpath) == cand else None
        if target is not None and not _package_leaves_submodule(index, target, ignore=b):
            return None
    if target is None:
        return None
    return _pin_in_module(index, target, parts[1])


def _has_star_import(tree: ast.AST) -> bool:
    """モジュールのどこか（`if` / `try` の中を含む）に `from ... import *` があるか。

    star import は、それより前の def や import で束縛された名前を黙って上書きする（`def handle` の後の
    `try: from impl import *`、`__init__.py` の `from .base import h` の後の `from .override import *`）。
    `_module_bindings` は star を束縛として数えないので、star のあるモジュールでは名前を一意に絞らない
    （D64 / U38 の敵対的レビュー ADV-1。絞ると本物のハンドラのユニットが消える誤 clear になる）。順序を見て
    「def より前の star だけ」と判定するより、解かずに裸名一致に落とす方が安全。
    """
    return any(
        isinstance(n, ast.ImportFrom) and any(a.name == "*" for a in n.names) for n in ast.walk(tree)
    )


def _package_leaves_submodule(index: SourceIndex, submodule: str, ignore: Optional[ast.AST] = None) -> bool:
    """`from pkg import m` の `m` がサブモジュール `pkg.m` だと言えるか（D64 / U38 の敵対的レビュー ADV-6）。

    `from pkg import m` は、pkg の `__init__.py` を実行した後に**属性 m があればそれを採り**、無いときだけ
    サブモジュール pkg.m を import する（`importlib._bootstrap._handle_fromlist`。mcp 2.2.0 の環境で
    `from pkg import handlers; handlers.__name__ == "pkg.impl_v2.tools"` をレビュー役が確認）。
    したがって `__init__.py` が m を束縛する・star import がある・動的な名前空間操作（`globals()` など）がある・
    `__getattr__`（PEP 562）を持つときは、サブモジュールと決めない（呼び出し側は裸名一致に落とす）。
    `__init__.py` の無い名前空間パッケージはサブモジュール。`ignore` はその import 文自身（登録文が
    パッケージの `__init__.py` の中の `from . import m` のとき。その時点で属性 m はまだ無いのでサブモジュール）。
    """
    from .val.engine import _module_bindings, _scan_module_writes

    parent, _, name = submodule.rpartition(".")
    if not parent:
        return True
    ppath = index.resolve_module_path(parent)
    if ppath is None:
        return True
    if index.module_name(ppath) != parent or os.path.basename(ppath) != "__init__.py":
        return False  # 別のモジュールに当たった / パッケージでない（決めない）
    ptree = index.parse(ppath)
    if ptree is None or _has_star_import(ptree):
        return False
    if "*" in _scan_module_writes(ptree):
        return False
    binds = [x for x in _module_bindings(ptree, name) if x is not ignore]
    return not (binds or _module_bindings(ptree, "__getattr__"))


def _import_from_base(
    index: SourceIndex, module: str, path: str, imp: ast.ImportFrom, allow_package: bool = False
) -> Optional[str]:
    """`from X import ...` の X を木の中のモジュールの dotted 名に厳密に解く（`level` で。D61 の改訂 G3）。"""
    if imp.level > 0:
        base = module if os.path.basename(path) == "__init__.py" else module.rpartition(".")[0]
        for _ in range(imp.level - 1):
            base = base.rpartition(".")[0]
        if not imp.module:
            if not allow_package or not base:
                return None
            nxt = base
        else:
            nxt = f"{base}.{imp.module}" if base else imp.module
        npath = index.resolve_module_path(nxt)
        return nxt if npath is not None and index.module_name(npath) == nxt else None
    return _unique_module(index, imp.module) if imp.module else None


def _unique_module(index: SourceIndex, dotted: str) -> Optional[str]:
    """絶対 import の名前に当たる木の中のモジュールが**ちょうど 1 つ**ならその dotted 名。

    `resolve_module_strict` は名前が `.<import 名>` で終わるモジュールの 1 つを採るので、`a/handlers.py` と
    `b/handlers.py` があると `from handlers import h` の行き先を取り違えうる（どれが import されるかは sys.path
    で決まる）。取り違えたまま絞るとハンドラのユニットが消える（誤 clear）ので、2 つ以上あれば解かない。
    """
    cache = index.__dict__.setdefault("_authgap_module_names", {})
    if "all" not in cache:
        cache["all"] = sorted({index.module_name(p) for p in index.py_files()})
    hits = [m for m in cache["all"] if m == dotted or m.endswith("." + dotted)]
    return hits[0] if len(hits) == 1 else None


def _unique_module_def(index: SourceIndex, module: str, name: str) -> Optional[FuncDef]:
    defs = [f for f in index.lookup_function(name) if f.module == module and f.qualname == name and f.classname is None]
    return defs[0] if len(defs) == 1 else None


def _pin_in_module(index: SourceIndex, module: str, name: str, hops: int = 3) -> Optional[FuncDef]:
    """`module` で `name` がちょうど 1 回束縛され、それが def なら その定義。モジュール直下の
    `from ... import` の再公開なら同じ条件でたどる（D61 の改訂 G3）。それ以外は None。"""
    from .val.engine import _module_bindings, _scan_module_writes

    for _ in range(hops):
        path = index.resolve_module_path(module)
        tree = index.parse(path) if path is not None else None
        if tree is None or index.module_name(path) != module:
            return None
        if _has_star_import(tree):
            return None  # 再公開の連鎖の中の star import も上書きしうる（ADV-1）
        binds = _module_bindings(tree, name)
        writes = _scan_module_writes(tree)
        if len(binds) != 1 or name in writes or "*" in writes:
            return None
        b = binds[0]
        if isinstance(b, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return _unique_module_def(index, module, name)
        if not (isinstance(b, ast.ImportFrom) and b in tree.body):
            return None
        alias = next(a for a in b.names if (a.asname or a.name) == name)
        nxt = _import_from_base(index, module, path, b)
        if nxt is None:
            return None
        module, name = nxt, alias.name
    return None


# --------------------------------------------------------------------------
# mcp の主版（snake_case の注釈の読み方。D64 / U38、R2-r1-1）
# --------------------------------------------------------------------------

#: `>=2.0` にしか無い import（mcp 2.2.0: `mcp.server.mcpserver`、`mcp/server/__init__.py` の `MCPServer`）。
MCP_GE2_IMPORTS: tuple[str, ...] = ("mcp.server.mcpserver", "mcp.server.MCPServer")
#: `<2.0` にしか無い import（mcp 1.30.0: `mcp.server.fastmcp`、`mcp/server/__init__.py` の `FastMCP`。2.x では
#: `ModuleNotFoundError: This is mcp 2.x, where FastMCP was renamed to MCPServer`）。
MCP_LT2_IMPORTS: tuple[str, ...] = ("mcp.server.fastmcp", "mcp.server.FastMCP")


def _import_hits(dotted: str, prefixes: tuple[str, ...]) -> bool:
    return any(dotted == p or dotted.startswith(p + ".") for p in prefixes)


def _version_class(ge2: list[str], lt2: list[str]) -> str:
    """両方の向きの証拠があれば、またはどちらも無ければ ``unknown``（既定でどちらにも仮定しない。版規則 (4)）。"""
    if (ge2 and lt2) or not (ge2 or lt2):
        return "unknown"
    return "ge2" if ge2 else "lt2"


def _dir_is_within(d: str, anc: str) -> bool:
    """ディレクトリ `d`（木の根からの相対。根は ``""``）が `anc` と同じか、その下か。"""
    return anc == "" or d == anc or d.startswith(anc + os.sep)


@dataclass
class _McpVersions:
    """:func:`_mcp_versions` の結果（索引ごとに記憶化）。"""

    #: mcp / fastmcp の版の**票を持つ**依存記載のディレクトリ（木の根は ``""``）。票の無い依存記載
    #: （`httpx` だけの requirements.txt など）のディレクトリは含めない（D64 / U38 の 3 巡目 RC-1）。
    dep_dirs: tuple[str, ...]
    #: サブツリー（票を持つ依存記載のディレクトリ。そういう記載が 1 つも無い木は ``""``）→ `(版, 根拠)`。
    groups: dict[str, tuple[str, tuple[str, ...]]]
    #: 木全体で集めた根拠（manifest の `mcp_version.evidence`）。
    evidence: tuple[str, ...]

    def group_of(self, relpath: str) -> Optional[str]:
        """ファイルのサブツリー: **いちばん近い**、票を持つ祖先の依存記載のディレクトリ。

        票を持つ記載が無い木・そのディレクトリが 1 つだけの木は、木全体を 1 つのサブプロジェクトとみなす。
        記載が複数のディレクトリに分かれていて、どれの下にも無いファイルは None（どれで動くか決まらない）。
        """
        d = os.path.dirname(relpath)
        best: Optional[str] = None
        for dd in self.dep_dirs:
            if _dir_is_within(d, dd) and (best is None or len(dd) > len(best)):
                best = dd
        if best is not None:
            return best
        if len(self.dep_dirs) <= 1:
            return self.dep_dirs[0] if self.dep_dirs else ""
        return None


def _mcp_versions(index: SourceIndex) -> _McpVersions:  # noqa: C901
    """mcp の主版の証拠を集め、**依存の記載のサブツリーごと**に版を決める（D64 / U38、R2-r1-1 と ADV-3）。

    Def 6 の執行表と同じ **(1) API の形 → (2) 版の記載** の順の証拠（fix_outline）:

    * API の形で >=2.0: `mcp.server.mcpserver` の import、mcp SDK に解ける `Server(on_call_tool=)`、
      SDK の 3 引数形の `add_request_handler`。
    * API の形で <2.0: `mcp.server.fastmcp` の import、`@<x>.call_tool()`（低レベル v1。2.x に無い）。
    * 版の記載: :func:`enforcement.mcp_major_votes_by_file`（lock・`==`・`>=2`・`<2`・fastmcp の版。**ファイルごと**）。

    **版は木全体で 1 つに決めない**（ADV-3）。monorepo では、サブプロジェクトごとに別の環境（別の依存記載）で
    動く。ファイルのサブツリーは :meth:`_McpVersions.group_of`（いちばん近い、mcp / fastmcp の票を持つ
    依存記載のディレクトリ）。サブツリーの証拠は、そのサブツリーに属するファイルの API の形と、そのディレクトリ
    **と祖先**の依存記載の票（uv の workspace のように、根の lock がメンバーの環境を決める形を落とさない。
    祖先の票が食い違えば決めない）。

    **票の無い依存記載のディレクトリはサブツリーにしない**（D64 / U38 の 3 巡目 RC-1）。`httpx` だけの
    `tools/requirements.txt` は、mcp の環境が祖先と別であることを何も言わない。サブツリーにすると、祖先の票だけを
    受け継いで祖先のファイルの API の形を受け継がないので、祖先で食い違って決まらない版が子では決まってしまう
    （根の app にツールを登録する tools/ の snake_case が宣言になり、誤警報の矛が出た）。
    **祖先のサブツリーが食い違いで決まらなければ、子のサブツリーも決めない**（同 RC-1。子が自分の票を持つとき。
    子は祖先の票を受け継ぐが祖先の API の形を受け継がないので、祖先の食い違いを子で消さない）。

    **両方の向きの証拠があれば決めない**（移行用の shim・形と lock の食い違い。fix_outline 条件 (1)）。
    どちらの証拠も無ければ決めない。**既定でどちらにも仮定しない**（版規則 (4)）。
    """
    from .enforcement import mcp_major_votes_by_file

    cache = index.__dict__.setdefault("_authgap_mcp_version", {})
    if "v" in cache:
        return cache["v"]
    #: `(ファイルの相対パス, 向き, 根拠)`
    shapes: list[tuple[str, str, str]] = []
    for path in index.py_files():
        tree = index.parse(path)
        if tree is None:
            continue
        rel = index.relpath(path)
        for node in _import_nodes(tree):
            names: list[str] = []
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                names = [node.module] + [f"{node.module}.{a.name}" for a in node.names]
            for n in names:
                for pfx in MCP_GE2_IMPORTS:
                    if _import_hits(n, (pfx,)):
                        shapes.append((rel, "ge2", f"import:{rel}:{pfx}"))
                for pfx in MCP_LT2_IMPORTS:
                    if _import_hits(n, (pfx,)):
                        shapes.append((rel, "lt2", f"import:{rel}:{pfx}"))
    for reg in lowlevel_v2_registrations(index):
        if reg.sdk:
            shapes.append((reg.relpath, "ge2", f"shape:{reg.relpath}:{reg.lineno}:{reg.form}"))
    for fd in index.functions():
        for name, call, _node in _decorator_calls(fd.node):
            if call is not None and name.split(".")[-1] == "call_tool":
                shapes.append((fd.relpath, "lt2", f"shape:{fd.relpath}:{fd.qualname}:call_tool"))
    votes = mcp_major_votes_by_file(index.src_root)
    # 票を持つ依存記載のディレクトリだけをサブツリーの境界にする（RC-1）。
    dep_dirs = tuple(sorted({os.path.dirname(rel) for rel, _label, _vote in votes}))
    mv = _McpVersions(dep_dirs=dep_dirs, groups={}, evidence=())
    group_names = {mv.group_of(index.relpath(p)) for p in index.py_files()}
    group_names |= set(dep_dirs) if dep_dirs else {""}
    #: 食い違いで決まらないサブツリー（自分の証拠の食い違い、または祖先から受け継いだもの）。
    conflicted: set[str] = set()
    # 浅いサブツリーから決める（祖先の食い違いを先に知る）。
    for g in sorted((x for x in group_names if x is not None), key=lambda x: (x.count(os.sep) if x else -1, x)):
        ge2 = [lbl for rel, vote, lbl in shapes if vote == "ge2" and mv.group_of(rel) == g]
        lt2 = [lbl for rel, vote, lbl in shapes if vote == "lt2" and mv.group_of(rel) == g]
        for rel, label, vote in votes:
            if _dir_is_within(g, os.path.dirname(rel)):
                (ge2 if vote == "ge2" else lt2).append(label)
        ev = set(f"ge2:{x}" for x in ge2) | set(f"lt2:{x}" for x in lt2)
        cls = _version_class(ge2, lt2)
        if ge2 and lt2:
            conflicted.add(g)
        anc = sorted(a for a in conflicted if a != g and _dir_is_within(g, a))
        if anc:
            cls = "unknown"
            conflicted.add(g)
            ev |= {f"conflict_inherited_from:{a or '.'}" for a in anc}
        mv.groups[g] = (cls, tuple(sorted(ev)))
    pooled = {f"{vote}:{lbl}" for _rel, vote, lbl in shapes} | {f"{vote}:{label}" for _rel, label, vote in votes}
    if len(mv.groups) > 1 or None in group_names:
        pooled |= {f"subtree:{g or '.'}={cls}" for g, (cls, _ev) in mv.groups.items()}
        if None in group_names:
            pooled.add("subtree:<outside every subproject>=unknown")
    mv.evidence = tuple(sorted(pooled))
    cache["v"] = mv
    return mv


def _import_nodes(tree: ast.AST) -> tuple[ast.AST, ...]:
    """ファイルの import 文（関数・クラス・制御構文の中を含む）。**import は文なので式の中には現れない**ので、
    文の列（`body` / `orelse` / `finalbody` / `handlers` / `cases`）だけをたどる。木の AST に覚えておく。

    `_mcp_versions` は以前 `ast.walk` で全ノードを歩いていた（式のノードが大半。run21 の速度の退行）。集める
    import 文は同じ（順は違うが、呼び出し側は集合として使う）。
    """
    cached = tree.__dict__.get("_authgap_import_nodes")
    if cached is None:
        out: list[ast.AST] = []
        stack: list[ast.AST] = [tree]
        while stack:
            node = stack.pop()
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                out.append(node)
                continue
            for field_name in ("body", "orelse", "finalbody", "handlers", "cases"):
                sub = getattr(node, field_name, None)
                if isinstance(sub, list):
                    stack.extend(sub)
        cached = tree.__dict__["_authgap_import_nodes"] = tuple(out)
    return cached


def mcp_version_for(index: SourceIndex, relpath: str) -> str:
    """ファイル `relpath` の mcp の主版（``"ge2"`` / ``"lt2"`` / ``"unknown"``）。サブツリーごと（ADV-3）。"""
    mv = _mcp_versions(index)
    g = mv.group_of(relpath)
    if g is None or g not in mv.groups:
        return "unknown"
    return mv.groups[g][0]


def mcp_version_class(index: SourceIndex) -> tuple[str, tuple[str, ...]]:
    """木全体の mcp の主版と根拠（manifest の `mcp_version`、ファイルの分からない呼び出し側）。

    木の `.py` ファイルのサブツリーの版が**すべて同じ**ときだけその版、そうでなければ ``"unknown"``
    （どのサブツリーにも属さないファイルがあれば ``"unknown"``）。ユニットの宣言の読み方は、ファイルごとの
    :func:`mcp_version_for` を使う。
    """
    mv = _mcp_versions(index)
    classes = set()
    for p in index.py_files():
        g = mv.group_of(index.relpath(p))
        classes.add("unknown" if g is None else mv.groups.get(g, ("unknown", ()))[0])
    if not classes:
        classes = {cls for cls, _ev in mv.groups.values()}
    cls = classes.pop() if len(classes) == 1 else "unknown"
    return cls, mv.evidence


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
    #: 版が決まらないため読み方が決まらない snake_case のキー（:attr:`Unit.undetermined_fields`）。
    undetermined_fields: tuple[str, ...] = ()


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
        snake = mcp_version_for(index, rel)  # リテラルのファイルのサブツリーの版（D64 / U38 の ADV-3）
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
            ann, form, malformed, undetermined = _read_annotations(ann_node, snake)
            out.append(ToolLiteral(name, ann, form, malformed, rel, getattr(node, "lineno", 0), undetermined))
    out.sort(key=lambda t: (t.relpath, t.lineno))
    return out


def _read_annotations(
    node: Optional[ast.AST], snake: str = "lt2"
) -> tuple[Optional[dict], str, tuple[str, ...], tuple[str, ...]]:
    """注釈の式を `(値, 形, malformed, undetermined)` に読む。

    **snake_case のキー（`read_only_hint` ほか）の読み方は mcp の主版で決める**（D64 / U38、R2-r1-1。
    呼び出し側が注釈のファイルのサブツリーの版を :func:`mcp_version_for` で渡す。敵対的レビュー ADV-3）:

    * ``"ge2"``（mcp>=2.0）: `ToolAnnotations` の属性名そのもの（alias_generator=to_camel、validate_by_name）で、
      protocol には camelCase で届く（mcp 2.2.0 で `ToolAnnotations(read_only_hint=True).model_dump(by_alias=True)
      == {"readOnlyHint": True}`、辞書の `annotations={"read_only_hint": True}` も同じ）。**宣言として
      `SNAKE_ALIASES` で camelCase に写す。** 同じ注釈に camelCase もあれば camelCase が勝つ（2.2.0 で実測:
      `ToolAnnotations(readOnlyHint=True, read_only_hint=False)` → `{"readOnlyHint": True}`）。
    * ``"lt2"``（mcp<2.0）: `extra="allow"` で protocol のフィールドにならない → 今までどおり `D_malformed`
      （仕様書 322 行目、O27 / D48）。
    * ``"unknown"``: 版が決まらない → camelCase の対が無いキーは `undetermined`（`D_unknown`）。malformed にも
      宣言にもしない。camelCase の対があるキーはどちらの版でも宣言を変えない（2.x は camelCase が勝ち、1.x は
      無視される）ので載せない。
    """
    if node is None:
        return None, "absent", (), ()
    if isinstance(node, ast.Constant) and node.value is None:
        # **`annotations=None` は読める明示の「無い」**であり `⊥`。読めない形
        # （`D_unknown`）ではない。unreadable にすると同名ツールの `D_unknown` を
        # 過大に数える（野外 run 1 で 5 件）。
        return None, "absent", (), ()
    malformed: list[str] = []
    snake_values: dict[str, Any] = {}
    values: dict[str, Any] = {}

    def take(key: Optional[str], value_node: ast.AST) -> None:
        if key is None:
            return
        if key in SNAKE_ALIASES:
            if snake == "lt2":
                malformed.append(key)
                return
            try:
                snake_values[key] = ast.literal_eval(value_node)
            except (ValueError, TypeError, SyntaxError):
                snake_values[key] = _UNREAD
            return
        if key not in ANNOTATION_FIELDS:
            return  # 仕様外のフィールド（`category` 等）は D ではない
        try:
            values[key] = ast.literal_eval(value_node)
        except (ValueError, TypeError, SyntaxError):
            pass

    def finish(form: str) -> tuple[Optional[dict], str, tuple[str, ...], tuple[str, ...]]:
        undetermined: list[str] = []
        for key, v in sorted(snake_values.items()):
            camel = SNAKE_ALIASES[key]
            if camel in values:
                continue  # camelCase が勝つ（2.x）/ snake は無視される（1.x）。どちらの版でも宣言は同じ
            if snake == "ge2":
                if v is not _UNREAD:
                    values[camel] = v
            else:
                undetermined.append(key)
        return values, form, tuple(sorted(set(malformed))), tuple(undetermined)

    if isinstance(node, ast.Call):
        fname = dotted_of(node.func) or ""
        if fname.split(".")[-1] != "ToolAnnotations":
            return None, "unreadable", (), ()
        form = "ToolAnnotations"
        for kw in node.keywords:
            if kw.arg is None:  # ToolAnnotations(**{...})
                form = "unpack"
                if isinstance(kw.value, ast.Dict):
                    for k, v in zip(kw.value.keys, kw.value.values, strict=False):
                        if isinstance(k, ast.Constant) and isinstance(k.value, str):
                            take(k.value, v)
                else:
                    return None, "unreadable", (), ()
            else:
                take(kw.arg, kw.value)
        return finish(form)
    if isinstance(node, ast.Dict):
        for k, v in zip(node.keys, node.values, strict=False):
            if isinstance(k, ast.Constant) and isinstance(k.value, str):
                take(k.value, v)
        return finish("dict")
    return None, "unreadable", (), ()


#: snake_case のキーの値がリテラルとして読めなかった印（camelCase の値が読めないときと同じく値を入れない）。
_UNREAD = object()


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
            u.undetermined_fields = lit.undetermined_fields
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
                # 版が決まらない snake_case も同じく和（D64 / U38）。ツールごとにも持つ（`D_kind_by_tool`）。
                u.dispatch_undetermined = {n: by_name[n].undetermined_fields for n in hit if by_name[n].undetermined_fields}
                u.undetermined_fields = tuple(sorted({m for v in u.dispatch_undetermined.values() for m in v}))
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
