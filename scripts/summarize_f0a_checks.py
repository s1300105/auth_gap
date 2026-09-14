#!/usr/bin/env python3
"""F0a run の事前点検（原ソースに当てた機械点検）の結果を集計して文書にする。

入力: `evidence/f0a/check_results.json`（点検ワークフローの戻り値をそのまま保存したもの）
      `evidence/f0a/check_sample.json`（seed 固定の検証標本。`sample_f0a_checks.py`）
出力: `docs/f0a_checks.md`

**点検者の返答をそのまま信用しない。** 次を機械的に確かめ、合わない件は
「照合不一致」として別に出す（集計には入れない）:

* 各件の (層, index) が標本に存在すること
* 返された `tree` が標本のその件の木と一致すること
* 返された `site` が標本のその件のサイト（効果層は効果の relpath:lineno、
  ユニット層は入口の relpath:lineno）と一致すること
* 標本の全件にちょうど 1 つの判定があること（**抜けと重複を数える**）

**これは C2 のラベルではない**（D14）。論文に載せる検証は学生が手で行う。
"""

from __future__ import annotations

import argparse
import collections
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EFFECT_LAYERS = ("OPQ", "RES")


def expected_site(layer: str, item: dict) -> str:
    if layer in EFFECT_LAYERS:
        e = item["effect"]
        return f"{e['relpath']}:{e['lineno']}"
    return f"{item['unit_relpath']}:{item['unit_lineno']}"


def reconcile(sample: dict, results: list[dict]) -> tuple[list[dict], list[str]]:
    """標本と点検結果を突き合わせる。`(採用した件, 問題の記述)` を返す。"""
    problems: list[str] = []
    seen: collections.Counter = collections.Counter()
    accepted: list[dict] = []
    for r in results:
        layer, idx = r.get("stratum"), r.get("index")
        items = sample["items"].get(layer)
        if items is None or not isinstance(idx, int) or not (0 <= idx < len(items)):
            problems.append(f"標本に無い件: stratum={layer!r} index={idx!r}")
            continue
        want = items[idx]
        site_want = expected_site(layer, want)
        # site は "relpath:lineno" の後ろに説明が付くことがあるので前方一致で見る。
        if r.get("tree") != want["tree"] or not str(r.get("site", "")).startswith(site_want):
            # **照合できない判定はその件の判定として数えない**（下で「抜け」にもなる）。
            problems.append(
                f"照合不一致 {layer}[{idx}]: 返答 {r.get('tree')} {r.get('site')} / "
                f"標本 {want['tree']} {site_want}"
            )
            continue
        seen[(layer, idx)] += 1
        if seen[(layer, idx)] > 1:
            continue  # **重複は最初の 1 件だけ採る**（集計で 2 回数えない）
        accepted.append(r)
    for layer, items in sample["items"].items():
        for i in range(len(items)):
            if seen[(layer, i)] == 0:
                problems.append(f"判定の抜け {layer}[{i}]")
            elif seen[(layer, i)] > 1:
                problems.append(f"判定の重複 {layer}[{i}]（{seen[(layer, i)]} 件）")
    return accepted, problems


