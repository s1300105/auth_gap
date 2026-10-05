"""`scripts/final_aggregate.py`（最終評価の集計、手順書 第 23 節・事前登録の下書き (f)(g)）の試験。入力は全部合成。"""

from __future__ import annotations

import csv
import json
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import final_aggregate as fa  # noqa: E402


def _counts(spec):
    """{木: (正, 誤, 不明)}。"""
    return {f"t{i:02d}": c for i, c in enumerate(spec)}


# --- bootstrap と区間 -----------------------------------------------------------------------------------

def test_bootstrap_is_deterministic_for_a_seed():
    counts = _counts([(1, 0, 0), (0, 2, 0), (2, 1, 0), (0, 1, 1), (1, 1, 1), (3, 0, 0), (0, 3, 0), (1, 2, 0),
                      (0, 0, 2), (2, 0, 1), (0, 1, 0), (1, 0, 0)])
    a = fa.tree_metrics(counts, N=30, M=100, n_scanned=500, seed=202610054, reps=2000)
    b = fa.tree_metrics(dict(reversed(list(counts.items()))), N=30, M=100, n_scanned=500, seed=202610054, reps=2000)
    assert a == b  # 入力の順に依らない（木を名前でソートしてから再標本）
    c = fa.tree_metrics(counts, N=30, M=100, n_scanned=500, seed=1, reps=2000)
    assert c["interval"]["a"] != a["interval"]["a"] or c["interval"]["precision_mean"] != a["interval"]["precision_mean"]
    lo, hi = a["interval"]["a"]
    assert lo <= a["a"] <= hi
    # (b)(c) の区間は (a) の区間 × N / 分母
    assert a["interval"]["c"] == pytest.approx([lo * 30 / 100, hi * 30 / 100])
    assert a["interval"]["b"] == pytest.approx([lo * 30 / 500, hi * 30 / 500])


def test_n_below_10_gives_no_interval_but_per_tree_table():
    nine = _counts([(1, 0, 0)] * 5 + [(0, 1, 0)] * 4)
    m = fa.tree_metrics(nine, N=9, M=20, n_scanned=40, seed=1, reps=100)
    assert m["interval"] is None and "D73" in m["interval_note"]
    assert len(m["per_tree"]) == 9 and m["per_tree"][0]["correct"] == 1
    ten = _counts([(1, 0, 0)] * 5 + [(0, 1, 0)] * 5)
    assert fa.tree_metrics(ten, N=10, M=20, n_scanned=40, seed=1, reps=100)["interval"] is not None


def test_c_formula_n_less_than_N():
    counts = _counts([(1, 0, 0)] * 4 + [(0, 2, 0)] * 6)  # n = 10, k = 4
    m = fa.tree_metrics(counts, N=20, M=50, n_scanned=100, seed=1, reps=50)
    assert (m["n"], m["k"]) == (10, 4)
    assert m["a"] == pytest.approx(0.4)
    assert m["K_hat"] == pytest.approx(8.0)  # (k / n) × N
    assert m["c"] == pytest.approx(8 / 50)
    assert m["b"] == pytest.approx(8 / 100)


def test_c_formula_n_equals_N_uses_k():
    counts = _counts([(1, 0, 0)] * 3 + [(0, 1, 0)] * 4)
    m = fa.tree_metrics(counts, N=7, M=21, n_scanned=70, seed=1, reps=50)
    assert m["K_hat"] == 3.0 and m["c"] == pytest.approx(3 / 21) and m["b"] == pytest.approx(3 / 70)


def test_n_greater_than_N_is_an_error():
    with pytest.raises(ValueError):
        fa.tree_metrics(_counts([(1, 0, 0)] * 3), N=2, M=5, n_scanned=10, seed=1, reps=10)


