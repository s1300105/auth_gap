"""D_prev 層（Def 6 の第 4 層 + Def 7 の `GAP_DRIFT`）の配線。

**期待は仕様 Def 6 / Def 7 の文言から書き、修正より先にコミットする**
（`CLAUDE.md` 規則 5。`tests/test_f0a_defects.py` と同じ型）。

仕様 `AUTHGAP_BRIEF_v3.md` Def 6 の D_prev:

* D_kind / D_dom / D_op がいずれも `⊥` のユニットについて、直前リリースの
  manifest を D とする: `D_prev(u) := M_{r-1}(u)`。
* **join は unit id の完全一致のみ。**
* 差分規則: `GAP_DRIFT(u, e) ⇔ e の kind が M_{r-1}(u) に無い、または制御位置 p の
  val が OP から MODEL になった、または req_occ / req_val の等級が下がった`。
* **行が増えないこと自体は verdict ではない。**
* 適用条件: 静的に取得できるリリースが 2 本以上あること。

**この層は一度も通っていなかった**（`docs/decisions.md` D22。修正済み。以後は回帰テスト）:

1. `dparse.py: DPrev.load` が manifest の入れ子を誤り、自分の `scan` 出力を
   `--prev-manifest` に渡すと `KeyError: 'unit_id'` で落ちる。`unit_id` は
   ユニット直下ではなく `units[i]["unit"]["unit_id"]` にある。
2. `report.py` の `n_units_with_D_prev_join` が `0` の決め打ちで、
   join が成立しても manifest に出ない。
3. `scripts/f0a.py` に `r_prev` が**無い**（`grep r_prev` が 0 件）。
   仕様書 §10 の「方向そのものを疑うべき条件」の 3 つ目がこれなので、
   **3 条件のうち 1 つが原理的に測れない状態だった。**
"""

from __future__ import annotations

import json
import textwrap

import pytest

from authgap.report import manifest_json, probe_json
from authgap.runner import RunConfig, run

HEAD = """\
import subprocess
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")
"""

#: 前リリース: FS_READ だけを持つ。
PREV = HEAD + '''

@mcp.tool()
def read_note(path: str) -> str:
    with open(path) as f:
        return f.read()


@mcp.tool()
def stable(path: str) -> str:
    with open(path) as f:
        return f.read()
'''

#: 新リリース。**3 種の差分を 1 つずつ置く。**
NEW = HEAD + '''

@mcp.tool()
def read_note(path: str) -> str:
    """効果 kind が増えた（FS_READ に SPAWN が加わる）→ GAP_DRIFT。"""
    subprocess.run(["cat", path])
    with open(path) as f:
        return f.read()


@mcp.tool()
def stable(path: str) -> str:
    """前リリースと同一。**行が増えないこと自体は verdict ではない** → drift なし。"""
    with open(path) as f:
        return f.read()


@mcp.tool()
def added(path: str) -> str:
    """前リリースに無い新規ユニット → join できない（drift も出ない）。"""
    with open(path) as f:
        return f.read()
'''


def _write(root, source: str):
    (root / "server.py").write_text(textwrap.dedent(source), encoding="utf-8")
    return root


@pytest.fixture(scope="module")
def prev_manifest(tmp_path_factory):
    """前リリースを scan して manifest を作る（`--prev-manifest` に渡す形）。"""
    root = _write(tmp_path_factory.mktemp("prev"), PREV)
    res = run(RunConfig(src_root=str(root), population="mcp_server", full=True))
    path = tmp_path_factory.mktemp("m") / "prev.json"
    path.write_text(json.dumps(manifest_json(res, "prev"), ensure_ascii=False), encoding="utf-8")
    return str(path)


@pytest.fixture(scope="module")
def new_root(tmp_path_factory):
    return str(_write(tmp_path_factory.mktemp("new"), NEW))


@pytest.fixture(scope="module")
def attempt(new_root, prev_manifest):
    """`--prev-manifest` を渡した実行。**例外も戻り値として返す。**

    fixture がそのまま送出すると pytest の setup エラー（ERROR）になり
    `xfail` が効かないので、期待値を修正より先にコミットできない。
    """
    try:
        return run(
            RunConfig(
                src_root=new_root,
                population="mcp_server",
                full=True,
                prev_manifest=prev_manifest,
            )
        ), None
    except Exception as exc:  # noqa: BLE001 — 何が出ても期待値として記録する
        return None, exc


def _result(attempt):
    res, exc = attempt
    assert exc is None, f"--prev-manifest の読み込みで例外: {exc!r}"
    return res


