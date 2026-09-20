"""D21（inline 形を strong-path に到達可能にした修正 `d745cb2`）の敵対的レビューで
確認された false-clean を凍結する。

**期待は敵対的レビューの報告（2026-09-20、94 エージェント、29 反例すべてが
再現 / 攻撃成立 / 由来の 3 レンズを通過）から書き、修正より先にコミットする**
（`CLAUDE.md` 規則 5。`docs/decisions.md` D21「結果」・D25）。

レビューが確定した機構は 4 つ:

* **M1 袋詰め採点**: `gate.py: _grade_inline` が候補述語 1 つではなく囲み関数の
  本体全体を `ast.walk` で集め、「正規化子の集合 × 包含述語の集合」で採点する。
  CFG も支配も主語も適用順序も見ないので、ログ用の `realpath` 1 行や死に分岐の
  検査が、別の述語（`os.path.exists` など）に strong-path を貸す。
* **M2 裏づけの存在量化**: `analyze.py: _strong_path_backed` が制御値の root の
  **どれか 1 つ**に symlink 系 alias があれば裏づけ済みとする。join で root が
  和になると、検証済み引数の裏づけが未検証引数に移る。
* **M3 領域不一致**: パス包含の等級（strong-path）が `shell_string` / `sql` /
  `code_text` / `url.host` の位置にも `req_val = OP` を与える。
* **M4 死んだ語彙**: `ROOT_EQUAL_STEPS` / `ALLOWED_OPERANDS` / `post_check_append`
  は定義のみで参照 0 件。Def 5 条件 (iii) と root-equal は未実装。

**誤りの向きはすべて false-clean**（実際に木の外を読める / 任意コマンドが動くのに
`verdicts` が空）。25 件は D21 が新たに入れた退行（修正前は `GAP_INJECT`）、
4 件は D21 以前からある helper 経路の欠陥。

ここでの期待は「**strong-path にしない**、`req_val` が `MODEL` のまま、
`GAP_INJECT` が残る」。対照（C 群）は「修正で動いてはいけない」。

**まだ直せない形**（helper 本体の袋詰め採点・条件 (ii)・条件 (iii)）は
`xfail(strict=True)` で凍結し、`docs/open_questions.md` O8 / O10 / O11 に記録する。
黙って安全側に倒さない。
"""

from __future__ import annotations

import textwrap

import pytest

from authgap.ir import Req
from authgap.runner import RunConfig, run

#: helper 本体の袋詰め採点（M1 の helper 版）+ 値の同一性を見ない裏づけ（M2）。
#: 条件 (ii)「包含述語が canonical alias **そのもの**に当たる」を val の値の同一性で
#: 確かめない限り、無関係な 1 行の `realpath(path)` で反転する。O8（拡張）/ O11。
KNOWN_HELPER_DECOY = pytest.mark.xfail(
    strict=True, reason="O8/O11: helper 経路の袋詰め採点 + 値の同一性を見ない裏づけ（未実装）"
)
#: Def 5 条件 (iii)（述語の他方の被演算子が定数 / config root / os.getcwd()）は未実装。
#: `ALLOWED_OPERANDS` / `DOWNGRADES.tainted` の参照が 0 件。O10。
KNOWN_COND_III = pytest.mark.xfail(strict=True, reason="O10: Def 5 条件 (iii) は未実装")
#: D21 の退行（現 HEAD で false-clean）。**修正コミットでこの印を外す。**
DEFECT = pytest.mark.xfail(strict=True, reason="D21 退行（false-clean）。D25 で直す")

