"""Def 5 の config atom を 4 源すべてから読む。

    コンストラクタ kwarg / モジュール定数 / `os.environ` 読み出し /
    CLI オプションの既定値（argparse の `dest`+`default`、click / typer の option 既定値）

**既定値が None や開放値なら default-open で `req` は MODEL のまま。**
hook 登録チェーン、generator 越し、HTTP 越しは `opaque`。

**曖昧な名前は解決しない。** 同じ名前の既定値が木の中で食い違うときは
`None`（源が特定できない）を返す。推定で片方を採ると、既定閉と既定開を
取り違えて `req` を誤って引き上げる（false-clean 方向の誤り）。
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from typing import Any, Optional

from .catalog import validators as V
from .ir import stable_repr
from .srcindex import SourceIndex, dotted_of

#: 曖昧（同名で既定値が食い違う）ことを表す番兵。
AMBIGUOUS = object()

#: CLI オプションを宣言する呼び出し。
_CLI_CALLS = ("add_argument", "option", "Option", "argument", "Argument")

#: pydantic の `Field(default=...)` / `Field(default_factory=...)`。
_FIELD_CALLS = ("Field", "field")


@dataclass(frozen=True)
class Atom:
    """解決した config atom。"""

    name: str
    source: str
    default: Any = None
    default_closed: Optional[bool] = None

    def to_json(self) -> dict:
        return {
            "name": self.name,
            "source": self.source,
            "default": self.default
            if isinstance(self.default, (str, int, float, bool, type(None)))
            else stable_repr(self.default),
            "default_closed": self.default_closed,
        }


@dataclass
class AtomIndex:
    """木全体の config atom 表。**1 回だけ作って使い回す。**"""

    #: `(module, name)` → 値。
    module_consts: dict[tuple[str, str], Any] = field(default_factory=dict)
    #: 名前 → 値（クラス体 / `__init__` の既定値）。曖昧なら :data:`AMBIGUOUS`。
    attr_defaults: dict[str, Any] = field(default_factory=dict)
    #: 名前 → 値（CLI オプションの既定値）。曖昧なら :data:`AMBIGUOUS`。
    cli_defaults: dict[str, Any] = field(default_factory=dict)
    #: `os.environ` から読まれる名前。
    environ_names: set[str] = field(default_factory=set)

    # -- 参照 -------------------------------------------------------------

    def lookup(self, name: str, module: Optional[str] = None) -> Optional[Atom]:
        """名前（`ALLOWED` / `self.config.allow_x` のような dotted）から引く。

        探す順は **モジュール定数 → コンストラクタ kwarg / クラス既定値 →
        CLI 既定値 → `os.environ`**。見つからなければ `None`。
        """
        last = name.split(".")[-1]

        if module is not None and (module, last) in self.module_consts:
            return self._atom(last, "module_const", self.module_consts[(module, last)])
        hits = [v for (m, n), v in self.module_consts.items() if n == last]
        if len(hits) == 1:
            return self._atom(last, "module_const", hits[0])
        if len(hits) > 1 and all(_same(h, hits[0]) for h in hits):
            return self._atom(last, "module_const", hits[0])

        for table, source in (
            (self.attr_defaults, "ctor_kwarg"),
            (self.cli_defaults, "cli_default"),
        ):
            if last in table:
                v = table[last]
                if v is AMBIGUOUS:
                    # **曖昧なら解決しない。** 既定閉／既定開を取り違えない。
                    return Atom(last, source, None, None)
                return self._atom(last, source, v)

        if last in self.environ_names:
            return Atom(last, "environ", None, None)
        return None

    @staticmethod
    def _atom(name: str, source: str, value: Any) -> Atom:
        return Atom(name, source, value, V.is_default_closed(value))


def build_atom_index(index: SourceIndex) -> AtomIndex:
    """木を 1 回走査して 4 源の config atom を集める。"""
    ai = AtomIndex()
    for path in index.py_files():
        tree = index.parse(path)
        if tree is None:
            continue
        module = index.module_name(path)
        _collect_module_consts(tree, module, ai)
        _collect_class_defaults(tree, ai)
        _collect_cli_defaults(tree, ai)
        _collect_environ(tree, ai)
    return ai


# --------------------------------------------------------------------------
# 源 2: モジュール定数
# --------------------------------------------------------------------------


def _collect_module_consts(tree: ast.Module, module: str, ai: AtomIndex) -> None:
    for node in tree.body:
        targets: list = []
        value = None
        if isinstance(node, ast.Assign):
            targets, value = list(node.targets), node.value
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            targets, value = [node.target], node.value
        if value is None:
            continue
        ok, lit = _literal(value)
        if not ok:
            continue
        for t in targets:
            if isinstance(t, ast.Name):
                ai.module_consts[(module, t.id)] = lit


# --------------------------------------------------------------------------
# 源 1: コンストラクタ kwarg / クラス体の既定値
# --------------------------------------------------------------------------


def _collect_class_defaults(tree: ast.Module, ai: AtomIndex) -> None:
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for sub in node.body:
                _class_member(sub, ai)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "__init__":
            _init_kwargs(node, ai)


def _class_member(sub: ast.AST, ai: AtomIndex) -> None:
    name = None
    value = None
    if isinstance(sub, ast.AnnAssign) and isinstance(sub.target, ast.Name):
        name, value = sub.target.id, sub.value
    elif isinstance(sub, ast.Assign) and len(sub.targets) == 1 and isinstance(sub.targets[0], ast.Name):
        name, value = sub.targets[0].id, sub.value
    if name is None or value is None or name.startswith("_"):
        return
    ok, lit = _literal(value)
    if not ok:
        ok, lit = _pydantic_field_default(value)
    if ok:
        _record(ai.attr_defaults, name, lit)


def _pydantic_field_default(value: ast.AST) -> tuple[bool, Any]:
    """`Field(default=X)` / `Field(X, ...)` の既定値。"""
    if not isinstance(value, ast.Call):
        return False, None
    fname = (dotted_of(value.func) or "").split(".")[-1]
    if fname not in _FIELD_CALLS:
        return False, None
    for kw in value.keywords:
        if kw.arg == "default":
            return _literal(kw.value)
        if kw.arg == "default_factory":
            # `default_factory=list` などは値が読めない。**推定しない。**
            return False, None
    if value.args:
        return _literal(value.args[0])
    return False, None


def _init_kwargs(fn: ast.AST, ai: AtomIndex) -> None:
    args = getattr(fn, "args", None)
    if args is None:
        return
    positional = list(args.posonlyargs) + list(args.args)
    defaults = list(args.defaults)
    pad = len(positional) - len(defaults)
    for i, a in enumerate(positional):
        if i < pad or a.arg in ("self", "cls"):
            continue
        ok, lit = _literal(defaults[i - pad])
        if ok:
            _record(ai.attr_defaults, a.arg, lit)
    for j, a in enumerate(args.kwonlyargs):
        d = args.kw_defaults[j]
        if d is None:
            continue
        ok, lit = _literal(d)
        if ok:
            _record(ai.attr_defaults, a.arg, lit)


# --------------------------------------------------------------------------
# 源 4: CLI オプションの既定値
# --------------------------------------------------------------------------


def _collect_cli_defaults(tree: ast.Module, ai: AtomIndex) -> None:
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fname = (dotted_of(node.func) or "").split(".")[-1]
        if fname not in _CLI_CALLS:
            continue
        default = None
        has_default = False
        dest = None
        for kw in node.keywords:
            if kw.arg == "default":
                has_default, default = _literal(kw.value)
            elif kw.arg == "dest" and isinstance(kw.value, ast.Constant):
                dest = kw.value.value
        if not has_default:
            continue
        names = [dest] if dest else []
        if not names:
            for a in node.args:
                if isinstance(a, ast.Constant) and isinstance(a.value, str):
                    names.append(a.value.lstrip("-").replace("-", "_"))
        for n in names:
            if n:
                _record(ai.cli_defaults, n, default)


# --------------------------------------------------------------------------
# 源 3: os.environ
# --------------------------------------------------------------------------


def _collect_environ(tree: ast.Module, ai: AtomIndex) -> None:
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            fname = dotted_of(node.func) or ""
            if fname.endswith("environ.get") or fname.endswith("getenv"):
                if node.args and isinstance(node.args[0], ast.Constant):
                    if isinstance(node.args[0].value, str):
                        ai.environ_names.add(node.args[0].value)
        elif isinstance(node, ast.Subscript):
            base = dotted_of(node.value) or ""
            if base.endswith("environ") and isinstance(node.slice, ast.Constant):
                if isinstance(node.slice.value, str):
                    ai.environ_names.add(node.slice.value)


# --------------------------------------------------------------------------
# 補助
# --------------------------------------------------------------------------


def _literal(node: ast.AST) -> tuple[bool, Any]:
    try:
        return True, ast.literal_eval(node)
    except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
        return False, None


def _same(a: Any, b: Any) -> bool:
    try:
        return bool(a == b)
    except Exception:  # pragma: no cover
        return False


def _record(table: dict[str, Any], name: str, value: Any) -> None:
    """同じ名前で既定値が食い違ったら :data:`AMBIGUOUS` にする。"""
    if name in table and not _same(table[name], value):
        table[name] = AMBIGUOUS
    elif name not in table:
        table[name] = value
