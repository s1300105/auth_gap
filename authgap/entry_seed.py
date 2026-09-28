"""入口の仮引数の注釈による種付けと lifespan の値（D64 / U23。所見 R4-r4-2, R4-r1-6, R4-r4-1）。

`analyze._seed` が作る既定の種（`seed_model_param`: 平らな MODEL の Atom）を、次の 3 つの場合だけ置き換える /
足す。**どれも解決できなければ何もしない（今日の種のまま）。** 注釈は宣言であって証明ではないので、
名前の解決は D61 の改訂の追記と同じ守り（先頭の名前がモジュール直下でちょうど 1 回束縛される、外部の型は
level 0 の import で木の外のモジュールを指す）を通す。

1. **pydantic / dataclass / NamedTuple の引数**（R4-r4-2）: 注釈が木内クラスに厳密に解け、クラスの家族
   （木内の基底をすべて含む）が `pydantic.BaseModel` / `@dataclass` / `typing.NamedTuple` で、**構築時フックが
   1 つも無い**ときだけ、`Obj((C,), fields)` を種にする。各フィールドは `MODEL / resolved`、root はフィールド
   ごと（`req.path`。主語一致 D25 / O34）。フックがある・外部の基底・二重束縛などでは今日どおり（`req.path` は
   MODEL に `opaque(unresolved)` を合流 → §9.3 で 不）。フレームワークが注釈どおりに構築することを確かめた
   入口（FastMCP: 公式 SDK / jlowin fastmcp。どちらも pydantic で引数を検証して構築する）だけに当てる。
2. **Path 注釈の引数**（R4-r1-6）: 注釈が `pathlib.Path` に厳密に解けるときだけ、形を `Path(base=...)` にする。
   主体・確度・root は変えない（`Path(path)` の構築と同じ形）。`Annotated[Path, ...]` は対象外（限界）。
3. **lifespan の yield 値**（R4-r4-1）: 装飾子の受け手名が指す自分の構築式（`FastMCP(...)` / `Server(...)`）が
   import 表で厳密に解け、`lifespan=` が木内の CM 関数名のときだけ、yield 値を `_opaque_deep`（型と主体は保ち、
   確度は opaque）で `ctx.request_context.lifespan_context` / `server.request_context.lifespan_context` に置く。
   lifespan_context は呼び出しをまたいで共有される可変オブジェクト（別のツールが書き込める）なので、起動時の
   定数を resolved で読まない（D17 改訂 4 / 5 と同じ規則。反例 ce_lifespan_rebound）。lifespan 本体の起動時の
   効果はツールに付けない（効果を集めない別のエンジンで評価する）。**型は受け手オブジェクトにだけ付け、葉の主体は
   直す前と同じく ctx 根の MODEL/opaque にする**（:func:`shared_state_view`。敵対的レビュー U23-A1: 別のツールが
   モデルの値を書き込める共有状態の葉を OP にすると、SELECT / INSERT の接頭辞の連結が 内 になった）。

敵対的レビュー（U23-P1 / P2 / P3 / S1）で足した守り: クラス体の代入で結ぶフック（`model_post_init = f`）と、読めない
クラス体の値（`_check: Any = field_validator(...)(f)`、名前で参照される記述子の既定値）はフック扱い。pydantic の
既定値つき `Final` はフィールドにしない。注釈の名前が入口を囲む関数 / クラスで束縛されうるとき、またはモジュールの
どこかで `global` 宣言されるときは解かない。
"""

from __future__ import annotations

import ast
from typing import Optional

from .ir import RESOLVED, Argv, Atom, Map, Obj, Path, Prin, Seq, Unknown, Value, opaque, prin_join, prov_merge
from .srcindex import FuncDef, SourceIndex, dotted_of

#: `pathlib` の具象パス型（注釈がこれに厳密に解けるときだけ Path 形にする）。
PATHLIB_TYPES = frozenset({"pathlib.Path", "pathlib.PosixPath", "pathlib.WindowsPath"})
#: pydantic のモデルの根。
PYDANTIC_ROOTS = frozenset(
    {"pydantic.BaseModel", "pydantic.main.BaseModel", "pydantic.v1.BaseModel", "pydantic.v1.main.BaseModel"}
)
#: `typing.NamedTuple`。
NAMEDTUPLE_ROOTS = frozenset({"typing.NamedTuple", "typing_extensions.NamedTuple"})
#: dataclass の装飾子（stdlib と pydantic）。
DATACLASS_DECORATORS = frozenset({"dataclasses.dataclass", "pydantic.dataclasses.dataclass"})
#: 注釈をほどく typing の構築子。
_OPTIONAL = frozenset({"typing.Optional", "typing_extensions.Optional"})
_UNION = frozenset({"typing.Union", "typing_extensions.Union"})
_ANNOTATED = frozenset({"typing.Annotated", "typing_extensions.Annotated"})
_LITERAL = frozenset({"typing.Literal", "typing_extensions.Literal"})
#: フィールドから外す注釈（モデルが埋めない）。
_NON_FIELD_ANNOTATIONS = frozenset(
    {"typing.ClassVar", "typing_extensions.ClassVar", "dataclasses.InitVar", "dataclasses.KW_ONLY"}
)
#: `Final`（pydantic の家族では既定値つきならクラス変数）。
_FINAL = frozenset({"typing.Final", "typing_extensions.Final"})
#: 引数を構築時に注釈どおりに検証・構築する入口（執行表の確認済み）。
_CONSTRUCTING_FRAMEWORKS = frozenset({"mcp", "fastmcp"})
#: 組込みの型名（モジュール直下で束縛されていなければ、そのまま型として読む）。
_BUILTIN_TYPES = frozenset(
    {"str", "int", "float", "bool", "bytes", "bytearray", "complex", "list", "dict", "tuple", "set", "frozenset",
     "object", "type", "None"}
)
#: 構築時に値を変えうるメソッド（どれか 1 つでも家族にあればフック）。
_HOOK_METHODS = frozenset(
    {
        "__init__",
        "__new__",
        "__post_init__",
        "model_post_init",
        "__pydantic_post_init__",
        "__setattr__",
        "__getattribute__",
        "__getattr__",
        "__init_subclass__",
        "__pydantic_init_subclass__",
        "__get_validators__",
        "model_validate",
        "model_validate_json",
        "model_validate_strings",
        "model_construct",
        "parse_obj",
        "parse_raw",
        "construct",
    }
)
#: 文字列を構築時に変える設定キー（pydantic v2 / v1）。
_TRANSFORM_CONFIG_KEYS = frozenset(
    {"str_to_lower", "str_to_upper", "str_strip_whitespace", "anystr_lower", "anystr_upper",
     "anystr_strip_whitespace", "coerce_numbers_to_str"}
)
#: FastMCP の構築子（公式 SDK / jlowin fastmcp）。
FASTMCP_CTORS = frozenset(
    {
        "mcp.server.fastmcp.FastMCP",
        "mcp.server.fastmcp.server.FastMCP",
        "fastmcp.FastMCP",
        "fastmcp.server.FastMCP",
        "fastmcp.server.server.FastMCP",
    }
)
#: 低レベル `Server` の構築子。
LOWLEVEL_CTORS = frozenset({"mcp.server.Server", "mcp.server.lowlevel.Server", "mcp.server.lowlevel.server.Server"})
#: FastMCP の `Context`。
CONTEXT_TYPES = frozenset(
    {
        "mcp.server.fastmcp.Context",
        "mcp.server.fastmcp.server.Context",
        "fastmcp.Context",
        "fastmcp.server.Context",
        "fastmcp.server.context.Context",
    }
)

_MAX_HOPS = 4


# --------------------------------------------------------------------------
# 名前の厳密な解決（D61 の改訂の追記と同じ守り）
# --------------------------------------------------------------------------


def _module_tree(index: SourceIndex, module: str) -> Optional[ast.Module]:
    path = index.resolve_module_path(module)
    if path is None or index.module_name(path) != module:
        return None
    return index.parse(path)


