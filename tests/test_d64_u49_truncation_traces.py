"""D64 / U49: 打ち切り・落としたファイルの痕跡をユニット水準に残す（R5-r2-2, R5-r3-2, R5-r1-6）。

**期待値はこのテストで、`authgap/` を直す前に書いた（D64 / U49）。**
規則は `docs/decisions.md` D64 の U49 行（「印・記録を足すだけで rows / verdict / effects は変えない。
VAL_OPAQUE_REASONS は動かさない」）と `evidence/review/triage.json` の U49 の fix_outline（守ること・反例）。
期待値は v2 / v3 の件数ではなく、規則（CLAUDE.md 規則 4、D52、D17 改訂 4、仕様書 640 行目）から決めた。

3 つの所見:

* (A) R5-r2-2（代表、誤 clear）: parse 失敗 / AST_NODE_CAP で落とした木内モジュールの関数を呼ぶツールに、
  依存先が読めていないことの印（`depends_on_dropped:<relpath>` の notes か、`unresolved_in_tree_calls` の
  理由つきの項）を残す。**行・効果・判定は変えない**（効果の無い行を作って「不」に数えるのは別の決定）。
* (B) R5-r3-2: RecursionError で打ち切ったユニットと 'module unresolved' の早期 return でも、宣言 D_kind
  （と D_kind_by_tool）は annotations から読む。ハンドラの中の parse_d_kind の失敗で木全体を落とさない。
* (C) R5-r1-6: ユニットの走査の途中で木の時間上限に当たった分を manifest の truncations に
  `{relpath, cap: tree_budget, count}` で残す（前処理側の tree_budget_prep と同じ形）。probe の cap 名は
  `TRUNCATED(<cap>)` の接頭から決め、接頭の無いもの（WALL_CLOCK_CAP 超え）は wall_clock のまま。

「今落ちる」テスト = 直すべき挙動、「今通る」テスト = 反例・対照（直した後も通らなければならない）。
"""

from __future__ import annotations

import dataclasses
import json
import os
import time as _real_time

import pytest

import authgap.runner as RN
from authgap.analyze import analyze_unit_f0a
from authgap.entries import find_units
from authgap.ir import VAL_OPAQUE_REASONS
from authgap.report import determinism_signature, manifest_json, probe_json
from authgap.runner import RunConfig, run
from authgap.srcindex import SourceIndex

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA = os.path.join(ROOT, "docs", "manifest.schema.json")

DROPPED_REASONS = ("parse_failure", "ast_node_cap")


def _write_tree(tmp_path_factory, name, files):
    d = tmp_path_factory.mktemp(name)
    for rel, src in files.items():
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(src, encoding="utf-8")
    return d


def _scan(d, **kw):
    return run(RunConfig(src_root=str(d), population="mcp_server", full=kw.pop("full", True), **kw))


def _by_name(man):
    return {u["unit"]["qualname"]: u for u in man["units"]}


def _notes_of_rows(u):
    return [n for r in u["rows"] for n in r.get("notes", [])]


def _has_contra(u, decl):
    return f"contradiction:{decl}" in _notes_of_rows(u)


def _has_unknown(u, decl):
    return any(n.startswith(f"contradiction_unknown:{decl}:") for n in _notes_of_rows(u))


def _dropped_marks(u) -> list[str]:
    """ユニットに付いた「落としたファイルへの依存」の印を文字列で返す（fix_outline (A) の 2 つの形を両方受ける）。

    * notes の `depends_on_dropped:<relpath>`（後ろに理由が付いてもよい）
    * `unresolved_in_tree_calls` の項で、理由（parse_failure / ast_node_cap）を持つもの
    """
    out = [n for n in (u.get("notes") or []) if str(n).startswith("depends_on_dropped:")]
    for item in u.get("unresolved_in_tree_calls") or []:
        if isinstance(item, dict) and any(v in DROPPED_REASONS for v in item.values() if isinstance(v, str)):
            out.append(json.dumps(item, sort_keys=True, ensure_ascii=False))
    return out


def _marked(u, relpath: str) -> bool:
    return any(relpath in m for m in _dropped_marks(u))


