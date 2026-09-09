#!/usr/bin/env python3
"""付録 G と支配 mutant を採点し、期待値との一致表を出す。

    python scripts/check_gates.py            # 一致表だけ
    python scripts/check_gates.py --verbose  # 候補ゲートの内訳も
    python scripts/check_gates.py --json out.json

**学生の手検証の入口。** 表の各行は
`(期待 verdict, 実測 verdict, 期待 reason, 実測 reason, 期待 witness 行, 実測 witness 行)`
を並べる。不一致は理由つきで出す。

受け入れ条件（§2.5.6）:

* B3a = 支配のみを問う 8 mutant を **8/8** 撃破（どれも DOM と判定しないこと。
  m6 / m7 は加えて該当行が出力されること）
* B3b = 付録 G の G1–G15 を `(verdict, reason クラス, witness 行番号)` の
  3 つ組で **15/15**
"""

from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from authgap.gateharness import analyze_case  # noqa: E402


def load(sub: str) -> dict:
    with open(os.path.join(ROOT, sub, "expected.json"), encoding="utf-8") as fh:
        return json.load(fh)


def run_dir(sub: str) -> list[dict]:
    data = load(sub)
    directory = os.path.join(ROOT, sub)
    rows: list[dict] = []
    for case, spec in sorted(data["cases"].items()):
        not_entries = frozenset(spec.get("not_entries", ()))
        res = analyze_case(
            directory,
            case,
            spec["file"],
            spec.get("effect_line"),
            spec.get("coordinate", "occ"),
            not_entries,
        )
        row = {
            "case": case,
            "hole": spec.get("hole", ""),
            "expected": {
                "verdict": spec.get("verdict"),
                "not_verdict": spec.get("not_verdict"),
                "reason": spec.get("reason"),
                "grade": spec.get("grade"),
                "witness_line": spec.get("witness_line"),
                "requires_rows": spec.get("requires_rows", []),
            },
            "actual": res.to_json(),
        }
        row["ok"], row["why"] = judge(row)
        rows.append(row)
    return rows


def judge(row: dict) -> tuple[bool, list[str]]:
    exp, act = row["expected"], row["actual"]
    why: list[str] = []
    if exp["not_verdict"]:
        if act["verdict"] == exp["not_verdict"]:
            why.append(f"verdict が {exp['not_verdict']} になってはならない")
        for need in exp["requires_rows"]:
            if need not in act["rows"]:
                why.append(f"行 {need!r} が出ていない（{act['rows']}）")
        return (not why), why
    if act["verdict"] != exp["verdict"]:
        why.append(f"verdict: 期待 {exp['verdict']} / 実測 {act['verdict']}")
    if act["reason"] != exp["reason"]:
        why.append(f"reason: 期待 {exp['reason']} / 実測 {act['reason']}")
    if exp["witness_line"] is not None and act["witness_line"] != exp["witness_line"]:
        why.append(f"witness 行: 期待 L{exp['witness_line']} / 実測 {act['witness']}")
    if exp["grade"] is not None and act["grade"] != exp["grade"]:
        why.append(f"grade: 期待 {exp['grade']} / 実測 {act['grade']}")
    return (not why), why


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json")
    args = ap.parse_args()

    all_rows: dict[str, list[dict]] = {}
    exit_code = 0
    for sub, label in (
        ("fixtures/dominance_mutants", "B3a 支配 mutant"),
        ("fixtures/gates", "B3b 付録 G"),
    ):
        rows = run_dir(sub)
        all_rows[sub] = rows
        passed = sum(1 for r in rows if r["ok"])
        print(f"\n=== {label} ({sub}) : {passed}/{len(rows)} ===")
        for r in rows:
            mark = "OK " if r["ok"] else "NG "
            a = r["actual"]
            exp = r["expected"]
            want = exp["verdict"] or f"not {exp['not_verdict']}"
            got = f"{a['verdict']}({a['reason']})" if a["reason"] else str(a["verdict"])
            print(
                f"{mark}{r['case']:32s} want={want:9s} got={got:32s} "
                f"grade={str(a['grade']):5s} witness={str(a['witness']):26s} rows={a['rows']}"
            )
            for w in r["why"]:
                print(f"      -> {w}")
            if args.verbose:
                for c in (a["score"] or {}).get("candidates", []):
                    print(f"      cand {c}")
        if passed != len(rows):
            exit_code = 1

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(all_rows, fh, ensure_ascii=False, indent=2, sort_keys=True)
            fh.write("\n")
        print(f"\nwrote {args.json}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
