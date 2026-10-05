#!/usr/bin/env python3
"""判定の 1 件について、解析器が何を見たかを manifest から 1 画面に出す（`docs/final_evaluation_procedure.md` 6.5、
手引き 手順 B・18.2 の 4・18A.2 の 2）。

    .venv/bin/python scripts/show_target.py <manifest> <ユニットの relpath> <ユニットの行> [<site>] [--decl D1] [--kind FS_WRITE]

* ユニットは **relpath と行で探す**（qualname だけだと、別のファイルにある同名のツールを取り違える。D64 / U50）。
  見つからなければ、その relpath にあるユニットの一覧を出して終了コード 1。同じ位置に複数のユニットがあれば全部を出す。
* `site` を渡すとその site の効果と行だけを出す。省くと全部（見落としの判定の 18.2 の 4 で、対象の宣言の
  `contradiction_unknown` を探すとき）。`--kind` で効果の種類も絞れる。
* 宣言の印: ユニットが明示した宣言（D1〜D4。解析器が矛を判定するときと同じ条件）と、行ごとに D1〜D4 の
  矛 / 不（理由つき）を出す。`--decl` を渡すとその宣言の印だけを出す。
"""

from __future__ import annotations

import argparse
import json
import sys

DECLS = ("D1", "D2", "D3", "D4")
#: slot の根は長くなりうる（数百）ので、既定ではこの数だけ出す（`--full` で全部）
MAX_ROOTS = 8


def declared(dk: dict) -> list[str]:
    ex = set(dk.get("explicit") or [])
    out = []
    if "readOnlyHint" in ex:
        out.append("D1")
    if "destructiveHint" in ex:
        out.append("D2")
    if dk.get("closed_world"):
        out.append("D3")
    if dk.get("idempotent"):
        out.append("D4")
    return out


def row_marks(notes: list[str], decls: tuple[str, ...]) -> list[str]:
    """行の注記から D1〜D4 の印（`D1=矛(fs_write)` / `D2=不(net_post)`）を作る。印の無い宣言は出さない。"""
    out = []
    for d in decls:
        contra = sorted(n.split(":", 2)[2] for n in notes if n.startswith(f"contradiction_reason:{d}:"))
        unknown = sorted(n.split(":", 2)[2] for n in notes if n.startswith(f"contradiction_unknown:{d}:"))
        if contra or any(n == f"contradiction:{d}" for n in notes):
            out.append(f"{d}=矛({','.join(contra)})")
        if unknown:
            out.append(f"{d}=不({','.join(unknown)})")
    return out


def find_units(m: dict, relpath: str, lineno: int) -> list[dict]:
    return [u for u in m.get("units", []) if u["unit"].get("relpath") == relpath and u["unit"].get("lineno") == lineno]


def show(m: dict, relpath: str, lineno: int, site: str | None = None, decl: str | None = None,
         kind: str | None = None, full: bool = False, out=sys.stdout) -> int:
    units = find_units(m, relpath, lineno)
    if not units:
        print(f"{relpath}:{lineno} にユニットが無い。", file=out)
        cands = sorted((u["unit"].get("lineno") or -1, u["unit"]["qualname"]) for u in m.get("units", [])
                       if u["unit"].get("relpath") == relpath)
        if cands:
            print(f"{relpath} にあるユニット: " + ", ".join(f"{q}:{ln}" for ln, q in cands), file=out)
        else:
            print(f"{relpath} にはユニットが 1 つも無い（relpath は木の根からの相対パス）。", file=out)
        return 1
    if len(units) > 1:
        print(f"注意: {relpath}:{lineno} にユニットが {len(units)} つある（全部を出す）。", file=out)
    decls = (decl,) if decl else DECLS
    for u in units:
        info = u["unit"]
        dk = u.get("D_kind") or {}
        print("=" * 72, file=out)
        print("ツール:", info.get("tool_name"), " qualname:", info["qualname"],
              " 定義:", f'{info.get("relpath")}:{info.get("lineno")}', " 宣言:", info.get("annotations"), file=out)
        print("明示された宣言:", dk.get("explicit"), " 宣言の印:", declared(dk) or "なし",
              " 打ち切り:", u.get("cap_hits"), " opaque:", u.get("opaque_reasons"), file=out)
        trunc = [n for n in (u.get("notes") or []) if str(n).startswith("TRUNCATED")]
        if trunc:
            print("打ち切りの印:", trunc, file=out)
        n_eff = 0
        for e in u.get("effects") or []:
            if (site and e.get("site") != site) or (kind and e.get("kind") != kind):
                continue
            n_eff += 1
            print("---- 効果", e.get("kind"), e.get("site"), f'{e.get("relpath")}:{e.get("lineno")}', file=out)
            print("  入口の呼び出し行:", e.get("entry_lineno"),
                  " 道筋:", " -> ".join(e.get("witness_chain") or []) or "(本体の中)", file=out)
            for name, s in (e.get("slots") or {}).items():
                roots = s.get("roots") or []
                shown = roots if full or len(roots) <= MAX_ROOTS else [*roots[:MAX_ROOTS], f"…ほか {len(roots) - MAX_ROOTS}"]
                print(f"  slot {name}: 主体={s.get('prin')} 確度={s.get('prov')} 根={shown}", file=out)
        n_row = 0
        for r in u.get("rows") or []:
            if (site and r.get("site") != site) or (kind and r.get("kind") != kind):
                continue
            marks = row_marks(r.get("notes") or [], decls)
            if decl and not marks:
                continue
            n_row += 1
            print("  行", f'{r.get("relpath")}:{r.get("lineno")}', r.get("kind"), r.get("site"), r.get("slot"),
                  marks or "印なし", file=out)
        print(f"（効果 {n_eff}、行 {n_row}）", file=out)
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("manifest")
    ap.add_argument("relpath", help="ユニットの relpath（木の根から）")
    ap.add_argument("lineno", type=int, help="ユニットの行")
    ap.add_argument("site", nargs="?", help="効果の site（省くと全部）")
    ap.add_argument("--decl", choices=DECLS)
    ap.add_argument("--kind")
    ap.add_argument("--full", action="store_true", help="slot の根を省略せずに全部出す")
    a = ap.parse_args(argv)
    with open(a.manifest, encoding="utf-8") as fh:
        m = json.load(fh)
    return show(m, a.relpath, a.lineno, a.site, a.decl, a.kind, a.full)


if __name__ == "__main__":
    raise SystemExit(main())
