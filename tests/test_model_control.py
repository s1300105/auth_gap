"""モデルの値が制御位置に届く矛の層（D90）の試験。

層の判定は `scripts/contradiction_by_decl.py: load_model_control` の 1 か所。ここでは小さな合成の manifest で
案 B（主 slot の主体 MODEL。GAP_INJECT は列で層の出入りに使わない）・S2（MODEL かつ resolved）・S1−S2（不明）・
行の軸と効果の軸・ゲートの状態・選択理由を確かめ、`scan_v2.py`・`final_sample.py`・`final_sheet.py`・
`final_aggregate.py` の層の欄を確かめる。最終評価・練習のデータは使わない。

最後の試験だけ、開発用の母集団 v2 の取り直し（`evidence/scan_v2_gi_run1`。木ごとの manifest は追跡しない）があれば、
宣言をまたいだ数を README・gi_counts.json と突き合わせる（無ければ飛ばす）。
"""

from __future__ import annotations

import csv
import glob
import json
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import contradiction_by_decl as cbd  # noqa: E402
import final_aggregate as fa  # noqa: E402
import final_sample as fs  # noqa: E402
import final_sheet as fsh  # noqa: E402
import scan_v2  # noqa: E402

from authgap.catalog import sinks  # noqa: E402

# ---------------------------------------------------------------- 合成の manifest


def slot(prin, prov="opaque"):
    return {"prin": prin, "prov": prov}


def effect(site, kind, relpath, lineno, slots, resolution="opaque"):
    return {"site": site, "kind": kind, "relpath": relpath, "lineno": lineno, "slots": slots, "resolution": resolution}


def rows_for(e, notes, inject=(), extra=None):
    """効果 e の slot ごとの行（manifest は 1 効果 1 slot に 1 行）。`inject` の slot に GAP_INJECT。"""
    out = []
    for s in e["slots"]:
        vs = ["CONTRADICTION"] if any(n.startswith("contradiction:") for n in notes) else ["UNKNOWN"]
        if s in inject:
            vs.append("GAP_INJECT")
        r = {"site": e["site"], "kind": e["kind"], "relpath": e["relpath"], "lineno": e["lineno"], "slot": s,
             "notes": list(notes), "verdicts": vs, "covered_by": None}
        r.update(extra or {})
        out.append(r)
    return out


def contra(decl, reason):
    return [f"contradiction:{decl}", f"contradiction_reason:{decl}:{reason}"]


def unit(qual, effects, rows, explicit=("readOnlyHint",), closed_world=False, req_val=None, grades=None):
    u = {"unit": {"qualname": qual, "tool_name": qual, "unit_id": f"mcp:{qual}:0", "relpath": "server.py",
                  "lineno": 10 + len(qual)},
         "D_kind": {"explicit": list(explicit), "closed_world": closed_world},
         "effects": effects, "rows": rows}
    if req_val is not None:
        u["req_val"] = req_val
    if grades is not None:
        u["grades"] = grades
    return u


def make_run(tmp_path, trees, name="run"):
    d = tmp_path / name
    d.mkdir()
    for t, units in trees.items():
        (d / f"{t}.json").write_text(json.dumps({"units": units}), encoding="utf-8")
    (d / "summary.json").write_text(json.dumps({"trees": [{"tree": t, "status": "ok"} for t in trees]}),
                                    encoding="utf-8")
    return str(d)


def all_model(effects):
    return {f"{i}:{s}": "MODEL" for i, e in enumerate(effects) for s in e["slots"]}


