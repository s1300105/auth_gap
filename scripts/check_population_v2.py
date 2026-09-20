#!/usr/bin/env python3
"""母集団 v2 の取得後条件（`docs/population_v2.md` 定義 2・3）を適用し、件数を出す。

    .venv/bin/python scripts/check_population_v2.py --sample docs/corpus_sample_v2.json --out evidence/population_v2/post_fetch_check.json

条件 2: 宣言ファイル（declaring_paths）のどれかが `mcp` または `fastmcp` から import する。
条件 3: 宣言ファイルが src 側にある（抽出時に適用済み。ここで再確認）。
**除外で減った分は補充しない。** 件数をそのまま出す。アーカイブ状態はオフラインでは
分からないので「未判定」と書く。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from fetch_corpus import _checkout_complete  # noqa: E402

IMPORT_RX = re.compile(r"^\s*(from\s+(mcp|fastmcp)(\.|\s)|import\s+(mcp|fastmcp)(\.|\s|$))", re.M)
DECL_RX = re.compile(r"annotations\s*=\s*(ToolAnnotations\(|\{)")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", default="docs/corpus_sample_v2.json")
    ap.add_argument("--corpus", default="corpus")
    ap.add_argument("--out", default="evidence/population_v2/post_fetch_check.json")
    args = ap.parse_args()
    spec = json.load(open(os.path.join(ROOT, args.sample), encoding="utf-8"))
    rows = []
    counts = {"fetched": 0, "not_fetched": 0, "mcp_server": 0, "declares_but_not_mcp_import": 0, "declaring_file_missing": 0}
    for t in spec["targets"]:
        d = os.path.join(ROOT, args.corpus, t["name"])
        row = {"name": t["name"], "repo": t["repo"], "ref": t["ref"]}
        if not os.path.isdir(d) or not _checkout_complete(d):
            row["status"] = "not_fetched"
            counts["not_fetched"] += 1
            rows.append(row)
            continue
        counts["fetched"] += 1
        found_decl = False
        mcp_import = False
        checked = []
        for p in t.get("declaring_paths", []):
            fp = os.path.join(d, p)
            if not os.path.isfile(fp):
                continue
            txt = open(fp, "rb").read().decode("utf-8", "replace")
            has_decl = bool(DECL_RX.search(txt))
            has_imp = bool(IMPORT_RX.search(txt))
            checked.append({"path": p, "declares": has_decl, "imports_mcp": has_imp})
            found_decl |= has_decl
            mcp_import |= has_decl and has_imp
        row["checked"] = checked
        if not found_decl:
            row["status"] = "declaring_file_missing"  # pin 時点と列挙時点の版がずれた等
            counts["declaring_file_missing"] += 1
        elif mcp_import:
            row["status"] = "mcp_server"
            counts["mcp_server"] += 1
        else:
            row["status"] = "declares_but_not_mcp_import"
            counts["declares_but_not_mcp_import"] += 1
        rows.append(row)
    out = {"_note": "docs/population_v2.md 定義 2・3 の取得後判定。archived は未判定（オフライン）。", "counts": counts, "rows": rows}
    with open(os.path.join(ROOT, args.out), "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print(counts)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
