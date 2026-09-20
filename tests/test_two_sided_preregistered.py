"""両側通過率の分子を、事前登録した期待タプル（`docs/expected_tuples.json`）と照合する。

**期待は `docs/cve_triage.csv` の `expected_tuple_change`（一次確認済みの散文）を
機械可読に転記した `docs/expected_tuples.json` から取り、修正より先にコミットする**
（`CLAUDE.md` 規則 5。`docs/preregistration.md` §5 #2 の判別実験 (a)）。

現行の `scripts/two_sided.py` は **8 座標のどれか 1 つでも値が違えば「通過」**
とする（any-change）。`cve_triage.csv` の `expected_tuple_change` を読むコードは
0 件（`grep` で確認）。その結果:

* `open` → `Path.read_text` に書き換えただけの対（検証は両側とも weak のまま）が通過する
* **修正版 → 脆弱版の逆向きの対**が通過する

「事前登録どおりに変化する」（仕様書 §6 :821）という主指標の文言を実装が
担保していない。ここでは `pass_preregistered`（向きつきの照合）を期待し、
現行の値は `pass_any_change` として併記する（両方を報告する。片方だけ出さない）。

`corpus/` は gitignore なので、未取得なら skip する
（`scripts/fetch_corpus.py --spec docs/corpus_spec.json`）。
"""

from __future__ import annotations

import json
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from scripts.two_sided import compare  # noqa: E402

#: 同じ対を何度も解析しない（A9 は 1 回に数分かかる）。キーに expected も入れる。
_CACHE: dict[tuple, object] = {}


def _cmp(pair_id: str, v: str, f: str, pop: str, **kw):
    key = (pair_id, v, f, pop, json.dumps(kw, sort_keys=True, default=str))
    if key not in _CACHE:
        _CACHE[key] = compare(pair_id, v, f, pop, **kw)
    return _CACHE[key]


#: cf75fd7 で `DEFECT`（xfail strict）として置き、実装で 7 対 + 逆向き 4 対 + noop が XPASS に
#: なったので印を外した。A18 だけは期待表の転記誤り（`docs/preregistration.md` §5 #5）で
#: 落ち、記録つきで表を直した。以後は回帰テストである。

EXPECTED = json.load(open(os.path.join(ROOT, "docs", "expected_tuples.json"), encoding="utf-8"))["pairs"]


def _roots(spec: dict) -> tuple[str, str]:
    return (os.path.join(ROOT, "corpus", spec["vuln"]), os.path.join(ROOT, "corpus", spec["fixed"]))


def _need(spec: dict) -> None:
    v, f = _roots(spec)
    if not (os.path.isdir(v) and os.path.isdir(f)):
        pytest.skip("コーパス未取得（scripts/fetch_corpus.py --spec docs/corpus_spec.json）")


# --------------------------------------------------------------------------
# 前提テスト（印なし）
# --------------------------------------------------------------------------


def test_precondition_expected_tuples_cover_the_scored_pairs():
    """期待表が `docs/corpus_spec.json` の対（+ A9 と修正コミットを共有する A10）を覆う。"""
    spec = json.load(open(os.path.join(ROOT, "docs", "corpus_spec.json"), encoding="utf-8"))
    scored = {t["name"].split("@")[0] for t in spec["targets"]}
    assert scored | {"A10"} == set(EXPECTED), f"corpus_spec={sorted(scored)} expected={sorted(EXPECTED)}"


@pytest.mark.parametrize("pair", sorted(EXPECTED))
def test_precondition_every_change_has_direction(pair):
    """各 change が from / to / coord / min_sites を持つ（向きの無い期待は書けない）。"""
    for c in EXPECTED[pair]["changes"]:
        assert {"coord", "from", "to", "min_sites"} <= set(c), f"{pair}: {c}"
        assert c["from"] != c["to"], f"{pair}: from と to が同じ（変化を期待していない）: {c}"


@pytest.mark.parametrize("pair", sorted(EXPECTED))
def test_precondition_any_change_still_passes(pair):
    """現行の any-change は 7/7（+A10）で通っている。**この値は併記として残す。**"""
    _need(EXPECTED[pair])
    v, f = _roots(EXPECTED[pair])
    res = _cmp(pair, v, f, EXPECTED[pair]["population"])
    assert res.two_sided, f"{pair}: any-change でも通らない（コーパスか解析器が変わった）"


# --------------------------------------------------------------------------
# 1. 事前登録どおりの変化で通ること
# --------------------------------------------------------------------------