# ===========================================================================
# (A) R5-r2-2: 落とした木内モジュールへの依存の印
# ===========================================================================

# どの Python 3 でも SyntaxError（版ずれに依らない parse 失敗。所見の再現は 3.14 の `except A, B:`）
BAD_BROKEN = '''import subprocess


def run(cmd: str) -> str:
    print "unreachable"
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout
'''

BAD_OK = '''import subprocess


def run(cmd: str) -> str:
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout
'''


def _big(n_rows: int) -> str:
    # 実 sink + 埋め草。n_rows=7000 で AST_NODE_CAP（2 万ノード）を超える（所見の再現と同じ形）
    lines = ["import os", "", "", "def wipe(path: str) -> None:", "    os.remove(path)", "", "", "TABLE = ["]
    lines += [f"    ({i}, 'v{i}')," for i in range(n_rows)]
    lines.append("]")
    return "\n".join(lines) + "\n"


HELPER = '''import bad


def go(cmd: str) -> str:
    return bad.run(cmd)
'''

SERVER = '''import bad
import big
import helper
import zz_external_pkg_u49
from bad import run as bad_run
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")


@mcp.tool(annotations={"readOnlyHint": True})
def via_bad(cmd: str) -> str:
    return bad.run(cmd)


@mcp.tool(annotations={"readOnlyHint": True})
def via_big(path: str) -> str:
    big.wipe(path)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def via_from_bad(cmd: str) -> str:
    return bad_run(cmd)


@mcp.tool(annotations={"readOnlyHint": True})
def via_helper(cmd: str) -> str:
    return helper.go(cmd)


@mcp.tool(annotations={"readOnlyHint": True})
def untouched(x: str) -> str:
    return x.upper()


@mcp.tool(annotations={"readOnlyHint": True})
def external(x: str) -> str:
    return zz_external_pkg_u49.lookup(x)
'''

CALLERS = ("via_bad", "via_big", "via_from_bad", "via_helper")
DEP_OF = {"via_bad": "bad.py", "via_big": "big.py", "via_from_bad": "bad.py", "via_helper": "bad.py"}


@pytest.fixture(scope="module")
def dropped_tree(tmp_path_factory):
    return _write_tree(
        tmp_path_factory,
        "u49_dropped",
        {"bad.py": BAD_BROKEN, "big.py": _big(7000), "helper.py": HELPER, "server.py": SERVER},
    )


@pytest.fixture(scope="module")
def dropped(dropped_tree):
    return manifest_json(_scan(dropped_tree), "t")


@pytest.fixture(scope="module")
def ok(tmp_path_factory):
    # 対照: 同じ server.py で bad.py を直し big.py の埋め草を外した木（= 本来の判定）
    d = _write_tree(
        tmp_path_factory,
        "u49_ok",
        {"bad.py": BAD_OK, "big.py": _big(0), "helper.py": HELPER, "server.py": SERVER},
    )
    return manifest_json(_scan(d), "t")


def test_a_premise_files_are_dropped(dropped):
    # 前提: bad.py は parse 失敗、big.py は AST_NODE_CAP で落ちている（ファイル水準の記録。今も直した後も出る）
    assert "bad.py" in dropped["parse_failures"], dropped["parse_failures"]
    caps = {(t.get("relpath"), t.get("cap")) for t in dropped["truncations"]}
    assert ("big.py", "ast_node_cap") in caps, dropped["truncations"]
    assert set(CALLERS) | {"untouched", "external"} <= set(_by_name(dropped)), sorted(_by_name(dropped))


def test_a_premise_ok_tree_is_d1_contradiction(ok):
    # 前提（対照、今通る）: 落とさなければ本来は D1 矛（spawn_model / fs_write）。所見の broken_helper_ok と同じ
    us = _by_name(ok)
    for name in CALLERS:
        assert _has_contra(us[name], "D1"), (name, us[name]["rows"])


