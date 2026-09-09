#!/usr/bin/env python3
"""両側条件の採点（§6 T1）。head-to-head の**主指標**を出す道具。

両側成功に数えるのは、**脆弱版と修正版の両方に同一の効果サイトが存在し**、
変化が次のいずれかで起きた対に限る（§6 T1.1）:

    effect kind | val 主体 | gate grade・reason | req_occ | req_val |
    exec mode | DISPATCH 候補集合の resolution

**副次指標（必須）**: 両側通過対のうち、修正版で verdict が GAP から外れる対の数
（verdict-clearing 数）を必ず併記する。タプル変化のみで通過した対と区別せずに
報告すると「修正を検出した」と誤読される。

使い方::

    python scripts/two_sided.py --pair A1 --vuln corpus/A1__vuln --fixed corpus/A1__fixed
    python scripts/two_sided.py --spec docs/corpus_spec.json --json evidence/w0/two_sided.json

効果サイトの同一性は **`(kind, site, slot, witness_chain)`** で取る。

* **行番号では取らない**（修正で行がずれる）。
* **呼び出し経路を入れる。** `git.Git.diff` は `git_diff` /
  `git_diff_staged` / `git_diff_unstaged` の 3 つのツールから到達し、
  検証子が付くのは `git_diff` だけである。経路を落として `(kind, site, slot)`
  だけで畳むと、検証の無い兄弟経路が最弱として採られ、**修正で入った検証が
  見えなくなる**（A2 の `git_diff` がこれで消えた）。

同じキーが複数残る場合は最弱を採る（攻撃者が最弱経路を選ぶ）。
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass, field
from typing import Any, Optional

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from authgap.report import manifest_json  # noqa: E402
from authgap.runner import RunConfig, run  # noqa: E402

#: 両側条件が見る座標（§6 T1.1）。
TUPLE_COORDS = (
    "kind",
    "principal",
    "grade",
    "weak_reason",
    "req_occ",
    "req_val",
    "exec_mode",
    "dispatch_resolution",
)

#: 消滅理由のうち**両側成功に数えるもの**（§6 T1.1 の表）。
ACCEPTED_REASONS = frozenset(
    {
        "validator-add",
        "normalisation-add",
        "approval-add",
        "selector-narrowing",
        "principal-demotion",
        "exec-mode-change",
        "sink-substitution",
    }
)
#: 数えないもの（N/A）。
NA_REASONS = frozenset(
    {
        "denylist-broadening",
        "parser-coverage",
        "redirect-rescope",
        "tool-delete",
        "feature-removal",
        "dependency-bump",
        "sink-removal",
        "no-fix",
    }
)


@dataclass
class SideRow:
    kind: str
    site: str
    slot: Optional[str]
    principal: str
    grade: Optional[str]
    weak_reason: Optional[str]
    req_occ: str
    req_val: Optional[str]
    exec_mode: Optional[Any]
    dispatch_resolution: Optional[str]
    verdicts: tuple[str, ...] = ()
    #: 入口からこの効果までの呼び出し経路（`witness_chain`）。
    chain: tuple[str, ...] = ()

    def key(self) -> tuple:
        return (self.kind, self.site, self.slot, self.chain)

    def tuple_view(self) -> dict:
        return {
            "kind": self.kind,
            "principal": self.principal,
            "grade": self.grade,
            "weak_reason": self.weak_reason,
            "req_occ": self.req_occ,
            "req_val": self.req_val,
            "exec_mode": self.exec_mode,
            "dispatch_resolution": self.dispatch_resolution,
        }


def collect(src_root: str, population: str) -> dict[tuple, SideRow]:
    res = run(RunConfig(src_root=src_root, population=population, full=True))
    man = manifest_json(res, run_id="two-sided", volatile=False)
    out: dict[tuple, SideRow] = {}
    for u in man["units"]:
        verdict_by_slot: dict[tuple, set[str]] = {}
        for r in u["rows"]:
            verdict_by_slot.setdefault((r["kind"], r["site"], r.get("slot")), set()).update(
                r["verdicts"]
            )
        for i, e in enumerate(u["effects"]):
            shell = (e.get("exec_mode") or {}).get("shell", {})
            exec_mode = shell.get("const", shell.get("source"))
            for slot, v in e["slots"].items():
                g = u["grades"].get(f"{i}:{slot}", {})
                row = SideRow(
                    kind=e["kind"],
                    site=e["site"],
                    slot=slot,
                    principal=v["prin"],
                    grade=g.get("grade"),
                    weak_reason=g.get("weak_reason"),
                    req_occ=u["req_occ_by_effect"].get(str(i), u["req_occ"]),
                    req_val=u["req_val"].get(f"{i}:{slot}"),
                    exec_mode=exec_mode,
                    dispatch_resolution=(u.get("trig") or {}).get("mode"),
                    verdicts=tuple(sorted(verdict_by_slot.get((e["kind"], e["site"], slot), ()))),
                    chain=tuple(e.get("witness_chain", ())),
                )
                prev = out.get(row.key())
                # 同じキーが複数行あるときは**最弱**を採る（攻撃者が最弱を選ぶ）。
                if prev is None or _weaker(row, prev):
                    out[row.key()] = row
    return out


_REQ_ORDER = {"MODEL": 0, "OP": 1, "USER": 2, None: 3}
_GRADE_ORDER = {None: 0, "unknown": 1, "allowlist": 2, "weak": 3, "strong-token": 4, "strong-path": 5}


def _weaker(a: SideRow, b: SideRow) -> bool:
    ka = (_REQ_ORDER.get(a.req_val, 3), _GRADE_ORDER.get(a.grade, 0))
    kb = (_REQ_ORDER.get(b.req_val, 3), _GRADE_ORDER.get(b.grade, 0))
    return ka < kb


@dataclass
class PairResult:
    pair_id: str
    vuln_root: str
    fixed_root: str
    #: 両版に存在する効果サイトのうち、タプルが変化したもの。
    changed: list[dict] = field(default_factory=list)
    #: 両版に存在するが不変のもの。
    unchanged: int = 0
    #: 片側にしかないもの（**同一効果サイトの条件を満たさないので数えない**）。
    only_vuln: list[str] = field(default_factory=list)
    only_fixed: list[str] = field(default_factory=list)
    #: verdict が GAP から外れたか（副次指標）。
    verdict_clearing: list[str] = field(default_factory=list)

    @property
    def two_sided(self) -> bool:
        return bool(self.changed)

    def to_json(self) -> dict:
        return {
            "pair_id": self.pair_id,
            "vuln_root": self.vuln_root,
            "fixed_root": self.fixed_root,
            "two_sided_pass": self.two_sided,
            "n_changed": len(self.changed),
            "n_unchanged": self.unchanged,
            "changed": self.changed,
            "only_vuln": sorted(self.only_vuln),
            "only_fixed": sorted(self.only_fixed),
            "verdict_clearing": sorted(self.verdict_clearing),
            "n_verdict_clearing": len(self.verdict_clearing),
        }


def compare(pair_id: str, vuln: str, fixed: str, population: str) -> PairResult:
    a = collect(vuln, population)
    b = collect(fixed, population)
    res = PairResult(pair_id, vuln, fixed)
    for key in sorted(set(a) | set(b), key=lambda k: tuple(str(x) for x in k)):
        ra, rb = a.get(key), b.get(key)
        chain = "->".join(key[3]) if key[3] else "-"
        label = f"{key[0]}@{key[1]}#{key[2]} [{chain}]"
        if ra is None:
            res.only_fixed.append(label)
            continue
        if rb is None:
            res.only_vuln.append(label)
            continue
        ta, tb = ra.tuple_view(), rb.tuple_view()
        diffs = {k: [ta[k], tb[k]] for k in TUPLE_COORDS if ta[k] != tb[k]}
        if not diffs:
            res.unchanged += 1
            continue
        res.changed.append({"site": label, "diffs": diffs, "vuln": ta, "fixed": tb})
        gap_a = any(v.startswith("GAP") for v in ra.verdicts)
        gap_b = any(v.startswith("GAP") for v in rb.verdicts)
        if gap_a and not gap_b:
            res.verdict_clearing.append(label)
    return res


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pair", default="pair")
    ap.add_argument("--vuln")
    ap.add_argument("--fixed")
    ap.add_argument("--population", default="mcp_server")
    ap.add_argument("--spec", help="docs/corpus_spec.json 形式。`<id>@vuln` / `<id>@fixed` を対にする")
    ap.add_argument("--json")
    args = ap.parse_args()

    pairs: list[tuple[str, str, str, str]] = []
    if args.spec:
        with open(args.spec, encoding="utf-8") as fh:
            targets = json.load(fh)["targets"]
        by_id: dict[str, dict[str, dict]] = {}
        for t in targets:
            if "@" not in t["name"]:
                continue
            pid, side = t["name"].split("@", 1)
            by_id.setdefault(pid, {})[side] = t
        for pid in sorted(by_id):
            sides = by_id[pid]
            if "vuln" in sides and "fixed" in sides:
                pairs.append(
                    (
                        pid,
                        os.path.join(ROOT, "corpus", f"{pid}__vuln"),
                        os.path.join(ROOT, "corpus", f"{pid}__fixed"),
                        sides["vuln"].get("population", "mcp_server"),
                    )
                )
    if args.vuln and args.fixed:
        pairs.append((args.pair, args.vuln, args.fixed, args.population))
    if not pairs:
        ap.error("--spec か --vuln/--fixed が要る")

    results = []
    for pid, v, f, pop in pairs:
        if not (os.path.isdir(v) and os.path.isdir(f)):
            print(f"SKIP {pid}: コーパスが無い（{v} / {f}）", file=sys.stderr)
            continue
        r = compare(pid, v, f, pop)
        results.append(r)
        print(f"\n=== {pid} : 両側通過 = {r.two_sided} ===")
        print(f"  変化した効果サイト {len(r.changed)} / 不変 {r.unchanged} "
              f"/ 脆弱側のみ {len(r.only_vuln)} / 修正側のみ {len(r.only_fixed)}")
        for c in r.changed[:12]:
            for k, (x, y) in sorted(c["diffs"].items()):
                print(f"    {c['site']:44s} {k:20s} {str(x):16s} -> {y}")
        print(f"  verdict-clearing（副次指標・必須併記）: {len(r.verdict_clearing)}")

    n_pass = sum(1 for r in results if r.two_sided)
    print(f"\n両側通過 {n_pass}/{len(results)} 対")
    print("**verdict-clearing 数を必ず併記すること**（タプル変化のみの通過と混ぜない）")

    if args.json:
        os.makedirs(os.path.dirname(args.json) or ".", exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(
                {
                    "accepted_reasons": sorted(ACCEPTED_REASONS),
                    "na_reasons": sorted(NA_REASONS),
                    "coords": list(TUPLE_COORDS),
                    "n_pairs": len(results),
                    "n_two_sided_pass": n_pass,
                    "pairs": [r.to_json() for r in results],
                },
                fh,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            fh.write("\n")
        print(f"wrote {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
