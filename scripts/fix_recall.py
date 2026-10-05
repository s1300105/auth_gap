"""開発者が宣言を直したコミットで、解析器の再現率を測る（D79）。

材料は `scripts/mine_annotation_fixes.py` の候補（宣言を副作用のある側に動かし、本体は変えなかったツール）。
**直す前の版**（親コミット）では宣言が実装と食い違っていた、とみなし、凍結した解析器がその版でそのツール・その宣言に
矛（または不）を出したかを数える。

    # 1. 対象と取得の指定を作る（fork はコミットの共有でまとめ、1 群につき 1 つの repo を代表にする）
    .venv/bin/python scripts/fix_recall.py targets evidence/annotation_fixes_frame/candidates.json --out-dir <dir> --prefix fx
    # 2. 直す前の版を取得して走査する（いつもの道具）
    .venv/bin/python scripts/fetch_corpus.py --spec <dir>/fetch_spec.json
    .venv312/bin/python -u scripts/scan_v2.py --sample <dir>/fetch_spec.json --label <label> --require-fingerprint docs/fingerprint.json
    # 3. 数える
    .venv/bin/python scripts/fix_recall.py evaluate <dir>/items.json evidence/scan_v2_<label> --out <dir>/recall.json --seed <④>

宣言と解析器の判定の対応: readOnlyHint → D1、destructiveHint → D2、openWorldHint → D3、idempotentHint → D4。
解析器は D2・D4 を `readOnlyHint` が明示されていないときだけ照らす（`authgap/dparse.py` の `contradiction_findings`）。
直す前の版で readOnly も明示していたツールの D2・D4 は「照らさない（readOnly あり）」として別に数える（捨てない）。

1 件の結果（どれかに必ず入る。黙って落とさない。CLAUDE.md 規則 4）:
* `矛` … その宣言の矛の印がユニットの行にある（見つけた）
* `不` … 矛は無いが、その宣言の不の印がある（決められないと言った）
* `なし` … 矛も不も無い（見落とした）
* `照らさない（readOnly あり）` … 上の注意
* `ユニットが無い` … 直す前の版の manifest に、その名前のツールが見つからない（入口の見つけ損ね、または名前の取り違え）
* `走査できず` … その版の木の走査が ok でなかった

再現率は宣言ごとに、(a) 厳しい = 矛 / (矛 + 不 + なし)、(b) 不を含む = (矛 + 不) / (矛 + 不 + なし)。分母の外の件数
（照らさない・ユニットが無い・走査できず）も並べる。区間は repo の群（fork をまとめたもの）を単位にした bootstrap。
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import random
import sys

DECL = {"readOnlyHint": "D1", "destructiveHint": "D2", "openWorldHint": "D3", "idempotentHint": "D4"}
OUTCOMES = ["矛", "不", "なし", "照らさない（readOnly あり）", "ユニットが無い", "走査できず"]


def _groups(cands: list[dict]) -> dict[str, str]:
    """コミットを共有する repo を 1 群にまとめる（fork）。repo → 群の代表（名前の辞書順で最初）。"""
    parent: dict[str, str] = {}

    def find(x: str) -> str:
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    by_sha: dict[str, set[str]] = collections.defaultdict(set)
    for c in cands:
        by_sha[c["sha"]].add(c["repo"])
        find(c["repo"])
    for repos in by_sha.values():
        rs = sorted(repos)
        for r in rs[1:]:
            a, b = find(rs[0]), find(r)
            if a != b:
                parent[max(a, b)] = min(a, b)
    members: dict[str, list[str]] = collections.defaultdict(list)
    for r in list(parent):
        members[find(r)].append(r)
    return {r: min(ms) for ms in members.values() for r in ms}


def cmd_targets(a) -> int:
    cands = json.load(open(a.candidates, encoding="utf-8"))["candidates"]
    group = _groups(cands)
    items: dict[tuple, dict] = {}
    for c in sorted(cands, key=lambda c: (c["repo"], c["date"], c["sha"])):
        for w in c["weakened"]:
            if w["body_changed"] is not False:  # 本体も変えたもの・本体を比べられない形（低レベル）は入れない
                continue
            g = group[c["repo"]]
            key = (g, w["tool"], w["hint"])
            if key in items:
                continue  # 同じ群・同じツール・同じ宣言は最初の直しだけ
            items[key] = {"group": g, "repo": c["repo"], "sha": c["sha"], "parent": c["parent"], "date": c["date"],
                          "subject": c["subject"], "file": w["file"], "tool": w["tool"], "hint": w["hint"],
                          "decl": DECL[w["hint"]], "old": w["old"], "new": w["new"]}
    item_list = sorted(items.values(), key=lambda x: (x["group"], x["tool"], x["hint"]))
    snaps = sorted({(x["repo"], x["parent"]) for x in item_list})
    names = {s: f"{a.prefix}-{s[0].replace('/', '__')}-{s[1][:10]}" for s in snaps}
    for x in item_list:
        x["tree"] = names[(x["repo"], x["parent"])]
    os.makedirs(a.out_dir, exist_ok=True)
    json.dump({"_note": "fix_recall.py targets の出力。1 件 = (群, ツール, 宣言)。tree は直す前の版（親コミット）の木の名前",
               "n_items": len(item_list), "n_groups": len({x['group'] for x in item_list}), "n_snapshots": len(snaps),
               "items": item_list}, open(os.path.join(a.out_dir, "items.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    json.dump({"_note": "直す前の版の取得の指定（fix_recall.py targets）",
               "targets": [{"name": names[s], "repo": s[0], "ref": s[1], "population": "mcp_server",
                            "note": "宣言を直したコミットの親（D79）"} for s in snaps]},
              open(os.path.join(a.out_dir, "fetch_spec.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    by = collections.Counter(x["decl"] for x in item_list)
    print(f"件 {len(item_list)}（群 {len({x['group'] for x in item_list})}・版 {len(snaps)}）  宣言ごと {dict(sorted(by.items()))}")
    return 0


def _outcome(item: dict, run_dir: str, status: dict) -> tuple[str, list[str]]:
    tree, decl = item["tree"], item["decl"]
    if status.get(tree) != "ok":
        return "走査できず", []
    m = json.load(open(os.path.join(run_dir, f"{tree}.json"), encoding="utf-8"))
    units = [u for u in m["units"]
             if u["unit"].get("tool_name") == item["tool"] or u["unit"]["qualname"].split(".")[-1] == item["tool"]]
    if not units:
        return "ユニットが無い", []
    found: set[str] = set()
    reasons: list[str] = []
    for u in units:
        explicit = set((u.get("D_kind") or {}).get("explicit") or [])
        if decl in ("D2", "D4") and "readOnlyHint" in explicit:
            found.add("照らさない（readOnly あり）")
            continue
        for r in u.get("rows") or []:
            for n in r.get("notes") or []:
                n = str(n)
                if n == f"contradiction:{decl}":
                    found.add("矛")
                elif n.startswith(f"contradiction_unknown:{decl}"):
                    found.add("不")
                    reasons.append(n.split(":", 2)[-1])
                elif n.startswith(f"contradiction_reason:{decl}:"):
                    reasons.append(n.split(":", 2)[-1])
    for o in ("矛", "不", "照らさない（readOnly あり）"):
        if o in found:
            return o, sorted(set(reasons))
    return "なし", []


def _boot(rows: list[tuple[str, int, int]], seed: int, reps: int) -> tuple[float, float] | None:
    """群を単位にした bootstrap。rows = [(群, 分子, 分母)]。百分位 2.5 / 97.5。"""
    by: dict[str, list[int]] = collections.defaultdict(lambda: [0, 0])
    for g, k, n in rows:
        by[g][0] += k
        by[g][1] += n
    gs = sorted(g for g in by if by[g][1] > 0)  # 分母に件を持つ群だけ（分母の外の件しかない群は数えない）
    if len(gs) < 10:
        return None
    rng = random.Random(seed)
    vals = []
    for _ in range(reps):
        pick = [gs[rng.randrange(len(gs))] for _ in gs]
        k = sum(by[g][0] for g in pick)
        n = sum(by[g][1] for g in pick)
        if n:
            vals.append(k / n)
    vals.sort()
    return vals[int(0.025 * (len(vals) - 1))], vals[int(0.975 * (len(vals) - 1))]


def cmd_evaluate(a) -> int:
    items = json.load(open(a.items, encoding="utf-8"))["items"]
    summ = json.load(open(os.path.join(a.run_dir, "summary.json"), encoding="utf-8"))
    status = {t["tree"]: t.get("status") for t in summ["trees"]}
    rows = []
    for x in items:
        o, reasons = _outcome(x, a.run_dir, status)
        rows.append({**x, "outcome": o, "reasons": reasons})
    table = {}
    for decl in ("D1", "D2", "D3", "D4"):
        rs = [r for r in rows if r["decl"] == decl]
        c = collections.Counter(r["outcome"] for r in rs)
        denom = c["矛"] + c["不"] + c["なし"]
        strict = [(r["group"], int(r["outcome"] == "矛"), int(r["outcome"] in ("矛", "不", "なし"))) for r in rs]
        loose = [(r["group"], int(r["outcome"] in ("矛", "不")), int(r["outcome"] in ("矛", "不", "なし"))) for r in rs]
        table[decl] = {
            "counts": {o: c[o] for o in OUTCOMES},
            "n_groups_in_denominator": len({r["group"] for r in rs if r["outcome"] in ("矛", "不", "なし")}),
            "recall_strict": (c["矛"] / denom) if denom else None,
            "recall_strict_ci": _boot(strict, a.seed, a.reps),
            "recall_incl_unknown": ((c["矛"] + c["不"]) / denom) if denom else None,
            "recall_incl_unknown_ci": _boot(loose, a.seed, a.reps),
            # 保守的な読み: 「ユニットが無い」を見落としに数える（入口を見つけ損ねたのも解析器の取りこぼし）
            "recall_incl_unknown_unit_missing_as_miss": ((c["矛"] + c["不"]) / (denom + c["ユニットが無い"]))
            if (denom + c["ユニットが無い"]) else None,
        }
    out = {"_note": "fix_recall.py evaluate（D79）。区間は群を単位にした bootstrap、群が 10 未満なら出さない",
           "run": a.run_dir, "analyzer": {k: summ.get(k) for k in ("implementation_sha256_combined", "authgap_dirty",
                                                                   "max_depth")},
           "seed": a.seed, "reps": a.reps, "by_decl": table, "items": rows}
    json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for d, t in table.items():
        print(d, t["counts"], "群", t["n_groups_in_denominator"], "厳しい", t["recall_strict"], t["recall_strict_ci"],
              "不を含む", t["recall_incl_unknown"], t["recall_incl_unknown_ci"])
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("targets")
    t.add_argument("candidates")
    t.add_argument("--out-dir", required=True)
    t.add_argument("--prefix", required=True)
    e = sub.add_parser("evaluate")
    e.add_argument("items")
    e.add_argument("run_dir")
    e.add_argument("--out", required=True)
    e.add_argument("--seed", type=int, required=True)
    e.add_argument("--reps", type=int, default=10000)
    a = ap.parse_args()
    return cmd_targets(a) if a.cmd == "targets" else cmd_evaluate(a)


if __name__ == "__main__":
    sys.exit(main())