@pytest.mark.parametrize("name", CALLERS)
def test_a_unit_marks_dropped_dependency(dropped, name):
    """R5-r2-2 の expected（規則 4）: 落とした木内モジュールの定義を呼ぶユニットに、依存先の relpath つきの印を残す。

    via_from_bad は `from bad import run` の形、via_helper は深さ 1 を経る形（木内の読めるモジュール経由）。
    """
    u = _by_name(dropped)[name]
    assert _marked(u, DEP_OF[name]), {"notes": u.get("notes"), "unresolved_in_tree_calls": u.get("unresolved_in_tree_calls")}


@pytest.mark.parametrize("name", CALLERS)
def test_a_mark_does_not_change_rows_or_effects(dropped, name):
    """D64 U49「印・記録を足すだけで rows / verdict / effects は変えない」。fix_outline: 効果の無い行を作って
    「不」に数えるのは別の決定（§7 は効果の無い行を作らない）。— 素朴な直し方（不の行を足す）で壊れる反例。"""
    u = _by_name(dropped)[name]
    assert u["effects"] == [], u["effects"]
    assert u["rows"] == [], u["rows"]
    assert not _has_contra(u, "D1") and not _has_unknown(u, "D1")


@pytest.mark.parametrize("name", CALLERS)
def test_a_opaque_vocabulary_is_not_reused(dropped, name):
    """fix_outline「凍結語彙 VAL_OPAQUE_REASONS は動かさない。既存の `cap`（summary_cap 用）を流用しない」。

    外部呼び出しと同じ `unresolved` は残り、`cap` は足されない（今通る）。
    """
    u = _by_name(dropped)[name]
    reasons = set(u.get("opaque_reasons") or [])
    assert reasons <= VAL_OPAQUE_REASONS, reasons
    assert "unresolved" in reasons, reasons
    assert "cap" not in reasons, reasons


def test_a_val_opaque_vocabulary_frozen():
    # D64 U49「VAL_OPAQUE_REASONS は動かさない」（CLAUDE.md の語彙表: 8 種）
    assert VAL_OPAQUE_REASONS == frozenset(
        {"depth", "unresolved", "receiver", "recursion", "dynamic", "cap", "loop", "context"}
    )


@pytest.mark.parametrize("name", ["untouched", "external"])
def test_a_no_mark_without_dropped_call(dropped, name):
    """対照（今通る）: 落としたモジュールを呼ばないツール（同じファイルにあっても）と、木に無い外部パッケージを
    呼ぶツールには印を付けない。fix_outline (A) は印を engine の木内解決（呼び出しの解決）に置く。"""
    u = _by_name(dropped)[name]
    assert _dropped_marks(u) == [], _dropped_marks(u)


@pytest.mark.parametrize("name", CALLERS + ("untouched", "external"))
def test_a_no_mark_when_nothing_dropped(ok, name):
    # 対照（今通る）: 何も落としていない木では、どのユニットにも印が付かない（印が余計に付かない）
    assert _dropped_marks(_by_name(ok)[name]) == []


def test_a_ok_tree_rows_unchanged(ok):
    # 対照（今通る）: 何も落としていない木の判定はそのまま（via_* は D1 矛、untouched は行なし）
    us = _by_name(ok)
    assert us["untouched"]["rows"] == []
    assert all(_has_contra(us[n], "D1") for n in CALLERS)


def test_a_marks_are_deterministic(dropped_tree):
    # 印を足しても 3 回一致の比較（volatile を落とした manifest）は変わらない（今通る）
    a = determinism_signature(manifest_json(_scan(dropped_tree), "a"))
    b = determinism_signature(manifest_json(_scan(dropped_tree), "b"))
    assert a == b


SAME_NAME_SERVER = '''import big
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")


@mcp.tool(annotations={"readOnlyHint": True})
def q(x: str) -> str:
    return big.lookup(x)
'''


