"""較正対の両側条件の回帰（コーパスが取得済みのときだけ走る）。

`corpus/` は gitignore なので、新規クローンでは skip される。
取得は `python scripts/fetch_corpus.py --spec docs/corpus_spec.json`。

**このテストが pin しているのは「変化が出ること」であって、仕様書に書かれた
期待タプルの文字列ではない。** 仕様書の A1/A2 の脆弱側は一次確認の結果
誤っていた（`docs/open_questions.md` Q8）。ここでは一次確認した値を pin する。
"""

import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from scripts.two_sided import compare  # noqa: E402

PAIRS = [
    # (pair_id, 変化が出る slot, 脆弱側の等級, 修正側の等級, 最低限の変化サイト数)
    ("A1", "cwd", None, "strong-path", 8),
    ("A2", "argv[*]", None, "strong-token", 2),
]


def _roots(pair: str) -> tuple[str, str]:
    return (
        os.path.join(ROOT, "corpus", f"{pair}__vuln"),
        os.path.join(ROOT, "corpus", f"{pair}__fixed"),
    )


@pytest.mark.parametrize("pair,slot,vuln_grade,fixed_grade,min_sites", PAIRS)
def test_two_sided_pair(pair, slot, vuln_grade, fixed_grade, min_sites):
    v, f = _roots(pair)
    if not (os.path.isdir(v) and os.path.isdir(f)):
        pytest.skip(f"{pair}: コーパス未取得（scripts/fetch_corpus.py）")
    res = compare(pair, v, f, "mcp_server")
    assert res.two_sided, f"{pair}: 両側条件を満たさない"
    hits = [
        c
        for c in res.changed
        if f"#{slot} " in c["site"]
        and c["vuln"]["grade"] == vuln_grade
        and c["fixed"]["grade"] == fixed_grade
    ]
    assert len(hits) >= min_sites, (
        f"{pair}: {slot} の等級変化 {vuln_grade} -> {fixed_grade} が "
        f"{len(hits)} 件（期待 >= {min_sites}）"
    )
    # 副次指標（必須併記）: verdict が GAP から外れた行があること。
    assert res.verdict_clearing, f"{pair}: verdict-clearing が 0"


def test_only_one_sided_sites_are_reported():
    """片側にしかない効果サイトは**数えないが報告する**（黙って落とさない）。"""
    v, f = _roots("A1")
    if not (os.path.isdir(v) and os.path.isdir(f)):
        pytest.skip("コーパス未取得")
    res = compare("A1", v, f, "mcp_server")
    assert isinstance(res.only_vuln, list)
    assert isinstance(res.only_fixed, list)