def _is_package(index: SourceIndex, module: str) -> bool:
    path = index.resolve_module_path(module)
    return path is not None and path.endswith("__init__.py")


def _relative_module(index: SourceIndex, module: str, level: int, name: Optional[str]) -> Optional[str]:
    """`from <level 個の点><name> import ...` が指す木内モジュール名（木の中に無ければ None）。"""
    parts = module.split(".") if module else []
    if not _is_package(index, module):
        parts = parts[:-1]
    drop = level - 1
    if drop > len(parts):
        return None
    if drop:
        parts = parts[: len(parts) - drop]
    base = ".".join(parts)
    target = f"{base}.{name}" if (base and name) else (name or base)
    if not target:
        return None
    path = index.resolve_module_path(target)
    return target if path is not None and index.module_name(path) == target else None


def _binding(scope_node: ast.AST, name: str) -> Optional[ast.AST]:
    """`scope_node` の本体で `name` を束縛する文が**ちょうど 1 つ**ならそれ（D61 の改訂 G3 の数え方）。"""
    from .val.engine import _module_bindings

    binds = _module_bindings(scope_node, name)
    return binds[0] if len(binds) == 1 else None


def resolve_name(index: SourceIndex, module: str, name: str, hops: int = 0) -> Optional[tuple[str, object]]:
    """モジュール直下でちょうど 1 回束縛される `name` の指す先。

    * `("def", (module, node))` — 木内の `class` / `def`
    * `("assign", (module, value))` — `name = value` / `name: T = value`
    * `("mod", module)` — 木内のモジュール
    * `("ext", dotted)` — **level 0 の import** で木の外を指す名前

    束縛が 0 / 2 以上、相対 import の外部、`*` import などは None（解決しない）。
    """
    if hops > _MAX_HOPS:
        return None
    cache = index.__dict__.setdefault("_authgap_entry_seed_names", {})
    key = (module, name)
    if key in cache:
        return cache[key]
    cache[key] = None  # 循環する import（a → b → a）を切る
    out = _resolve_name_uncached(index, module, name, hops)
    cache[key] = out
    return out


def _global_names(index: SourceIndex, module: str, tree: ast.AST) -> frozenset[str]:
    """モジュールのどこか（関数・クラスの本体の中を含む）で `global` 宣言される名前。"""
    cache = index.__dict__.setdefault("_authgap_entry_seed_globals", {})
    if module not in cache:
        cache[module] = frozenset(
            n for node in ast.walk(tree) if isinstance(node, ast.Global) for n in node.names
        )
    return cache[module]


