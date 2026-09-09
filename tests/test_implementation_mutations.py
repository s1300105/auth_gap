"""実装変異試験（§2.5.6）。**生存 ≤ 2** が受け入れ条件。

前身の比較値: 56 テスト時代の実装変異 15 件中 9〜10 件が生存（監査 §1.5
stage2-guard-5）。監査応答でテストは 99 件に増えたが監査自身が変異試験を
再実施していないため **HEAD での生存数は未知**である。

生存数は**付録 G と支配 mutant の fixture テストだけ**で計算する（§2.5.6 の
定義どおり）。fixture 外の単体テストを足して生存数を下げない。
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from scripts.mutation_test import MUTATIONS, failing_cases  # noqa: E402


def test_baseline_is_clean():
    assert failing_cases() == [], "変異を入れる前から期待値と食い違っている"


def test_survival_within_budget():
    survived = []
    for name, _desc, factory in MUTATIONS:
        with factory():
            if not failing_cases():
                survived.append(name)
    assert len(survived) <= 2, f"生存 {len(survived)}/15: {survived}"


def test_known_survivor_is_documented():
    """既知の生存は 1 件だけであり、理由が文書に記録されていること。

    `no_finally_copies` が生存するのは、`(G-i)∧(G-ii)` が同じ誤りを先に
    捕まえるため、G12 の 3 つ組（verdict, reason, witness）が複製の有無で
    変わらないからである。複製が変えるのは効果行に対応する CFG ノードの**個数**
    （2 対 1）と witness の脱出種別表記であって、付録 G の受け入れ条件は
    そこを見ていない。**これは fixture 集合の被覆の穴であり、隠さず記録する。**

    複製の性質そのものは `tests/test_cfg_structure.py` が構造的に固定するが、
    **その単体テストは生存数の計算に入れない**（§2.5.6 の定義を動かさない）。
    """
    doc = os.path.join(ROOT, "docs", "decisions.md")
    assert os.path.exists(doc), "docs/decisions.md が無い"
    with open(doc, encoding="utf-8") as fh:
        text = fh.read()
    assert "no_finally_copies" in text
    assert "1/15" in text, "生存数の報告値が記録されていない"
