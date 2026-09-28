"""添削の「直す単位」の表を作る（`docs/review_plan.md` §4.3）。

    .venv/bin/python scripts/review_triage.py --md docs/review_triage.md

入力: evidence/review/triage.json（根本原因ごとの単位と、単位ごとの記述。検証役ではなく整理役のエージェントが書いた）、
evidence/review/explore_*.json（所見の題）。**推奨は整理役の推奨で、採否は学生が決める。**
本記録者の提案（段階 A / B / C）は `TIERS` に書き、推奨とは別の列に出す。
"""

from __future__ import annotations

import argparse
import glob
import json
import os
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EV = os.path.join(ROOT, "evidence", "review")

SEV_JA = {"high": "高", "medium": "中", "low": "低"}
REC_JA = {"fix": "直す", "fix_partially": "一部直す", "record_as_limitation": "限界として記録"}
DIR_JA = {"false_clean": "誤 clear", "false_alarm": "誤警報", "count_loss": "数え落とし",
          "nondeterminism": "非決定", "rule_mismatch": "規則との食い違い", "mixed": "混在"}
FIX_JA = {"yes": "ある", "yes_with_conditions": "条件つきである", "no": "無い", "unclear": "不明"}

#: 本記録者の提案（整理役の推奨とは別）。
#: A = 最終評価の数字を直接狂わせる（評価の道具・非決定・痕跡の欠け・書いた規則との食い違い）。先に直す。
#: B = 新しいデータで頻出しうる書き方で、D1〜D4 の判定が系統的に変わる high。直すかを学生が選ぶ。
#: C = それ以外。既定は限界として記録（学生が望めば個別に B へ上げる）。
TIERS = {
    "A": ["U25", "U49", "U50", "U51", "U52", "U53", "U54", "U32", "U55", "U33", "U34", "U36"],
    "B": ["U38", "U40", "U09", "U01", "U23", "U03", "U13", "U12", "U02", "U06", "U26"],
}


def tier_of(uid: str) -> str:
    for t, us in TIERS.items():
        if uid in us:
            return t
    return "C"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", required=True)
    a = ap.parse_args()
    r = json.load(open(os.path.join(EV, "triage.json")))
    titles = {}
    for p in glob.glob(os.path.join(EV, "explore_*.json")):
        for f in json.load(open(p))["findings"]:
            titles[f["id"]] = f["title"]
    T = sorted(r["triage"], key=lambda t: ({"high": 0, "medium": 1, "low": 2}[t["severity"]], t["unit_id"]))
    n_members = sum(len(t["members"]) for t in T)
    L = ["# 添削の「直す単位」（採否の表。`scripts/review_triage.py` で再生成）", ""]
    L.append(f"所見 {n_members} 件を根本原因ごとに **{len(T)} 単位**にまとめた（`evidence/review/triage.json`。"
             f"全所見がちょうど 1 回ずつ入ることをコードで確かめた: 欠け {len(r['coverage']['missing'])} / 重複 {len(r['coverage']['dup'])}）。")
    L.append("整理は Opus のエージェント（単位分け 1 本 + 単位ごとの記述 55 本）。**「推奨」は整理役の推奨、「段階」は本記録者の提案で、"
             "採否（直す / 限界として記録）は学生が決める。**")
    L.append("")
    c = Counter((t["severity"], t["recommendation"]) for t in T)
    L.append("| 重大度 | 直す | 一部直す | 限界として記録 |")
    L.append("|---|---|---|---|")
    for s in ("high", "medium", "low"):
        L.append(f"| {SEV_JA[s]} | {c[(s, 'fix')]} | {c[(s, 'fix_partially')]} | {c[(s, 'record_as_limitation')]} |")
    L.append("")
    L.append("## 本記録者の提案: 段階")
    L.append("")
    L.append("- **A（先に直す）**: 最終評価の数字を直接狂わせるもの。評価の道具・非決定・打ち切りの痕跡・書いた規則（§7）との食い違い。"
             "多くは `scripts/` だけで直り、解析器の凍結の指紋に触れない。")
    L.append("- **B（直すかを選ぶ）**: 新しいデータで頻出しうる書き方で、D1〜D4 の判定が系統的に変わる high。ほぼすべて"
             "解決率を上げる向き（CLAUDE.md の敵対的レビューが要る）で、規模は M〜L。直すと解析器が変わり、再凍結・run21 の取り直しが要る。")
    L.append("- **C（既定は限界として記録）**: それ以外。論文の限界節に書く一覧にする。")
    L.append("")
    L.append("| 段階 | 単位 | 重大度 | 推奨 | 向き | 宣言 | 一般に正しい直し方 | 解決率↑ | 規模 | 語彙の追加 | scripts だけ | 所見 | 名前 |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for tier in ("A", "B", "C"):
        for t in T:
            if tier_of(t["unit_id"]) != tier:
                continue
            L.append(f"| **{tier}** | {t['unit_id']} | {SEV_JA[t['severity']]} | {REC_JA[t['recommendation']]} | {DIR_JA[t['direction']]} | "
                     f"{' '.join(t['decls'])} | {FIX_JA[t['fix_general']]} | {'○' if t['raises_resolution'] else ''} | {t['size']} | "
                     f"{'要' if t['vocabulary_change'] else ''} | {'○' if t['frozen_tooling_only'] else ''} | {len(t['members'])} | "
                     f"{t['name'].replace('|', '｜')} |")
    L.append("")
    L.append("## 単位ごとの記述")
    for t in T:
        L.append("")
        L.append(f"### {t['unit_id']} {t['name']}（段階 {tier_of(t['unit_id'])}・重大度 {SEV_JA[t['severity']]}・推奨 {REC_JA[t['recommendation']]}）")
        L.append("")
        L.append(t["plain_summary"])
        L.append("")
        L.append(f"- **宣言**: {' / '.join(t['decls'])}　**向き**: {DIR_JA[t['direction']]}　**規模**: {t['size']}"
                 f"　**解決率を上げる向き**: {'はい' if t['raises_resolution'] else 'いいえ'}"
                 f"　**語彙の追加**: {'要' if t['vocabulary_change'] else '不要'}"
                 f"　**scripts/ だけで直る**: {'はい' if t['frozen_tooling_only'] else 'いいえ'}")
        L.append(f"- **根本原因**: {t['root_cause']}")
        L.append(f"- **コードの場所**: {', '.join(t['code_locus'])}")
        L.append(f"- **重大度の根拠**: {t['severity_basis']}")
        L.append(f"- **直し方（一般に正しいか: {FIX_JA[t['fix_general']]}）**: {t['fix_outline']}")
        L.append(f"- **記録済みの限界・決定との重なり**: {t['known_overlap']}")
        L.append(f"- **旧文言（D3 / D4 だけなら low）による格下げ**: {t['old_wording_downgrade']}")
        L.append(f"- **推奨の理由**: {t['recommendation_reason']}")
        L.append("- **所見**:")
        for m in t["members_detail"]:
            L.append(f"  - {m['id']}: {m['note']}（{titles.get(m['id'], '')[:120]}）")
    open(a.md, "w").write("\n".join(L) + "\n")
    print(f"units {len(T)} members {n_members} tiers " + str(Counter(tier_of(t['unit_id']) for t in T)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
