"""ソース索引。決定論的な走査、parse 失敗の記録、スコープつき import 表。

§13 の判定に従い、前身の `SourceIndex._parse` / `_build_module_map` /
`file_defs` / `resolve_module_path` の**構造**（sorted walk による決定論、
parse 失敗の記録、import 表）を踏襲する。ただし前身の `imports()` は
`ast.walk(tree)` でモジュール全体を舐めるため関数ローカル `import` も平坦な表に
混ざりスコープを無視する。**ここでは `(モジュール, 関数)` 粒度に拡張する。**
"""

from __future__ import annotations

import ast
import os
from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Optional

from .ir import AST_NODE_CAP

#: 明示 import なしで使える組込み sink 名。
BUILTIN_SINK_NAMES: frozenset[str] = frozenset({"eval", "exec", "compile", "open"})


@dataclass
class FuncDef:
    """木内のユーザ定義関数 1 個。"""

    #: `src_root` からの相対パス。
    relpath: str
    #: `pkg.mod`。
    module: str
    #: `Class.method` または `func`。
    qualname: str
    node: ast.AST
    #: メソッドなら所属クラス名。
    classname: Optional[str] = None
    is_async: bool = False

    @property
    def key(self) -> str:
        return f"{self.module}:{self.qualname}"


@dataclass
class ClassDef:
    relpath: str
    module: str
    name: str
    node: ast.ClassDef
    bases: tuple[str, ...] = ()


@dataclass
class Scope:
    """名前解決の文脈。モジュール表とローカル表の 2 段。"""

    module: str
    relpath: str
    module_imports: dict[str, str]
    local_imports: dict[str, str] = field(default_factory=dict)
    #: この関数内で定義された名前（import を隠す）。
    local_bindings: frozenset[str] = frozenset()

    def lookup(self, name: str) -> Optional[str]:
        """局所 import を優先し、次にモジュール import を見る。"""
        if name in self.local_imports:
            return self.local_imports[name]
        if name in self.module_imports:
            return self.module_imports[name]
        return None