def _unit(res, tool: str):
    found = [u for u in res.tree.units if u.unit.tool_name == tool]
    assert len(found) == 1, f"{tool!r} のユニットが 1 件でない: {[u.unit.tool_name for u in res.tree.units]}"
    return found[0]


def _drift_rows(res, tool: str) -> set:
    out: set = set()
    for r in _unit(res, tool).rows:
        out |= {x for x in r.verdicts if x == "GAP_DRIFT"}
    return out


# --------------------------------------------------------------------------
# 前提テスト（印なし）。**fixture が当該経路に届いていること。**
# --------------------------------------------------------------------------


def test_precondition_prev_manifest_is_readable(prev_manifest):
    """前リリースの manifest が `unit_id` を持つ形で書けている。"""
    data = json.loads(open(prev_manifest, encoding="utf-8").read())
    units = data.get("units") or []
    assert len(units) == 2, f"前リリースのユニットが 2 件でない: {len(units)}"
    ids = {u["unit"]["unit_id"] for u in units}
    assert all(i.startswith("mcp:") for i in ids), ids


def test_precondition_unit_ids_match_across_releases(attempt, prev_manifest):
    """`read_note` と `stable` の unit id が 2 リリースで一致している。

    **join は unit id の完全一致のみ**（Def 6）なので、これが崩れていると
    drift の有無ではなく join の失敗を見ることになる。
    """
    res, exc = attempt
    if exc is not None:
        pytest.skip(f"--prev-manifest が読めないので join 以前の前提（O: D22）: {exc!r}")
    prev_ids = {u["unit"]["unit_id"] for u in json.loads(open(prev_manifest, encoding="utf-8").read())["units"]}
    now_ids = {u.unit.unit_id for u in res.tree.units}
    assert len(prev_ids & now_ids) == 2, f"共通の unit id が 2 件でない: prev={prev_ids} now={now_ids}"


# --------------------------------------------------------------------------
# 1. `--prev-manifest` が自分の scan 出力を読めること
# --------------------------------------------------------------------------


def test_prev_manifest_accepts_own_scan_output(attempt):
    """**自分の出力を自分で読めない層は一度も通っていない。**

    `DPrev.load` が `units[i]["unit_id"]` を引いていたので `KeyError` で落ちた。
    正しい場所は `units[i]["unit"]["unit_id"]`。
    """
    assert _result(attempt).tree.units, "ユニットが 1 件も無い"


# --------------------------------------------------------------------------
# 2. Def 6 の差分規則
# --------------------------------------------------------------------------


def test_new_effect_kind_is_drift(attempt):
    """効果 kind が増えたユニットは `GAP_DRIFT`。"""
    assert _drift_rows(_result(attempt), "read_note") == {"GAP_DRIFT"}


def test_unchanged_unit_is_not_drift(attempt):
    """**行が増えないこと自体は verdict ではない**（Def 6）。"""
    assert _drift_rows(_result(attempt), "stable") == set()


def test_unit_absent_from_previous_release_is_not_drift(attempt):
    """前リリースに無いユニットは join できないので drift を出さない。

    Def 6 は「qualified_name が消えて別名が現れた行は delete+add であり
    **rename と新規追加を区別しない**」と明記しており、D_prev は rename を
    跨いだ主張をしない。
    """
    assert _drift_rows(_result(attempt), "added") == set()


# --------------------------------------------------------------------------
# 3. join 数が manifest に出ること（`r_prev` の分子）
# --------------------------------------------------------------------------


def test_join_count_is_reported(attempt):
    """`n_units_with_D_prev_join` が実際の join 数になる（`0` の決め打ちではない）。

    仕様書 §10 の `r_prev` はこの値を分子に使う。**決め打ちのままだと
    「方向そのものを疑うべき条件」の 3 つ目が原理的に測れない。**
    """
    m = probe_json(_result(attempt), "t")
    assert m["n_units_with_D_prev_join"] == 2, f"join 数={m['n_units_with_D_prev_join']}（期待 2）"


def test_join_count_is_zero_without_prev_manifest(new_root):
    """`--prev-manifest` を渡さなければ join 数は 0。"""
    res = run(RunConfig(src_root=new_root, population="mcp_server", full=True))
    assert probe_json(res, "t")["n_units_with_D_prev_join"] == 0


# --------------------------------------------------------------------------
# 4. `scripts/f0a.py` の `r_prev`
#
# **この節のテストはコードと同一コミットで書いた**（規則 5 の手続きを踏んで
# いない）。1〜3 と違い `r_prev` は既存の壊れた機能ではなく新規の測定なので、
# 「先に凍結すべき期待値」が存在しなかった。期待は仕様書 §10 の定義と
# `docs/preregistration.md` §2.2 の主分母から書いている。
# --------------------------------------------------------------------------