def write_md(sample: dict, data: dict, accepted: list[dict], problems: list[str], out: str) -> None:
    lines = [
        "# F0a run 1 の事前点検（原ソースに当てた機械点検）",
        "",
        "**これは C2 のラベルではない**（`docs/decisions.md` D14）。解析器の欠陥を",
        "見つけるための点検であり、論文に載せる検証は学生が",
        "`docs/verification_guide.md` §3.1 の手順で行う。",
        "",
        f"標本: `evidence/f0a/check_sample.json`（seed {sample['seed']}）。",
        f"層ごとの母集団 {sample['pool_sizes']}、抽出 "
        f"{ {k: len(v) for k, v in sample['items'].items()} }。",
        "結果の生データ: `evidence/f0a/check_results.json`。",
        "",
        "## 照合",
        "",
        f"採用 {len(accepted)} 件。**照合の問題 {len(problems)} 件**（集計に入れていない）:",
        "",
    ]
    lines += [f"- {p}" for p in problems] or ["- なし"]
    lines += [
        "",
        "## 読み方の注意（`docs/decisions.md` D17）",
        "",
        "- **VAL 層の analyzer_wrong は解析器の欠陥ではない。** 点検プロンプトは",
        "  「拒否の形で使われているか」を基準にしたが、§6 F0a の validator 形状は",
        "  **構文的**で、語彙に `split` と `ctor_path` を含む。この層の数は",
        "  「構文的形状の保有が実際の検証を表さない率」として読む。",
        "- unit id の衝突（同じツールの複製）は §5.1 の定義どおり。",
        "- カタログに無いツールの形は直さず、取りこぼしとして件数を報告する。",
        "",
        "## 層ごとの判定", "", "| 層 | 件数 | analyzer_correct | analyzer_wrong | by_design_scope | undecidable |",
        "|---|---|---|---|---|---|",
    ]
    by_layer: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    for r in accepted:
        by_layer[r["stratum"]][r["verdict"]] += 1
    for layer in sample["items"]:
        c = by_layer[layer]
        lines.append(
            f"| {layer} | {sum(c.values())} | {c['analyzer_correct']} | {c['analyzer_wrong']} | "
            f"{c['by_design_scope']} | {c['undecidable']} |"
        )
    lines += ["", "## 欠陥の分類（analyzer_wrong のみ）", "",
              "| defect_category | 誤りの向き | 件数 | 件 |", "|---|---|---|---|"]
    cats: dict[tuple[str, str], list[str]] = collections.defaultdict(list)
    for r in accepted:
        if r["verdict"] == "analyzer_wrong":
            cats[(r["defect_category"], r["error_direction"])].append(f"{r['stratum']}[{r['index']}]")
    for (cat, direction), refs in sorted(cats.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        lines.append(f"| `{cat}` | {direction} | {len(refs)} | {', '.join(refs)} |")
    if not cats:
        lines.append("| — | — | 0 | — |")

    lines += ["", "## 1 件ずつ", ""]
    for r in sorted(accepted, key=lambda r: (list(sample["items"]).index(r["stratum"]), r["index"])):
        lines.append(f"### {r['stratum']}[{r['index']}] `{r['tree']}` `{r['site']}`")
        lines.append("")
        lines.append(f"- 判定: **{r['verdict']}**（{r['defect_category']}, {r['error_direction']}）")
        lines.append(f"- {r['explanation']}")
        for ev in r.get("evidence", []):
            lines.append(f"  - `{ev}`" if "`" not in ev else f"  - {ev}")
        lines.append("")

    trees = data.get("zero_unit_trees") or []
    lines += ["## ユニット 0 件（と極端に少ない）木", "",
              "| 木 | 母集団 | 分類 | 見つかったツール形（カタログ内か） | 説明 |", "|---|---|---|---|---|"]
    for t in trees:
        forms = "; ".join(
            f"{f['form']}@{f['site']}{'（内）' if f.get('in_catalog') else '（外）'}"
            for f in t.get("tool_forms_found", [])
        ) or "—"
        expl = t["explanation"].replace("\n", " ").replace("|", "\\|")
        forms = forms.replace("|", "\\|")
        lines.append(f"| `{t['tree']}` | {t['population']} | **{t['classification']}** | {forms} | {expl} |")
    cls = collections.Counter(t["classification"] for t in trees)
    lines += ["", f"分類の集計: {dict(sorted(cls.items()))}", ""]

    ann = data.get("annotations") or {}
    lines += ["## annotation の読み取り（`r_kind = 0%` の確認）", "",
              f"**読み取りの仕組み**: {ann.get('parser_explanation', '（結果なし）')}", ""]
    if ann.get("d_unknown_explanation"):
        lines += [f"**D_unknown**: {ann['d_unknown_explanation']}", ""]
    lines += ["| 木 | 箇所 | 形 | ツール | 解析器がユニットを見つけたか | 判定 | 説明 |", "|---|---|---|---|---|---|---|"]
    for f in ann.get("findings", []):
        # f-string の式部にバックスラッシュを書くと 3.10 では SyntaxError（PEP 701 は 3.12）。
        expl = f["explanation"].replace("\n", " ").replace("|", "\\|")
        form = f["annotation_form"].replace("|", "\\|")
        lines.append(
            f"| `{f['tree']}` | `{f['site']}` | {form} | "
            f"{f.get('tool_name') or '—'} | {f.get('unit_found_by_analyzer')} | **{f['verdict']}** | {expl} |"
        )
    if data.get("dropped"):
        lines += ["", f"**結果を返さなかった点検者**: {data['dropped']}（その範囲は未点検）"]
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", default=os.path.join(ROOT, "evidence", "f0a", "check_results.json"))
    ap.add_argument("--sample", default=os.path.join(ROOT, "evidence", "f0a", "check_sample.json"))
    ap.add_argument("--out", default=os.path.join(ROOT, "docs", "f0a_checks.md"))
    args = ap.parse_args()

    with open(args.sample, encoding="utf-8") as fh:
        sample = json.load(fh)
    with open(args.results, encoding="utf-8") as fh:
        data = json.load(fh)
    accepted, problems = reconcile(sample, data.get("sample_items", []))
    write_md(sample, data, accepted, problems, args.out)
    print(f"採用 {len(accepted)} / 照合の問題 {len(problems)} -> {args.out}")
    for p in problems:
        print("  ", p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
