#!/usr/bin/env python3
"""母集団 v2（`docs/population_v2.md`）から seed 固定で抽出し、取得時 SHA で pin する。

    .venv/bin/python scripts/sample_population_v2.py --n 100 --seed 20260920

入力: evidence/population_v2/enumeration.jsonl（列挙の生データ、ファイル単位）
出力: docs/corpus_sample_v2.json（name / repo / ref=SHA / population / declaring_paths）
規則（列挙前に固定）: repo の full_name（小文字）で重複除去 → SDK 自身を除く →
宣言ファイルが src 側に 1 つ以上ある repo だけを母集団とする → seed で n 件抽出 →
`git ls-remote <url> HEAD` で default branch の SHA を取り pin する。
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--seed", type=int, default=20260920)
    ap.add_argument("--enum", default="evidence/population_v2/enumeration.jsonl")
    ap.add_argument("--out", default="docs/corpus_sample_v2.json")
    ap.add_argument("--exclude", action="append", default=[],
                    help="除く repo の標本（`targets[].repo`）。v3 は v2 の抽出分を除く（docs/population_v3.md）")
    ap.add_argument("--prefix", default="v2", help="木の名前の接頭辞（v3 は v3）")
    args = ap.parse_args()
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
    rng = random.Random(args.seed)
    chosen = sorted(rng.sample(pop, args.n)) if len(pop) > args.n else pop
    targets = []
    for repo in chosen:
        url = f"https://github.com/{repo}.git"
        p = subprocess.run(["git", "ls-remote", url, "HEAD"], capture_output=True, text=True, timeout=120)
        sha = p.stdout.split()[0] if p.returncode == 0 and p.stdout.strip() else None
        targets.append({
            "name": f"{args.prefix}-" + repo.replace("/", "__"), "repo": repo, "ref": sha or "UNRESOLVED",
            "population": "mcp_server", "note": f"母集団 {args.prefix}（seed={args.seed}）",
            "declaring_paths": sorted(p for p in repos[repo] if cls(p) == "src")[:10],
        })
        print(f"  {repo:50s} {sha[:10] if sha else 'UNRESOLVED'}")
    out = {"_note": f"docs/population_{args.prefix}.md の抽出結果。ref は抽出時の default branch HEAD の SHA（pin）。",
           "seed": args.seed, "n_population": len(pop), "n_enumerated_repos": len(repos),
           "excluded_samples": args.exclude, "targets": targets}
    with open(os.path.join(ROOT, args.out), "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print(f"-> {args.out}  unresolved={sum(1 for t in targets if t['ref'] == 'UNRESOLVED')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