def synthetic(tmp_path):
    # t1: D1。path が MODEL・resolved（S2）。理由は fs_write（選択理由でない）
    e1 = [effect("os.remove", "FS_WRITE", "a.py", 5, {"path": slot("MODEL", "resolved")})]
    u1 = unit("rm", e1, rows_for(e1[0], contra("D1", "fs_write")), req_val=all_model(e1))
    # t1: D1。sql が MODEL・opaque（S1−S2）。GAP_INJECT は無い（案 B では層に入る）
    e2 = [effect("db.execute", "DB", "b.py", 7, {"sql": slot("MODEL"), "params": slot("MODEL")})]
    u2 = unit("upd", e2, rows_for(e2[0], contra("D1", "db_modify"), inject=("params",)), req_val=all_model(e2))
    # t2: D2。主 slot は OP、params にだけ GAP_INJECT（G1_nonprimary）
    e3 = [effect("db.execute", "DB", "c.py", 9, {"sql": slot("OP", "resolved"), "params": slot("MODEL")})]
    u3 = unit("put", e3, rows_for(e3[0], contra("D2", "db_modify"), inject=("params",)),
              explicit=("destructiveHint",), req_val=all_model(e3))
    # t2: D2。同じ行に効果が 2 つ（MODEL・resolved と OP）。保守的なら外、寛容なら S2
    e4 = [effect("open", "FS_WRITE", "d.py", 3, {"path": slot("MODEL", "resolved")}),
          effect("open", "FS_WRITE", "d.py", 3, {"path": slot("OP", "resolved")})]
    u4 = unit("w2", e4, rows_for(e4[0], contra("D2", "fs_writeout_model_path")) + rows_for(e4[1], contra("D2", "fs_write")),
              explicit=("destructiveHint",), req_val=all_model(e4))
    # t3: D3。url.host が MODEL・resolved（S2、選択理由 net_model_host）。ゲートは承認（req_val = USER）
    e5 = [effect("httpx.get", "NET", "e.py", 4, {"url.host": slot("MODEL", "resolved")})]
    u5 = unit("fetch", e5, rows_for(e5[0], contra("D3", "net_model_host"), inject=()),
              explicit=(), closed_world=True, req_val={"0:url.host": "USER"})
    # t3: D1。組に 2 行。片方だけ MODEL（行の軸 any なら S1、all なら外）。片方は weak のゲート
    e6 = [effect("os.unlink", "FS_WRITE", "f.py", 1, {"path": slot("MODEL")}),
          effect("os.unlink", "FS_WRITE", "f.py", 50, {"path": slot("OP", "resolved")})]
    u6 = unit("del2", e6, rows_for(e6[0], contra("D1", "fs_write"), inject=("path",))
              + rows_for(e6[1], contra("D1", "fs_write")),
              req_val={"0:path": "OP", "1:path": "MODEL"}, grades={"0:path": {"grade": "weak"}})
    # t4: D4 の矛（層には出さない）と、D1 の不で主 slot が MODEL（併記の側）
    e7 = [effect("requests.post", "NET", "g.py", 2, {"url.host": slot("MODEL")})]
    u7 = unit("post", e7, rows_for(e7[0], ["contradiction:D4", "contradiction_reason:D4:net_nonidempotent_method",
                                           "contradiction_unknown:D1:net_post"]),
              explicit=("readOnlyHint",), req_val=all_model(e7))
    return make_run(tmp_path, {"t1": [u1, u2], "t2": [u3, u4], "t3": [u5, u6], "t4": [u7]})


def by_qual(mc):
    return {(k[3], k[6]): v for k, v in mc.items()}


# ---------------------------------------------------------------- 層の判定（1 か所）


def test_primary_slots_are_imported_not_copied():
    assert cbd.PRIMARY_SLOTS is sinks.PRIMARY_SLOTS


def test_choice_reasons_are_the_seven_named_reasons():
    assert cbd.CHOICE_REASONS == {"spawn_model", "fs_writeout_model_path", "fs_unknown_model_path",
                                  "net_put_model_url", "exec_model", "net_model_host", "db_model_sql"}
    # 3-b の部分文字列の集合との差は net_method_model だけ（名前で固定する理由）
    reasons = {"spawn_model", "spawn_model_opaque", "net_method_model", "exec_model", "net_model_host",
               "db_model_sql", "fs_writeout_model_path", "fs_unknown_model_path", "net_put_model_url"}
    three_b = {r for r in reasons if "model" in r and not r.endswith("_opaque")}
    assert three_b - cbd.CHOICE_REASONS == {"net_method_model"}


def test_layer_statuses_case_B(tmp_path):
    mc = by_qual(cbd.load_model_control(synthetic(tmp_path)))
    assert mc[("rm", "D1")]["status"] == "S2"
    assert mc[("rm", "D1")]["choice_reason"] is False
    # 案 B: GAP_INJECT が無くても主 slot が MODEL なら層に入る（GAP_INJECT は列）
    assert mc[("upd", "D1")]["status"] == "S1_opaque"
    assert mc[("upd", "D1")]["gap_inject_primary"] is False and mc[("upd", "D1")]["gap_inject_any"] is True
    assert mc[("put", "D2")]["status"] == "G1_nonprimary"
    assert mc[("fetch", "D3")]["status"] == "S2" and mc[("fetch", "D3")]["choice_reason"] is True
    # D4 は層に出さない。不の組は既定では返さない
    assert not any(d == "D4" for _, d in mc)
    assert ("post", "D1") not in mc