def test_unknown_variants():
    counts = {"a": (1, 1, 1), "b": (0, 0, 2), "c": (2, 0, 0)}
    m = fa.tree_metrics(counts, N=3, M=3, n_scanned=3, seed=1, reps=10)
    # 主: 全部不明の木 b を除く。a = 1/2、c = 1 → 0.75
    assert m["precision_mean"] == pytest.approx(0.75)
    assert m["n_trees_all_unknown"] == 1 and m["n_trees_precision"] == 2
    # 不明を誤: a = 1/3、b = 0、c = 1 → 4/9
    assert m["precision_mean_unknown_as_wrong"] == pytest.approx((1 / 3 + 0 + 1) / 3)
    # k は不明の扱いに依らない
    assert m["k"] == 2
    pl = fa.pair_level([fa.Pair(id=str(i), tree="t", decl="D1", verdict=v)
                        for i, v in enumerate(["正", "正", "誤", "不明", "不明"])])
    assert pl["precision"] == pytest.approx(2 / 3)
    assert pl["precision_unknown_as_wrong"] == pytest.approx(2 / 5)
    assert pl["unknown"] == 2


def test_percentile_is_linear_interpolation():
    xs = [0.0, 1.0, 2.0, 3.0, 4.0]
    assert fa.percentile(xs, 0.5) == 2.0
    assert fa.percentile(xs, 0.025) == pytest.approx(0.1)
    assert fa.percentile(xs, 0.975) == pytest.approx(3.9)


# --- Wilson と κ ---------------------------------------------------------------------------------------

def test_wilson_matches_v4_value_in_procedure():
    lo, hi = fa.wilson(46, 60)
    assert (round(lo * 100, 1), round(hi * 100, 1)) == (64.6, 85.6)  # 手順書 23.4
    lo0, hi0 = fa.wilson(0, 3)
    assert lo0 == pytest.approx(0.0, abs=1e-12) and 0 < hi0 < 1
    assert fa.wilson(0, 0) is None


def test_kappa_hand_computed():
    a = ["正", "正", "正", "誤", "誤", "不明"]
    b = ["正", "正", "誤", "誤", "不明", "不明"]
    # 一致 4/6。期待一致 = (3·2 + 2·2 + 1·2) / 36 = 1/3。κ = (2/3 − 1/3) / (1 − 1/3) = 0.5
    r = fa.cohen_kappa(a, b)
    assert r["percent_agreement"] == pytest.approx(4 / 6)
    assert r["p_expected"] == pytest.approx(1 / 3)
    assert r["kappa"] == pytest.approx(0.5)
    assert r["disagree"] == 2
    same = fa.cohen_kappa(["正"] * 4, ["正"] * 4)
    assert same["kappa"] is None and same["percent_agreement"] == 1.0


# --- 判定表の検証 ---------------------------------------------------------------------------------------

def _crow(**kw):
    base = {"pair_id": "C-D1-001", "tree": "t1", "decl": "D1", "verdict": "正", "reachable": "はい", "violates": "はい",
            "condition_type": "なし", "error_class": "", "write_target": "ログ", "unknown_reason": "",
            "minutes": "12", "ai_used": "なし", "ai_model": "", "ai_log": ""}
    base.update(kw)
    return base


def test_unknown_reason_class_parsing():
    assert fa.parse_unknown_reason("手引きで決まらない: 事例", "x") == "手引きで決まらない"
    assert fa.parse_unknown_reason("外の値：戻り値", "x") == "外の値"
    assert fa.parse_unknown_reason("その他", "x") == "その他"
    with pytest.raises(fa.VocabularyError):
        fa.parse_unknown_reason("外の値かも", "x")


def test_valid_row_parses():
    (p,) = fa.parse_contradiction_rows([_crow()])
    assert p.verdict == "正" and p.conditions == ("なし",) and p.write_target == "ログ"
    (q,) = fa.parse_contradiction_rows([_crow(verdict="誤", violates="いいえ", condition_type="", write_target="",
                                              error_class="E1: lifespan で済む")])
    assert q.error_class == "E1"


