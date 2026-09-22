#!/usr/bin/env python3
"""HintLint（先行研究 R1）と AuthGap を母集団 v2 の同じ木で突き合わせる。

**入口を揃えた比較ではない。** `scripts/codeql_fair.py` と違い、HintLint は MCP ツールを
自分で抽出するので、AuthGap と同じ入口集合を渡す手段が無い。**したがって「どちらが多く
見つけたか」ではなく「何が見えて何が見えないか」を見る比較である。**

公平性のために先に書いておく（`docs/related_work.md` R1 と D40）:

1. **HintLint は TypeScript / JavaScript も対象**で、そちらには到達解析
   （`src/evidence/typescript-reachability.js`）がある。母集団 v2 は Python の MCP サーバ
   だけなので、**この比較は HintLint の Python 経路だけを見ている。** 設計全体の評価ではない。
2. **規則の範囲が違う。** HintLint は `OPEN-WORLD-001` と 5 つの flow 規則を持ち、AuthGap は
   `openWorldHint` を実装していない。**比較できるのは readOnly / destructive の矛盾だけ**で、
   それ以外は「向こうにしかない」として別に数える。
3. **目的が違う。** HintLint は CI に載せる linter で、精度を優先して不確実な事例を落とす
   （`confidence: needs-review` は build を落とさない）。AuthGap は測定研究で、解決できな
   かったものを opaque として残し率を報告する。**どちらが正しいという比較ではない。**
4. **数えている現象が違う。** HintLint の `DESTRUCTIVE-001` は `destructiveHint` が**無い**
   ことで発火する。AuthGap の CONTRADICTION は明示の宣言 D に**反する**ことを要求する。
   run1 の実測では比較可 65 件のうち **61 件が `declared_annotations == {}`**（宣言なし）で、
   **真に比較できたのは 4 件**だった。件数の大小を並べてはいけない。
5. **AuthGap 側の欠測を先に申告する。** `v2-david-li0406__meta-skill-evloving` は
   180 秒の tree budget で打ち切られユニット 0 件（`budget_skipped: 716`）、
   `v2-mcparmory__registry` は `@mcp.tool` 10,170 個のうち 9,524 個が `AST_NODE_CAP` で
   切られたファイルの中にある（`docs/open_questions.md` O21）。**この 2 木は比較として
   成立していない。**

出力は `evidence/hintlint_<label>/`:

* `<tree>.json`   … HintLint の生出力（`.gitignore` で追跡しない）
* `summary.json`  … 木ごとの件数と、AuthGap（`scan_v2_run4`）との対比

**結果の読み方は `docs/related_work.md` の R1 節と `docs/decisions.md` D40 にある。**

    node --version                     # HintLint は Node 製
    .venv/bin/python scripts/hintlint_compare.py --hintlint /home/user/complira/hintlint --label run1
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#: AuthGap 側で「宣言に反する」と判定した verdict。比較の対象はこれだけ。
AUTHGAP_VERDICT = "CONTRADICTION"
#: HintLint 側で対応する finding。**flow 系と OPEN-WORLD は対応物が無いので別に数える。**
HINTLINT_COMPARABLE = {"HINTLINT-READONLY-001", "HINTLINT-DESTRUCTIVE-001"}


def run_hintlint(hintlint_dir: str, tree: str, timeout: float) -> dict | None:
    cli = os.path.join(hintlint_dir, "src", "cli.js")
    try:
        p = subprocess.run(
            ["node", cli, tree, "--format", "json"],
            capture_output=True, text=True, timeout=timeout, cwd=hintlint_dir,
        )
    except subprocess.TimeoutExpired:
        return {"_error": "timeout"}
    if not p.stdout.strip():
        return {"_error": f"no stdout (rc={p.returncode}): {p.stderr.strip()[:200]}"}
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError as exc:
        return {"_error": f"bad json: {exc}"}


def authgap_counts(scan_dir: str) -> dict[str, dict]:
    """AuthGap の full scan から、木ごとの ユニット数 / 危険ユニット / CONTRADICTION を出す。"""
    out: dict[str, dict] = {}
    for fn in sorted(os.listdir(scan_dir)):
        if not fn.endswith(".json") or fn in ("summary.json", "contradictions.json"):
            continue
        with open(os.path.join(scan_dir, fn), encoding="utf-8") as fh:
            man = json.load(fh)
        pairs = set()
        dangerous = 0
        for u in man.get("units", []):
            if u.get("effects"):
                dangerous += 1
            for r in u.get("rows", []):
                if AUTHGAP_VERDICT in r.get("verdicts", []):
                    pairs.add((u["unit"]["unit_id"], r["site"], r["kind"]))
        out[fn[:-5]] = {
            "units": len(man.get("units", [])),
            "dangerous_units": dangerous,
            "contradictions": len(pairs),
        }
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--hintlint", required=True, help="HintLint の clone のパス")
    ap.add_argument("--label", required=True)
    ap.add_argument("--sample", default=os.path.join(ROOT, "evidence", "population_v2", "sample_v2_mcp.json"))
    ap.add_argument("--authgap-scan", default=os.path.join(ROOT, "evidence", "scan_v2_run4"))
    ap.add_argument("--timeout", type=float, default=600.0)
    args = ap.parse_args(argv)

    cli = os.path.join(args.hintlint, "src", "cli.js")
    if not os.path.exists(cli):
        raise SystemExit(f"HintLint の cli.js が無い: {cli}")
    head = subprocess.run(["git", "-C", args.hintlint, "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()

    ag = authgap_counts(args.authgap_scan)
    targets = json.load(open(args.sample, encoding="utf-8"))["targets"]
    out_dir = os.path.join(ROOT, "evidence", f"hintlint_{args.label}")
    os.makedirs(out_dir, exist_ok=True)

    rows: list[dict] = []
    tot = collections.Counter()
    by_rule: collections.Counter = collections.Counter()
    for t in targets:
        name = t["name"]
        tree = os.path.join(ROOT, "corpus", name)
        if not os.path.isdir(tree):
            rows.append({"tree": name, "status": "missing"})
            continue
        t0 = time.monotonic()
        res = run_hintlint(args.hintlint, tree, args.timeout)
        elapsed = round(time.monotonic() - t0, 1)
        if res is None or "_error" in (res or {}):
            rows.append({"tree": name, "status": "failed", "error": (res or {}).get("_error"), "elapsed_s": elapsed})
            print(f"FAIL {name}: {(res or {}).get('_error')}", file=sys.stderr)
            continue
        with open(os.path.join(out_dir, f"{name}.json"), "w", encoding="utf-8") as fh:
            json.dump(res, fh, ensure_ascii=False)
        s = res.get("summary", {})
        findings = res.get("findings", [])
        rule_counts = collections.Counter(f.get("id", "?") for f in findings)
        by_rule.update(rule_counts)
        comparable = sum(v for k, v in rule_counts.items() if k in HINTLINT_COMPARABLE)
        a = ag.get(name, {})
        rows.append({
            "tree": name, "status": "ok", "elapsed_s": elapsed,
            "hintlint": {
                "tools_scanned": s.get("tools_scanned"),
                "handlers_resolved": s.get("handlers_resolved"),
                "annotations_present": s.get("annotations_present"),
                "unsupported_patterns": s.get("unsupported_patterns"),
                "coverage_status": s.get("coverage_status"),
                "findings": len(findings),
                "comparable_findings": comparable,
                "by_rule": dict(sorted(rule_counts.items())),
            },
            "authgap": a,
        })
        tot["hl_tools"] += s.get("tools_scanned") or 0
        tot["hl_findings"] += len(findings)
        tot["hl_comparable"] += comparable
        tot["ag_units"] += a.get("units", 0)
        tot["ag_dangerous"] += a.get("dangerous_units", 0)
        tot["ag_contradictions"] += a.get("contradictions", 0)
        print(f"  {name:48s} HL tools={s.get('tools_scanned'):>4} find={len(findings):>3} "
              f"(比較可 {comparable:>3}) | AG units={a.get('units', 0):>4} contra={a.get('contradictions', 0):>3} {elapsed:6.1f}s")

    summary = {
        "_note": "HintLint（R1）と AuthGap の突き合わせ。**入口を揃えた比較ではない**（script の docstring）。",
        "hintlint_commit": head,
        "authgap_scan": os.path.relpath(args.authgap_scan, ROOT),
        "n_trees": len(rows),
        "n_ok": sum(1 for r in rows if r.get("status") == "ok"),
        "totals": dict(tot),
        "hintlint_by_rule": dict(sorted(by_rule.items())),
        "comparable_rules": sorted(HINTLINT_COMPARABLE),
        "trees": rows,
    }
    with open(os.path.join(out_dir, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print(f"\nwrote {out_dir}")
    print(f"  HintLint: ツール {tot['hl_tools']} / finding {tot['hl_findings']}（比較可 {tot['hl_comparable']}）")
    print(f"  AuthGap : ユニット {tot['ag_units']} / 危険 {tot['ag_dangerous']} / CONTRADICTION {tot['ag_contradictions']}")
    print(f"  HintLint の規則別: {dict(sorted(by_rule.items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
