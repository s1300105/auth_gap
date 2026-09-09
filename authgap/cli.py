"""CLI: `python -m authgap probe <path>` / `scan <path>`。

**LLM を判定入力に使わない。出力は決定的**（同一入力で 3 回バイト一致）。
"""

from __future__ import annotations

import argparse
import os
import sys

from .report import (
    annotation_patch,
    canonical_json,
    determinism_signature,
    fingerprint,
    manifest_json,
    probe_json,
    write_evidence,
)
from .runner import POPULATIONS, RunConfig, run
from .val import Options


def _common(ap: argparse.ArgumentParser) -> None:
    ap.add_argument("path", help="解析対象の木（インストール前のパッケージ木）")
    ap.add_argument(
        "--population",
        choices=POPULATIONS,
        default="mcp_server",
        help="母集団。D_op の帰属規則がこれで決まる（Def 6）",
    )
    ap.add_argument("--exposure", help="運用者が供給する exposure ファイル（D_op）")
    ap.add_argument("--prev-manifest", help="直前リリースの manifest.json（D_prev）")
    ap.add_argument("--rubric-1c", help="docs/rubric_1c.json のパス")
    ap.add_argument("--evidence", help="evidence/<run_id> ディレクトリに書き出す")
    ap.add_argument("--run-id", default="local", help="evidence の run_id")
    ap.add_argument("--corpus-id", default="local", help="probe.json の corpus_id")
    ap.add_argument(
        "--loop-probe",
        action="store_true",
        help="ループを 3 周回して 2 周目との env 一致を確かめる（§2.6 の反証条件）",
    )
    ap.add_argument("--hosted", action="store_true", help="配備モード --hosted（付録の感度分析）")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="authgap", description="モデル実効権限の静的推論")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_probe = sub.add_parser("probe", help="F0a の測定量を出す（支配判定に依存しない）")
    _common(p_probe)
    p_probe.add_argument(
        "--with-traced-ratio",
        action="store_true",
        help="traced_ratio を書き込む。**A5 の run では使わない**（§5.1）",
    )

    p_scan = sub.add_parser("scan", help="manifest + verdict を出す")
    _common(p_scan)
    p_scan.add_argument("--sarif", help="SARIF を書き出すパス")
    p_scan.add_argument("--annotation-patch", help="CONTRADICTION 行を書き出すパス")
    p_scan.add_argument(
        "--determinism", type=int, default=0, metavar="N", help="N 回走らせてバイト一致を確かめる"
    )

    sub.add_parser("fingerprint", help="解析指紋を出す（月 10 の凍結物）")

    args = ap.parse_args(argv)
    if args.cmd == "fingerprint":
        sys.stdout.write(canonical_json(fingerprint()))
        return 0

    cfg = RunConfig(
        src_root=args.path,
        population=args.population,
        exposure_file=args.exposure,
        prev_manifest=args.prev_manifest,
        rubric_1c_path=args.rubric_1c,
        options=Options(loop_probe=args.loop_probe),
        full=(args.cmd == "scan"),
    )
    res = run(cfg)

    if args.cmd == "probe":
        out = probe_json(res, args.corpus_id, traced_ratio_null=not args.with_traced_ratio)
        sys.stdout.write(canonical_json(out))
    else:
        manifest = manifest_json(res, args.run_id)
        sys.stdout.write(canonical_json(manifest))
        if args.sarif:
            from .report import sarif as _sarif

            with open(args.sarif, "w", encoding="utf-8") as fh:
                fh.write(canonical_json(_sarif(res)))
        if args.annotation_patch:
            with open(args.annotation_patch, "w", encoding="utf-8") as fh:
                fh.write(canonical_json(annotation_patch(res)))
        if args.determinism:
            first = determinism_signature(manifest)
            for i in range(args.determinism - 1):
                again = manifest_json(run(cfg), args.run_id)
                if determinism_signature(again) != first:
                    sys.stderr.write(f"決定論の不一致: 実行 {i + 2} 回目\n")
                    return 3
            sys.stderr.write(f"決定論: {args.determinism} 回バイト一致\n")

    if args.evidence:
        out_dir = os.path.join(args.evidence)
        paths = write_evidence(res, out_dir, args.run_id, args.corpus_id)
        sys.stderr.write("wrote " + ", ".join(sorted(paths.values())) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