class SourceIndex:
    """解析対象の木を 1 回だけ走査して索引を作る。

    **決定論**: `os.walk` の結果を毎回ソートする。parse 失敗は握り潰さず
    :attr:`parse_failures` に記録する（行として出力される）。
    """

    def __init__(self, src_root: str) -> None:
        self.src_root = os.path.abspath(src_root)
        self._ast: dict[str, Optional[ast.Module]] = {}
        self._node_counts: dict[str, int] = {}
        self._modname_to_path: dict[str, str] = {}
        self._built = False
        #: parse に失敗したファイル（相対パス、ソート済み）。
        self.parse_failures: list[str] = []
        #: cap に当たったファイル（`(relpath, cap 名, 件数)`）。
        self.cap_hits: list[tuple[str, str, int]] = []
        self._funcs: dict[str, FuncDef] = {}
        self._classes: dict[str, ClassDef] = {}
        self._funcs_by_qual: dict[str, list[FuncDef]] = {}

    # -- 走査 -------------------------------------------------------------

    def py_files(self) -> list[str]:
        """`.py` ファイルの絶対パス（決定論的な順序）。"""
        out: list[str] = []
        for dirpath, dirs, files in os.walk(self.src_root):
            dirs[:] = sorted(d for d in dirs if d not in _SKIP_DIRS)
            for fn in sorted(files):
                if fn.endswith(".py"):
                    out.append(os.path.join(dirpath, fn))
        return out

    def relpath(self, path: str) -> str:
        return os.path.relpath(os.path.abspath(path), self.src_root)

    def module_name(self, path: str) -> str:
        rel = self.relpath(path)
        dotted = rel[:-3].replace(os.sep, ".")
        if dotted.endswith(".__init__"):
            dotted = dotted[: -len(".__init__")]
        return dotted

    def parse(self, path: str) -> Optional[ast.Module]:
        """ファイルを parse する。失敗と cap 到達を記録する。**黙って捨てない。**"""
        path = os.path.abspath(path)
        if path in self._ast:
            return self._ast[path]
        rel = self.relpath(path)
        tree: Optional[ast.Module]
        try:
            # **バイト列で渡す。** `open(encoding="utf-8")` で文字列にすると先頭の
            # BOM（U+FEFF）が残り、3.10 でも 3.12 でも SyntaxError になる。
            # `ast.parse` はバイト列なら BOM と PEP 263 の coding 宣言を処理する。
            with open(path, "rb") as fh:
                src = fh.read()
            tree = ast.parse(src, filename=path)
        except (OSError, SyntaxError, ValueError, RecursionError):
            tree = None
            if rel not in self.parse_failures:
                self.parse_failures.append(rel)
        if tree is not None:
            n = sum(1 for _ in ast.walk(tree))
            self._node_counts[rel] = n
            if n > AST_NODE_CAP:
                self.cap_hits.append((rel, "ast_node_cap", n))
                tree = None  # cap 到達は TRUNCATED 行として出力する（行は消えない）
        self._ast[path] = tree
        return tree

    def node_count(self, path: str) -> int:
        return self._node_counts.get(self.relpath(path), 0)

    # -- モジュール表 ------------------------------------------------------

    def build(self) -> None:
        if self._built:
            return
        self._built = True
        for full in self.py_files():
            dotted = self.module_name(full)
            self._modname_to_path.setdefault(dotted, full)
            last = dotted.split(".")[-1]
            self._modname_to_path.setdefault(last, full)
        for full in self.py_files():
            self._index_defs(full)

    def resolve_module_path(self, dotted: str) -> Optional[str]:
        """dotted モジュール名を木内のパスへ。末尾成分での照合も試す。"""
        self.build()
        if dotted in self._modname_to_path:
            return self._modname_to_path[dotted]
        parts = dotted.split(".")
        for i in range(1, len(parts)):
            cand = ".".join(parts[i:])
            if cand in self._modname_to_path:
                return self._modname_to_path[cand]
        return None

    # -- 定義表 -----------------------------------------------------------

    def _index_defs(self, path: str) -> None:
        tree = self.parse(path)
        if tree is None:
            return
        rel = self.relpath(path)
        mod = self.module_name(path)
        self._index_body(tree.body, rel, mod, prefix="", classname=None)

    def _index_body(
        self, body: list, rel: str, mod: str, prefix: str, classname: Optional[str]
    ) -> None:
        """入れ子定義も索引する。

        **入れ子関数を落としてはならない。** 低レベル MCP のハンドラは
        ほぼ常に `async def serve(...)` の中の `@server.call_tool()` 付き
        入れ子関数であり、モジュール直下しか見ないと R2 の入口が 0 件になる。
        qualname は `serve.call_tool` のように `.` で連ねる。
        """
        for node in body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                qual = f"{prefix}{node.name}"
                fd = FuncDef(rel, mod, qual, node, classname, isinstance(node, ast.AsyncFunctionDef))
                self._funcs.setdefault(fd.key, fd)
                self._funcs_by_qual.setdefault(qual, []).append(fd)
                if qual != node.name:
                    self._funcs_by_qual.setdefault(node.name, []).append(fd)
                self._index_body(node.body, rel, mod, prefix=f"{qual}.", classname=classname)
            elif isinstance(node, ast.ClassDef):
                cd = ClassDef(rel, mod, node.name, node, tuple(_base_names(node)))
                self._classes.setdefault(f"{mod}:{node.name}", cd)
                self._classes.setdefault(node.name, cd)
                self._index_body(
                    node.body, rel, mod, prefix=f"{prefix}{node.name}.", classname=node.name
                )
            elif isinstance(node, (ast.If, ast.Try, ast.With, ast.AsyncWith)):
                for sub in (
                    list(getattr(node, "body", []))
                    + list(getattr(node, "orelse", []))
                    + list(getattr(node, "finalbody", []))
                ):
                    self._index_body([sub], rel, mod, prefix, classname)
                for h in getattr(node, "handlers", []):
                    self._index_body(h.body, rel, mod, prefix, classname)

    def functions(self) -> Iterator[FuncDef]:
        self.build()
        for key in sorted(self._funcs):
            yield self._funcs[key]

    def classes(self) -> Iterator[ClassDef]:
        self.build()
        seen: set[str] = set()
        for key in sorted(self._classes):
            cd = self._classes[key]
            ident = f"{cd.module}:{cd.name}"
            if ident in seen:
                continue
            seen.add(ident)
            yield cd

    def get_class(self, name: str, module: Optional[str] = None) -> Optional[ClassDef]:
        self.build()
        if module is not None:
            hit = self._classes.get(f"{module}:{name}")
            if hit is not None:
                return hit
        return self._classes.get(name)

    def lookup_function(self, qualname: str, module: Optional[str] = None) -> list[FuncDef]:
        """qualname から木内の定義候補を引く。

        **同名メソッドを無条件に 1 つ採らない**（前身 `find_method` の欠陥）。
        候補が複数ならすべて返し、呼び出し側が受け手型で絞る。絞れなければ
        `opaque(unresolved)` にする。
        """
        self.build()
        if module is not None:
            hit = self._funcs.get(f"{module}:{qualname}")
            if hit is not None:
                return [hit]
        return list(self._funcs_by_qual.get(qualname, ()))

    # -- スコープつき import 表 --------------------------------------------

    def module_scope(self, path: str) -> Scope:
        """モジュール水準の import 表だけを持つスコープ。

        **条件つき import を必ず拾う。** 任意依存を
        `try: from sqlalchemy import text / except ImportError: ...` で包むのは
        母集団の常套形で、`tree.body` の直下だけを見ると `text` が解決できず
        sink 表に当たらない（langroid の SQL agent がこれで無言になった）。
        """
        tree = self.parse(path)
        imports: dict[str, str] = {}
        if tree is not None:
            _collect_imports(tree.body, imports, recurse=True)
        return Scope(self.module_name(path), self.relpath(path), imports)

    def function_scope(self, path: str, fn: ast.AST) -> Scope:
        """関数水準のスコープ。**関数ローカルの import はここにだけ入る。**"""
        base = self.module_scope(path)
        local: dict[str, str] = {}
        body = getattr(fn, "body", [])
        _collect_imports(body, local, recurse=True)
        bindings = _local_bindings(fn)
        return Scope(base.module, base.relpath, base.module_imports, local, bindings)


