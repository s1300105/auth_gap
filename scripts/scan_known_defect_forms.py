#!/usr/bin/env python3
"""D19 の既知の欠陥 K1〜K7 の形が、F0a 標本の木に構文上いくつあるかを数える（上限値の近似）。

**構文だけの走査である。** ユニットから到達するか、解析器が実際にその形で誤るかは見ない。
「その形が標本に 0 件」は言えるが、「この数だけ誤った」とは読まない（テスト・スクリプトも数える）。

形（`docs/decisions.md` D19 の「結果」の表）:

* K1 ``pipe_spawn_from_module_name``: `Popen` / `create_subprocess_*` の argv か `shell=` がモジュール水準の
  名前で、同じファイルに pipe 書き込み（`.stdin.write(...)` / `.communicate(...)`）がある
* K2 / K3 ``global_rebinds_module_def``: 関数内の `global f` で、モジュール直下の def `f` を入れ子 def か
  代入で書き換え、ファイル内で `f(...)` と呼ぶ
* K4 ``method_nested_def_shadows_module_def``: メソッドの中の入れ子 def と同名のモジュール直下の def を、
  同じメソッドの中の入れ子関数から素の名前で呼ぶ
* K5 ``enclosing_import_shadows_module_def``: 囲む関数の局所 import と同名のモジュール直下の def を、
  入れ子関数から素の名前で呼ぶ
* K6 ``deep_module_dict_write``: 3 段以上入れ子のモジュール水準 dict に、3 段以上の添字で書き込む
* K7 ``aliased_in_tree_import_call``: `from X import f as g`（g != f）で木内のモジュールの def `f` を指し、
  ファイル内で `g(...)` と呼ぶ。相対 import の基点は、`__init__.py` ではそのパッケージ自身

**数を信じる前に走査器を確かめる**（`tests/test_f0a_defects.py` 15 節の fixture で各形を検出し、
K7 の別名なしの対照を検出しないこと）::

    python scripts/scan_known_defect_forms.py --self-test

使い方::

    python scripts/scan_known_defect_forms.py                              # run 6 の analyzed 木
    python scripts/scan_known_defect_forms.py --trees evidence/f0a_run5/trees.jsonl
    python scripts/scan_known_defect_forms.py --roots corpus/<木> ... --examples 20
"""

from __future__ import annotations

import argparse
import ast
import importlib.util
import json
import os
import sys
import tempfile
import textwrap
import warnings
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

SKIP_DIRS = frozenset({".git", "node_modules", "__pycache__", ".venv", "venv", "site-packages"})

FORMS = (
    "pipe_spawn_from_module_name",
    "global_rebinds_module_def",
    "method_nested_def_shadows_module_def",
    "enclosing_import_shadows_module_def",
    "deep_module_dict_write",
    "aliased_in_tree_import_call",
)


def _parse_tree(root: str) -> dict[str, ast.Module]:
    files: dict[str, ast.Module] = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for fn in sorted(filenames):
            if not fn.endswith(".py"):
                continue
            path = os.path.join(dirpath, fn)
            try:
                with open(path, "rb") as fh, warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    files[os.path.relpath(path, root)] = ast.parse(fh.read())
            except (SyntaxError, ValueError, RecursionError, MemoryError):
                continue
    return files


def _module_level_defs(body: list, out: set[str]) -> None:
    for n in body:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            out.add(n.name)
        elif isinstance(n, (ast.If, ast.Try, ast.With)):
            nested = list(getattr(n, "body", [])) + list(getattr(n, "orelse", [])) + list(getattr(n, "finalbody", []))
            nested += [s for h in getattr(n, "handlers", []) for s in h.body]
            _module_level_defs(nested, out)


def _own_nodes(fn: ast.AST):
    """関数本体のうち、入れ子の関数 / クラス / lambda の中を除くノード。"""
    stack = list(getattr(fn, "body", []))
    while stack:
        n = stack.pop()
        yield n
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
            continue
        stack.extend(ast.iter_child_nodes(n))


def _bare_calls(node: ast.AST) -> set[str]:
    return {n.func.id for n in ast.walk(node) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}


def _dict_depth(v: ast.AST) -> int:
    if isinstance(v, ast.Dict):
        return 1 + max([_dict_depth(x) for x in v.values if x is not None] or [0])
    return 0


def _subscript_base(t: ast.AST) -> tuple[int, str | None]:
    depth = 0
    while isinstance(t, ast.Subscript):
        depth += 1
        t = t.value
    return depth, (t.id if isinstance(t, ast.Name) else None)


