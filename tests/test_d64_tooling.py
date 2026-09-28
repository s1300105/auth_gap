"""D64 段階 A の評価の道具（scripts/ だけ）の修正。**期待値はこのテストで、scripts/ を直す前に書いた。**

所見と直し方は `docs/review_triage.md`（U50 / U51 / U52 / U53 / U54 / U32）と `evidence/review/triage.json`。
検証役が見つけた「素朴な直し方で壊れる反例」もここに入れる。
"""

from __future__ import annotations

import json
import os
import subprocess
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


# ---------------------------------------------------------------------------
# 小さな run ディレクトリを作る道具
# ---------------------------------------------------------------------------

def _row(site, kind, relpath, lineno, notes=(), verdicts=("CONTRADICTION",), slot="path"):
    return {"site": site, "kind": kind, "relpath": relpath, "lineno": lineno, "slot": slot,
            "notes": list(notes), "verdicts": list(verdicts)}


def _unit(qualname, relpath, lineno, rows, effects=(), unit_id=None, explicit=("readOnlyHint",)):
    return {
        "unit": {"qualname": qualname, "relpath": relpath, "lineno": lineno, "tool_name": qualname,
                 "unit_id": unit_id or f"mcp:{qualname}:abc"},
        "D_kind": {"explicit": list(explicit)},
        "rows": list(rows),
        "effects": list(effects),
    }


def _write_run(d, trees: dict, summary_trees=None, extra_files=None):
    os.makedirs(d, exist_ok=True)
    for name, units in trees.items():
        with open(os.path.join(d, f"{name}.json"), "w", encoding="utf-8") as fh:
            json.dump({"units": units}, fh)
    if summary_trees is not None:
        with open(os.path.join(d, "summary.json"), "w", encoding="utf-8") as fh:
            json.dump({"trees": [{"tree": t, "status": s} for t, s in summary_trees]}, fh)
    for fn, obj in (extra_files or {}).items():
        with open(os.path.join(d, fn), "w", encoding="utf-8") as fh:
            json.dump(obj, fh)
    return d


D1 = ("contradiction:D1", "contradiction_reason:D1:fs_write")


# ---------------------------------------------------------------------------
# U52: run ディレクトリの manifest の集合は summary.json の ok の木で決める（R5-r1-4 / R5-r2-7）
# ---------------------------------------------------------------------------

def test_run_manifests_uses_summary_and_warns(tmp_path):
    from scripts.runlib import run_manifests

    u = _unit("rm", "server.py", 3, [_row("os.remove", "FS_WRITE", "server.py", 4, D1)])
    d = _write_run(
        str(tmp_path / "run"),
        {"A9__vuln": [u], "eval_01": [u], "stale-tree": [u]},  # stale-tree は summary に無い（古い manifest）
        summary_trees=[("A9__vuln", "ok"), ("eval_01", "ok"), ("gone-tree", "ok"), ("bad-tree", "analysis_failed")],
        extra_files={"notes.json": {"hello": 1}},  # manifest 以外の .json（素朴な直し方の反例）
    )
    got, warnings = run_manifests(d)
    names = [t for t, _ in got]
    # 「-」の無い名前も読む。summary に無い古い manifest と manifest 以外の .json は読まない
    assert names == ["A9__vuln", "eval_01"]
    joined = "\n".join(warnings)
    assert "stale-tree" in joined  # 余分な manifest を警告する
    assert "gone-tree" in joined  # summary にあるのにファイルが無いものを警告する


def test_run_manifests_without_summary_falls_back(tmp_path):
    from scripts.runlib import run_manifests

    u = _unit("rm", "server.py", 3, [])
    d = _write_run(str(tmp_path / "run"), {"A9__vuln": [u]}, summary_trees=None,
                   extra_files={"notes.json": {"hello": 1}, "contradictions.json": {"n": 0, "rows": []}})
    got, warnings = run_manifests(d)
    assert [t for t, _ in got] == ["A9__vuln"]  # units 鍵の無いファイルは飛ばす（KeyError で落ちない）
    assert any("summary.json" in w for w in warnings)


