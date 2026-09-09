"""語彙の凍結を実装レベルで守る。

* validator 形状は 11 語（§6 F0a が唯一の定義点）
* weak 理由は 19 語（Def 5。月 6 凍結）
* OPAQUE はゲート側 8 語 / val 側 8 語で**別語彙**
* NODOM は 4 語。**語彙外の理由を新設してはならない**
"""

import hashlib
import os

import pytest

from authgap.catalog import validators as V
from authgap.ir import (
    GATE_NODOM_REASONS,
    GATE_OPAQUE_REASONS,
    VAL_OPAQUE_REASONS,
    DomKind,
    DomResult,
    Prov,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_shape_vocabulary_is_eleven():
    assert len(V.SHAPE_NAMES) == 11
    # A1 の修正版は Path.resolve と relative_to だけで構成される。
    # 旧語彙（この 2 つを欠く）では脈拍が A1 を判別できない。
    assert V.shape_for_method("resolve") == "realpath"
    assert V.shape_for_method("relative_to") == "containment"


def test_weak_reason_vocabulary_is_nineteen():
    assert len(V.WEAK_REASONS) == 19
    assert "self_granted" not in V.WEAK_REASONS, "self_granted は格下げ属性であり weak 理由ではない"
    with pytest.raises(ValueError):
        V.validate_weak_reason("absolute_only")


def test_every_weak_reason_has_witness():
    assert set(V.WITNESS_TEMPLATES) == set(V.WEAK_REASONS)


def test_opaque_vocabularies_are_separate():
    assert len(VAL_OPAQUE_REASONS) == 8
    assert len(GATE_OPAQUE_REASONS) == 8
    assert VAL_OPAQUE_REASONS != GATE_OPAQUE_REASONS
    # 同じ語が両方に現れるが、混ぜて集計してはならない。
    assert {"depth", "unresolved"} <= VAL_OPAQUE_REASONS & GATE_OPAQUE_REASONS
    assert "dynamic_registry" in GATE_OPAQUE_REASONS
    assert "dynamic_registry" not in VAL_OPAQUE_REASONS


def test_nodom_vocabulary_is_four():
    assert GATE_NODOM_REASONS == {"no_gate", "deny_reaches_effect", "non_binding_gate", "alt_entry"}


def test_vocabulary_is_enforced_at_construction():
    """語彙外の理由は**作れない**。実装レベルで新設を止める。"""
    with pytest.raises(ValueError):
        DomResult(DomKind.NODOM, "made_up_reason")
    with pytest.raises(ValueError):
        DomResult(DomKind.OPAQUE, "made_up_reason")
    with pytest.raises(ValueError):
        Prov("opaque", ("dynamic_registry",))  # ゲート側語彙を val 側に入れない
    with pytest.raises(ValueError):
        Prov("resolved", ("depth",))  # resolved が理由を持ってはならない


def test_prin_has_no_unknown():
    from authgap.ir import Prin

    assert {p.name for p in Prin} == {"USER", "OP", "MODEL"}


def test_preludes_identical():
    """付録 G と支配 mutant は同一の前置きを使う（比較可能性のため）。"""
    a = hashlib.sha256(open(os.path.join(ROOT, "fixtures/gates/_prelude.py"), "rb").read()).hexdigest()
    b = hashlib.sha256(
        open(os.path.join(ROOT, "fixtures/dominance_mutants/_prelude.py"), "rb").read()
    ).hexdigest()
    assert a == b, "2 つの _prelude.py が食い違っている。cp で揃えること"
