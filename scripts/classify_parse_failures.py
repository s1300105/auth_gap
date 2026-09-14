#!/usr/bin/env python3
"""F0a の parse 失敗を原因別に分類する（§5.2「黙って落とさない」の中身を出す）。

`SourceIndex.parse_failures` はパスしか持たないので、1 件ずつ解析器と同じ
Python（3.10）で parse し直し、失敗した行を読んで分類する。

分類（**失敗行の字面による判定。3.12 の処理系で parse し直してはいない**
— 環境に 3.12 以上が無いため。確定させるには 3.12 で再 parse する）:

* ``parses_from_bytes`` — バイト列で渡せば parse できる（BOM / PEP 263 の coding 宣言）。
  **解析器の欠陥**（`open(encoding="utf-8")` で読むと BOM が残る）。
* ``pep695`` — `type X = ...` / `def f[T]` / `class C[T]`（3.12 の構文）。
* ``pep701_fstring`` — f-string 内の同種引用符・バックスラッシュ（3.12 の構文）。
* ``template_placeholder`` — `{{name}}` を含む雛形ファイル（正しく parse できない）。
* ``other_invalid`` — それ以外（壊れたファイル、全角引用符など。3.11+ 構文が混ざりうる）。

使い方::

    python scripts/classify_parse_failures.py            # evidence/f0a/trees.jsonl の木
"""

from __future__ import annotations

import argparse
import ast
import collections
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from authgap.srcindex import SourceIndex  # noqa: E402

#: ツール定義の目印（parse 失敗でユニットを失った可能性の目安。**網羅ではない**）。
TOOL_MARKERS = re.compile(
    r"@\w+\.tool\b|@tool\b|@function_tool|\(BaseTool\)|call_tool|Toolkit\)|FunctionTool\."
)


def classify(path: str) -> tuple[str, str]:
    raw = open(path, "rb").read()
    try:
        ast.parse(raw)
        return "parses_from_bytes", ""
    except SyntaxError as e:
        line = (e.text or "").strip()[:120]
        loc = f"{e.lineno}: {line}"
        msg = e.msg or ""
    if re.match(r"^type\s+\w+.*=", line) or re.search(r"^(async\s+)?def\s+\w+\[|^class\s+\w+\[", line):
        return "pep695", loc
    if "f-string" in msg or re.search(r"""f["'].*\{[^}]*["\\]""", line) or (
        "unterminated string" in msg and re.search(r"""f["']""", line)
    ):
        return "pep701_fstring", loc
    if re.search(r"\{\{|\}\}", line):
        return "template_placeholder", loc
    return "other_invalid", loc


def parses_with(python: str, path: str) -> bool:
    """別の処理系（例: 3.12）の `ast` で parse できるか。**字面の分類を確かめる手段。**"""
    import subprocess

    code = "import ast,sys; ast.parse(open(sys.argv[1],'rb').read())"
    return subprocess.run([python, "-c", code, path], capture_output=True).returncode == 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--trees", default=os.path.join(ROOT, "evidence", "f0a", "trees.jsonl"))
    ap.add_argument("--out", default=os.path.join(ROOT, "evidence", "f0a", "parse_failures.json"))
    ap.add_argument("--newer-python", default=None,
                    help="新しい処理系で再 parse して字面の分類を確かめる（例: `uv python find 3.12`）")
    args = ap.parse_args()

    rows = []
    with open(args.trees, encoding="utf-8") as fh:
        trees = [json.loads(line) for line in fh if line.strip()]
    for t in trees:
        if not t.get("parse_failures"):
            continue
        ix = SourceIndex(os.path.join(ROOT, "corpus", t["tree"]))
        ix.build()
        for rel in sorted(ix.parse_failures):
            p = os.path.join(ROOT, "corpus", t["tree"], rel)
            cat, loc = classify(p)
            text = open(p, "rb").read().decode("utf-8", "replace")
            rows.append({
                "population": t["population"],
                "tree": t["tree"],
                "relpath": rel,
                "category": cat,
                "failing_line": loc,
                "has_tool_marker": bool(TOOL_MARKERS.search(text)),
                "parses_in_newer_python": parses_with(args.newer_python, p) if args.newer_python else None,
            })
    by_cat = collections.Counter(r["category"] for r in rows)
    by_pop = collections.Counter((r["population"], r["category"]) for r in rows)
    out = {
        "n_files": len(rows),
        "by_category": dict(sorted(by_cat.items())),
        "by_population_category": {f"{p}:{c}": n for (p, c), n in sorted(by_pop.items())},
        "n_with_tool_marker": sum(r["has_tool_marker"] for r in rows),
        "newer_python": _version(args.newer_python) if args.newer_python else None,
        "n_parses_in_newer_python": (
            sum(bool(r["parses_in_newer_python"]) for r in rows) if args.newer_python else None
        ),
        "files": rows,
    }
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")
    print(json.dumps({k: v for k, v in out.items() if k != "files"}, ensure_ascii=False, indent=1))
    for r in rows:
        if r["has_tool_marker"]:
            print("TOOL MARKER:", r["tree"], r["relpath"], r["category"])
    return 0


def _version(python: str) -> str:
    import subprocess

    p = subprocess.run([python, "--version"], capture_output=True, text=True)
    return (p.stdout or p.stderr).strip()


if __name__ == "__main__":
    raise SystemExit(main())
