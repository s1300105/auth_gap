"""最終評価の抜き取りと判定表の道具（`scripts/final_sample.py`・`final_sheet.py`・`show_target.py`、手順書 6.3〜6.5）。

小さな合成の run（summary.json・contradictions.json・木ごとの manifest）で、決定論・上限・見落としの対象・不の抜き取り・
判定の一致の 10%（切り上げ）・判定表の欄（見落としの表に解析器の出力が無いこと）を確かめる。
"""

from __future__ import annotations

import csv
import io
import json
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import final_sample as fs  # noqa: E402
import final_sheet as fsh  # noqa: E402
import show_target as st  # noqa: E402

# ---------------------------------------------------------------- 合成の run


def row(site, kind, relpath, lineno, notes, slot="path"):
    return {"site": site, "kind": kind, "relpath": relpath, "lineno": lineno, "slot": slot, "notes": list(notes)}


def unit(qual, relpath, lineno, explicit=(), closed_world=False, idempotent=False, rows=(), notes=(), n_effects=0):
    dk = {"explicit": list(explicit)}
    if closed_world:
        dk["closed_world"] = True
    if idempotent:
        dk["idempotent"] = True
    return {"unit": {"qualname": qual, "tool_name": qual, "relpath": relpath, "lineno": lineno, "annotations": {}},
            "D_kind": dk, "rows": list(rows), "notes": list(notes), "cap_hits": [], "opaque_reasons": [],
            "effects": [{"site": "x.y", "kind": "FS_WRITE", "relpath": relpath, "lineno": lineno + 1 + i,
                         "witness_chain": [], "slots": {}} for i in range(n_effects)]}


def contra_rows(decl, n, reason="fs_write", relpath="lib.py"):
    """宣言 `decl` の矛の行を n 組（site を変えて別の組にする）。"""
    return [row(f"site{i}", "FS_WRITE", relpath, 100 + i, [f"contradiction:{decl}", f"contradiction_reason:{decl}:{reason}"])
            for i in range(n)]


def unknown_rows(decl, n, reason="net_post"):
    return [row(f"usite{i}", "NET", "lib.py", 200 + i, [f"contradiction_unknown:{decl}:{reason}"]) for i in range(n)]


def make_run(tmp_path, trees: dict[str, list[dict]], name="run") -> str:
    d = tmp_path / name
    d.mkdir()
    for t, units in trees.items():
        (d / f"{t}.json").write_text(json.dumps({"units": units}), encoding="utf-8")
    (d / "summary.json").write_text(json.dumps({
        "analyzer_commit": "abc", "implementation_sha256_combined": "fff", "max_depth": 4,
        "trees": [{"tree": t, "status": "ok"} for t in trees]}), encoding="utf-8")
    rows = []
    for t, units in trees.items():
        for u in units:
            seen = {}
            for r in u["rows"]:
                ds = sorted({n.split(":")[1] for n in r["notes"] if n.startswith("contradiction:")})
                if ds:
                    seen.setdefault((r["site"], r["kind"]), set()).update(ds)
            for (site, kind), ds in seen.items():
                rows.append({"tree": t, "unit": u["unit"]["qualname"], "site": site, "effect_kind": kind,
                             "declarations": sorted(ds)})
    (d / "contradictions.json").write_text(json.dumps({"n": len(rows), "rows": rows}), encoding="utf-8")
    return str(d)


def many_trees(n_trees, decl="D1", explicit=("readOnlyHint",)):
    """木 i に (i % 6) + 1 組の矛。"""
    return {f"t{i:03d}": [unit("tool", "server.py", 10, explicit=explicit, rows=contra_rows(decl, (i % 6) + 1))]
            for i in range(n_trees)}


# ---------------------------------------------------------------- 矛


def test_contradiction_deterministic_and_seed_sensitive(tmp_path):
    run = make_run(tmp_path, many_trees(30))
    a = fs.sample_contradiction(run, 11, max_trees=10)
    b = fs.sample_contradiction(run, 11, max_trees=10)
    c = fs.sample_contradiction(run, 12, max_trees=10)
    assert a == b
    assert a["targets"] != c["targets"]
    # 件数は seed に依らない
    assert a["by_decl"]["D1"]["n_pairs"] == c["by_decl"]["D1"]["n_pairs"]


