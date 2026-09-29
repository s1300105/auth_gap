"""`r_malformed`（snake_case で書いて mcp < 2.0 では届かない宣言の率）を full scan の run から数える。

**定義は測定より先に `docs/preregistration.md` §2.10 にコミットした**（O27、2026-09-29 の学生の決定: 最終評価のデータで
数えて報告する。分母は「注釈を書いたユニット」）。

* 分子: `D_kind.malformed` が空でないユニット（mcp の版が < 2.0 と決まったサブツリーで snake_case の注釈を書いたもの。D64 / U38）
* 分母（主）: `unit.annotation_form` が `ToolAnnotations` / `dict` / `unreadable` のユニット（`annotations=` を書いた）
* 併記: 全ユニットを分母にした率、版が決まらない snake_case（`unit.undetermined_fields` が空でない = D_unknown）の件数、木の数

使い方: `python scripts/r_malformed.py evidence/<run>`
"""

from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from runlib import load_manifest, print_warnings, run_manifests  # noqa: E402

ANNOTATED_FORMS = frozenset({"ToolAnnotations", "dict", "unreadable"})


def count(run_dir: str) -> dict:
    manifests, warnings = run_manifests(run_dir)
    print_warnings(warnings, run_dir)
    n = annotated = malformed = undetermined = 0
    trees_mal: set[str] = set()
    trees_und: set[str] = set()
    for tree, path in manifests:
        for u in load_manifest(path).get("units", []):
            n += 1
            un = u["unit"]
            if un.get("annotation_form") in ANNOTATED_FORMS:
                annotated += 1
            if u.get("D_kind", {}).get("malformed"):
                malformed += 1
                trees_mal.add(tree)
            if un.get("undetermined_fields"):
                undetermined += 1
                trees_und.add(tree)
    return {
        "run": os.path.basename(os.path.normpath(run_dir)),
        "n_trees": len(manifests),
        "n_units": n,
        "n_annotated_units": annotated,
        "n_malformed_units": malformed,
        "r_malformed_annotated": (malformed / annotated) if annotated else None,
        "r_malformed_all_units": (malformed / n) if n else None,
        "n_trees_malformed": len(trees_mal),
        "n_undetermined_units": undetermined,
        "n_trees_undetermined": len(trees_und),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    args = ap.parse_args()
    print(json.dumps(count(args.run_dir), ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