@pytest.mark.parametrize("pair", sorted(EXPECTED))
def test_preregistered_direction_passes(pair):
    """`pass_preregistered` が `docs/expected_tuples.json` の向きつき照合で True。"""
    _need(EXPECTED[pair])
    v, f = _roots(EXPECTED[pair])
    res = _cmp(pair, v, f, EXPECTED[pair]["population"])
    assert res.pass_preregistered is True, f"{pair}: {getattr(res, 'preregistered_misses', None)}"


@pytest.mark.parametrize("pair", sorted(EXPECTED))
def test_any_change_is_reported_alongside(pair):
    """3 列（厳密一致 / 座標一致 / any-change）が**併記**される。片方だけ出さない。

    `docs/preregistration.md` §5 #2 (a) の文言: 「厳密一致 / 座標一致 / any-change の
    3 列を出す」。座標一致は「期待した座標が期待した位置で動いた」だけを見て、
    値の向きは問わない（厳密一致 ⊆ 座標一致 ⊆ any-change）。
    """
    _need(EXPECTED[pair])
    v, f = _roots(EXPECTED[pair])
    res = _cmp(pair, v, f, EXPECTED[pair]["population"])
    assert isinstance(res.pass_any_change, bool)
    assert res.pass_any_change == res.two_sided
    assert isinstance(res.pass_coord_match, bool)
    # 包含関係。厳密に通るなら座標も通り、座標が通るなら any-change も通る。
    if res.pass_preregistered:
        assert res.pass_coord_match
    if res.pass_coord_match:
        assert res.pass_any_change


# --------------------------------------------------------------------------
# 2. 逆向きの対は通らないこと（**現行 any-change は通してしまう**）
# --------------------------------------------------------------------------


@pytest.mark.parametrize("pair", ("A1", "A2", "A4", "A10"))
def test_reversed_pair_does_not_pass_preregistered(pair):
    """修正版を脆弱側に、脆弱版を修正側に置いた対は `pass_preregistered` が False。

    any-change は「値が違う」だけを見るので逆向きでも通る。**向きを見ない指標は
    『修正を検出した』と読めない。** A1 / A2 / A4 / A10 はいずれも grade が
    none / weak → strong に変わる対で、逆向きなら strong → none / weak になる。
    """
    _need(EXPECTED[pair])
    v, f = _roots(EXPECTED[pair])
    res = _cmp(pair + "-reversed", f, v, EXPECTED[pair]["population"], expected=EXPECTED[pair])
    assert res.pass_any_change is True, "前提: any-change は逆向きでも通る（それが問題）"
    assert res.pass_preregistered is False


# --------------------------------------------------------------------------
# 3. 事前登録に無い座標が動いても通らないこと
# --------------------------------------------------------------------------


def test_unrelated_coordinate_change_does_not_pass_preregistered(tmp_path):
    """検証を足さずに `open` を `Path.read_text` に置き換えただけの対。

    `site` 座標（sink の名前）は変わるが、事前登録した変化（grade / req_val）は
    起きていない。any-change は通し、`pass_preregistered` は通してはいけない。
    """
    import textwrap

    head = "from pathlib import Path\nfrom mcp.server.fastmcp import FastMCP\nmcp = FastMCP('t')\nROOT = '/srv'\n"
    vuln = head + textwrap.dedent('''
        @mcp.tool()
        def read(path: str) -> str:
            if not path.startswith(ROOT):
                raise ValueError(path)
            with open(path) as f:
                return f.read()
    ''')
    fixed = head + textwrap.dedent('''
        @mcp.tool()
        def read(path: str) -> str:
            if not path.startswith(ROOT):
                raise ValueError(path)
            return Path(path).read_text()
    ''')
    (tmp_path / "v").mkdir()
    (tmp_path / "f").mkdir()
    (tmp_path / "v" / "server.py").write_text(vuln, encoding="utf-8")
    (tmp_path / "f" / "server.py").write_text(fixed, encoding="utf-8")
    res = compare("noop", str(tmp_path / "v"), str(tmp_path / "f"), "mcp_server")
    # 事前登録の無い対なので、期待表を明示的に渡す（grade が weak → strong-path になるべき、という偽の期待）。
    res2 = compare(
        "noop",
        str(tmp_path / "v"),
        str(tmp_path / "f"),
        "mcp_server",
        expected={"changes": [{"slot": "path", "coord": "grade", "from": "weak", "to": "strong-path", "min_sites": 1}]},
    )
    assert res.pass_any_change is True or res2.pass_any_change is True
    assert res.pass_preregistered is None, "期待表に無い対は None（未測定）。False にして安全側に倒さない"
    assert res2.pass_preregistered is False