def test_contradiction_caps_default_200_trees_and_3_per_tree(tmp_path):
    run = make_run(tmp_path, many_trees(205))
    out = fs.sample_contradiction(run, 1)
    d1 = out["by_decl"]["D1"]
    assert d1["n_trees"] == 205 and d1["trees_sampled"] is True
    assert d1["n_trees_selected"] == 200
    assert d1["n_pairs"] == sum((i % 6) + 1 for i in range(205))
    per_tree = {}
    for t in out["targets"]:
        per_tree[t["tree"]] = per_tree.get(t["tree"], 0) + 1
    assert len(per_tree) == 200 and max(per_tree.values()) <= 3
    # 3 組以下の木は全組、それより多い木はちょうど 3 組
    for tr in d1["trees"]:
        if tr["selected"]:
            assert tr["n_selected"] == min(3, tr["n_pairs"]) == per_tree[tr["tree"]]
        else:
            assert tr["n_selected"] == 0 and tr["tree"] not in per_tree
    # 選ばなかった木も件数に残る
    assert len(d1["trees"]) == 205 and sum(1 for tr in d1["trees"] if not tr["selected"]) == 5
    assert out["consistency"]["match"] is True


def test_contradiction_all_when_under_caps_and_per_decl(tmp_path):
    trees = {
        "a": [unit("t1", "s.py", 1, explicit=("readOnlyHint",), closed_world=True,
                   rows=contra_rows("D1", 2) + [row("net", "NET", "s.py", 9, ["contradiction:D3", "contradiction_reason:D3:net_external"])])],
        "b": [unit("t2", "s.py", 1, explicit=("destructiveHint",), idempotent=True,
                   rows=contra_rows("D2", 5) + [row("app", "FS_WRITE", "s.py", 7, ["contradiction:D4", "contradiction_reason:D4:fs_append"])])],
    }
    out = fs.sample_contradiction(make_run(tmp_path, trees), 3)
    bd = out["by_decl"]
    assert (bd["D1"]["n_pairs"], bd["D1"]["n_pairs_selected"]) == (2, 2)
    assert (bd["D2"]["n_pairs"], bd["D2"]["n_pairs_selected"]) == (5, 3)
    assert (bd["D3"]["n_pairs"], bd["D4"]["n_pairs"]) == (1, 1)
    assert bd["D3"]["trees_sampled"] is False
    ids = [t["pair_id"] for t in out["targets"]]
    assert ids == sorted(ids) and len(set(ids)) == len(ids)
    assert {t["decl"] for t in out["targets"]} == {"D1", "D2", "D3", "D4"}
    assert out["denominators"]["M_d"] == {"D1": 1, "D2": 1, "D3": 1, "D4": 1}
    assert out["denominators"]["n_trees_scanned"] == 2


def test_contradiction_locations_only_rows_with_that_decl(tmp_path):
    rows = [row("db.exec", "DB", "db.py", 273, []),  # 同じ (site, kind) だが矛の注記なし（SELECT）
            row("db.exec", "DB", "db.py", 332, ["contradiction:D2", "contradiction_reason:D2:db_modify"])]
    run = make_run(tmp_path, {"a": [unit("edit", "s.py", 5, explicit=("destructiveHint",), rows=rows)]})
    (t,) = fs.sample_contradiction(run, 1)["targets"]
    assert t["locations"] == ["db.py:332"] and t["reasons"] == ["db_modify"]


def test_pair_with_both_contradiction_and_unknown_is_contradiction(tmp_path):
    rows = [row("s", "NET", "x.py", 1, ["contradiction:D1", "contradiction_reason:D1:net_put"]),
            row("s", "NET", "x.py", 2, ["contradiction_unknown:D1:net_post"])]
    run = make_run(tmp_path, {"a": [unit("t", "s.py", 1, explicit=("readOnlyHint",), rows=rows)]})
    c = fs.sample_contradiction(run, 1)
    u = fs.sample_unknown(run, 1)
    assert c["by_decl"]["D1"]["n_pairs"] == 1 and c["targets"][0]["locations"] == ["x.py:1"]
    assert u["by_decl"]["D1"]["n_pairs"] == 0 and u["targets"] == []
    assert u["by_decl"]["D1"]["reason_pairs_incl_contradiction_pairs"] == {"net_post": 1}


def test_missing_manifest_stops(tmp_path):
    run = make_run(tmp_path, many_trees(3))
    os.remove(os.path.join(run, "t001.json"))
    with pytest.raises(SystemExit):
        fs.sample_contradiction(run, 1)
    out = fs.sample_contradiction(run, 1, allow_missing=True)
    assert out["by_decl"]["D1"]["n_trees"] == 2 and out["warnings"]
    assert out["consistency"]["match"] is False


# ---------------------------------------------------------------- 見落とし


