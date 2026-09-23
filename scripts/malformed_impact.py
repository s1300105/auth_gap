#!/usr/bin/env python3
"""snake_case の注釈が **camelCase だったら判定が変わったか**を測る（O27 / D48）。

`DKind.malformed` はキー名しか持たない（仕様書 322 行目が求めるのは「別行で報告」まで）。
**値まで見ないと「宣言が届いていたら矛盾だったか」は分からない。** この script は

1. full scan の manifest から、`malformed` を持つユニットの**効果**を取る。
2. **同じ木のソースを読み直して**注釈の snake_case キーと**値**を拾い、
   camelCase に読み替えた `DKind` を作る。
3. その `DKind` と効果で `dparse.contradiction` を評価し、
   **「綴りが正しければ CONTRADICTION だったユニット」**を数える。

**解析器は変えない。** ここで読み替えるのは測定のためだけで、
`authgap` 本体は snake_case を宣言として扱わない（扱うと protocol に届いていないものを
届いたものとして扱う誤 clear になる）。

    .venv/bin/python scripts/malformed_impact.py evidence/scan_v2_run6
"""

from __future__ import annotations

import argparse
import ast
import collections
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from authgap.catalog.sinks import DANGEROUS_KINDS  # noqa: E402
from authgap.dparse import contradiction, d_kind_from  # noqa: E402
from authgap.entries import SNAKE_ALIASES  # noqa: E402


class _Eff:
    """`dparse.contradiction` が見る最小の効果（kind と destructive だけ）。"""

    def __init__(self, kind: str, destructive):
        self.kind = kind
        self.destructive = destructive


def _pairs_of(v: ast.AST) -> dict:
    """`annotations=` の値ノードから `{キー: 値}` を読む（辞書 / `ToolAnnotations(...)`）。"""
    pairs: dict = {}
    if isinstance(v, ast.Dict):
        for k, val in zip(v.keys, v.values, strict=False):
            if isinstance(k, ast.Constant) and isinstance(k.value, str):
                try:
                    pairs[k.value] = ast.literal_eval(val)
                except Exception:  # noqa: BLE001
                    pass
    elif isinstance(v, ast.Call):
        for k2 in v.keywords:
            if k2.arg is None:
                continue
            try:
                pairs[k2.arg] = ast.literal_eval(k2.value)
            except Exception:  # noqa: BLE001
                pass
    return pairs


def _annotations_by_lineno(tree: ast.AST) -> dict[int, dict]:
    """**関数ごと**に `annotations=` を拾う（`関数の lineno -> {キー: 値}`）。

    **ファイル単位で拾ってはいけない。** 1 つのファイルに複数のツールがあると、
    別のツールの注釈を当ててしまう。初版はこれで 7 件と数え、目視で 2 件が
    `destructive_hint=True`（著者の宣言自体は正しい）の取り違えだった。
    """
    out: dict[int, dict] = {}
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for dec in node.decorator_list:
            if not isinstance(dec, ast.Call):
                continue
            for kw in dec.keywords:
                if kw.arg == "annotations":
                    pairs = _pairs_of(kw.value)
                    if pairs:
                        out[node.lineno] = pairs
    return out


def _to_camel(pairs: dict) -> dict:
    """snake_case を camelCase に読み替える（**測定のためだけ**）。"""
    out = {}
    for k, v in pairs.items():
        out[SNAKE_ALIASES.get(k, k)] = v
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("scan_dir")
    args = ap.parse_args(argv)
    scan = args.scan_dir if os.path.isabs(args.scan_dir) else os.path.join(ROOT, args.scan_dir)

    c: collections.Counter = collections.Counter()
    hidden: list[tuple] = []
    for fn in sorted(os.listdir(scan)):
        if not fn.endswith(".json") or fn in ("summary.json", "contradictions.json"):
            continue
        tree_name = fn[:-5]
        with open(os.path.join(scan, fn), encoding="utf-8") as fh:
            man = json.load(fh)
        targets = {u["unit"]["qualname"]: u for u in man["units"]
                   if (u.get("D_kind") or {}).get("malformed")}
        if not targets:
            continue
        # その木のソースから、**関数の lineno ごと**に注釈の値を拾う
        by_rel: dict[str, dict[int, dict]] = {}
        root = os.path.join(ROOT, "corpus", tree_name)
        for u in targets.values():
            rel = u["unit"]["relpath"]
            if rel in by_rel:
                continue
            path = os.path.join(root, rel)
            try:
                with open(path, "rb") as fh:
                    by_rel[rel] = _annotations_by_lineno(ast.parse(fh.read()))
            except Exception:  # noqa: BLE001
                by_rel[rel] = {}
        for q, u in targets.items():
            c["malformed を持つユニット"] += 1
            effs = [_Eff(e["kind"], e.get("destructive")) for e in u.get("effects", [])
                    if e["kind"] in DANGEROUS_KINDS]
            if not effs:
                continue
            c["うち危険効果あり"] += 1
            # **そのユニットの関数自身の注釈だけを見る**（lineno で一致させる）。
            pairs = by_rel.get(u["unit"]["relpath"], {}).get(u["unit"].get("lineno"))
            if not pairs or not any(k in SNAKE_ALIASES for k in pairs):
                c["注釈を lineno で対応づけられなかった"] += 1 if not pairs else 0
                continue
            dk = d_kind_from(_to_camel(pairs), "dict")
            if dk.explicit and contradiction(dk, effs):
                c["**綴りが正しければ CONTRADICTION**"] += 1
                hidden.append((tree_name, q, sorted({e.kind for e in effs}), dict(pairs),
                               [e["site"] for e in u.get("effects", [])][:3]))
    print(f"scan: {os.path.relpath(scan, ROOT)}")
    for k, v in c.most_common():
        print(f"  {v:5d}  {k}")
    print("\n綴りが正しければ CONTRADICTION だったユニット:")
    for t, q, kinds, pairs, sites in hidden:
        print(f"  {t} / {q}")
        print(f"      書かれた注釈: {pairs}")
        print(f"      効果: {kinds} / {sites}")
    print("\n**対応づけは関数の lineno で行う。** ファイル単位で拾うと別のツールの注釈を"
          "当ててしまう（初版はこれで 7 件と数え、目視で 2 件が取り違えだった）。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
