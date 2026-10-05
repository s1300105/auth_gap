"""開発者が ToolAnnotations の宣言を「弱めた」コミットを、repo の履歴から探す（正解の候補集め。D78）。

「弱めた」= 副作用が**ある**側に直した変更。直す前の版は、開発者自身が「宣言が実装と合っていなかった」と
認めた例の候補になる（脆弱 / 修正の組と同じ作り）:

* `readOnlyHint` True → False（または True の行が消えた）
* `destructiveHint` False → True（または False の行が消えた）
* `idempotentHint` True → False（または消えた）
* `openWorldHint` False → True（または消えた）

逆向き（強めた）・新しく足した宣言も数えるが、候補には入れない。

**候補であって正解ではない**: 同じコミットでツールの本体に書き込みを足し、宣言をそれに合わせただけなら、直す前の版は
「合っていた」。コミットごとに `body_changed`（同じファイルで宣言以外の行も変わったか）を付けるので、宣言だけを
直したコミットから人が確かめる。

対象は、取得済みの repo の履歴（`corpus/_cache/<owner>__<repo>/`、blob を後から取る clone）。**最終評価のデータに
触れないよう、渡す repo の一覧は開発用のデータ（v2〜v4 の抽出分）だけにする**（D78）。

    .venv/bin/python scripts/mine_annotation_fixes.py --repos <repo の一覧の JSON> --out <出力の JSON> [--jobs 8]
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "corpus", "_cache")
HINTS = ("readOnlyHint", "destructiveHint", "idempotentHint", "openWorldHint")
# 副作用が「無い」側の値（これが消える・反対になると「弱めた」）
SAFE_VALUE = {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False}


DEFAULT = {"readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": True}  # MCP の既定値


def _hint_kw(node) -> dict[str, bool]:
    """式の中の `readOnlyHint=True` / `{"readOnlyHint": True}` を全部拾う。"""
    out: dict[str, bool] = {}
    for n in ast.walk(node):
        if isinstance(n, ast.keyword) and n.arg in HINTS and isinstance(n.value, ast.Constant) \
                and isinstance(n.value.value, bool):
            out[n.arg] = n.value.value
        elif isinstance(n, ast.Dict):
            for k, v in zip(n.keys, n.values, strict=False):
                if isinstance(k, ast.Constant) and k.value in HINTS and isinstance(v, ast.Constant) \
                        and isinstance(v.value, bool):
                    out[k.value] = v.value
    return out


def tools_in(src: bytes) -> dict[str, dict]:
    """ファイルの中のツール: 名前 → {hints, body}。デコレータの宣言（FastMCP）と、`Tool(name="x", annotations=...)`
    の形（低レベル）の両方。名前が重なったら最初のもの。"""
    try:
        tree = ast.parse(src)
    except (SyntaxError, ValueError):
        return {}
    out: dict[str, dict] = {}
    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.decorator_list:
            hints: dict[str, bool] = {}
            for d in n.decorator_list:
                hints.update(_hint_kw(d))
            if hints:
                body = ast.unparse(ast.Module(body=n.body, type_ignores=[]))
                out.setdefault(n.name, {"hints": hints, "body": body})
        elif isinstance(n, ast.Call):
            name = next((k.value.value for k in n.keywords if k.arg == "name" and isinstance(k.value, ast.Constant)
                         and isinstance(k.value.value, str)), None)
            ann = next((k.value for k in n.keywords if k.arg == "annotations"), None)
            if name and ann is not None:
                hints = _hint_kw(ann)
                if hints:
                    out.setdefault(name, {"hints": hints, "body": None})
    return out


def _show(d: str, rev: str, path: str) -> bytes | None:
    r = subprocess.run(["git", "-C", d, "show", f"{rev}:{path}"], capture_output=True, timeout=600)
    return r.stdout if r.returncode == 0 else None


def compare(old: dict[str, dict], new: dict[str, dict]) -> list[dict]:
    """両方の版にあるツールで、宣言が副作用の「ある」側に動いたものを拾う（弱めた）。"""
    out = []
    for name in sorted(set(old) & set(new)):
        o, n = old[name]["hints"], new[name]["hints"]
        for h in HINTS:
            if o.get(h) == SAFE_VALUE[h] and n.get(h, DEFAULT[h]) != SAFE_VALUE[h]:
                out.append({"tool": name, "hint": h, "old": o.get(h), "new": n.get(h, "（消えた＝既定値）"),
                            "body_changed": None if old[name]["body"] is None else old[name]["body"] != new[name]["body"]})
    return out


def mine(repo: str) -> dict:
    d = os.path.join(CACHE, repo.replace("/", "__"))
    if not os.path.isdir(d):
        return {"repo": repo, "status": "no_cache"}
    r = subprocess.run(["git", "-C", d, "log", "--all", "--format=@@COMMIT %H %P|%ad|%s", "--date=short", "--name-only",
                        "-G", "|".join(HINTS), "--", "*.py"],
                       capture_output=True, text=True, errors="replace", timeout=1800)
    if r.returncode != 0:
        return {"repo": repo, "status": "git_failed", "error": r.stderr[-500:]}
    commits = []
    n_touch = 0
    for chunk in r.stdout.split("@@COMMIT ")[1:]:
        head, _, rest = chunk.partition("\n")
        shas, date, subject = (head.split("|", 2) + ["", ""])[:3]
        sha, *parents = shas.split()
        if len(parents) != 1:  # 最初のコミットとマージは飛ばす（比べる前の版が 1 つに決まらない）
            continue
        n_touch += 1
        weak = []
        for path in [x for x in rest.split("\n") if x.endswith(".py")]:
            old_src, new_src = _show(d, parents[0], path), _show(d, sha, path)
            if old_src is None or new_src is None:
                continue
            for w in compare(tools_in(old_src), tools_in(new_src)):
                weak.append({"file": path, **w})
        if weak:
            commits.append({"sha": sha, "parent": parents[0], "date": date, "subject": subject, "weakened": weak})
    return {"repo": repo, "status": "ok", "n_commits_touching_hints": n_touch, "commits": commits}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repos", required=True, help='JSON: ["owner/repo", ...]')
    ap.add_argument("--out", required=True)
    ap.add_argument("--jobs", type=int, default=8)
    a = ap.parse_args()
    repos = json.load(open(a.repos, encoding="utf-8"))
    with ThreadPoolExecutor(max_workers=a.jobs) as pool:
        results = list(pool.map(mine, repos))
    summary = {"n_repos": len(results), "status": {}, "n_commits_touching_hints": 0, "n_repos_with_weakening": 0,
               "n_weakening_commits": 0, "n_weakened_tools": 0, "n_weakened_tools_body_unchanged": 0, "by_hint": {}}
    for res in results:
        summary["status"][res["status"]] = summary["status"].get(res["status"], 0) + 1
        summary["n_commits_touching_hints"] += res.get("n_commits_touching_hints", 0)
        cs = res.get("commits", [])
        if cs:
            summary["n_repos_with_weakening"] += 1
        summary["n_weakening_commits"] += len(cs)
        for c in cs:
            for w in c["weakened"]:
                summary["n_weakened_tools"] += 1
                summary["n_weakened_tools_body_unchanged"] += 1 if w["body_changed"] is False else 0
                summary["by_hint"][w["hint"]] = summary["by_hint"].get(w["hint"], 0) + 1
    json.dump({"summary": summary, "results": results}, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
