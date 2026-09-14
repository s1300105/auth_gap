"""ユニット単位の解析パイプライン。

    R2 入口 → val（値）→ effects（制御位置）→ CFG/支配 → gate（等級）→ Def 7（判定）

**F0a と F0b を分ける**（§6）。

* :func:`analyze_unit_f0a` — **支配判定に依存しない床**。ユニットごとの危険効果
  kind の真偽値、構文的 validator 形状、config atom と既定値、annotation の有無、
  **ゲート述語の存在（支配判定なし）**。
* :func:`analyze_unit_full` — F0a + 支配判定 + 等級 + 判定。

root id は**入口引数の名前**を使う。解析はユニット単位なので局所で一意であり、
ゲート述語の AST 名と直接照合できる（主語一致が名前の書き換えを跨げる）。
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from typing import Any, Optional

from .catalog import validators as V
from .catalog.entries import APPROVAL_INTERRUPTS
from .catalog.sinks import DANGEROUS_KINDS, PRIMARY_SLOTS
from .cfgbuild import build_cfg
from .dominance import compute_dominators
from .dparse import DKind, DOp, parse_d_kind
from .effects import Effect, EffectExtractor
from .entries import (
    Unit,  # noqa: F401
    params_of,
)
from .gate import GateCandidate, GateScore, SummaryCache, find_gate_candidates, score_gates
from .ir import RESOLVED, DomKind, DomResult, Prin, Prov, Req, Value, prov_merge, req_meet
from .srcindex import Scope, SourceIndex, dotted_of
from .trig import TrigIndex, TrigResult
from .val import Env, Options, ValEngine, ValResult, seed_model_param
from .verdict import Row, UnitVerdictInput, decide

#: LLM 戻り値（R1）の root id の前置き。
R1_ROOT_PREFIX = "llm:"

#: §3 の 3 腕アブレーション。**3 腕は同一バイナリのフラグ違いでなければならない**
#: （別実装なら不合格）。ゲートは 3 腕とも入っている。
#:
#: * ``A`` — trig を計算し、**val を全位置で OP に固定**する（INJECT が出ない）
#: * ``B`` — val を計算し、**trig を全て assumed に固定**する（SELECT が出ない）
#: * ``C`` — 完全版
ARMS = ("A", "B", "C")


@dataclass
class UnitReport:
    """1 ユニットの解析結果。**手で読める形で全部出す。**"""

    unit: Unit
    effects: list[Effect] = field(default_factory=list)
    val: Optional[ValResult] = None
    #: F0a: 構文的 validator 形状（§6 の 11 語。支配判定なし）。
    validator_shapes: tuple[str, ...] = ()
    #: F0a: ゲート述語の存在（支配判定なし）。
    gate_predicate_present: bool = False
    #: F0a: 読んだ config atom（名前 → 既定が閉か）。
    config_atoms: dict[str, Optional[bool]] = field(default_factory=dict)
    d_kind: DKind = field(default_factory=DKind)
    trig: Optional[TrigResult] = None
    req_occ: Req = Req.MODEL
    #: `(effect index, slot) -> req_val`
    req_val: dict[tuple[int, str], Req] = field(default_factory=dict)
    #: `(effect index, slot) -> (等級, weak 理由)`
    grades: dict[tuple[int, str], tuple[Optional[str], Optional[str]]] = field(default_factory=dict)
    #: `(effect index, slot) -> ゲートの 3 値`
    gate_results: dict[tuple[int, str], dict] = field(default_factory=dict)
    #: `effect index -> req_occ`（**`req_occ(e)` は効果ごと**。Def 5）
    req_occ_by_effect: dict[int, Req] = field(default_factory=dict)
    occ_gate: Optional[dict] = None
    #: `effect index -> req_occ のゲート 3 値`
    occ_gate_by_effect: dict[int, dict] = field(default_factory=dict)
    rows: list[Row] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    # -- 集計用 ------------------------------------------------------------

    @property
    def has_dangerous_effect(self) -> bool:
        return any(e.kind in DANGEROUS_KINDS for e in self.effects)

    def control_positions(self, primary_only: bool = False) -> list[tuple[int, str, Value]]:
        out: list[tuple[int, str, Value]] = []
        for i, e in enumerate(self.effects):
            for slot, v in sorted(e.control_slots().items()):
                if primary_only and slot not in PRIMARY_SLOTS:
                    continue
                out.append((i, slot, v))
        return out

    def resolution_counts(self) -> dict[str, int]:
        counts = {"resolved": 0, "opaque": 0, "remote": 0}
        for e in self.effects:
            counts[e.resolution.kind] += 1
        return counts

    def to_json(self) -> dict:
        d: dict[str, Any] = {
            "unit": self.unit.to_json(),
            "effects": [e.to_json() for e in self.effects],
            "validator_shapes": list(self.validator_shapes),
            "gate_predicate_present": self.gate_predicate_present,
            "config_atoms": dict(sorted(self.config_atoms.items())),
            "D_kind": self.d_kind.to_json(),
            "req_occ": self.req_occ.name,
            "req_occ_by_effect": {str(i): r.name for i, r in sorted(self.req_occ_by_effect.items())},
            "gate_occ_by_effect": {str(i): g for i, g in sorted(self.occ_gate_by_effect.items())},
            "req_val": {f"{i}:{s}": r.name for (i, s), r in sorted(self.req_val.items())},
            "grades": {
                f"{i}:{s}": {"grade": g, "weak_reason": w}
                for (i, s), (g, w) in sorted(self.grades.items())
            },
            "gate": {f"{i}:{s}": g for (i, s), g in sorted(self.gate_results.items())},
            "rows": [r.to_json() for r in self.rows],
            "notes": sorted(set(self.notes)),
        }
        if self.trig is not None:
            d["trig"] = self.trig.to_json()
        if self.occ_gate is not None:
            d["gate_occ"] = self.occ_gate
        if self.val is not None:
            d["alias_facts"] = [a.to_json() for a in self.val.alias_facts]
            d["opaque_reasons"] = sorted(set(self.val.opaque_reasons))
            d["cap_hits"] = sorted(set(self.val.cap_hits))
            if self.val.loop_unstable:
                d["loop_unstable"] = list(self.val.loop_unstable)
        return d


# --------------------------------------------------------------------------
# F0a: 支配判定に依存しない床
# --------------------------------------------------------------------------


def analyze_unit_f0a(
    index: SourceIndex, unit: Unit, options: Optional[Options] = None
) -> UnitReport:
    """支配判定を使わずに測れるものだけを出す（§6 F0a）。"""
    report = UnitReport(unit=unit)
    path = index.resolve_module_path(unit.module)
    if path is None:
        report.notes.append("module unresolved")
        return report
    scope = index.function_scope(path, unit.node)

    seed = _seed(unit, index)
    extractor = EffectExtractor()
    engine = ValEngine(index, options or Options(), on_call=extractor.on_call)
    report.val = engine.analyze(unit.node, scope, seed)
    report.effects = extractor.effects
    _mark_shape_from(report, unit)

    shapes, _ = _syntactic_shapes(unit.node, scope)
    report.validator_shapes = tuple(sorted(shapes))
    report.gate_predicate_present = _gate_predicate_present(index, unit, scope)
    report.config_atoms = _config_atoms(index, unit, scope)
    report.d_kind = parse_d_kind(unit)
    return report


def _seed(unit: Unit, index: Optional[SourceIndex] = None) -> dict[str, Value]:
    """R2 が与える MODEL 引数と、メソッドの受け手を種付ける。"""
    from .ir import Atom, Obj

    seed: dict[str, Value] = {}
    for p in unit.params:
        if p.excluded:
            seed[p.name] = Value(Prin.OP, RESOLVED, Atom(formal=p.name))
            continue
        seed[p.name] = seed_model_param(p.name, p.name, p.annotation)
    if unit.qualname.count(".") >= 1:
        cls = unit.qualname.split(".")[0]
        fields = _self_fields(index, cls, unit.module) if index is not None else ()
        seed["self"] = Value(Prin.OP, RESOLVED, Obj((cls,), fields))
    if index is not None:
        for name, v in _closure_seed(index, unit).items():
            seed.setdefault(name, v)
    if unit.message_param:
        # langroid 形: MODEL 値は `ToolMessage` 派生クラスのフィールドにある。
        fields = tuple(
            (
                name,
                seed_model_param(f"{unit.message_param}.{name}", f"{unit.message_param}.{name}", ann),
            )
            for name, ann in unit.message_fields
        )
        seed[unit.message_param] = Value(
            Prin.OP, RESOLVED, Obj((unit.message_class or "ToolMessage",), fields)
        )
    return seed


def _closure_seed(index: SourceIndex, unit: Unit) -> dict[str, Value]:
    """入れ子関数の入口が掴む、外側の関数の仮引数を種付ける（D17）。

    `def register(mcp, store: Store): @mcp.tool() def post(text): store.post(text)` の
    `store` は入口の仮引数ではないので種が無く、受け手型が付かずに sink を落としていた
    （野外 NOE[11]、false-clean）。**MODEL にはしない**（ツール引数ではない）。
    注釈が木内クラス（同じモジュールか import 先）なら `Obj((C,), fields)`、それ以外は
    注釈の文字列から形だけを種付ける。外側の関数の本体で代入された自由変数は扱わない。
    """
    from .ir import Obj
    from .val.engine import _seed_from_annotation

    out: dict[str, Value] = {}
    parent_qual = unit.qualname.rpartition(".")[0]
    if not parent_qual:
        return out
    parents = [f for f in index.lookup_function(parent_qual, unit.module) if f.module == unit.module]
    if len(parents) != 1:
        return out
    fn_args = getattr(parents[0].node, "args", None)
    if fn_args is None:
        return out
    own = {p.name for p in unit.params}
    path = index.resolve_module_path(unit.module)
    mscope = index.module_scope(path) if path is not None else None
    for a in list(fn_args.posonlyargs) + list(fn_args.args) + list(fn_args.kwonlyargs):
        if a.arg in own or a.arg in ("self", "cls"):
            continue
        cd = _annotated_class(index, a.annotation, unit.module, mscope)
        if cd is not None:
            out[a.arg] = Value(Prin.OP, RESOLVED, Obj((cd.name,), _self_fields(index, cd.name, cd.module)))
        else:
            out[a.arg] = _seed_from_annotation(a)
    return out


def _annotated_class(index: SourceIndex, ann: Optional[ast.AST], module: str, mscope: Optional[Scope]):
    """注釈が指す木内クラス（同じモジュールか import 先）。**名前だけで引かない。**"""
    if isinstance(ann, ast.Constant) and isinstance(ann.value, str):
        text: Optional[str] = ann.value.strip()
    else:
        text = dotted_of(ann) if ann is not None else None
    if not text:
        return None
    head, _, rest = text.partition(".")
    last = text.split(".")[-1]
    target = mscope.lookup(head) if mscope is not None else None
    if target is not None:
        full = f"{target}.{rest}" if rest else target
        mod = full.rpartition(".")[0]
        # 外部パッケージを末尾成分一致で木内モジュールと取り違えない（D17 改訂 2）
        mname = index.resolve_import_module(module, mod)
        return index.get_class(last, mname, strict=True) if mname else None
    return index.get_class(last, module, strict=True)


#: `__init__` の解析結果を使い回すための記憶化。
_SELF_FIELD_CACHE: dict[tuple[int, str, str], tuple] = {}


def _self_fields(
    index: SourceIndex, classname: str, module: str
) -> tuple[tuple[str, Value], ...]:
    """`self.<name>` に書かれた値を集めて `Obj.fields` にする（§2.6）。

    **クラス体のフィールド既定値と `__init__` の両方を見る。**
    これが無いと `self.conn.execute(...)` のような受け手が解決できず、
    proxy sink（DB / HTTP / git）が 1 つも当たらない。

    受け手アクセスパスの深さは 2 までで、それ以上は `opaque(receiver)`
    （val エンジンの規則をそのまま使う）。
    """
    key = (id(index), module, classname)
    if key in _SELF_FIELD_CACHE:
        return _SELF_FIELD_CACHE[key]
    _SELF_FIELD_CACHE[key] = ()  # 再帰の打ち切り
    cd = index.get_class(classname, module)
    if cd is None:
        return ()
    path = index.resolve_module_path(cd.module)
    if path is None:
        return ()

    from .ir import Atom, Obj

    fields: dict[str, Value] = {}
    scope = index.module_scope(path)
    engine = ValEngine(index)

    # (1) クラス体のフィールド既定値
    body_res = ValResult()
    env = Env({"self": Value(Prin.OP, RESOLVED, Obj((classname,), ()))})
    class_body = [n for n in cd.node.body if isinstance(n, (ast.Assign, ast.AnnAssign))]
    engine._exec_body(class_body, env, scope, body_res, 1, (classname,))
    for name, v in env.items():
        if not name.startswith("self."):
            fields.setdefault(name[len("self.") :], v)
    for node in class_body:
        target = None
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
        elif isinstance(node, ast.AnnAssign):
            target = node.target
        if isinstance(target, ast.Name) and node.value is not None:
            fields.setdefault(target.id, engine._eval(node.value, env, scope, body_res, 1, ()))

    # (2) `__init__` の本体
    for fd in index.lookup_function(f"{classname}.__init__", cd.module):
        init_scope = index.function_scope(path, fd.node)
        init_env = Env({"self": Value(Prin.OP, RESOLVED, Obj((classname,), ()))})
        for p in params_of(fd.node):
            init_env.set(p.name, Value(Prin.OP, RESOLVED, Atom(formal=p.name)))
        init_res = ValResult()
        engine._exec_body(getattr(fd.node, "body", []), init_env, init_scope, init_res, 1, (classname,))
        for name, v in init_env.items():
            if name.startswith("self."):
                fields[name[len("self.") :]] = v
        break

    out = tuple(sorted(fields.items()))
    _SELF_FIELD_CACHE[key] = out
    return out


def _mark_shape_from(report: UnitReport, unit: Unit) -> None:
    """注釈由来の shape を使った位置に `shape_from = annotation` を記録する。"""
    annotated = {p.name for p in unit.params if p.annotation}
    for e in report.effects:
        for slot, v in e.control_slots().items():
            if v.roots & annotated:
                e.shape_from[slot] = "annotation"


def _syntactic_shapes(fn: ast.AST, scope: Scope) -> tuple[set[str], set[str]]:
    """§6 F0a の構文的 validator 形状（11 語）。**支配判定を使わない。**"""
    from .gate import _shapes_in

    return _shapes_in(fn, scope)


def _gate_predicate_present(index: SourceIndex, unit: Unit, scope: Scope) -> bool:
    """F0a: ゲート述語の**存在**（支配判定なし）。"""
    cfg = build_cfg(unit.node)
    cands = find_gate_candidates(cfg, scope, index)
    return any(c.recognition in ("A-a", "A-b", "A-c", "V") for c in cands)


def _config_atoms(index: SourceIndex, unit: Unit, scope: Scope) -> dict[str, Optional[bool]]:
    cfg = build_cfg(unit.node)
    out: dict[str, Optional[bool]] = {}
    for c in find_gate_candidates(cfg, scope, index):
        if c.atom is not None:
            out[c.atom.name] = c.atom.default_closed
    return out


# --------------------------------------------------------------------------
# F0b + 判定
# --------------------------------------------------------------------------


def analyze_unit_full(
    index: SourceIndex,
    unit: Unit,
    trig_index: TrigIndex,
    d_op: DOp,
    rubric_1c: frozenset[str] = frozenset(),
    exposure_supplied: bool = False,
    prev_unit: Optional[dict] = None,
    options: Optional[Options] = None,
    arm: str = "C",
) -> UnitReport:
    """F0a に支配判定・等級・判定を足す。

    :param arm: §3 の 3 腕（``A`` / ``B`` / ``C``）。**同一の解析経路を通り、
        座標を 1 つずつ止めるだけ**である。腕ごとに別の実装を書いてはならない。
    """
    if arm not in ARMS:
        raise ValueError(f"未知の腕: {arm!r}")
    report = analyze_unit_f0a(index, unit, options)
    if report.val is None:
        return report
    path = index.resolve_module_path(unit.module)
    assert path is not None
    scope = index.function_scope(path, unit.node)

    cfg = build_cfg(unit.node)
    dom = compute_dominators(cfg)
    cands = find_gate_candidates(cfg, scope, index, 0, SummaryCache(index))
    _attach_subject_roots(cands, report.val)

    report.trig = trig_index.trig_for(unit)
    if arm == "B":
        # 腕 B: trig を全て assumed に固定する（SELECT 座標を止める）。
        report.trig = TrigResult(report.trig.label, "assumed", None)
    if arm == "A":
        # 腕 A: val を全位置で OP に固定する（INJECT 座標を止める）。
        # **効果行そのものは残す**（ゲートも残る）。座標だけを止める。
        for e in report.effects:
            for slot, v in list(e.slots.items()):
                e.slots[slot] = Value(Prin.OP, v.prov, v.shape, v.attrs, v.roots)

    # -- req_occ（**効果ごと**。Def 5 は `req_occ(e)` と書く）-----------------
    # デコレータ形の承認割り込み（`@require_approval(risk_level=...)` など）は
    # 関数全体を包むので、その関数の**すべての効果**をゲートする。
    # CFG 上の呼び出しではないので、候補探索とは別に見る必要がある。
    decorator_approval = _decorator_approval(unit)
    selector_roots = _selector_roots(unit, report)
    for i, e in enumerate(report.effects):
        nodes = cfg.nodes_for_line(e.entry_lineno) or [cfg.exit]
        sc = score_gates(cfg, dom, cands, nodes, "occ", selector_roots)
        if decorator_approval is not None and arm != "A":
            name, lineno = decorator_approval
            sc = GateScore(
                DomResult(DomKind.DOM, None, Req.USER, f"decorator:{name}@L{lineno}"),
                Req.USER,
                sc.candidates,
                sc.passing,
                sc.per_copy,
                sc.notes + [f"decorator_approval:{name}"],
            )
        report.req_occ_by_effect[i] = sc.req
        report.occ_gate_by_effect[i] = sc.to_json()
    dangerous_idx = [i for i, e in enumerate(report.effects) if e.kind in DANGEROUS_KINDS]
    if dangerous_idx:
        # ユニット水準の `req_occ` は危険効果の**最弱**（⊓。攻撃者が最弱を選ぶ）。
        report.req_occ = req_meet(*(report.req_occ_by_effect[i] for i in dangerous_idx))
        weakest = min(dangerous_idx, key=lambda i: report.req_occ_by_effect[i])
        report.occ_gate = report.occ_gate_by_effect[weakest]

    # -- req_val（制御位置ごと）-------------------------------------------
    for i, slot, value in report.control_positions():
        nodes = cfg.nodes_for_line(report.effects[i].entry_lineno) or [cfg.exit]
        # root が空 = 定数 / OP 由来。**「主語が無い」のであって「未知」ではない**
        # ので、どの値検証も束縛しない番兵を渡す（空集合を渡すと主語一致が
        # 素通りして無関係な検証が等級として表示される）。
        subjects = value.roots or frozenset({"<no-root>"})
        sc = score_gates(cfg, dom, cands, nodes, "val", subjects)
        report.req_val[(i, slot)] = sc.req
        report.gate_results[(i, slot)] = sc.to_json()
        report.grades[(i, slot)] = _grade_of(sc.passing, sc.candidates, value, report.effects[i])

    from .dparse import drift as _drift

    drift_reasons = tuple(
        _drift(prev_unit, {"effects": [e.to_json() for e in report.effects], "req_occ": report.req_occ.name})
    )

    report.rows = decide(
        UnitVerdictInput(
            unit_id=unit.unit_id,
            tool_name=unit.tool_name,
            effects=report.effects,
            trig_label=report.trig.label,
            trig_mode=report.trig.mode,
            req_occ=report.req_occ,
            req_val=report.req_val,
            grades=report.grades,
            d_kind=report.d_kind,
            d_op=d_op,
            drift_reasons=drift_reasons,
            opaque_reasons=tuple(sorted(set(report.val.opaque_reasons))),
            exposure_supplied=exposure_supplied,
            rubric_1c_names=rubric_1c,
        )
    )
    return report


def _is_argv_exec(effect: Optional[Effect]) -> bool:
    """効果が argv 実行（`shell=False`）か。判定できなければ偽（**推定で strong にしない**）。"""
    if effect is None:
        return False
    if effect.kind != "SPAWN":
        return True  # SPAWN 以外に argv 条件は無い
    shell = effect.exec_mode.get("shell", {})
    return shell.get("const") is False or shell.get("source") == "proxy"


#: デコレータ形の承認割り込み名（Def 5 の語彙のうち `decorator` 形）。
_DECORATOR_APPROVALS: frozenset[str] = frozenset(
    r.name for r in APPROVAL_INTERRUPTS if r.form == "decorator"
)


def _decorator_approval(unit: Unit) -> Optional[tuple[str, int]]:
    """ユニットの関数に承認割り込みデコレータが付いているか。

    付いていればその関数の**すべての効果**が `req_occ = USER` になる。
    A9（PraisonAI の `@require_approval(risk_level="high")`）がこの形。
    """
    for d in getattr(unit.node, "decorator_list", []):
        target = d.func if isinstance(d, ast.Call) else d
        name = dotted_of(target)
        if name and name.split(".")[-1] in _DECORATOR_APPROVALS:
            return name, getattr(d, "lineno", getattr(unit.node, "lineno", 0))
    return None


def _selector_roots(unit: Unit, report: UnitReport) -> frozenset[str]:
    """セレクタ（ディスパッチキー）に流れる値の root 集合。

    ユニット本体の中で **dispatch キーの位置に現れる式**の名前を集め、
    val の env で root へ写す。低レベル MCP ハンドラの `name` 引数がこれに当たる。

    dispatch キーの位置は Def 4 が限定する 3 形だけを見る:
    `REGISTRY[<sel>]` / `<x>.get(<sel>)` / `if <sel> == "..."`（`in` を含む）。
    **一般分岐は見ない。**
    """
    if report.val is None or report.val.env is None:
        return frozenset()
    names: set[str] = set()
    for node in ast.walk(unit.node):
        if isinstance(node, ast.Subscript) and isinstance(node.ctx, ast.Load):
            names |= _plain_names(node.slice)
        elif isinstance(node, ast.Call):
            callee = getattr(node.func, "attr", None)
            if callee in ("get", "getattr") and node.args:
                names |= _plain_names(node.args[-1])
        elif isinstance(node, ast.Compare) and node.ops:
            if isinstance(node.ops[0], (ast.Eq, ast.In)):
                if all(isinstance(c, (ast.Constant, ast.Tuple, ast.List, ast.Set)) for c in node.comparators):
                    names |= _plain_names(node.left)
    roots: set[str] = set()
    for n in names:
        v = report.val.env.get(n)
        if v is not None:
            roots |= v.roots
    return frozenset(roots)


def _plain_names(node: ast.AST) -> set[str]:
    return {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}


def _entry_effect_nodes(cfg, report: UnitReport) -> list[int]:
    """`req_occ` を採点する対象ノード（危険効果の行すべて）。"""
    out: list[int] = []
    for e in report.effects:
        if e.kind in DANGEROUS_KINDS:
            out += cfg.nodes_for_line(e.entry_lineno)
    return sorted(set(out)) or [cfg.exit]


def _attach_subject_roots(cands: list[GateCandidate], val: ValResult) -> None:
    """ゲート述語のオペランドの root 集合を env から引いて付ける。

    **主語一致を root で取れるようにする**ためのもの。root は名前の書き換え
    （`safe = validate_path(path)`）を跨いで保たれる。
    """
    env = val.env
    if env is None:
        return
    for c in cands:
        roots: set[str] = set()
        for expr in c.subject_exprs:
            roots |= _roots_of_expr(expr, env)
        if not roots:
            for name in c.subjects:
                v = env.get(name)
                if v is not None:
                    roots |= v.roots
        c.subject_roots = frozenset(roots)


def _roots_of_expr(node, env) -> frozenset[str]:
    """式から root 集合を取る。**添字は root を精緻化する。**

    `arguments["branch_name"]` を `{arguments}` に潰すと、別の引数への検証が
    同じ root に見え、Def 5 が禁じている型エラー（無関係な検証が別の位置の
    判定を動かす）が主語一致をすり抜ける。
    """
    if isinstance(node, ast.Name):
        v = env.get(node.id)
        return v.roots if v is not None else frozenset()
    if isinstance(node, ast.Attribute):
        from .val import access_path

        p = access_path(node)
        if p is not None:
            v = env.get(p)
            if v is not None:
                return v.roots
        return _roots_of_expr(node.value, env)
    if isinstance(node, ast.Subscript):
        base = _roots_of_expr(node.value, env)
        idx = node.slice
        if isinstance(idx, ast.Constant) and isinstance(idx.value, str) and base:
            return frozenset(f'{r}["{idx.value}"]' for r in base)
        return base
    if isinstance(node, ast.Call):
        out: set[str] = set()
        for a in node.args:
            out |= _roots_of_expr(a, env)
        if isinstance(node.func, ast.Attribute):
            out |= _roots_of_expr(node.func.value, env)
        return frozenset(out)
    out2: set[str] = set()
    for sub in ast.iter_child_nodes(node) if node is not None else ():
        out2 |= _roots_of_expr(sub, env)
    return frozenset(out2)


def _grade_of(
    passing: list[GateCandidate],
    candidates: list[GateCandidate],
    value: Value,
    effect: Optional[Effect] = None,
) -> tuple[Optional[str], Optional[str]]:
    """位置の等級と weak 理由。**strong は推定で出さない。**

    通過したゲートに strong があればそれ。無く、weak を持つ候補があれば
    `weak(reason)`。どちらも無ければ `(None, None)`（検証が無い）。

    **主語一致しない候補は等級に寄与しない。** 寄与させると、無関係な引数への
    allowlist が当該位置の等級として表示され、Def 5 が禁じている型エラー
    （無関係な検証がツール全体の判定を動かす）が manifest の見た目に現れる。
    """
    best: Optional[str] = None
    weak_reason: Optional[str] = None
    for c in passing:
        if c.value_grade == "strong-token":
            # Def 5 の strong-token は 3 条件目に **argv 実行（shell=False）** を
            # 要求する。検証子の本体からは分からないので効果側で確かめる。
            if _is_argv_exec(effect):
                return "strong-token", None
            return "unknown", None
        if c.value_grade and c.value_grade.startswith("strong"):
            return c.value_grade, None
    # **主語一致しない候補は等級に寄与しない。** 位置の値に root が無い
    # （定数 / OP 由来）なら、どの値検証もその位置には束縛されない。
    bound = [c for c in candidates if c.form == "value" and (c.subject_roots & value.roots)]
    for c in bound:
        if c.value_grade == "weak" and c.weak_reason:
            if weak_reason is None:
                weak_reason = c.weak_reason
                best = "weak"
        elif c.value_grade in ("allowlist", "unknown") and best is None:
            # **`allowlist` は Def 5 の等級語彙に無い。** 語彙外の等級を作らない。
            # 会員判定は req の引き上げ（config atom 規則）で効き、等級としては
            # `unknown`（判定不能）にとどめる。どの候補が束縛したかは
            # manifest の `gate.candidates[]` に残る。
            # SQL 文型 allowlist のような形に Def 5 の等級が無いことは
            # `docs/open_questions.md` Q10 に記録した。
            best = "unknown"
    if weak_reason is not None:
        V.validate_weak_reason(weak_reason)
        return "weak", weak_reason
    if best is not None and best not in V.GRADES:
        raise ValueError(f"Def 5 の等級語彙にない等級: {best!r}")
    return best, None


# --------------------------------------------------------------------------
# 木全体
# --------------------------------------------------------------------------


@dataclass
class TreeReport:
    """1 つの解析対象木の結果。"""

    src_root: str
    population: str
    units: list[UnitReport] = field(default_factory=list)
    parse_failures: list[str] = field(default_factory=list)
    cap_hits: list[tuple[str, str, int]] = field(default_factory=list)
    trig_index: Optional[TrigIndex] = None
    d_op: Optional[DOp] = None
    n_tool_literals: int = 0
    n_annotation_joined: int = 0
    n_annotation_unjoined: int = 0

    def resolution_counts(self) -> dict[str, int]:
        out = {"resolved": 0, "opaque": 0, "remote": 0}
        for u in self.units:
            for k, v in u.resolution_counts().items():
                out[k] += v
        return out

    def in_tree_resolution_ratio(self) -> Optional[float]:
        """`resolved / (resolved + opaque + remote)`（§1 の効果サイトの解決率）。"""
        c = self.resolution_counts()
        total = c["resolved"] + c["opaque"] + c["remote"]
        return c["resolved"] / total if total else None

    def opaque_ratio(self, primary_only: bool = True) -> Optional[float]:
        """`opaque な制御位置 / (resolved + opaque な制御位置)`。

        **`remote` は分母に入れない**（別行の報告値）。省略された既定引数の
        slot は分母に入れない（`control_positions` が返さない）。
        """
        resolved = opaque = 0
        for u in self.units:
            for _i, _slot, v in u.control_positions(primary_only=primary_only):
                if v.prov.kind == "opaque":
                    opaque += 1
                elif v.prov.kind == "resolved":
                    resolved += 1
        total = resolved + opaque
        return opaque / total if total else None


def merge_prov(*ps: Prov) -> Prov:
    return prov_merge(*ps)


def gate_verdict_counts(report: TreeReport) -> dict[str, int]:
    """OPAQUE / NODOM の内訳（§6 の指標）。**合計と NODOM 件数を必ず並記する。**"""
    counts: dict[str, int] = {}
    for u in report.units:
        for g in u.gate_results.values():
            v = g["gate"]["verdict"]
            key = v if v == "DOM" else f"{v}({g['gate'].get('reason')})"
            counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items()))


__all__ = [
    "DomKind",
    "TreeReport",
    "UnitReport",
    "analyze_unit_f0a",
    "analyze_unit_full",
    "gate_verdict_counts",
]