def _resolve_name_uncached(index: SourceIndex, module: str, name: str, hops: int) -> Optional[tuple[str, object]]:
    tree = _module_tree(index, module)
    if tree is None:
        return None
    if name in _global_names(index, module, tree):
        # **関数の `global <名前>` はモジュールの束縛を差し替える**（U23-S1。D17 改訂 2 が名指しした穴）。
        # 以前はモジュール直下の束縛だけを数え、`def _harden(): global Req; class Req(...)` の差し替えを
        # 見落として、検証子つきのクラスのフィールドを resolved にしていた（誤警報）。
        return None
    b = _binding(tree, name)
    if b is None:
        return None
    if isinstance(b, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
        return ("def", (module, b))
    if isinstance(b, ast.Assign):
        if len(b.targets) == 1 and isinstance(b.targets[0], ast.Name):
            return ("assign", (module, b.value))
        return None
    if isinstance(b, ast.AnnAssign):
        if isinstance(b.target, ast.Name) and b.value is not None:
            return ("assign", (module, b.value))
        return None
    if isinstance(b, ast.Import):
        alias = next((a for a in b.names if (a.asname or a.name.split(".")[0]) == name), None)
        if alias is None:
            return None
        dotted = alias.name if alias.asname else alias.name.split(".")[0]
        strict = index.resolve_import_module(module, dotted)
        return ("mod", strict) if strict is not None else ("ext", dotted)
    if isinstance(b, ast.ImportFrom):
        alias = next((a for a in b.names if (a.asname or a.name) == name), None)
        if alias is None or alias.name == "*":
            return None
        if b.level > 0:
            src = _relative_module(index, module, b.level, b.module)
            if src is None:
                return None
        else:
            if not b.module:
                return None
            src = index.resolve_import_module(module, b.module)
            if src is None:
                return ("ext", f"{b.module}.{alias.name}")
        # 木内のモジュールから: そのモジュールの束縛をたどる（無ければサブモジュール）
        hit = resolve_name(index, src, alias.name, hops + 1)
        if hit is not None:
            return hit
        sub = f"{src}.{alias.name}"
        path = index.resolve_module_path(sub)
        return ("mod", sub) if path is not None and index.module_name(path) == sub else None
    return None


def resolve_expr(index: SourceIndex, module: str, node: ast.AST) -> Optional[tuple[str, object]]:
    """`Name` / `Attribute` の連鎖を :func:`resolve_name` と同じ規則で解決する。"""
    dotted = dotted_of(node)
    if dotted is None:
        return None
    head, *rest = dotted.split(".")
    cur = resolve_name(index, module, head)
    for attr in rest:
        if cur is None:
            return None
        kind, payload = cur
        if kind == "ext":
            cur = ("ext", f"{payload}.{attr}")
        elif kind == "mod":
            hit = resolve_name(index, str(payload), attr)
            if hit is None:
                sub = f"{payload}.{attr}"
                path = index.resolve_module_path(sub)
                hit = ("mod", sub) if path is not None and index.module_name(path) == sub else None
            cur = hit
        else:
            return None
    return cur


def _ext(r: Optional[tuple[str, object]]) -> Optional[str]:
    return str(r[1]) if r is not None and r[0] == "ext" else None


# --------------------------------------------------------------------------
# 注釈をほどく
# --------------------------------------------------------------------------


def _parse_str(node: ast.AST) -> Optional[ast.AST]:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        try:
            return ast.parse(node.value.strip(), mode="eval").body
        except SyntaxError:
            return None
    return node


def _field_call_ok(index: SourceIndex, module: str, node: ast.AST) -> bool:
    """`Field(...)`（pydantic）の呼び出しか。"""
    return isinstance(node, ast.Call) and _ext(resolve_expr(index, module, node.func)) in (
        "pydantic.Field",
        "pydantic.fields.Field",
    )


def unwrap_annotation(index: SourceIndex, module: str, ann: ast.AST) -> tuple[Optional[ast.AST], bool]:
    """文字列注釈・`Optional[X]` / `Union[X, None]` / `X | None` / `Annotated[X, ...]` をほどいた中身と、
    `Annotated` の付加情報が `Field(...)` / 文字列だけか（偽なら検証子などが付いている）。"""
    node = _parse_str(ann)
    clean = True
    for _ in range(6):
        if node is None:
            return None, clean
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
            sides = [x for x in (node.left, node.right) if not (isinstance(x, ast.Constant) and x.value is None)]
            if len(sides) != 1:
                return None, clean
            node = _parse_str(sides[0])
            continue
        if isinstance(node, ast.Subscript):
            head = _ext(resolve_expr(index, module, node.value))
            if head in _OPTIONAL:
                node = _parse_str(node.slice)
                continue
            if head in _UNION:
                elts = node.slice.elts if isinstance(node.slice, ast.Tuple) else [node.slice]
                sides = [x for x in elts if not (isinstance(x, ast.Constant) and x.value is None)]
                if len(sides) != 1:
                    return None, clean
                node = _parse_str(sides[0])
                continue
            if head in _ANNOTATED:
                elts = node.slice.elts if isinstance(node.slice, ast.Tuple) else [node.slice]
                if not elts:
                    return None, clean
                for meta in elts[1:]:
                    if isinstance(meta, ast.Constant) and isinstance(meta.value, str):
                        continue
                    if _field_call_ok(index, module, meta):
                        continue
                    clean = False
                node = _parse_str(elts[0])
                continue
        return node, clean
    return None, clean


# --------------------------------------------------------------------------
# クラスの家族とフック
# --------------------------------------------------------------------------


def _decorator_target(d: ast.AST) -> ast.AST:
    return d.func if isinstance(d, ast.Call) else d


def _tail(node: ast.AST) -> str:
    d = dotted_of(node)
    return d.split(".")[-1] if d else ""


def model_family(
    index: SourceIndex, module: str, cd: ast.ClassDef, depth: int = 0
) -> Optional[tuple[str, list[tuple[str, ast.ClassDef]]]]:
    """クラスが pydantic / dataclass / NamedTuple の家族なら `(種類, 基底が先の家族)`。

    基底はすべて木内のクラス（厳密に解けるもの）か、家族の根（`BaseModel` / `NamedTuple`）でなければならない。
    外部の基底・解けない基底・`Generic[T]` などの添字・`metaclass=`・dataclass 以外のクラス装飾子があれば None。
    """
    if depth > _MAX_HOPS:
        return None
    is_dc = False
    for d in cd.decorator_list:
        if _ext(resolve_expr(index, module, _decorator_target(d))) in DATACLASS_DECORATORS:
            is_dc = True
        else:
            return None
    for kw in cd.keywords:
        if kw.arg is None or kw.arg == "metaclass":
            return None
    kinds: set[str] = set()
    chain: list[tuple[str, ast.ClassDef]] = []
    for b in cd.bases:
        if isinstance(b, (ast.Subscript, ast.Call, ast.Starred)):
            return None
        r = resolve_expr(index, module, b)
        ext = _ext(r)
        if ext in PYDANTIC_ROOTS:
            kinds.add("pydantic")
        elif ext in NAMEDTUPLE_ROOTS:
            kinds.add("namedtuple")
        elif r is not None and r[0] == "def" and isinstance(r[1][1], ast.ClassDef):  # type: ignore[index]
            bmod, bnode = r[1]  # type: ignore[misc]
            sub = model_family(index, bmod, bnode, depth + 1)
            if sub is None:
                return None
            kinds.add(sub[0])
            for item in sub[1]:
                if all(item[1] is not c[1] for c in chain):
                    chain.append(item)
        else:
            return None
    chain.append((module, cd))
    if is_dc:
        # dataclass: 基底も dataclass だけ（木内）。外部の根は持たない
        if kinds - {"dataclass"}:
            return None
        return "dataclass", chain
    if kinds == {"pydantic"}:
        return "pydantic", chain
    if (
        kinds == {"namedtuple"}
        and depth == 0
        and len(cd.bases) == 1
        and _ext(resolve_expr(index, module, cd.bases[0])) in NAMEDTUPLE_ROOTS
    ):
        return "namedtuple", chain
    return None


def _config_transforms(node: ast.AST) -> bool:
    """設定（`model_config = ConfigDict(...)` / `{...}` / `class Config:`）が文字列を変えるキーを持つか。
    `**shared` の展開・`*args` のように中身が読めない設定も真（今日どおり）。"""
    for n in ast.walk(node):
        if isinstance(n, ast.keyword) and n.arg is None:
            return True
        if isinstance(n, ast.Starred) or (isinstance(n, ast.Dict) and any(k is None for k in n.keys)):
            return True
        if isinstance(n, ast.keyword) and n.arg in _TRANSFORM_CONFIG_KEYS:
            return True
        if isinstance(n, ast.Constant) and isinstance(n.value, str) and n.value in _TRANSFORM_CONFIG_KEYS:
            return True
        if isinstance(n, ast.Name) and n.id in _TRANSFORM_CONFIG_KEYS:
            return True
    return False


def _annotation_hooked(
    index: SourceIndex, module: str, ann: ast.AST, depth: int = 0, seen: frozenset = frozenset()
) -> bool:
    """フィールドの注釈が構築時に値を変えうるもの（`Annotated` の検証子・`constr(...)` のような呼び出し・
    検証子を含む木内の型別名・フックを持つ木内クラス・解けない名前）を含むか。**解けないものはフック扱い**（今日どおり）。"""
    if depth > _MAX_HOPS:
        return True
    node = _parse_str(ann)
    if node is None:
        return True
    return _expr_hooked(index, module, node, depth, seen)


def _expr_hooked(index: SourceIndex, module: str, node: ast.AST, depth: int, seen: frozenset) -> bool:
    if isinstance(node, ast.Constant):
        if isinstance(node.value, str):
            return _annotation_hooked(index, module, node, depth + 1, seen)
        return False
    if isinstance(node, (ast.Name, ast.Attribute)):
        dotted = dotted_of(node)
        if dotted is None:
            return True
        if dotted in _BUILTIN_TYPES:
            from .val.engine import _module_bindings

            tree = _module_tree(index, module)
            if tree is not None and not _module_bindings(tree, dotted):
                return False
        r = resolve_expr(index, module, node)
        if r is None:
            return True
        kind, payload = r
        if kind == "ext":
            return str(payload).split(".")[-1].endswith("Validator")
        if kind == "assign":
            amod, value = payload  # type: ignore[misc]
            return _annotation_hooked(index, amod, value, depth + 1, seen)
        if kind == "def":
            dmod, dnode = payload  # type: ignore[misc]
            if not isinstance(dnode, ast.ClassDef):
                return True
            return class_hooked(index, dmod, dnode, depth + 1, seen)
        return True
    if isinstance(node, ast.Subscript):
        head = _ext(resolve_expr(index, module, node.value))
        if head in _LITERAL:
            return False
        if head in _ANNOTATED:
            elts = node.slice.elts if isinstance(node.slice, ast.Tuple) else [node.slice]
            for meta in elts[1:]:
                if isinstance(meta, ast.Constant) and isinstance(meta.value, str):
                    continue
                if not _field_call_ok(index, module, meta):
                    return True
            return not elts or _expr_hooked(index, module, elts[0], depth, seen)
        if _expr_hooked(index, module, node.value, depth, seen):
            return True
        return _expr_hooked(index, module, node.slice, depth, seen)
    if isinstance(node, (ast.Tuple, ast.List)):
        return any(_expr_hooked(index, module, e, depth, seen) for e in node.elts)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        return _expr_hooked(index, module, node.left, depth, seen) or _expr_hooked(
            index, module, node.right, depth, seen
        )
    # 呼び出し（`constr(...)` など）やその他の式
    return True


def _own_hooks(index: SourceIndex, module: str, cd: ast.ClassDef, depth: int, seen: frozenset) -> bool:
    """クラス本体（家族の 1 つ）に構築時フックがあるか。"""
    fam = model_family(index, module, cd)
    pydantic = fam is not None and fam[0] == "pydantic"
    for kw in cd.keywords:
        if kw.arg in _TRANSFORM_CONFIG_KEYS:
            return True
    for d in cd.decorator_list:
        # `@dataclass(init=False)` / pydantic dataclass の `config=`（文字列の変換を含みうる）
        if isinstance(d, ast.Call) and any(kw.arg in ("init", "config") or kw.arg is None for kw in d.keywords):
            return True
    for st in cd.body:
        if isinstance(st, ast.Pass) or (
            isinstance(st, ast.Expr) and isinstance(st.value, ast.Constant) and isinstance(st.value.value, str)
        ):
            continue
        if not isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Assign, ast.AnnAssign)):
            # `if PYDANTIC_V2: @field_validator ... else: @validator ...` のような条件つきの定義・クラス体の
            # 呼び出しは読み切れない: フック扱い（今日どおり）
            return True
        if isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if st.name in _HOOK_METHODS or st.name.startswith("__get_pydantic"):
                return True
            for d in st.decorator_list:
                if not _safe_method_decorator(index, module, d):
                    return True
        elif isinstance(st, ast.ClassDef) and st.name == "Config":
            if _config_transforms(st):
                return True
        elif isinstance(st, (ast.Assign, ast.AnnAssign)):
            targets = st.targets if isinstance(st, ast.Assign) else [st.target]
            names = [n.id for t in targets for n in ast.walk(t) if isinstance(n, ast.Name)]
            # **フックの名前に代入で結ぶ形**（`model_post_init = _post` / `__post_init__ = _post`。U23-P1）。
            # pydantic / dataclasses は名前で引くので、def で定義したときと同じく登録される。以前は
            # FunctionDef の名前しか見ず、フィールドを resolved にしていた（誤警報）
            if any(n in _HOOK_METHODS or n.startswith("__get_pydantic") for n in names):
                return True
            if "model_config" in names:
                value = st.value
                if value is None or not isinstance(value, (ast.Call, ast.Dict)) or _config_transforms(value):
                    return True
                continue
            # **クラス体の値は、読める静的な値でなければフック扱い**（U23-P1 / P3）。`_check: Any =
            # field_validator("path")(f)` のように `_` 始まりや ClassVar の注釈つき代入に置いた検証子も
            # pydantic は登録する（以前は除外フィールドの検査を先にして見落とした）。名前で参照される既定値
            # （`path: str = CONF`）は記述子かもしれない（dataclass は `__set__` を構築時に呼ぶ）。
            # 除外フィールドかどうかの判定より**前に**見る
            if st.value is not None and not _static_class_value(index, module, st.value, pydantic=pydantic):
                return True
            if isinstance(st, ast.Assign):
                continue
            if names and not _excluded_field(index, module, st):
                if _annotation_hooked(index, module, st.annotation, depth + 1, seen):
                    return True
    return False