SOURCE = '''\
import logging
import os
import subprocess
from pathlib import Path

import requests
import sqlalchemy
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")
log = logging.getLogger(__name__)
ROOT = "/srv/data"
BASE_DIR = ROOT
ALLOWED_ROOTS = ["/srv/data", "/srv/pub"]
AUDIT = False
engine = sqlalchemy.create_engine("sqlite://")
conn = engine.connect()


# ==========================================================================
# R 群: D21 が新たに入れた退行（修正前は GAP_INJECT）。すべて inline 形。
# ==========================================================================


@mcp.tool()
def r01_tail_log(path: str) -> str:
    """R1: ログ用 realpath + 生 path の prefix。sink は shell_string（コマンド注入）。"""
    audit = os.path.realpath(path)
    log.info("tail_log audit=%s", audit)
    if not path.startswith(ROOT + os.sep):
        raise ValueError("outside data root")
    return subprocess.check_output("tail -n 50 " + path, shell=True).decode()


@mcp.tool()
def r02_enum_lends_exists(path: str, fmt: str = "text") -> str:
    """R2: 無関係な引数の enum + 応答用 realpath が os.path.exists を strong にする。"""
    if fmt not in ("text", "json"):
        raise ValueError("bad format")
    real = os.path.realpath(path)
    log.info("real=%s", real)
    if not os.path.exists(path):
        raise ValueError("no such file")
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


@mcp.tool()
def r03_join_one_root_checked(base: str, name: str) -> str:
    """R3: join した値に realpath。検査は base だけ。sink は生の target。"""
    target = os.path.join(base, name)
    canonical = os.path.realpath(target)
    if not os.path.exists(canonical):
        raise ValueError("no such file")
    if not base.startswith(ROOT + os.sep):
        raise ValueError("outside data root")
    with open(target, "r", encoding="utf-8") as fh:
        return fh.read()


@mcp.tool()
def r04_realpath_after_sink(path: str) -> str:
    """R4: 裏づけの realpath が sink より後ろ。"""
    if not path.startswith(ROOT + os.sep):
        raise ValueError("outside data root")
    with open(path, "r", encoding="utf-8") as fh:
        data = fh.read()
    log.info("read_note audit=%s", os.path.realpath(path))
    return data


@mcp.tool()
def r05_else_branch_lends_grade(path: str, preview: bool = False) -> str:
    """R5: 支配しない else 側の包含検査が、sink を支配する exists に等級を貸す。"""
    if preview:
        if os.path.exists(path):
            with open(path) as fh:
                return fh.read()
        return "missing"
    real = os.path.realpath(path)
    if not real.startswith(BASE_DIR + os.sep):
        raise ValueError("outside")
    return "ok"


@mcp.tool()
def r06_early_return_bypass(path: str, use_cache: bool = True) -> str:
    """R6: 高速経路が検査を迂回。効果 0（生の path）が clear されてはいけない。"""
    if use_cache and os.path.isfile(path):
        with open(path) as fh:
            return fh.read()
    real = os.path.realpath(path)
    if not real.startswith(BASE_DIR + os.sep):
        raise ValueError("outside")
    with open(real) as fh:
        return fh.read()


@mcp.tool()
def r07_except_swallows_reject(path: str) -> str:
    """R7: 拒否を except で握りつぶす。"""
    try:
        real = os.path.realpath(path)
        if not real.startswith(BASE_DIR + os.sep):
            raise ValueError("outside")
    except ValueError:
        pass
    if os.path.isfile(path):
        with open(path) as fh:
            return fh.read()
    return "missing"


@mcp.tool()
def r08_loop_continue_no_reject(path: str) -> str:
    """R8: 包含検査を for の中に置き、外れても raise しない。"""
    real = os.path.realpath(path)
    for root in ALLOWED_ROOTS:
        if not real.startswith(root + os.sep):
            continue
        break
    if os.path.isfile(path):
        with open(path) as fh:
            return fh.read()
    return "missing"


@mcp.tool()
def r09_unused_predicate_result(path: str) -> str:
    """R9: 包含検査の結果をどの分岐にも使わない。"""
    real = os.path.realpath(path)
    inside = real.startswith(BASE_DIR + os.sep)
    if os.path.isfile(path):
        with open(path) as fh:
            return fh.read()
    return "missing:%s" % inside


@mcp.tool()
def r10_join_two_args(subdir: str, name: str) -> str:
    """R10: 検証済み subdir の裏づけが、未検証の name に移る（root の和）。"""
    real = os.path.realpath(os.path.join(ROOT, subdir))
    base = os.path.realpath(ROOT)
    if os.path.commonpath([real, base]) != base:
        raise ValueError(subdir)
    target = f"{real}/{name}"
    with open(target) as f:
        return f.read()


@mcp.tool()
def r11_model_root_inline(workspace: str, rel: str) -> str:
    """R11: 包含 root 自体がモデル引数（条件 (iii) 違反）。inline 形。"""
    base = os.path.realpath(workspace)
    target = os.path.realpath(os.path.join(base, rel))
    if os.path.commonpath([target, base]) != base:
        raise ValueError(rel)
    with open(target) as f:
        return f.read()


@mcp.tool()
def r12_exec_after_check(path: str, args: str) -> str:
    """R12: 検証済み path と未検証 args を同じシェル文字列に合流。"""
    real = os.path.realpath(path)
    base = os.path.realpath(ROOT)
    if os.path.commonpath([real, base]) != base:
        raise ValueError(path)
    return subprocess.run(f"cat {real}/{args}", shell=True, capture_output=True).stdout.decode()


@mcp.tool()
def r13_dead_branch_realpath(path: str) -> str:
    """R13: 実行時に通らない分岐の realpath が条件 (i) の裏づけになる。"""
    if AUDIT:
        path = os.path.realpath(path)
    base = os.path.realpath(ROOT)
    if os.path.commonpath([path, base]) != base:
        raise ValueError(path)
    with open(path) as f:
        return f.read()


@mcp.tool()
def r14_realpath_after_sink_commonpath(path: str) -> str:
    """R14: 生の path を照合、sink の後ろで realpath。"""
    base = os.path.realpath(ROOT)
    if os.path.commonpath([path, base]) != base:
        raise ValueError(path)
    with open(path) as f:
        data = f.read()
    _log = os.path.realpath(path)
    return data


@mcp.tool()
def r15_sibling_value_realpath(path: str) -> str:
    """R15: realpath が path ではなく dirname(path) に当たる。"""
    parent = os.path.realpath(os.path.dirname(path))
    base = os.path.realpath(ROOT)
    if os.path.commonpath([path, base]) != base:
        raise ValueError(path)
    del parent
    with open(path) as f:
        return f.read()


@mcp.tool()
def r16a_discard_canon(path: str) -> str:
    """R16 v1: 正規化した値を捨てて生の値を commonpath に掛ける。"""
    _ = os.path.realpath(path)
    base = os.path.realpath(ROOT)
    if os.path.commonpath([path, base]) != base:
        raise ValueError(path)
    with open(path) as f:
        return f.read()


@mcp.tool()
def r16b_rebound_canon(path: str) -> str:
    """R16 v3: canonical alias の名前を持ちながら中身は生の値。"""
    real = os.path.realpath(path)
    real = path
    base = os.path.realpath(ROOT)
    if os.path.commonpath([real, base]) != base:
        raise ValueError(path)
    with open(real) as f:
        return f.read()


@mcp.tool()
def r17_join_after_check(project: str, name: str) -> str:
    """R17: 検査後に os.path.join で MODEL segment を足す（仕様 :264 の post_check_append）。"""
    real = os.path.realpath(os.path.join(ROOT, project))
    base = os.path.realpath(ROOT)
    if os.path.commonpath([real, base]) != base:
        raise ValueError(project)
    target = os.path.join(real, name)
    with open(target) as f:
        return f.read()


@mcp.tool()
def r18_canon_after_check(name: str) -> str:
    """R18: symlink 解決が包含検査の後（check-then-canonicalise）。"""
    candidate = os.path.join(ROOT, name)
    base = ROOT + os.sep
    if not candidate.startswith(base):
        raise ValueError(name)
    real = os.path.realpath(candidate)
    with open(real) as f:
        return f.read()


@mcp.tool()
def r19_shell_after_check(directory: str, extra: str) -> str:
    """R19: 検査後の MODEL 連結でシェル文字列を組む。"""
    real = os.path.realpath(os.path.join(ROOT, directory))
    base = os.path.realpath(ROOT)
    if os.path.commonpath([real, base]) != base:
        raise ValueError(directory)
    cmd = f"tar -czf /tmp/out.tgz {real} {extra}"
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout


@mcp.tool()
def r20_pathdiv_after_check(project: str, name: str) -> str:
    """R20: Path.resolve + is_relative_to の後に / 演算子で MODEL 値を足す。"""
    base = Path(ROOT).resolve()
    d = (base / project).resolve()
    if not d.is_relative_to(base):
        raise ValueError(project)
    target = d / name
    return target.read_text()


@mcp.tool()
def r21_b2_with_audit_log(path: str) -> str:
    """R21: 凍結済みの b2（join 後の正規化）に無害なログ行を 1 つ足しただけ。"""
    log.info("request for %s", os.path.realpath(path))
    base = os.path.realpath(ROOT)
    target = os.path.join(base, path)
    if not target.startswith(base + os.sep):
        raise ValueError(path)
    with open(target) as f:
        return f.read()


@mcp.tool()
def r22_head_file_shell(name: str) -> str:
    """R22: パス包含の等級が SPAWN(shell_string) に漏れる。sink に渡るのは生の name。"""
    resolved = os.path.realpath(os.path.join(ROOT, name))
    base = os.path.realpath(ROOT)
    if os.path.commonpath([resolved, base]) != base:
        raise ValueError(name)
    return subprocess.run("head -n 20 " + name, shell=True, capture_output=True, text=True).stdout


@mcp.tool()
def r23_query_table_sql(name: str) -> str:
    """R23: パス包含の等級が DB(sql) に漏れる。"""
    resolved = os.path.realpath(os.path.join(ROOT, name + ".csv"))
    base = os.path.realpath(ROOT)
    if os.path.commonpath([resolved, base]) != base:
        raise ValueError(name)
    rows = conn.execute(sqlalchemy.text("SELECT * FROM " + name))
    return str(list(rows))


@mcp.tool()
def r24_compute_eval(expr: str) -> str:
    """R24: パス包含の等級が EXEC(code_text) に漏れる。"""
    resolved = os.path.realpath(os.path.join(ROOT, expr))
    base = os.path.realpath(ROOT)
    if os.path.commonpath([resolved, base]) != base:
        raise ValueError(expr)
    return str(eval(expr))


@mcp.tool()
def r25_fetch_host(host: str) -> str:
    """R25: パス包含の等級が NET(url.host) に漏れる。"""
    resolved = os.path.realpath(os.path.join(ROOT, host))
    base = os.path.realpath(ROOT)
    if os.path.commonpath([resolved, base]) != base:
        raise ValueError(host)
    return requests.get("http://" + host + "/api").text


# ==========================================================================
# X 群: D21 以前からある helper 経路の欠陥（レビュー §3）
# ==========================================================================


def _validate_root_only(path, root):
    """ROOT だけ realpath。検査対象は生の path のまま（条件 (i) 違反）。"""
    base = os.path.realpath(root)
    if os.path.commonpath([path, base]) != base:
        raise ValueError(path)
    return path


def _validate_strong(path, root):
    """付録 G の基準形（Def 5 を満たす）。"""
    real = os.path.realpath(path)
    base = os.path.realpath(root)
    if os.path.commonpath([real, base]) != base:
        raise ValueError(path)
    return real


def _contain(target, base):
    real = os.path.realpath(target)
    if os.path.commonpath([real, base]) != base:
        raise ValueError(target)
    return real


@mcp.tool()
def x01_helper_root_only_with_decoy(path: str) -> str:
    """§3-1: b1（helper が root だけ realpath）に、ログ用 realpath(path) を 1 行足す。"""
    log.info("read %s", os.path.realpath(path))
    p = _validate_root_only(path, ROOT)
    with open(p) as f:
        return f.read()


@mcp.tool()
def x02_helper_strong_then_shell(path: str, extra: str) -> str:
    """§3-2: helper で正しく検証した real に、未検証の extra を連結して shell へ。"""
    real = _validate_strong(path, ROOT)
    return subprocess.run(f"cat {real} {extra}", shell=True, capture_output=True, text=True).stdout


@mcp.tool()
def x03_helper_model_root(workspace: str, rel: str) -> str:
    """R11 helper 形: 包含 root がモデル引数（条件 (iii) 違反）。"""
    base = os.path.realpath(workspace)
    target = _contain(os.path.join(base, rel), base)
    with open(target) as f:
        return f.read()


@mcp.tool()
def x04_container_join(a: str, b: str) -> str:
    """§3-3: 容器要素の合流。a への検証で open(b) が clear されてはいけない。"""
    targets = [_validate_strong(a, ROOT), b]
    out = []
    for t in targets:
        with open(t) as f:
            out.append(f.read())
    return "".join(out)


@mcp.tool()
def x05_conditional_reassign(path: str, raw_path: str, unsafe: bool = False) -> str:
    """§3-4: 検証後に条件つきで上書き。合流後の root は {path, raw_path}。"""
    target = _validate_strong(path, ROOT)
    if unsafe:
        target = raw_path
    with open(target) as f:
        return f.read()


@mcp.tool()
def x06_helper_strong_sql(name: str) -> str:
    """R23 helper 形: helper でパス検証した name を SQL に連結。"""
    _validate_strong(os.path.join(ROOT, name + ".csv"), ROOT)
    rows = conn.execute(sqlalchemy.text("SELECT * FROM " + name))
    return str(list(rows))


# ==========================================================================
# C 群: 対照。修正で動いてはいけない（strong-path のまま clear）。
# ==========================================================================


@mcp.tool()
def c01_helper_strong_read(path: str) -> str:
    real = _validate_strong(path, ROOT)
    with open(real) as f:
        return f.read()


@mcp.tool()
def c02_helper_strong_argv(path: str) -> str:
    """argv[*] はパス領域（較正対 A4 の git_add と同じ形）。"""
    real = _validate_strong(path, ROOT)
    return subprocess.run(["cat", real], capture_output=True, text=True).stdout


@mcp.tool()
def c03_helper_strong_cwd(path: str) -> str:
    """cwd はパス領域（較正対 A1 と同じ形）。"""
    real = _validate_strong(path, ROOT)
    return subprocess.run(["ls"], cwd=real, capture_output=True, text=True).stdout


@mcp.tool()
def c04_no_validator(path: str) -> str:
    with open(path) as f:
        return f.read()
'''


