"""付録 G / 支配 mutant を採点するためのハーネス。

`fixtures/gates/` と `fixtures/dominance_mutants/` の各ケースについて
`(verdict, reason クラス, witness 行)` の 3 つ組を出す（§2.5.6 の受け入れ条件）。

**このハーネスは受け入れ条件の実装であって、期待値の出所ではない。**
期待値は `expected.json`（`scripts/gen_expected.py` が仕様書の表と
fixture のマーカーから生成）にある。

付録 G の慣習をここで明文化する:

* 囲み関数は注記が無い限りユニット入口とする。
* 唯一の例外は G14 の `run_shell` で、これは R2 のカタログ化エントリでは
  ないのでユニット入口として数えない（`expected.json` の `not_entries`）。
"""

from __future__ import annotations

import ast
import os
import shutil
import tempfile
from dataclasses import dataclass, field
from typing import Optional

from .cfgbuild import CFG, build_cfg, build_comprehension_cfg
from .dominance import compute_dominators
from .gate import GateCandidate, GateScore, SummaryCache, find_gate_candidates, module_constants, score_gates
from .ir import REQ_BOTTOM, DomKind, DomResult
from .srcindex import SourceIndex, dotted_of


@dataclass
class CaseResult:
    """1 ケースの採点結果。手で読める形で全部出す。"""

    case: str
    file: str
    effect_line: Optional[int]
    coordinate: str
    score: Optional[GateScore] = None
    #: 効果に対応する CFG ノード（`finally` 複製で複数になりうる）。
    effect_nodes: list[int] = field(default_factory=list)
    subjects: frozenset[str] = frozenset()
    #: ディスパッチ候補集合の解決結果。
    dispatch_resolution: str = "n/a"
    dispatch_candidates: list[str] = field(default_factory=list)
    #: 出力されるべき追加行（`parse_failure` / `TRUNCATED` / `OPAQUE(cfg_cap)`）。
    rows: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def verdict(self) -> Optional[str]:
        return self.score.result.kind.value if self.score else None

    @property
    def reason(self) -> Optional[str]:
        return self.score.result.reason if self.score else None

    @property
    def witness(self) -> Optional[str]:
        return self.score.result.witness if self.score else None

    @property
    def witness_line(self) -> Optional[int]:
        w = self.witness
        if not w:
            return None
        # "L14" / "finally-copy(exc) @ L14"
        tail = w.rsplit("L", 1)[-1]
        return int(tail) if tail.isdigit() else None

    @property
    def grade(self) -> Optional[str]:
        if self.score and self.score.result.grade is not None:
            return self.score.result.grade.name
        return None

    def to_json(self) -> dict:
        return {
            "case": self.case,
            "file": self.file,
            "effect_line": self.effect_line,
            "coordinate": self.coordinate,
            "verdict": self.verdict,
            "reason": self.reason,
            "grade": self.grade,
            "witness": self.witness,
            "witness_line": self.witness_line,
            "effect_nodes": self.effect_nodes,
            "subjects": sorted(self.subjects),
            "dispatch_resolution": self.dispatch_resolution,
            "dispatch_candidates": sorted(self.dispatch_candidates),
            "rows": sorted(set(self.rows)),
            "score": self.score.to_json() if self.score else None,
            "notes": sorted(set(self.notes)),
        }


# --------------------------------------------------------------------------
# 効果の位置づけ
# --------------------------------------------------------------------------


def enclosing_function(tree: ast.Module, lineno: int) -> Optional[ast.AST]:
    """その行を含む最も内側の関数定義。"""
    best: Optional[ast.AST] = None
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        start = node.lineno
        end = getattr(node, "end_lineno", None) or start
        if start <= lineno <= end:
            if best is None or node.lineno > best.lineno:  # type: ignore[attr-defined]
                best = node
    return best


