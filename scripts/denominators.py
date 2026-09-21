#!/usr/bin/env python3
"""事前登録した分母（`docs/preregistration.md` §2）で率を計算する。

**この スクリプトは分母の定義を固定するためのものであり、値を選ぶためのものではない。**
`docs/preregistration.md` が定めた**すべての**分母の組み合わせを出力する。
片方だけを出力する経路は意図的に用意していない（§3 の併記規則）。

入力は `evidence/<run>/units.jsonl`（コミット済みの証拠）だけで、解析器を再実行しない。
したがって解析器を直した後は evidence を取り直してからこれを当てる。

    python3 scripts/denominators.py evidence/f0a_run6
    python3 scripts/denominators.py evidence/f0a_run6 --json

`path_class` の規則は `docs/preregistration.md` §2.3 が唯一の定義点であり、
本ファイルはその規則を機械可読にしたものである。**規則を変えるときは先に
preregistration.md を直し、逸脱として §5 に記録する。**
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

#: §2.3 の `path_class` 規則。**ディレクトリ名の構文規則のみ**で判定し、
#: ファイルの中身を見ない（測定集合を見て調整できないようにするため）。
#: 相対パスの**いずれかの構成要素**がこの集合に一致したら `non_src`。
NON_SRC_DIRS: frozenset[str] = frozenset(
    {
        "test",
        "tests",
        "testing",
        "script",
        "scripts",
        "example",
        "examples",
        "sample",
        "samples",
        "doc",
        "docs",
        "benchmark",
        "benchmarks",
        "demo",
        "demos",
    }
)

#: §2.1 の母集団。出力順もこれで固定する（再現時の diff を安定させるため）。
POPULATIONS: tuple[str, ...] = ("mcp_server", "tool_package", "app")

#: §2.2 のユニット分母。キーは preregistration.md の表と一致させる。
UNIT_DENOMS: tuple[str, ...] = ("all_units", "dangerous", "dangerous_fp_excluded", "dangerous_non_net")

#: §2.3 のパス分母。
PATH_DENOMS: tuple[str, ...] = ("all_paths", "src_only")

#: §2.2 の関門。**閾値は仕様書 §10 の値で、本文書では動かさない。**
VALIDATOR_GATE = 0.05


def path_class(relpath: str) -> str:
    """§2.3: 相対パスの構成要素が `NON_SRC_DIRS` に一致したら `non_src`。"""
    parts = re.split(r"[/\\]", relpath or "")
    return "non_src" if any(p.lower() in NON_SRC_DIRS for p in parts[:-1]) else "src"


def load_units(run_dir: Path) -> list[dict]:
    path = run_dir / "units.jsonl"
    if not path.exists():
        raise SystemExit(f"units.jsonl が無い: {path}")
    with path.open(encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def select(units: list[dict], population: str, path_denom: str, unit_denom: str) -> list[dict]:
    """§2 の分母をそのまま適用する。**ここ以外で絞り込まない。**"""
    rows = [u for u in units if u.get("population") == population]
    if path_denom == "src_only":
        rows = [u for u in rows if path_class(u.get("relpath", "")) == "src"]
    if unit_denom == "dangerous":
        rows = [u for u in rows if u.get("dangerous")]
    elif unit_denom == "dangerous_fp_excluded":
        # `dangerous_fp_excluded` は「危険効果があり、かつ効果検出器の偽陽性クラス
        # （非 DB の `.execute()` 等）を除いても残る」ユニット。run6 時点では
        # `dangerous` と恒等（preregistration.md §2.2 の注記を参照）。
        rows = [u for u in rows if u.get("dangerous") and u.get("dangerous_fp_excluded", True)]
    elif unit_denom == "dangerous_non_net":
        # §2.10: NET 以外の危険効果を持つユニット（NET 込みの `dangerous` と併記）。
        rows = [u for u in rows if _has_non_net_dangerous(u)]
    return rows


NON_NET_DANGEROUS: frozenset[str] = frozenset({"EXEC", "SPAWN", "FS_WRITE", "FS_READ", "DB"})


def _has_non_net_dangerous(u: dict) -> bool:
    effs = u.get("effects") or []
    kinds = set()
    for e in effs:
        if isinstance(e, dict):
            kinds.add(e.get("kind"))
        elif isinstance(e, str):
            kinds.add(e.split("@")[0])
    return bool(kinds & NON_NET_DANGEROUS)


def compute(units: list[dict]) -> list[dict]:
    out: list[dict] = []
    for population in POPULATIONS:
        for path_denom in PATH_DENOMS:
            for unit_denom in UNIT_DENOMS:
                rows = select(units, population, path_denom, unit_denom)
                denom = len(rows)
                numer = sum(1 for u in rows if u.get("validator_shapes"))
                out.append(
                    {
                        "population": population,
                        "path_denom": path_denom,
                        "unit_denom": unit_denom,
                        "numerator": numer,
                        "denominator": denom,
                        "ratio": (numer / denom) if denom else None,
                        "gate_pass": (numer / denom >= VALIDATOR_GATE) if denom else None,
                    }
                )
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run_dir", type=Path, help="evidence/<run> ディレクトリ")
    ap.add_argument("--json", action="store_true", help="JSON で出す")
    args = ap.parse_args(argv)

    units = load_units(args.run_dir)
    rows = compute(units)

    if args.json:
        json.dump(
            {"run_dir": str(args.run_dir), "n_units": len(units), "rows": rows},
            sys.stdout,
            ensure_ascii=False,
            indent=1,
        )
        print()
        return 0

    print(f"# validator 保有率 — 全分母（{args.run_dir}、ユニット {len(units)} 件）")
    print(f"# 関門は仕様書 §10 の `>= {VALIDATOR_GATE:.0%}`。**主分母は dangerous_fp_excluded × all_paths**")
    print("# （preregistration.md §2.2 / §2.3）。他は併記義務のある値であり、選んでよい値ではない。")
    print()
    print(f"{'母集団':<14} {'パス分母':<11} {'ユニット分母':<22} {'分子':>5} {'分母':>6} {'率':>8}  関門")
    print("-" * 78)
    last = None
    for r in rows:
        if last is not None and r["population"] != last:
            print()
        last = r["population"]
        ratio = "—" if r["ratio"] is None else f"{100 * r['ratio']:.2f}%"
        gate = "—" if r["gate_pass"] is None else ("○" if r["gate_pass"] else "×")
        print(
            f"{r['population']:<14} {r['path_denom']:<11} {r['unit_denom']:<22} "
            f"{r['numerator']:>5} {r['denominator']:>6} {ratio:>8}  {gate}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