def test_contradiction_by_decl_reads_names_without_hyphen(tmp_path):
    from scripts.contradiction_by_decl import load_reasons

    u = _unit("rm", "server.py", 3, [_row("os.remove", "FS_WRITE", "server.py", 4, D1)])
    d = _write_run(str(tmp_path / "run"), {"A9__vuln": [u]}, summary_trees=[("A9__vuln", "ok")])
    reasons = load_reasons(d)
    assert len(reasons) == 1  # 以前は「-」の無い名前を黙って読み飛ばして 0 だった


# ---------------------------------------------------------------------------
# U50: 鍵に位置と宣言を入れる（R5-r1-3 / R5-r3-3）
# ---------------------------------------------------------------------------

def _two_modules_same_name():
    a = _unit("delete_file", "pkg/a.py", 10, [_row("os.remove", "FS_WRITE", "pkg/a.py", 12, D1)])
    b = _unit("delete_file", "pkg/b.py", 20, [_row("os.remove", "FS_WRITE", "pkg/b.py", 22, D1)])
    return [a, b]


def test_same_qualname_in_two_modules_counts_twice_by_decl(tmp_path):
    from scripts.contradiction_by_decl import load_reasons

    d = _write_run(str(tmp_path / "run"), {"v2-x": _two_modules_same_name()}, summary_trees=[("v2-x", "ok")])
    assert len(load_reasons(d)) == 2


def test_same_qualname_in_two_modules_counts_twice_compare_scans(tmp_path):
    from scripts.compare_scans import load

    d = _write_run(str(tmp_path / "run"), {"v2-x": _two_modules_same_name()}, summary_trees=[("v2-x", "ok")])
    m = load(d)
    assert len({c[:-1] for c in m["contradictions"]}) == 2


def test_same_qualname_in_two_modules_counts_twice_intersection(tmp_path):
    from scripts.intersection_rows import scan

    sel_inj = ("GAP_SELECT", "GAP_INJECT")
    a = _unit("f", "pkg/a.py", 1, [_row("os.remove", "FS_WRITE", "pkg/a.py", 2, (), verdicts=sel_inj)])
    b = _unit("f", "pkg/b.py", 1, [_row("os.remove", "FS_WRITE", "pkg/b.py", 2, (), verdicts=sel_inj)])
    d = _write_run(str(tmp_path / "run"), {"v2-x": [a, b]}, summary_trees=[("v2-x", "ok")])
    assert scan(d)["n_intersection_rows"] == 2


def test_same_qualname_in_two_modules_two_candidate_rows(tmp_path):
    from scripts.scan_v2 import _contradiction_rows

    man = {"units": _two_modules_same_name()}
    # unit_id が同じでも（schema_hash が同じ同名ツール）位置が違えば別の行
    for u in man["units"]:
        u["unit"]["unit_id"] = "mcp:delete_file:same"
    assert len(_contradiction_rows("v2-x", man)) == 2


def test_compare_scans_sees_d1_loss_when_d3_remains(tmp_path):
    from scripts.compare_scans import load

    before = _unit("fetch", "s.py", 1, [_row("requests.request", "NET", "s.py", 2,
                                            ("contradiction:D1", "contradiction:D3"))])
    after = _unit("fetch", "s.py", 1, [_row("requests.request", "NET", "s.py", 2, ("contradiction:D3",))])
    a = load(_write_run(str(tmp_path / "a"), {"v2-x": [before]}, summary_trees=[("v2-x", "ok")]))
    b = load(_write_run(str(tmp_path / "b"), {"v2-x": [after]}, summary_trees=[("v2-x", "ok")]))
    removed = a["contradictions"] - b["contradictions"]
    assert len(removed) == 1 and next(iter(removed))[-1] == "D1"


