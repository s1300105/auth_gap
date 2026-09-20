"""Def 5 の値検証等級（strong-path）が「検証子の置き場所」で変わる欠陥の再現。

**期待は仕様 Def 5 の文言から書き、修正より先にコミットした**（コミット 7ed20db。
`tests/test_f0a_defects.py` と同じ型で、8 件を `xfail(strict=True)` にしてあった）。
**解析器の修正（D21）で 8 件すべてが XPASS になったので印を外した。**
以後この 20 件は回帰テストである。

仕様 `AUTHGAP_BRIEF_v3.md` Def 5 の strong-path は 3 条件
（`authgap/catalog/validators.py: strong_path_requirements`）:

1. 制御引数の **root** について symlink 解決子を通った canonical alias が存在する
2. 同じ root の canonical alias に包含述語が適用され、その述語が sink をゲートする
3. 述語の他方の被演算子が定数 / config root / `os.getcwd()`

さらに root-equal（`ROOT_EQUAL_STEPS`）が「sink に届く値と検査された alias の差は
identity / canonicalising_transform / OP リテラル segment 追加のみ」を要求する。

**この 3 条件は「検証子をヘルパー関数に切り出したか、ツール本体に inline で
書いたか」を区別していない。** 現在の実装は区別しており、誤りは両方向にある:

* **false-dirty**: inline 形は `gate.py: _grade_from_shape` に落ちるため
  「単独で strong にはしない」規則で weak に固定され、Def 5 を満たす修正が
  脆弱版と同じ等級になっていた（A 群）。→ `gate.py: _grade_inline` で
  囲み関数の本体を helper 経路と同じ規則で採点するようにした。
* **false-clean**: ヘルパー経路 `gate.py: _value_grade` は本体に現れた形状の
  集合だけを見るので、条件 1（root の canonical alias）を検査せずに
  strong-path を返していた（B 群 b1）。**`..` 遍歴で抜けられる検証子が
  clear されていた。** → `analyze.py: _strong_path_backed` が val の
  canonical-alias 表で条件 1 を裏づけ、`_demote_unbacked_strong` が
  `score_gates` に渡す前に候補を落とす。

**条件 2（包含述語が canonical alias そのものに当たるか）は未実装**で、
b3 がその形である（O8）。

出所: `docs/decisions.md` D21。
"""

from __future__ import annotations

import textwrap

import pytest

from authgap.ir import Req
from authgap.runner import RunConfig, run

#: Def 5 の条件 (ii)（包含述語が canonical alias **そのもの**に適用されたか）は
#: 現在の実装では確かめられない。手続き間に跨る形（較正対 A4 の `git_add` が
#: その実例）では canonical alias が callee の中にあり最終 env に残らないので、
#: 条件 (i) を `alias_facts` で見るところまでしか行けていない。
#: **黙って安全側に倒さず未解決として記録する**（`docs/open_questions.md` O8）。
COND_II = pytest.mark.xfail(strict=True, reason="O8: Def 5 条件 (ii) は未実装")

SOURCE = '''\
import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")
ROOT = "/srv/data"


# --- A 群: Def 5 の 3 条件を inline で満たす（strong-path であるべき） ---
@mcp.tool()
def a1_inline_commonpath(path: str) -> str:
    real = os.path.realpath(path)
    base = os.path.realpath(ROOT)
    if os.path.commonpath([real, base]) != base:
        raise ValueError(path)
    with open(real) as f:
        return f.read()


@mcp.tool()
def a2_inline_relative_to(path: str) -> str:
    root = Path(ROOT).resolve()
    target = (root / path).resolve()
    if not target.is_relative_to(root):
        raise ValueError(path)
    with open(target) as f:
        return f.read()


@mcp.tool()
def a3_inline_startswith_sep(path: str) -> str:
    real = os.path.realpath(path)
    base = os.path.realpath(ROOT)
    if not base.endswith(os.sep):
        base += os.sep
    if not real.startswith(base):
        raise ValueError(path)
    with open(real) as f:
        return f.read()


# --- B 群: Def 5 の条件 1 / root-equal を満たさない（strong にしてはいけない） ---
def _validate_root_only(path, root):
    """ROOT だけ realpath。**検査対象は生の path のまま**なので条件 1 を満たさない。"""
    base = os.path.realpath(root)
    if os.path.commonpath([path, base]) != base:
        raise ValueError(path)
    return path


@mcp.tool()
def b1_helper_root_only(path: str) -> str:
    p = _validate_root_only(path, ROOT)
    with open(p) as f:
        return f.read()


@mcp.tool()
def b2_join_after_canon(path: str) -> str:
    base = os.path.realpath(ROOT)
    target = os.path.join(base, path)
    if not target.startswith(base + os.sep):
        raise ValueError(path)
    with open(target) as f:
        return f.read()


@mcp.tool()
def b3_canon_unused(path: str) -> str:
    real = os.path.realpath(path)
    base = os.path.realpath(ROOT)
    _audit = real
    if not path.startswith(base + os.sep):
        raise ValueError(path)
    with open(path) as f:
        return f.read()


# --- C 群: 対照。修正の前後で動いてはいけない ---
@mcp.tool()
def c1_no_validator(path: str) -> str:
    with open(path) as f:
        return f.read()


def _validate_strong(path, root):
    """付録 G `fixtures/gates/_prelude.py: validate_path` と同じ形。"""
    real = os.path.realpath(path)
    base = os.path.realpath(root)
    if os.path.commonpath([real, base]) != base:
        raise ValueError(path)
    return real


@mcp.tool()
def c2_helper_strong(path: str) -> str:
    real = _validate_strong(path, ROOT)
    with open(real) as f:
        return f.read()
'''