@pytest.fixture(scope="module")
def units(tmp_path_factory):
    root = tmp_path_factory.mktemp("d21_adv")
    (root / "server.py").write_text(textwrap.dedent(SOURCE), encoding="utf-8")
    res = run(RunConfig(src_root=str(root), population="mcp_server", full=True))
    return {u.unit.tool_name: u for u in res.tree.units}


#: 反例: tool -> (効果 index, slot, 参照)。
#: 効果 index は**その位置の値が生のまま sink に届く効果**（R6 は効果 0）。
CASES: dict[str, tuple[int, str, str]] = {
    "r01_tail_log": (0, "shell_string", "R1"),
    "r02_enum_lends_exists": (0, "path", "R2"),
    "r03_join_one_root_checked": (0, "path", "R3"),
    "r04_realpath_after_sink": (0, "path", "R4"),
    "r05_else_branch_lends_grade": (0, "path", "R5"),
    "r06_early_return_bypass": (0, "path", "R6"),
    "r07_except_swallows_reject": (0, "path", "R7"),
    "r08_loop_continue_no_reject": (0, "path", "R8"),
    "r09_unused_predicate_result": (0, "path", "R9"),
    "r10_join_two_args": (0, "path", "R10"),
    "r11_model_root_inline": (0, "path", "R11"),
    "r12_exec_after_check": (0, "shell_string", "R12"),
    "r13_dead_branch_realpath": (0, "path", "R13"),
    "r14_realpath_after_sink_commonpath": (0, "path", "R14"),
    "r15_sibling_value_realpath": (0, "path", "R15"),
    "r16a_discard_canon": (0, "path", "R16"),
    "r16b_rebound_canon": (0, "path", "R16"),
    "r17_join_after_check": (0, "path", "R17"),
    "r18_canon_after_check": (0, "path", "R18"),
    "r19_shell_after_check": (0, "shell_string", "R19"),
    "r20_pathdiv_after_check": (0, "path", "R20"),
    "r21_b2_with_audit_log": (0, "path", "R21"),
    "r22_head_file_shell": (0, "shell_string", "R22"),
    "r23_query_table_sql": (0, "sql", "R23"),
    "r24_compute_eval": (0, "code_text", "R24"),
    "r25_fetch_host": (0, "url.host", "R25"),
    "x01_helper_root_only_with_decoy": (0, "path", "§3-1"),
    "x02_helper_strong_then_shell": (0, "shell_string", "§3-2"),
    "x03_helper_model_root": (0, "path", "R11 helper"),
    "x04_container_join": (0, "path", "§3-3"),
    "x05_conditional_reassign": (0, "path", "§3-4"),
    "x06_helper_strong_sql": (0, "sql", "R23 helper"),
}