def test_effect_axis_conservative_is_primary(tmp_path):
    v = by_qual(cbd.load_model_control(synthetic(tmp_path)))[("w2", "D2")]
    assert v["status"] == "none"  # 保守的: 同じ行の効果の全部が満たすときだけ
    assert v["axes"]["row_any/effect_any"] == "S2"
    assert v["axes"]["row_any/effect_all"] == "none"
    loc = v["locations"][0]
    assert loc["n_effects"] == 2 and loc["model_choice"] == "none" and loc["model_choice_by_effect"] == ["chosen", "none"]


def test_row_axis_any_is_primary(tmp_path):
    v = by_qual(cbd.load_model_control(synthetic(tmp_path)))[("del2", "D1")]
    assert v["status"] == "S1_opaque" and v["rows_S1"] == ["f.py:1"]
    assert v["axes"]["row_all/effect_all"] == "G1_nonprimary"  # 全部の行では満たさない。GAP_INJECT はある
    assert v["gate_states"] == ["weak"]


def test_gate_states_from_manifest(tmp_path):
    mc = by_qual(cbd.load_model_control(synthetic(tmp_path)))
    assert mc[("fetch", "D3")]["gate_states"] == ["承認"]
    assert mc[("rm", "D1")]["gate_states"] == ["なし"]
    u = {"req_val": {"0:path": "OP"}, "grades": {}}
    assert cbd.gate_state(u, 0, "path", []) == "strong・allowlist"
    assert cbd.gate_state({}, 0, "path", []) == "不明"  # 記録が無ければ「なし」に倒さない
    assert cbd.gate_state({"req_val": {"0:path": "MODEL"}}, 0, "path",
                          [{"covered_by": "op", "verdicts": ["INVENTORY"]}]) == "D_op"
    assert cbd.gate_state({"req_val": {"0:path": "MODEL"}}, 0, "path",
                          [{"covered_by": "op", "verdicts": ["INVENTORY"],
                            "rubric_1c": "inventory(no_validator+exposure)"}]) == "rubric 1c"


def test_counts_and_fixed_wording(tmp_path):
    mc = cbd.load_model_control(synthetic(tmp_path))
    c1 = cbd.model_control_counts(mc, "D1")
    assert (c1["S1"]["pairs"], c1["S2"]["pairs"], c1["S1_minus_S2"]["pairs"]) == (3, 1, 2)
    assert (c1["S1"]["trees"], c1["S1"]["locations"]) == (2, 3)
    assert c1["S2_other_reason"]["pairs"] == 1 and c1["S2_choice_reason"]["pairs"] == 0
    assert c1["S1_gap_inject_primary"]["pairs"] == 1  # S1 ∩ 案 A（del2 だけ）
    assert c1["outside_S1_gap_inject_primary"]["pairs"] == 0
    # D90 の 10 で固定した字面のまま（木の数は文に足さない）
    assert cbd.fixed_wording(c1) == "解析器で選べると言えたものが 1 件、不明が 2 件"
    c2 = cbd.model_control_counts(mc, "D2", ("any", "any"))
    assert c2["S2"]["pairs"] == 1 and c2["S2_choice_reason"]["pairs"] == 1


def test_unknown_pairs_reported_separately(tmp_path):
    mc = cbd.load_model_control(synthetic(tmp_path), include_unknown=True)
    assert by_qual(mc)[("post", "D1")]["contradiction"] == "不"
    assert cbd.unknown_model_reasons(mc, "D1") == {"pairs": 1, "by_reason": {"net_post": 1}}
    # 不の組は矛の全数に入らない
    assert cbd.model_control_counts(mc, "D1")["S1"]["pairs"] == 3


def test_markdown_has_per_declaration_tables(tmp_path):
    md = cbd.to_md(synthetic(tmp_path))
    assert "モデルの値が制御位置に届く矛の層" in md
    assert "| D1 | S1 流れ込む | 3 | 3 | 2 |" in md
    assert md.index("| D1 | S1 流れ込む") < md.index("| D2 | S1 流れ込む") < md.index("| D3 | S1 流れ込む")
    assert "| D4 | S1" not in md


