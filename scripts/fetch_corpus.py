#!/usr/bin/env python3
"""解析対象の木を `corpus/` に取得する。

規則（§9-12 と §7.6 D14）:

* sparse パターンに `/**/*.txt` と `/**/*.lock` を**必ず含める**。
  前測のコーパスは `requirements*.txt` / `uv.lock` / `poetry.lock` を 1 件も
  含まないまま「依存版を読んだ」と書いていた。
* repo ごとの commit SHA を `docs/frame.csv` に記録する。
* **取得失敗を件数として記録する。黙って落とさない**
  （`docs/fetch_failures.md`）。
* ref は `git rev-parse` で解決できることを確認してから記録する。

使い方::

    python scripts/fetch_corpus.py --spec docs/corpus_spec.json
    python scripts/fetch_corpus.py --repo modelcontextprotocol/servers \\
        --ref 9e5d5b8e --name mcp-server-git@vuln \\
        --subdir src/git

sparse checkout を worktree に対して実際に適用する。パターンは
:data:`BASE_PATTERNS`（`--subdir` を渡すとその部分木 + 依存ファイル）。
**`.txt` と `.lock` を必ず含める**（§9-12。前測のコーパスはこれらを 1 件も
含まないまま「依存版を読んだ」と書いていた）。
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Optional

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(ROOT, "corpus")
FRAME_CSV = os.path.join(ROOT, "docs", "frame.csv")
FAILURES_MD = os.path.join(ROOT, "docs", "fetch_failures.md")

#: sparse checkout のパターン。**`.txt` と `.lock` を必ず含める。**
BASE_PATTERNS = [
    "/**/*.py",
    "/**/*.toml",
    "/**/*.txt",
    "/**/*.lock",
    "/**/*.json",
    "/**/*.cfg",
]


@dataclass
class Target:
    repo: str
    ref: str
    name: str
    subdir: Optional[str] = None
    population: str = "mcp_server"
    note: str = ""


@dataclass
class Fetched:
    target: Target
    path: str
    sha: str
    n_py: int
    has_requirements: bool
    has_lock: bool
    files_sample: list[str] = field(default_factory=list)


def _run(args: list[str], cwd: Optional[str] = None) -> tuple[int, str]:
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip()


CACHE = os.path.join(CORPUS, "_cache")


def _cache_dir(repo: str) -> str:
    slug = repo.replace("https://github.com/", "").replace(".git", "").replace("/", "__")
    return os.path.join(CACHE, slug)


def ensure_cache(repo: str) -> tuple[Optional[str], Optional[str]]:
    """リポジトリを 1 回だけ部分クローンする（blob はオンデマンド）。

    対ごとに fetch し直すと、浅い取得が SHA を掴めずに default branch へ
    落ちる事故が起きる。**cache + worktree にして pin を確実にする。**
    """
    url = repo if repo.startswith("http") else f"https://github.com/{repo}.git"
    dest = _cache_dir(repo)
    if os.path.isdir(os.path.join(dest, ".git")):
        return dest, None
    os.makedirs(CACHE, exist_ok=True)
    code, out = _run(["git", "clone", "--filter=blob:none", "--no-checkout", url, dest])
    if code != 0:
        return None, f"clone {repo} -> {out}"
    return dest, None


def fetch(t: Target, depth: int = 1) -> tuple[Optional[Fetched], Optional[str]]:
    """1 つの pin を worktree として取り出す。

    **取り出した SHA が要求した ref に一致することを必ず確認する。**
    一致しなければ失敗として記録する（黙って default branch を掴まない）。
    """
    del depth
    dest = os.path.join(CORPUS, t.name.replace("/", "_").replace("@", "__"))
    if os.path.isdir(os.path.join(dest, ".git")) or os.path.isfile(os.path.join(dest, ".git")):
        code, out = _run(["git", "rev-parse", "HEAD"], cwd=dest)
        if code == 0 and _sha_matches(t.ref, out.strip()) and _checkout_complete(dest):
            return _describe(t, dest, out.strip()), None
        _run(["git", "worktree", "remove", "--force", dest], cwd=_cache_dir(t.repo))
        if os.path.isdir(dest):
            # worktree として登録されていない残骸（中断時）も消す。
            import shutil

            shutil.rmtree(dest)
        _run(["git", "worktree", "prune"], cwd=_cache_dir(t.repo))

    cache, err = ensure_cache(t.repo)
    if cache is None:
        return None, f"{t.name}: {err}"

    code, resolved = _run(["git", "rev-parse", "--verify", f"{t.ref}^{{commit}}"], cwd=cache)
    if code != 0:
        _run(["git", "fetch", "--tags", "origin"], cwd=cache)
        code, resolved = _run(["git", "rev-parse", "--verify", f"{t.ref}^{{commit}}"], cwd=cache)
    if code != 0:
        return None, f"{t.name}: ref {t.ref!r} を rev-parse で解決できない -> {resolved}"
    sha = resolved.strip()

    # **sparse checkout を実際に適用する。** `--no-checkout` で worktree を作り、
    # パターンを設定してから checkout する。適用しないと巨大な repo を丸ごと
    # 展開してしまう（野外 90 木では致命的）。
    code, out = _run(
        ["git", "worktree", "add", "--no-checkout", "--detach", "--force", dest, sha], cwd=cache
    )
    if code != 0:
        return None, f"{t.name}: worktree add -> {out}"
    patterns = list(BASE_PATTERNS)
    if t.subdir:
        patterns = [f"/{t.subdir.strip('/')}/**"] + [
            p for p in BASE_PATTERNS if p.endswith((".txt", ".lock", ".toml", ".cfg"))
        ]
    code, out = _run(["git", "sparse-checkout", "init", "--no-cone"], cwd=dest)
    if code != 0:
        return None, f"{t.name}: sparse-checkout init -> {out}"
    code, out = _run(["git", "sparse-checkout", "set", *patterns], cwd=dest)
    if code != 0:
        return None, f"{t.name}: sparse-checkout set -> {out}"
    code, out = _run(["git", "checkout", "--detach", sha], cwd=dest)
    if code != 0:
        return None, f"{t.name}: checkout -> {out}"

    code, head = _run(["git", "rev-parse", "HEAD"], cwd=dest)
    if code != 0 or head.strip() != sha:
        return None, f"{t.name}: checkout 後の HEAD が要求 ref と違う（{head.strip()} != {sha}）"
    if not _sha_matches(t.ref, sha):
        return None, f"{t.name}: ref {t.ref} と HEAD {sha} が前方一致しない"
    return _describe(t, dest, sha), None


def _checkout_complete(dest: str) -> bool:
    """worktree の checkout が最後まで終わっているか。

    **HEAD の一致だけでは足りない。** `worktree add --no-checkout` の直後に
    中断すると HEAD は要求 SHA を指したまま中身が空で、`git status` には
    staged deletion が並ぶ。これを完了扱いすると、その木は「ユニット 0 件」
    （フレームの雑音）として数えられ、**ユニットが黙って消える**。
    sparse パターンが設定済みで、作業木が index と一致していることを要求する。
    """
    code, sparse = _run(["git", "sparse-checkout", "list"], cwd=dest)
    if code != 0 or not sparse.strip():
        return False
    code, status = _run(["git", "status", "--porcelain", "--untracked-files=no"], cwd=dest)
    return code == 0 and not status.strip()


def _sha_matches(ref: str, sha: str) -> bool:
    """ref が SHA 前置きなら前方一致を要求する。tag / branch 名なら常に真。"""
    r = ref.strip()
    if all(c in "0123456789abcdef" for c in r.lower()) and len(r) >= 6:
        return sha.lower().startswith(r.lower())
    return True


def _describe(t: Target, dest: str, sha: str) -> Fetched:
    n_py = 0
    has_req = has_lock = False
    sample: list[str] = []
    for dirpath, dirs, files in os.walk(dest):
        dirs[:] = sorted(d for d in dirs if d != ".git")
        for fn in sorted(files):
            if fn.endswith(".py"):
                n_py += 1
                if len(sample) < 5:
                    sample.append(os.path.relpath(os.path.join(dirpath, fn), dest))
            if fn.startswith("requirements") and fn.endswith(".txt"):
                has_req = True
            if fn in ("uv.lock", "poetry.lock", "Pipfile.lock"):
                has_lock = True
    return Fetched(t, dest, sha, n_py, has_req, has_lock, sample)


def write_frame(rows: list[Fetched]) -> None:
    os.makedirs(os.path.dirname(FRAME_CSV), exist_ok=True)
    existing: dict[str, dict] = {}
    if os.path.exists(FRAME_CSV):
        with open(FRAME_CSV, encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                existing[r["name"]] = r
    for f in rows:
        existing[f.target.name] = {
            "name": f.target.name,
            "repo": f.target.repo,
            "ref": f.target.ref,
            "commit_sha": f.sha,
            "subdir": f.target.subdir or "",
            "population": f.target.population,
            "path": os.path.relpath(f.path, ROOT),
            "n_py": str(f.n_py),
            "has_requirements_txt": str(f.has_requirements),
            "has_lock": str(f.has_lock),
            "note": f.target.note,
        }
    cols = [
        "name",
        "repo",
        "ref",
        "commit_sha",
        "subdir",
        "population",
        "path",
        "n_py",
        "has_requirements_txt",
        "has_lock",
        "note",
    ]
    with open(FRAME_CSV, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for name in sorted(existing):
            w.writerow({c: existing[name].get(c, "") for c in cols})


def write_failures(failures: list[str]) -> None:
    with open(FAILURES_MD, "w", encoding="utf-8") as fh:
        fh.write("# コーパス取得の失敗\n\n")
        fh.write("**黙って落とさない。** 失敗は件数として記録し、母集団の分母に反映する。\n\n")
        fh.write(f"失敗 {len(failures)} 件。\n\n")
        for f in failures:
            fh.write(f"- {f}\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", help="取得対象の JSON（`targets` の配列）")
    ap.add_argument("--repo")
    ap.add_argument("--ref")
    ap.add_argument("--name")
    ap.add_argument("--subdir")
    ap.add_argument("--population", default="mcp_server")
    ap.add_argument("--note", default="")
    ap.add_argument("--jobs", type=int, default=4, help="並列数（clone が律速なので 4 程度）")
    args = ap.parse_args()

    targets: list[Target] = []
    if args.spec:
        with open(args.spec, encoding="utf-8") as fh:
            for row in json.load(fh)["targets"]:
                targets.append(Target(**row))
    if args.repo:
        targets.append(
            Target(args.repo, args.ref, args.name or args.repo.split("/")[-1], args.subdir, args.population, args.note)
        )
    if not targets:
        ap.error("--spec か --repo のどちらかが要る")

    os.makedirs(CORPUS, exist_ok=True)
    ok: list[Fetched] = []
    failures: list[str] = []

    # 同一 repo への worktree 追加は直列でなければならないので、repo 単位で束ねる。
    from concurrent.futures import ThreadPoolExecutor

    by_repo: dict[str, list[Target]] = {}
    for t in targets:
        by_repo.setdefault(t.repo, []).append(t)

    def do_repo(ts: list[Target]) -> list[tuple[Optional[Fetched], Optional[str]]]:
        return [fetch(t) for t in ts]

    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        for batch in pool.map(do_repo, by_repo.values()):
            for f, err in batch:
                if f is None:
                    failures.append(err or "unknown error")
                    print(f"FAIL {err}", file=sys.stderr)
                    continue
                ok.append(f)
                flags = []
                if not f.has_requirements:
                    flags.append("no requirements*.txt")
                if not f.has_lock:
                    flags.append("no lock file")
                print(f"OK   {f.target.name} {f.sha[:12]} py={f.n_py} "
                      + ("; ".join(flags) if flags else ""))
    write_frame(ok)
    write_failures(failures)
    print(f"\nframe: {FRAME_CSV}  failures: {len(failures)} -> {FAILURES_MD}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
