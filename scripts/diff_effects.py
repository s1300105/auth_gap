#!/usr/bin/env python3
"""解析器の 2 つの版で、同じ木の効果行を突き合わせる（**消えた効果行を見つける**）。

解析器を直したら、較正対の木でこれを走らせてからコミットする。受け入れテストが
「両側通過 7/7」のまま通っても、**経路の効果行が黙って消えている**ことがある
（D17 の改訂: 受け手型の無いメソッド呼び出しを解決しないようにしたら、langroid の
`compute_from_docs` の eval と PraisonAI の `_apply_step` の subprocess.run が消えた）。

行の同一性は `unit_id | witness_chain | kind@site relpath:lineno`。slot の中身
（主体 / 確度）の変化は「変化」として別に出す。

使い方::

    python scripts/diff_effects.py --before 186d406 corpus/A9__vuln corpus/A9__fixed
    python scripts/diff_effects.py --before 186d406 --after 0662b39 corpus/A18__fixed

`--after` を省くと作業木（未コミットの変更を含む）と比べる。**消えた行が 1 件でも
あれば終了コード 1**（意図した削除なら、その行を 1 件ずつ原ソースで確かめて理由を
コミットメッセージに書く）。
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#: 各版の解析器で走らせるコード（その版の `authgap` を import する）。
DUMP = r"""
import json, sys
from authgap.runner import RunConfig, run
out = {}
for tree in sys.argv[1:]:
    res = run(RunConfig(src_root=tree, full=True))
    rows = {}
    for u in res.tree.units:
        for e in u.effects:
            key = f"{u.unit.unit_id} | {'>'.join(e.witness_chain)} | {e.kind}@{e.site} {e.relpath}:{e.lineno}"
            slots = ",".join(
                f"{s}={v.prin.name}/{v.prov.kind}" for s, v in sorted(e.control_slots().items())
            )
            reasons = "+".join(e.resolution.reasons)
            val = f"{slots} ; resolution={e.resolution.kind}{('(' + reasons + ')') if reasons else ''}"
            rows.setdefault(key, set()).add(val)
    out[tree] = {k: sorted(v) for k, v in sorted(rows.items())}
json.dump(out, sys.stdout)
"""


def _dump(code_root: str, trees: list[str]) -> dict:
    env = dict(os.environ, PYTHONPATH=code_root)
    p = subprocess.run(
        [sys.executable, "-c", DUMP, *trees], cwd=code_root, env=env, capture_output=True, text=True
    )
    if p.returncode != 0:
        raise SystemExit(f"解析に失敗（{code_root}）:\n{p.stderr[-2000:]}")
    return json.loads(p.stdout)


def _checkout(ref: str) -> str:
    dest = tempfile.mkdtemp(prefix="authgap-diff-")
    os.rmdir(dest)
    p = subprocess.run(
        ["git", "-C", ROOT, "worktree", "add", "--detach", dest, ref], capture_output=True, text=True
    )
    if p.returncode != 0:
        raise SystemExit(f"git worktree add {ref} に失敗: {p.stderr}")
    return dest


def _release(dest: str) -> None:
    subprocess.run(["git", "-C", ROOT, "worktree", "remove", "--force", dest], capture_output=True)
    shutil.rmtree(dest, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--before", required=True, help="比べる元の commit")
    ap.add_argument("--after", default=None, help="比べる先の commit（省略時は作業木）")
    ap.add_argument("--json", default=None, help="差分を JSON で書き出す")
    ap.add_argument("trees", nargs="+")
    args = ap.parse_args()
    trees = [os.path.abspath(t) for t in args.trees]

    made: list[str] = []
    try:
        before_root = _checkout(args.before)
        made.append(before_root)
        if args.after:
            after_root = _checkout(args.after)
            made.append(after_root)
        else:
            after_root = ROOT
        before = _dump(before_root, trees)
        after = _dump(after_root, trees)
    finally:
        for d in made:
            _release(d)

    report: dict = {"before": args.before, "after": args.after or "WORKTREE", "trees": {}}
    n_gone_total = 0
    for t in trees:
        b, a = before.get(t, {}), after.get(t, {})
        gone = sorted(set(b) - set(a))
        new = sorted(set(a) - set(b))
        changed = sorted(k for k in set(a) & set(b) if a[k] != b[k])
        n_gone_total += len(gone)
        name = os.path.basename(t)
        print(f"== {name}: 行 {len(b)} → {len(a)}（消えた {len(gone)} / 増えた {len(new)} / slot 変化 {len(changed)}）")
        for k in gone:
            print(f"  - {k}\n      {b[k]}")
        for k in changed:
            print(f"  ~ {k}\n      {b[k]}\n   => {a[k]}")
        for k in new:
            print(f"  + {k}")
        report["trees"][name] = {
            "gone": {k: b[k] for k in gone},
            "new": {k: a[k] for k in new},
            "changed": {k: {"before": b[k], "after": a[k]} for k in changed},
        }
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(report, fh, ensure_ascii=False, indent=2, sort_keys=True)
            fh.write("\n")
    if n_gone_total:
        print(f"\n**消えた効果行 {n_gone_total} 件。** 1 件ずつ原ソースで確かめること。")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