#: 修正後も残ると分かっている形（未解決として記録済み）。
KNOWN: dict[str, object] = {
    "x01_helper_root_only_with_decoy": KNOWN_HELPER_DECOY,
    "x03_helper_model_root": KNOWN_COND_III,
}

CONTROLS_STRONG = ("c01_helper_strong_read", "c02_helper_strong_argv", "c03_helper_strong_cwd")
CONTROL_SLOT = {
    "c01_helper_strong_read": (0, "path"),
    "c02_helper_strong_argv": (0, "argv[*]"),
    "c03_helper_strong_cwd": (0, "cwd"),
}


def _params(names):
    out = []
    for n in names:
        marks = [KNOWN[n]] if n in KNOWN else [DEFECT]
        out.append(pytest.param(n, marks=marks, id=n))
    return out


def _row(u, idx: int, slot: str):
    rows = [r for r in u.rows if r.slot == slot and u.effects.index(r.effect) == idx]
    assert rows, f"効果 {idx} の slot {slot!r} の行が無い: {[(u.effects.index(r.effect), r.slot) for r in u.rows]}"
    return rows[0]


# --------------------------------------------------------------------------
# 前提（印なし）: fixture が解析器の当該経路に届いている
# --------------------------------------------------------------------------


@pytest.mark.parametrize("tool", sorted(CASES) + list(CONTROLS_STRONG) + ["c04_no_validator"])
def test_precondition_unit_and_slot_exist(units, tool):
    assert tool in units, f"{tool} のユニットが無い: {sorted(units)}"
    u = units[tool]
    idx, slot = (CASES.get(tool) or (CONTROL_SLOT.get(tool) or (0, "path")))[:2]
    assert idx < len(u.effects), f"{tool}: 効果 {idx} が無い（effects={[e.kind for e in u.effects]}）"
    assert (idx, slot) in u.req_val, f"{tool}: req_val に {(idx, slot)} が無い: {list(u.req_val)}"


