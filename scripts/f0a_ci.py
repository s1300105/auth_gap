#!/usr/bin/env python3
"""F0a の §10 関門の率に、木単位のブートストラップ信頼区間を付ける（D18）。

**なぜ要るか。** 効果サイトは木に集まる（1 本の木に数十サイト）。サイトを独立と
みなした区間は狭すぎる。標本設計の抽出単位は**木**なので、木を復元抽出して率を
計算し直す（クラスタ・ブートストラップ）。

率の定義は `scripts/f0a.py` と同じ:

* `in_tree_resolution_ratio_sites` = resolved サイト / 全サイト。サイト =
  (木, relpath, lineno, kind)。同一サイトの行の確度は opaque > remote > resolved で合流。
* `opaque_ratio_primary_slots_sites` = opaque / (resolved + opaque)、サイト × 主 slot 7 種。
  **remote は分母に入れない。**
* `validator_holding_ratio` = validator 形状を持つユニット / 全ユニット。

手続き: seed 20260914、反復 2000、パーセンタイル法の 95% 区間。解析した木
（`trees.jsonl` の status=analyzed。ユニット 0 件の木を含む）を抽出単位にする。

**関門の判定は点推定のまま**（§10 の手続きは変えない）。区間が閾値を跨ぐときは
「境界」と併記し、**点推定だけで合格 / 不合格を主張しない。**

使い方::

    python scripts/f0a_ci.py                      # 既定の run（存在するものだけ）
    python scripts/f0a_ci.py run2=evidence/f0a_run2
"""

from __future__ import annotations

import json
import os
import random
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from authgap.catalog.sinks import PRIMARY_SLOTS  # noqa: E402

OUT = os.path.join(ROOT, "docs", "f0a_ci.md")
SEED = 20260914
ITERATIONS = 2000

DEFAULT_RUNS = (
    ("run1", "evidence/f0a"),
    ("run1py312", "evidence/f0a_run1py312"),
    ("run2", "evidence/f0a_run2"),
    ("run2app", "evidence/f0a_run2app"),
    ("run3", "evidence/f0a_run3"),
    ("run4", "evidence/f0a_run4"),
)

#: `(率の名前, 向き, 閾値)`（`scripts/f0a.py` の §10 関門と同じ値）。
GATES = (
    ("in_tree_resolution_ratio_sites", ">=", 0.50),
    ("opaque_ratio_primary_slots_sites", "<=", 0.40),
    ("validator_holding_ratio", ">=", 0.05),
)

_RANK = {"resolved": 0, "remote": 1, "opaque": 2}


def _merge(old: str | None, new: str) -> str:
    return new if old is None or _RANK[new] > _RANK[old] else old


def per_tree(evidence_dir: str) -> dict[str, dict[str, dict]]:
    """母集団 → 木 → 集計（分子と分母）。"""
    trees: dict[str, dict[str, dict]] = defaultdict(dict)
    with open(os.path.join(evidence_dir, "trees.jsonl"), encoding="utf-8") as fh:
        for line in fh:
            t = json.loads(line)
            if t.get("status") == "analyzed":
                trees[t["population"]][t["tree"]] = {
                    "sites": {}, "slots": {}, "n_units": 0, "n_validator": 0,
                }
    with open(os.path.join(evidence_dir, "units.jsonl"), encoding="utf-8") as fh:
        for line in fh:
            u = json.loads(line)
            agg = trees[u["population"]].get(u["tree"])
            if agg is None:
                continue
            agg["n_units"] += 1
            if u["validator_shapes"]:
                agg["n_validator"] += 1
            for e in u["effects"]:
                site = (e["relpath"], e["lineno"], e["kind"])
                agg["sites"][site] = _merge(agg["sites"].get(site), e["resolution"])
                for slot, kind in e["slots"].items():
                    key = site + (slot,)
                    agg["slots"][key] = _merge(agg["slots"].get(key), kind)
    return trees


def _counts(agg: dict) -> tuple[int, int, int, int, int, int]:
    site_kinds = list(agg["sites"].values())
    primary = [k for (_r, _l, _k, slot), k in agg["slots"].items() if slot in PRIMARY_SLOTS]
    return (
        site_kinds.count("resolved"),
        len(site_kinds),
        primary.count("opaque"),
        primary.count("resolved") + primary.count("opaque"),
        agg["n_validator"],
        agg["n_units"],
    )


def _ratios(counts: list[tuple[int, ...]]) -> dict[str, float | None]:
    s = [sum(c[i] for c in counts) for i in range(6)]
    return {
        "in_tree_resolution_ratio_sites": s[0] / s[1] if s[1] else None,
        "opaque_ratio_primary_slots_sites": s[2] / s[3] if s[3] else None,
        "validator_holding_ratio": s[4] / s[5] if s[5] else None,
    }


def bootstrap(trees: dict[str, dict]) -> dict[str, tuple]:
    names = sorted(trees)
    counts = [_counts(trees[n]) for n in names]
    point = _ratios(counts)
    rng = random.Random(SEED)
    samples: dict[str, list[float]] = defaultdict(list)
    for _ in range(ITERATIONS):
        draw = [counts[rng.randrange(len(counts))] for _ in counts]
        for k, v in _ratios(draw).items():
            if v is not None:
                samples[k].append(v)
    out = {}
    for k, v in point.items():
        xs = sorted(samples[k])
        if v is None or not xs:
            out[k] = (v, None, None)
            continue
        lo = xs[int(0.025 * (len(xs) - 1))]
        hi = xs[int(0.975 * (len(xs) - 1))]
        out[k] = (v, lo, hi)
    return out


def _judge(op: str, thr: float, point, lo, hi) -> tuple[str, str]:
    if point is None:
        return "不明", "—"
    ok = point >= thr if op == ">=" else point <= thr
    if lo is None:
        return ("○" if ok else "×"), "—"
    straddles = lo < thr < hi
    return ("○" if ok else "×"), ("**境界**（区間が閾値を跨ぐ）" if straddles else "区間も同じ側")


def main(argv: list[str]) -> int:
    runs = [tuple(a.split("=", 1)) for a in argv] if argv else list(DEFAULT_RUNS)
    lines = [
        "# F0a の §10 関門の率と木単位ブートストラップ区間（D18）",
        "",
        "再現: `python scripts/f0a_ci.py`",
        "",
        f"抽出単位は木（`trees.jsonl` の analyzed）。seed {SEED}、反復 {ITERATIONS}、"
        "パーセンタイル法 95% 区間。**関門の判定は点推定のまま**（§10）。区間が閾値を",
        "跨ぐものは「境界」と書き、点推定だけで合格 / 不合格を主張しない。",
        "",
        "| run | 母集団 | 木 | 率 | 点推定 | 95% 区間 | 閾値 | 点推定の判定 | 区間 |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for label, rel in runs:
        d = rel if os.path.isabs(rel) else os.path.join(ROOT, rel)
        if not os.path.exists(os.path.join(d, "units.jsonl")):
            print(f"{d} が無いので {label} は飛ばす", file=sys.stderr)
            continue
        for pop, trees in sorted(per_tree(d).items()):
            res = bootstrap(trees)
            for name, op, thr in GATES:
                point, lo, hi = res[name]
                verdict, band = _judge(op, thr, point, lo, hi)
                ci = "—" if lo is None else f"[{lo:.1%}, {hi:.1%}]"
                pt = "—" if point is None else f"{point:.1%}"
                lines.append(
                    f"| {label} | {pop} | {len(trees)} | `{name}` | {pt} | {ci} | {op} {thr:.0%} | {verdict} | {band} |"
                )
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"\nwrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