@pytest.mark.parametrize("bad", [
    {"verdict": "正しい"},
    {"verdict": ""},
    {"decl": "D5"},
    {"condition_type": "なし;引数"},
    {"condition_type": "引数；初回"},  # 全角の区切りは語彙の外
    {"condition_type": "環境変数"},
    {"condition_type": ""},  # 正なのに空
    {"write_target": "ファイル"},
    {"write_target": ""},  # 正なのに空
    {"decl": "D3", "write_target": "データベース"},  # D3 は通信先の種類
    {"verdict": "誤", "violates": "いいえ", "error_class": "X1 なにか", "write_target": ""},
    {"verdict": "誤", "violates": "いいえ", "error_class": "E10", "write_target": ""},
    {"verdict": "誤", "violates": "いいえ", "error_class": "", "write_target": ""},
    {"error_class": "E3"},  # 正に誤の原因
    {"verdict": "誤"},  # reachable / violates が「はい / はい」なのに誤
    {"reachable": "たぶん"},
    {"verdict": "不明", "reachable": "決められない", "violates": "", "unknown_reason": ""},
    {"ai_used": "少し"},
    {"ai_used": "あり"},  # ai_model / ai_log が空
    {"minutes": "十分"},
    # D76 の書き方の既定
    {"verdict": "不明", "reachable": "決められない", "violates": "", "condition_type": "", "write_target": "",
     "unknown_reason": "よく分からない"},  # 第 19 節の類で始まらない
    {"verdict": "誤", "reachable": "いいえ", "violates": "", "write_target": "", "error_class": "E6: 死んだコード"},
    # ↑ 到達しないのに condition_type（base の「なし」）がある
    {"verdict": "誤", "violates": "いいえ", "condition_type": "", "write_target": "", "error_class": "E3: 組み込みの set"},
    {"verdict": "誤", "reachable": "いいえ", "violates": "", "condition_type": "", "write_target": "",
     "error_class": "E5: パイプ"},
])
def test_vocabulary_errors_raise(bad):
    with pytest.raises(fa.VocabularyError):
        fa.parse_contradiction_rows([_crow(**bad)])


def test_missing_column_and_duplicate_id_raise():
    row = _crow()
    del row["ai_used"]
    with pytest.raises(fa.VocabularyError):
        fa.parse_contradiction_rows([row])
    with pytest.raises(fa.VocabularyError):
        fa.parse_contradiction_rows([_crow(), _crow()])


def _mrow(**kw):
    base = {"pair_id": "M-001", "tree": "t1", "decl": "D1", "outcome": "見落とし", "cause": "語彙", "write_target": "ログ",
            "condition_type": "なし", "depth": "1", "ai_found": "", "minutes": "20", "ai_used": "なし"}
    base.update(kw)
    return base


@pytest.mark.parametrize("bad", [
    {"outcome": "見落とし(深さ4の外)"},
    {"outcome": "見落し"},
    {"cause": "型"},
    {"cause": ""},
    {"decl": "D3"},
    {"depth": "5"},  # 見落としで深さ 4 の外
    {"depth": "x"},
    {"cause": "その他（打ち切り）"},  # D76 で無くなった細分
    {"outcome": "見落とし（深さ 4 の外）", "cause": "語彙", "depth": "6"},
    {"outcome": "不明", "cause": "", "write_target": "", "condition_type": "", "unknown_reason": ""},
    {"outcome": "不明（打ち切り）", "cause": "", "write_target": "", "condition_type": "", "unknown_reason": "外の値: x"},
    {"outcome": "不明", "cause": "", "write_target": "", "condition_type": "", "unknown_reason": "打ち切り"},
])
def test_miss_vocabulary_errors_raise(bad):
    with pytest.raises(fa.VocabularyError):
        fa.parse_miss_rows([_mrow(**bad)])


def test_unknown_sheet_vocabulary_errors_raise():
    good = {"pair_id": "U-D2-001", "tree": "t1", "decl": "D2", "reasons": "net_post", "outcome": "違反", "reachable": "はい",
            "violates": "はい", "write_target": "相手側の状態", "condition_type": "引数", "unknown_reason": "",
            "minutes": "", "ai_used": "なし"}
    assert fa.parse_unknown_rows([good])[0].reasons == ("net_post",)
    for bad in ({"outcome": "違反あり"}, {"decl": "D3"}, {"reasons": "Net-Post"}, {"write_target": ""},
                {"outcome": "違反でない"}):
        with pytest.raises(fa.VocabularyError):
            fa.parse_unknown_rows([{**good, **bad}])


# --- (B)(C) の読み方 -----------------------------------------------------------------------------------