def _module_name(rel: str) -> str:
    dotted = rel[:-3].replace(os.sep, ".")
    if dotted == "__init__":
        return ""
    return dotted[: -len(".__init__")] if dotted.endswith(".__init__") else dotted


def _relative_base(rel: str) -> str:
    """相対 import の基点。`pkg/__init__.py` ではパッケージ自身（`pkg`）、`pkg/mod.py` では `pkg`。"""
    name = _module_name(rel)
    return name if os.path.basename(rel) == "__init__.py" else name.rpartition(".")[0]


def scan_tree(root: str) -> dict[str, list[tuple]]:
    """木 1 本の形ごとの候補 `(relpath, lineno, 詳細)`。"""
    files = _parse_tree(root)
    top_defs = {
        _module_name(rel): {n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
        for rel, tree in files.items()
    }
    hits: dict[str, list[tuple]] = defaultdict(list)
    for rel, tree in files.items():
        mdefs: set[str] = set()
        _module_level_defs(tree.body, mdefs)
        mnames = {t.id for n in tree.body if isinstance(n, ast.Assign) for t in n.targets if isinstance(t, ast.Name)}
        called = _bare_calls(tree)
        classes = [c for c in ast.walk(tree) if isinstance(c, ast.ClassDef)]
        for f in (n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))):
            own = list(_own_nodes(f))
            for name in sorted({nm for n in own if isinstance(n, ast.Global) for nm in n.names} & mdefs):
                rebinds = any(
                    (isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name)
                    or (isinstance(n, ast.Assign) and any(isinstance(x, ast.Name) and x.id == name for x in n.targets))
                    for n in own
                )
                if rebinds and name in called:
                    hits["global_rebinds_module_def"].append((rel, f.lineno, name))
            inner_funcs = [n for n in own if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
            local_defs = {n.name for n in inner_funcs}
            local_imports = {
                (a.asname or a.name).split(".")[0] for n in own if isinstance(n, (ast.Import, ast.ImportFrom)) for a in n.names
            }
            is_method = any(f in c.body for c in classes)
            for inner in inner_funcs:
                stored = {x.id for x in ast.walk(inner) if isinstance(x, ast.Name) and isinstance(x.ctx, ast.Store)}
                stored |= {a.arg for a in inner.args.args}
                for name in sorted((_bare_calls(inner) & mdefs) - stored):
                    if name in local_imports:
                        hits["enclosing_import_shadows_module_def"].append((rel, inner.lineno, name))
                    if is_method and name in local_defs and name != inner.name:
                        hits["method_nested_def_shadows_module_def"].append((rel, inner.lineno, name))
        has_pipe = any(
            isinstance(n, ast.Call)
            and isinstance(n.func, ast.Attribute)
            and (
                (n.func.attr == "write" and isinstance(n.func.value, ast.Attribute) and n.func.value.attr == "stdin")
                or (n.func.attr == "communicate" and (n.args or any(k.arg == "input" for k in n.keywords)))
            )
            for n in ast.walk(tree)
        )
        if has_pipe:
            for n in ast.walk(tree):
                if not isinstance(n, ast.Call):
                    continue
                name = n.func.attr if isinstance(n.func, ast.Attribute) else getattr(n.func, "id", "")
                if name not in ("Popen", "create_subprocess_exec", "create_subprocess_shell"):
                    continue
                argv = n.args[0] if n.args else None
                shell = next((k.value for k in n.keywords if k.arg == "shell"), None)
                if isinstance(argv, ast.Name) and argv.id in mnames:
                    hits["pipe_spawn_from_module_name"].append((rel, n.lineno, f"argv={argv.id}"))
                elif isinstance(shell, ast.Name) and shell.id in mnames:
                    hits["pipe_spawn_from_module_name"].append((rel, n.lineno, f"shell={shell.id}"))
        deep = {
            n.targets[0].id
            for n in tree.body
            if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)
            and _dict_depth(n.value) >= 3
        }
        for n in ast.walk(tree):
            if isinstance(n, (ast.Assign, ast.AugAssign)):
                for t in n.targets if isinstance(n, ast.Assign) else [n.target]:
                    depth, base = _subscript_base(t)
                    if depth >= 3 and base in deep:
                        hits["deep_module_dict_write"].append((rel, n.lineno, base))
        rel_base = _relative_base(rel)
        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom):
                continue
            if node.level:
                base = rel_base
                for _ in range(node.level - 1):
                    base = base.rpartition(".")[0]
                target = ".".join(x for x in (base, node.module or "") if x)
                modules = [target] if target in top_defs else []
            else:
                m = node.module or ""
                modules = [d for d in top_defs if d == m or d.endswith("." + m)]
            for a in node.names:
                if a.asname and a.asname != a.name and a.asname in called and any(a.name in top_defs[d] for d in modules):
                    kind = "relative" if node.level else "absolute"
                    hits["aliased_in_tree_import_call"].append((rel, node.lineno, f"{a.name} as {a.asname} ({kind})"))
    return hits


