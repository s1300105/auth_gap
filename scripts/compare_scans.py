#!/usr/bin/env python3
"""母集団 v2 の full scan 2 本を突き合わせ、**変更の前後を両方出す**。

CLAUDE.md の約束「仕様書と実データが食い違ったら実データを採り、仕様書の値も残す」と
`docs/preregistration.md` の逸脱記録に要る数字を作る。**解析器を変えたあとに
run を取り直したら必ずこれを通す。**

見るもの:

* 木ごと・全体の **ユニット / 効果行 / verdict の件数**の増減。
* **消えたユニット**（回帰の疑い。増えるより消える方が重い）。
* **CONTRADICTION の増減**を (木, ユニットの relpath:行, qualname, site, kind, **宣言**) の集合差で出し、宣言ごとに
  分けて数える（D64 / U50。以前は位置と宣言が鍵に無く、別モジュールの同名ツールの矛が 1 件に潰れ、同じ位置に
  D3 / D4 の矛が残ると消えた D1 / D2 の矛が見えなかった）。注記の無い CONTRADICTION 行は宣言 `?` で残す。
* manifest の集合は `summary.json` の ok の木で決める（`scripts/runlib.py`）。2 つの run の Python の版が違えば
  警告する（unit_id は既定値を `ast.unparse` した文字列を含み、処理系で変わりうる。R5-r3-4）。
* 効果の件数は、生の行数と一意の行数（バイト同一の複製を 1 本に数えたもの。R4-r1-8 / O18）を併記する。
* **slot の主体の分布**（`OP` / `MODEL`）と「root はあるのに主体が OP」の件数。
  D44 が直したのはここなので、率の変化を明示する。

    .venv/bin/python scripts/compare_scans.py evidence/scan_v2_run4 evidence/scan_v2_run5
    .venv/bin/python scripts/compare_scans.py evidence/scan_v2_run4 evidence/scan_v2_run5 --md docs/scan_v2_run5_diff.md
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from runlib import load_manifest, print_warnings, row_decls, run_manifests, unit_key  # noqa: E402


def python_warning(sa: dict, sb: dict) -> str | None:
    """2 つの run の summary.json の Python の版（major.minor）が違えば警告の文を返す。記録が無ければ None。"""
    pa, pb = sa.get("python"), sb.get("python")
    if not pa or not pb:
        return None
    if pa.split(".")[:2] != pb.split(".")[:2]:
        return (f"Python の版が違う（{pa} / {pb}）。unit_id は処理系で変わりうるので、ユニットの消失・増加は"
                "処理系の差でありうる（R5-r3-4）")
    return None


def load(evidence_dir: str) -> dict:
    """1 つの run から、比較に要る形だけを取り出す。"""
    units: dict[str, dict] = {}
    collisions: list[str] = []
    contradictions: set[tuple] = set()
    verdict_rows: collections.Counter = collections.Counter()
    prin: collections.Counter = collections.Counter()
    n_rows = n_effects = n_units_raw = 0
    uniq_effects: set[str] = set()
    manifests, warnings = run_manifests(evidence_dir)
    for tree, path in manifests:
        man = load_manifest(path)
        for u in man.get("units", []):
            # **鍵に qualname と位置を混ぜる。** `unit_id` は木の中で一意ではない
            # （`docs/open_questions.md` O13）ので、`unit_id` だけを鍵にすると
            # 衝突したユニットが dict で潰れ、**その分の変化が比較から消える**
            # （CLAUDE.md「同一キーの衝突で MODEL 行を落とさない」）。
            # run4 では 4 件が潰れていた。
            un = u["unit"]
            uid = f'{tree}|{un["unit_id"]}|{un["qualname"]}|{un.get("relpath")}:{un.get("lineno")}'
            if uid in units:
                collisions.append(uid)
            n_units_raw += 1
            n_effects += len(u.get("effects", []))
            for e in u.get("effects", []):
                uniq_effects.add(uid + "|" + json.dumps(e, sort_keys=True, ensure_ascii=False))
                for v in (e.get("slots") or {}).values():
                    if not isinstance(v, dict):
                        continue
                    prin[(v.get("prin"), bool(v.get("roots")))] += 1
            vs: collections.Counter = collections.Counter()
            uk = unit_key(tree, un)
            for r in u.get("rows", []):
                n_rows += 1
                for v in r.get("verdicts", []):
                    vs[v] += 1
                    verdict_rows[v] += 1
                if "CONTRADICTION" in r.get("verdicts", []):
                    for d in row_decls(r):
                        contradictions.add((uk[0], f"{uk[1]}:{uk[2]}", uk[3], r["site"], r["kind"], d))
            units[uid] = {"tree": tree, "qualname": u["unit"]["qualname"],
                          "n_effects": len(u.get("effects", [])), "verdicts": dict(vs)}
    summary = {}
    spath = os.path.join(evidence_dir, "summary.json")
    if os.path.exists(spath):
        with open(spath, encoding="utf-8") as fh:
            summary = json.load(fh)
    return {"units": units, "contradictions": contradictions, "verdict_rows": verdict_rows,
            "prin": prin, "n_rows": n_rows, "n_effects": n_effects, "n_effects_unique": len(uniq_effects),
            "n_units_raw": n_units_raw, "collisions": collisions, "warnings": warnings, "summary": summary}


def to_md(a_dir: str, b_dir: str, a: dict, b: dict) -> str:
    o: list[str] = []
    an, bn = os.path.basename(a_dir), os.path.basename(b_dir)
    o.append(f"# full scan の突き合わせ: `{an}` → `{bn}`")
    o.append("")
    o.append(f"再現: `python scripts/compare_scans.py {os.path.relpath(a_dir, ROOT)} "
             f"{os.path.relpath(b_dir, ROOT)}`")
    o.append("")
    o.append("**変更の前後を両方出す**（CLAUDE.md の約束）。この表の値は逸脱として")
    o.append("`docs/preregistration.md` に記録する。")
    o.append("")
    o.append("## 全体")
    o.append("")
    o.append(f"| 項目 | {an} | {bn} | 差 |")
    o.append("|---|---|---|---|")
    for label, ka, kb in [("ユニット（manifest の生の件数）", a["n_units_raw"], b["n_units_raw"]),
                          ("ユニット（比較の鍵で数えたもの）", len(a["units"]), len(b["units"])),
                          ("効果（生の行数）", a["n_effects"], b["n_effects"]),
                          ("効果（一意の行数。バイト同一の複製を 1 本に）", a["n_effects_unique"], b["n_effects_unique"]),
                          ("行", a["n_rows"], b["n_rows"])]:
        o.append(f"| {label} | {ka} | {kb} | {kb - ka:+d} |")
    for v in sorted(set(a["verdict_rows"]) | set(b["verdict_rows"])):
        x, y = a["verdict_rows"][v], b["verdict_rows"][v]
        o.append(f"| `{v}` の行 | {x} | {y} | {y - x:+d} |")
    o.append("")
    if a["collisions"] or b["collisions"]:
        o.append(f"**鍵の衝突**（`unit_id` + qualname + 位置でも同じになったユニット）: "
                 f"{an} {len(a['collisions'])} 件 / {bn} {len(b['collisions'])} 件。"
                 f"この分は比較から落ちている（`docs/open_questions.md` O13）。")
        o.append("")

    warn = [f"{an}: {w}" for w in a["warnings"]] + [f"{bn}: {w}" for w in b["warnings"]]
    pw = python_warning(a["summary"], b["summary"])
    if pw:
        warn.append(pw)
    if warn:
        o.append("**警告**:")
        o.append("")
        for w in warn:
            o.append(f"- {w}")
        o.append("")

    o.append("## CONTRADICTION（ユニット × site × kind × 宣言。D1〜D4 は 4 つとも主指標、D62）")
    o.append("")
    added = sorted(b["contradictions"] - a["contradictions"])
    removed = sorted(a["contradictions"] - b["contradictions"])
    decls = sorted({c[-1] for c in a["contradictions"] | b["contradictions"]})
    o.append(f"| | 計 | {' | '.join(decls)} |")
    o.append("|---|---|" + "---|" * len(decls))

    def _row(label, xs):
        c = collections.Counter(x[-1] for x in xs)
        return f"| {label} | {len(xs)} | " + " | ".join(str(c[d]) for d in decls) + " |"

    o.append(_row(an, a["contradictions"]))
    o.append(_row(bn, b["contradictions"]))
    o.append(_row("**増えた**", added))
    o.append(_row("**消えた**（回帰の疑い）", removed))
    o.append("")
    if removed:
        o.append("### 消えた CONTRADICTION — **1 件ずつ理由を確かめること**")
        o.append("")
        for t, pos, q, site, kind, d in removed:
            o.append(f"- `{t}` / `{q}`（{pos}）/ `{kind}@{site}` / {d}")
        o.append("")
    if added:
        o.append("### 増えた CONTRADICTION")
        o.append("")
        for t, pos, q, site, kind, d in added:
            o.append(f"- `{t}` / `{q}`（{pos}）/ `{kind}@{site}` / {d}")
        o.append("")

    o.append("## slot の主体（D44 が直した箇所）")
    o.append("")
    o.append(f"| 主体 / root | {an} | {bn} | 差 |")
    o.append("|---|---|---|---|")
    for key in sorted(set(a["prin"]) | set(b["prin"]), key=str):
        x, y = a["prin"][key], b["prin"][key]
        label = f"`{key[0]}` / root {'あり' if key[1] else 'なし'}"
        o.append(f"| {label} | {x} | {y} | {y - x:+d} |")
    ax = a["prin"][("OP", True)]
    bx = b["prin"][("OP", True)]
    o.append("")
    o.append(f"**「root はあるのに主体が OP」**（D44 が矛盾と呼んだ状態）: "
             f"{ax} → {bx}（{bx - ax:+d}）。")
    o.append("")

    o.append("## 消えたユニット / 増えたユニット")
    o.append("")
    gone = sorted(set(a["units"]) - set(b["units"]))
    new = sorted(set(b["units"]) - set(a["units"]))
    o.append(f"消えた {len(gone)} / 増えた {len(new)}。")
    o.append("")
    o.append("**ユニットが消えるのは入口の認識が変わったということなので、解析器の変更で"
             "起きたなら回帰である。** 1 件ずつ確かめる。")
    o.append("")
    for uid in gone[:40]:
        o.append(f"- 消えた: `{uid}`（{a['units'][uid]['qualname']}）")
    for uid in new[:40]:
        o.append(f"- 増えた: `{uid}`（{b['units'][uid]['qualname']}）")
    o.append("")

    o.append("## 効果数が変わったユニット（上位 20）")
    o.append("")
    both = set(a["units"]) & set(b["units"])
    delta = [(b["units"][u]["n_effects"] - a["units"][u]["n_effects"], u) for u in both]
    delta = [d for d in delta if d[0] != 0]
    delta.sort(key=lambda d: (-abs(d[0]), d[1]))
    o.append(f"変わったユニット: {len(delta)}")
    o.append("")
    for d, u in delta[:20]:
        o.append(f"- `{u}`: {a['units'][u]['n_effects']} → {b['units'][u]['n_effects']}（{d:+d}）")
    o.append("")
    return "\n".join(o)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("before")
    ap.add_argument("after")
    ap.add_argument("--md")
    args = ap.parse_args(argv)
    a_dir = args.before if os.path.isabs(args.before) else os.path.join(ROOT, args.before)
    b_dir = args.after if os.path.isabs(args.after) else os.path.join(ROOT, args.after)
    for d in (a_dir, b_dir):
        if not os.path.isdir(d):
            raise SystemExit(f"{d} が無い")
    la, lb = load(a_dir), load(b_dir)
    for w in la["warnings"]:
        print_warnings([w], os.path.basename(a_dir))
    for w in lb["warnings"]:
        print_warnings([w], os.path.basename(b_dir))
    md = to_md(a_dir, b_dir, la, lb)
    print(md)
    if args.md:
        p = args.md if os.path.isabs(args.md) else os.path.join(ROOT, args.md)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(md)
        print(f"\nwrote {args.md}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
