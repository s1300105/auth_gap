#!/usr/bin/env python3
"""母集団 v2（`docs/population_v2.md`）から seed 固定で抽出し、取得時 SHA で pin する。

    .venv/bin/python scripts/sample_population_v2.py --n 100 --seed 20260920
    .venv/bin/python scripts/sample_population_v2.py --all --exclude ... --prefix final   # 最終評価（D69・D73 の 5）

入力: evidence/population_v2/enumeration.jsonl（列挙の生データ、ファイル単位）
出力: docs/corpus_sample_v2.json（name / repo / ref=SHA / population / declaring_paths）
規則（列挙前に固定）: repo の full_name（小文字）で重複除去 → SDK 自身を除く →
宣言ファイルが src 側に 1 つ以上ある repo だけを母集団とする → seed で n 件抽出 →
`git ls-remote <url> HEAD` で default branch の SHA を取り pin する。

`--all` は抽出せずに全部を取る（最終評価、D69）。乱数の種を使わないので、出力の `seed` は null、`mode` は "all" と書く。
前は `--n 100000` で全部を返させていたが、そのときも既定の種（20260920）が出力に「抽出の種」として残り、使っていない種が
記録に載っていた（D73 の 5）。
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from denominators import path_class  # noqa: E402

VENDORED = ("site-packages", "node_modules", ".venv", "venv", "vendor")


def cls(p: str) -> str:
    parts = re.split(r"[/\\]", p)[:-1]
    if any(x in VENDORED for x in parts) or p.endswith("mcp/types.py") or "/mcp/server/" in "/" + p:
        return "vendored"
    return path_class(p)


def choose(pop: list[str], n: int | None, seed: int | None, take_all: bool) -> list[str]:
    """母集団（除外の後）から対象を選ぶ。`take_all` なら全部（抽出しない）。"""
    if take_all:
        return sorted(pop)
    rng = random.Random(seed)
    return sorted(rng.sample(pop, n)) if len(pop) > n else sorted(pop)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=None, help="抽出数（既定 100）。--all とは同時に使えない")
    ap.add_argument("--seed", type=int, default=None, help="抽出の種（既定 20260920）。--all とは同時に使えない")
    ap.add_argument("--all", action="store_true", help="抽出せずに全部を取る（最終評価、D69・D73 の 5）")
    ap.add_argument("--enum", default="evidence/population_v2/enumeration.jsonl")
    ap.add_argument("--out", default="docs/corpus_sample_v2.json")
    ap.add_argument("--exclude", action="append", default=[],
                    help="除く repo の標本（`targets[].repo`）。v3 は v2 の抽出分を除く（docs/population_v3.md）")
    ap.add_argument("--prefix", default="v2", help="木の名前の接頭辞（v3 は v3）")
    args = ap.parse_args()
    if args.all and (args.n is not None or args.seed is not None):
        ap.error("--all と --n / --seed は同時に使えない（全部を取るときは種を使わない）")
    if not args.all:
        args.n = 100 if args.n is None else args.n
        args.seed = 20260920 if args.seed is None else args.seed
    excluded: set[str] = set()
    for path in args.exclude:
        with open(os.path.join(ROOT, path), encoding="utf-8") as fh:
            excluded |= {t["repo"].lower() for t in json.load(fh)["targets"]}
    repos: dict[str, set[str]] = {}
    with open(os.path.join(ROOT, args.enum), encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            r = json.loads(line)
            repo = (r.get("repo") or "").lower()
            if "/" in repo:
                repos.setdefault(repo, set()).add(r.get("path", ""))
    pop = sorted(repo for repo, paths in repos.items()
                 if repo != "modelcontextprotocol/python-sdk" and any(cls(p) == "src" for p in paths))
    print(f"母集団（src 側に宣言のある repo）: {len(pop)} / 列挙 repo {len(repos)}")
    if excluded:
        pop = [r for r in pop if r not in excluded]
        print(f"除外（--exclude の標本）: {len(excluded)} → 抽出元 {len(pop)}")
    chosen = choose(pop, args.n, args.seed, args.all)
    if args.all:
        overlap = set(chosen) & excluded
        if len(chosen) != len(pop) or overlap:
            raise SystemExit(f"全数のはずが件数が合わない: 選んだ {len(chosen)} / 母集団 − 除外 {len(pop)}、除外との重なり {len(overlap)}")
        print(f"全数（抽出しない）: {len(chosen)} 件")
    targets = []
    for repo in chosen:
        url = f"https://github.com/{repo}.git"
        p = subprocess.run(["git", "ls-remote", url, "HEAD"], capture_output=True, text=True, timeout=120)
        sha = p.stdout.split()[0] if p.returncode == 0 and p.stdout.strip() else None
        targets.append({
            "name": f"{args.prefix}-" + repo.replace("/", "__"), "repo": repo, "ref": sha or "UNRESOLVED",
            "population": "mcp_server",
            "note": f"母集団 {args.prefix}（全数）" if args.all else f"母集団 {args.prefix}（seed={args.seed}）",
            "declaring_paths": sorted(p for p in repos[repo] if cls(p) == "src")[:10],
        })
        print(f"  {repo:50s} {sha[:10] if sha else 'UNRESOLVED'}")
    out = {"_note": f"docs/population_{args.prefix}.md の抽出結果。ref は抽出時の default branch HEAD の SHA（pin）。",
           "mode": "all" if args.all else "sample", "seed": None if args.all else args.seed,
           "n_population": len(pop), "n_enumerated_repos": len(repos),
           "excluded_samples": args.exclude, "targets": targets}
    with open(os.path.join(ROOT, args.out), "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print(f"-> {args.out}  unresolved={sum(1 for t in targets if t['ref'] == 'UNRESOLVED')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
