"""B3a: 支配のみを問う 8 mutant を 8/8 撃破。

(1)-(5) と (8) は「非支配と判定されるべき形」であり、**1 件でも支配と判定したら
不合格**。(6) と (7) は支配規則ではなくハーネスの性質を突くので、期待値は
「非支配」に加えて該当行（`parse_failure` / `TRUNCATED` + `OPAQUE(cfg_cap)`）が
出力されることであり、行が出なければ不合格とする。
"""

import json
import os

import pytest

from authgap.gateharness import analyze_case

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURES = os.path.join(ROOT, "fixtures", "dominance_mutants")

with open(os.path.join(FIXTURES, "expected.json"), encoding="utf-8") as fh:
    EXPECTED = json.load(fh)["cases"]


@pytest.mark.parametrize("case", sorted(EXPECTED))
def test_mutant_not_dominating(case):
    spec = EXPECTED[case]
    res = analyze_case(FIXTURES, case, spec["file"], spec["effect_line"], spec["coordinate"])
    assert res.verdict != spec["not_verdict"], f"{case}: {spec['hole']} を支配と誤判定した"
    for need in spec.get("requires_rows", []):
        assert need in res.rows, f"{case}: 行 {need!r} が出ていない（{res.rows}）"


def test_all_eight_present():
    assert len(EXPECTED) == 8, "支配 mutant は 8 件（§2.5.6 B3a）"
