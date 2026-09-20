#!/usr/bin/env python3
"""`r_prev` を測る（`docs/preregistration.md` §2.7 (h) の手順 2〜5）。

**規則の定義点は §2.7 であり、本ファイルはその機械化である。** タグの選択は
手順 1（`scripts/prev_releases.py` → `docs/prev_releases.json`、測定より先に
コミット済み）で終わっており、**本スクリプトはタグを選び直さない。**

    .venv/bin/python scripts/r_prev.py --label run1
    # → evidence/r_prev_run1/{r_prev.json, trees.jsonl, prev/<tree>.json, prev5/<tree>.json}

手順:

2. 直前リリース（`prev_sha`）と 5 リリース前（`prev5_sha`、§2.7 (e) の感度分析）を
   `corpus/prev__<tree>` / `corpus/prev5__<tree>` に取得する。取得は
   `scripts/fetch_corpus.fetch` をそのまま使う（**SHA 一致と checkout 完了を検証する。**
   浅い fetch が default branch に落ちる事故を避けるため）。現リリースも
   `evidence/f0a_run6/trees.jsonl` の `commit_sha` で `corpus/<tree>` に取り直す
   （標本の pin が `HEAD` なので、run6 と同じ木を指すために SHA を明示する。O9）。
3. 前リリースを解析して manifest を作る（`authgap.report.manifest_json`）。
4. 現リリースを `prev_manifest` 付きで解析する（`runner.RunConfig.prev_manifest`）。
5. `scripts/f0a.py` の `PopStats` / `accumulate(..., prev_ids=...)` で集計する。
   **`None`（前リリースを供給できなかった木）と `frozenset()`（供給したが
   ユニット 0）を区別する**（§2.7 (f)、D22）。

分母（§2.7 (f)）: 手順 1 で `ok` になった木のうち、取得と解析に成功した木の
危険ユニット（主）/ 全ユニット（粗）。取得失敗は分母に入れず件数を出す。
前リリースにユニットが 0 の木は分母に**入れる**（`r_prev` を下げる側）。

**閾値 50%（§10）はここでは判定しない。** 値を出すだけである。判定は
`docs/preregistration.md` §3 の併記規則に従って本文で行う。
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
import time
from typing import Optional

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from fetch_corpus import Target, fetch  # noqa: E402

from authgap.report import manifest_json  # noqa: E402
from authgap.runner import RunConfig, run  # noqa: E402


def _load_f0a():
    """`scripts/f0a.py` を module として読む（`PopStats` / `accumulate` を再利用）。"""
    if "f0a_mod" in sys.modules:
        return sys.modules["f0a_mod"]
    spec = importlib.util.spec_from_file_location("f0a_mod", os.path.join(ROOT, "scripts", "f0a.py"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["f0a_mod"] = mod
    spec.loader.exec_module(mod)
    return mod


def _fetch(name: str, repo: str, sha: str, population: str) -> tuple[Optional[str], Optional[str]]:
    """`corpus/<name>` に `sha` を取り出す。戻り値 `(path, error)`。"""
    got, err = fetch(Target(repo=repo, ref=sha, name=name, population=population, note="r_prev"))
    if got is None:
        return None, err
    if got.sha != sha:
        return None, f"{name}: 取得 SHA {got.sha[:12]} が要求 {sha[:12]} と違う"
    return got.path, None


def _scan(path: str, population: str, budget: float, prev_manifest: Optional[str] = None):
    return run(
        RunConfig(
            src_root=path,
            population=population,
            full=False,
            max_tree_seconds=budget,
            prev_manifest=prev_manifest,
        )
    )


def _write_manifest(res, out_path: str) -> frozenset[str]:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    man = manifest_json(res, run_id="r_prev", volatile=False)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(man, fh, ensure_ascii=False, indent=1, sort_keys=True)
    return frozenset(u["unit"]["unit_id"] for u in man["units"] if (u.get("unit") or {}).get("unit_id"))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--prev", default="docs/prev_releases.json")
    ap.add_argument("--run", default="evidence/f0a_run6", help="現リリースの SHA を取る run（trees.jsonl）")
    ap.add_argument("--label", default="run1")
    ap.add_argument("--tree-budget", type=float, default=180.0, help="f0a と同じ 1 木の壁時計上限（秒）")
    ap.add_argument("--only", nargs="*", help="木を絞る（デバッグ用）")
    args = ap.parse_args()

    prev = json.load(open(os.path.join(ROOT, args.prev), encoding="utf-8"))
    cur_sha = {}
    with open(os.path.join(ROOT, args.run, "trees.jsonl"), encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                t = json.loads(line)
                cur_sha[t["tree"]] = t.get("commit_sha")

    f0a = _load_f0a()
    rubric = f0a.load_rubric_1c()
    out_dir = os.path.join(ROOT, "evidence", f"r_prev_{args.label}")
    os.makedirs(out_dir, exist_ok=True)

    ok_trees = [t for t in prev["trees"] if t["status"] == "ok"]
    if args.only:
        ok_trees = [t for t in ok_trees if t["tree"] in set(args.only)]
    print(f"手順 1 で ok の木: {len(ok_trees)}（{args.prev}）")

    # 集計は「直前」と「5 リリース前」を別々に持つ（§2.7 (e)）。
    stats: dict[str, dict[str, object]] = {"prev": {}, "prev5": {}}
    rows: list[dict] = []
    for t in ok_trees:
        tree, repo, pop = t["tree"], t["repo"], t["population"]
        sha = cur_sha.get(tree) or t["analyzed_sha"]
        if sha != t["analyzed_sha"]:
            print(f"  ! {tree}: trees.jsonl の SHA と prev_releases.json の analyzed_sha が違う", file=sys.stderr)
        row: dict = {"tree": tree, "repo": repo, "population": pop, "analyzed_sha": sha,
                     "prev_tag": t["prev_tag"], "prev_sha": t["prev_sha"],
                     "prev5_tag": t["prev5_tag"], "prev5_sha": t["prev5_sha"], "prev5_steps_back": t["prev5_steps_back"]}
        t0 = time.monotonic()

        # 現リリース。
        cur_path, err = _fetch(tree, repo, sha, pop)
        if cur_path is None:
            row["status"] = "current_fetch_failed"
            row["error"] = err
            rows.append(row)
            print(f"  FAIL {tree}: {err}")
            continue

        for which in ("prev", "prev5"):
            psha = t[f"{which}_sha"]
            st = stats[which].setdefault(pop, f0a.PopStats(pop))
            if which == "prev5" and psha == t["prev_sha"]:
                # 5 つ遡れず直前と同じタグ（steps_back < 5）。同じ値を再計算せず記録だけ。
                pass
            ppath, err = _fetch(f"{which}__{tree}", repo, psha, pop)
            if ppath is None:
                row[f"{which}_status"] = "prev_fetch_failed"
                row[f"{which}_error"] = err
                print(f"  FAIL {which} {tree}: {err}")
                continue
            try:
                pres = _scan(ppath, pop, args.tree_budget)
            except Exception as exc:  # 1 本の失敗で全体を落とさない。件数として残す。
                row[f"{which}_status"] = "prev_analysis_failed"
                row[f"{which}_error"] = f"{type(exc).__name__}: {exc}"
                print(f"  FAIL {which} scan {tree}: {exc}")
                continue
            man_path = os.path.join(out_dir, which, f"{tree}.json")
            prev_ids = _write_manifest(pres, man_path)
            row[f"{which}_n_units"] = len(pres.tree.units)
            row[f"{which}_budget_skipped"] = pres.tree_budget_skipped
            try:
                cres = _scan(cur_path, pop, args.tree_budget, prev_manifest=man_path)
            except Exception as exc:
                row[f"{which}_status"] = "current_analysis_failed"
                row[f"{which}_error"] = f"{type(exc).__name__}: {exc}"
                print(f"  FAIL current scan {tree}: {exc}")
                continue
            f0a.accumulate(st, cres, rubric, False, prev_ids=prev_ids)
            n_join = sum(1 for u in cres.tree.units if u.d_prev_joined)
            n_dang = sum(1 for u in cres.tree.units if u.has_dangerous_effect)
            n_join_dang = sum(1 for u in cres.tree.units if u.d_prev_joined and u.has_dangerous_effect)
            row[f"{which}_status"] = "ok"
            row["cur_n_units"] = len(cres.tree.units)
            row["cur_n_dangerous"] = n_dang
            row["cur_budget_skipped"] = cres.tree_budget_skipped
            row[f"{which}_n_join"] = n_join
            row[f"{which}_n_join_dangerous"] = n_join_dang
        row["elapsed_s"] = round(time.monotonic() - t0, 1)
        rows.append(row)
        print(f"  {tree:44s} cur={row.get('cur_n_units', '?'):>4} dang={row.get('cur_n_dangerous', '?'):>3} "
              f"prev={row.get('prev_n_units', '?'):>4} join={row.get('prev_n_join', '?'):>3}/{row.get('prev_n_join_dangerous', '?'):>3} "
              f"prev5={row.get('prev5_n_units', '?'):>4} join5={row.get('prev5_n_join', '?'):>3} {row['elapsed_s']:6.1f}s")

    with open(os.path.join(out_dir, "trees.jsonl"), "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")

    summary = {
        "_note": (
            "docs/preregistration.md §2.7 (h) の手順 2〜5 の出力。タグの選択は docs/prev_releases.json"
            "（手順 1、測定より先にコミット）で固定。閾値の判定はここでは行わない。"
        ),
        "label": args.label,
        "prev_releases": args.prev,
        "current_run": args.run,
        "tree_budget_s": args.tree_budget,
        "n_ok_trees_step1": len(ok_trees),
        "by_population": {},
    }
    for which in ("prev", "prev5"):
        summary["by_population"][which] = {}
        for pop, st in stats[which].items():
            summary["by_population"][which][pop] = {
                "n_trees_with_prev": st.n_trees_with_prev,
                "n_units_with_prev_available": st.n_units_with_prev_available,
                "n_dangerous_with_prev_available": st.n_dangerous_with_prev_available,
                "n_units_with_D_prev_join": st.n_d_prev_join,
                "n_dangerous_with_D_prev_join": st.n_d_prev_join_dangerous,
                "r_prev": st.r_prev,
                "r_prev_crude": st.r_prev_crude,
            }
    # 全母集団を合わせた値も出す（§2.7 (a)）。
    for which in ("prev", "prev5"):
        agg = {"n_trees_with_prev": 0, "n_units_with_prev_available": 0, "n_dangerous_with_prev_available": 0,
               "n_units_with_D_prev_join": 0, "n_dangerous_with_D_prev_join": 0}
        for pop in summary["by_population"][which].values():
            for k in agg:
                agg[k] += pop[k]
        agg["r_prev"] = (agg["n_dangerous_with_D_prev_join"] / agg["n_dangerous_with_prev_available"]
                         if agg["n_dangerous_with_prev_available"] else None)
        agg["r_prev_crude"] = (agg["n_units_with_D_prev_join"] / agg["n_units_with_prev_available"]
                               if agg["n_units_with_prev_available"] else None)
        summary["by_population"][which]["_all"] = agg
    with open(os.path.join(out_dir, "r_prev.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write("\n")

    print()
    for which in ("prev", "prev5"):
        print(f"[{which}]")
        for pop, v in summary["by_population"][which].items():
            rp = "None" if v["r_prev"] is None else f"{100 * v['r_prev']:.1f}%"
            rc = "None" if v["r_prev_crude"] is None else f"{100 * v['r_prev_crude']:.1f}%"
            print(f"  {pop:12s} 木 {v['n_trees_with_prev']:2d}  r_prev {rp:>6} "
                  f"({v['n_dangerous_with_D_prev_join']}/{v['n_dangerous_with_prev_available']})  "
                  f"粗 {rc:>6} ({v['n_units_with_D_prev_join']}/{v['n_units_with_prev_available']})")
    print(f"\n-> {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
