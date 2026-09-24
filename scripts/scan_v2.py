#!/usr/bin/env python3
"""母集団 v2（`evidence/population_v2/sample_v2_mcp.json`）の full scan を取り直す。

出力は `evidence/scan_v2_<label>/`:

* `<tree>.json`          … 木ごとの manifest（`.gitignore` で追跡しない。13 MB になる）
* `summary.json`         … 木ごとの行数 / 判定の件数と全体の合計
* `contradictions.json`  … CONTRADICTION の行を **ユニット × (site, kind)** に畳んだ手検証の候補表

`evidence/scan_v2_run1..3` は同じ形を手作業のループで作った（D31 / D32）。run4 以降は
この script で作る。**判定の規則はここに無い**（`authgap/verdict.py` のもの）。tree budget は
§2.1 の手続きと同じ 180 秒。

    .venv312/bin/python scripts/scan_v2.py --label run4
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from authgap.report import canonical_json, manifest_json  # noqa: E402
from authgap.runner import RunConfig, run  # noqa: E402
from authgap.val.engine import Options  # noqa: E402


def _contradiction_rows(tree: str, manifest: dict) -> list[dict]:
    out: dict[tuple, dict] = {}
    for u in manifest["units"]:
        dk = u.get("D_kind") or {}
        eff_by = {}
        for e in u.get("effects", []):
            eff_by.setdefault((e["site"], e["kind"]), e)
        for r in u.get("rows", []):
            if "CONTRADICTION" not in r.get("verdicts", []):
                continue
            key = (u["unit"]["unit_id"], r["site"], r["kind"])
            if key in out:
                out[key]["lineno"] = min(out[key]["lineno"], r["lineno"])
                continue
            e = eff_by.get((r["site"], r["kind"]), {})
            out[key] = {
                "tree": tree,
                "unit": u["unit"]["qualname"],
                "tool": u["unit"].get("tool_name"),
                "relpath": r["relpath"],
                "effect_kind": r["kind"],
                "site": r["site"],
                "lineno": r["lineno"],
                "destructive": e.get("destructive"),
                "D_explicit": list(dk.get("explicit", [])),
            }
    return [out[k] for k in sorted(out)]


def _tally(manifest: dict) -> tuple[collections.Counter, int, int]:
    verdicts: collections.Counter = collections.Counter()
    rows = 0
    for u in manifest["units"]:
        for r in u.get("rows", []):
            rows += 1
            for v in r.get("verdicts", []):
                verdicts[v] += 1
    dangerous = sum(1 for u in manifest["units"] if u.get("effects"))
    return verdicts, rows, dangerous


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--label", required=True)
    ap.add_argument("--sample", default=os.path.join(ROOT, "evidence", "population_v2", "sample_v2_mcp.json"))
    ap.add_argument("--tree-budget", type=float, default=180.0)
    ap.add_argument("--note", default="")
    ap.add_argument("--max-depth", type=int, default=None,
                    help="感度分析用（O29）。既定は authgap/ir.py の MAX_DEPTH。manifest の fingerprint は"
                         "定数の値のままなので、実際に使った深さは summary.json の max_depth に残す。")
    ap.add_argument("--resume", action="store_true",
                    help="progress.jsonl にある木を解析し直さない（途中で止まった run の再開）")
    args = ap.parse_args(argv)

    out_dir = os.path.join(ROOT, "evidence", f"scan_v2_{args.label}")
    os.makedirs(out_dir, exist_ok=True)
    targets = json.load(open(args.sample, encoding="utf-8"))["targets"]
    options = Options() if args.max_depth is None else Options(max_depth=args.max_depth)

    # **再開できるようにする。** 木ごとの summary 行を `progress.jsonl` に 1 行ずつ足す。
    # `--resume` はそこにある木を解析し直さず、manifest から件数を数え直す
    # （コンテナの再起動で途中の run が消えたことがある。所要時間は元の run の値のまま）。
    progress_path = os.path.join(out_dir, "progress.jsonl")
    done: dict[str, dict] = {}
    if args.resume and os.path.exists(progress_path):
        with open(progress_path, encoding="utf-8") as fh:
            for line in fh:
                if line.strip():
                    e = json.loads(line)
                    done[e["tree"]] = e
    elif os.path.exists(progress_path):
        os.remove(progress_path)
    n_resumed = 0

    trees: list[dict] = []
    totals: collections.Counter = collections.Counter()
    n_units = n_dangerous = n_rows = 0
    contradictions: list[dict] = []
    for t in targets:
        name = t["name"]
        path = os.path.join(ROOT, "corpus", name)
        mpath = os.path.join(out_dir, f"{name}.json")
        if name in done and (done[name].get("status") != "ok" or os.path.exists(mpath)):
            entry = done[name]
            trees.append(entry)
            n_resumed += 1
            if entry.get("status") == "ok":
                manifest = json.load(open(mpath, encoding="utf-8"))
                verdicts, rows, dangerous = _tally(manifest)
                n_units += len(manifest["units"])
                n_dangerous += dangerous
                n_rows += rows
                totals.update(verdicts)
                contradictions += _contradiction_rows(name, manifest)
            print(f"  {name:48s} (resumed)")
            continue
        t0 = time.monotonic()
        if not os.path.isdir(path):
            entry = {"tree": name, "status": "missing"}
        else:
            try:
                res = run(RunConfig(src_root=path, population=t.get("population", "mcp_server"),
                                    full=True, max_tree_seconds=args.tree_budget, options=options,
                                    prep_budget_exit=True))
            except Exception as exc:  # noqa: BLE001  1 本の失敗で全体を落とさない。件数として残す。
                entry = {"tree": name, "status": "analysis_failed", "error": f"{type(exc).__name__}: {exc}"}
                print(f"FAIL {name}: {type(exc).__name__}: {exc}", file=sys.stderr)
            else:
                manifest = manifest_json(res, args.label)
                with open(mpath, "w", encoding="utf-8") as fh:
                    fh.write(canonical_json(manifest))
                verdicts, rows, dangerous = _tally(manifest)
                n_units += len(manifest["units"])
                n_dangerous += dangerous
                n_rows += rows
                totals.update(verdicts)
                contradictions += _contradiction_rows(name, manifest)
                elapsed = round(time.monotonic() - t0, 1)
                entry = {
                    "tree": name, "status": "ok", "n_units": len(manifest["units"]), "n_rows": rows,
                    "verdicts": dict(sorted(verdicts.items())), "budget_skipped": res.tree_budget_skipped,
                    "elapsed_s": elapsed,
                }
                print(f"  {name:48s} units={len(manifest['units']):4d} rows={rows:4d} {elapsed:6.1f}s")
        trees.append(entry)
        with open(progress_path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")

    summary = {
        "_note": args.note or f"母集団 v2 の full scan（{args.label}）。scripts/scan_v2.py で作成。",
        "analyzer_commit": _git_head(),
        "max_depth": options.max_depth,
        "n_trees_resumed": n_resumed,
        "n_trees": len(trees),
        "n_units": n_units,
        "n_dangerous_units": n_dangerous,
        "n_rows": n_rows,
        "verdict_rows": dict(sorted(totals.items())),
        "trees": trees,
    }
    with open(os.path.join(out_dir, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    with open(os.path.join(out_dir, "contradictions.json"), "w", encoding="utf-8") as fh:
        json.dump({"_note": "CONTRADICTION（ユニット × (site, kind)）。手検証の候補表。",
                   "n": len(contradictions), "rows": contradictions}, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print(f"\nwrote {out_dir}: units {n_units} / dangerous {n_dangerous} / rows {n_rows} / "
          f"verdicts {dict(totals)} / contradictions {len(contradictions)}")
    return 0


def _git_head() -> str:
    import subprocess

    try:
        return subprocess.run(["git", "-C", ROOT, "rev-parse", "HEAD"], capture_output=True, text=True,
                              check=True).stdout.strip()
    except Exception:  # noqa: BLE001
        return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