def _report(targets: list[tuple[str, str]], examples: int) -> None:
    per_form: dict[str, list[tuple]] = defaultdict(list)
    for population, root in targets:
        for form, rows in scan_tree(root).items():
            per_form[form] += [(population, os.path.basename(os.path.normpath(root))) + r for r in rows]
    print(f"木 {len(targets)} 本")
    for form in FORMS:
        rows = per_form.get(form, [])
        trees = Counter(pop for pop, _tree in {(r[0], r[1]) for r in rows})
        sites = Counter(r[0] for r in rows)
        print(f"  {form}: 箇所 {len(rows)} / 木 {sum(trees.values())}  箇所の内訳 {dict(sites)}  木の内訳 {dict(trees)}")
        for r in rows[:examples]:
            print("      ", r)


def _self_test() -> int:
    """`tests/test_f0a_defects.py` 15 節の fixture で、各形を検出すること（と K7 の対照を検出しないこと）を確かめる。"""
    spec = importlib.util.spec_from_file_location("_known_fixtures", os.path.join(ROOT, "tests", "test_f0a_defects.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    in_package_init = {
        "pkg/__init__.py": "from .net import fetch_url as http_get\n\ndef fetch(url):\n    return http_get(url)\n",
        "pkg/net.py": mod._ALIAS_NET,
    }
    cases = [
        ("pipe_argv0", {"s.py": mod.PIPE_ARGV0_FROM_MODULE_LIST}, "pipe_spawn_from_module_name", True),
        ("pipe_shell", {"s.py": mod.PIPE_SHELL_FROM_REBOUND_NAME}, "pipe_spawn_from_module_name", True),
        ("global_nested_def", mod.KNOWN_SCOPE_FORMS["global_nested_def"], "global_rebinds_module_def", True),
        ("global_assign", mod.KNOWN_SCOPE_FORMS["global_assign"], "global_rebinds_module_def", True),
        ("method_nested_def", mod.KNOWN_SCOPE_FORMS["method_nested_def"], "method_nested_def_shadows_module_def", True),
        ("enclosing_import", mod.KNOWN_SCOPE_FORMS["enclosing_import"], "enclosing_import_shadows_module_def", True),
        ("deep_dict", {"s.py": mod.DEEP_MODULE_DICT_URL}, "deep_module_dict_write", True),
        ("alias_relative", mod._alias_import_files("relative"), "aliased_in_tree_import_call", True),
        ("alias_absolute", mod._alias_import_files("absolute"), "aliased_in_tree_import_call", True),
        ("alias_in_package_init", in_package_init, "aliased_in_tree_import_call", True),
        ("alias_plain_control", mod._alias_import_files("plain"), "aliased_in_tree_import_call", False),
    ]
    failed = 0
    with tempfile.TemporaryDirectory() as tmp:
        for name, files, form, expect in cases:
            root = os.path.join(tmp, name)
            for rel, content in files.items():
                path = os.path.join(root, rel)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(textwrap.dedent(content))
            found = bool(scan_tree(root).get(form))
            ok = found == expect
            failed += not ok
            print(f"{'ok  ' if ok else 'FAIL'} {name}: {form} {'検出' if found else '非検出'}（期待: {'検出' if expect else '非検出'}）")
    print("走査器の自己検査: " + ("通過" if not failed else f"**{failed} 件失敗。数を使わないこと**"))
    return 1 if failed else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--trees", default="evidence/f0a_run6/trees.jsonl", help="status=analyzed の木を走査する")
    ap.add_argument("--roots", nargs="*", help="木のディレクトリを直接渡す（母集団は 'roots'）")
    ap.add_argument("--examples", type=int, default=0, help="形ごとに表示する候補の件数")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return _self_test()
    if args.roots:
        targets = [("roots", r) for r in args.roots]
    else:
        path = args.trees if os.path.isabs(args.trees) else os.path.join(ROOT, args.trees)
        with open(path, encoding="utf-8") as fh:
            rows = [json.loads(line) for line in fh]
        targets = [(r["population"], os.path.join(ROOT, "corpus", r["tree"])) for r in rows if r.get("status") == "analyzed"]
    _report(targets, args.examples)
    return 0


if __name__ == "__main__":
    sys.exit(main())
