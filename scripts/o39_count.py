"""O39（仕様書の sink 語彙に無い HTTP のメソッドと本体の引数）の規模を構文で数える（D59）。

**上限の目安であって効果の件数ではない。** 受け手の型は見ない（`x.delete(...)` の `x` が
httpx / requests のセッションかは確かめない）。

手続き:
- 対象: `--run` の full scan と同じ木（`evidence/<run>/v2-*.json` の名前。`corpus/v2-*` の全部ではない）。
  テストファイル（`authgap.srcindex.is_test_path`）は除く。ソースは `ast.parse` にバイト列で渡す。
- (a) モジュール関数: `httpx.put|patch|delete|head|options(...)`、`requests.options(...)`
  （`import httpx` / `import requests` の名前のまま呼ぶ形だけ）。
- (b) セッションのメソッドの**上限**: `httpx` か `requests` を import するファイルの中の、属性呼び出し
  `<式>.put|patch|delete|head|options(...)`（受け手の型は問わない）。
- (c) 本体の引数: (a)(b) と、sink 表にある HTTP 呼び出しの形（`.get|post|request(...)` と
  `requests.*` / `httpx.*`）で、キーワード `content=` か `files=` を持つもの。
- 分母: 木の数（その run の木すべて）と、(a)〜(c) が 1 件以上ある木の数を併記する。
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from authgap.srcindex import is_test_path  # noqa: E402

METHODS = {"put", "patch", "delete", "head", "options"}
SPEC_METHODS = {"get", "post", "request"}
BODY_KWS = {"content", "files"}


def count_tree(tree_dir: str) -> Counter:
    c: Counter = Counter()
    for dp, dns, fns in os.walk(tree_dir):
        dns[:] = [d for d in dns if d not in {".git", "node_modules", ".venv", "venv", "__pycache__"}]
        for fn in fns:
            if not fn.endswith(".py"):
                continue
            path = os.path.join(dp, fn)
            rel = os.path.relpath(path, tree_dir)
            if is_test_path(rel):
                continue
            try:
                mod = ast.parse(open(path, "rb").read())
            except (SyntaxError, ValueError):
                continue
            imports = set()
            for n in ast.walk(mod):
                if isinstance(n, ast.Import):
                    imports.update(a.name.split(".")[0] for a in n.names)
                elif isinstance(n, ast.ImportFrom) and n.module:
                    imports.add(n.module.split(".")[0])
            http_file = bool(imports & {"httpx", "requests"})
            for n in ast.walk(mod):
                if not isinstance(n, ast.Call) or not isinstance(n.func, ast.Attribute):
                    continue
                attr = n.func.attr
                base = n.func.value.id if isinstance(n.func.value, ast.Name) else None
                kws = {k.arg for k in n.keywords if k.arg}
                is_module_fn = base in {"httpx", "requests"}
                if is_module_fn and (attr in METHODS and not (base == "requests" and attr != "options")):
                    c["a_module_fn"] += 1
                    c[f"a_module_fn:{attr}"] += 1
                elif http_file and not is_module_fn and attr in METHODS:
                    c["b_session_method_upper"] += 1
                    c[f"b_session_method_upper:{attr}"] += 1
                if (is_module_fn or (http_file and attr in METHODS | SPEC_METHODS)) and kws & BODY_KWS:
                    c["c_body_kw_upper"] += 1
    return c


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=os.path.join(ROOT, "corpus"))
    ap.add_argument("--run", default=os.path.join(ROOT, "evidence", "scan_v2_run16"))
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    trees = sorted(f[:-5] for f in os.listdir(a.run) if f.startswith("v2-") and f.endswith(".json"))
    per: dict[str, dict] = {}
    total: Counter = Counter()
    for t in trees:
        c = count_tree(os.path.join(a.corpus, t))
        if c:
            per[t] = dict(c)
        total.update(c)
    out = {
        "run": os.path.relpath(a.run, ROOT),
        "n_trees": len(trees),
        "trees_with": {k: sum(1 for v in per.values() if v.get(k)) for k in ("a_module_fn", "b_session_method_upper", "c_body_kw_upper")},
        "total": dict(sorted(total.items())),
        "per_tree": per,
    }
    s = json.dumps(out, ensure_ascii=False, indent=1)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(s + "\n")
    print(json.dumps({k: out[k] for k in ("run", "n_trees", "trees_with", "total")}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
