"""Def 4 の `trig`: 効果の**発生**を誰が決めるか。

`trig(e)` は効果の発生を支配する述語のラベル結び。制御辺は
**dispatch key（subscript / `.get` / `getattr` / 解決済みレジストリ上の match）と
カタログ化したゲート述語に限定**する。一般分岐と `for tc in tool_calls` は除外
（implicit flow の爆発を避ける）。

`traced` / `assumed` の区別（Def 2）:

* MODEL ラベル付きセレクタから木内の dispatch を辿って到達すれば ``traced``
* 登録 API（`@mcp.tool` 等）による仮定なら ``assumed``

**両者の比率を必ず報告する**（§6 の `traced_ratio`）。

**`assumed` の trig では SELECT 行は GAP ではなくマニフェスト行**（Def 7。
この規則は narrow しない）。これが無いと定数 argv の
`subprocess.run(["git","status"])` が全部 GAP になる。
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from typing import Optional

from .entries import Unit, is_llm_call
from .ir import Prin
from .srcindex import SourceIndex, dotted_of


@dataclass
class DispatchSite:
    """木内の dispatch 1 か所。"""

    relpath: str
    lineno: int
    #: セレクタ式のテキスト（`tc.name` など）。
    selector: str
    #: セレクタが MODEL 由来か（R1 の LLM 戻り値 / R2 の入口引数から来ているか）。
    selector_is_model: bool
    #: 候補集合。解決できなければ空。
    candidates: tuple[str, ...] = ()
    #: ``resolved`` / ``opaque``
    resolution: str = "opaque"
    #: `opaque` のときの理由（ゲート側語彙）。
    opaque_reason: Optional[str] = None
    #: 形（`subscript` / `get` / `getattr` / `if_chain` / `match`）。
    form: str = "subscript"

    def to_json(self) -> dict:
        return {
            "relpath": self.relpath,
            "lineno": self.lineno,
            "selector": self.selector,
            "selector_is_model": self.selector_is_model,
            "candidates": list(self.candidates),
            "resolution": self.resolution,
            "opaque_reason": self.opaque_reason,
            "form": self.form,
        }


@dataclass
class TrigResult:
    """1 ユニットの `trig`。"""

    label: Prin = Prin.MODEL
    #: ``traced`` / ``assumed``
    mode: str = "assumed"
    #: 根拠になった dispatch（`traced` のとき）。
    via: Optional[DispatchSite] = None

    def to_json(self) -> dict:
        d = {"label": self.label.name, "mode": self.mode}
        if self.via is not None:
            d["via"] = self.via.to_json()
        return d


@dataclass
class TrigIndex:
    """木全体の dispatch 表と、そこから決まるユニットごとの `trig`。"""

    sites: list[DispatchSite] = field(default_factory=list)
    #: 候補名 → その名前を候補に持つ dispatch。
    by_candidate: dict[str, list[DispatchSite]] = field(default_factory=dict)

    def traced_ratio(self, units: list[Unit]) -> Optional[float]:
        if not units:
            return None
        n = sum(1 for u in units if self.trig_for(u).mode == "traced")
        return n / len(units)

    def registry_resolution_ratio(self) -> Optional[float]:
        """dispatch のうち候補集合が木内で解決した割合（F0c(i)）。"""
        if not self.sites:
            return None
        n = sum(1 for s in self.sites if s.resolution == "resolved")
        return n / len(self.sites)

    def trig_for(self, unit: Unit) -> TrigResult:
        """ユニットの `trig`。

        木内の dispatch の候補にそのユニットの名前が現れ、かつセレクタが
        MODEL 由来なら ``traced``。そうでなければ ``assumed``。
        """
        keys = {unit.qualname, unit.qualname.split(".")[-1]}
        if unit.tool_name:
            keys.add(unit.tool_name)
        for key in sorted(keys):
            for site in self.by_candidate.get(key, ()):
                if site.selector_is_model:
                    return TrigResult(Prin.MODEL, "traced", site)
        # 低レベルハンドラ自身は、入口引数 `name` で分岐する dispatcher である。
        # **`dispatch_names` の有無を条件にしない。** 候補名が `GitTools.STATUS` の
        # ような Enum メンバで、文字列として読めないことがあるためで、
        # 「MODEL セレクタで分岐している」ことは候補名が読めなくても決まる。
        if unit.entry_kind.startswith("lowlevel"):
            for site in self.sites:
                if site.relpath == unit.relpath and site.selector_is_model:
                    return TrigResult(Prin.MODEL, "traced", site)
        return TrigResult(Prin.MODEL, "assumed", None)


# --------------------------------------------------------------------------
# dispatch の発見
# --------------------------------------------------------------------------


def build_trig_index(index: SourceIndex, units: list[Unit]) -> TrigIndex:
    """木内の dispatch を集める。"""
    out = TrigIndex()
    unit_params: dict[str, set[str]] = {}
    for u in units:
        unit_params.setdefault(u.relpath, set()).update(p.name for p in u.model_params)

    for path in index.py_files():
        tree = index.parse(path)
        if tree is None:
            continue
        rel = index.relpath(path)
        model_names = _model_names(tree, unit_params.get(rel, set()))
        consts = _module_dicts(tree)
        for fn in _functions(tree):
            for site in _sites_in(fn, rel, model_names, consts, index):
                out.sites.append(site)
    out.sites.sort(key=lambda s: (s.relpath, s.lineno, s.selector))
    for s in out.sites:
        for c in s.candidates:
            out.by_candidate.setdefault(c, []).append(s)
            out.by_candidate.setdefault(c.split(".")[-1], []).append(s)
    return out


def _functions(tree: ast.Module) -> list[ast.AST]:
    out: list[ast.AST] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            out.append(node)
    return out


def _module_dicts(tree: ast.Module) -> dict[str, ast.Dict]:
    out: dict[str, ast.Dict] = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Dict):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    out[t.id] = node.value
    return out


def _model_names(tree: ast.Module, param_names: set[str]) -> set[str]:
    """MODEL 由来の名前（R1 の LLM 戻り値の射影と、R2 の入口引数）。

    **一般分岐は追わない**（Def 4 の制御辺の限定）。R1 は「LLM 呼び出しの
    戻り値に束縛された名前とその属性到達」だけを見る。
    """
    names: set[str] = set(param_names)
    changed = True
    while changed:
        changed = False
        for node in ast.walk(tree):
            value = None
            targets: list[ast.AST] = []
            if isinstance(node, ast.Assign):
                targets, value = list(node.targets), node.value
            elif isinstance(node, ast.AnnAssign) and node.value is not None:
                targets, value = [node.target], node.value
            elif isinstance(node, (ast.For, ast.AsyncFor)):
                targets, value = [node.target], node.iter
            elif isinstance(node, ast.withitem) and node.optional_vars is not None:
                targets, value = [node.optional_vars], node.context_expr
            if value is None:
                continue
            src_model = False
            if isinstance(value, ast.Call) and is_llm_call(value):
                src_model = True
            else:
                for sub in ast.walk(value):
                    if isinstance(sub, ast.Name) and sub.id in names:
                        src_model = True
                    elif isinstance(sub, ast.Attribute):
                        d = dotted_of(sub)
                        if d and d.split(".")[0] in names:
                            src_model = True
                    elif isinstance(sub, ast.Call) and is_llm_call(sub):
                        src_model = True
            if not src_model:
                continue
            for t in targets:
                for sub in ast.walk(t):
                    if isinstance(sub, ast.Name) and sub.id not in names:
                        names.add(sub.id)
                        changed = True
    return names


def _is_model_expr(node: ast.AST, model_names: set[str]) -> bool:
    for sub in ast.walk(node):
        if isinstance(sub, ast.Name) and sub.id in model_names:
            return True
        if isinstance(sub, ast.Attribute):
            d = dotted_of(sub)
            if d and d.split(".")[0] in model_names:
                return True
    return False


def _sites_in(
    fn: ast.AST, rel: str, model_names: set[str], consts: dict[str, ast.Dict], index: SourceIndex
) -> list[DispatchSite]:
    out: list[DispatchSite] = []
    for node in ast.walk(fn):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        # (1) `REGISTRY[key](...)`
        if isinstance(func, ast.Subscript):
            sel = _text(func.slice)
            cands, resolution, reason = _candidates_of_container(func.value, consts)
            out.append(
                DispatchSite(
                    rel,
                    getattr(node, "lineno", 0),
                    sel,
                    _is_model_expr(func.slice, model_names),
                    cands,
                    resolution,
                    reason,
                    "subscript",
                )
            )
            continue
        # (2) `REGISTRY.get(key)(...)` / `getattr(obj, key)(...)`
        if isinstance(func, ast.Call):
            inner = func
            iname = dotted_of(inner.func) or ""
            if iname.split(".")[-1] in ("get", "getattr") and inner.args:
                sel_node = inner.args[-1]
                container = inner.args[0] if iname.split(".")[-1] == "getattr" else inner.func
                base = container.value if isinstance(container, ast.Attribute) else container
                cands, resolution, reason = _candidates_of_container(base, consts)
                out.append(
                    DispatchSite(
                        rel,
                        getattr(node, "lineno", 0),
                        _text(sel_node),
                        _is_model_expr(sel_node, model_names),
                        cands,
                        resolution,
                        reason,
                        "get" if iname.endswith("get") else "getattr",
                    )
                )
    # (3) `if name == "x": tool_x(...)` の連鎖
    out += _if_chain_sites(fn, rel, model_names)
    # (4) `match name: case GitTools.STATUS: ...`（Def 4 の「解決済みレジストリ上の match」）
    out += _match_sites(fn, rel, model_names)
    return out


def _candidates_of_container(
    container: ast.AST, consts: dict[str, ast.Dict]
) -> tuple[tuple[str, ...], str, Optional[str]]:
    if isinstance(container, ast.Name) and container.id in consts:
        d = consts[container.id]
        cands = tuple(sorted({dotted_of(v) or "<expr>" for v in d.values}))
        return cands, "resolved", None
    if isinstance(container, ast.Dict):
        cands = tuple(sorted({dotted_of(v) or "<expr>" for v in container.values}))
        return cands, "resolved", None
    return (), "opaque", "dynamic_registry"


def _if_chain_sites(fn: ast.AST, rel: str, model_names: set[str]) -> list[DispatchSite]:
    """`if name == "x": f(...)` / `elif name in (...)` の連鎖を dispatch とみなす。"""
    out: list[DispatchSite] = []
    for node in ast.walk(fn):
        if not isinstance(node, ast.If):
            continue
        sel = _selector_of_test(node.test)
        if sel is None:
            continue
        if not _is_model_expr(node.test, model_names):
            continue
        callees = sorted(
            {
                dotted_of(c.func)
                for c in ast.walk(ast.Module(body=node.body, type_ignores=[]))
                if isinstance(c, ast.Call) and dotted_of(c.func)
            }
        )
        out.append(
            DispatchSite(
                rel,
                getattr(node, "lineno", 0),
                sel,
                True,
                tuple(c for c in callees if c),
                "resolved" if callees else "opaque",
                None if callees else "dynamic_registry",
                "if_chain",
            )
        )
    return out


def _match_sites(fn: ast.AST, rel: str, model_names: set[str]) -> list[DispatchSite]:
    """`match <sel>: case <定数>:` を dispatch とみなす（Def 4）。

    これを落とすと `mcp-server-git` のような `match name:` 形の低レベル
    ハンドラで trig が常に `assumed` になり、SELECT 座標が原理的に発火しない。
    """
    match_cls = getattr(ast, "Match", None)
    if match_cls is None:  # pragma: no cover - 3.10 未満
        return []
    out: list[DispatchSite] = []
    for node in ast.walk(fn):
        if not isinstance(node, match_cls):
            continue
        if not _is_model_expr(node.subject, model_names):
            continue
        for case in node.cases:
            if not _is_constant_pattern(case.pattern):
                continue
            callees = sorted(
                {
                    dotted_of(c.func)
                    for c in ast.walk(ast.Module(body=case.body, type_ignores=[]))
                    if isinstance(c, ast.Call) and dotted_of(c.func)
                }
            )
            out.append(
                DispatchSite(
                    rel,
                    getattr(case.pattern, "lineno", getattr(node, "lineno", 0)),
                    _text(node.subject),
                    True,
                    tuple(c for c in callees if c),
                    "resolved" if callees else "opaque",
                    None if callees else "dynamic_registry",
                    "match",
                )
            )
    return out


def _is_constant_pattern(pattern: ast.AST) -> bool:
    """`case "x":` / `case Enum.MEMBER:` のように**定数へ解決できる**パターンか。

    `case _:` や捕捉パターンは候補集合を決めないので dispatch に数えない。
    """
    mv = getattr(ast, "MatchValue", None)
    ms = getattr(ast, "MatchSingleton", None)
    mo = getattr(ast, "MatchOr", None)
    if mv is not None and isinstance(pattern, mv):
        return isinstance(pattern.value, (ast.Constant, ast.Attribute, ast.Name))
    if ms is not None and isinstance(pattern, ms):
        return True
    if mo is not None and isinstance(pattern, mo):
        return all(_is_constant_pattern(p) for p in pattern.patterns)
    return False


def _selector_of_test(test: ast.AST) -> Optional[str]:
    if isinstance(test, ast.Compare) and test.ops:
        if isinstance(test.ops[0], (ast.Eq, ast.In)):
            return _text(test.left)
    return None


def _text(node: ast.AST) -> str:
    try:
        return ast.unparse(node)
    except Exception:  # pragma: no cover
        return "<expr>"