# ---------------------------------------------------------------- scan_v2: contradictions.json の列


def test_scan_v2_locations_keep_old_keys_first(tmp_path):
    run = synthetic(tmp_path)
    m = json.load(open(os.path.join(run, "t3.json"), encoding="utf-8"))
    rows = scan_v2._contradiction_rows("t3", m)
    del2 = next(r for r in rows if r["unit"] == "del2")
    loc = del2["locations"][0]
    assert list(loc)[:4] == ["relpath", "lineno", "declarations", "destructive"]
    assert list(loc)[4:] == list(scan_v2.LOCATION_LAYER_FIELDS)
    assert loc["inject_slots"] == ["path"] and loc["inject_primary_slots"] == ["path"]
    assert loc["model_choice"] == "influenced" and loc["effect_resolution"] == "opaque"
    assert del2["locations"][1]["model_choice"] == "none"


# ---------------------------------------------------------------- final_sample / final_sheet


def test_final_sample_layer_totals_and_targets(tmp_path):
    out = fs.sample_contradiction(synthetic(tmp_path), 3)
    d1 = out["by_decl"]["D1"]
    assert (d1["n_pairs_S1"], d1["n_pairs_S2"], d1["n_trees_S1"], d1["n_trees_S2"]) == (3, 1, 2, 1)
    assert out["by_decl"]["D4"]["n_pairs_S1"] is None
    t = next(x for x in out["targets"] if x["unit"] == "del2")
    assert t["model_control"]["status"] == "S1_opaque" and t["model_control_rows"] == {"S1": ["f.py:1"], "S2": []}
    assert all("model_control" not in x for x in out["targets"] if x["decl"] == "D4")


def test_sheet_does_not_carry_layer_fields(tmp_path):
    out = fs.sample_contradiction(synthetic(tmp_path), 3)
    cols = fsh.columns("contradiction")
    assert not (cbd.MODEL_CONTROL_FIELDS & set(cols))
    rows = fsh.sheet_rows("contradiction", out["targets"], 5)
    fsh.check_no_layer_leak(cols, rows, "contradiction.csv")
    text = "\n".join(",".join(r) for r in rows)
    for st in ("S1_opaque", "G1_nonprimary", "model_control"):
        assert st not in text
    # 欄を足してしまったら止まる
    with pytest.raises(AssertionError, match="D90"):
        fsh.check_no_layer_leak([*cols, "model_control"], [[*r, "S2"] for r in rows], "x")
    with pytest.raises(AssertionError, match="D90"):
        fsh.check_no_layer_leak(cols, [[*r[:-1], "S1_opaque"] for r in rows], "x")


def test_sheet_columns_function_rejects_layer_column(monkeypatch):
    monkeypatch.setitem(fsh.TARGET_COLS, "contradiction", [*fsh.TARGET_COLS["contradiction"], "model_control"])
    with pytest.raises(AssertionError, match="D90"):
        fsh.columns("contradiction")


# ---------------------------------------------------------------- final_aggregate


def _pair(i, tree, decl, verdict, tba=None, wt=None):
    return fa.Pair(id=i, tree=tree, decl=decl, verdict=verdict, target_by_arg=tba, write_target=wt)