def test_readings_B_and_C_replace_correct_with_wrong():
    ps = [fa.Pair(id="1", tree="a", decl="D1", verdict="正", conditions=("なし",)),
          fa.Pair(id="2", tree="b", decl="D1", verdict="正", conditions=("引数",)),
          fa.Pair(id="3", tree="c", decl="D1", verdict="正", conditions=("引数", "運用者の設定")),
          fa.Pair(id="4", tree="d", decl="D1", verdict="正", conditions=("起動の方法",)),
          fa.Pair(id="5", tree="e", decl="D1", verdict="誤")]
    assert [fa.reading_B(p) for p in ps] == ["正", "正", "誤", "誤", "誤"]
    assert [fa.reading_C(p) for p in ps] == ["正", "誤", "誤", "誤", "誤"]
    cb = fa.condition_breakdown([p for p in ps if p.verdict == "正"])
    assert (cb["A"], cb["B"], cb["C"]) == (4, 2, 1)
    assert cb["per_type"]["引数"] == 2 and cb["per_type"]["運用者の設定"] == 1


# --- 見落とし ------------------------------------------------------------------------------------------

def test_miss_aggregation_separates_beyond_depth4_and_ai_added():
    ms = fa.parse_miss_rows([
        _mrow(pair_id="M-001"),
        _mrow(pair_id="M-002", tree="t2", outcome="見落とし（深さ 4 の外）", cause="深さ", depth="6"),
        _mrow(pair_id="M-003", tree="t3", outcome="反する動作は無い", cause="", write_target="", condition_type="",
              ai_found="server.py:10 open(p, 'w')"),
        _mrow(pair_id="M-004", tree="t4", outcome="不明（打ち切り）", cause="", write_target="", condition_type="",
              unknown_reason="打ち切り: TRUNCATED(depth) の先"),
        _mrow(pair_id="M-005", tree="t5", decl="D2", outcome="解析器が不として出している", cause="", write_target="",
              condition_type="", ai_found="なし"),
    ])
    r = fa.aggregate_misses(ms)["all"]
    assert r["miss_main"] == 1 and r["miss_beyond_depth4"] == 1
    assert r["outcomes"]["不明"] == 1 and r["unknown_truncated_subcount"] == 1
    assert r["miss_with_ai_added"] == 2 and r["ai_added_units"] == ["M-003"]
    assert r["ai_found_checked"] == 2 and r["ai_found_new"] == 1
    assert r["unknown_reason_classes"]["打ち切り"] == 1


# --- 走査の結果から N・M_d（合成の run） -----------------------------------------------------------------

def _unit(q, rel, line, d_kind, rows=()):
    return {"unit": {"qualname": q, "relpath": rel, "lineno": line, "tool_name": q}, "D_kind": d_kind,
            "rows": list(rows), "effects": []}


def _row(site, kind, notes):
    return {"site": site, "kind": kind, "relpath": "s.py", "lineno": 3, "slot": "path", "notes": list(notes),
            "verdicts": ["CONTRADICTION"]}


