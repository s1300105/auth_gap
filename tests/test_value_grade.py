"""Def 5 の値検証等級（strong-path）が「検証子の置き場所」で変わる欠陥の再現。

**期待は仕様 Def 5 の文言から書き、修正より先にコミットした**（コミット 7ed20db。
`tests/test_f0a_defects.py` と同じ型で、8 件を `xfail(strict=True)` にしてあった）。
解析器の修正（D21）で 8 件すべてが XPASS になったので印を外したが、**D21 の
inline 採点（`_grade_inline`）は敵対的レビューで false-clean を 25 形入れたことが
確定し、D25 で戻した**（`tests/test_d21_adversarial.py`）。A 群（inline で
Def 5 を満たす形が strong-path になること）は再び未達で、`xfail(strict=True)` に
戻す。**誤りの向きは false-dirty（安全側）**。B 群・C 群は回帰テストのまま。

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
  脆弱版と同じ等級になっていた（A 群）。→ D21 は `_grade_inline` で囲み関数の
  本体を helper 経路と同じ規則で採点したが、**その袋詰め採点が false-clean を
  25 形入れた**ので D25 で戻した。A 群は未達のまま（O8 に統合）。
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
#: inline 形を strong-path にするには、当該述語が sink を支配し、canonical alias
#: そのものに当たり（(ii)）、他方の被演算子が定数で（(iii)）、sink に届く値が
#: root-equal であることを**その述語について**確かめる必要がある。D21 の袋詰め
#: 採点はそれを飛ばして false-clean を作ったので戻した（D25）。未達 = false-dirty。
INLINE_STRONG = pytest.mark.xfail(strict=True, reason="O8: inline 形の strong-path は未実装（D25 で D21 の袋詰め採点を撤回）")

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


@INLINE_STRONG
@pytest.mark.parametrize("tool", ("a1_inline_commonpath", "a2_inline_relative_to", "a3_inline_startswith_sep"))
def test_inline_form_is_strong_path(units, tool):
    grade, weak_reason = _grade(units, tool)
    assert grade == "strong-path", f"{tool}: grade={grade!r} weak_reason={weak_reason!r}"
    assert weak_reason is None


@INLINE_STRONG
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


def test_canon_unused_is_not_strong(units):
    """正規化した値を**検査に使わず**生の値を照合する形（Def 5 条件 (ii) 違反）。

    `real = realpath(path)` があるので条件 (i) は満たすが、包含述語
    （`path.startswith(...)`）は生の `path` に当たっており canonical alias に
    当たっていない。D21 の inline 採点では (i) までしか見ないので strong-path に
    なっていた（O8 で凍結）。**D25 で inline 採点を戻したので weak に戻る**が、
    それは (ii) を実装したからではなく inline 形を一律 weak にしたからである。
    helper 形の同形は `tests/test_d21_adversarial.py` x01 が O8/O11 として凍結する。
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


# --------------------------------------------------------------------------
# D. 等級潰し腕 C0（`docs/preregistration.md` §5 #2 の判別実験 (b)）
#
# **期待は判別実験の判定規則（prereg §5 #2）から書き、実装より先にコミットした**（d2b501a）。
# 実装で 10 件すべてが XPASS になったので印を外した。以後は回帰テスト。
#
# C0 = 「位置をゲートする値検証子（form=value の候補が主語一致で束縛され、
# sink を支配している）があれば、**等級に関係なく** req_val = OP」。
# 腕 A / B と同じく**同一の解析経路を通り、座標を 1 つ止めるだけ**である。
# 別の実装を書いてはならない（analyze.py の ARMS の規則）。
#
# C − C0（C で GAP、C0 で clear になる位置）が「等級づけが verdict を動かした
# 位置」である。この fixture 集合での事前登録した期待値は {b1, b2} だった:
#   b1 helper が root だけ正規化（weak）… C: MODEL / C0: OP
#   b2 join 後の正規化（weak）…………… C: MODEL / C0: OP
# a1〜a3 / b3 / c2 は C でも strong なので差が出ず、c1 は検証子が無いので
# C0 でも MODEL のまま、というのが d2b501a の期待だった。
#
# **D25 で D21 の inline 採点を撤回したため、a1〜a3 と b3 は C で weak（MODEL）に
# 戻り、C − C0 = {a1, a2, a3, b1, b2, b3} になる。** これは結果を見て期待を
# 動かしたのではなく、解析器の等級規則が変わった（inline 形は一律 weak）ことの
# 機械的な帰結である。`docs/preregistration.md` §5 #3 に逸脱として記録した。
# a1〜a3 が C − C0 に入るのは false-dirty（Def 5 を満たす形を weak と見ている）
# の側なので、「等級づけが verdict を動かした位置」としては b1 / b2 と性質が違う。
# 較正対での C − C0 は `scripts/two_sided.py --arm C0` で別に取る。
# --------------------------------------------------------------------------

