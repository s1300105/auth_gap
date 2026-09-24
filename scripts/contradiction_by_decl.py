#!/usr/bin/env python3
"""CONTRADICTION を宣言ごとに数え、判定原理を 1 つずつ反対側にした感度分析を出す（D56）。

**判定の規則はここに無い**（`authgap/dparse.py: contradiction_findings`）。この script は
manifest の行の注記（`contradiction:<宣言>` / `contradiction_unknown:<宣言>:<理由>`）を読むだけ。

    .venv/bin/python scripts/contradiction_by_decl.py evidence/scan_v2_run13 --md docs/contradiction_by_decl.md

数え方（CLAUDE.md 規則 3）:

* 単位は `compare_scans.py` と同じ **(木, ユニットの qualname, site, kind)**。宣言ごとに、その組の
  どれかの行に `contradiction:<宣言>` があれば「矛」、無くて `contradiction_unknown:<宣言>:…`
  があれば「不」（理由は組の中の理由の集合）。
* D1 / D2 は事前登録済みの主指標、D3 / D4 は**探索的**（`docs/contradiction_principles.md` §6）。
  **合算しない。**
* 感度分析: 理由のコードは §7 の判定表のどの分岐を通ったかを表すので、原理を反対側にしたときの
  結果は注記から正確に決まる（再走査は要らない）:
  - 1-i-a（永続する設定を含めない）: 理由 `db_persistent` を宣言内に
  - 1-ii-a（リモートの状態を含めない）: D1 / D2 の理由 `net_*` を宣言内に
  - 2-b（不明を矛盾に倒す）/ 2-c（宣言内に倒す）: 「不」をすべて矛 / 内に
  - 3-b（モデル由来の値を能力として読まない）: 理由に `model` を含む「矛」を「不」に
  - 4-b（破壊性の 2 つだけ）: D3 / D4 を数えない
"""

from __future__ import annotations

import argparse
import collections
import json
import os

DECLS = ("D1", "D2", "D3", "D4")


def load_reasons(run_dir: str) -> dict:
    """`{(木, qualname, site, kind): {宣言: {(status, reason)}}}` を行の注記から作る。"""
    out: dict = collections.defaultdict(lambda: collections.defaultdict(set))
    for fn in sorted(os.listdir(run_dir)):
        if not fn.startswith("v2-") or not fn.endswith(".json"):
            continue
        t = fn[:-5]
        for u in json.load(open(os.path.join(run_dir, fn), encoding="utf-8"))["units"]:
            q = u["unit"]["qualname"]
            for r in u.get("rows", []):
                key = (t, q, r["site"], r["kind"])
                for n in r.get("notes", []):
                    if n.startswith("contradiction_reason:"):
                        _, d, reason = n.split(":", 2)
                        out[key][d].add(("contradiction", reason))
                    elif n.startswith("contradiction_unknown:"):
                        _, d, reason = n.split(":", 2)
                        out[key][d].add(("unknown", reason))
    return out


def apply_flip(findings: set, decl: str, flip: str | None) -> str:
    """原理を 1 つ反対側にしたときの、宣言 1 つ分の結果（矛 / 不 / 内）。"""
    res = set()
    for status, reason in findings:
        s = "矛" if status == "contradiction" else "不"
        if flip == "1-i-a" and reason == "db_persistent":
            continue
        if flip == "1-ii-a" and decl in ("D1", "D2") and reason.startswith("net_"):
            continue
        if flip == "3-b" and s == "矛" and "model" in reason:
            s = "不"
        if flip == "2-b" and s == "不":
            s = "矛"
        if flip == "2-c" and s == "不":
            continue
        res.add(s)
    if flip == "4-b" and decl in ("D3", "D4"):
        return "内"
    return "矛" if "矛" in res else ("不" if "不" in res else "内")


FLIPS = [(None, "採った原理（1-i b / 1-ii b / 2 a / 3 a / 4 a）"),
         ("1-i-a", "1-i を a に（永続する設定を含めない）"),
         ("1-ii-a", "1-ii を a に（リモートの状態を含めない）"),
         ("2-b", "2 を b に（不明を矛盾に倒す）"),
         ("2-c", "2 を c に（不明を宣言内に倒す）"),
         ("3-b", "3 を b に（モデル由来の値を能力として読まない）"),
         ("4-b", "4 を b に（破壊性の 2 つだけ）")]


def to_md(run_dir: str) -> str:
    rs = load_reasons(run_dir)
    o = ["# CONTRADICTION の宣言ごとの件数と、判定原理の感度分析（D56）", "",
         f"再現: `python scripts/contradiction_by_decl.py {os.path.relpath(run_dir)}`", "",
         "単位は (木, ユニット, site, kind)。**D1 / D2 は事前登録済みの主指標、D3 / D4 は探索的。合算しない。**", ""]
    o += ["## 採った原理での件数", "", "| 宣言 | 矛 | 不 | 矛の木 |", "|---|---|---|---|"]
    for d in DECLS:
        c = collections.Counter()
        trees = set()
        for key, per in rs.items():
            s = apply_flip(per.get(d, set()), d, None)
            c[s] += 1
            if s == "矛":
                trees.add(key[0])
        o.append(f"| {d} | {c['矛']} | {c['不']} | {len(trees)} |")
    o += ["", "## 理由ごとの内訳（採った原理）", "", "| 宣言 | 結果 | 理由 | 組 |", "|---|---|---|---|"]
    rc = collections.Counter()
    for per in rs.values():
        for d, fs in per.items():
            for status, reason in fs:
                rc[(d, "矛" if status == "contradiction" else "不", reason)] += 1
    for (d, s, r), n in sorted(rc.items()):
        o.append(f"| {d} | {s} | `{r}` | {n} |")
    o += ["", "## 感度分析（原理を 1 つずつ反対側にする）", "",
          "| 変えた原理 | D1 矛 | D1 不 | D2 矛 | D2 不 | **D1+D2 矛** | D3 矛 | D3 不 | D4 矛 | D4 不 |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for flip, label in FLIPS:
        cnt = {d: collections.Counter() for d in DECLS}
        main = set()
        for key, per in rs.items():
            for d in DECLS:
                s = apply_flip(per.get(d, set()), d, flip)
                cnt[d][s] += 1
                if s == "矛" and d in ("D1", "D2"):
                    main.add(key)
        o.append(f"| {label} | {cnt['D1']['矛']} | {cnt['D1']['不']} | {cnt['D2']['矛']} | {cnt['D2']['不']} | "
                 f"**{len(main)}** | {cnt['D3']['矛']} | {cnt['D3']['不']} | {cnt['D4']['矛']} | {cnt['D4']['不']} |")
    o.append("")
    return "\n".join(o)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run")
    ap.add_argument("--md")
    args = ap.parse_args(argv)
    md = to_md(args.run)
    if args.md:
        with open(args.md, "w", encoding="utf-8") as fh:
            fh.write(md + "\n")
    print(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