def test_compare_scans_keeps_rows_without_decl_note(tmp_path):
    from scripts.compare_scans import load

    u = _unit("f", "s.py", 1, [_row("os.system", "SPAWN", "s.py", 2, ())])  # 注記の無い CONTRADICTION 行
    m = load(_write_run(str(tmp_path / "a"), {"v2-x": [u]}, summary_trees=[("v2-x", "ok")]))
    assert len(m["contradictions"]) == 1 and next(iter(m["contradictions"]))[-1] == "?"


# ---------------------------------------------------------------------------
# U51: 候補表の位置と destructive（R5-r3-1 / R5-r1-8）
# ---------------------------------------------------------------------------

def test_candidate_row_position_is_a_real_pair():
    from scripts.scan_v2 import _contradiction_rows

    u = _unit("t", "server.py", 5, [
        _row("builtins.open", "FS_WRITE", "server.py", 30, D1),
        _row("builtins.open", "FS_WRITE", "helpers.py", 3, D1),
    ], effects=[
        {"site": "builtins.open", "kind": "FS_WRITE", "relpath": "server.py", "lineno": 30, "destructive": True},
        {"site": "builtins.open", "kind": "FS_WRITE", "relpath": "helpers.py", "lineno": 3, "destructive": True},
    ])
    (row,) = _contradiction_rows("v2-x", {"units": [u]})
    # 以前は relpath=server.py（最初の行）と lineno=3（別ファイルの行）の実在しない組を出していた
    assert (row["relpath"], row["lineno"]) == ("helpers.py", 3)
    assert sorted((loc["relpath"], loc["lineno"]) for loc in row["locations"]) == [("helpers.py", 3), ("server.py", 30)]


def test_candidate_row_destructive_is_from_the_row_effects():
    from scripts.scan_v2 import _contradiction_rows

    # readOnlyHint のもとで追記 open('a')（L8）と上書き open('w')（L10）が両方とも矛
    u = _unit("t", "server.py", 5, [
        _row("builtins.open", "FS_WRITE", "server.py", 8, D1),
        _row("builtins.open", "FS_WRITE", "server.py", 10, D1),
    ], effects=[
        {"site": "builtins.open", "kind": "FS_WRITE", "relpath": "server.py", "lineno": 8, "destructive": False},
        {"site": "builtins.open", "kind": "FS_WRITE", "relpath": "server.py", "lineno": 10, "destructive": True},
    ])
    (row,) = _contradiction_rows("v2-x", {"units": [u]})
    assert row["destructive"] is True  # 素朴な (site, kind, lineno=min) だと False のまま残る
    by_line = {loc["lineno"]: loc["destructive"] for loc in row["locations"]}
    assert by_line == {8: False, 10: True}


def test_candidate_row_single_file_unchanged():
    from scripts.scan_v2 import _contradiction_rows

    u = _unit("t", "server.py", 5, [
        _row("os.remove", "FS_WRITE", "server.py", 16, D1),
        _row("os.remove", "FS_WRITE", "server.py", 10, D1),
    ], effects=[{"site": "os.remove", "kind": "FS_WRITE", "relpath": "server.py", "lineno": 10, "destructive": True},
                {"site": "os.remove", "kind": "FS_WRITE", "relpath": "server.py", "lineno": 16, "destructive": True}])
    (row,) = _contradiction_rows("v2-x", {"units": [u]})
    assert (row["relpath"], row["lineno"]) == ("server.py", 10)  # 同一ファイルなら今と同じ（最小の行）


# ---------------------------------------------------------------------------
# U52: 書き出し（R5-r2-6）と既存の manifest（R5-r2-7）
# ---------------------------------------------------------------------------

def test_write_text_survives_lone_surrogate(tmp_path):
    from authgap.report import canonical_json
    from scripts.scan_v2 import _write_text

    obj = {"units": [{"const": "a\ud800b", "path": "x\\y"}]}
    p = str(tmp_path / "m.json")
    _write_text(p, canonical_json(obj))
    back = json.load(open(p, encoding="utf-8"))
    assert back == obj  # エスケープとして書かれ、元の str に戻る。本物のバックスラッシュは混ざらない
    assert not [f for f in os.listdir(tmp_path) if f != "m.json"]  # 一時ファイルを残さない