def test_strata_small_n_gives_table_only_and_correspondence(tmp_path):
    run = synthetic(tmp_path)
    smp = fs.sample_contradiction(run, 3)
    ids = {(t["unit"], t["decl"]): t["pair_id"] for t in smp["targets"]}
    pairs = [_pair(ids[("rm", "D1")], "t1", "D1", "正", "はい", "利用者のファイル"),
             _pair(ids[("upd", "D1")], "t1", "D1", "誤"),
             _pair(ids[("del2", "D1")], "t3", "D1", "正", "いいえ", "一時ファイル"),
             _pair(ids[("fetch", "D3")], "t3", "D3", "正", wt="モデルが決める宛先"),
             _pair(ids[("put", "D2")], "t2", "D2", "誤")]
    w: list = []
    st = fa.model_control_strata(pairs, smp, cbd.load_model_control(run), {"D1": 2, "D2": 1, "D3": 1},
                                 {"D1": 4, "D2": 2, "D3": 1}, seed=7, reps=50, warnings=w)
    d1 = st["D1"]
    assert d1["totals"]["S1"] == {"pairs": 3, "locations": 3, "trees": 2}
    assert d1["tree_ratios"]["S1"] == {"trees": 2, "per_N": 1.0, "per_M_d": 0.5}
    j = d1["judged"]["S1"]
    assert (j["n_S"], j["k_S"], j["pairs"], j["interval"]) == (2, 2, 3, None)
    assert "D73" in j["interval_note"]
    assert d1["judged"]["S2"]["n_S"] == 1
    corr = d1["d84_step3_correspondence"]["all_correct"]
    assert corr["はい"]["S2"] == 1 and corr["いいえ"]["S1_opaque"] == 1
    assert st["D3"]["d3_destination_correspondence"]["table"]["モデルが決める宛先"]["S2"] == 1
    assert d1["fixed_wording"] == "解析器で選べると言えたものが 1 件、不明が 2 件"
    assert d1["judged"]["S1"]["prereg"] is True and d1["judged"]["S2"]["prereg"] is False
    assert w == []
    md = "\n".join(fa.model_control_md(st))
    assert "D84 の ③ × 層" in md and "k_S / n_S" in md
    # n_S < 10 の木ごとの表は全部の群に出す（層の外も同じ打ち切り）
    assert "D2 outside の木ごと" in md and "D1 S1_minus_S2 の木ごと" in md
    assert "② 重い書き込み先の正（事前登録の外の参考）" in md and "S2（参考）" in md


def test_strata_bootstrap_when_n_at_least_10():
    pairs, targets = [], []
    for i in range(12):
        pid = f"C-D1-{i:03d}"
        pairs.append(_pair(pid, f"t{i:02d}", "D1", "正" if i % 3 else "誤", "はい", "利用者のファイル"))
        targets.append({"pair_id": pid, "tree": f"t{i:02d}", "decl": "D1",
                        "model_control": {"status": "S1_opaque" if i % 2 else "S2"}})
    smp = {"kind": "contradiction", "by_decl": {}, "targets": targets}
    a = fa.model_control_strata(pairs, smp, None, {"D1": 12}, {"D1": 20}, seed=11, reps=200, warnings=[])
    b = fa.model_control_strata(pairs, smp, None, {"D1": 12}, {"D1": 20}, seed=11, reps=200, warnings=[])
    j = a["D1"]["judged"]["S1"]
    assert j["n_S"] == 12 and j["interval"] is not None and a == b
    # 同じ seed・同じ関数（tree_metrics）の区間
    tm = fa.tree_metrics(fa.tree_counts(pairs), None, None, None, 11, 200)
    assert j["interval"] == tm["interval"]["a"]
    assert a["D1"]["judged"]["S2"]["interval"] is None  # 6 木 < 10


def test_strata_missing_layer_record_in_new_format_sample_warns():
    smp = {"kind": "contradiction", "by_decl": {"D1": {"n_pairs_S1": 1, "n_trees_S1": 1, "n_pairs_S2": 0,
                                                       "n_trees_S2": 0}},
           "targets": [{"pair_id": "C-D1-001", "tree": "t", "decl": "D1"}]}
    w: list = []
    st = fa.model_control_strata([_pair("C-D1-001", "t", "D1", "正")], smp, None, {"D1": 1}, {"D1": 1}, 1, 10, w)
    assert any("model_control" in x for x in w)
    assert st["D1"]["totals"]["S1"]["pairs"] == 1 and "judged" not in st["D1"]


def test_strata_sample_and_run_must_agree(tmp_path):
    run = synthetic(tmp_path)
    smp = fs.sample_contradiction(run, 3)
    smp["by_decl"]["D1"]["n_pairs_S1"] = 99
    with pytest.raises(ValueError, match="D90"):
        fa.model_control_strata([], smp, cbd.load_model_control(run), {}, {}, 1, 10, [])