def miss_trees():
    return {
        "a": [
            unit("ok_d1", "s.py", 10, explicit=("readOnlyHint",), n_effects=2),                      # 対象
            unit("bad_d1", "s.py", 20, explicit=("readOnlyHint",), rows=contra_rows("D1", 1)),         # D1 の矛あり
            unit("unk_d2", "s.py", 30, explicit=("destructiveHint",), rows=unknown_rows("D2", 1)),    # 不だけ → 対象
            unit("ow", "s.py", 40, explicit=("openWorldHint",)),                                      # D1/D2 でない
            unit("cw", "s.py", 50, closed_world=True, idempotent=True),                               # D3/D4 だけ
        ],
        "b": [
            unit("trunc", "s.py", 10, explicit=("readOnlyHint",), notes=["TRUNCATED(depth)"]),       # 打ち切り → 対象
            # 同じ qualname でも別のファイルのユニットの矛は、こちらを対象から外さない（D64 / U50）
            unit("same", "a.py", 5, explicit=("readOnlyHint",)),
            unit("same", "b.py", 5, explicit=("readOnlyHint",), rows=contra_rows("D1", 1)),
        ],
        "c": [unit("d3only", "s.py", 1, closed_world=True, rows=[
            row("n", "NET", "s.py", 2, ["contradiction:D3", "contradiction_reason:D3:net_external"])])],
    }


def test_miss_eligibility(tmp_path):
    out = fs.sample_miss(make_run(tmp_path, miss_trees()), 7)
    assert out["pool"]["n_units"] == 4 and out["pool"]["n_trees"] == 2
    assert out["pool"]["n_units_by_decl"] == {"D1": 3, "D2": 1}
    assert out["pool"]["n_units_truncated"] == 1
    assert len(out["targets"]) == 2 and {t["tree"] for t in out["targets"]} == {"a", "b"}
    names = {(t["tree"], t["unit"], t["unit_relpath"]) for t in out["targets"]}
    assert names <= {("a", "ok_d1", "s.py"), ("a", "unk_d2", "s.py"), ("b", "trunc", "s.py"), ("b", "same", "a.py")}


def test_miss_truncated_unit_is_kept_with_mark(tmp_path):
    trees = {"b": [unit("trunc", "s.py", 10, explicit=("readOnlyHint",), notes=["TRUNCATED(depth)", "other"])]}
    (t,) = fs.sample_miss(make_run(tmp_path, trees), 1)["targets"]
    assert t["unit"] == "trunc" and t["truncated"] == ["TRUNCATED(depth)"]


def test_miss_one_per_tree_cap_and_determinism(tmp_path):
    trees = {f"t{i:02d}": [unit(f"u{j}", "s.py", j, explicit=("readOnlyHint",)) for j in range(1, 5)]
             for i in range(20)}
    run = make_run(tmp_path, trees)
    a = fs.sample_miss(run, 5, max_trees=8)
    assert a == fs.sample_miss(run, 5, max_trees=8)
    assert a["targets"] != fs.sample_miss(run, 6, max_trees=8)["targets"]
    assert len(a["targets"]) == 8 and len({t["tree"] for t in a["targets"]}) == 8
    assert a["pool"]["n_units"] == 80
    full = fs.sample_miss(run, 5)  # 既定 200 木 > 20 木 → 全木
    assert len(full["targets"]) == 20


# ---------------------------------------------------------------- 不


def test_unknown_sampling(tmp_path):
    trees = {}
    for i in range(12):
        trees[f"r{i:02d}"] = [unit("ro", "s.py", 1, explicit=("readOnlyHint",), rows=unknown_rows("D1", 1 + i % 3))]
        trees[f"d{i:02d}"] = [unit("nd", "s.py", 1, explicit=("destructiveHint",), closed_world=True,
                                   rows=unknown_rows("D2", 2, "fs_writeout") + unknown_rows("D3", 1, "net_host_opaque"))]
    run = make_run(tmp_path, trees)
    a = fs.sample_unknown(run, 3, max_trees=5)
    assert a == fs.sample_unknown(run, 3, max_trees=5)
    assert a["targets"] != fs.sample_unknown(run, 4, max_trees=5)["targets"]
    bd = a["by_decl"]
    assert bd["D1"]["n_trees"] == 12 and bd["D1"]["n_pairs"] == sum(1 + i % 3 for i in range(12))
    assert bd["D1"]["n_trees_selected"] == 5 and bd["D1"]["n_pairs_selected"] == 5
    assert bd["D2"]["n_trees_selected"] == 5 and bd["D2"]["reason_pairs"] == {"fs_writeout": 24}
    # D3・D4 は件数と理由だけ
    assert bd["D3"]["judged"] is False and bd["D3"]["n_pairs"] == 12 and "trees" not in bd["D3"]
    assert bd["D3"]["reason_pairs"] == {"net_host_opaque": 12}
    assert {t["decl"] for t in a["targets"]} == {"D1", "D2"}
    for decl in ("D1", "D2"):
        ts = [t["tree"] for t in a["targets"] if t["decl"] == decl]
        assert len(ts) == len(set(ts)) == 5
    assert all(t["pair_id"].startswith("U-") and t["locations"] for t in a["targets"])
    # 既定 50 木 > 12 木 → 全木、各 1 組
    full = fs.sample_unknown(run, 3)
    assert full["by_decl"]["D1"]["n_pairs_selected"] == 12 and full["by_decl"]["D1"]["trees_sampled"] is False


