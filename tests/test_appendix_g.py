"""B3b: 付録 G の G1–G15 を `(verdict, reason クラス, witness 行番号)` で 15/15。

§2.5.6 の受け入れ条件。期待値は `fixtures/gates/expected.json`（採点器より先に
コミットされたもの）。**このテストが落ちたら実装を直す。期待値を直さない。**
"""

import json
import os

import pytest

from authgap.gateharness import analyze_case

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURES = os.path.join(ROOT, "fixtures", "gates")

with open(os.path.join(FIXTURES, "expected.json"), encoding="utf-8") as fh:
    EXPECTED = json.load(fh)["cases"]


@pytest.mark.parametrize("case", sorted(EXPECTED))
def test_appendix_g(case):
    spec = EXPECTED[case]
    res = analyze_case(
        FIXTURES,
        case,
        spec["file"],
        spec["effect_line"],
        spec["coordinate"],
        frozenset(spec.get("not_entries", ())),
    )
    assert res.verdict == spec["verdict"], f"{case}: {spec['hole']}"
    assert res.reason == spec["reason"], f"{case}: reason クラス"
    if spec["witness_line"] is not None:
        assert res.witness_line == spec["witness_line"], f"{case}: witness 行"
    if spec.get("grade") is not None:
        assert res.grade == spec["grade"], f"{case}: 等級"


def test_all_fifteen_present():
    assert len(EXPECTED) == 15, "付録 G は 15 件（§2.5.6 B3b）"
