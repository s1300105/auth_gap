"""§2.5.5 の不動点と、`score_gates` の直接計算が一致することを確かめる。

仕様書は `req(e)` を前向きデータフローの最小不動点で定義する。実装は同値な
直接計算（`⊔ over passing gates`）を使う。同値性の根拠は「(G-i) に支配が
含まれるので、`gates(n,e)` を満たす n は e へのすべての経路上にある」こと。

**根拠が正しいことを毎回の実行で確かめる。** ここが割れたら直接計算が
使えないので `score_gates` を不動点版に差し替える。
"""

import json
import os

import pytest

from authgap.cfgbuild import build_cfg, build_comprehension_cfg
from authgap.dominance import compute_dominators
from authgap.gate import SummaryCache, find_gate_candidates, req_by_fixpoint, score_gates
from authgap.gateharness import (
    comprehension_containing,
    effect_call,
    enclosing_function,
    origin_closure,
    selector_names,
    value_names,
)
from authgap.srcindex import SourceIndex

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASES = []
for sub in ("fixtures/gates", "fixtures/dominance_mutants"):
    d = os.path.join(ROOT, sub)
    with open(os.path.join(d, "expected.json"), encoding="utf-8") as fh:
        for case, spec in json.load(fh)["cases"].items():
            if spec["file"].endswith(".py") and spec["effect_line"]:
                CASES.append((d, case, spec))


@pytest.mark.parametrize("directory,case,spec", CASES, ids=[c[1] for c in CASES])
def test_direct_equals_fixpoint(directory, case, spec):
    index = SourceIndex(directory)
    index.build()
    path = os.path.join(directory, spec["file"])
    tree = index.parse(path)
    assert tree is not None
    fn = enclosing_function(tree, spec["effect_line"])
    assert fn is not None
    scope = index.function_scope(path, fn)
    comp = comprehension_containing(fn, spec["effect_line"])
    if comp is not None:
        cfg = build_comprehension_cfg(comp)
        effect_nodes = [n for n, nd in cfg.nodes.items() if nd.label == "comp-elt"]
    else:
        cfg = build_cfg(fn)
        effect_nodes = cfg.nodes_for_line(spec["effect_line"])
    dom = compute_dominators(cfg)
    call = effect_call(fn, spec["effect_line"])
    coord = spec["coordinate"]
    names = selector_names(call, fn) if coord == "occ" else value_names(call)
    subjects = origin_closure(fn, names)
    cands = find_gate_candidates(cfg, scope, index, 0, SummaryCache(index))
    score = score_gates(cfg, dom, cands, effect_nodes, coord, subjects)
    fixed = req_by_fixpoint(cfg, dom, score.passing, effect_nodes)
    assert score.req == fixed, f"{case}: 直接計算 {score.req} != 不動点 {fixed}"


def test_lattice_laws():
    """2 つの束を混同していないことの単体確認。"""
    from authgap.ir import Prin, Req, prin_join, req_join, req_meet

    # P: USER ⊑ OP ⊑ MODEL、join は MODEL 方向。
    assert prin_join(Prin.USER, Prin.MODEL) is Prin.MODEL
    assert prin_join(Prin.USER, Prin.OP) is Prin.OP
    # P^op: MODEL < OP < USER。⊔ は経路上で最強、⊓ は経路集合で最弱。
    assert req_join(Req.MODEL, Req.USER) is Req.USER
    assert req_meet(Req.MODEL, Req.USER) is Req.MODEL
    # ゲート無し = bottom = MODEL
    assert req_join() is Req.MODEL