SLOT = (0, "path")


@pytest.fixture(scope="module")
def units(tmp_path_factory):
    root = tmp_path_factory.mktemp("value_grade")
    (root / "server.py").write_text(textwrap.dedent(SOURCE), encoding="utf-8")
    res = run(RunConfig(src_root=str(root), population="mcp_server", full=True))
    return {u.unit.tool_name: u for u in res.tree.units}


def _grade(units, tool: str) -> tuple:
    u = units[tool]
    g = units[tool].grades.get(SLOT)
    assert g is not None, f"{tool}: slot {SLOT} の等級が無い（grades={list(u.grades)}）"
    return g


def _verdicts(units, tool: str) -> set:
    rows = [r for r in units[tool].rows if r.slot == "path"]
    assert rows, f"{tool}: slot 'path' の行が無い"
    return set(rows[0].verdicts)


# --------------------------------------------------------------------------
# 前提テスト（印なし）。**fixture が解析器の当該経路に届いていること。**
# これが無いと、書き損じでユニットが消えただけのテストも xfail として「通る」。
# --------------------------------------------------------------------------

ALL_TOOLS = (
    "a1_inline_commonpath",
    "a2_inline_relative_to",
    "a3_inline_startswith_sep",
    "b1_helper_root_only",
    "b2_join_after_canon",
    "b3_canon_unused",
    "c1_no_validator",
    "c2_helper_strong",
)


@pytest.mark.parametrize("tool", ALL_TOOLS)
def test_precondition_unit_and_slot_exist(units, tool):
    """8 ツールすべてが FS_READ の `path` 位置を持つユニットとして見えている。"""
    assert tool in units, f"{tool} のユニットが無い: {sorted(units)}"
    u = units[tool]
    slots = [s for e in u.effects if e.kind == "FS_READ" for s in e.control_slots()]
    assert "path" in slots, f"{tool}: FS_READ の path 位置が無い（effects={[e.kind for e in u.effects]}）"
    assert SLOT in u.req_val, f"{tool}: req_val に {SLOT} が無い"


@pytest.mark.parametrize("tool", ("a1_inline_commonpath", "a2_inline_relative_to", "a3_inline_startswith_sep"))
def test_precondition_a_group_has_canonical_alias(units, tool):
    """A 群は val が条件 1 の証拠（root の symlink alias）を実際に記録している。

    これが無いと、A 群を strong-path にする修正は「val の裏づけ無しに strong を
    出す」ことになり、B 群の false-clean と同じ誤りになる。
    """
    facts = {(a.root, a.transform) for a in units[tool].val.alias_facts}
    symlink = {(r, t) for r, t in facts if t in ("realpath", "Path.resolve")}
    assert symlink, f"{tool}: symlink 系の alias 事実が無い（alias_facts={sorted(facts)}）"
    assert any(r == "path" for r, _ in symlink), f"{tool}: root 'path' の alias が無い: {sorted(symlink)}"