def comprehension_containing(fn: ast.AST, lineno: int) -> Optional[ast.AST]:
    """効果行が内包表記 / genexp の要素式の中にあるなら、その内包表記を返す。

    内包表記のフィルタ `if` は要素式をゲートするが、外側の CFG では
    「文 1 個 = ノード 1 個」なのでゲートと効果が同一ノードに潰れる。
    §2.5.1 はそのために別 CFG を要求している。
    """
    for node in ast.walk(fn):
        if not isinstance(node, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
            continue
        elt = getattr(node, "elt", None) or getattr(node, "value", None)
        if elt is None:
            continue
        start = getattr(elt, "lineno", None)
        end = getattr(elt, "end_lineno", None) or start
        if start is not None and start <= lineno <= end:
            return node
    return None


def calls_at_line(fn: ast.AST, lineno: int) -> list[ast.Call]:
    out = [
        n for n in ast.walk(fn) if isinstance(n, ast.Call) and getattr(n, "lineno", None) == lineno
    ]
    return sorted(out, key=lambda c: c.col_offset)


def effect_call(fn: ast.AST, lineno: int) -> Optional[ast.Call]:
    """その行の**効果**にあたる呼び出し式。

    最も外側の呼び出しを採ると `out.append(TOOLS[name](args))` で `out.append`
    を効果と見なしてしまい、セレクタが `out` になる（G10 がこれで落ちる）。
    したがって **dispatch 形（被呼び出しが `Subscript`）を最優先**し、
    無ければ最も外側を採る。
    """
    calls = calls_at_line(fn, lineno)
    if not calls:
        return None
    for c in calls:
        if isinstance(c.func, ast.Subscript):
            return c
    return calls[0]


def selector_names(call: Optional[ast.Call], fn: Optional[ast.AST] = None) -> frozenset[str]:
    """効果の**発生**を決める値に相当する名前（`req_occ` の主語）。

    2 段で決める:

    1. 被呼び出しが `Subscript`（`TOOLS[name](args)`）なら、その添字がセレクタ。
    2. そうでなければ、**ユニット入口の仮引数のうち効果の実引数に現れないもの**を
       セレクタとする。g15 の `dispatch(name, argstr)` で `git_log(argstr)` を
       呼ぶ形がこれで、`name` がセレクタ、`argstr` が制御位置の値である。

    2 の規則は「セレクタ」を機械的に決めるための運用定義であり、
    val エンジンが入ったら「MODEL ラベルを持ちどの slot にも入らない入口引数」に
    置き換える（`docs/open_questions.md` に記録）。
    """
    if call is None:
        return frozenset()
    func = call.func
    if isinstance(func, ast.Subscript):
        return _names(func.slice)
    if fn is not None:
        params = _param_names(fn)
        used = value_names(call)
        rest = params - used
        if rest:
            return frozenset(rest)
    if isinstance(func, ast.Name):
        return frozenset({func.id})
    if isinstance(func, ast.Attribute):
        return _names(func)
    return frozenset()


def _param_names(fn: ast.AST) -> frozenset[str]:
    args = getattr(fn, "args", None)
    if args is None:
        return frozenset()
    out: set[str] = set()
    for a in list(args.posonlyargs) + list(args.args) + list(args.kwonlyargs):
        if a.arg not in ("self", "cls"):
            out.add(a.arg)
    if args.vararg:
        out.add(args.vararg.arg)
    if args.kwarg:
        out.add(args.kwarg.arg)
    return frozenset(out)


def value_names(call: Optional[ast.Call]) -> frozenset[str]:
    """効果の制御位置に届く値に相当する名前（`req_val` の主語）。"""
    if call is None:
        return frozenset()
    out: set[str] = set()
    for a in call.args:
        out |= set(_names(a))
    for kw in call.keywords:
        out |= set(_names(kw.value))
    return frozenset(out)


def _names(node: ast.AST) -> frozenset[str]:
    out: set[str] = set()
    for sub in ast.walk(node):
        if isinstance(sub, ast.Name):
            out.add(sub.id)
        elif isinstance(sub, ast.Attribute):
            d = dotted_of(sub)
            if d:
                out.add(d)
    return frozenset(out)


def origin_closure(fn: ast.AST, names: frozenset[str]) -> frozenset[str]:
    """前向き def-use の逆をたどって、その値の由来になった名前を集める。

    `safe = validate_path(path, ROOT)` のとき `{safe}` から `{safe, path, ROOT}`
    を得る。**これは val エンジンの `Roots` の暫定版である。** val が入ったら
    `Value.roots` に置き換える（`docs/open_questions.md` に記録）。
    """
    out = set(names)
    changed = True
    while changed:
        changed = False
        for node in ast.walk(fn):
            targets: list[ast.AST] = []
            value: Optional[ast.AST] = None
            if isinstance(node, ast.Assign):
                targets, value = list(node.targets), node.value
            elif isinstance(node, ast.AnnAssign) and node.value is not None:
                targets, value = [node.target], node.value
            elif isinstance(node, ast.withitem) and node.optional_vars is not None:
                targets, value = [node.optional_vars], node.context_expr
            if value is None:
                continue
            for t in targets:
                if _names(t) & out:
                    new = _names(value)
                    if not new <= out:
                        out |= new
                        changed = True
    return frozenset(out)


# --------------------------------------------------------------------------
# ディスパッチ候補集合の解決（§2.5.4）
# --------------------------------------------------------------------------


def _lookup_const(name: str, tree: ast.Module, scope, index: SourceIndex):
    """モジュール定数を、当該モジュール → import 元の木内モジュールの順に引く。"""
    consts = module_constants(tree)
    if name in consts:
        return consts[name]
    dotted = scope.lookup(name) if scope is not None else None
    if dotted:
        mod = dotted.rsplit(".", 1)[0] if "." in dotted else dotted
        path = index.resolve_module_path(mod)
        if path:
            other = index.parse(path)
            if other is not None:
                return module_constants(other).get(dotted.rsplit(".", 1)[-1])
    return None


def resolve_dispatch(
    call: Optional[ast.Call], fn: ast.AST, tree: ast.Module, index: SourceIndex, scope=None
) -> tuple[str, list[str], Optional[str], Optional[int]]:
    """DISPATCH の候補集合を解決する。

    :returns: `(resolution, candidates, opaque_reason, 解決に失敗した行)`。
        `resolution` は ``"resolved"`` / ``"opaque"`` / ``"n/a"``。

    **解決できない場合は `OPAQUE(dynamic_registry)`。決して drop しない。**
    """
    if call is None:
        return "n/a", [], None, None
    func = call.func

    if isinstance(func, ast.Subscript):
        base = func.value
        if isinstance(base, ast.Name):
            init = _lookup_const(base.id, tree, scope, index)
            if isinstance(init, ast.Dict):
                cands = [dotted_of(v) or ast.dump(v) for v in init.values]
                return "resolved", cands, None, None
        return "opaque", [], "dynamic_registry", getattr(call, "lineno", None)

    if isinstance(func, ast.Name):
        # 局所変数に束縛された被呼び出し。束縛元を見る。
        rhs = _last_binding(fn, func.id)
        if rhs is None:
            if index.lookup_function(func.id):
                return "n/a", [func.id], None, None
            return "n/a", [], None, None
        if isinstance(rhs, ast.Call):
            callee = dotted_of(rhs.func) or ""
            if callee.endswith(".get") or callee.startswith("getattr"):
                base = callee.rsplit(".", 1)[0] if "." in callee else ""
                head = base.split(".")[0] if base else ""
                init = _lookup_const(head, tree, scope, index) if head else None
                if isinstance(init, ast.Dict):
                    return "resolved", [dotted_of(v) or ast.dump(v) for v in init.values], None, None
        return "opaque", [], "dynamic_registry", getattr(rhs, "lineno", None)
    return "n/a", [], None, None


def _last_binding(fn: ast.AST, name: str) -> Optional[ast.AST]:
    found: Optional[ast.AST] = None
    for node in ast.walk(fn):
        if isinstance(node, ast.Assign) and node.value is not None:
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == name:
                    found = node.value
    return found


# --------------------------------------------------------------------------
# 入口の列挙と alt_entry
# --------------------------------------------------------------------------


def top_level_functions(tree: ast.Module) -> list[ast.AST]:
    out: list[ast.AST] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            out.append(node)
        elif isinstance(node, ast.ClassDef):
            for sub in node.body:
                if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    out.append(sub)
    return out


def detect_alt_entry(
    tree: ast.Module,
    this_fn: ast.AST,
    callee_names: frozenset[str],
    index: SourceIndex,
    scope,
    not_entries: frozenset[str],
) -> tuple[bool, Optional[str]]:
    """同一の効果本体に、ゲートを持つ**別の**ユニット入口が在るか（§2.5.4 / G14）。

    在る場合、この入口の行の NODOM 理由は `no_gate` ではなく `alt_entry` になる。
    「別の入口から無ガードで届く」ことこそが報告したい事実だからである。

    :returns: `(在るか, 別入口のゲートの witness)`
    """
    if not callee_names:
        return False, None
    from .dominance import gates as _gates

    short = {n.split(".")[-1] for n in callee_names}
    for fn in top_level_functions(tree):
        if fn is this_fn or getattr(fn, "name", None) in not_entries:
            continue
        cfg = build_cfg(fn)
        targets = _calls_to(cfg, short)
        if not targets:
            continue
        dom = compute_dominators(cfg)
        for c in find_gate_candidates(cfg, scope, index):
            if c.recognition not in ("A-a", "A-b", "A-c"):
                continue
            if all(_gates(cfg, dom, c.node, t, c.raises_form).ok for t in targets):
                return True, cfg.nodes[c.witness_node or c.node].witness()
    return False, None


def _calls_to(cfg: CFG, names: set[str]) -> list[int]:
    out: list[int] = []
    for nid, node in cfg.nodes.items():
        src = node.ast_node or node.test_expr
        if src is None:
            continue
        for sub in ast.walk(src):
            if isinstance(sub, ast.Call):
                d = dotted_of(sub.func)
                if d and d.split(".")[-1] in names:
                    out.append(nid)
                    break
    return sorted(out)


# --------------------------------------------------------------------------
# ケースの採点
# --------------------------------------------------------------------------


def analyze_case(
    fixture_dir: str,
    case: str,
    filename: str,
    effect_line: Optional[int],
    coordinate: str,
    not_entries: frozenset[str] = frozenset(),
) -> CaseResult:
    """1 ケースを採点する。"""
    index = SourceIndex(fixture_dir)
    index.build()
    res = CaseResult(case=case, file=filename, effect_line=effect_line, coordinate=coordinate)

    path = os.path.join(fixture_dir, filename)
    if filename.endswith(".broken"):
        # parse 失敗の mutant。**索引を通して読ませる。**
        # ここで `ast.parse` を直に呼ぶと、SourceIndex の失敗記録が試験されず、
        # 「parse 失敗の記録を削除する」実装変異が生き残ってしまう。
        with tempfile.TemporaryDirectory() as tmp:
            shutil.copy(os.path.join(fixture_dir, "_prelude.py"), os.path.join(tmp, "_prelude.py"))
            dest = os.path.join(tmp, filename[: -len(".broken")])
            shutil.copy(path, dest)
            tmp_index = SourceIndex(tmp)
            tmp_index.build()
            tree = tmp_index.parse(dest)
            if tree is None and tmp_index.parse_failures:
                res.rows.append("parse_failure")
                res.score = GateScore(DomResult(DomKind.NODOM, "no_gate"), REQ_BOTTOM)
                res.notes.append("parse 失敗。**黙って捨てず行として出す。**")
            else:
                res.notes.append("parse に成功してしまった（または失敗が記録されなかった）")
        return res

    tree = index.parse(path)
    if tree is None:
        res.rows.append("parse_failure")
        res.score = GateScore(DomResult(DomKind.NODOM, "no_gate"), REQ_BOTTOM)
        return res

    assert effect_line is not None, f"{case}: # EFFECT マーカーが無い"
    fn = enclosing_function(tree, effect_line)
    assert fn is not None, f"{case}: 効果行 {effect_line} を含む関数が無い"

    scope = index.function_scope(path, fn)
    comp = comprehension_containing(fn, effect_line)
    if comp is not None:
        # §2.5.1: 内包表記 / genexp は合成した無名関数として**別 CFG**。
        # 外側の CFG では 1 文 1 ノードなのでゲートと効果が同一ノードになり、
        # 支配関係が存在しない（G7 はこの別 CFG の上でしか採点できない）。
        cfg = build_comprehension_cfg(comp)
        res.notes.append("内包表記の別 CFG で採点した（§2.5.1）")
    else:
        cfg = build_cfg(fn)
    dom = compute_dominators(cfg)
    if cfg.opaque:
        res.rows.append("TRUNCATED")
        for r in cfg.opaque:
            res.rows.append(f"OPAQUE({r})")

    if comp is not None:
        effect_nodes = [n for n, node in cfg.nodes.items() if node.label == "comp-elt"]
    else:
        effect_nodes = cfg.nodes_for_line(effect_line)
    if not effect_nodes:
        res.notes.append("効果行に対応する CFG ノードが無い")
        return res
    res.effect_nodes = effect_nodes

    call = effect_call(fn, effect_line)
    resolution, cands, opaque_reason, opaque_line = resolve_dispatch(call, fn, tree, index, scope)
    res.dispatch_resolution = resolution
    res.dispatch_candidates = [c for c in cands]

    if coordinate == "occ":
        subjects = origin_closure(fn, selector_names(call, fn))
    else:
        subjects = origin_closure(fn, value_names(call))
    res.subjects = subjects

    summaries = SummaryCache(index)
    candidates: list[GateCandidate] = find_gate_candidates(cfg, scope, index, 0, summaries)

    callee_names = frozenset(cands) if resolution == "resolved" else frozenset()
    alt, alt_witness = (
        detect_alt_entry(tree, fn, callee_names, index, scope, not_entries)
        if callee_names
        else (False, None)
    )

    path_opaque = tuple(cfg.opaque) + ((opaque_reason,) if opaque_reason else ())
    opaque_witness = f"L{opaque_line}" if opaque_line else None
    if not opaque_witness and cfg.opaque:
        opaque_witness = f"L{effect_line}"
    res.score = score_gates(
        cfg,
        dom,
        candidates,
        effect_nodes,
        coordinate,
        subjects,
        path_opaque=path_opaque,
        alt_entry=alt,
        opaque_witness=opaque_witness,
        alt_entry_witness=alt_witness,
    )
    return res


__all__ = [
    "CaseResult",
    "analyze_case",
    "enclosing_function",
    "origin_closure",
    "effect_call",
    "resolve_dispatch",
    "selector_names",
    "value_names",
]