# ---------------------------------------------------------------- 判定の一致


def fake_sample(kind, n):
    p = fs.ID_PREFIX[kind]
    return {"kind": kind, "seed": 1, "run": "r", "targets": [{"pair_id": f"{p}-{i:03d}"} for i in range(n)]}


@pytest.mark.parametrize("n,k", [(0, 0), (1, 1), (9, 1), (10, 1), (11, 2), (71, 8), (200, 20), (201, 21)])
def test_ceil_tenth(n, k):
    assert fs.ceil_tenth(n) == k


def test_agreement_proportional_ceil_and_deterministic():
    samples = {"contradiction": fake_sample("contradiction", 71), "miss": fake_sample("miss", 63),
               "unknown": fake_sample("unknown", 35)}
    a = fs.sample_agreement(samples, 6)
    assert a == fs.sample_agreement(samples, 6)
    assert a["targets"] != fs.sample_agreement(samples, 7)["targets"]
    assert {k: v["k"] for k, v in a["by_kind"].items()} == {"contradiction": 8, "miss": 7, "unknown": 4}
    for kind, v in a["by_kind"].items():
        ids = {t["pair_id"] for t in samples[kind]["targets"]}
        assert set(v["pair_ids"]) <= ids and len(set(v["pair_ids"])) == v["k"]
    assert a["n_targets"] == 19


def test_agreement_requires_all_kinds():
    with pytest.raises(SystemExit):
        fs.sample_agreement({"contradiction": fake_sample("contradiction", 3)}, 1)


# ---------------------------------------------------------------- 判定表


ANALYZER_COLS = {"reasons", "locations", "site", "kind", "n_effects", "truncated", "witness_chain"}


def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def build_all(tmp_path):
    trees = miss_trees()
    trees.update(many_trees(8))
    trees["z"] = [unit("trunc_only", "s.py", 3, explicit=("readOnlyHint",), notes=["TRUNCATED(wall_clock)"])]
    run = make_run(tmp_path, trees)
    paths = {}
    for kind, fn in (("contradiction", fs.sample_contradiction), ("miss", fs.sample_miss),
                     ("unknown", fs.sample_unknown)):
        paths[kind] = str(tmp_path / f"{kind}.json")
        fs.write_json(paths[kind], fn(run, 1))
    paths["agreement"] = str(tmp_path / "agreement.json")
    fs.write_json(paths["agreement"], fs.sample_agreement(
        {k: json.load(open(paths[k], encoding="utf-8")) for k in fs.KINDS}, 6))
    return paths


def run_sheet(paths, out_dir, seed):
    argv = ["--seed", str(seed), "--out-dir", str(out_dir)]
    for k in (*fs.KINDS, "agreement"):
        argv += [f"--{k}", paths[k]]
    assert fsh.main(argv) == 0