def _write_run(d, trees):
    os.makedirs(d, exist_ok=True)
    for name, units in trees.items():
        with open(os.path.join(d, f"{name}.json"), "w", encoding="utf-8") as fh:
            json.dump({"units": units}, fh)
    with open(os.path.join(d, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump({"trees": [{"tree": t, "status": "ok"} for t in trees]
                   + [{"tree": "tX", "status": "analysis_failed"}]}, fh)


def _synthetic_run(d):
    ro = {"explicit": ["readOnlyHint"]}
    _write_run(d, {
        "t1": [_unit("a", "s.py", 1, ro, [_row("builtins.open", "FS_WRITE",
                                                ["contradiction:D1", "contradiction_reason:D1:fs_write"])])],
        "t2": [_unit("b", "s.py", 1, ro, [_row("requests.post", "NET", ["contradiction_unknown:D1:net_post"])]),
               _unit("c", "s.py", 9, {"explicit": ["destructiveHint"], "closed_world": True})],
        # readOnlyHint と destructiveHint が両方 explicit（meet の和）: D2 には数えない（解析器の elif と同じ）
        "t3": [_unit("d", "s.py", 1, {"explicit": ["destructiveHint", "readOnlyHint"], "idempotent": True})],
        "t4": [_unit("e", "s.py", 1, {"explicit": ["openWorldHint"], "open_world": True})],
    })


def test_run_facts_counts_N_M_and_scanned(tmp_path):
    d = str(tmp_path / "run")
    _synthetic_run(d)
    f = fa.run_facts(d)
    assert f.n_scanned == 4  # analysis_failed の木は走査した木に入れない
    assert f.status_counts == {"analysis_failed": 1, "ok": 4}
    assert f.N == {"D1": 1, "D2": 0, "D3": 0, "D4": 0}
    assert f.M == {"D1": 3, "D2": 1, "D3": 1, "D4": 0}  # t3 は D1 に数え、D2・D4 には数えない
    assert f.unknown_pairs["D1"] == 1 and f.unknown_reasons["D1"] == {"net_post": 1}


def test_declares_matches_analyzer_conditions():
    assert fa.declares({"explicit": ["readOnlyHint"]}, "D1")
    assert not fa.declares({"explicit": ["readOnlyHint", "destructiveHint"]}, "D2")
    assert fa.declares({"explicit": ["destructiveHint"]}, "D2")
    assert not fa.declares({"explicit": ["openWorldHint"]}, "D3")  # openWorldHint: true は D3 の宣言ではない
    assert fa.declares({"explicit": [], "closed_world": True}, "D3")
    assert fa.declares({"explicit": [], "idempotent": True}, "D4")
    assert not fa.declares({"explicit": ["readOnlyHint"], "idempotent": True}, "D4")


# --- 端から端まで ---------------------------------------------------------------------------------------

def _write_csv(path, rows):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def _csample(path, n_trees=1, n_pairs=1, targets=None, m_d=None, scanned=4):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"kind": "contradiction",
                   "by_decl": {"D1": {"n_trees": n_trees, "n_pairs": n_pairs}, "D2": {"n_trees": 0, "n_pairs": 0},
                               "D3": {"n_trees": 0, "n_pairs": 0}, "D4": {"n_trees": 0, "n_pairs": 0}},
                   "denominators": {"n_trees_scanned": scanned, "M_d": m_d or {"D1": 3, "D2": 1, "D3": 1, "D4": 0}},
                   "targets": targets if targets is not None else [{"pair_id": "C-D1-001", "tree": "t1", "decl": "D1"}]},
                  fh)


def test_cli_end_to_end_and_sample_check(tmp_path):
    d = str(tmp_path / "run")
    _synthetic_run(d)
    sheet = str(tmp_path / "c.csv")
    _write_csv(sheet, [_crow(pair_id="C-D1-001", tree="t1")])
    sample = str(tmp_path / "s.json")
    _csample(sample)
    out = str(tmp_path / "o.json")
    md = str(tmp_path / "o.md")
    base = ["--run", d, "--contradiction-sample", sample, "--contradictions", sheet, "--seed", "7", "--reps", "50"]
    assert fa.main([*base, "--out-json", out, "--out-md", md]) == 0
    res = json.load(open(out, encoding="utf-8"))
    m = res["contradictions"]["D1"]["main"]
    assert (m["n"], m["k"], m["N"], m["M_d"], m["n_scanned"]) == (1, 1, 1, 3, 4)
    assert m["c"] == pytest.approx(1 / 3) and m["b"] == pytest.approx(0.25) and m["interval"] is None
    assert "tool_check_v4" not in res  # 合算の行は v4 の試験でだけ
    assert res["warnings"] == []
    # 抜き取りにある組の判定し残しは誤り（--allow-partial なら警告）
    _csample(sample, targets=[{"pair_id": "C-D1-001", "tree": "t1", "decl": "D1"},
                              {"pair_id": "C-D1-002", "tree": "t1", "decl": "D1"}])
    with pytest.raises(ValueError, match="判定し残し"):
        fa.main(base)
    assert fa.main([*base, "--allow-partial", "--out-json", out]) == 0
    assert json.load(open(out, encoding="utf-8"))["partial"] is True
    # N・組の数・走査した木の数の食い違いは誤り
    for kw, pat in (({"n_trees": 5}, "N = 1"), ({"n_pairs": 9}, "組の数"), ({"scanned": 3}, "走査した木の数")):
        _csample(sample, **kw)
        with pytest.raises(ValueError, match=pat):
            fa.main(base)
    # M_d の食い違いは警告にして両方を残す
    _csample(sample, m_d={"D1": 4, "D2": 1, "D3": 1, "D4": 0})
    assert fa.main([*base, "--out-json", out]) == 0
    res = json.load(open(out, encoding="utf-8"))
    assert res["run"]["M_d"]["D1"] == 3 and res["run"]["M_d_sample"]["D1"] == 4
    assert any("M_d が食い違う" in w for w in res["warnings"])
    # 種類の取り違え
    with open(sample, "w", encoding="utf-8") as fh:
        json.dump({"kind": "miss", "targets": []}, fh)
    with pytest.raises(ValueError, match="kind"):
        fa.main(base)


