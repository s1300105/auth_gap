#!/usr/bin/env python3
"""宣言 D の全数調査（`docs/preregistration.md` §2.8 段 A の機械化）。

**規則の定義点は §2.8 であり、本ファイルはその適用である。** 族の定義・分母を
変えるときは先に §2.8 を直し、§5 に逸脱として記録する。

    .venv/bin/python scripts/declaration_census.py --run evidence/f0a_run6 --out evidence/decl_census_run6

出力:
  trees.jsonl   木ごとの族別ヒット（src / non-src 別）とパーサの読み取り数
  hits.jsonl    ヒット 1 件 = 1 行（tree, relpath, path_class, family, lineno, detail）
  summary.json  族別・path_class 別の集計と判定規則の適用結果
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from denominators import path_class  # noqa: E402

#: §2.8 (a) の族。**合算しない。**
FAMILIES: dict[str, re.Pattern] = {
    "mcp_hint_key": re.compile(r"\b(readOnlyHint|destructiveHint|idempotentHint|openWorldHint)\b"),
    "mcp_ToolAnnotations": re.compile(r"\bToolAnnotations\b"),
    "openhands_ToolDefinition": re.compile(r"\bToolDefinition\s*\("),
    "agno_confirmation": re.compile(r"\b(requires_confirmation|external_execution)\b"),
    "openai_needs_approval": re.compile(r"\b(needs_approval|require_approval)\b"),
}
#: 族 3（AST）: keyword `annotations=` を持つ呼び出しで、被呼び出し名の末尾がこれ。
ANNOTATIONS_CALLEE_SUFFIX = ("tool", "Tool", "add_tool", "ToolDefinition")

#: 同梱 SDK / 仮想環境は non-src（§2.8 (a) 分母）。
VENDORED_MARKERS = ("site-packages", "node_modules", "/.venv/", "/venv/", "/mcp/server/", "/mcp/types.py")


def _dotted(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _dotted(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return ""


def _value_form(node: ast.AST) -> str:
    if node is None:
        return "missing"
    if isinstance(node, ast.Constant) and node.value is None:
        return "None"
    if isinstance(node, ast.Call):
        name = _dotted(node.func).split(".")[-1]
        return "ToolAnnotations" if name == "ToolAnnotations" else f"call:{name}"
    if isinstance(node, ast.Dict):
        return "dict"
    if isinstance(node, ast.Name):
        return "Name"
    return type(node).__name__


def scan_file(path: str, rel: str, tree_name: str, pclass: str) -> tuple[list[dict], bool]:
    """1 ファイルのヒット列と parse 可否。**バイト列で読み ast.parse にバイト列で渡す。**"""
    try:
        raw = open(path, "rb").read()
    except OSError:
        return [], False
    text = raw.decode("utf-8", errors="replace")
    hits: list[dict] = []
    for fam, rx in FAMILIES.items():
        for i, line in enumerate(text.splitlines(), 1):
            m = rx.search(line)
            if m:
                hits.append({"tree": tree_name, "relpath": rel, "path_class": pclass, "family": fam,
                             "lineno": i, "detail": m.group(0)})
    try:
        mod = ast.parse(raw, filename=rel)
    except (SyntaxError, ValueError, RecursionError):
        return hits, False
    for node in ast.walk(mod):
        if not isinstance(node, ast.Call):
            continue
        callee = _dotted(node.func)
        if not callee.endswith(ANNOTATIONS_CALLEE_SUFFIX):
            continue
        for kw in node.keywords:
            if kw.arg == "annotations":
                hits.append({"tree": tree_name, "relpath": rel, "path_class": pclass,
                             "family": "mcp_annotations_kwarg", "lineno": node.lineno,
                             "detail": f"{callee}(annotations={_value_form(kw.value)})"})
    return hits, True


def scan_tree(tree_dir: str, tree_name: str) -> tuple[list[dict], dict]:
    hits: list[dict] = []
    n_py = n_parsed = 0
    for dp, dns, fns in os.walk(tree_dir):
        dns[:] = [d for d in dns if d != ".git"]
        for fn in fns:
            if not fn.endswith(".py"):
                continue
            full = os.path.join(dp, fn)
            rel = os.path.relpath(full, tree_dir)
            pclass = path_class(rel)
            if any(mk in "/" + rel for mk in VENDORED_MARKERS):
                pclass = "vendored"
            n_py += 1
            h, ok = scan_file(full, rel, tree_name, pclass)
            n_parsed += ok
            hits.extend(h)
    return hits, {"n_py": n_py, "n_parsed": n_parsed}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", default="evidence/f0a_run6")
    ap.add_argument("--corpus", default="corpus")
    ap.add_argument("--out", default="evidence/decl_census_run6")
    args = ap.parse_args()

    trees = [json.loads(line) for line in open(os.path.join(ROOT, args.run, "trees.jsonl"), encoding="utf-8") if line.strip()]
    # パーサが読んだ annotations（run6 の units.jsonl）
    parsed_ann: dict[str, int] = {}
    with open(os.path.join(ROOT, args.run, "units.jsonl"), encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            u = json.loads(line)
            if u.get("annotations_present"):
                parsed_ann[u["tree"]] = parsed_ann.get(u["tree"], 0) + 1

    out_dir = os.path.join(ROOT, args.out)
    os.makedirs(out_dir, exist_ok=True)
    all_hits: list[dict] = []
    rows: list[dict] = []
    missing = 0
    for t in trees:
        d = os.path.join(ROOT, args.corpus, t["tree"])
        if not os.path.isdir(d):
            rows.append({"tree": t["tree"], "population": t["population"], "status": "missing"})
            missing += 1
            continue
        hits, meta = scan_tree(d, t["tree"])
        all_hits.extend(hits)
        by = {}
        for h in hits:
            key = f"{h['family']}:{'src' if h['path_class'] == 'src' else 'non_src'}"
            by[key] = by.get(key, 0) + 1
        rows.append({"tree": t["tree"], "population": t["population"], "status": "ok", "sha": t.get("commit_sha"),
                     **meta, "hits": by, "parser_annotations_present": parsed_ann.get(t["tree"], 0),
                     "n_tool_literals_run6": t.get("n_tool_literals", 0)})
        print(f"  {t['tree']:44s} py={meta['n_py']:4d} hits={sum(by.values()):3d} {by}")

    with open(os.path.join(out_dir, "trees.jsonl"), "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    with open(os.path.join(out_dir, "hits.jsonl"), "w", encoding="utf-8") as fh:
        for h in all_hits:
            fh.write(json.dumps(h, ensure_ascii=False, sort_keys=True) + "\n")

    fams = list(FAMILIES) + ["mcp_annotations_kwarg"]
    summary = {"_note": "docs/preregistration.md §2.8 段 A の出力。族は合算しない。", "n_trees": len(trees),
               "n_trees_missing": missing, "families": {}}
    for fam in fams:
        fh_ = [h for h in all_hits if h["family"] == fam]
        src = [h for h in fh_ if h["path_class"] == "src"]
        summary["families"][fam] = {
            "hits_total": len(fh_), "hits_src": len(src), "hits_non_src": len(fh_) - len(src),
            "trees_src": sorted({h["tree"] for h in src}), "trees_non_src": sorted({h["tree"] for h in fh_ if h["path_class"] != "src"}),
            "files_src": sorted({(h["tree"], h["relpath"]) for h in src}).__len__(),
        }
    # 判定規則（§2.8 (a)）: 族 1〜3 の src ヒットがパーサ未読の木
    core = {"mcp_hint_key", "mcp_ToolAnnotations", "mcp_annotations_kwarg"}
    src_trees = {h["tree"] for h in all_hits if h["family"] in core and h["path_class"] == "src"}
    unread = sorted(t for t in src_trees if parsed_ann.get(t, 0) == 0)
    summary["rule"] = {
        "core_families": sorted(core),
        "trees_with_src_hits": sorted(src_trees),
        "trees_with_src_hits_parser_unread": unread,
        "verdict": ("parser_recall_defect" if unread else ("no_src_declarations" if not src_trees else "all_read")),
    }
    with open(os.path.join(out_dir, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write("\n")
    print()
    for fam, v in summary["families"].items():
        print(f"  {fam:26s} total {v['hits_total']:4d}  src {v['hits_src']:4d} (木 {len(v['trees_src'])})  non-src {v['hits_non_src']:4d} (木 {len(v['trees_non_src'])})")
    print(f"\n判定: {summary['rule']['verdict']}  src ヒット木 {len(src_trees)}  うちパーサ未読 {len(unread)}: {unread}")
    print(f"-> {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