#: フィールドの既定値として読んでよい構築子（値を変えない）。
_FIELD_FACTORIES = frozenset(
    {
        "dataclasses.field",
        "pydantic.Field",
        "pydantic.fields.Field",
        "pydantic.PrivateAttr",
        "pydantic.fields.PrivateAttr",
    }
)


def _literal(node: ast.AST) -> bool:
    """リテラル（定数・定数の単項演算・リテラルだけのタプル / リスト / 集合 / 辞書）か。"""
    if isinstance(node, ast.Constant):
        return True
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
        return isinstance(node.operand, ast.Constant)
    if isinstance(node, (ast.Tuple, ast.List, ast.Set)):
        return all(_literal(e) for e in node.elts)
    if isinstance(node, ast.Dict):
        return all(k is not None and _literal(k) for k in node.keys) and all(_literal(v) for v in node.values)
    return False


#: pydantic の `Field(...)` / `PrivateAttr(...)` の文書だけの引数（検証される値を変えない。U23-R2）。
_DOC_ONLY_FIELD_KWARGS = frozenset(
    {"description", "title", "examples", "json_schema_extra", "alias", "serialization_alias"}
)
#: pydantic の `Field` / `PrivateAttr`（文書だけの引数を検査しない構築子）。
_PYDANTIC_FIELD_FACTORIES = frozenset(
    {"pydantic.Field", "pydantic.fields.Field", "pydantic.PrivateAttr", "pydantic.fields.PrivateAttr"}
)
#: Enum の根。
_ENUM_ROOTS = frozenset({"enum.Enum", "enum.IntEnum", "enum.StrEnum", "enum.Flag", "enum.IntFlag"})
#: Enum のメンバーを記述子にしうる（またはクラス属性に置いたときに呼ばれる）メソッド。
_DESCRIPTOR_METHODS = frozenset({"__get__", "__set__", "__delete__", "__set_name__"})


def _enum_class_ok(index: SourceIndex, module: str, cd: ast.ClassDef, depth: int = 0) -> Optional[bool]:
    """木内の Enum クラス（とその木内の基底）が記述子のメソッドを持たず、読める形か。読めなければ None、
    読めれば「Enum の根を持つか」。"""
    if depth > _MAX_HOPS or cd.keywords or cd.name in _patched_class_names(index):
        return None
    for d in cd.decorator_list:
        if _ext(resolve_expr(index, module, d)) != "enum.unique":
            return None
    for st in cd.body:
        if isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef)) and st.name in _DESCRIPTOR_METHODS:
            return None
        if isinstance(st, (ast.Assign, ast.AnnAssign)):
            targets = st.targets if isinstance(st, ast.Assign) else [st.target]
            if any(isinstance(n, ast.Name) and n.id in _DESCRIPTOR_METHODS for t in targets for n in ast.walk(t)):
                return None
    rooted = False
    for b in cd.bases:
        if isinstance(b, ast.Name) and b.id in _BUILTIN_TYPES:
            from .val.engine import _module_bindings

            tree = _module_tree(index, module)
            if tree is not None and not _module_bindings(tree, b.id):
                continue
        r = resolve_expr(index, module, b)
        if _ext(r) in _ENUM_ROOTS:
            rooted = True
            continue
        if r is not None and r[0] == "def" and isinstance(r[1][1], ast.ClassDef):  # type: ignore[index]
            bmod, bnode = r[1]  # type: ignore[misc]
            sub = _enum_class_ok(index, bmod, bnode, depth + 1)
            if sub is None:
                return None
            rooted = rooted or sub
            continue
        return None
    return rooted


def _enum_member(index: SourceIndex, module: str, node: ast.AST) -> bool:
    """`node` が木内の Enum クラス（`__get__` / `__set__` などを定義しない）の**メンバー**（クラス本体の直下で
    ちょうど 1 回、リテラルか `enum.auto()` に束縛される `_` 始まりでない名前）の参照か（U23-R2）。"""
    if not isinstance(node, ast.Attribute) or node.attr.startswith("_"):
        return False
    r = resolve_expr(index, module, node.value)
    if r is None or r[0] != "def" or not isinstance(r[1][1], ast.ClassDef):  # type: ignore[index]
        return False
    cmod, cd = r[1]  # type: ignore[misc]
    if not _enum_class_ok(index, cmod, cd):
        return False
    from .val.engine import _module_bindings

    binds = _module_bindings(cd, node.attr)
    if len(binds) != 1 or not any(st is binds[0] for st in cd.body):
        return False
    b = binds[0]
    if not (isinstance(b, ast.Assign) and len(b.targets) == 1 and isinstance(b.targets[0], ast.Name)):
        return False
    v = b.value
    if _literal(v):
        return True
    return (
        isinstance(v, ast.Call)
        and not v.args
        and not v.keywords
        and _ext(resolve_expr(index, cmod, v.func)) == "enum.auto"
    )


def _static_class_value(index: SourceIndex, module: str, node: ast.AST, hops: int = 0, pydantic: bool = False) -> bool:
    """クラス体の代入の値が、構築時に値を変えるもの（記述子・検証子の登録）ではないと**読める**か。

    読めるのは、リテラル、モジュール直下でちょうど 1 回リテラルに束縛される名前、`Field(...)` /
    `PrivateAttr(...)` / `dataclasses.field(...)` で引数が同じく読めるもの（`default_factory=` は呼び出し可能な
    値の参照なのでクラス属性の記述子にはならない）。それ以外（呼び出し・名前で参照されるオブジェクト・
    属性・解けない名前）は偽（フック扱い = 今日どおり）。

    `pydantic` が真（クラスが pydantic の家族）のときだけ（U23-R2）:

    * `Field(...)` / `PrivateAttr(...)` の文書だけの引数（description / title / examples / json_schema_extra /
      alias / serialization_alias）は検査しない。以前は `Field(description=f"file under {ROOT}")` の f 文字列で
      クラス全体をフック扱いにし、D2 の矛を不に落としていた（件数の欠落）。
    * 木内の Enum クラス（記述子のメソッドを持たない）のメンバーは既定値として読める。
    dataclass の既定値の規則（`__set__` を構築時に呼ぶ記述子の恐れ）は変えない。
    """
    if hops > _MAX_HOPS:
        return False
    if _literal(node):
        return True
    if isinstance(node, (ast.Name, ast.Attribute)):
        r = resolve_expr(index, module, node)
        if r is not None and r[0] == "assign":
            amod, value = r[1]  # type: ignore[misc]
            return _static_class_value(index, amod, value, hops + 1, pydantic) and not isinstance(value, ast.Call)
        if pydantic and _enum_member(index, module, node):
            return True
        return False
    factory = _ext(resolve_expr(index, module, node.func)) if isinstance(node, ast.Call) else None
    if factory in _FIELD_FACTORIES:
        doc_ok = pydantic and factory in _PYDANTIC_FIELD_FACTORIES
        for a in node.args:  # type: ignore[union-attr]
            if isinstance(a, ast.Starred) or not _static_class_value(index, module, a, hops + 1, pydantic):
                return False
        for kw in node.keywords:  # type: ignore[union-attr]
            if kw.arg is None:
                return False
            if kw.arg == "default_factory":
                if isinstance(kw.value, (ast.Name, ast.Attribute, ast.Lambda)):
                    continue
                return False
            if doc_ok and kw.arg in _DOC_ONLY_FIELD_KWARGS:
                continue
            if not _static_class_value(index, module, kw.value, hops + 1, pydantic):
                return False
        return True
    return False