def test_without_run_uses_sample_denominators(tmp_path):
    sheet = str(tmp_path / "c.csv")
    _write_csv(sheet, [_crow(pair_id="C-D1-001", tree="t1")])
    sample = str(tmp_path / "s.json")
    _csample(sample, n_trees=2, n_pairs=2, m_d={"D1": 10, "D2": 1, "D3": 1, "D4": 0}, scanned=20)
    out = str(tmp_path / "o.json")
    assert fa.main(["--contradiction-sample", sample, "--contradictions", sheet, "--seed", "1", "--reps", "10",
                    "--out-json", out]) == 0
    m = json.load(open(out, encoding="utf-8"))["contradictions"]["D1"]["main"]
    assert (m["N"], m["M_d"], m["n_scanned"], m["K_hat"]) == (2, 10, 20, 2.0)


def test_sheet_columns_from_final_sheet_satisfy_aggregator():
    fs = pytest.importorskip("final_sheet")
    for kind, need in (("contradiction", fa.CONTRA_COLUMNS), ("miss", fa.MISS_COLUMNS), ("unknown", fa.UNKNOWN_COLUMNS)):
        missing = set(need) - set(fs.columns(kind))
        assert not missing, (kind, missing)


def test_agreement_requires_known_ids_and_vocabulary(tmp_path):
    primary = {"M1": "正", "M2": "誤"}
    r = fa.agreement(primary, [{"pair_id": "M1", "verdict": "正"}, {"pair_id": "M2", "verdict": "不明"}], "verdict",
                     fa.VERDICTS, "2 人目")
    assert r["agree"] == 1 and r["disagreeing_ids"] == ["M2"]
    with pytest.raises(fa.VocabularyError):
        fa.agreement(primary, [{"pair_id": "M9", "verdict": "正"}], "verdict", fa.VERDICTS, "2 人目")
    with pytest.raises(fa.VocabularyError):
        fa.agreement(primary, [{"pair_id": "M1", "verdict": "たぶん正"}], "verdict", fa.VERDICTS, "2 人目")


V4 = os.path.join(ROOT, "evidence", "population_v4", "v4_judgments.json")


@pytest.mark.skipif(not os.path.exists(V4), reason="v4 の判定が無い")
def test_v4_pair_level_reproduces_46_of_60():
    pairs, misses = fa.read_v4_judgments(V4)
    pl = fa.pair_level([p for p in pairs if p.decl in ("D1", "D2")])
    assert (pl["correct"], pl["correct"] + pl["wrong"]) == (46, 60)
    assert len(misses) == 30


def test_unknown_contents_rate_excludes_unknown_and_reports_variant():
    good = {"pair_id": "", "tree": "", "decl": "D1", "reasons": "net_post", "outcome": "", "reachable": "",
            "violates": "", "write_target": "", "condition_type": "", "unknown_reason": "", "minutes": "",
            "ai_used": "なし"}
    rows = []
    for i, o in enumerate(["違反"] * 3 + ["違反でない"] * 5 + ["不明"] * 2):
        r = {**good, "pair_id": f"U-D1-{i:03d}", "tree": f"t{i:02d}", "outcome": o}
        if o == "違反":
            r.update(reachable="はい", violates="はい", write_target="相手側の状態", condition_type="引数")
        elif o == "違反でない":
            r.update(reachable="はい", violates="いいえ")
        else:
            r.update(reachable="決められない", unknown_reason="相手の API: 文書が無い")
        rows.append(r)
    res = fa.aggregate_unknowns(fa.parse_unknown_rows(rows), None, seed=3, reps=200)["judged"]["D1"]
    assert res["violation_rate_trees"] == pytest.approx(3 / 8)  # 不明を除く
    assert res["violation_rate_trees_unknown_as_not"] == pytest.approx(3 / 10)
    assert res["n_trees_decided"] == 8 and res["violation_rate_trees_interval"] is not None
    assert res["by_reason"]["net_post"] == {"違反": 3, "違反でない": 5, "不明": 2}
    assert res["unknown_reasons"] == ["相手の API: 文書が無い"] * 2
    assert res["unknown_reason_classes"]["相手の API"] == 2
