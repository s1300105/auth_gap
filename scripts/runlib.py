"""full scan の run ディレクトリを読む評価の道具が共有する部分（D64 / U50・U52）。

**manifest の集合は `summary.json` の `trees` のうち `status == "ok"` の木で決める**（ファイル名の形には頼らない）。
以前は各 script がディレクトリの `.json` を名前で拾っており、`contradiction_by_decl.py` は名前に「-」の無い
manifest を黙って読み飛ばし、同じ label で走らせ直すと標本から外れた木の古い manifest を数えていた
（R5-r1-4 / R5-r2-7。どちらも数え落とし・上乗せの向き）。

* summary.json に無いのにディレクトリにある manifest（余分）と、summary.json にあるのにファイルが無い木（不足）は
  **警告として返す**（黙って数えない・黙って落とさない）。
* summary.json の無い書きかけの run は、今までどおりディレクトリを列挙し、`units` 鍵の無い .json を飛ばす
  （手書きの notes.json で KeyError にしない。検証役の反例）。

ユニットの鍵（U50 / R5-r1-3）: **(木, ユニットの relpath, ユニットの行, qualname)**。`unit_id` と qualname は木の中で
一意でない（O13）ので、別モジュールの同名ツールの矛が 1 件に潰れていた。1 ユニットの中で (site, kind) /
(site, slot) を畳む設計（O18）は変えない。
"""

from __future__ import annotations

import json
import os

_NOT_MANIFESTS = frozenset({"summary.json", "contradictions.json"})


def run_manifests(run_dir: str) -> tuple[list[tuple[str, str]], list[str]]:
    """`([(木の名前, manifest のパス), ...], 警告)` を返す。順は木の名前の順。"""
    warnings: list[str] = []
    present = {fn[:-5] for fn in os.listdir(run_dir) if fn.endswith(".json") and fn not in _NOT_MANIFESTS}
    spath = os.path.join(run_dir, "summary.json")
    if os.path.exists(spath):
        with open(spath, encoding="utf-8") as fh:
            summary = json.load(fh)
        ok = [t["tree"] for t in summary.get("trees", []) if t.get("status") == "ok"]
        missing = sorted(t for t in ok if t not in present)
        extra = sorted(present - set(ok))
        if missing:
            warnings.append(f"summary.json で ok なのに manifest が無い木 {len(missing)}: {', '.join(missing[:10])}")
        if extra:
            # manifest 以外の手書きの .json もここに入るが、どちらにしても数えない
            warnings.append(f"summary.json に無いファイル {len(extra)}（数えない）: {', '.join(extra[:10])}")
        names = sorted(t for t in ok if t in present)
    else:
        warnings.append(f"{run_dir} に summary.json が無い。ディレクトリの .json を列挙する（書きかけの run の可能性）")
        names = []
        for t in sorted(present):
            try:
                with open(os.path.join(run_dir, f"{t}.json"), encoding="utf-8") as fh:
                    if "units" in json.load(fh):
                        names.append(t)
            except (OSError, ValueError):
                warnings.append(f"{t}.json を読めない（飛ばす）")
    return [(t, os.path.join(run_dir, f"{t}.json")) for t in names], warnings


def load_manifest(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def unit_key(tree: str, unit: dict) -> tuple:
    """ユニットの鍵 (木, relpath, 行, qualname)。`unit` は manifest の `u["unit"]`。"""
    return (tree, unit.get("relpath"), unit.get("lineno"), unit["qualname"])


def row_decls(row: dict) -> list[str]:
    """CONTRADICTION 行が反した宣言。注記 `contradiction:<宣言>` が無ければ `?`（落とさない。R5-r3-3）。"""
    ds = sorted({n.split(":")[1] for n in row.get("notes", []) if n.startswith("contradiction:")})
    return ds or ["?"]


def print_warnings(warnings: list[str], label: str = "") -> None:
    import sys

    for w in warnings:
        print(f"警告{('（' + label + '）') if label else ''}: {w}", file=sys.stderr)