#: 構築時に値を変えないメソッドの装飾子。**これ以外の装飾子はフック扱い**（別名 import の `field_validator`・
#: 木内の包み関数も含めて読めないものは今日どおりにする）。
_SAFE_METHOD_DECORATORS = frozenset(
    {
        "builtins.property",
        "builtins.classmethod",
        "builtins.staticmethod",
        "functools.cached_property",
        "abc.abstractmethod",
        "typing.override",
        "typing_extensions.override",
        "pydantic.computed_field",
        "pydantic.field_serializer",
        "pydantic.model_serializer",
    }
)


def _safe_method_decorator(index: SourceIndex, module: str, d: ast.AST) -> bool:
    target = _decorator_target(d)
    if isinstance(target, ast.Name) and target.id in ("property", "classmethod", "staticmethod"):
        from .val.engine import _module_bindings

        tree = _module_tree(index, module)
        if tree is not None and not _module_bindings(tree, target.id):
            return True
    if isinstance(target, ast.Attribute) and target.attr in ("setter", "getter", "deleter"):
        return False  # `@x.setter` は代入時に値を変える
    return _ext(resolve_expr(index, module, target)) in _SAFE_METHOD_DECORATORS


def class_hooked(
    index: SourceIndex, module: str, cd: ast.ClassDef, depth: int = 0, seen: frozenset = frozenset()
) -> bool:
    """クラスとその木内の基底（厳密に解けるもの）のどれかに構築時フックがあるか。

    自己参照（`children: list["Node"]`）は、調べている途中のクラスに戻ったら「そこでは新しいフックなし」とする
    （そのクラス自身の本体は外側の呼び出しが調べる）。"""
    key = (module, cd.name, cd.lineno)
    if key in seen:
        return False
    if depth > _MAX_HOPS:
        return True
    seen = seen | {key}
    if _own_hooks(index, module, cd, depth, seen) or cd.name in _patched_class_names(index):
        return True
    for b in cd.bases:
        r = resolve_expr(index, module, b) if not isinstance(b, ast.Subscript) else None
        if r is not None and r[0] == "def" and isinstance(r[1][1], ast.ClassDef):  # type: ignore[index]
            bmod, bnode = r[1]  # type: ignore[misc]
            if class_hooked(index, bmod, bnode, depth + 1, seen):
                return True
    return False


def _patched_class_names(index: SourceIndex) -> frozenset[str]:
    """木のどこかで `C.<attr> = ...` / `setattr(C, ...)` と、クラスの外から書き換えられる名前（末尾名。保守的に
    名前だけで見る）。`Req.model_post_init = f` のような後付けのフックを読み落とさないため。"""
    cache = index.__dict__
    if "_authgap_patched_classes" not in cache:
        out: set[str] = set()
        for path in index.py_files():
            tree = index.parse(path)
            if tree is None:
                continue
            for n in ast.walk(tree):
                if isinstance(n, ast.Attribute) and isinstance(n.ctx, (ast.Store, ast.Del)):
                    d = dotted_of(n.value)
                    if d and d.split(".")[0] not in ("self", "cls"):
                        out.add(d.split(".")[-1])
                elif isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in ("setattr", "delattr"):
                    if n.args:
                        d = dotted_of(n.args[0])
                        if d:
                            out.add(d.split(".")[-1])
        cache["_authgap_patched_classes"] = frozenset(out)
    return cache["_authgap_patched_classes"]


def _excluded_field(index: SourceIndex, module: str, st: ast.AnnAssign, kind: Optional[str] = None) -> bool:
    """モデルが埋めるフィールドではないもの（`_` 始まり・`ClassVar` / `InitVar`・`PrivateAttr`・`init=False`、
    pydantic の家族では既定値つきの `Final`）。`kind` は家族の種類（分からなければ None）。"""
    if not isinstance(st.target, ast.Name) or st.target.id.startswith("_"):
        return True
    ann = _parse_str(st.annotation)
    head = ann.value if isinstance(ann, ast.Subscript) else ann
    if head is not None and (
        _ext(resolve_expr(index, module, head)) in _NON_FIELD_ANNOTATIONS
        or _tail(head) in ("ClassVar", "InitVar", "KW_ONLY")
    ):
        return True
    if (
        kind == "pydantic"
        and st.value is not None
        and head is not None
        and (_ext(resolve_expr(index, module, head)) in _FINAL or _tail(head) == "Final")
    ):
        # **pydantic は既定値つきの `Final` をクラス変数として扱う**（model_fields に入らない。U23-P2）。
        # 以前はフィールドとして MODEL/resolved にし、OP の定数 FIXED を開く書き込みを矛にしていた（誤警報）。
        # dataclass / NamedTuple では既定値つきの Final も init の引数（フィールド）のまま
        return True
    v = st.value
    if isinstance(v, ast.Call):
        if _tail(v.func) == "PrivateAttr":
            return True
        for kw in v.keywords:
            if kw.arg == "init" and not (isinstance(kw.value, ast.Constant) and kw.value.value is True):
                return True
    return False


def _family_fields(
    index: SourceIndex, chain: list[tuple[str, ast.ClassDef]], kind: Optional[str] = None
) -> list[tuple[str, str, ast.AST]]:
    """家族のフィールド `(名前, 定義したモジュール, 注釈)`。基底が先、同名は後の定義が勝つ。
    同じ名前が家族のどこかで `def` / 注釈なしの代入としても束縛されるフィールドは外す（property など）。"""
    fields: dict[str, tuple[str, ast.AST]] = {}
    other: set[str] = set()
    for mod, cd in chain:
        for st in cd.body:
            if isinstance(st, ast.AnnAssign):
                if _excluded_field(index, mod, st, kind):
                    if isinstance(st.target, ast.Name):
                        other.add(st.target.id)
                    continue
                fields[st.target.id] = (mod, st.annotation)  # type: ignore[union-attr]
            elif isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                other.add(st.name)
            elif isinstance(st, ast.Assign):
                for t in st.targets:
                    for n in ast.walk(t):
                        if isinstance(n, ast.Name):
                            other.add(n.id)
    return [(name, mod, ann) for name, (mod, ann) in fields.items() if name not in other]


# --------------------------------------------------------------------------
# 種
# --------------------------------------------------------------------------


def _model_value(root: str, shape) -> Value:
    return Value(Prin.MODEL, RESOLVED, shape, frozenset(), frozenset({root}))


