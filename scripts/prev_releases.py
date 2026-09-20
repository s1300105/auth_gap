#!/usr/bin/env python3
"""各木の「直前リリース」を決める（`docs/preregistration.md` §2.7 の手順 1）。

**規則の定義点は `docs/preregistration.md` §2.7 であり、本ファイルはその機械化
である。** 規則を変えるときは先に §2.7 を直し、同 §5 に逸脱として記録する。
ここだけを直してはならない。

出力 `docs/prev_releases.json` は **測定より先にコミットする**。どの木にどのタグを
選んだかを後から動かせないようにするため（`CLAUDE.md` 規則 5 と同じ趣旨）。

    python3 scripts/prev_releases.py --run evidence/f0a_run6 --out docs/prev_releases.json

**このスクリプトは `r_prev` を計算しない。** タグを選ぶだけである。値を出すのは
別の段（§2.7 (h) の手順 3〜5）で、選択と測定を分けておくため。
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import re
import subprocess
from dataclasses import dataclass
from typing import Optional

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#: タグ列挙専用の cache。`corpus/_cache`（作業木を切る方）とは別に置く。
#: `--filter=tree:0 --bare` なので commit だけで blob も tree も持たない。
TAGCACHE = os.path.join(ROOT, "corpus", "_tagcache")

#: §2.7 (c) リリースタグの形。**接頭辞つき（`python-servers-0.6.2`）も含める。**
#: 素朴な `^v?\d+\.\d+` だと modelcontextprotocol/servers のタグが 1 本も
#: 取れない（実測で確認済み）。
RELEASE_RE = re.compile(r"\d+\.\d+")

#: §2.7 (c) プレリリースの語。大文字小文字を無視して部分一致で除く。
PRERELEASE_WORDS: tuple[str, ...] = ("rc", "alpha", "beta", "dev", "pre", "snapshot", "nightly")

#: §2.7 (e) 感度分析の距離。
SENSITIVITY_STEPS = 5


def _run(cmd: list[str], cwd: Optional[str] = None, timeout: int = 600) -> tuple[int, str]:
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return 124, "timeout"
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def is_release_tag(name: str) -> bool:
    """§2.7 (c)。**本関数だけが判定点。**"""
    if not RELEASE_RE.search(name):
        return False
    low = name.lower()
    return not any(w in low for w in PRERELEASE_WORDS)


def _slug(repo: str) -> str:
    return repo.replace("https://github.com/", "").replace(".git", "").replace("/", "__")


def ensure_tagcache(repo: str) -> tuple[Optional[str], Optional[str]]:
    """commit だけの bare clone。タグの peel・日付・祖先判定に必要な最小構成。"""
    url = repo if repo.startswith("http") else f"https://github.com/{repo}.git"
    dest = os.path.join(TAGCACHE, _slug(repo))
    if os.path.isdir(os.path.join(dest, "refs")):
        return dest, None
    os.makedirs(TAGCACHE, exist_ok=True)
    code, out = _run(["git", "clone", "--filter=tree:0", "--no-checkout", "--bare", url, dest])
    if code != 0:
        return None, f"clone {repo}: {out.strip()[:200]}"
    return dest, None


@dataclass
class TagInfo:
    name: str
    sha: str
    date: str = ""
    ancestor: bool = False


@dataclass
class TreeResult:
    tree: str
    repo: str
    analyzed_sha: str
    population: str
    #: `ok` / `no_release_tag` / `single_release` / `no_ancestor_release` / `fetch_failed`
    status: str = "ok"
    n_tags_total: int = 0
    n_release_tags: int = 0
    n_ancestor_release_tags: int = 0
    prev_tag: Optional[str] = None
    prev_sha: Optional[str] = None
    prev_date: Optional[str] = None
    prev5_tag: Optional[str] = None
    prev5_sha: Optional[str] = None
    prev5_steps_back: Optional[int] = None
    note: str = ""

    def to_json(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


def resolve_tree(tree: str, repo: str, analyzed_sha: str, population: str) -> TreeResult:
    """1 木について §2.7 (c)(d)(e) を適用する。"""
    r = TreeResult(tree=tree, repo=repo, analyzed_sha=analyzed_sha, population=population)
    cache, err = ensure_tagcache(repo)
    if cache is None:
        r.status, r.note = "fetch_failed", (err or "")[:200]
        return r

    code, out = _run(
        ["git", "for-each-ref", "--format=%(refname:short)\t%(objectname)\t%(*objectname)", "refs/tags"],
        cwd=cache,
    )
    if code != 0:
        r.status, r.note = "fetch_failed", f"for-each-ref: {out.strip()[:200]}"
        return r

    tags: list[TagInfo] = []
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) < 2 or not parts[0]:
            continue
        name, obj = parts[0], parts[1]
        peeled = parts[2] if len(parts) > 2 and parts[2] else obj
        tags.append(TagInfo(name=name, sha=peeled))
    r.n_tags_total = len(tags)

    releases = [t for t in tags if is_release_tag(t.name)]
    r.n_release_tags = len(releases)
    if len(releases) < 2:
        # §2.7 (f) 1 行目: リリースタグが 0 本または 1 本 → 分母に入れない。
        r.status = "no_release_tag" if not releases else "single_release"
        return r

    # 解析 commit がこの cache に居るか（居なければ祖先判定ができない）。
    code, _ = _run(["git", "cat-file", "-e", f"{analyzed_sha}^{{commit}}"], cwd=cache)
    if code != 0:
        _run(["git", "fetch", "--tags", "origin"], cwd=cache)
        code, _ = _run(["git", "cat-file", "-e", f"{analyzed_sha}^{{commit}}"], cwd=cache)
        if code != 0:
            r.status, r.note = "fetch_failed", f"解析 commit {analyzed_sha[:12]} を cache で解決できない"
            return r

    # §2.7 (d) 祖先であり、解析 commit 自身を指さないもの。
    usable: list[TagInfo] = []
    for t in releases:
        if t.sha == analyzed_sha:
            continue
        code, _ = _run(["git", "merge-base", "--is-ancestor", t.sha, analyzed_sha], cwd=cache)
        if code != 0:
            continue
        dc, dout = _run(["git", "show", "-s", "--format=%cI", t.sha], cwd=cache)
        if dc != 0:
            continue
        t.date = dout.strip().splitlines()[-1] if dout.strip() else ""
        t.ancestor = True
        usable.append(t)

    r.n_ancestor_release_tags = len(usable)
    if not usable:
        r.status = "no_ancestor_release"
        return r

    # §2.7 (d) committer date の新しい順。同着はタグ名で決める（決定論のため）。
    usable.sort(key=lambda t: (t.date, t.name), reverse=True)
    top = usable[0]
    r.prev_tag, r.prev_sha, r.prev_date = top.name, top.sha, top.date

    # §2.7 (e) 5 リリース前。足りなければ最も古いものを使い、実際の距離を記録する。
    idx = min(SENSITIVITY_STEPS - 1, len(usable) - 1)
    r.prev5_tag, r.prev5_sha, r.prev5_steps_back = usable[idx].name, usable[idx].sha, idx + 1
    return r


def load_inputs(run_dir: str, sample_path: str) -> list[tuple[str, str, str, str]]:
    """`(tree, repo, analyzed_sha, population)` の列。**run6 の 98 木に限る**（§2.7 (b)）。"""
    repos = {t["name"]: t["repo"] for t in json.load(open(sample_path, encoding="utf-8"))["targets"]}
    out = []
    with open(os.path.join(run_dir, "trees.jsonl"), encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            t = json.loads(line)
            repo = repos.get(t["tree"])
            if repo is None:
                raise SystemExit(f"標本に無い木: {t['tree']}")
            out.append((t["tree"], repo, t.get("commit_sha") or "", t.get("population") or ""))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", default="evidence/f0a_run6", help="trees.jsonl のある run ディレクトリ")
    ap.add_argument("--sample", default="docs/corpus_sample.json")
    ap.add_argument("--out", default="docs/prev_releases.json")
    ap.add_argument("--jobs", type=int, default=8)
    args = ap.parse_args()

    rows = load_inputs(os.path.join(ROOT, args.run), os.path.join(ROOT, args.sample))
    print(f"対象 {len(rows)} 木（{args.run}）")

    results: list[TreeResult] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as ex:
        futs = {ex.submit(resolve_tree, *row): row[0] for row in rows}
        for i, fut in enumerate(concurrent.futures.as_completed(futs), 1):
            r = fut.result()
            results.append(r)
            if i % 10 == 0 or i == len(rows):
                print(f"  {i}/{len(rows)}")

    results.sort(key=lambda r: (r.population, r.tree))
    counts: dict[str, int] = {}
    for r in results:
        counts[r.status] = counts.get(r.status, 0) + 1

    payload = {
        "_note": (
            "docs/preregistration.md §2.7 の手順 1 の出力。**測定より先にコミットする。** "
            "規則の定義点は §2.7 であり、本ファイルはその適用結果である。"
        ),
        "_rules": {
            "release_tag_regex": RELEASE_RE.pattern,
            "prerelease_words": list(PRERELEASE_WORDS),
            "sensitivity_steps": SENSITIVITY_STEPS,
            "ordering": "祖先であるリリースタグを committer date の降順。同着はタグ名で決める",
        },
        "run": args.run,
        "n_trees": len(results),
        "status_counts": dict(sorted(counts.items())),
        "trees": [r.to_json() for r in results],
    }
    out_path = os.path.join(ROOT, args.out)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1, sort_keys=False)
        fh.write("\n")

    print()
    print("status:")
    for k, v in sorted(counts.items()):
        print(f"  {k:24} {v}")
    by_pop: dict[str, list[int]] = {}
    for r in results:
        d = by_pop.setdefault(r.population, [0, 0])
        d[0] += 1
        if r.status == "ok":
            d[1] += 1
    print()
    print("母集団別（ok = 直前リリースを決められた木）:")
    for pop in ("mcp_server", "tool_package", "app"):
        if pop in by_pop:
            n, ok = by_pop[pop]
            print(f"  {pop:14} ok {ok}/{n} = {100 * ok / n:.1f}%")
    print(f"\n-> {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