@pytest.fixture(scope="module")
def units_c0(tmp_path_factory):
    root = tmp_path_factory.mktemp("value_grade_c0")
    (root / "server.py").write_text(textwrap.dedent(SOURCE), encoding="utf-8")
    res = run(RunConfig(src_root=str(root), population="mcp_server", full=True, arm="C0"))
    return {u.unit.tool_name: u for u in res.tree.units}


#: (tool, C の req_val, C0 の req_val)。prereg §5 #2 (b) の期待値。
C_VS_C0 = (
    ("a1_inline_commonpath", Req.MODEL, Req.OP),  # D25: inline は weak（false-dirty 側）
    ("a2_inline_relative_to", Req.MODEL, Req.OP),
    ("a3_inline_startswith_sep", Req.MODEL, Req.OP),
    ("b1_helper_root_only", Req.MODEL, Req.OP),
    ("b2_join_after_canon", Req.MODEL, Req.OP),
    ("b3_canon_unused", Req.MODEL, Req.OP),  # D25: inline は weak
    ("c1_no_validator", Req.MODEL, Req.MODEL),
    ("c2_helper_strong", Req.OP, Req.OP),
)


@pytest.mark.parametrize("tool,req_c,req_c0", C_VS_C0)
def test_precondition_arm_c_req_val(units, tool, req_c, req_c0):
    """前提: 腕 C（完全版）の req_val が期待どおり（D21 の結果と一致）。"""
    assert units[tool].req_val.get(SLOT) is req_c, f"{tool}: C の req_val={units[tool].req_val.get(SLOT)}"


@pytest.mark.parametrize("tool,req_c,req_c0", C_VS_C0)
def test_arm_c0_collapses_grade(units_c0, tool, req_c, req_c0):
    """腕 C0 では、束縛された値検証子があれば等級に関係なく req_val = OP。"""
    assert units_c0[tool].req_val.get(SLOT) is req_c0, f"{tool}: C0 の req_val={units_c0[tool].req_val.get(SLOT)}"


def test_c_minus_c0_is_exactly_a_and_b(units, units_c0):
    """C − C0 = {a1, a2, a3, b1, b2, b3}（D25 後）。

    d2b501a の期待は {b1, b2} だった。D25 で inline 形が一律 weak に戻ったため
    a1〜a3 / b3 が加わった（上の注記）。**等級づけが「正しく」verdict を動かした
    位置は依然 b1 / b2 の 2 つ**で、a1〜a3 は false-dirty 側の差である。
    これが空なら「等級づけは verdict に寄与していない」であり、
    prereg §5 #2 の判定規則により等級づけを主張から降ろす。
    """
    diff = sorted(
        t for t, _, _ in C_VS_C0
        if units[t].req_val.get(SLOT) is Req.MODEL and units_c0[t].req_val.get(SLOT) is Req.OP
    )
    assert diff == [
        "a1_inline_commonpath",
        "a2_inline_relative_to",
        "a3_inline_startswith_sep",
        "b1_helper_root_only",
        "b2_join_after_canon",
        "b3_canon_unused",
    ], diff


def test_arm_c0_is_a_known_arm():
    """`ARMS` に C0 が入り、未知の腕は依然として例外になる。"""
    from authgap.analyze import ARMS

    assert "C0" in ARMS
    assert set(ARMS) == {"A", "B", "C", "C0"}
