#!/usr/bin/env python3
"""F0a の報告に使う解析器を凍結する記録を書く（D19）。

**何を凍結するか。** `authgap.report.fingerprint()`（§6 の凍結物: sink 表・入口カタログ・
ゲート語彙・cap・D パーサ規則・執行表の sha256）だけでは足りない。F0a run 1 の後の修正は
すべて val エンジンの**実装**（`authgap/val/engine.py` など）に入っており、カタログの指紋は
それを区別しない。そこで次を 1 つの JSON に書く:

* git commit と、`authgap/` に未コミットの変更が無いこと（あれば書かずに止まる）
* Python の版
* `fingerprint()` の出力
* `authgap/` 以下の全 `.py` の sha256（実装の指紋）と、その結合 sha256
* 凍結の根拠: 直前のレビューの run id と確認件数（向きごと）、使う F0a run のラベル

出力: `evidence/f0a_freeze/<label>.json`。**書いたあとで `git tag` を打つのは人が行う**
（このスクリプトはタグを打たない）。

使い方::

    python scripts/freeze_f0a.py --label freeze1 --run run5 \\
        --review wf_0befeae9-69c --confirmed-false-clean 0 --confirmed-drop-or-crash 0 \\
        --confirmed-precision 1
"""

from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from authgap.report import canonical_json, fingerprint  # noqa: E402


def _git(*args: str) -> str:
    p = subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} に失敗: {p.stderr}")
    return p.stdout.strip()


def implementation_hashes() -> dict[str, str]:
    out: dict[str, str] = {}
    base = os.path.join(ROOT, "authgap")
    for dirpath, dirs, files in os.walk(base):
        dirs[:] = sorted(d for d in dirs if d != "__pycache__")
        for fn in sorted(files):
            if fn.endswith(".py"):
                path = os.path.join(dirpath, fn)
                with open(path, "rb") as fh:
                    out[os.path.relpath(path, ROOT)] = hashlib.sha256(fh.read()).hexdigest()
    return dict(sorted(out.items()))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True, help="凍結の名前（例: freeze1）")
    ap.add_argument("--run", required=True, help="この解析器で取った F0a run のラベル（例: run5）")
    ap.add_argument("--review", required=True, help="凍結の根拠にしたレビューの run id")
    ap.add_argument("--confirmed-false-clean", type=int, required=True)
    ap.add_argument("--confirmed-drop-or-crash", type=int, required=True)
    ap.add_argument("--confirmed-precision", type=int, default=0)
    ap.add_argument("--note", default="")
    args = ap.parse_args()

    if _git("status", "--porcelain", "--", "authgap"):
        print("**authgap/ に未コミットの変更がある。凍結しない。**", file=sys.stderr)
        return 2
    if args.confirmed_false_clean or args.confirmed_drop_or_crash:
        print(
            "**D19 の凍結条件を満たさない**（false-clean / 消失・クラッシュの確認済み指摘が 0 でない）。"
            "凍結ではなく既知の欠陥として報告する場合は、その旨を --note に書いて docs に記録すること。",
            file=sys.stderr,
        )
        return 3

    impl = implementation_hashes()
    record = {
        "schema": "authgap/f0a-freeze/v1",
        "label": args.label,
        "commit": _git("rev-parse", "HEAD"),
        "python": sys.version.split()[0],
        "f0a_run": args.run,
        "review": {
            "run_id": args.review,
            "confirmed_false_clean": args.confirmed_false_clean,
            "confirmed_drop_or_crash": args.confirmed_drop_or_crash,
            "confirmed_precision_loss": args.confirmed_precision,
        },
        "catalog_fingerprint": fingerprint(),
        "implementation_sha256": impl,
        "implementation_sha256_combined": hashlib.sha256(canonical_json(impl).encode("utf-8")).hexdigest(),
        "note": args.note,
    }
    dest_dir = os.path.join(ROOT, "evidence", "f0a_freeze")
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, f"{args.label}.json")
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(canonical_json(record))
    print(f"wrote {dest}")
    print(f"実装の結合 sha256: {record['implementation_sha256_combined']}")
    print(f"次に人が打つ: git tag -a f0a-{args.label} {record['commit']} -m 'F0a 凍結（D19）'")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
