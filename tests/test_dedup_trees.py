"""`scripts/dedup_trees.py`（D70 の 6 の中身の重複の除去）の試験。入力は合成。"""

from __future__ import annotations

import json
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import dedup_trees as dt  # noqa: E402

H = {c: c * 64 for c in "abcdef0123"}  # 合成の sha256（64 桁の 16 進）


def _t(repo, **files):
    return {"repo": repo, "files": {k.replace("__", "/") + ".py": H[v] for k, v in files.items()}}


def test_within_new_keeps_first_by_lowercase_repo_and_reports_partner():
    new = {
        "final-zeta": _t("Zeta/x", server="a"),
        "final-beta": _t("Beta/z", server="a", util="b"),  # 大文字のまま並べると alpha より前になる
        "final-alpha": _t("alpha/y", main="a"),
        "final-solo": _t("solo/q", server="c"),
    }
    r = dt.dedup(new, {})
    assert r["kept"] == ["final-alpha", "final-solo"]
    ex = {e["tree"]: e for e in r["excluded"]}
    assert ex["final-beta"]["partner"] == "final-alpha" and ex["final-beta"]["reason"] == "within_new"
    assert ex["final-beta"]["hash"] == H["a"]
    assert ex["final-beta"]["relpath"] == "server.py" and ex["final-beta"]["partner_relpath"] == "main.py"
    assert ex["final-zeta"]["partner"] == "final-alpha"


def test_prior_match_excludes_and_lists_all_partners():
    new = {"final-a": _t("o/a", server="a", x="d"), "final-b": _t("o/b", server="e")}
    prior = {"hashes_v4": {"v4-p": _t("p/p", tools__srv="d"), "v4-q": _t("q/q", other="d")},
             "hashes_v2": {"v2-r": _t("r/r", s="f")}}
    r = dt.dedup(new, prior)
    assert r["kept"] == ["final-b"]
    (e,) = r["excluded"]
    assert e["reason"] == "prior" and e["partner"] == "hashes_v4:v4-p" and e["hash"] == H["d"]
    assert e["relpath"] == "x.py" and e["partner_relpath"] == "tools/srv.py"
    assert sorted(m["prior_tree"] for m in e["all_matches"]) == ["v4-p", "v4-q"]
    assert r["n_excluded_prior"] == 1 and r["prior_trees"] == {"hashes_v2": 1, "hashes_v4": 2}


def test_prior_excluded_tree_does_not_exclude_others():
    # final-a は v4 と一致して除かれる。final-b は final-a とだけ一致する → 残す（除いた木はもう標本に無い）
    new = {"final-a": _t("a/a", s="a", t="b"), "final-b": _t("b/b", s="b")}
    r = dt.dedup(new, {"v4": {"v4-x": _t("x/x", s="a")}})
    assert r["kept"] == ["final-b"]


def test_chain_is_greedy_against_kept_trees():
    # A–B が一致、B–C が一致、A–C は一致しない。A を残し B を除き、C は残した木のどれとも一致しないので残す
    new = {"c": _t("c/c", s="b"), "a": _t("a/a", s="a"), "b": _t("b/b", s="a", t="b")}
    r = dt.dedup(new, {})
    assert r["kept"] == ["a", "c"] and [e["tree"] for e in r["excluded"]] == ["b"]


def test_tree_without_tool_files_is_kept_and_listed():
    r = dt.dedup({"x": {"repo": "x/x", "files": {}}, "y": _t("y/y", s="a")}, {})
    assert r["kept"] == ["x", "y"] and r["no_tool_files"] == ["x"]


def test_dedup_is_deterministic_under_input_order():
    new = {f"t{i}": _t(f"o/r{i % 4}", s="abcd"[i % 4], u="e" if i % 3 == 0 else "f") for i in range(12)}
    prior = {"v4": {"p": _t("p/p", s="0")}}
    r1 = dt.dedup(new, prior)
    r2 = dt.dedup(dict(reversed(list(new.items()))), prior)
    assert json.dumps(r1, sort_keys=True) == json.dumps(r2, sort_keys=True)


def test_load_hashes_accepts_flat_list_and_rejects_bad_sha(tmp_path):
    p = tmp_path / "v2.json"
    p.write_text(json.dumps([{"tree": "v2-a", "relpath": "s.py", "sha256": H["a"]},
                             {"tree": "v2-a", "relpath": "t.py", "sha256": H["b"]}]), encoding="utf-8")
    h = dt.load_hashes(str(p))
    assert h == {"v2-a": {"repo": None, "files": {"s.py": H["a"], "t.py": H["b"]}}}
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"trees": {"x": {"files": {"s.py": "XYZ"}}}}), encoding="utf-8")
    with pytest.raises(ValueError):
        dt._check_sha(str(bad), dt.load_hashes(str(bad)))


SERVER = b"""from mcp.server.fastmcp import FastMCP
from helper import go

mcp = FastMCP("demo")


@mcp.tool()
def run(path: str) -> str:
    return go(path)
"""


def test_hash_uses_analyzer_entry_discovery(tmp_path):
    tree = tmp_path / "corpus" / "final-o__r"
    tree.mkdir(parents=True)
    (tree / "server.py").write_bytes(SERVER)
    (tree / "helper.py").write_bytes(b"def go(p):\n    return p\n")
    rels, failures = dt.tool_files_by_analyzer(str(tree))
    assert rels == ["server.py"] and failures == []
    sample = tmp_path / "pins.json"
    sample.write_text(json.dumps({"targets": [{"name": "final-o__r", "repo": "o/R"},
                                              {"name": "final-missing", "repo": "o/m"}]}), encoding="utf-8")
    out = tmp_path / "h.json"
    assert dt.main(["hash", "--corpus", str(tmp_path / "corpus"), "--sample", str(sample), "--label", "final",
                    "--out", str(out)]) == 0
    h = json.loads(out.read_text(encoding="utf-8"))
    assert h["missing_trees"] == ["final-missing"]
    assert h["trees"]["final-o__r"]["files"] == {"server.py": dt.sha256_file(str(tree / "server.py"))}
    assert h["trees"]["final-o__r"]["repo"] == "o/R"


def test_dedup_cli_records_partners_and_python_mismatch(tmp_path):
    new = tmp_path / "hashes_final.json"
    new.write_text(json.dumps({"python": "3.12.3", "method": "m", "trees": {
        "final-a": _t("o/a", s="a"), "final-b": _t("o/b", s="b")}}), encoding="utf-8")
    v4 = tmp_path / "hashes_v4.json"
    v4.write_text(json.dumps({"python": "3.10.20", "method": "m", "trees": {"v4-x": _t("x/x", s="b")}}),
                  encoding="utf-8")
    out = tmp_path / "dedup.json"
    assert dt.main(["dedup", "--new", str(new), "--prior", str(v4), "--out", str(out)]) == 0
    r = json.loads(out.read_text(encoding="utf-8"))
    assert r["kept"] == ["final-a"]
    assert r["excluded"][0]["partner"] == "hashes_v4:v4-x" and r["excluded"][0]["hash"] == H["b"]
    assert any("Python の版" in w for w in r["warnings"])