def _typed_seed(
    index: SourceIndex, module: str, ann: ast.AST, root: str, depth: int, models_ok: bool
) -> Optional[Value]:
    """注釈から作る MODEL の種。作れなければ None（呼び出し側が今日の種を使う）。"""
    node, clean = unwrap_annotation(index, module, ann)
    if node is None or not isinstance(node, (ast.Name, ast.Attribute)):
        return None
    r = resolve_expr(index, module, node)
    if r is None:
        return None
    if _ext(r) in PATHLIB_TYPES:
        if not _plain_optional(index, module, ann):
            return None  # `Annotated[Path, ...]` は対象外（限界）
        return _model_value(root, Path(base=_model_value(root, Atom(formal=root))))
    if not models_ok or not clean or r[0] != "def" or depth >= 2:
        return None
    cmod, cnode = r[1]  # type: ignore[misc]
    if not isinstance(cnode, ast.ClassDef):
        return None
    fam = model_family(index, cmod, cnode)
    if fam is None or class_hooked(index, cmod, cnode):
        return None
    fields: list[tuple[str, Value]] = []
    for fname, fmod, fann in _family_fields(index, fam[1], fam[0]):
        froot = f"{root}.{fname}"
        v = _typed_seed(index, fmod, fann, froot, depth + 1, models_ok)
        if v is None:
            from .val.engine import seed_model_param

            try:
                text = ast.unparse(fann)
            except Exception:  # pragma: no cover
                text = None
            v = seed_model_param(froot, froot, text)
        fields.append((fname, v))
    return _model_value(root, Obj((cnode.name,), tuple(sorted(fields))))


def _plain_optional(index: SourceIndex, module: str, ann: ast.AST) -> bool:
    """注釈が `Annotated` を含まず、`Optional` / `| None` / 文字列だけでほどけるか。"""
    node = _parse_str(ann)
    for _ in range(6):
        if node is None:
            return False
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
            sides = [x for x in (node.left, node.right) if not (isinstance(x, ast.Constant) and x.value is None)]
            node = _parse_str(sides[0]) if len(sides) == 1 else None
            continue
        if isinstance(node, ast.Subscript):
            head = _ext(resolve_expr(index, module, node.value))
            if head in _OPTIONAL:
                node = _parse_str(node.slice)
                continue
            if head in _UNION:
                elts = node.slice.elts if isinstance(node.slice, ast.Tuple) else [node.slice]
                sides = [x for x in elts if not (isinstance(x, ast.Constant) and x.value is None)]
                node = _parse_str(sides[0]) if len(sides) == 1 else None
                continue
            return False
        return isinstance(node, (ast.Name, ast.Attribute))
    return False


def _arg_nodes(fn: ast.AST) -> dict[str, ast.arg]:
    args = getattr(fn, "args", None)
    if args is None:
        return {}
    return {a.arg: a for a in list(args.posonlyargs) + list(args.args) + list(args.kwonlyargs)}


def _parent_map(index: SourceIndex, module: str, tree: ast.AST) -> dict[int, ast.AST]:
    cache = index.__dict__.setdefault("_authgap_entry_seed_parents", {})
    if module not in cache:
        pm: dict[int, ast.AST] = {}
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                pm[id(child)] = node
        cache[module] = pm
    return cache[module]


