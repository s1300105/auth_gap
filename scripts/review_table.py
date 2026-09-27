"""添削の 3 観点（実行 / 設計 / 一般性）の判定を突き合わせて、所見の表を作る（`docs/review_plan.md` §4.2 / §4.3）。

    .venv/bin/python scripts/review_table.py --md docs/review_findings.md

入力: evidence/review/explore_*.json（所見）、exec_lens_*.json（実行）、verify_*.json（設計・一般性）。
生き残り = 3 観点のうち 2 観点以上を生き延びたもの（§4.2）。第 5 回以降の所見は事前登録の上限（4 回）の外なので
id に † を付ける（review_plan.md §7.3）。重大度は探索役・設計・一般性の 3 つの意見を
並べ、代表値はその中央値（high > medium > low の順で真ん中）。
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EV = os.path.join(ROOT, "evidence", "review")
SEV = {"high": 2, "medium": 1, "low": 0}
SEV_JA = {"high": "高", "medium": "中", "low": "低"}
DIR_JA = {"false_clean": "誤 clear", "false_alarm": "誤警報", "count_loss": "数え落とし",
          "nondeterminism": "非決定", "rule_mismatch": "規則との食い違い"}


def load():
    findings = {}
    for p in sorted(glob.glob(os.path.join(EV, "explore_*.json"))):
        for f in json.load(open(p))["findings"]:
            findings[f["id"]] = f
    execs = {}
    for p in sorted(glob.glob(os.path.join(EV, "exec_lens_*.json"))):
        for it in json.load(open(p))["items"]:
            execs[it["id"]] = it
    verifs = {}
    for p in sorted(glob.glob(os.path.join(EV, "verify_*.json"))):
        for v in json.load(open(p))["verdicts"]:
            verifs[v["id"]] = v
    return findings, execs, verifs


def median_sev(vals):
    vals = sorted((SEV[v] for v in vals if v in SEV), reverse=True)
    if not vals:
        return "?"
    inv = {v: k for k, v in SEV.items()}
    return inv[vals[len(vals) // 2]]


def rows(findings, execs, verifs):
    out = []
    for fid, f in findings.items():
        e = execs.get(fid)
        v = verifs.get(fid) or {}
        d = v.get("design")
        g = v.get("generality")
        lenses = {
            "exec": None if e is None else bool(e.get("reproduces")),
            "design": None if not d else not d["refuted"],
            "generality": None if not g else not g["refuted"],
        }
        judged = [x for x in lenses.values() if x is not None]
        complete = len(judged) == 3
        survived = sum(judged) >= 2 if complete else None
        sevs = [f["severity"]] + [x["severity_opinion"] for x in (d, g) if x]
        dirs = [f["direction"]] + [x["direction_opinion"] for x in (d, g) if x]
        fix_general = [x["fix_is_general"] for x in (d, g) if x]
        expected_ok = [x["expected_is_correct"] for x in (d, g) if x]
        out.append({
            "id": fid, "lane": f["lane"], "round": f.get("round"), "title": f["title"],
            "affects": f["affects"], "direction": Counter(dirs).most_common(1)[0][0],
            "directions": dirs, "severity": median_sev(sevs), "severities": sevs,
            "lenses": lenses, "complete": complete, "survived": survived,
            "fix_general": all(fix_general) if fix_general else None,
            "expected_ok": all(expected_ok) if expected_ok else None,
            "files": f["files"],
        })
    order = {"high": 0, "medium": 1, "low": 2, "?": 3}
    out.sort(key=lambda r: (order[r["severity"]], r["affects"] == "tooling", r["id"]))
    return out


def mark(x):
    return "—" if x is None else ("○" if x else "✗")


def md(rs):
    n = len(rs)
    comp = [r for r in rs if r["complete"]]
    surv = [r for r in comp if r["survived"]]
    dead = [r for r in comp if not r["survived"]]
    lines = ["# 添削の所見の表（3 観点の突き合わせ。`scripts/review_table.py` で再生成）", ""]
    lines.append(f"所見 {n} 件。3 観点そろった {len(comp)} 件のうち **生き残り {len(surv)} / 落ちた {len(dead)}**"
                 f"（未完 {n - len(comp)}）。生き残り = 2 観点以上を生き延びたもの（review_plan.md §4.2）。")
    lines.append("")
    c = Counter((r["severity"], r["affects"] == "tooling") for r in surv)
    lines.append("| 生き残りの重大度（代表値） | D1 / D2 に効く | 評価の道具 |")
    lines.append("|---|---|---|")
    for s in ("high", "medium", "low"):
        lines.append(f"| {SEV_JA[s]} | {c[(s, False)]} | {c[(s, True)]} |")
    lines.append("")
    lines.append("向き（生き残り）: " + "、".join(f"{DIR_JA[k]} {v}" for k, v in Counter(r["direction"] for r in surv).most_common()))
    lines.append("")
    lines.append("## 生き残った所見（重大度順）")
    lines.append("")
    lines.append("| id | 重大度（探索 / 設計 / 一般性） | 向き | 影響 | 実行 | 設計 | 一般性 | 直し方は一般に正しいか | 所見 |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for r in surv:
        sev = " / ".join(SEV_JA.get(s, s) for s in r["severities"])
        rid = r['id'] + ("†" if (r.get("round") or 0) > 4 else "")
        lines.append(f"| {rid} | **{SEV_JA[r['severity']]}**（{sev}） | {DIR_JA[r['direction']]} | {r['affects']} | "
                     f"{mark(r['lenses']['exec'])} | {mark(r['lenses']['design'])} | {mark(r['lenses']['generality'])} | "
                     f"{mark(r['fix_general'])} | {r['title'][:140].replace('|', '｜')} |")
    lines.append("")
    lines.append("## 落ちた所見（2 観点以上で反証）")
    lines.append("")
    lines.append("| id | 実行 | 設計 | 一般性 | 所見 |")
    lines.append("|---|---|---|---|---|")
    for r in dead:
        lines.append(f"| {r['id']} | {mark(r['lenses']['exec'])} | {mark(r['lenses']['design'])} | "
                     f"{mark(r['lenses']['generality'])} | {r['title'][:140].replace('|', '｜')} |")
    inc = [r for r in rs if not r["complete"]]
    if inc:
        lines.append("")
        lines.append("## 未完（観点が欠けている）")
        lines.append("")
        for r in inc:
            lines.append(f"- {r['id']}: " + ", ".join(f"{k}={mark(v)}" for k, v in r["lenses"].items()))
    lines.append("")
    lines.append("記号: ○ = その観点を生き延びた、✗ = 反証された、— = 未実施。判定の全文は `evidence/review/verify_*.json`、"
                 "再現は `evidence/review/exec_lens_*.json`、所見の本文は `evidence/review/explore_*.json`。"
                 "† = 第 5 回（事前登録の上限 4 回の外。review_plan.md §7.3）。")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--md")
    ap.add_argument("--json")
    a = ap.parse_args()
    findings, execs, verifs = load()
    rs = rows(findings, execs, verifs)
    if a.json:
        json.dump(rs, open(a.json, "w"), ensure_ascii=False, indent=1)
    text = md(rs)
    if a.md:
        open(a.md, "w").write(text)
    else:
        sys.stdout.write(text)
    comp = [r for r in rs if r["complete"]]
    print(f"findings {len(rs)} complete {len(comp)} survived {sum(1 for r in comp if r['survived'])}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
