"""矛・不の 1 組について、ツールの本体から効果の行までの「道筋」に出てくる関数だけを、1 つの画面に並べて出す。

判定の手順 C〜D（本体から効果の位置までたどる）で、関数を 1 つずつ探して開く手間を省くための**読む補助**。
解析器の道筋（manifest の `witness_chain`）を地図として使い、その名前の関数の定義を木の中から探して、
ソースを行番号つきで出す。印:

* `▶` … 次の段の関数を呼んでいる行（本体では、解析器が記録した入口の呼び出し行）
* `★` … 効果の行（ファイルを書く・消すなど）
* `?` … 条件の行（`if` / `elif` / `else` / `try` / `except` / `for` / `while` / `with` / `return` / `raise`）。
  効果に届くかどうかは、たいていこの行で決まる

**注意**: これは解析器の道筋をなぞった表示で、正しいとは限らない（同じ名前の関数が複数あれば候補を全部出す。
解析器が呼び出し先を取り違えていることもある＝誤の原因 E3）。判定の根拠は、自分で開いて確かめた行だけにする。
**見落としの判定では、18.2 の 1〜3 を終えるまで使わない**（解析器の出力を元にしているため）。

    .venv/bin/python scripts/path_view.py <manifest> <木のフォルダ> <ユニットの relpath> <ユニットの行> <site> [--decl D1]

例（練習の P-C08）:

    .venv/bin/python scripts/path_view.py evidence/scan_v2_v4_run1/v4-twelvetake-studios__reaper-mcp.json \\
        corpus/v4-twelvetake-studios__reaper-mcp reaper_mcp_server.py 605 pathlib.Path.unlink --decl D2
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import sys

COND = ("if ", "elif ", "else:", "try:", "except", "finally:", "for ", "async for ", "while ", "with ",
        "async with ", "return", "raise", "break", "continue")
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", "site-packages"}


def _defs_in_tree(root: str) -> dict[str, list[tuple[str, int, int, str]]]:
    """木の中の関数定義: 名前（`f` と `Class.f`）→ [(relpath, 開始行, 終了行, qualname)]。"""
    out: dict[str, list[tuple[str, int, int, str]]] = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if not fn.endswith(".py"):
                continue
            path = os.path.join(dirpath, fn)
            rel = os.path.relpath(path, root)
            try:
                with open(path, "rb") as fh:  # バイト列で渡す（BOM 付きのファイルを落とさない。CLAUDE.md）
                    tree = ast.parse(fh.read())
            except (SyntaxError, ValueError):
                continue

            def visit(node, prefix: str, rel: str = rel) -> None:
                for ch in ast.iter_child_nodes(node):
                    if isinstance(ch, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        start = min([ch.lineno] + [d.lineno for d in ch.decorator_list])
                        q = f"{prefix}{ch.name}"
                        rec = (rel, start, ch.end_lineno or ch.lineno, q)
                        out.setdefault(ch.name, []).append(rec)
                        if prefix:
                            out.setdefault(q, []).append(rec)
                        visit(ch, f"{q}.")
                    elif isinstance(ch, ast.ClassDef):
                        visit(ch, f"{prefix}{ch.name}.")
                    else:
                        visit(ch, prefix)

            visit(tree, "")
    return out


def _find(defs: dict, name: str) -> list[tuple[str, int, int, str]]:
    """道筋の名前から定義を探す。`A.b` ならクラス A のメソッド b を先に、無ければ末尾名 b で探す。"""
    if name in defs and "." in name:
        return defs[name]
    tail = name.split(".")[-1]
    cands = defs.get(tail, [])
    if "." in name:  # 末尾が一致し、qualname の末尾も一致するものを先に
        exact = [c for c in cands if c[3].endswith(name)]
        if exact:
            return exact
    return cands


def _lines(root: str, rel: str) -> list[str]:
    with open(os.path.join(root, rel), encoding="utf-8", errors="replace") as fh:
        return fh.read().split("\n")


def _show(root: str, rel: str, start: int, end: int, call_names: list[str], call_lines: set[int],
          effect_lines: set[int]) -> str:
    src = _lines(root, rel)
    out = []
    for i in range(start, min(end, len(src)) + 1):
        text = src[i - 1]
        s = text.strip()
        mark = " "
        if i in effect_lines:
            mark = "★"
        elif i in call_lines or any(f"{n}(" in s for n in call_names if n):
            mark = "▶"
        elif s.startswith(COND):
            mark = "?"
        out.append(f"{mark} {i:5d}  {text}")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("manifest")
    ap.add_argument("tree_dir", help="corpus/<木の名前>")
    ap.add_argument("relpath")
    ap.add_argument("lineno", type=int)
    ap.add_argument("site")
    ap.add_argument("--decl", choices=["D1", "D2", "D3", "D4"], help="その宣言の矛か不の印のある行の効果だけ")
    a = ap.parse_args()

    m = json.load(open(a.manifest, encoding="utf-8"))
    units = [u for u in m["units"] if u["unit"]["relpath"] == a.relpath and u["unit"]["lineno"] == a.lineno]
    if not units:
        print(f"ユニットが見つからない: {a.relpath}:{a.lineno}", file=sys.stderr)
        return 1
    defs = _defs_in_tree(a.tree_dir)
    for u in units:
        info = u["unit"]
        marked: set[tuple[str, int]] | None = None
        if a.decl:
            marked = set()
            for r in u.get("rows") or []:
                if r.get("site") == a.site and any(str(n).startswith("contradiction") and f":{a.decl}" in str(n)
                                                    for n in r.get("notes") or []):
                    marked.add((r["relpath"], r["lineno"]))
        # 同じ道筋（入口の行・関数の列）ごとにまとめる
        paths: dict[tuple, set[tuple[str, int]]] = {}
        for e in u["effects"]:
            if e["site"] != a.site:
                continue
            if marked is not None and (e["relpath"], e["lineno"]) not in marked:
                continue
            chain = e.get("witness_chain") or []
            if isinstance(chain, str):
                chain = ast.literal_eval(chain)
            paths.setdefault((e.get("entry_lineno"), tuple(chain)), set()).add((e["relpath"], e["lineno"]))
        print("=" * 100)
        print(f"ツール {info['tool_name']}  本体 {info['relpath']}:{info['lineno']}  宣言 {info.get('annotations')}")
        effects_all = sorted({x for v in paths.values() for x in v})
        print("効果の行: " + ", ".join(f"{r}:{ln}" for r, ln in effects_all))
        print(f"\n【1】道筋の一覧（解析器が通った関数の列。{len(paths)} 本）")
        entries: set[int] = set()
        nexts: dict[str, set[str]] = {}  # 関数 → その中で呼ぶ次の段の名前
        order: list[str] = []
        body_key = "（本体）"
        for n, ((entry, chain), effects) in enumerate(sorted(paths.items(), key=lambda kv: (kv[0][0] or 0, kv[0][1])), 1):
            if entry:
                entries.add(entry)
            seq = [body_key] + list(chain)
            print(f"  道筋 {n}: 本体の {entry} 行 → " + " → ".join(chain or ["（本体の中）"])
                  + "  → 効果 " + ", ".join(f"{r}:{ln}" for r, ln in sorted(effects)))
            for i, name in enumerate(seq):
                if name not in order:
                    order.append(name)
                if i + 1 < len(seq):
                    nexts.setdefault(name, set()).add(seq[i + 1].split(".")[-1])
        print("\n【2】関数のソース（道筋に出てくる順に 1 回ずつ。深さは道筋によって違うので一覧で確かめる）")
        eff_set = set(effects_all)
        for name in order:
            if name == body_key:
                cands = [d for d in _find(defs, info["qualname"]) if d[0] == info["relpath"]] or \
                        [d for d in defs.get(info["qualname"].split(".")[-1], []) if d[0] == info["relpath"]]
                title = f"本体 {info['qualname']}"
                calls = entries
            else:
                cands = _find(defs, name)
                title = name
                calls = set()
            print("\n" + "-" * 100)
            print(f"■ {title}" + ("" if len(cands) == 1 else f"  （同じ名前の定義が {len(cands)} 個。全部出す）"))
            if not cands:
                print("（木の中に定義が見つからなかった。木の外のライブラリか、動的な呼び出し）")
            for rel, s_, e_, q in cands:
                here = {ln for r, ln in eff_set if r == rel and s_ <= ln <= e_}
                print(f"[{q}  {rel}:{s_}-{e_}]")
                print(_show(a.tree_dir, rel, s_, e_, sorted(nexts.get(name, set())), calls, here))
    print("\n印: ▶ 次の段を呼ぶ行  ★ 効果の行  ? 条件の行（届くかはたいていここで決まる）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
