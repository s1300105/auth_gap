#!/usr/bin/env python3
"""最終評価の判定の対象を抜き取る（`docs/final_evaluation_procedure.md` 6.3・第 10 節、事前登録 §2.12 (d)）。

4 つの副命令があり、どれも **seed を引数で受け取る**（本物の seed は封をする日に決まるので、ここに書かない）。

* `contradiction` … 矛（seed ①）。D1〜D4 の**宣言ごと**に、矛の出た木が `--max-trees`（200）を超えたら 200 木を選び
  （以下なら全木）、選んだ木ごとに最大 `--per-tree`（3）組を選ぶ。3 組に満たない木は全組（D69、D70 の 1）。
* `miss` … 見落とし（seed ②）。D1 か D2 を明示し（`D_kind.explicit`）、その宣言への矛が 1 件も無いユニットを持つ木から
  `--max-trees`（200）木、各木 1 ユニット。打ち切りの印（`TRUNCATED(...)` の notes）のあるユニットも含め、印は出力の
  `truncated` に残す（D70 の 2。判定表には載せない）。
* `unknown` … 不の中身（seed ③）。D1・D2 のそれぞれで、不の組を持つ木から `--max-trees`（50）木、各木 1 組。
  D3・D4 の不は件数と理由だけ（判定しない）。
* `agreement` … 判定の一致を確かめる組（seed ⑥）。上の 3 つの出力の全件から、種類ごとに件数の 10%（端数は切り上げ）を選ぶ。

組の鍵は `scripts/v3_judge_sample.py` と同じ **(木, ユニットの relpath, ユニットの行, qualname, site, kind, 宣言)**。
組の矛 / 不は `scripts/contradiction_by_decl.py` の `load_reasons` と `apply_flip(…, None)` で決める（同じ組・同じ宣言に
矛と不の両方の注記があれば矛。`docs/population_v4.md` の「矛」「不」の列と同じ数え方）。見落としの対象の決め方は
`scripts/v3_miss_sample.py` と同じ（manifest の集合は summary.json の ok の木、ユニットは relpath と行で区別。D64）。

決定論（CLAUDE.md、6.3）: 木と組は型つきの鍵で**ソートしてから** `random.Random(seed)` で選ぶ。乱数は 1 本の列を
決まった順に使う（出力の `rng_order` に書く）。`random` の `sample` / `randrange` の結果は Python の版で変わりうる
（保証されているのは `seed` と `random()` だけ）ので、出力に `python` を書く。**同じ Python で走らせる。**

出力には、選んだ組に加えて**選ばなかった分を含む件数**（宣言ごと・木ごとの矛の総数、不の理由ごとの総数、見落としの
対象の総数）を書く。件数は第 23 節の「参考（件数）」と分母に使う。**判定の前に出力をコミットする。**

    .venv/bin/python scripts/final_sample.py contradiction evidence/scan_v2_final_run1 --seed <①> \\
        --out evidence/population_final/final_judge_targets.json
    .venv/bin/python scripts/final_sample.py miss evidence/scan_v2_final_run1 --seed <②> \\
        --out evidence/population_final/final_miss_targets.json
    .venv/bin/python scripts/final_sample.py unknown evidence/scan_v2_final_run1 --seed <③> \\
        --out evidence/population_final/final_unknown_targets.json
    .venv/bin/python scripts/final_sample.py agreement --seed <⑥> \\
        --contradiction evidence/population_final/final_judge_targets.json \\
        --miss evidence/population_final/final_miss_targets.json \\
        --unknown evidence/population_final/final_unknown_targets.json \\
        --out evidence/population_final/final_agreement_targets.json
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from contradiction_by_decl import apply_flip, load_reasons  # noqa: E402
from runlib import load_manifest, run_manifests, unit_key  # noqa: E402

DECLS = ("D1", "D2", "D3", "D4")
#: 不の中身を判定する宣言（D69。D3・D4 は件数と理由だけ）
UNKNOWN_JUDGED = ("D1", "D2")
KINDS = ("contradiction", "miss", "unknown")
ID_PREFIX = {"contradiction": "C", "miss": "M", "unknown": "U"}


# ---------------------------------------------------------------- 共通


def pair_sort_key(p: tuple) -> tuple:
    """組の鍵 (木, relpath, 行, qualname, site, kind[, 宣言]) を型つきで並べる鍵（None でも落ちない）。"""
    tree, relpath, lineno, qual, *rest = p
    return (str(tree), str(relpath or ""), lineno if isinstance(lineno, int) else -1, str(qual),
            *(str(x) for x in rest))


def unit_sort_key(u: dict) -> tuple:
    return (str(u["unit_relpath"] or ""), u["unit_lineno"] if isinstance(u["unit_lineno"], int) else -1,
            str(u["unit"]))


def declared(dk: dict) -> set[str]:
    """ユニットが明示した宣言（解析器が矛を判定するときと同じ条件。事前登録 §2.12 (f)、D73 の 3）。"""
    # `authgap/dparse.py: contradiction_findings` と同じ分岐: D2 は readOnly が無いとき（elif）、D4 も readOnly が無いとき
    ex = set(dk.get("explicit") or [])
    ro = "readOnlyHint" in ex
    out = set()
    if ro:
        out.add("D1")
    elif "destructiveHint" in ex:
        out.add("D2")
    if dk.get("closed_world"):
        out.add("D3")
    if dk.get("idempotent") and not ro:
        out.add("D4")
    return out


def miss_decl(dk: dict) -> str | None:
    """見落としの対象の宣言（`v3_miss_sample.py` と同じ。D1 と D2 は `explicit` で排他）。"""
    ex = set(dk.get("explicit") or [])
    return "D1" if "readOnlyHint" in ex else ("D2" if "destructiveHint" in ex else None)


def truncation_marks(u: dict) -> list[str]:
    return sorted(str(n) for n in (u.get("notes") or []) if str(n).startswith("TRUNCATED"))


def checked_manifests(run_dir: str, allow_missing: bool) -> tuple[list[tuple[str, str]], list[str]]:
    """manifest の集合（summary.json の ok の木）。ok なのに manifest が無い木があれば止まる（数え落としになる）。"""
    manifests, warnings = run_manifests(run_dir)
    for w in warnings:
        print(f"警告: {w}", file=sys.stderr)
    if any("manifest が無い" in w for w in warnings) and not allow_missing:
        raise SystemExit("summary.json で ok なのに manifest が無い木がある。件数が欠けるので止める"
                         "（--allow-missing-manifests で続けると、その木は数えない）")
    return manifests, warnings


def run_meta(run_dir: str) -> dict:
    p = os.path.join(run_dir, "summary.json")
    if not os.path.exists(p):
        return {"run": os.path.basename(run_dir.rstrip("/")), "summary": None}
    with open(p, encoding="utf-8") as fh:
        s = json.load(fh)
    return {"run": os.path.basename(run_dir.rstrip("/")), "analyzer_commit": s.get("analyzer_commit"),
            "implementation_sha256_combined": s.get("implementation_sha256_combined"),
            "authgap_dirty": s.get("authgap_dirty"), "max_depth": s.get("max_depth"), "python_scan": s.get("python"),
            "n_trees_ok": sum(1 for t in s.get("trees", []) if t.get("status") == "ok"),
            "n_trees_summary": len(s.get("trees", []))}


def classify_pairs(run_dir: str) -> dict[tuple, dict]:
    """`{(木, relpath, 行, qualname, site, kind, 宣言): {"status": "矛"|"不", "reasons": [...], "unknown_reasons": [...]}}`。

    `reasons` は、矛なら矛の理由、不なら不の理由。`unknown_reasons` は組に付いた不の理由の全部（矛の組にも残す。
    `contradiction_by_decl.py` の理由ごとの内訳と突き合わせるため）。
    """
    out = {}
    for key, decls in load_reasons(run_dir).items():
        for decl, findings in decls.items():
            status = apply_flip(findings, decl, None)
            if status == "内":
                continue
            want = "contradiction" if status == "矛" else "unknown"
            out[(*key, decl)] = {"status": status,
                                 "reasons": sorted({r for s, r in findings if s == want}),
                                 "unknown_reasons": sorted({r for s, r in findings if s == "unknown"})}
    return out


def pair_locations(run_dir: str, pairs: list[tuple], status: str) -> dict[tuple, list[str]]:
    """選んだ組の位置: その組（site, kind）の行のうち、その宣言の矛（`contradiction_reason:<宣言>:`）か
    不（`contradiction_unknown:<宣言>:`）の注記を持つ行の位置。`contradictions.json` の `locations` と同じ範囲。"""
    note = "contradiction_reason" if status == "矛" else "contradiction_unknown"
    want: dict[str, dict[tuple, list[tuple]]] = collections.defaultdict(lambda: collections.defaultdict(list))
    for p in pairs:
        want[p[0]][p[:4]].append(p)
    out: dict[tuple, set] = {p: set() for p in pairs}
    for tree, units in want.items():
        for u in load_manifest(os.path.join(run_dir, f"{tree}.json"))["units"]:
            uk = unit_key(tree, u["unit"])
            if uk not in units:
                continue
            for p in units[uk]:
                site, kind, decl = p[4], p[5], p[6]
                for r in u.get("rows", []):
                    if r.get("site") == site and r.get("kind") == kind and any(
                            str(n).startswith(f"{note}:{decl}:") for n in r.get("notes", [])):
                        out[p].add((r.get("relpath"), r.get("lineno")))
    return {p: [f"{a}:{b}" for a, b in sorted(v, key=lambda x: (str(x[0] or ""), x[1] if isinstance(x[1], int) else -1))]
            for p, v in out.items()}


def pair_record(p: tuple) -> dict:
    tree, relpath, lineno, qual, site, kind, decl = p
    return {"tree": tree, "unit": qual, "unit_relpath": relpath, "unit_lineno": lineno,
            "site": site, "kind": kind, "decl": decl}


def write_json(path: str, obj: dict) -> None:
    d = os.path.dirname(os.path.abspath(path))
    os.makedirs(d, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


def select_trees_then_pairs(rng: random.Random, by_tree: dict[str, list[tuple]], max_trees: int,
                            per_tree: int) -> tuple[list[str], dict[str, list[tuple]]]:
    """木をソートし、`max_trees` を超えたら `rng.sample` で選ぶ。選んだ木を順に、組をソートして `per_tree` を
    超えたら `rng.sample` で選ぶ（`per_tree == 1` のときも sample で 1 つ）。以下なら全部（乱数を使わない）。"""
    trees = sorted(by_tree)
    chosen = sorted(rng.sample(trees, max_trees)) if len(trees) > max_trees else trees
    picked = {}
    for t in chosen:
        ps = sorted(by_tree[t], key=pair_sort_key)
        idx = sorted(rng.sample(range(len(ps)), per_tree)) if len(ps) > per_tree else list(range(len(ps)))
        picked[t] = [ps[i] for i in idx]
    return chosen, picked


# ---------------------------------------------------------------- 矛


def contradictions_json_counts(run_dir: str) -> dict | None:
    p = os.path.join(run_dir, "contradictions.json")
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as fh:
        c = json.load(fh)
    cnt = collections.Counter(d for r in c.get("rows", []) for d in r.get("declarations", []))
    return {d: cnt.get(d, 0) for d in DECLS}


def denominators(manifests: list[tuple[str, str]]) -> dict:
    """主 (c) の分母 M_d（宣言 d を明示したユニットを 1 つ以上持つ木）と、参考 (b) の分母（走査した木）。"""
    m = {d: set() for d in DECLS}
    for tree, path in manifests:
        for u in load_manifest(path)["units"]:
            for d in declared(u.get("D_kind") or {}):
                m[d].add(tree)
    return {"n_trees_scanned": len(manifests), "M_d": {d: len(m[d]) for d in DECLS},
            "_note": "M_d は D_kind で決める（D1: explicit に readOnlyHint、D2: explicit に destructiveHint、"
                     "D3: closed_world、D4: idempotent。事前登録 §2.12 (f)）。走査した木 = summary.json の ok の木。"}


def sample_contradiction(run_dir: str, seed: int, max_trees: int = 200, per_tree: int = 3,
                         allow_missing: bool = False) -> dict:
    manifests, warnings = checked_manifests(run_dir, allow_missing)
    pairs = classify_pairs(run_dir)
    rng = random.Random(seed)
    by_decl, targets = {}, []
    for decl in DECLS:
        by_tree: dict[str, list[tuple]] = collections.defaultdict(list)
        for p, v in pairs.items():
            if p[6] == decl and v["status"] == "矛":
                by_tree[p[0]].append(p)
        chosen, picked = select_trees_then_pairs(rng, by_tree, max_trees, per_tree)
        sel = [p for t in chosen for p in picked[t]]
        locs = pair_locations(run_dir, sel, "矛")
        for k, p in enumerate(sel):
            targets.append({"pair_id": f"C-{decl}-{k + 1:03d}", **pair_record(p),
                            "reasons": pairs[p]["reasons"], "locations": locs[p],
                            "n_pairs_in_tree": len(by_tree[p[0]])})
        chosen_set = set(chosen)
        by_decl[decl] = {
            "n_pairs": sum(len(v) for v in by_tree.values()), "n_trees": len(by_tree),
            "trees_sampled": len(by_tree) > max_trees,
            "n_trees_selected": len(chosen), "n_pairs_selected": len(sel),
            "trees": [{"tree": t, "n_pairs": len(by_tree[t]), "selected": t in chosen_set,
                       "n_selected": len(picked.get(t, []))} for t in sorted(by_tree)],
        }
    cj = contradictions_json_counts(run_dir)
    consistency = {"contradictions_json_by_decl": cj,
                   "manifest_by_decl": {d: by_decl[d]["n_pairs"] for d in DECLS},
                   "match": None if cj is None else all(cj[d] == by_decl[d]["n_pairs"] for d in DECLS)}
    if consistency["match"] is False:
        msg = f"contradictions.json と manifest の矛の件数が合わない: {consistency}"
        if not allow_missing:
            raise SystemExit(msg)
        # manifest の無い木を数えないと決めたときは、合わないのが当然なので記録だけ
        print(f"警告: {msg}", file=sys.stderr)
        warnings = [*warnings, msg]
    return {
        "_note": "最終評価の矛の判定対象（事前登録 §2.12 (d)、D69・D70 の 1）。判定の前にコミットする。",
        "kind": "contradiction", "seed": seed, "seed_role": "① 矛の抜き取り",
        "rules": {"max_trees_per_decl": max_trees, "max_pairs_per_tree": per_tree, "unit": "宣言ごと（D70 の 1 (a)）"},
        "rng_order": "random.Random(seed) を 1 本。D1→D2→D3→D4 の順に、(1) 木が上限を超えたら木の sample、"
                     "(2) 選んだ木を名前の順に、組が上限を超えたらその木の組の sample。上限以下なら乱数を使わない。",
        "python": sys.version.split()[0], **run_meta(run_dir), "warnings": warnings,
        "denominators": denominators(manifests), "consistency": consistency,
        "by_decl": by_decl, "n_targets": len(targets), "targets": targets,
    }


# ---------------------------------------------------------------- 見落とし


def sample_miss(run_dir: str, seed: int, max_trees: int = 200, allow_missing: bool = False) -> dict:
    manifests, warnings = checked_manifests(run_dir, allow_missing)
    contra = {(*p[:4], p[6]) for p, v in classify_pairs(run_dir).items() if v["status"] == "矛"}
    pool: dict[str, list[dict]] = collections.defaultdict(list)
    for tree, path in manifests:
        for u in load_manifest(path)["units"]:
            decl = miss_decl(u.get("D_kind") or {})
            if decl is None or (*unit_key(tree, u["unit"]), decl) in contra:
                continue
            pool[tree].append({"tree": tree, "unit": u["unit"]["qualname"], "unit_relpath": u["unit"].get("relpath"),
                               "unit_lineno": u["unit"].get("lineno"), "decl": decl,
                               "n_effects": len(u.get("effects") or []), "truncated": truncation_marks(u)})
    rng = random.Random(seed)
    trees = sorted(pool)
    chosen = sorted(rng.sample(trees, max_trees)) if len(trees) > max_trees else trees
    targets = []
    for k, tree in enumerate(chosen):
        units = sorted(pool[tree], key=unit_sort_key)
        targets.append({"pair_id": f"M-{k + 1:03d}", **units[rng.randrange(len(units))],
                        "n_units_in_tree": len(units)})
    allu = [x for v in pool.values() for x in v]
    return {
        "_note": "最終評価の見落としの判定対象（事前登録 §2.12 (d)、D69・D70 の 2）。判定の前にコミットする。"
                 "n_effects と truncated は解析器の情報なので、判定表（final_sheet.py の miss.csv）には載せない。",
        "kind": "miss", "seed": seed, "seed_role": "② 見落としの抜き取り",
        "rules": {"max_trees": max_trees, "units_per_tree": 1,
                  "eligible": "D_kind.explicit に readOnlyHint（D1）か destructiveHint（D2）があり、その宣言への矛が"
                              "1 件も無いユニット。打ち切りの印のあるユニットも含める。D1 と D2 は木を選ぶときに合わせて扱う"},
        "rng_order": "random.Random(seed) を 1 本。(1) 木が上限を超えたら木の sample、(2) 選んだ木を名前の順に、"
                     "その木の対象のユニット（relpath・行・qualname の順）から randrange で 1 つ"
                     "（`scripts/v4pilot_depth.py` と同じ）。",
        "python": sys.version.split()[0], **run_meta(run_dir), "warnings": warnings,
        "pool": {"n_units": len(allu), "n_trees": len(trees),
                 "n_units_by_decl": {d: sum(1 for x in allu if x["decl"] == d) for d in ("D1", "D2")},
                 "n_trees_by_decl": {d: len({x["tree"] for x in allu if x["decl"] == d}) for d in ("D1", "D2")},
                 "n_units_truncated": sum(1 for x in allu if x["truncated"])},
        "n_targets": len(targets), "targets": targets,
    }


# ---------------------------------------------------------------- 不


def sample_unknown(run_dir: str, seed: int, max_trees: int = 50, allow_missing: bool = False) -> dict:
    _, warnings = checked_manifests(run_dir, allow_missing)
    pairs = classify_pairs(run_dir)
    rng = random.Random(seed)
    by_decl, targets = {}, []
    for decl in DECLS:
        by_tree: dict[str, list[tuple]] = collections.defaultdict(list)
        reason_pairs: collections.Counter = collections.Counter()
        reason_all: collections.Counter = collections.Counter()
        for p, v in pairs.items():
            if p[6] != decl:
                continue
            for r in v["unknown_reasons"]:
                reason_all[r] += 1
            if v["status"] == "不":
                by_tree[p[0]].append(p)
                for r in v["reasons"]:
                    reason_pairs[r] += 1
        entry = {"n_pairs": sum(len(v) for v in by_tree.values()), "n_trees": len(by_tree),
                 "reason_pairs": dict(sorted(reason_pairs.items())),
                 "reason_pairs_incl_contradiction_pairs": dict(sorted(reason_all.items())),
                 "judged": decl in UNKNOWN_JUDGED}
        if decl in UNKNOWN_JUDGED:
            chosen, picked = select_trees_then_pairs(rng, by_tree, max_trees, 1)
            sel = [p for t in chosen for p in picked[t]]
            locs = pair_locations(run_dir, sel, "不")
            for k, p in enumerate(sel):
                targets.append({"pair_id": f"U-{decl}-{k + 1:03d}", **pair_record(p),
                                "reasons": pairs[p]["reasons"], "locations": locs[p],
                                "n_pairs_in_tree": len(by_tree[p[0]])})
            chosen_set = set(chosen)
            entry.update({"trees_sampled": len(by_tree) > max_trees, "n_trees_selected": len(chosen),
                          "n_pairs_selected": len(sel),
                          "trees": [{"tree": t, "n_pairs": len(by_tree[t]), "selected": t in chosen_set}
                                    for t in sorted(by_tree)]})
        by_decl[decl] = entry
    return {
        "_note": "最終評価の不の中身の判定対象（事前登録 §2.12 (d)、D69 の 4、手順書 0-14）。判定の前にコミットする。"
                 "不の組 = その宣言に不の注記があり、矛の注記が無い組（contradiction_by_decl.py と同じ）。"
                 "reason_pairs は不の組を理由ごとに数えた数（1 組に理由が複数あれば各理由に 1 ずつ。合計は組の数以上）。"
                 "reason_pairs_incl_contradiction_pairs は矛の組に付いた不の理由も含めた数"
                 "（contradiction_by_decl.py の「理由ごとの内訳」の不の行と同じ数え方）。",
        "kind": "unknown", "seed": seed, "seed_role": "③ 不の中身の抜き取り",
        "rules": {"judged_decls": list(UNKNOWN_JUDGED), "max_trees_per_decl": max_trees, "pairs_per_tree": 1},
        "rng_order": "random.Random(seed) を 1 本。D1→D2 の順に、(1) 木が上限を超えたら木の sample、(2) 選んだ木を"
                     "名前の順に、その木の不の組（鍵の順）が 2 組以上なら sample で 1 組。",
        "python": sys.version.split()[0], **run_meta(run_dir), "warnings": warnings,
        "by_decl": by_decl, "n_targets": len(targets), "targets": targets,
    }


# ---------------------------------------------------------------- 判定の一致


def ceil_tenth(n: int) -> int:
    return (n + 9) // 10


def sample_agreement(samples: dict[str, dict], seed: int) -> dict:
    """種類ごとに件数の 10%（切り上げ）を選ぶ。種類の順は contradiction → miss → unknown（1 本の乱数の列）。"""
    rng = random.Random(seed)
    by_kind, targets = {}, []
    for kind in KINDS:
        s = samples.get(kind)
        if s is None:
            raise SystemExit(f"{kind} の抜き取りの出力が無い（3 つ全部を渡す）")
        if s.get("kind") != kind:
            raise SystemExit(f"--{kind} に渡したファイルの kind が {s.get('kind')!r}")
        ids = sorted(t["pair_id"] for t in s["targets"])
        if len(set(ids)) != len(ids):
            raise SystemExit(f"{kind} の pair_id が重複している")
        k = ceil_tenth(len(ids))
        pick = sorted(rng.sample(ids, k)) if k < len(ids) else ids
        by_kind[kind] = {"n": len(ids), "k": len(pick), "pair_ids": pick}
        targets += [{"kind": kind, "pair_id": i} for i in pick]
    return {
        "_note": "判定の一致を確かめる組（事前登録 §2.12 (d)(e)、D73 の 1）。(i) 2 人目の判定者か (ii) 判定し直しに使う。"
                 "判定の前にコミットする。",
        "kind": "agreement", "seed": seed, "seed_role": "⑥ 判定の一致を確かめる組の抜き取り",
        "rules": {"rate": "10%", "rounding": "切り上げ（k = ceil(n / 10)）", "strata": list(KINDS)},
        "rng_order": "random.Random(seed) を 1 本。contradiction → miss → unknown の順に、pair_id をソートして sample。",
        "python": sys.version.split()[0],
        "inputs": {kind: {"seed": samples[kind].get("seed"), "run": samples[kind].get("run"),
                          "n_targets": len(samples[kind]["targets"])} for kind in KINDS},
        "by_kind": by_kind, "n_targets": len(targets), "targets": targets,
    }


# ---------------------------------------------------------------- CLI


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, default_trees in (("contradiction", 200), ("miss", 200), ("unknown", 50)):
        p = sub.add_parser(name)
        p.add_argument("run_dir", help="evidence/scan_v2_<label>/")
        p.add_argument("--seed", type=int, required=True)
        p.add_argument("--out", required=True)
        p.add_argument("--max-trees", type=int, default=default_trees)
        p.add_argument("--allow-missing-manifests", action="store_true")
        if name == "contradiction":
            p.add_argument("--per-tree", type=int, default=3)
    p = sub.add_parser("agreement")
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--out", required=True)
    for kind in KINDS:
        p.add_argument(f"--{kind}", required=True)
    a = ap.parse_args(argv)
    if a.cmd == "contradiction":
        out = sample_contradiction(a.run_dir, a.seed, a.max_trees, a.per_tree, a.allow_missing_manifests)
        summary = {d: {k: v[k] for k in ("n_pairs", "n_trees", "n_trees_selected", "n_pairs_selected")}
                   for d, v in out["by_decl"].items()}
    elif a.cmd == "miss":
        out = sample_miss(a.run_dir, a.seed, a.max_trees, a.allow_missing_manifests)
        summary = {**out["pool"], "n_targets": out["n_targets"]}
    elif a.cmd == "unknown":
        out = sample_unknown(a.run_dir, a.seed, a.max_trees, a.allow_missing_manifests)
        summary = {d: {k: v.get(k) for k in ("n_pairs", "n_trees", "n_trees_selected", "n_pairs_selected")}
                   for d, v in out["by_decl"].items()}
    else:
        samples = {}
        for kind in KINDS:
            with open(getattr(a, kind), encoding="utf-8") as fh:
                samples[kind] = json.load(fh)
        out = sample_agreement(samples, a.seed)
        summary = {k: {"n": v["n"], "k": v["k"]} for k, v in out["by_kind"].items()}
    write_json(a.out, out)
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