def test_aggregate_cli_writes_strata(tmp_path):
    run = synthetic(tmp_path)
    smp = fs.sample_contradiction(run, 3)
    sp = tmp_path / "s.json"
    sp.write_text(json.dumps(smp, ensure_ascii=False), encoding="utf-8")
    rows = []
    for t in smp["targets"]:
        v = "正" if t["decl"] != "D4" else "誤"
        rows.append({"pair_id": t["pair_id"], "tree": t["tree"], "decl": t["decl"], "verdict": v,
                     "condition_type": "なし" if v == "正" else "", "error_class": "" if v == "正" else "E5: x",
                     "write_target": ("モデルが決める宛先" if t["decl"] == "D3" else "利用者のファイル") if v == "正" else "",
                     "target_by_arg": "はい" if (t["decl"] == "D1" and v == "正") else "",
                     "unknown_reason": "", "minutes": "", "ai_used": "なし"})
    cp = tmp_path / "c.csv"
    with open(cp, "w", encoding="utf-8", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rows[0]))
        wr.writeheader()
        wr.writerows(rows)
    out = tmp_path / "o.json"
    assert fa.main(["--run", run, "--contradiction-sample", str(sp), "--contradictions", str(cp), "--seed", "4",
                    "--reps", "20", "--out-json", str(out)]) == 0
    res = json.load(open(out, encoding="utf-8"))
    st = res["model_control_strata"]
    assert set(st) >= {"D1", "D2", "D3"} and "D4" not in st
    assert st["D1"]["judged"]["S1"]["k_S"] == 2


# ---------------------------------------------------------------- 開発用 v2（あれば）

V2 = os.path.join(ROOT, "evidence", "scan_v2_gi_run1")


@pytest.mark.skipif(not glob.glob(os.path.join(V2, "v2-*.json")), reason="v2 の木ごとの manifest が無い（追跡しない）")
def test_v2_cross_declaration_counts_against_readme():
    """案 B の宣言をまたいだ数を README・gi_counts.json の G0・G2・G3 と突き合わせる（探索の数の再現。決定ではない）。"""
    gi = json.load(open(os.path.join(V2, "gi_counts.json"), encoding="utf-8"))
    reasons = cbd.load_reasons(V2)
    g0 = {k for k, per in reasons.items() if any(cbd.apply_flip(per.get(d, set()), d, None) == "矛" for d in cbd.DECLS)}
    assert len(g0) == gi["G0"]["unit_site_kind"] == 193
    mc = cbd.load_model_control(V2)
    s1 = {k[:6] for k, v in mc.items() if v["status"] in ("S2", "S1_opaque")}
    s2 = {k[:6] for k, v in mc.items() if v["status"] == "S2"}
    a = {k[:6] for k, v in mc.items() if v["status"] in ("S2", "S1_opaque") and v["gap_inject_primary"]}
    locs1 = {(k[0], *r.rsplit(":", 1), k[4]) for k, v in mc.items() for r in v["rows_S1"]}
    # 案 B の S1 = 8 組（ユニット × (site, kind)）・4 位置・4 木。案 A（主 slot に GAP_INJECT）も同じ 8（draft §0）
    assert len(s1) == gi["G2"]["unit_site_kind"] == 8
    assert a == s1
    assert len(locs1) == 4 and len({k[0] for k in s1}) == gi["G2"]["trees"] == 4
    assert len(s2) == gi["G3"]["unit_site_kind"] == 1


# ---------------------------------------------------------------- レビュー反映（D90）


def test_unknown_reasons_only_from_rows_that_satisfy_S1(tmp_path):
    """不の組の理由は、主の軸で S1 を満たす行の理由だけ（主体が MODEL でない行の理由を混ぜない）。"""
    ea = effect("requests.post", "NET", "g.py", 10, {"url.host": slot("MODEL")})
    eb = effect("requests.post", "NET", "g.py", 20, {"url.host": slot("OP", "resolved")})
    rows = rows_for(ea, ["contradiction_unknown:D1:net_post"]) + rows_for(eb, ["contradiction_unknown:D1:net_host_unknown"])
    run = make_run(tmp_path, {"t": [unit("mix", [ea, eb], rows, req_val=all_model([ea, eb]))]})
    mc = cbd.load_model_control(run, include_unknown=True)
    assert cbd.unknown_model_reasons(mc, "D1") == {"pairs": 1, "by_reason": {"net_post": 1}}


