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
from dataclasses import dataclass, field
from typing import Any, Optional

from .catalog.entries import (
    ENTRY_RULES,
    LLM_CALLS,
    LOWLEVEL_V2_KWARGS,
    LOWLEVEL_V2_REQUEST,
    R2_EXCEPTIONS,
    TOOLMESSAGE_META_FIELDS,
    EntryRule,
)
from .srcindex import Scope, SourceIndex, dotted_of

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
    #: 低レベル経路のとき、ハンドラ内の name 分岐から得た候補名。
    dispatch_names: tuple[str, ...] = ()
    is_async: bool = False
    #: `toolmessage_handler` 形のとき、MODEL 値を運ぶ仮引数の名前（`msg`）。
    message_param: Optional[str] = None
    #: 同じく、`ToolMessage` 派生クラスの `(フィールド名, 注釈)`。
    message_fields: tuple[tuple[str, Optional[str]], ...] = ()
    #: 同じく、`ToolMessage` 派生クラス名。
    message_class: Optional[str] = None

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
        if self.dispatch_names:
            d["dispatch_names"] = list(self.dispatch_names)
        if self.message_param:
            d["message_param"] = self.message_param
            d["message_class"] = self.message_class
            d["message_fields"] = [[n, a] for n, a in self.message_fields]
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
            tool_name = _kwarg_str(call, "name") or fd.qualname.split(".")[-1]
            units.append(
                Unit(
                    framework=rule.framework,
                    entry_kind="decorator",
                    module=fd.module,
                    qualname=fd.qualname,
                    relpath=fd.relpath,
                    node=fd.node,
                    params=params_of(fd.node, rule.exclude_params),
                    tool_name=tool_name,
                    is_async=fd.is_async,
                )
            )
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
    units += find_tools_list_units(index, {u.qualname for u in units})
    units.sort(key=lambda u: (u.relpath, u.qualname, u.framework))
    return units


# --------------------------------------------------------------------------
# `tools=[...]` 形（フレームワーク横断）
# --------------------------------------------------------------------------


def find_tools_list_units(index: SourceIndex, already: frozenset[str] | set[str] = frozenset()) -> list[Unit]:
    """`Agent(tools=[f, g])` / `tools = [f, g]` の要素を入口にする。

    **木内のユーザ定義関数に一意に解決できる要素だけを採る。** 名前だけで
    拾うと同名の無関係な関数まで入口になり、母集団が膨らむ。
    """
    names: set[str] = set()
    for path in index.py_files():
        tree = index.parse(path)
        if tree is None:
            continue
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
                    names.add(n.split(".")[-1])
                elif isinstance(e, ast.Constant) and isinstance(e.value, str):
                    # `tools=["ast_grep_search", "ast_grep_rewrite"]` の文字列形。
                    names.add(e.value)

    out: list[Unit] = []
    seen: set[str] = set()
    for name in sorted(names):
        if name in already:
            continue
        fds = index.lookup_function(name)
        fds = [f for f in fds if f.qualname == name]
        if len(fds) != 1:
            continue  # 一意に解決できないものは採らない
        fd = fds[0]
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
        if key and key in by_name:
            lit = by_name[key]
            u.annotations = lit.annotations
            u.annotation_form = lit.form
            joined += 1
            used.add(key)
    unjoined = len([lit for lit in literals if not lit.name or lit.name not in used])
    return joined, unjoined


def scope_for(index: SourceIndex, unit: Unit) -> Optional[Scope]:
    path = index.resolve_module_path(unit.module)
    if path is None:
        return None
    return index.function_scope(path, unit.node)
