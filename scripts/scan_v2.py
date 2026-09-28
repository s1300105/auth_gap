#!/usr/bin/env python3
"""母集団 v2（`evidence/population_v2/sample_v2_mcp.json`）の full scan を取り直す。

出力は `evidence/scan_v2_<label>/`:

* `<tree>.json`          … 木ごとの manifest（`.gitignore` で追跡しない。13 MB になる）
* `summary.json`         … 木ごとの行数 / 判定の件数と全体の合計
* `contradictions.json`  … CONTRADICTION の行を **ユニット × (site, kind)** に畳んだ手検証の候補表

`evidence/scan_v2_run1..3` は同じ形を手作業のループで作った（D31 / D32）。run4 以降は
この script で作る。**判定の規則はここに無い**（`authgap/verdict.py` のもの）。tree budget は
§2.1 の手続きと同じ 180 秒。

D64（添削の段階 A）で直したこと:

* 候補表の畳み込みの鍵に**ユニットの位置**を入れる（U50 / R5-r1-3。unit_id が同じ別モジュールの同名ツールを潰さない）。
  代表の位置は (relpath, lineno) の**対**の最小（U51 / R5-r3-1。以前は別の行の relpath と lineno を混ぜていた）。
  destructive はその組の CONTRADICTION 行に (relpath, lineno, site, kind) で一致する効果の any（R5-r1-8）。
  組の全位置を `locations` に並べる。
* 書き出しはすべて `errors="backslashreplace"` で、manifest は一時ファイル + `os.replace`（U52 / R5-r2-6。
  孤立サロゲートの定数で run 全体が止まり書きかけのファイルが残っていた）。
* `--resume` なしで、出力先にすでに manifest があれば止める。解析に失敗した木の古い manifest は消す（R5-r2-7）。
* summary に実装の指紋（`authgap/` の結合 sha256・未コミットの変更の有無・authgap の最終 commit・Python の版）を
  残す。`--require-fingerprint` で凍結の記録と照合する（U54 / R5-r2-4）。
* 効果の件数は生の行数と一意の行数を併記する（U32 / R4-r1-8。解析器は変えない）。

    .venv312/bin/python scripts/scan_v2.py --label run4
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import os
import sys
import tempfile
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from authgap.report import canonical_json, manifest_json  # noqa: E402
from authgap.runner import RunConfig, run  # noqa: E402
from authgap.val.engine import Options  # noqa: E402


def _contradiction_rows(tree: str, manifest: dict) -> list[dict]:
    """CONTRADICTION 行を **ユニット × (site, kind)** に畳む（D31）。ユニットは unit_id と位置で区別する。"""
    groups: dict[tuple, dict] = {}
    for u in manifest["units"]:
        un = u["unit"]
        dk = u.get("D_kind") or {}
        eff_by: dict[tuple, list] = collections.defaultdict(list)
        for e in u.get("effects", []):
            eff_by[(e.get("relpath"), e.get("lineno"), e["site"], e["kind"])].append(e)
        for r in u.get("rows", []):
            if "CONTRADICTION" not in r.get("verdicts", []):
                continue
            key = (un["unit_id"], un.get("relpath") or "", un.get("lineno") or 0, r["site"], r["kind"])
            g = groups.setdefault(key, {"unit": u, "dk": dk, "locs": {}})
            decls = sorted({n.split(":")[1] for n in r.get("notes", []) if n.startswith("contradiction:")})
            effs = eff_by.get((r["relpath"], r["lineno"], r["site"], r["kind"]), [])
            ds = [e.get("destructive") for e in effs if "destructive" in e]
            loc = g["locs"].setdefault((r["relpath"], r["lineno"]), {"declarations": set(), "ds": []})
            loc["declarations"] |= set(decls)
            loc["ds"] += ds
    out = []
    for key in sorted(groups, key=lambda k: tuple(str(x) for x in k)):
        g = groups[key]
        u = g["unit"]
        for v in g["locs"].values():
            v["destructive"] = _any_destructive(v.pop("ds"))
        locs = sorted(g["locs"].items(), key=lambda kv: (kv[0][0] or "", kv[0][1] or 0))
        (relpath, lineno), _ = locs[0]
        destructive = _any_destructive([v["destructive"] for _, v in locs])
        out.append({
            "tree": tree,
            "unit": u["unit"]["qualname"],
            "unit_relpath": u["unit"].get("relpath"),
            "unit_lineno": u["unit"].get("lineno"),
            "tool": u["unit"].get("tool_name"),
            "relpath": relpath,
            "effect_kind": key[4],
            "site": key[3],
            "lineno": lineno,
            "destructive": destructive,
            "D_explicit": list(g["dk"].get("explicit", [])),
            # どの宣言に反したか（D56。D1〜D4 は 4 つとも主指標、D62）
            "declarations": sorted(set().union(*(v["declarations"] for _, v in locs))),
            "locations": [{"relpath": rp, "lineno": ln, "declarations": sorted(v["declarations"]),
                           "destructive": v["destructive"]} for (rp, ln), v in locs],
        })
    return out


def _any_destructive(vals: list) -> bool | None:
    """True が 1 つでもあれば True、全部 False なら False、それ以外（無い・None を含む）は None。"""
    if any(v is True for v in vals):
        return True
    if vals and all(v is False for v in vals):
        return False
    return None


def _tally(manifest: dict) -> dict:
    verdicts: collections.Counter = collections.Counter()
    rows = 0
    n_effects = 0
    uniq: set[str] = set()
    for u in manifest["units"]:
        uid = json.dumps(u["unit"], sort_keys=True, ensure_ascii=False)
        for e in u.get("effects", []):
            n_effects += 1
            uniq.add(uid + "|" + json.dumps(e, sort_keys=True, ensure_ascii=False))
        for r in u.get("rows", []):
            rows += 1
            for v in r.get("verdicts", []):
                verdicts[v] += 1
    dangerous = sum(1 for u in manifest["units"] if u.get("effects"))
    return {"verdicts": verdicts, "rows": rows, "dangerous": dangerous,
            "n_effects": n_effects, "n_effects_unique": len(uniq)}


def _write_text(path: str, text: str) -> None:
    """UTF-8 で書けない文字（孤立サロゲート）はバックスラッシュのエスケープにし、一時ファイル + os.replace で書く。

    JSON の文字列の中では json.load で元の str に戻る。本物のバックスラッシュは json.dumps がすでに二重にしている。
    """
    d = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(prefix=".tmp-", dir=d)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", errors="backslashreplace") as fh:
            fh.write(text)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def _check_out_dir(out_dir: str, resume: bool) -> str | None:
    """`--resume` なしで出力先に manifest がすでにあれば、止める理由を返す（古い木の manifest を数えないため）。"""
    if resume or not os.path.isdir(out_dir):
        return None
    old = [fn for fn in os.listdir(out_dir) if fn.endswith(".json") and fn not in ("summary.json", "contradictions.json")]
    if old:
        return (f"{out_dir} にすでに manifest が {len(old)} 件ある。同じ label で取り直すなら別の label にするか、"
                "中身を確かめて消してから走らせる（--resume は途中で止まった run の再開用）")
    return None


def _implementation_record() -> dict:
    """run を取った解析器の実装の指紋（U54）。比べるのは HEAD の文字列ではなくこの値。"""
    from freeze_f0a import implementation_hashes

    from authgap.report import canonical_json as _cj

    impl = implementation_hashes()
    return {
        "implementation_sha256_combined": hashlib.sha256(_cj(impl).encode("utf-8")).hexdigest(),
        "authgap_dirty": bool(_git("status", "--porcelain", "--", "authgap")),
        "authgap_last_commit": _git("log", "-1", "--format=%H", "--", "authgap"),
        "python": sys.version.split()[0],
    }


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
    ap.add_argument("--require-fingerprint", default=None,
                    help="凍結の記録（docs/fingerprint.json）。実装の結合 sha256 が一致しないか authgap/ に未コミットの"
                         "変更があれば走らせない（最終評価で使う。既定では照合しない）")
    args = ap.parse_args(argv)

    out_dir = os.path.join(ROOT, "evidence", f"scan_v2_{args.label}")
    why = _check_out_dir(out_dir, args.resume)
    if why:
        print(f"**止める**: {why}", file=sys.stderr)
        return 2
    impl = _implementation_record()
    if args.require_fingerprint:
        with open(args.require_fingerprint, encoding="utf-8") as fh:
            frozen = json.load(fh)
        if impl["authgap_dirty"] or frozen.get("implementation_sha256_combined") != impl["implementation_sha256_combined"]:
            print(f"**止める**: 解析器が凍結の記録と一致しない（dirty={impl['authgap_dirty']}、"
                  f"今 {impl['implementation_sha256_combined'][:12]} / 凍結 "
                  f"{str(frozen.get('implementation_sha256_combined'))[:12]}）", file=sys.stderr)
            return 2
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
    n_units = n_dangerous = n_rows = n_effects = n_effects_unique = 0
    contradictions: list[dict] = []

    def _add(manifest: dict, name: str) -> dict:
        nonlocal n_units, n_dangerous, n_rows, n_effects, n_effects_unique, contradictions
        tl = _tally(manifest)
        n_units += len(manifest["units"])
        n_dangerous += tl["dangerous"]
        n_rows += tl["rows"]
        n_effects += tl["n_effects"]
        n_effects_unique += tl["n_effects_unique"]
        totals.update(tl["verdicts"])
        contradictions += _contradiction_rows(name, manifest)
        return tl
    for t in targets:
        name = t["name"]
        path = os.path.join(ROOT, "corpus", name)
        mpath = os.path.join(out_dir, f"{name}.json")
        if name in done and (done[name].get("status") != "ok" or os.path.exists(mpath)):
            entry = done[name]
            trees.append(entry)
            n_resumed += 1
            if entry.get("status") == "ok":
                with open(mpath, encoding="utf-8") as fh:
                    _add(json.load(fh), name)
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
                try:
                    _write_text(mpath, canonical_json(manifest))
                except OSError as exc:
                    entry = {"tree": name, "status": "write_failed", "error": f"{type(exc).__name__}: {exc}"}
                    print(f"FAIL {name}: {type(exc).__name__}: {exc}", file=sys.stderr)
                else:
                    tl = _add(manifest, name)
                    elapsed = round(time.monotonic() - t0, 1)
                    entry = {
                        "tree": name, "status": "ok", "n_units": len(manifest["units"]), "n_rows": tl["rows"],
                        "n_effects": tl["n_effects"], "n_effects_unique": tl["n_effects_unique"],
                        "verdicts": dict(sorted(tl["verdicts"].items())), "budget_skipped": res.tree_budget_skipped,
                        "n_parse_failures": len(manifest.get("parse_failures") or []),
                        "n_truncations": len(manifest.get("truncations") or []),
                        "elapsed_s": elapsed,
                    }
                    print(f"  {name:48s} units={len(manifest['units']):4d} rows={tl['rows']:4d} {elapsed:6.1f}s")
        if entry.get("status") != "ok" and os.path.exists(mpath):
            os.remove(mpath)  # 前の run の manifest を今の結果として数えない（R5-r2-7）
        trees.append(entry)
        with open(progress_path, "a", encoding="utf-8", errors="backslashreplace") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")

    summary = {
        "_note": args.note or f"母集団 v2 の full scan（{args.label}）。scripts/scan_v2.py で作成。",
        "analyzer_commit": _git_head(),
        **impl,
        "max_depth": options.max_depth,
        "n_trees_resumed": n_resumed,
        "n_trees": len(trees),
        "n_units": n_units,
        "n_dangerous_units": n_dangerous,
        "n_rows": n_rows,
        "n_effects": n_effects,
        "n_effects_unique": n_effects_unique,
        "verdict_rows": dict(sorted(totals.items())),
        "trees": trees,
    }
    _write_text(os.path.join(out_dir, "summary.json"), json.dumps(summary, ensure_ascii=False, indent=1) + "\n")
    _write_text(os.path.join(out_dir, "contradictions.json"), json.dumps(
        {"_note": "CONTRADICTION（ユニット × (site, kind)。ユニットは unit_id と位置で区別）。手検証の候補表。"
                  "relpath / lineno は組の中の (relpath, lineno) の対の最小、全位置は locations。",
         "n": len(contradictions), "rows": contradictions}, ensure_ascii=False, indent=1) + "\n")
    print(f"\nwrote {out_dir}: units {n_units} / dangerous {n_dangerous} / rows {n_rows} / "
          f"verdicts {dict(totals)} / contradictions {len(contradictions)}")
    return 0


def _git(*args: str) -> str:
    import subprocess

    try:
        return subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True, check=True).stdout.strip()
    except Exception:  # noqa: BLE001
        return "unknown"


def _git_head() -> str:
    return _git("rev-parse", "HEAD")


if __name__ == "__main__":
    raise SystemExit(main())