def _f0a():
    """`scripts/f0a.py` をモジュールとして読む（パッケージ外のスクリプトなので）。

    `sys.modules` への登録を先に行う。dataclass の型注釈の解決が
    `sys.modules[cls.__module__]` を引くので、登録しないと `PopStats` の構築で
    `AttributeError` になる。
    """
    import importlib.util
    import pathlib
    import sys

    if "f0a_mod" in sys.modules:
        return sys.modules["f0a_mod"]
    spec = importlib.util.spec_from_file_location(
        "f0a_mod", pathlib.Path(__file__).resolve().parents[1] / "scripts" / "f0a.py"
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules["f0a_mod"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_r_prev_is_none_when_no_previous_release_supplied(new_root):
    """**未測定と 0 は違う。** 前リリースを供給しない run では `None`。

    これが `0.0` を返すと、測っていないことが「join 率 0%」に化けて
    §10 の「方向そのものを疑うべき条件」の 3 つ目が誤って成立する。
    """
    mod = _f0a()
    st = mod.PopStats(population="mcp_server")
    res = run(RunConfig(src_root=new_root, population="mcp_server", full=True))
    mod.accumulate(st, res, frozenset(), False, prev_ids=None)
    assert st.r_prev is None
    assert st.r_prev_crude is None
    assert st.n_trees_with_prev == 0


def test_r_prev_uses_the_preregistered_denominator(new_root, prev_manifest):
    """分母は `docs/preregistration.md` §2.2 の主分母（危険効果を持つユニット）。

    粗い分母（全ユニット）の値も必ず併記する（同 §3）。
    """
    mod = _f0a()
    prev_ids = frozenset(
        u["unit"]["unit_id"] for u in json.loads(open(prev_manifest, encoding="utf-8").read())["units"]
    )
    st = mod.PopStats(population="mcp_server")
    res = run(RunConfig(src_root=new_root, population="mcp_server", full=True))
    mod.accumulate(st, res, frozenset(), False, prev_ids=prev_ids)
    # 新リリースは 3 ユニット（read_note / stable / added）。前リリースにあるのは 2 つ。
    assert st.n_units_with_prev_available == 3
    assert st.n_d_prev_join == 2
    assert st.r_prev_crude == pytest.approx(2 / 3)
    # 3 つとも危険効果（FS_READ）を持つので主分母でも同じ値になる。
    assert st.n_dangerous_with_prev_available == 3
    assert st.r_prev == pytest.approx(2 / 3)
    assert st.n_trees_with_prev == 1


def test_probe_mode_sets_d_prev_joined(tmp_path):
    """probe 経路（full=False）でも `--prev-manifest` の join が `d_prev_joined` に立つ。

    D22 の配線後も runner の probe 経路は prev を読まず、`scripts/r_prev.py` の run1 で
    木ごとの join が全木 0 と表示された（集計は unit id 一致で数えていたので正しかった）。
    黙って無視される形だったので回帰として固定する（D27）。
    """
    import json as _json
    import textwrap as _tw

    from authgap.report import manifest_json
    from authgap.runner import RunConfig, run

    src = _tw.dedent('''
        from mcp.server.fastmcp import FastMCP
        mcp = FastMCP("t")

        @mcp.tool()
        def read(path: str) -> str:
            with open(path) as f:
                return f.read()
    ''')
    prev_dir = tmp_path / "prev"
    prev_dir.mkdir()
    (prev_dir / "server.py").write_text(src, encoding="utf-8")
    cur_dir = tmp_path / "cur"
    cur_dir.mkdir()
    (cur_dir / "server.py").write_text(src, encoding="utf-8")

    prev_res = run(RunConfig(src_root=str(prev_dir), population="mcp_server", full=False))
    man = tmp_path / "prev.json"
    man.write_text(_json.dumps(manifest_json(prev_res, run_id="t", volatile=False)), encoding="utf-8")

    cur = run(RunConfig(src_root=str(cur_dir), population="mcp_server", full=False, prev_manifest=str(man)))
    assert cur.tree.units, "ユニットが無い"
    assert all(u.d_prev_joined for u in cur.tree.units), [u.unit.unit_id for u in cur.tree.units]
    # 前リリースを渡さなければ立たない。
    cur2 = run(RunConfig(src_root=str(cur_dir), population="mcp_server", full=False))
    assert not any(u.d_prev_joined for u in cur2.tree.units)
