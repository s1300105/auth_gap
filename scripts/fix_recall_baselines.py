"""D79 の同じ件で、既存の道具（HintLint・mcp-doctor）の再現率を測り、AuthGap と並べる（D80）。

    .venv/bin/python scripts/fix_recall_baselines.py run evidence/annotation_fixes_frame/items.json \\
        --hintlint <HintLint の clone> --mcp-doctor <mcp-doctor の実行ファイル> --out-dir <dir>
    .venv/bin/python scripts/fix_recall_baselines.py compare <dir> evidence/annotation_fixes_frame/recall_run1.json \\
        --out evidence/annotation_fixes_frame/baselines_run1.json --seed 20261005

`run` は木ごとの生出力を `<dir>/<道具>/<木>.json` に置く（続きから再開できる）。見つけたと数える規則は D80。
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fix_recall import _boot  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HL_RULE = {"D1": "HINTLINT-READONLY-001", "D2": "HINTLINT-DESTRUCTIVE-001", "D3": "HINTLINT-OPEN-WORLD-001"}


def _run(cmd: list[str], cwd: str | None, timeout: int) -> dict:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=cwd)
    except subprocess.TimeoutExpired:
        return {"_error": "timeout"}
    if not p.stdout.strip():
        return {"_error": f"no stdout (rc={p.returncode}): {p.stderr.strip()[-300:]}"}
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError as exc:
        return {"_error": f"bad json: {exc}"}


def cmd_run(a) -> int:
    items = json.load(open(a.items, encoding="utf-8"))["items"]
    trees = sorted({x["tree"] for x in items})
    for tool in ("hintlint", "mcp_doctor"):
        os.makedirs(os.path.join(a.out_dir, tool), exist_ok=True)
    for i, t in enumerate(trees, 1):
        path = os.path.join(ROOT, "corpus", t)
        for tool, cmd, cwd in (
            ("hintlint", ["node", os.path.join(a.hintlint, "src", "cli.js"), path, "--format", "json"], a.hintlint),
            ("mcp_doctor", [a.mcp_doctor, "--json", "--no-color", path], None),
        ):
            out = os.path.join(a.out_dir, tool, f"{t}.json")
            if os.path.exists(out):
                continue
            res = _run(cmd, cwd, a.timeout)
            with open(out, "w", encoding="utf-8") as fh:
                json.dump(res, fh, ensure_ascii=False)
        print(f"[{i}/{len(trees)}] {t}", flush=True)
    return 0


def _hl_found(raw: dict, tool: str, decl: str) -> dict[str, bool]:
    fs = [f for f in raw.get("findings") or [] if f.get("tool") == tool]
    rule = HL_RULE.get(decl)
    hit = [f for f in fs if rule and f.get("id") == rule]
    return {"strict": any(f.get("confidence") == "source-backed" for f in hit), "loose": bool(hit),
            "any_finding": bool(fs)}


def _md_found(raw: dict, tool: str, decl: str) -> bool:
    if decl != "D1":
        return False
    for t in raw.get("tools") or []:
        if t.get("name") == tool and any(i.get("check") == "annotation_mismatch" for i in t.get("issues") or []):
            return True
    return False


def cmd_compare(a) -> int:
    ag = json.load(open(a.authgap, encoding="utf-8"))
    d0 = {}
    if a.authgap_d0:  # 深さ 0（本体だけ）の同じ件の結果（D80 の追記）
        for x in json.load(open(a.authgap_d0, encoding="utf-8"))["items"]:
            d0[(x["group"], x["tool"], x["hint"])] = x["outcome"]
    rows = []
    for x in ag["items"]:
        hl = json.load(open(os.path.join(a.dir, "hintlint", f"{x['tree']}.json"), encoding="utf-8"))
        md = json.load(open(os.path.join(a.dir, "mcp_doctor", f"{x['tree']}.json"), encoding="utf-8"))
        r = {k: x[k] for k in ("group", "repo", "tree", "tool", "hint", "decl", "outcome")}
        r["authgap_contra"] = x["outcome"] == "矛"
        r["authgap_contra_or_unknown"] = x["outcome"] in ("矛", "不")
        r["in_authgap_denominator"] = x["outcome"] in ("矛", "不", "なし")
        r["authgap_d0_outcome"] = d0.get((x["group"], x["tool"], x["hint"]))
        if "_error" in hl:
            r["hintlint"] = "道具が失敗"
        else:
            r["hintlint"] = _hl_found(hl, x["tool"], x["decl"])
        r["mcp_doctor"] = "道具が失敗" if "_error" in md else _md_found(md, x["tool"], x["decl"])
        rows.append(r)

    def rate(rs: list[dict], fn) -> dict:
        ok = [r for r in rs if fn(r) is not None]
        k = sum(1 for r in ok if fn(r))
        return {"found": k, "n": len(ok), "rate": (k / len(ok)) if ok else None,
                "ci": _boot([(r["group"], int(bool(fn(r))), 1) for r in ok], a.seed, a.reps),
                "n_groups": len({r["group"] for r in ok})}

    measures = {
        "AuthGap 矛": lambda r: r["authgap_contra"],
        "AuthGap 矛+不": lambda r: r["authgap_contra_or_unknown"],
        "AuthGap 深さ0 矛": lambda r: None if r["authgap_d0_outcome"] is None else r["authgap_d0_outcome"] == "矛",
        "AuthGap 深さ0 矛+不": lambda r: None if r["authgap_d0_outcome"] is None else r["authgap_d0_outcome"] in ("矛", "不"),
        "HintLint 厳しい": lambda r: None if r["hintlint"] == "道具が失敗" else r["hintlint"]["strict"],
        "HintLint 緩い": lambda r: None if r["hintlint"] == "道具が失敗" else r["hintlint"]["loose"],
        "HintLint 参考（何かの finding）": lambda r: None if r["hintlint"] == "道具が失敗" else r["hintlint"]["any_finding"],
        "mcp-doctor": lambda r: None if r["mcp_doctor"] == "道具が失敗" else r["mcp_doctor"],
    }
    table: dict = {}
    for decl in ("D1", "D2", "D3", "D4"):
        rs = [r for r in rows if r["decl"] == decl]
        sub = [r for r in rs if r["in_authgap_denominator"]]
        table[decl] = {"all_items": {m: rate(rs, f) for m, f in measures.items()},
                       "authgap_denominator": {m: rate(sub, f) for m, f in measures.items()},
                       "tool_failed": {"hintlint": sum(r["hintlint"] == "道具が失敗" for r in rs),
                                       "mcp_doctor": sum(r["mcp_doctor"] == "道具が失敗" for r in rs)}}
    out = {"_note": "fix_recall_baselines.py compare（D80）。区間は群を単位にした bootstrap、群が 10 未満なら出さない",
           "seed": a.seed, "reps": a.reps, "by_decl": table, "items": rows}
    json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for d, t in table.items():
        print(f"== {d}  道具の失敗 {t['tool_failed']}")
        for part in ("all_items", "authgap_denominator"):
            print(f"  [{part}]", "  ".join(f"{m}: {v['found']}/{v['n']}" for m, v in t[part].items()))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("items")
    r.add_argument("--hintlint", required=True)
    r.add_argument("--mcp-doctor", required=True)
    r.add_argument("--out-dir", required=True)
    r.add_argument("--timeout", type=int, default=600)
    c = sub.add_parser("compare")
    c.add_argument("dir")
    c.add_argument("authgap")
    c.add_argument("--authgap-d0", help="深さ 0 の fix_recall.py evaluate の出力（D80 の追記）")
    c.add_argument("--out", required=True)
    c.add_argument("--seed", type=int, required=True)
    c.add_argument("--reps", type=int, default=10000)
    a = ap.parse_args()
    return cmd_run(a) if a.cmd == "run" else cmd_compare(a)


if __name__ == "__main__":
    sys.exit(main())
