#!/usr/bin/env python3
"""解析器を凍結する記録 `docs/fingerprint.json` を書く（仕様書 843 行目「月 10: 解析指紋」、D59）。

**何を書くか**（`scripts/freeze_f0a.py` と同じ考え方）:

* `authgap.report.fingerprint()`（sink 表・入口カタログ・ゲート語彙・cap と深さ・執行表の sha256）。
  **ただしこの指紋は sink 表の slot の名前しか見ず、引数の割り当て（`A(1, kw="url")`、
  `body ← data|json`）や val エンジンの実装を区別しない**ので、次も入れる。
* `authgap/` 以下の全 `.py` の sha256 と、その結合 sha256（実装の指紋）
* 凍結時の git commit と日付、Python の版、凍結の根拠にした run と決定

`authgap/` に未コミットの変更があれば書かずに止まる。**タグは人が打つ**（このスクリプトは打たない）。

使い方::

    python scripts/freeze_analyzer.py --run scan_v2_run18 --decision D59 --date 2026-09-24
"""

from __future__ import annotations

import argparse
import hashlib
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from freeze_f0a import _git, implementation_hashes  # noqa: E402

from authgap.report import canonical_json, fingerprint  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True, help="この解析器で取った full scan（例: scan_v2_run18）")
    ap.add_argument("--decision", required=True, help="凍結を決めた docs/decisions.md の項（例: D59）")
    ap.add_argument("--date", required=True, help="凍結の日付（YYYY-MM-DD。スクリプトは時計を読まない）")
    ap.add_argument("--out", default=os.path.join(ROOT, "docs", "fingerprint.json"))
    ap.add_argument("--tag", default="analyzer-freeze-1", help="人が打つタグの名前（表示だけ）")
    args = ap.parse_args()

    if _git("status", "--porcelain", "--", "authgap"):
        print("**authgap/ に未コミットの変更がある。凍結しない。**", file=sys.stderr)
        return 2
    summary = os.path.join(ROOT, "evidence", args.run, "summary.json")
    if not os.path.exists(summary):
        print(f"**{summary} が無い。**", file=sys.stderr)
        return 2

    fp = fingerprint()
    commit = _git("rev-parse", "HEAD")
    fp["frozen_at"] = args.date
    fp["git_commit"] = commit
    impl = implementation_hashes()
    record = {
        **fp,
        "freeze": {
            "decision": args.decision,
            "tag": args.tag,
            # authgap/ を最後に変えた commit（HEAD は docs だけの commit でありうる）
            "analyzer_commit": _git("log", "-1", "--format=%H", "--", "authgap"),
            "scan_run": args.run,
            "python": sys.version.split()[0],
            "note": (
                "母集団 v2 と v3 は開発用のデータ。論文の評価は、学生が v2 / v3 を含まない別の新しいデータで行う（D60）。"
                "凍結後に解析器を変えるなら docs/preregistration.md に逸脱として書く（D61）。"
            ),
        },
        "implementation_sha256": impl,
        "implementation_sha256_combined": hashlib.sha256(canonical_json(impl).encode("utf-8")).hexdigest(),
    }
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(canonical_json(record))
    print(f"wrote {os.path.relpath(args.out, ROOT)}")
    print(f"実装の結合 sha256: {record['implementation_sha256_combined']}")
    print(f"次に人が打つ: git tag -a {args.tag} {commit} -m '解析器の凍結（{args.decision}）'")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