def test_primary_inject_outside_S1_is_counted_separately(tmp_path):
    """案 A は S1 の部分集合ではない: 同じ行の別の効果の主 slot が MODEL でないと、保守的な効果の軸で S1 から外れる。"""
    e = [effect("open", "FS_WRITE", "h.py", 3, {"path": slot("MODEL")}),
         effect("open", "FS_WRITE", "h.py", 3, {"path": slot("OP", "resolved")})]
    rows = rows_for(e[0], contra("D2", "fs_write"), inject=("path",)) + rows_for(e[1], contra("D2", "fs_write"))
    run = make_run(tmp_path, {"t": [unit("w", e, rows, explicit=("destructiveHint",), req_val=all_model(e))]})
    mc = cbd.load_model_control(run)
    c = cbd.model_control_counts(mc, "D2")
    assert c["S1"]["pairs"] == 0 and c["G1_nonprimary"]["pairs"] == 1
    assert c["S1_gap_inject_primary"]["pairs"] == 0 and c["outside_S1_gap_inject_primary"]["pairs"] == 1
    ca = cbd.model_control_counts(mc, "D2", ("any", "any"))
    assert ca["S1_gap_inject_primary"]["pairs"] == 1 and ca["outside_S1_gap_inject_primary"]["pairs"] == 0
    md = cbd.to_md(run)
    assert "案 A の数" not in md and "S1 の外で主 slot に GAP_INJECT" in md


def test_groups_are_defined_once_and_unknown_status_raises():
    assert fa.MC_PREREG_GROUPS == ("S1", "outside")
    assert set(cbd.MC_GROUPS["S1"]) == set(cbd.MC_GROUPS["S2"]) | set(cbd.MC_GROUPS["S1_minus_S2"])
    assert set(cbd.MC_STATUSES) == set(cbd.MC_GROUPS["S1"]) | set(cbd.MC_GROUPS["outside"])
    assert [cbd.mc_col(x) for x in (*cbd.MC_STATUSES, None)] == ["S2", "S1_opaque", "outside", "outside", "（層の記録なし）"]
    with pytest.raises(ValueError, match="D90"):
        cbd.mc_col("S3")
    smp = {"targets": [{"pair_id": "C-D1-001", "model_control": {"status": "S3"}}]}
    with pytest.raises(ValueError, match="D90"):
        fa.layer_status_by_pair_id(smp)


def test_aggregate_checks_each_pair_against_the_scan(tmp_path):
    """層の値は抜き取りの targets から pair_id で読み、--run があれば組ごとに走査の値と照合する。"""
    run = synthetic(tmp_path)
    smp = fs.sample_contradiction(run, 3)
    mc = cbd.load_model_control(run)
    assert set(fa.layer_status_by_pair_id(smp, mc).values()) >= {"S2", "S1_opaque"}
    t = next(x for x in smp["targets"] if x["unit"] == "rm")
    t["model_control"]["status"] = "none"
    with pytest.raises(ValueError, match="走査から数え直した値"):
        fa.layer_status_by_pair_id(smp, mc)


def test_sheet_leak_check_ignores_source_names():
    """ソース由来の欄（ツール名・ファイル名）に model_control の語があっても止まらない。層の値の完全一致で止まる。"""
    cols = fsh.columns("contradiction")
    row = ["" for _ in cols]
    row[cols.index("unit")] = "set_model_control"
    row[cols.index("locations")] = "model_control.py:3 none.py:4"
    row[cols.index("site")] = "S2"
    row[cols.index("reasons")] = "fs_write"
    fsh.check_no_layer_leak(cols, [row], "x")
    row[cols.index("reasons")] = "fs_write S1_opaque"
    with pytest.raises(AssertionError, match="D90"):
        fsh.check_no_layer_leak(cols, [row], "x")
    row[cols.index("reasons")] = "{'model_control': 1}"
    with pytest.raises(AssertionError, match="D90"):
        fsh.check_no_layer_leak(cols, [row], "x")


@pytest.mark.skipif(not glob.glob(os.path.join(V2, "v2-*.json")), reason="v2 の木ごとの manifest が無い（追跡しない）")
def test_v2_per_declaration_counts():
    """宣言ごとの層の数（D90 の後に実装者とレビューが見た値。定義の根拠ではない。D90 の開示）。4 つの軸で同じ。"""
    mc = cbd.load_model_control(V2)
    for a in cbd.AXES:
        c = {d: cbd.model_control_counts(mc, d, a) for d in cbd.LAYER_DECLS}
        trip = {d: {g: tuple(c[d][g][k] for k in ("pairs", "locations", "trees")) for g in ("S1", "S2")}
                for d in c}
        assert trip == {"D1": {"S1": (7, 3, 3), "S2": (0, 0, 0)}, "D2": {"S1": (0, 0, 0), "S2": (0, 0, 0)},
                        "D3": {"S1": (1, 1, 1), "S2": (1, 1, 1)}}