def _enclosing_scopes(index: SourceIndex, unit) -> Optional[list[ast.AST]]:
    """入口の定義を囲む関数 / クラス（内側が先）。モジュールの木の中に見つからなければ None。"""
    tree = _module_tree(index, unit.module)
    if tree is None:
        return None
    pm = _parent_map(index, unit.module, tree)
    out: list[ast.AST] = []
    cur = unit.node
    while True:
        par = pm.get(id(cur))
        if par is None:
            return None
        if par is tree:
            return out
        if isinstance(par, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
            out.append(par)
        cur = par


def _binders(index: SourceIndex, scope: ast.AST) -> dict[str, list[ast.AST]]:
    """スコープ（関数 / クラス）の中で名前を束縛しうるノード（名前 → ノードの列）。

    * 関数: **入れ子の本体も含めて保守的に**数える（仮引数・代入先・def / class・import・`global` /
      `nonlocal`・except / match の名前）。入れ子の関数の `nonlocal` や局所も束縛として数える（今どおり）。
    * クラス: **クラス本体の直下の束縛だけ**（U23-R1）。メソッド / 入れ子のクラスの本体の中の局所は、
      クラスの中の注釈の評価に使われない（Python はクラスのスコープから入れ子の関数の局所を見ない）。
      入れ子の def / class の名前・装飾子・既定値・基底はクラス本体で評価されるので数える。

    AST は `SourceIndex` の parse の結果（同じオブジェクトが保たれる）なので、スコープごとに覚えておく
    （入口ごとに同じ関数を歩き直していた遅さも消える）。"""
    cache = index.__dict__.setdefault("_authgap_entry_seed_binders", {})
    hit = cache.get(id(scope))
    if hit is not None and hit[0] is scope:
        return hit[1]
    out: dict[str, list[ast.AST]] = {}

    def add(name: str, node: ast.AST) -> None:
        out.setdefault(name, []).append(node)

    def record(n: ast.AST) -> None:
        if isinstance(n, ast.arg):
            add(n.arg, n)
        elif isinstance(n, ast.Name) and isinstance(n.ctx, (ast.Store, ast.Del)):
            add(n.id, n)
        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n is not scope:
            add(n.name, n)
        elif isinstance(n, ast.Import):
            for a in n.names:
                add(a.asname or a.name.split(".")[0], n)
        elif isinstance(n, ast.ImportFrom):
            for a in n.names:
                add(a.asname or a.name, n)
        elif isinstance(n, (ast.Global, ast.Nonlocal)):
            for name in n.names:
                add(name, n)
        elif isinstance(n, ast.ExceptHandler) and n.name:
            add(n.name, n)
        elif isinstance(n, (ast.MatchAs, ast.MatchStar)) and n.name:
            add(n.name, n)
        elif isinstance(n, ast.MatchMapping) and n.rest:
            add(n.rest, n)

    if isinstance(scope, ast.ClassDef):
        # クラス本体の直下: 入れ子のスコープの本体には降りない（名前・装飾子・既定値・基底だけ）
        stack: list[ast.AST] = list(scope.body)
        while stack:
            n = stack.pop()
            record(n)
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                stack.extend(n.decorator_list)
                stack.extend(d for d in n.args.defaults)
                stack.extend(d for d in n.args.kw_defaults if d is not None)
                continue
            if isinstance(n, ast.ClassDef):
                stack.extend(n.decorator_list)
                stack.extend(n.bases)
                stack.extend(kw.value for kw in n.keywords)
                continue
            if isinstance(n, ast.Lambda):
                stack.extend(n.args.defaults)
                stack.extend(d for d in n.args.kw_defaults if d is not None)
                continue
            stack.extend(ast.iter_child_nodes(n))
    else:
        for n in ast.walk(scope):
            record(n)
    cache[id(scope)] = (scope, out)
    return out


def _import_dotted(node: ast.AST, name: str) -> Optional[str]:
    """level 0 の `import` / `from ... import` が `name` に結ぶ外部の dotted 名（:func:`_resolve_name_uncached`
    の `ext` と同じ綴り）。level > 0・`*`・該当なしは None。"""
    if isinstance(node, ast.Import):
        alias = next((a for a in node.names if (a.asname or a.name.split(".")[0]) == name), None)
        if alias is None:
            return None
        return alias.name if alias.asname else alias.name.split(".")[0]
    if isinstance(node, ast.ImportFrom):
        if node.level != 0 or not node.module:
            return None
        alias = next((a for a in node.names if (a.asname or a.name) == name and a.name != "*"), None)
        if alias is None:
            return None
        return f"{node.module}.{alias.name}"
    return None


def _same_as_module_import(index: SourceIndex, module: str, scope: ast.AST, name: str, nodes: list) -> bool:
    """囲むスコープでの `name` の束縛が、その本体の直下の level 0 の import **ちょうど 1 つ**で、モジュール水準の
    解決と**同じ外部の dotted 名**に解けるか（U23-R1）。そうなら注釈の評価はモジュール直下で解くのと同じ。"""
    if len(nodes) != 1:
        return False
    node = nodes[0]
    if not isinstance(node, (ast.Import, ast.ImportFrom)):
        return False
    body = getattr(scope, "body", None)
    if not isinstance(body, list) or not any(st is node for st in body):
        return False  # `try:` / `if` の中の import は本体の直下ではない（今どおり隠す）
    dotted = _import_dotted(node, name)
    if dotted is None:
        return False
    if isinstance(node, ast.ImportFrom):
        if index.resolve_import_module(module, node.module) is not None:
            return False  # 木内のモジュール（外部の名前ではない）
    elif index.resolve_import_module(module, dotted) is not None:
        return False
    return _ext(resolve_name(index, module, name)) == dotted


def _annotation_names(ann: ast.AST) -> set[str]:
    """注釈に現れる名前（文字列注釈の中も）。"""
    out: set[str] = set()
    stack = [ann]
    while stack:
        node = stack.pop()
        for n in ast.walk(node):
            if isinstance(n, ast.Name):
                out.add(n.id)
            elif isinstance(n, ast.Constant) and isinstance(n.value, str):
                sub = _parse_str(n)
                if sub is not None and sub is not n:
                    stack.append(sub)
    return out


def _shadowed_annotation(index: SourceIndex, unit, ann: ast.AST) -> bool:
    """注釈の名前が、入口を囲む関数 / クラスのスコープで束縛されうるか（U23-S1）。

    仮引数の注釈は定義の時点で囲むスコープで評価される。`def register(mcp): class Req(...)` / 局所の
    `from store import Path` のように囲むスコープで束縛される名前をモジュール直下の束縛で解くと、別の
    クラス / 型の種を置く（誤警報）。囲むスコープが見つからないときも真（種を置かない = 今日どおり）。

    ただし、囲むスコープでの束縛が本体の直下の level 0 の import ちょうど 1 つで、モジュール水準の解決と同じ
    外部の dotted 名に解けるなら隠されていない（U23-R1）。以前は `def register(m): from pathlib import Path`
    のように同じ pathlib.Path を局所でもう一度 import する形でも種を捨て、readOnlyHint の下の
    `path.write_text(...)` の D1 矛を失っていた（誤 clear）。それ以外の束縛（def / class / 代入 / 仮引数 /
    global、2 つ以上の束縛、`try` / `if` の中の import、別の名前に解ける import）は今どおり隠す。"""
    scopes = _enclosing_scopes(index, unit)
    if scopes is None:
        return True
    if not scopes:
        return False
    names = _annotation_names(ann)
    for sc in scopes:
        binders = _binders(index, sc)
        for name in names:
            nodes = binders.get(name)
            if nodes and not _same_as_module_import(index, unit.module, sc, name, nodes):
                return True
    return False


def annotated_param_seeds(index: SourceIndex, unit) -> dict[str, Value]:
    """入口の仮引数のうち、注釈から形を与えられるものの種（R4-r4-2 / R4-r1-6）。"""
    out: dict[str, Value] = {}
    args = _arg_nodes(unit.node)
    models_ok = unit.framework in _CONSTRUCTING_FRAMEWORKS
    for p in unit.params:
        if p.excluded:
            continue
        a = args.get(p.name)
        if a is None or a.annotation is None:
            continue
        if _shadowed_annotation(index, unit, a.annotation):
            continue
        v = _typed_seed(index, unit.module, a.annotation, p.name, 0, models_ok)
        if v is not None:
            out[p.name] = v
    return out


def opaque_field(v: Value) -> Value:
    """フックが値を変えうるフィールド: 主体・形・root は保ち、確度に `opaque(unresolved)` を合流する。"""
    from .val.engine import _opaque_deep

    return _opaque_deep(v)


def message_class_hooked(index: SourceIndex, unit) -> bool:
    """langroid の `ToolMessage` 派生クラス（同名の候補のどれか）に構築時フックがあるか（R4-r4-2 の条件）。"""
    name = unit.message_class
    if not name:
        return False
    for cd in index.classes():
        if cd.name == name and class_hooked(index, cd.module, cd.node):
            return True
    return False


# --------------------------------------------------------------------------
# lifespan（R4-r4-1）
# --------------------------------------------------------------------------


def _rebinds(fn: ast.AST, name: str) -> bool:
    """関数本体で `name` を束縛し直すか（代入・入れ子の定義・`global` / `nonlocal`）。"""
    for n in ast.walk(fn):
        if n is fn:
            continue
        if isinstance(n, ast.Name) and isinstance(n.ctx, (ast.Store, ast.Del)) and n.id == name:
            return True
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n.name == name:
            return True
        if isinstance(n, (ast.Global, ast.Nonlocal)) and name in n.names:
            return True
        if isinstance(n, ast.arg) and n.arg == name and n not in _arg_nodes(fn).values():
            return True
        if isinstance(n, (ast.Import, ast.ImportFrom)) and any(
            (a.asname or a.name.split(".")[0]) == name for a in n.names
        ):
            return True
    return False


def _receiver_value(index: SourceIndex, unit, recv: str) -> Optional[tuple[str, ast.AST]]:
    """装飾子の受け手名 `recv` の構築式 `(モジュール, 右辺)`。**ちょうど 1 回の代入**でなければ None。

    入口がモジュール直下の関数ならモジュール直下の束縛、モジュール直下の関数の入れ子（低レベル形の
    `serve()` の中）なら、その関数の本体の束縛（無ければモジュール直下）。それより深い入れ子・メソッドは扱わない。
    """
    tree = _module_tree(index, unit.module)
    if tree is None:
        return None
    parts = unit.qualname.split(".")
    if len(parts) > 2:
        return None
    if len(parts) == 2:
        parents = [
            f for f in index.lookup_function(parts[0], unit.module) if f.module == unit.module and f.classname is None
        ]
        if len(parents) != 1 or parents[0].node not in tree.body:
            return None
        parent = parents[0].node
        if recv in _arg_nodes(parent) or any(
            isinstance(n, (ast.Global, ast.Nonlocal)) and recv in n.names for n in ast.walk(parent)
        ):
            return None
        from .val.engine import _module_bindings

        binds = _module_bindings(parent, recv)
        if len(binds) > 1:
            return None
        if len(binds) == 1:
            rv = _assign_value(binds[0], unit.module)
            if rv is None or not isinstance(rv[1], ast.Call):
                return None
            # 構築式の名前（`Server` / `lifespan=` の関数名）は下でモジュール直下の束縛として解く。
            # 外側の関数の中で同じ名前を束縛し直す（局所の import・入れ子の def・仮引数）なら解かない
            names = [n.id for n in ast.walk(rv[1]) if isinstance(n, ast.Name)]
            if any(n in _arg_nodes(parent) or _module_bindings(parent, n) for n in names):
                return None
            return rv
    b = _binding(tree, recv)
    return _assign_value(b, unit.module) if b is not None else None


def _assign_value(b: ast.AST, module: str) -> Optional[tuple[str, ast.AST]]:
    if isinstance(b, ast.Assign) and len(b.targets) == 1 and isinstance(b.targets[0], ast.Name):
        return module, b.value
    if isinstance(b, ast.AnnAssign) and isinstance(b.target, ast.Name) and b.value is not None:
        return module, b.value
    return None


def _lifespan_touched(tree: ast.AST, recv: str) -> bool:
    """`recv.<...lifespan...> = ...` のように、構築後に lifespan を差し替えうる書き込みがあるか。"""
    for n in ast.walk(tree):
        if isinstance(n, ast.Attribute) and isinstance(n.ctx, (ast.Store, ast.Del)):
            d = dotted_of(n)
            if d and d.split(".")[0] == recv and any("lifespan" in p for p in d.split(".")[1:]):
                return True
    return False


def _mounted_names(index: SourceIndex) -> frozenset[str]:
    """木のどこかで `x.mount(...)` / `x.import_server(...)` の実引数に現れる名前（末尾名。保守的に名前だけで見る）。"""
    cache = index.__dict__
    if "_authgap_mounted_names" not in cache:
        out: set[str] = set()
        for path in index.py_files():
            tree = index.parse(path)
            if tree is None:
                continue
            for n in ast.walk(tree):
                if (
                    isinstance(n, ast.Call)
                    and isinstance(n.func, ast.Attribute)
                    and n.func.attr in ("mount", "import_server")
                ):
                    for a in list(n.args) + [kw.value for kw in n.keywords]:
                        d = dotted_of(a)
                        if d:
                            out.add(d.split(".")[-1])
        cache["_authgap_mounted_names"] = frozenset(out)
    return cache["_authgap_mounted_names"]


def _lifespan_function(index: SourceIndex, module: str, call: ast.Call) -> Optional[FuncDef]:
    """`lifespan=` が木内の CM 関数名（`@asynccontextmanager` / `@contextmanager`）ならその定義。"""
    from .val.engine import _is_context_manager

    kws = [kw for kw in call.keywords if kw.arg == "lifespan"]
    if len(kws) != 1 or not isinstance(kws[0].value, ast.Name):
        return None
    r = resolve_name(index, module, kws[0].value.id)
    if r is None or r[0] != "def":
        return None
    fmod, fnode = r[1]  # type: ignore[misc]
    if not isinstance(fnode, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return None
    hits = [f for f in index.lookup_function(fnode.name, fmod) if f.module == fmod and f.node is fnode]
    if len(hits) != 1:
        return None
    path = index.resolve_module_path(fmod)
    if path is None or not _is_context_manager(fnode, index.module_scope(path)):
        return None
    return hits[0]


def _yield_value(index: SourceIndex, fd: FuncDef) -> Optional[Value]:
    """lifespan 関数の yield 値（`_opaque_deep` 済み）。**効果を集めない別のエンジン**で評価する（起動時の
    効果をツールに付けない）。形が分からないときは None（種を置かない。MODEL の ctx 根を OP に替えない）。"""
    cache = index.__dict__.setdefault("_authgap_lifespan_values", {})
    if fd.key in cache:
        return cache[fd.key]
    from .val.engine import Options, ValEngine, ValResult, _opaque_deep

    fn_args = getattr(fd.node, "args", None)
    positional = list(fn_args.posonlyargs) + list(fn_args.args) if fn_args is not None else []
    server = Value(Prin.OP, opaque("unresolved"), Unknown())
    call = ast.Call(
        func=ast.Name(id=fd.node.name, ctx=ast.Load()),
        args=[ast.Name(id="<server>", ctx=ast.Load())] if positional else [],
        keywords=[],
    )
    call.lineno = getattr(fd.node, "lineno", 0)
    engine = ValEngine(index, Options(), on_call=None)
    out: Optional[Value] = None
    try:
        ret, sub = engine._descend_env(fd, call, [server] if positional else [], {}, None, ValResult(), 0, ())
    except RecursionError:
        ret, sub = None, None
    if sub is not None and ret is not None and sub.get("<yield>") is not None and not isinstance(ret.shape, Unknown):
        out = _opaque_deep(ret)
    cache[fd.key] = out
    return out


def lifespan_seeds(index: SourceIndex, unit) -> dict[str, Value]:
    """lifespan の yield 値を `<ctx>.request_context.lifespan_context` / `<server>.request_context.lifespan_context`
    に置く種（R4-r4-1）。条件を満たさなければ空。"""
    out: dict[str, Value] = {}
    tree = _module_tree(index, unit.module)
    if tree is None:
        return out
    for d in getattr(unit.node, "decorator_list", []):
        target = _decorator_target(d)
        if not (isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name)):
            continue
        recv, attr = target.value.id, target.attr
        if attr not in ("tool", "call_tool"):
            continue
        rv = _receiver_value(index, unit, recv)
        if rv is None or not isinstance(rv[1], ast.Call) or _lifespan_touched(tree, recv):
            continue
        if recv in _mounted_names(index):
            continue  # mount / import_server で合成されるサーバ: 実行時の lifespan が決まらない
        cmod, call = rv
        ctor = _ext(resolve_expr(index, cmod, call.func))
        if not ((attr == "tool" and ctor in FASTMCP_CTORS) or (attr == "call_tool" and ctor in LOWLEVEL_CTORS)):
            continue
        fd = _lifespan_function(index, cmod, call)
        if fd is None:
            continue
        value = _yield_value(index, fd)
        if value is None:
            continue
        if attr == "call_tool":
            if not _rebinds(unit.node, recv) and recv not in _arg_nodes(unit.node):
                key = f"{recv}.request_context.lifespan_context"
                out[key] = shared_state_view(value, key)
            continue
        for name, a in _arg_nodes(unit.node).items():
            if a.annotation is None or _rebinds(unit.node, name):
                continue
            if _shadowed_annotation(index, unit, a.annotation):
                continue  # 囲むスコープで束縛される `Context`（U23-S1）
            node, _clean = unwrap_annotation(index, unit.module, a.annotation)
            if isinstance(node, ast.Subscript):  # `Context[ServerSession, AppContext]`
                node = node.value
            if node is None or _ext(resolve_expr(index, unit.module, node)) not in CONTEXT_TYPES:
                continue
            # root は ctx（直す前に ctx の属性・添字から読んだときと同じ部分パス `ctx["table"]` になる）
            view = shared_state_view(value, name)
            out[f"{name}.request_context.lifespan_context"] = view
            if ctor is not None and ctor.startswith("fastmcp."):
                out[f"{name}.lifespan_context"] = view
    return out


def shared_state_view(v: Value, root: str) -> Value:
    """lifespan_context（呼び出しをまたいで共有される可変の状態）の種の見え方（U23-A1）。

    **型は受け手オブジェクトにだけ付け、受け手型の要らない葉（Atom / Str / 形不明 / 定数）は、直す前と同じく
    ctx 根の MODEL（確度 opaque(unresolved)、root は ctx の部分パス）にする。** 別のツールが
    `lifespan_context["table"] = table` とモデルの値を書き込めるので、葉はモデルの値かもしれない。以前は
    yield 値の主体（OP）をそのまま置き、`"SELECT … " + st["table"]` / `"INSERT … '" + st["tag"]` を
    OP/opaque の接頭辞として READ / INSERT(additive) → 内 にしていた（誤 clear。fix_outline (4)「D1 / D2 の類は
    不 → 不で変わらない」に反した）。

    * 容器（Map / Seq / Argv）と受け手オブジェクト（Obj / Path）は形を保ち（受け手型と、キー / 属性で葉まで
      たどるため）、主体に MODEL を合流し、確度を opaque にする。読めていない要素（Map / 列の tail、Obj の
      知らない属性は容器の主体に倒れる）も MODEL/opaque。
    * Map のキーで降りると root を `root["key"]` にする（エンジンの定数キーの添字と同じ精緻化）。属性・列の
      要素・パスの部分は root を変えない（直す前に ctx の属性から読んだときと同じ）。
    * 形の再帰は打ち切らない。循環（あり得ないはずのもの）と処理系の再帰の上限は葉として扱う（fail closed）。
    """

    def leaf(r: str) -> Value:
        return Value(Prin.MODEL, opaque("unresolved"), Unknown(), frozenset(), frozenset({r}))

    active: set[int] = set()

    def go(x: Value, r: str) -> Value:
        s = x.shape
        if not isinstance(s, (Map, Seq, Argv, Obj, Path)) or id(x) in active:
            return leaf(r)
        active.add(id(x))
        try:
            if isinstance(s, Map):
                ns: object = Map(
                    tuple((k, go(e, f'{r}["{k}"]')) for k, e in s.entries),
                    go(s.tail, r) if s.tail is not None else leaf(r),
                )
            elif isinstance(s, (Seq, Argv)):
                ns = type(s)(tuple(go(e, r) for e in s.elems), go(s.tail, r) if s.tail is not None else leaf(r))
            elif isinstance(s, Obj):
                ns = Obj(s.classes, tuple((k, go(e, r)) for k, e in s.fields))
            else:
                ns = Path(
                    go(s.base, r) if s.base is not None else None,
                    tuple(go(e, r) for e in s.segs),
                    go(s.tail, r) if s.tail is not None else None,
                )
        finally:
            active.discard(id(x))
        return Value(
            prin_join(x.prin, Prin.MODEL), prov_merge(x.prov, opaque("unresolved")), ns, x.attrs, frozenset({r})
        )

    try:
        return go(v, root)
    except RecursionError:
        return leaf(root)