def test_precondition_no_validator_is_gap(units):
    u = units["c04_no_validator"]
    assert u.grades.get((0, "path")) == (None, None)
    assert _row(u, 0, "path").verdicts == {"GAP_INJECT"}


# --------------------------------------------------------------------------
# 1. 反例は strong-path にならず、req_val は MODEL のまま、GAP_INJECT が残る
# --------------------------------------------------------------------------


@pytest.mark.parametrize("tool", _params(sorted(CASES)))
def test_counterexample_is_not_strong_path(units, tool):
    idx, slot, ref = CASES[tool]
    grade, weak_reason = units[tool].grades.get((idx, slot), (None, None))
    assert grade != "strong-path", f"{tool} ({ref}): grade={grade!r} weak_reason={weak_reason!r}"


@pytest.mark.parametrize("tool", _params(sorted(CASES)))
def test_counterexample_keeps_req_val_model(units, tool):
    idx, slot, ref = CASES[tool]
    assert units[tool].req_val.get((idx, slot)) is Req.MODEL, (
        f"{tool} ({ref}): req_val={units[tool].req_val.get((idx, slot))}"
    )


@pytest.mark.parametrize("tool", _params(sorted(CASES)))
def test_counterexample_keeps_gap_inject(units, tool):
    idx, slot, ref = CASES[tool]
    v = _row(units[tool], idx, slot).verdicts
    assert "GAP_INJECT" in v, f"{tool} ({ref}): verdicts={sorted(v)}"


# --------------------------------------------------------------------------
# 2. 対照: helper の基準形は strong-path のまま clear（修正で動いてはいけない）
# --------------------------------------------------------------------------


@pytest.mark.parametrize("tool", CONTROLS_STRONG)
def test_control_helper_strong_stays_strong(units, tool):
    idx, slot = CONTROL_SLOT[tool]
    grade, weak_reason = units[tool].grades.get((idx, slot), (None, None))
    assert grade == "strong-path", f"{tool}: grade={grade!r} weak_reason={weak_reason!r}"
    assert units[tool].req_val.get((idx, slot)) is Req.OP
    assert "GAP_INJECT" not in _row(units[tool], idx, slot).verdicts
