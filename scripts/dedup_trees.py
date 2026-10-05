#!/usr/bin/env python3
"""最終評価の中身の重複の除去（D70 の 6、事前登録の下書き §2.12 (b)）。**走査の前に当てる。補充しない。**

2 段で使う。

1. `hash`: 木ごとに「ツールの定義を含む `.py` ファイル」の sha256 を取り、JSON に残す（中身は残さない）。

       # v4（手元の corpus/v4-*）
       .venv/bin/python scripts/dedup_trees.py hash --corpus corpus --sample docs/corpus_sample_v4.json \\
           --label v4 --out evidence/population_final/hashes_v4.json
       # v2・v3: pin から取り直した木で同じことをする（取り直した中身は消してよい。ハッシュだけ残す）
       # 今回の木
       .venv/bin/python scripts/dedup_trees.py hash --corpus corpus --sample <今回の pin> --label final \\
           --out evidence/population_final/hashes_final.json

2. `dedup`: 今回の木のハッシュと、v2〜v4 のハッシュ（`--prior` を繰り返す）から、残す木と除く木を決める。

       .venv/bin/python scripts/dedup_trees.py dedup --new evidence/population_final/hashes_final.json \\
           --prior hashes_v2.json --prior hashes_v3.json --prior hashes_v4.json \\
           --out evidence/population_final/dedup.json

「ツールの定義を含む `.py` ファイル」の決め方
=============================================

**解析器そのものの入口の発見**（`authgap.srcindex.SourceIndex` + `authgap.entries.find_units`。走査と同じ関数を
読み取りだけで呼ぶ。`authgap/` は変えない）で見つけたユニットの `relpath`（ツールの関数を**定義した**ファイル）の集合。
呼び出し形の登録（`x.add_tool(fn)`）の登録文だけがあるファイルは入れない（定義のファイルではないため）。
`--from-run <run>` を渡すと、代わりに manifest の `units[].unit.relpath` を使う（同じ関数の出力なので、
同じ解析器の版なら同じ集合になる。corpus を消した後の照合用）。どちらで取ったかは出力の `method` に残す。
ハッシュは木の中の**ファイルのバイト列**の sha256（改行や BOM を正規化しない）。

**走査と同じ Python（3.12、`.venv312`）で走らせる。** 入口の発見は `ast.parse` に頼るので、3.10 では 3.12 の構文の
ファイルが parse 失敗になり、その中のツールの定義ファイルが集合から黙って抜ける（v4 で 2 木、各 1 ファイル。
3.12 の manifest と食い違った）。出力に `python` を書き、`dedup` は入力の Python の版が揃わなければ警告を出力に残す。
parse に失敗したファイルは木ごとに `parse_failures` に残す。

規則（D70 の 6）
================

1. **v2〜v4 との重複**: 今回の木の定義ファイルのハッシュが、`--prior` のどれかの木のどれかのファイルと 1 つでも
   一致した木は除く。一致した相手（木と、ハッシュ・両方の relpath）を全部書く。
2. **今回の中の重複**: 1 で残った木を repo 名（`owner/repo` を小文字にしたもの。同じなら木の名前）の辞書順に並べ、
   前から順に見て、**既に残した木**と定義ファイルのハッシュが 1 つでも一致した木を除く（相手は一致した残した木のうち
   順で最初のもの）。既に除いた木との一致では除かない（除いた木はもう標本に無いため）。
3. 定義ファイルが 1 つも無い木（入口が見つからない）は、比べようがないので残し、`no_tool_files` に列挙する。
4. 乱数を使わない。同じ入力なら同じ出力。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from typing import Optional

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#: 走査の Python（手順書 6.1、事前登録 (c)）
SCAN_PYTHON = (3, 12)


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def tool_files_by_analyzer(tree_dir: str) -> tuple[list[str], list[str]]:
    """`(定義ファイルの relpath（ソート済み）, parse に失敗したファイル)`。解析器の入口の発見を読み取りだけで使う。"""
    if ROOT not in sys.path:
        sys.path.insert(0, ROOT)
    from authgap.entries import find_units
    from authgap.srcindex import SourceIndex

    index = SourceIndex(tree_dir)
    index.build()
    rels = sorted({u.relpath for u in find_units(index)})
    return rels, sorted(index.parse_failures)


def tool_files_from_manifest(manifest_path: str) -> list[str]:
    with open(manifest_path, encoding="utf-8") as fh:
        m = json.load(fh)
    return sorted({u["unit"]["relpath"] for u in m.get("units", []) if u.get("unit", {}).get("relpath")})


def hash_tree(tree_dir: str, rels: list[str]) -> dict[str, str]:
    out = {}
    for r in rels:
        p = os.path.join(tree_dir, r)
        if not os.path.isfile(p):
            raise FileNotFoundError(f"{tree_dir}: 定義ファイル {r} が無い（corpus と manifest の版が違う？）")
        out[r] = sha256_file(p)
    return out


def _targets(sample_path: str) -> list[tuple[str, Optional[str]]]:
    with open(sample_path, encoding="utf-8") as fh:
        s = json.load(fh)
    return [(t["name"], t.get("repo")) for t in s["targets"]]


def cmd_hash(a: argparse.Namespace) -> int:
    if not a.from_run and sys.version_info[:2] != SCAN_PYTHON:
        print(f"警告: Python {sys.version_info[0]}.{sys.version_info[1]} で入口を発見している。走査は "
              f"{SCAN_PYTHON[0]}.{SCAN_PYTHON[1]}（.venv312）。parse できるファイルが変わりうる", file=sys.stderr)
    if a.sample:
        targets = _targets(a.sample)
    else:
        prefix = a.prefix or ""
        targets = [(n, None) for n in sorted(os.listdir(a.corpus)) if n.startswith(prefix)
                   and os.path.isdir(os.path.join(a.corpus, n))]
    trees: dict = {}
    missing = []
    no_manifest: list[str] = []
    for name, repo in targets:
        d = os.path.join(a.corpus, name)
        if not os.path.isdir(d):
            missing.append(name)
            continue
        entry: dict = {"repo": repo}
        if a.from_run:
            mp = os.path.join(a.from_run, f"{name}.json")
            if not os.path.exists(mp):
                no_manifest.append(name)
                continue
            rels = tool_files_from_manifest(mp)
        else:
            rels, failures = tool_files_by_analyzer(d)
            if failures:
                entry["parse_failures"] = failures
        entry["files"] = hash_tree(d, rels)
        trees[name] = entry
        print(f"{name}: {len(rels)} files", file=sys.stderr)
    out = {"_note": "scripts/dedup_trees.py hash の出力（D70 の 6）。ツールの定義を含む .py ファイルの sha256。",
           "label": a.label,
           "method": f"manifest units[].unit.relpath（{a.from_run}）" if a.from_run
           else "authgap.entries.find_units の Unit.relpath（解析器の入口の発見）",
           "python": ".".join(str(x) for x in sys.version_info[:3]), "corpus": a.corpus, "n_trees": len(trees), "missing_trees": missing,
           **({"no_manifest_trees": no_manifest} if a.from_run else {}),
           "trees": dict(sorted(trees.items()))}
    if missing:
        print(f"警告: corpus に無い木 {len(missing)}: {missing[:10]}", file=sys.stderr)
    if no_manifest:
        print(f"警告: manifest の無い木 {len(no_manifest)}（ハッシュを取らない）: {no_manifest[:10]}", file=sys.stderr)
    _dump(out, a.out)
    return 0


def load_hashes(path: str) -> dict[str, dict]:
    """ハッシュの一覧を `{木: {"repo": ..., "files": {relpath: sha256}}}` で返す。

    受け付ける形: `hash` の出力（`{"trees": {木: {"repo", "files"}}}`）か、平たい列
    `[{"tree": 木, "relpath": ..., "sha256": ...}, ...]`（v2・v3 を別の手段で取り直したとき用）。
    """
    with open(path, encoding="utf-8") as fh:
        d = json.load(fh)
    if isinstance(d, dict) and isinstance(d.get("trees"), dict):
        out = {}
        for t, e in d["trees"].items():
            files = e.get("files")
            if not isinstance(files, dict):
                raise ValueError(f"{path}: 木 {t} に files が無い")
            out[t] = {"repo": e.get("repo"), "files": dict(files)}
        return out
    if isinstance(d, list):
        out = {}
        for i, r in enumerate(d):
            if not all(k in r for k in ("tree", "relpath", "sha256")):
                raise ValueError(f"{path}: {i} 番目に tree / relpath / sha256 が無い")
            out.setdefault(r["tree"], {"repo": r.get("repo"), "files": {}})["files"][r["relpath"]] = r["sha256"]
        return out
    raise ValueError(f"{path}: ハッシュの一覧の形が分からない")


def _check_sha(path: str, hashes: dict) -> None:
    for t, e in hashes.items():
        for r, h in e["files"].items():
            if not (isinstance(h, str) and len(h) == 64 and all(c in "0123456789abcdef" for c in h)):
                raise ValueError(f"{path}: {t}:{r} の sha256 {h!r} が 64 桁の小文字 16 進でない")


def order_key(tree: str, repo: Optional[str]) -> tuple[str, str]:
    """残す順: repo 名（`owner/repo`）を小文字にした辞書順。repo が無ければ木の名前。同じなら木の名前。"""
    return ((repo or tree).lower(), tree)


def dedup(new: dict[str, dict], prior: dict[str, dict[str, dict]]) -> dict:
    """`new`: `{木: {"repo", "files"}}`。`prior`: `{ラベル: {木: {"repo", "files"}}}`。"""
    prior_index: dict[str, list[tuple[str, str, str]]] = {}
    for label in sorted(prior):
        for t in sorted(prior[label]):
            for r, h in sorted(prior[label][t]["files"].items()):
                prior_index.setdefault(h, []).append((label, t, r))
    order = sorted(new, key=lambda t: order_key(t, new[t].get("repo")))
    pos = {t: i for i, t in enumerate(order)}
    kept: list[str] = []
    kept_hash: dict[str, str] = {}  # ハッシュ → それを持つ最初の残した木
    excluded = []
    no_files = []
    for t in order:
        files = new[t]["files"]
        if not files:
            no_files.append(t)
        prior_matches = [{"hash": h, "relpath": r, "prior_label": pl, "prior_tree": pt, "prior_relpath": pr}
                         for r, h in sorted(files.items()) for pl, pt, pr in prior_index.get(h, [])]
        if prior_matches:
            first = min(prior_matches, key=lambda m: (m["prior_label"], m["prior_tree"], m["prior_relpath"], m["relpath"]))
            excluded.append({"tree": t, "repo": new[t].get("repo"), "reason": "prior",
                             "partner": f"{first['prior_label']}:{first['prior_tree']}", "hash": first["hash"],
                             "relpath": first["relpath"], "partner_relpath": first["prior_relpath"],
                             "all_matches": prior_matches})
            continue
        within = sorted({(pos[kept_hash[h]], kept_hash[h], h, r) for r, h in files.items() if h in kept_hash})
        if within:
            _pos, partner, h, r = within[0]
            excluded.append({"tree": t, "repo": new[t].get("repo"), "reason": "within_new", "partner": partner,
                             "hash": h, "relpath": r,
                             "partner_relpath": sorted(pr for pr, ph in new[partner]["files"].items() if ph == h)[0],
                             "all_matches": [{"hash": hh, "relpath": rr, "kept_tree": pp} for _p, pp, hh, rr in within]})
            continue
        kept.append(t)
        for h in files.values():
            kept_hash.setdefault(h, t)
    return {
        "n_new": len(new), "n_kept": len(kept), "n_excluded": len(excluded),
        "n_excluded_prior": sum(1 for e in excluded if e["reason"] == "prior"),
        "n_excluded_within_new": sum(1 for e in excluded if e["reason"] == "within_new"),
        "kept": kept, "excluded": excluded, "no_tool_files": no_files,
        "prior_trees": {label: len(v) for label, v in sorted(prior.items())},
    }


def _hash_meta(path: str) -> tuple[Optional[str], Optional[str]]:
    with open(path, encoding="utf-8") as fh:
        d = json.load(fh)
    if isinstance(d, dict):
        return d.get("python"), d.get("method")
    return None, None


def cmd_dedup(a: argparse.Namespace) -> int:
    metas = {p: _hash_meta(p) for p in [a.new, *a.prior]}
    warnings = []
    pyminor = {p: ".".join(v.split(".")[:2]) for p, (v, _m) in metas.items() if v}
    if len(set(pyminor.values())) > 1:
        warnings.append(f"ハッシュの一覧の Python の版が揃わない: {pyminor}")
    if len({m for _v, m in metas.values()}) > 1:
        warnings.append(f"ハッシュの一覧の取り方（method）が揃わない: { {p: m for p, (_v, m) in metas.items()} }")
    for w in warnings:
        print(f"警告: {w}", file=sys.stderr)
    new = load_hashes(a.new)
    _check_sha(a.new, new)
    prior: dict = {}
    for p in a.prior:
        label = os.path.splitext(os.path.basename(p))[0]
        if label in prior:
            raise ValueError(f"--prior のラベル {label} が重なる（ファイル名を変える）")
        prior[label] = load_hashes(p)
        _check_sha(p, prior[label])
    res = dedup(new, prior)
    out = {"_note": "scripts/dedup_trees.py dedup の出力（D70 の 6）。走査の前に当てる。補充しない。",
           "new": a.new, "prior": a.prior, "inputs_meta": {p: {"python": v, "method": m} for p, (v, m) in metas.items()},
           "warnings": warnings,
           "rule": "v2〜v4 と定義ファイルの sha256 が 1 つでも一致 → 除く。残りを repo 名（小文字）の辞書順に見て、"
                   "既に残した木と 1 つでも一致 → 除く", **res}
    _dump(out, a.out)
    print(f"新しい木 {res['n_new']}: 残す {res['n_kept']}、除く {res['n_excluded']}"
          f"（v2〜v4 と一致 {res['n_excluded_prior']}、今回の中で一致 {res['n_excluded_within_new']}）。"
          f"定義ファイルの無い木 {len(res['no_tool_files'])}", file=sys.stderr)
    return 0


def _dump(obj: dict, path: Optional[str]) -> None:
    text = json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=False) + "\n"
    if path:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
    else:
        sys.stdout.write(text)


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    h = sub.add_parser("hash", help="木ごとの定義ファイルの sha256 を取る")
    h.add_argument("--corpus", required=True)
    h.add_argument("--sample", help="pin の JSON（targets[].name / repo）。無ければ --prefix で corpus を列挙")
    h.add_argument("--prefix", help="--sample が無いときの木の名前の接頭辞（例 v4-）")
    h.add_argument("--from-run", help="解析器を呼ばず、この run の manifest の units[].unit.relpath を使う")
    h.add_argument("--label", required=True)
    h.add_argument("--out")
    d = sub.add_parser("dedup", help="残す木と除く木を決める")
    d.add_argument("--new", required=True)
    d.add_argument("--prior", action="append", default=[], help="v2〜v4 のハッシュ（繰り返す）")
    d.add_argument("--out")
    a = ap.parse_args(argv)
    return cmd_hash(a) if a.cmd == "hash" else cmd_dedup(a)


if __name__ == "__main__":
    raise SystemExit(main())