def test_precondition_b1_has_no_canonical_alias(units):
    """b1 は条件 1 を満たさない（root 'path' の canonical alias が存在しない）。

    ヘルパーは `realpath(root)` しか通しておらず、検査対象も sink に届く値も
    生の `path` である。**この事実が b1 を strong にしてはいけない根拠である。**
    """
    facts = {(a.root, a.transform) for a in units["b1_helper_root_only"].val.alias_facts}
    symlink = {(r, t) for r, t in facts if t in ("realpath", "Path.resolve") and r == "path"}
    assert not symlink, f"b1: root 'path' の symlink alias があってはならない: {sorted(symlink)}"


# --------------------------------------------------------------------------
# A 群: Def 5 を inline で満たす形は strong-path であるべき（現在は weak。false-dirty）
# --------------------------------------------------------------------------


@pytest.mark.parametrize("tool", ("a1_inline_commonpath", "a2_inline_relative_to", "a3_inline_startswith_sep"))
def test_inline_form_is_strong_path(units, tool):
    grade, weak_reason = _grade(units, tool)
    assert grade == "strong-path", f"{tool}: grade={grade!r} weak_reason={weak_reason!r}"
    assert weak_reason is None


@pytest.mark.parametrize("tool", ("a1_inline_commonpath", "a2_inline_relative_to", "a3_inline_startswith_sep"))
def test_inline_form_clears_gap(units, tool):
    assert units[tool].req_val.get(SLOT) is Req.OP, f"{tool}: req_val={units[tool].req_val.get(SLOT)}"
    assert _verdicts(units, tool) == set(), f"{tool}: verdicts={_verdicts(units, tool)}"


# --------------------------------------------------------------------------
# B 群: 条件 1 / root-equal を満たさない形は strong にしてはいけない
# --------------------------------------------------------------------------


def test_helper_without_canonical_alias_is_not_strong(units):
    """**false-clean。** `..` 遍歴で抜けられる検証子が strong-path で clear される。"""
    grade, weak_reason = _grade(units, "b1_helper_root_only")
    assert grade == "weak", f"b1: grade={grade!r}"
    assert weak_reason == "no_symlink_resolution", f"b1: weak_reason={weak_reason!r}"


def test_helper_without_canonical_alias_keeps_gap(units):
    assert units["b1_helper_root_only"].req_val.get(SLOT) is Req.MODEL
    assert _verdicts(units, "b1_helper_root_only") == {"GAP_INJECT"}


def test_join_after_canon_is_not_strong(units):
    """`join(realpath(ROOT), path)` は root 'path' の alias を作らない（対照。現在も正しい）。"""
    grade, _ = _grade(units, "b2_join_after_canon")
    assert grade == "weak", f"b2: grade={grade!r}"
    assert _verdicts(units, "b2_join_after_canon") == {"GAP_INJECT"}


@COND_II
def test_canon_unused_is_not_strong(units):
    """正規化した値を**検査に使わず**生の値を照合する形（Def 5 条件 (ii) 違反）。

    `real = realpath(path)` があるので条件 (i) は満たすが、包含述語
    （`path.startswith(...)`）は生の `path` に当たっており canonical alias に
    当たっていない。**現在の実装は (i) までしか見ないので strong-path になる。**
    条件 (ii) を満たさない形はここで凍結し、O8 として記録した。
    """
    grade, _ = _grade(units, "b3_canon_unused")
    assert grade == "weak", f"b3: grade={grade!r}"
    assert _verdicts(units, "b3_canon_unused") == {"GAP_INJECT"}


# --------------------------------------------------------------------------
# C 群: 対照。**修正の前後で動いてはいけない。**
# --------------------------------------------------------------------------


def test_no_validator_stays_gap(units):
    grade, weak_reason = units["c1_no_validator"].grades.get(SLOT, (None, None))
    assert grade is None and weak_reason is None, f"c1: grade={grade!r} weak_reason={weak_reason!r}"
    assert _verdicts(units, "c1_no_validator") == {"GAP_INJECT"}


def test_helper_strong_stays_strong(units):
    """付録 G の基準形。**修正でこれが落ちたら較正対 A1 / A10 が壊れる。**"""
    grade, weak_reason = _grade(units, "c2_helper_strong")
    assert grade == "strong-path", f"c2: grade={grade!r} weak_reason={weak_reason!r}"
    assert units["c2_helper_strong"].req_val.get(SLOT) is Req.OP
    assert _verdicts(units, "c2_helper_strong") == set()