def test_sheet_columns_and_no_analyzer_output_in_miss(tmp_path):
    paths = build_all(tmp_path)
    out = tmp_path / "sheets"
    run_sheet(paths, out, 5)
    miss = read_csv(out / "miss.csv")
    assert miss and not (ANALYZER_COLS & set(miss[0]))
    for col in ("outcome", "cause", "write_target", "condition_type", "condition", "depth", "evidence", "ai_found",
                "note", "minutes", "ai_used", "ai_model", "ai_log", "pair_id", "decl", "unit_relpath", "unit_lineno"):
        assert col in miss[0]
    # 打ち切りの印は sample の JSON にだけある
    raw = (out / "miss.csv").read_text(encoding="utf-8-sig")
    assert "TRUNCATED" not in raw
    assert any(t["truncated"] for t in json.load(open(paths["miss"], encoding="utf-8"))["targets"])
    con = read_csv(out / "contradiction.csv")
    for col in ("tree", "unit", "unit_relpath", "unit_lineno", "site", "kind", "decl", "reasons", "locations",
                "verdict", "condition_type", "error_class", "write_target",
                "unknown_reason", "evidence", "note", "minutes", "ai_used", "ai_model", "ai_log"):
        assert col in con[0]
    for col in ("reachable", "violates", "condition"):  # D83 で書かない欄にした
        assert col not in con[0]
    unk = read_csv(out / "unknown.csv")
    for col in ("outcome", "reachable", "violates", "write_target", "condition_type", "condition", "unknown_reason",
                "evidence", "reasons", "ai_used"):
        assert col in unk[0]
    # 判定の欄は空
    for rows, kind in ((con, "contradiction"), (miss, "miss"), (unk, "unknown")):
        for r in rows:
            assert all(r[c] == "" for c in fsh.JUDGE_COLS[kind])


def test_sheet_order_is_seeded_shuffle_with_stable_ids(tmp_path):
    paths = build_all(tmp_path)
    run_sheet(paths, tmp_path / "s1", 5)
    run_sheet(paths, tmp_path / "s2", 5)
    run_sheet(paths, tmp_path / "s3", 99)
    for kind in fs.KINDS:
        a = (tmp_path / "s1" / f"{kind}.csv").read_text(encoding="utf-8-sig")
        assert a == (tmp_path / "s2" / f"{kind}.csv").read_text(encoding="utf-8-sig")
        r1 = read_csv(tmp_path / "s1" / f"{kind}.csv")
        r3 = read_csv(tmp_path / "s3" / f"{kind}.csv")
        assert [r["seq"] for r in r1] == [str(i) for i in range(1, len(r1) + 1)]
        assert sorted(r["pair_id"] for r in r1) == sorted(r["pair_id"] for r in r3)
        ids = sorted(t["pair_id"] for t in json.load(open(paths[kind], encoding="utf-8"))["targets"])
        assert sorted(r["pair_id"] for r in r1) == ids
    big = read_csv(tmp_path / "s1" / "contradiction.csv")
    assert len(big) > 5
    assert [r["pair_id"] for r in big] != sorted(r["pair_id"] for r in big)
    assert [r["pair_id"] for r in big] != [r["pair_id"] for r in read_csv(tmp_path / "s3" / "contradiction.csv")]
    # 一致の確認の表は本表の部分列
    ag = json.load(open(paths["agreement"], encoding="utf-8"))
    for kind in fs.KINDS:
        sub = read_csv(tmp_path / "s1" / f"agreement_{kind}.csv")
        main = [r["pair_id"] for r in read_csv(tmp_path / "s1" / f"{kind}.csv")]
        assert {r["pair_id"] for r in sub} == set(ag["by_kind"][kind]["pair_ids"])
        assert [r["pair_id"] for r in sub] == [p for p in main if p in set(ag["by_kind"][kind]["pair_ids"])]


def test_miss_columns_guard():
    assert not (fsh.MISS_FORBIDDEN & set(fsh.columns("miss")))
    assert "reasons" in fsh.columns("contradiction")


# ---------------------------------------------------------------- show_target


def test_show_target_finds_by_relpath_and_lineno():
    m = {"units": [
        unit("same", "a.py", 5, explicit=("readOnlyHint",), rows=[
            row("open", "FS_WRITE", "a.py", 9, ["contradiction:D1", "contradiction_reason:D1:fs_write"]),
            row("post", "NET", "a.py", 11, ["contradiction_unknown:D1:net_post"])]),
        unit("same", "b.py", 5, explicit=("destructiveHint",), rows=[
            row("open", "FS_WRITE", "b.py", 7, ["contradiction:D2", "contradiction_reason:D2:fs_remove"])]),
    ]}
    buf = io.StringIO()
    assert st.show(m, "b.py", 5, "open", out=buf) == 0
    text = buf.getvalue()
    assert "D2=矛(fs_remove)" in text and "D1=" not in text and "b.py:7" in text
    buf = io.StringIO()
    assert st.show(m, "a.py", 5, None, decl="D1", out=buf) == 0
    text = buf.getvalue()
    assert "D1=矛(fs_write)" in text and "D1=不(net_post)" in text and "宣言の印: ['D1']" in text
    buf = io.StringIO()
    assert st.show(m, "a.py", 6, "open", out=buf) == 1
    assert "same:5" in buf.getvalue()