def test_a_counterexample_same_name_external_keeps_verdict(tmp_path_factory):
    """検証役の反例（R5-r2-2 generality）: 木の中の落としたファイル tests/big.py と同名の外部パッケージを
    `import big` すると、resolve_import_module の厳密解決（D17 改訂 2）が木内側に解いて印が付きうる。
    fix_outline はこれを保守的な向き（V3 の抜き取りから外しすぎる側）として受け入れ、限界として記す。
    **印の有無はここでは決めない。判定（rows / effects）が変わらないことだけを確かめる**（今通る）。"""
    d = _write_tree(tmp_path_factory, "u49_same_name", {"tests/big.py": _big(7000), "server.py": SAME_NAME_SERVER})
    man = manifest_json(_scan(d), "t")
    assert ("tests/big.py", "ast_node_cap") in {(t.get("relpath"), t.get("cap")) for t in man["truncations"]}
    u = _by_name(man)["q"]
    assert u["effects"] == [] and u["rows"] == []
    assert not _has_contra(u, "D1") and not _has_unknown(u, "D1")
    # 付くなら、指す先は木内の落としたファイル
    for m in _dropped_marks(u):
        assert "tests/big.py" in m, m


# ===========================================================================
# (B) R5-r3-2: RecursionError の代替 report と 'module unresolved' でも D_kind を読む
# ===========================================================================

CHAIN = "sqlite3.connect('data.db')" + ".cursor().connection" * 400

DEEP_SERVER = f'''import sqlite3
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")


@mcp.tool(annotations={{"readOnlyHint": True}})
def deep(sql: str) -> str:
    conn = {CHAIN}
    return str(conn.execute(sql).fetchall())


@mcp.tool(annotations={{"readOnlyHint": True}})
def shallow(sql: str) -> str:
    conn = sqlite3.connect("data.db")
    return str(conn.execute(sql).fetchall())
'''

DEEP_LOWLEVEL = f'''import sqlite3

from mcp.server import Server
from mcp.types import Tool, ToolAnnotations

server = Server("t")


@server.list_tools()
async def list_tools():
    return [
        Tool(name="read_q", description="r", inputSchema={{}}, annotations=ToolAnnotations(readOnlyHint=True)),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "read_q":
        conn = {CHAIN}
        return str(conn.execute(arguments["sql"]).fetchall())
    raise ValueError(name)
'''


@pytest.fixture(scope="module")
def deep_tree(tmp_path_factory):
    return _write_tree(tmp_path_factory, "u49_deep", {"server.py": DEEP_SERVER})


@pytest.fixture(scope="module", params=[True, False], ids=["full", "f0a"])
def deep_res(request, deep_tree):
    return _scan(deep_tree, full=request.param)


def test_b_premise_deep_is_truncated(deep_res):
    # 前提（今通る）: deep は val エンジンの RecursionError で TRUNCATED(recursion)、shallow は解析される
    us = _by_name(manifest_json(deep_res, "t"))
    assert "TRUNCATED(recursion)" in us["deep"]["notes"], us["deep"]["notes"]
    assert "TRUNCATED(recursion)" not in us["shallow"]["notes"]
    assert us["shallow"]["D_kind"]["explicit"] == ["readOnlyHint"]


def test_b_truncated_unit_keeps_d_kind(deep_res):
    """R5-r3-2 の expected: D_kind は annotations から読む（仕様書 320 行目）ので解析の成否と独立。
    同じ annotations の shallow と同じ D_kind を持つ。"""
    us = _by_name(manifest_json(deep_res, "t"))
    assert us["deep"]["D_kind"]["bottom"] is False, us["deep"]["D_kind"]
    assert us["deep"]["D_kind"]["explicit"] == ["readOnlyHint"], us["deep"]["D_kind"]
    assert us["deep"]["D_kind"] == us["shallow"]["D_kind"]


def test_b_truncated_unit_has_no_rows(deep_res):
    """D64 U49「rows / verdict / effects は変えない」: 打ち切ったユニットは宣言を持っても行を作らない
    （矛にも不にも数えない。今通る）。TRUNCATED(recursion) の印は残る。"""
    u = _by_name(manifest_json(deep_res, "t"))["deep"]
    assert u["rows"] == [] and u["effects"] == []
    assert "TRUNCATED(recursion)" in u["notes"]


def test_b_shallow_unchanged(deep_res):
    # 対照（今通る）: 同じ木の他のユニットはそのまま解析され、効果が出る
    u = _by_name(manifest_json(deep_res, "t"))["shallow"]
    assert u["effects"], u