_SKIP_DIRS = frozenset(
    {
        ".git",
        ".hg",
        ".svn",
        "__pycache__",
        ".venv",
        "venv",
        "node_modules",
        ".tox",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        "site-packages",
    }
)


def _base_names(node: ast.ClassDef) -> list[str]:
    out: list[str] = []
    for b in node.bases:
        name = dotted_of(b)
        if name:
            out.append(name)
    return out


def _collect_imports(body: list, out: dict[str, str], recurse: bool = False) -> None:
    """import 文を表に入れる。

    `from mod import name` は ``mod.name`` に展開する（前身の ``mod::name``
    という独自表記をやめ、dotted 名に一本化してカタログ照合と同じ土俵に載せる）。
    """
    stack = list(body)
    while stack:
        node = stack.pop(0)
        if isinstance(node, ast.Import):
            for a in node.names:
                if a.asname:
                    out[a.asname] = a.name
                else:
                    out[a.name.split(".")[0]] = a.name.split(".")[0]
                    out.setdefault(a.name, a.name)
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            for a in node.names:
                local = a.asname or a.name
                out[local] = f"{mod}.{a.name}" if mod else a.name
        elif recurse and isinstance(node, (ast.If, ast.Try, ast.With, ast.AsyncWith)):
            stack.extend(getattr(node, "body", []))
            stack.extend(getattr(node, "orelse", []))
            stack.extend(getattr(node, "finalbody", []))
            for h in getattr(node, "handlers", []):
                stack.extend(h.body)


def _local_bindings(fn: ast.AST) -> frozenset[str]:
    """関数内で代入・定義される名前（import を隠す）。"""
    names: set[str] = set()
    for node in ast.walk(fn):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            names.add(node.id)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.arg):
            names.add(node.arg)
    return frozenset(names)


# --------------------------------------------------------------------------
# dotted 名の正規化
# --------------------------------------------------------------------------


def dotted_of(node: ast.AST) -> Optional[str]:
    """`ast.Attribute` / `ast.Name` の連鎖を dotted 文字列にする。"""
    parts: list[str] = []
    cur = node
    while True:
        if isinstance(cur, ast.Attribute):
            parts.append(cur.attr)
            cur = cur.value
        elif isinstance(cur, ast.Name):
            parts.append(cur.id)
            break
        else:
            return None
    return ".".join(reversed(parts))


def resolve_call_name(func: ast.AST, scope: Scope) -> Optional[str]:
    """呼び出し式の被呼び出し名を、import 表を使って dotted 名に正規化する。

    * ``run(...)``            + ``from subprocess import run`` → ``subprocess.run``
    * ``sp.run(...)``         + ``import subprocess as sp``    → ``subprocess.run``
    * ``os.path.realpath()``  + ``import os``                  → ``os.path.realpath``
    * ``eval(...)``（局所束縛なし）                            → ``builtins.eval``

    解決できなければ ``None``（**推定で埋めない**）。
    """
    raw = dotted_of(func)
    if raw is None:
        return None
    head, _, rest = raw.partition(".")
    if not rest:
        if head in scope.local_bindings:
            return None  # 局所で再束縛されている。組込みとみなさない
        mapped = scope.lookup(head)
        if mapped:
            return mapped
        if head in BUILTIN_SINK_NAMES:
            return f"builtins.{head}"
        return None
    mapped = scope.lookup(head)
    if mapped:
        return f"{mapped}.{rest}"
    if head in scope.local_bindings:
        return None  # 受け手が局所変数。受け手型の推論に回す
    return raw
