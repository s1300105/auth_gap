#!/usr/bin/env python3
"""実態調査の名簿を、解析器を使わずに作り、seed ⑦ で順番の列を抜き取る（D85。D82 の名簿づくりの改訂）。

**`authgap/` を import しない。** 名簿は解析器から独立に作る（解析器が入口を見つけ損ねたツールも名簿に入る）。

名簿の規則（D85）:

1. 木の中の `.py` ファイルのうち、パスの分類が `src` のもの（`scripts/sample_population_v2.py` の `cls`。テスト・例・
   同梱のライブラリなどを除く。母集団 v2 の枠と同じ分類）を、Python の `ast` で読む（バイト列で渡す）。
2. **D1 の宣言**を探す。次の 3 つの書き方で、値が定数の `True` のもの:
   - 呼び出しのキーワード `readOnlyHint=True`（`ToolAnnotations(readOnlyHint=True)` など）
   - 呼び出しのキーワード `read_only_hint=True`（snake_case の版）
   - 辞書のキー `"readOnlyHint": True`
3. その宣言がどのツールのものかを、次の順で決める（1 件の宣言が複数のツールに使われていれば、ツールごとに 1 件）:
   - `decorator`: 関数のデコレータの呼び出しの中にある → その関数
   - `name`: モジュールの一番上で名前に代入され（`RO = ToolAnnotations(readOnlyHint=True)`）、同じファイルのデコレータか
     `add_tool(...)` の呼び出しの引数にその名前がある → その関数
   - `add_tool`: `<何か>.add_tool(fn, ...)` の呼び出しの中にある → 最初の引数の関数
   - `tool_ctor`: `Tool(name="...", ...)` の呼び出しの中にある（低水準のサーバ）→ `name` の文字列
   - `call_register`: `mcp.tool(annotations=...)(fn)` のように、ツールを登録する呼び出しの結果を関数に当てている → その関数
   - `dict_registry`: 自前の表（辞書）に書いた宣言。同じ辞書（または宣言を値に持つ外側の辞書）の `handler` / `func` /
     `function` / `fn` の値の関数、無ければ `name` の文字列、無ければ外側の辞書のキーの文字列 → それ
   - どれでもない → `unmapped`（ツールを決められない宣言）。名簿には入れ、判定者が読んでツールを決める。ツールの宣言で
     なければ判定で「対象外」とする（件数を報告する）
4. 名簿の 1 件 = (木, ツールを定義した場所, ツールの名前, 宣言の場所)。

    # 名簿を作る（取得・重複の除去の後。--keep は残す木の一覧の JSON。無ければ corpus の下の名前が一致する木を全部）
    .venv312/bin/python scripts/survey_roster.py build --corpus corpus --prefix final- \\
        --keep evidence/population_final/dedup.json --out evidence/population_final/survey_roster.json
    # 順番の列を抜き取る（seed ⑦。木を並べ、各木から 1 件）
    .venv312/bin/python scripts/survey_roster.py sample evidence/population_final/survey_roster.json \\
        --seed <⑦> --n 200 --out evidence/population_final/survey_targets.json

決定論: 木・ファイル・件をソートしてから `random.Random(seed)` を 1 本使う（`rng_order` に書く）。同じ Python で走らせる。
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from sample_population_v2 import cls  # noqa: E402  （authgap/ を使わない分類）

RO_KEYWORDS = ("readOnlyHint", "read_only_hint")
RO_DICT_KEY = "readOnlyHint"


def _is_true(node: ast.AST) -> bool:
    return isinstance(node, ast.Constant) and node.value is True


def _contains_ro(node: ast.AST) -> list[ast.AST]:
    """部分木の中の D1 の宣言（`readOnlyHint=True` のキーワード、`"readOnlyHint": True` の辞書）の節点。"""
    found = []
    for n in ast.walk(node):
        if isinstance(n, ast.Call):
            for kw in n.keywords:
                if kw.arg in RO_KEYWORDS and _is_true(kw.value):
                    found.append(kw.value)
        elif isinstance(n, ast.Dict):
            for k, v in zip(n.keys, n.values, strict=True):
                if isinstance(k, ast.Constant) and k.value == RO_DICT_KEY and _is_true(v):
                    found.append(v)
    return found


def _names_in(node: ast.AST) -> set[str]:
    return {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}


def _callee_attr(call: ast.Call) -> str | None:
    f = call.func
    if isinstance(f, ast.Attribute):
        return f.attr
    if isinstance(f, ast.Name):
        return f.id
    return None


def _fn_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def declarations(src: bytes, relpath: str) -> list[dict]:
    """1 ファイルの D1 の宣言を、ツールに結びつけて返す。parse に失敗したら SyntaxError を投げる。"""
    tree = ast.parse(src, filename=relpath)
    out: list[dict] = []
    used: set[int] = set()  # ツールに結びつけた宣言の節点（id）

    # name: モジュールの一番上で、D1 の宣言を含む式を代入した名前
    ro_names: dict[str, list[ast.AST]] = {}
    for st in tree.body:
        if isinstance(st, ast.Assign):
            ros = _contains_ro(st.value)
            if ros:
                for t in st.targets:
                    if isinstance(t, ast.Name):
                        ro_names.setdefault(t.id, []).extend(ros)
        elif isinstance(st, ast.AnnAssign) and st.value is not None and isinstance(st.target, ast.Name):
            ros = _contains_ro(st.value)
            if ros:
                ro_names.setdefault(st.target.id, []).extend(ros)

    def add(form: str, tool: str | None, def_line: int | None, ros: list[ast.AST]) -> None:
        for r in ros:
            used.add(id(r))
        out.append({"relpath": relpath, "form": form, "tool": tool, "def_lineno": def_line,
                    "decl_lineno": min(getattr(r, "lineno", 0) for r in ros) if ros else None})

    parent: dict[int, ast.AST] = {}
    for n in ast.walk(tree):
        for ch in ast.iter_child_nodes(n):
            parent[id(ch)] = n

    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Call) and n.args \
                and _callee_attr(n.func) in ("tool", "add_tool", "register_tool"):
            ros = _contains_ro(n.func)
            hit = sorted(_names_in(n.func) & set(ro_names))
            if ros or hit:
                add("call_register", _fn_name(n.args[0]), n.lineno, ros + [r for h in hit for r in ro_names[h]])
                continue
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for dec in n.decorator_list:
                if not isinstance(dec, ast.Call):
                    continue
                ros = _contains_ro(dec)
                if ros:
                    add("decorator", n.name, n.lineno, ros)
                    continue
                hit = sorted(_names_in(dec) & set(ro_names))
                if hit:
                    add("name", n.name, n.lineno, [r for h in hit for r in ro_names[h]])
        elif isinstance(n, ast.Call):
            attr = _callee_attr(n)
            if attr == "add_tool" and n.args:
                ros = _contains_ro(n)
                hit = sorted(_names_in(ast.Module(body=[ast.Expr(k.value) for k in n.keywords], type_ignores=[]))
                             & set(ro_names))
                if ros or hit:
                    add("add_tool" if ros else "name", _fn_name(n.args[0]), n.lineno,
                        ros + [r for h in hit for r in ro_names[h]])
            elif attr == "Tool":
                ros = _contains_ro(n)
                if ros:
                    name = next((k.value.value for k in n.keywords
                                 if k.arg == "name" and isinstance(k.value, ast.Constant)), None)
                    add("tool_ctor", name, n.lineno, ros)

    # dict_registry: 自前の表に書いた宣言
    def _dict_key(d: ast.Dict, key: str) -> ast.AST | None:
        for k, v in zip(d.keys, d.values, strict=True):
            if isinstance(k, ast.Constant) and k.value == key:
                return v
        return None

    def _tool_of_dict(d: ast.Dict) -> str | None:
        for key in ("handler", "func", "function", "fn"):
            v = _dict_key(d, key)
            if v is not None and _fn_name(v):
                return _fn_name(v)
        v = _dict_key(d, "name")
        if isinstance(v, ast.Constant) and isinstance(v.value, str):
            return v.value
        return None

    for n in ast.walk(tree):
        if not isinstance(n, ast.Dict):
            continue
        ros = [v for k, v in zip(n.keys, n.values, strict=True)
               if isinstance(k, ast.Constant) and k.value == RO_DICT_KEY and _is_true(v) and id(v) not in used]
        if not ros:
            continue
        cur: ast.AST = n
        tool = None
        for _ in range(3):  # 宣言の辞書 → 外側の辞書（"annotations": {...}）→ 表の辞書（"tool_name": {...}）まで
            if isinstance(cur, ast.Dict):
                tool = _tool_of_dict(cur)
                if tool:
                    break
            par = parent.get(id(cur))
            if isinstance(par, ast.Dict):
                for k, v in zip(par.keys, par.values, strict=True):
                    if v is cur and isinstance(k, ast.Constant) and isinstance(k.value, str) \
                            and k.value != "annotations":
                        tool = k.value
                if tool:
                    break
            if par is None:
                break
            cur = par
        if tool:
            add("dict_registry", tool, n.lineno, ros)

    # どのツールにも結びつかなかった宣言（名前に代入しただけで使い先が同じファイルに無いものを含む）
    for n in sorted(_contains_ro(tree), key=lambda r: (getattr(r, "lineno", 0), getattr(r, "col_offset", 0))):
        if id(n) not in used:
            out.append({"relpath": relpath, "form": "unmapped", "tool": None, "def_lineno": None,
                        "decl_lineno": getattr(n, "lineno", None)})
    # 同じツール・同じ定義の行は 1 件にまとめる（1 つのデコレータに宣言が 2 回書いてある形など）
    seen, uniq = set(), []
    for e in out:
        key = (e["form"] if e["form"] == "unmapped" else "tool", e["tool"], e["def_lineno"],
               e["decl_lineno"] if e["form"] == "unmapped" else None)
        if key not in seen:
            seen.add(key)
            uniq.append(e)
    return uniq


def build_tree(tree_dir: str, tree: str) -> dict:
    entries, failures, n_files = [], [], 0
    for dp, dns, fns in os.walk(tree_dir):
        dns[:] = sorted(d for d in dns if d != ".git")
        for fn in sorted(fns):
            if not fn.endswith(".py"):
                continue
            rel = os.path.relpath(os.path.join(dp, fn), tree_dir).replace(os.sep, "/")
            if cls(rel) != "src":
                continue
            n_files += 1
            with open(os.path.join(dp, fn), "rb") as fh:
                src = fh.read()
            try:
                for e in declarations(src, rel):
                    entries.append({"tree": tree, **e})
            except (SyntaxError, ValueError) as exc:
                failures.append({"relpath": rel, "error": f"{type(exc).__name__}: {exc}"[:200]})
    entries.sort(key=lambda e: (e["relpath"], e["def_lineno"] or 0, e["decl_lineno"] or 0, e["tool"] or ""))
    return {"tree": tree, "n_src_py": n_files, "entries": entries, "parse_failures": failures}


def cmd_build(a) -> int:
    keep = None
    if a.keep:
        with open(a.keep, encoding="utf-8") as fh:
            k = json.load(fh)
        keep = set(k.get("kept") or k.get("keep") or k.get("trees") or [])
        if not keep:
            raise SystemExit(f"{a.keep} に残す木の一覧（kept / keep / trees）が無い")
    trees = sorted(t for t in os.listdir(a.corpus) if t.startswith(a.prefix) and os.path.isdir(os.path.join(a.corpus, t)))
    if keep is not None:
        missing = sorted(keep - set(trees))
        trees = [t for t in trees if t in keep]
    else:
        missing = []
    per_tree = [build_tree(os.path.join(a.corpus, t), t) for t in trees]
    entries = [e for p in per_tree for e in p["entries"]]
    out = {
        "_note": "実態調査の名簿（D85）。解析器を使わずに、src の .py の D1 の宣言（readOnlyHint=True・read_only_hint=True・"
                 "\"readOnlyHint\": True）を ast で探し、ツールに結びつけた。form = decorator / name / add_tool / tool_ctor / unmapped。",
        "python": sys.version.split()[0], "corpus": a.corpus, "prefix": a.prefix, "keep": a.keep,
        "n_trees_scanned": len(per_tree), "keep_missing_in_corpus": missing,
        "n_trees_with_entries": sum(1 for p in per_tree if p["entries"]),
        "n_entries": len(entries),
        "n_entries_by_form": {f: sum(1 for e in entries if e["form"] == f)
                              for f in ("decorator", "name", "add_tool", "tool_ctor", "call_register", "dict_registry",
                                        "unmapped")},
        "n_parse_failures": sum(len(p["parse_failures"]) for p in per_tree),
        "trees": per_tree,
    }
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print(json.dumps({k: out[k] for k in ("n_trees_scanned", "n_trees_with_entries", "n_entries", "n_entries_by_form",
                                          "n_parse_failures")}, ensure_ascii=False))
    return 0


def sample(roster: dict, seed: int, n: int) -> dict:
    by_tree = {p["tree"]: p["entries"] for p in roster["trees"] if p["entries"]}
    rng = random.Random(seed)
    order = sorted(by_tree)
    rng.shuffle(order)
    targets = []
    for k, t in enumerate(order[:n]):
        es = by_tree[t]
        e = es[rng.randrange(len(es))]
        targets.append({"seq": k + 1, "pair_id": f"S-{k + 1:03d}", **e, "tree": t, "n_entries_in_tree": len(es)})
    return {
        "_note": "実態調査の順番の列（D82・D85）。列の順に判定し、最低 100・最大 200 件（段階 B1 で確定）。判定の前にコミットする。"
                 "判定表には解析器の出力の欄を載せない。",
        "kind": "survey", "seed": seed, "seed_role": "⑦ 実態調査の抜き取り",
        "rng_order": "random.Random(seed) を 1 本。(1) 名簿のある木を名前の順に並べて shuffle、(2) 先頭から n 木について、"
                     "その木の名簿（relpath・定義の行・宣言の行・名前の順）から randrange で 1 件。",
        "python": sys.version.split()[0], "n_trees_in_roster": len(by_tree), "n": n,
        "n_targets": len(targets), "targets": targets,
    }


def cmd_sample(a) -> int:
    with open(a.roster, encoding="utf-8") as fh:
        roster = json.load(fh)
    out = sample(roster, a.seed, a.n)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print(json.dumps({k: out[k] for k in ("n_trees_in_roster", "n", "n_targets")}, ensure_ascii=False))
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--corpus", default=os.path.join(ROOT, "corpus"))
    b.add_argument("--prefix", required=True, help="木の名前の接頭辞（例 final-）")
    b.add_argument("--keep", help="残す木の一覧の JSON（kept / keep / trees のどれかの欄）")
    b.add_argument("--out", required=True)
    s = sub.add_parser("sample")
    s.add_argument("roster")
    s.add_argument("--seed", type=int, required=True)
    s.add_argument("--n", type=int, default=200)
    s.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    return cmd_build(a) if a.cmd == "build" else cmd_sample(a)


if __name__ == "__main__":
    raise SystemExit(main())