def test_b_shallow_contradiction_unchanged(deep_tree):
    # 対照（今通る）: full では shallow は D1 矛（DB に MODEL の SQL）のまま。打ち切りの修正で判定は変わらない
    u = _by_name(manifest_json(_scan(deep_tree), "t"))["shallow"]
    assert _has_contra(u, "D1"), u["rows"]


def test_b_probe_counts_truncated_unit_with_d_kind(deep_tree):
    # R5-r3-2 の expected: probe の n_units_with_D_kind（r_kind の分子の生の件数）から黙って消えない
    p = probe_json(_scan(deep_tree, full=False), "t")
    assert p["n_units_with_D_kind"] == 2, p["n_units_with_D_kind"]


@pytest.mark.parametrize("full", [True, False], ids=["full", "f0a"])
def test_b_truncated_dispatch_unit_keeps_d_kind_by_tool(tmp_path_factory, full):
    """R5-r3-2 fix_outline (B): 代替 report に d_kind_by_tool=parse_d_kind_by_tool(unit) も入れる。
    低レベル MCP のハンドラが打ち切られても、`Tool(...)` の宣言の join は残る。"""
    d = _write_tree(tmp_path_factory, "u49_deep_ll", {"server.py": DEEP_LOWLEVEL})
    us = _by_name(manifest_json(_scan(d, full=full), "t"))
    u = us["call_tool"]
    assert "TRUNCATED(recursion)" in u["notes"], u["notes"]  # 前提
    by_tool = u.get("D_kind_by_tool") or {}
    assert "read_q" in by_tool, u.get("D_kind_by_tool")
    assert by_tool["read_q"]["explicit"] == ["readOnlyHint"]
    assert u["rows"] == []


def test_b_handler_second_recursion_does_not_drop_tree(deep_tree, monkeypatch):
    """検証役の実装上の注意（R5-r3-2 generality notes）: except の中の parse_d_kind も RecursionError を投げうる。
    それで木全体を落とさない（⊥ に戻す）。素朴に代替 report の中で parse_d_kind を呼ぶだけの直し方で壊れる反例。

    parse_d_kind を deep に対してだけ RecursionError を投げるものに差し替える（今通る。直した後も通ること）。
    """
    import authgap.analyze as AN
    import authgap.dparse as DP

    orig = DP.parse_d_kind

    def boom(unit, *a, **kw):
        if unit.qualname == "deep":
            raise RecursionError("simulated")
        return orig(unit, *a, **kw)

    for mod in (DP, AN, RN):
        if hasattr(mod, "parse_d_kind"):
            monkeypatch.setattr(mod, "parse_d_kind", boom)
    res = _scan(deep_tree)
    us = _by_name(manifest_json(res, "t"))
    assert set(us) == {"deep", "shallow"}, sorted(us)
    assert us["deep"]["D_kind"]["bottom"] is True
    assert any(str(n).startswith("TRUNCATED(recursion)") for n in us["deep"]["notes"]), us["deep"]["notes"]
    assert us["deep"]["rows"] == []
    assert us["shallow"]["D_kind"]["explicit"] == ["readOnlyHint"]
    assert us["shallow"]["effects"]


def test_b_handler_second_recursion_leaves_note(deep_tree, monkeypatch):
    """fix_outline (B)「失敗したら ⊥ に戻し、notes に印を残す」: parse_d_kind が失敗したことを
    TRUNCATED(recursion) とは別の印で残す（印の名前は決めない。wall_clock 以外の別の注記があること）。"""
    import authgap.analyze as AN
    import authgap.dparse as DP

    orig = DP.parse_d_kind

    def boom(unit, *a, **kw):
        if unit.qualname == "deep":
            raise RecursionError("simulated")
        return orig(unit, *a, **kw)

    for mod in (DP, AN, RN):
        if hasattr(mod, "parse_d_kind"):
            monkeypatch.setattr(mod, "parse_d_kind", boom)
    u = _by_name(manifest_json(_scan(deep_tree), "t"))["deep"]
    others = [n for n in u["notes"] if n not in ("TRUNCATED(recursion)", "TRUNCATED(wall_clock)")]
    assert others, u["notes"]