def test_refuses_existing_manifests_without_resume(tmp_path):
    from scripts.scan_v2 import _check_out_dir

    d = _write_run(str(tmp_path / "run"), {"v2-x": []})
    assert _check_out_dir(d, resume=False) is not None  # 止める理由を返す
    assert _check_out_dir(d, resume=True) is None
    assert _check_out_dir(str(tmp_path / "empty"), resume=False) is None


# ---------------------------------------------------------------------------
# U32: 効果行の一意の件数を併記する（R4-r1-8。解析器は変えない）
# ---------------------------------------------------------------------------

def test_tally_counts_unique_effects():
    from scripts.scan_v2 import _tally

    e = {"site": "os.remove", "kind": "FS_WRITE", "relpath": "s.py", "lineno": 3, "slots": {}}
    e2 = dict(e, lineno=4)
    man = {"units": [_unit("t", "s.py", 1, [], effects=[e, dict(e), e2])]}
    out = _tally(man)
    assert out["n_effects"] == 3 and out["n_effects_unique"] == 2


# ---------------------------------------------------------------------------
# U53: diff_effects は §7 の判定に効く属性の変化を見る（R5-r2-3）
# ---------------------------------------------------------------------------

def test_diff_effects_value_includes_verdict_attributes(tmp_path):
    from scripts.diff_effects import DUMP

    src = tmp_path / "t"
    src.mkdir()
    (src / "server.py").write_text(
        "from mcp.server.fastmcp import FastMCP\nmcp = FastMCP('t')\n\n"
        "@mcp.tool(annotations={'readOnlyHint': True})\n"
        "def w(path: str) -> str:\n    open(path, 'w').write('x')\n    return 'ok'\n",
        encoding="utf-8",
    )
    p = subprocess.run([sys.executable, "-c", DUMP, str(src)], cwd=ROOT, capture_output=True, text=True,
                       env=dict(os.environ, PYTHONPATH=ROOT))
    assert p.returncode == 0, p.stderr
    vals = [v for rows in json.loads(p.stdout).values() for vs in rows.values() for v in vs]
    assert any("fs_mode=w" in v and "destructive=True" in v for v in vals)


# ---------------------------------------------------------------------------
# U54: run と解析器の実装の指紋（R5-r2-4）
# ---------------------------------------------------------------------------

def test_freeze_refuses_run_from_other_implementation():
    from scripts.freeze_analyzer import run_matches

    ok, why = run_matches({"implementation_sha256_combined": "aaa"}, current_combined="aaa", current_last_commit="c1")
    assert ok
    ok, why = run_matches({"implementation_sha256_combined": "bbb"}, current_combined="aaa", current_last_commit="c1")
    assert not ok and "sha256" in why
    # 欄の無い古い run は authgap の最終 commit で比べる（HEAD の文字列では比べない）
    ok, why = run_matches({"authgap_last_commit": "c1", "analyzer_commit": "docs-only-head"},
                          current_combined="aaa", current_last_commit="c1")
    assert ok and "未コミット" in why
    ok, why = run_matches({"analyzer_commit": "zzz"}, current_combined="aaa", current_last_commit="c1",
                          last_commit_of=lambda c: "c0")
    assert not ok


def test_summary_records_implementation():
    from scripts.scan_v2 import _implementation_record

    rec = _implementation_record()
    for k in ("implementation_sha256_combined", "authgap_dirty", "python", "authgap_last_commit"):
        assert k in rec


@pytest.mark.parametrize("a,b,warn", [("3.10.20", "3.10.20", False), ("3.10.20", "3.12.3", True), (None, "3.12.3", False)])
def test_compare_scans_warns_on_python_version(a, b, warn):
    from scripts.compare_scans import python_warning

    assert (python_warning({"python": a} if a else {}, {"python": b}) is not None) == warn
