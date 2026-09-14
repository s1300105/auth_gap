#!/usr/bin/env python3
"""F0a の判断を 1 件ずつ検証するための標本を seed 固定で抜く。

**この手続きは run 1 のユニット行を見る前にコミットする。** 見てから検証対象を
選ぶと、解析器が当たっている / 外れているところだけを選ぶ事後選択になる。

層（`evidence/f0a/units.jsonl` の行から作る）:

====  ===========================  ============================================
層    母集団（抽出単位）            確かめる主張
====  ===========================  ============================================
OPQ   `resolution=opaque` の効果    本当に木内で解決できないか（§1 / Def 4 の
      サイト                        「木内で解決できない呼び出し」に当たるか）
RES   `resolution=resolved` の効果  解決したと言ってよいか（誤 resolved）
      サイト
EFF   危険効果を持つユニット        その kind の効果が本当にあるか（kind の精度）
NOE   効果 0 件のユニット           危険効果を取りこぼしていないか（再現率）
VAL   validator 形状を持つユニット  形状語彙の当てはめが正しいか
DKD   `D_kind` が ⊥ でないユニット  annotation の読み取りが正しいか
====  ===========================  ============================================

**効果サイトは (木, relpath, lineno, kind) で重複除去する。** 同じサイトに複数の
呼び出し経路から届くと行が複製される（§2.6 の出力側の指数項）ので、行のまま
抜くと同じサイトを何度も確かめることになる。

**これは C2 のラベル付けではない。** 解析器の欠陥を見つけるための事前点検であり、
論文に書く検証は学生が手で行う（`docs/verification_guide.md`）。

使い方::

    python scripts/sample_f0a_checks.py --units evidence/f0a/units.jsonl
"""

from __future__ import annotations

import argparse
import json
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#: **固定 seed。動かさない。**
DEFAULT_SEED = 20260914

#: 層ごとの抽出数（母集団がこれより小さければ全件）。
SIZES = {"OPQ": 25, "RES": 20, "EFF": 20, "NOE": 20, "VAL": 20, "DKD": 10}


def load(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def strata(units: list[dict]) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {k: [] for k in SIZES}
    sites: dict[str, dict[tuple, dict]] = {"OPQ": {}, "RES": {}}
    for u in units:
        base = {
            "tree": u["tree"],
            "population": u["population"],
            "unit_id": u["unit_id"],
            "tool_name": u["tool_name"],
            "unit_relpath": u["relpath"],
            "unit_lineno": u["lineno"],
        }
        for e in u["effects"]:
            layer = {"opaque": "OPQ", "resolved": "RES"}.get(e["resolution"])
            if layer is None:
                continue
            key = (u["tree"], e["relpath"], e["lineno"], e["kind"])
            # 最初に見たユニットを代表にする（units.jsonl は木の抽出順 → ソース順）。
            sites[layer].setdefault(key, {**base, "effect": e})
        if u["dangerous"]:
            out["EFF"].append({**base, "effects": u["effects"]})
        if not u["effects"]:
            out["NOE"].append(base)
        if u["validator_shapes"]:
            out["VAL"].append({**base, "validator_shapes": u["validator_shapes"]})
        if not u["D_kind"].get("bottom", True):
            out["DKD"].append({**base, "D_kind": u["D_kind"]})
    for layer, d in sites.items():
        out[layer] = [d[k] for k in sorted(d)]
    return out


def draw(pools: dict[str, list[dict]], seed: int) -> dict:
    rng = random.Random(seed)
    picked: dict[str, list[dict]] = {}
    # **層の順序を固定する**（辞書順ではなく SIZES の宣言順）。
    for layer, n in SIZES.items():
        pool = pools[layer]
        k = min(n, len(pool))
        picked[layer] = rng.sample(pool, k) if k else []
    return {
        "seed": seed,
        "sizes_wanted": SIZES,
        "pool_sizes": {k: len(v) for k, v in pools.items()},
        "items": picked,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--units", default=os.path.join(ROOT, "evidence", "f0a", "units.jsonl"))
    ap.add_argument("--seed", type=int, default=DEFAULT_SEED)
    ap.add_argument("--out", default=os.path.join(ROOT, "evidence", "f0a", "check_sample.json"))
    args = ap.parse_args()

    s = draw(strata(load(args.units)), args.seed)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(s, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")
    print(f"pool {s['pool_sizes']}")
    print(f"drawn { {k: len(v) for k, v in s['items'].items()} } -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