def test_b_module_unresolved_keeps_d_kind(deep_tree):
    """R5-r3-2 設計の検証役: analyze_unit_f0a の 'module unresolved' の早期 return でも D_kind は ⊥ になる（同じ原因）。
    fix_outline「設定を関数の冒頭に動かすと同じ原因も直る」。"""
    index = SourceIndex(str(deep_tree))
    index.build()
    unit = next(u for u in find_units(index) if u.qualname == "shallow")
    ghost = dataclasses.replace(unit, module="zz_no_such_module_u49")
    report = analyze_unit_f0a(index, ghost)
    assert "module unresolved" in report.notes  # 前提
    assert not report.d_kind.is_bottom, report.d_kind
    assert not report.effects and not report.rows  # 解析はしない（行も効果も作らない）


# ===========================================================================
# (C) R5-r1-6: 走査の途中の時間切れを manifest の truncations に残す
# ===========================================================================

BUDGET_SERVER = '''from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")
''' + "".join(
    f'''

@mcp.tool(annotations={{"readOnlyHint": True}})
def write_{i}(path: str) -> str:
    with open(path, "w") as f:
        f.write("x")
    return "ok"
'''
    for i in range(5)
)


class _FakeTime:
    """runner の `time` だけを差し替える（決定論のため）。1 つ目のユニットを解析し終えたら `jump` 秒進む。"""

    def __init__(self, jump: float, after_calls: int | None = None):
        self.jump = jump
        self.after_calls = after_calls
        self.n_calls = 0
        self.analyzed = 0

    def _now(self) -> float:
        self.n_calls += 1
        if self.after_calls is not None:
            return 0.0 if self.n_calls <= self.after_calls else self.jump
        return 0.0 if self.analyzed == 0 else self.jump

    def monotonic(self) -> float:
        return self._now()

    def perf_counter(self) -> float:
        return self._now()

    def __getattr__(self, name):
        return getattr(_real_time, name)


def _install_clock(monkeypatch, clock: _FakeTime):
    monkeypatch.setattr(RN, "time", clock)
    for fname in ("analyze_unit_full", "analyze_unit_f0a"):
        orig = getattr(RN, fname)

        def wrapped(*a, _orig=orig, **kw):
            try:
                return _orig(*a, **kw)
            finally:
                clock.analyzed += 1

        monkeypatch.setattr(RN, fname, wrapped)


@pytest.fixture(scope="module")
def budget_tree(tmp_path_factory):
    return _write_tree(tmp_path_factory, "u49_budget", {"server.py": BUDGET_SERVER})


@pytest.fixture()
def budget_res(budget_tree, monkeypatch):
    # 1 つ目を解析した後で 5 秒進む: max_tree_seconds=3 を超え、WALL_CLOCK_CAP（10 秒）は超えない
    _install_clock(monkeypatch, _FakeTime(jump=5.0))
    return _scan(budget_tree, max_tree_seconds=3.0)


def test_c_premise_mid_loop_budget(budget_res):
    # 前提（今通る）: 1 つ解析して残り 4 つを走査の途中の時間上限で打ち切った（前処理側ではない）
    assert budget_res.tree_budget_skipped == 4
    man = manifest_json(budget_res, "t")
    assert [u["unit"]["qualname"] for u in man["units"]] == ["write_0"]
    assert not any(t.get("cap") == "tree_budget_prep" for t in man["truncations"])


def test_c_manifest_records_tree_budget(budget_res):
    """R5-r1-6 の expected（仕様書 640 行目、runner.py:41 の約束、D52 と同じ形）: manifest の truncations に
    `{relpath, cap: "tree_budget", count: 4}` の行が出る。"""
    man = manifest_json(budget_res, "t")
    rows = [t for t in man["truncations"] if t.get("cap") == "tree_budget"]
    assert len(rows) == 1, man["truncations"]
    assert rows[0]["count"] == 4, rows
    assert set(rows[0]) == {"relpath", "cap", "count"}, rows  # 前処理側 tree_budget_prep と同じ形


def test_c_probe_names_tree_budget(budget_res):
    # R5-r1-6 の expected: probe の cap 名は TRUNCATED(<cap>) の接頭から決める（wall_clock と誤記しない）
    p = probe_json(budget_res, "t")
    caps = [t.get("cap") for t in p["truncations"]]
    assert "tree_budget" in caps, p["truncations"]
    assert "wall_clock" not in caps, p["truncations"]


