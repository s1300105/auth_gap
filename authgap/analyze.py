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
from .catalog.sinks import DANGEROUS_KINDS, PRIMARY_SLOTS
from .cfgbuild import build_cfg
from .dominance import compute_dominators
from .dparse import DKind, DOp, parse_d_kind
from .effects import Effect, EffectExtractor
from .entries import Unit
from .gate import GateCandidate, SummaryCache, find_gate_candidates, score_gates
from .ir import RESOLVED, DomKind, Prin, Prov, Req, Value, prov_merge, req_meet
from .srcindex import Scope, SourceIndex
from .trig import TrigIndex, TrigResult
from .val import Options, ValEngine, ValResult, seed_model_param
from .verdict import Row, UnitVerdictInput, decide

#: LLM 戻り値（R1）の root id の前置き。
R1_ROOT_PREFIX = "llm:"


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

    seed = _seed(unit)
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


def _seed(unit: Unit) -> dict[str, Value]:
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
        seed["self"] = Value(Prin.OP, RESOLVED, Obj((cls,), ()))
    return seed


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
) -> UnitReport:
    """F0a に支配判定・等級・判定を足す。"""
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

    # -- req_occ（**効果ごと**。Def 5 は `req_occ(e)` と書く）-----------------
    selector_roots = _selector_roots(unit, report)
    for i, e in enumerate(report.effects):
        nodes = cfg.nodes_for_line(e.entry_lineno) or [cfg.exit]
        sc = score_gates(cfg, dom, cands, nodes, "occ", selector_roots)
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
        sc = score_gates(cfg, dom, cands, nodes, "val", value.roots)
        report.req_val[(i, slot)] = sc.req
        report.gate_results[(i, slot)] = sc.to_json()
        report.grades[(i, slot)] = _grade_of(sc.passing, sc.candidates, value)  # noqa: E501

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
        for name in c.subjects:
            v = env.get(name)
            if v is not None:
                roots |= v.roots
        c.subject_roots = frozenset(roots)


def _grade_of(
    passing: list[GateCandidate], candidates: list[GateCandidate], value: Value
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
            best = c.value_grade
    if weak_reason is not None:
        V.validate_weak_reason(weak_reason)
        return "weak", weak_reason
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