def test_c_record_does_not_change_units_or_rows(budget_res):
    """D64 U49「記録を足すだけ」（今通る）: 打ち切ったユニットを manifest の units に足さない。
    解析した write_0 の判定（D1 矛）はそのまま。"""
    man = manifest_json(budget_res, "t")
    assert [u["unit"]["qualname"] for u in man["units"]] == ["write_0"]
    assert _has_contra(man["units"][0], "D1"), man["units"][0]["rows"]


def test_c_no_budget_row_without_budget(budget_tree):
    # 対照（今通る）: 時間上限に当たらなければ tree_budget の行は出ない（0 件と区別できる）
    man = manifest_json(_scan(budget_tree), "t")
    assert len(man["units"]) == 5
    assert not any(str(t.get("cap", "")).startswith("tree_budget") for t in man["truncations"]), man["truncations"]


def test_c_counterexample_prep_budget_not_double_counted(budget_tree, monkeypatch):
    """素朴な直し方で壊れる反例: 前処理で打ち切った経路（D52）も res.tree_budget_skipped と
    `TRUNCATED(tree_budget)` の文字列を持つ。それをそのまま truncations に足すと tree_budget_prep と二重に数える。
    打ち切りの行は tree_budget_prep の 1 本だけで、件数の合計はユニット数（今通る）。"""
    _install_clock(monkeypatch, _FakeTime(jump=100.0, after_calls=1))
    res = _scan(budget_tree, max_tree_seconds=3.0, prep_budget_exit=True)
    assert res.tree_budget_skipped == 5  # 前提: 前処理側の打ち切り
    man = manifest_json(res, "t")
    assert man["units"] == []
    budget = [t for t in man["truncations"] if str(t.get("cap", "")).startswith("tree_budget")]
    assert [t["cap"] for t in budget] == ["tree_budget_prep"], man["truncations"]
    assert sum(t["count"] for t in budget) == 5


def test_c_counterexample_unprefixed_stays_wall_clock(budget_tree, monkeypatch):
    """fix_outline (C) 守ること: runner.py:146 は WALL_CLOCK_CAP 超えのユニットを接頭無しの unit_id で入れる。
    接頭の無いものは wall_clock のまま（今通る）。ユニットの TRUNCATED(wall_clock) の印も残る。"""
    _install_clock(monkeypatch, _FakeTime(jump=100.0))
    res = _scan(budget_tree)  # 木の時間上限なし。1 つ目だけ WALL_CLOCK_CAP を超える
    p = probe_json(res, "t")
    wall = [t for t in p["truncations"] if t.get("cap") == "wall_clock"]
    assert len(wall) == 1, p["truncations"]
    assert not any(t.get("cap") == "tree_budget" for t in p["truncations"])
    us = _by_name(manifest_json(res, "t"))
    assert "TRUNCATED(wall_clock)" in us["write_0"]["notes"]
    assert len(us) == 5


def test_c_probe_names_recursion(deep_tree):
    # R5-r1-6 fix_sketch: TRUNCATED(recursion):<unit> の cap 名は recursion（今は一律に wall_clock）
    p = probe_json(_scan(deep_tree, full=False), "t")
    caps = [t.get("cap") for t in p["truncations"]]
    assert "recursion" in caps, p["truncations"]
    assert "wall_clock" not in caps, p["truncations"]


# ===========================================================================
# 共通: manifest の schema（unresolved_in_tree_calls / truncations の形を変えたら schema の版を上げる）
# ===========================================================================


def test_manifests_validate_against_schema(dropped, budget_res, deep_tree):
    # fix_outline「unresolved_in_tree_calls の形を変えるなら docs/manifest.schema.json の版を上げる」（今通る）
    jsonschema = pytest.importorskip("jsonschema")
    with open(SCHEMA, encoding="utf-8") as fh:
        schema = json.load(fh)
    for man in (dropped, manifest_json(budget_res, "t"), manifest_json(_scan(deep_tree), "t")):
        jsonschema.validate(man, schema)
