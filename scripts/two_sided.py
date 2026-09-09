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

**同一性は 2 段で取る。**

1. **経路単位（主）**: `witness_chain`（入口からのツール経路）。その経路の下に
   出た `(kind, site, slot, ...)` タプルの**集合**を比べる。
   `effect kind` が座標に入っているのは A3（`FS_WRITE(index.add)` →
   `SPAWN(git.Git.add)`）が自分の定義で落ちないようにするためであり、
   sink 名を同一性に含めると kind が変わる対が「両側に同一サイトが無い」と
   判定されて落ちる。**経路単位が §6 T1.1 の言う「同一の効果サイト」である。**
2. **サイト単位（詳細）**: `(kind, site, slot, witness_chain)`。どの位置が
   どう変わったかを読むための内訳。

* **行番号では同一性を取らない**（修正で行がずれる）。
* **呼び出し経路を落とさない。** `git.Git.diff` は `git_diff` /
  `git_diff_staged` / `git_diff_unstaged` の 3 つのツールから到達し、
  検証子が付くのは `git_diff` だけである。経路を落とすと検証の無い兄弟経路が
  最弱として採られ、**修正で入った検証が見えなくなる**（A2 の `git_diff` が
  これで消えた）。

同じサイトキーが複数残る場合は最弱を採る（攻撃者が最弱経路を選ぶ）。
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
    """`a` のほうが弱い（= 危険）か。

    **主体を最優先で見る。** `repo.git.add(".")`（OP）と
    `repo.git.add("--", *files)`（MODEL）が同じキーに衝突したとき、主体を見ないと
    どちらが残るかが走査順に依存し、A3 の `OP -> MODEL` の変化が消える。
    """
    ka = (a.principal != "MODEL", _REQ_ORDER.get(a.req_val, 3), _GRADE_ORDER.get(a.grade, 0))
    kb = (b.principal != "MODEL", _REQ_ORDER.get(b.req_val, 3), _GRADE_ORDER.get(b.grade, 0))
    return ka < kb


@dataclass
class PairResult:
    pair_id: str
    vuln_root: str
    fixed_root: str
    #: 両版に存在する**経路**のうち、タプル集合が変化したもの（主指標）。
    changed_paths: list[dict] = field(default_factory=list)
    #: 両版に存在するが不変の経路。
    unchanged_paths: int = 0
    #: 片側にしかない経路（**同一効果サイトの条件を満たさないので数えない**）。
    only_vuln: list[str] = field(default_factory=list)
    only_fixed: list[str] = field(default_factory=list)
    #: サイト単位の内訳（詳細）。
    changed_sites: list[dict] = field(default_factory=list)
    #: verdict が GAP から外れた**経路**（内訳）。
    verdict_clearing: list[str] = field(default_factory=list)
    #: 変化した経路のうち、修正側にまだ GAP が残っているもの。
    still_gap: list[str] = field(default_factory=list)

    @property
    def two_sided(self) -> bool:
        return bool(self.changed_paths)

    @property
    def pair_cleared(self) -> bool:
        """**対単位の verdict-clearing**（§6 T1.1 の副次指標はこちら）。

        変化した経路のどれにも修正側で GAP が残っていないこと。1 本でも
        残っていれば AuthGap はそのツールを依然 GAP として報告するので、
        「修正を検出した」とは書けない。
        """
        return self.two_sided and not self.still_gap

    def to_json(self) -> dict:
        return {
            "pair_id": self.pair_id,
            "vuln_root": self.vuln_root,
            "fixed_root": self.fixed_root,
            "two_sided_pass": self.two_sided,
            "n_changed_paths": len(self.changed_paths),
            "n_unchanged_paths": self.unchanged_paths,
            "changed_paths": self.changed_paths,
            "changed_sites": self.changed_sites,
            "only_vuln": sorted(self.only_vuln),
            "only_fixed": sorted(self.only_fixed),
            "verdict_clearing_paths": sorted(self.verdict_clearing),
            "n_verdict_clearing_paths": len(self.verdict_clearing),
            "still_gap_paths": sorted(self.still_gap),
            "pair_cleared": self.pair_cleared,
        }

    # 旧名（テストと既存の呼び出し向け）。
    @property
    def changed(self) -> list[dict]:
        return self.changed_sites


def _chain_label(chain: tuple) -> str:
    return "->".join(chain) if chain else "-"


def compare(pair_id: str, vuln: str, fixed: str, population: str) -> PairResult:
    a = collect(vuln, population)
    b = collect(fixed, population)
    res = PairResult(pair_id, vuln, fixed)

    def by_path(rows: dict[tuple, SideRow]) -> dict[str, dict[tuple, SideRow]]:
        out: dict[str, dict[tuple, SideRow]] = {}
        for r in rows.values():
            out.setdefault(_chain_label(r.chain), {})[(r.kind, r.site, r.slot)] = r
        return out

    pa, pb = by_path(a), by_path(b)
    for path in sorted(set(pa) | set(pb)):
        sa, sb = pa.get(path), pb.get(path)
        if sa is None:
            res.only_fixed.append(path)
            continue
        if sb is None:
            res.only_vuln.append(path)
            continue
        site_diffs: list[dict] = []
        for key in sorted(set(sa) | set(sb), key=lambda k: tuple(str(x) for x in k)):
            ra, rb = sa.get(key), sb.get(key)
            label = f"{key[0]}@{key[1]}#{key[2]} [{path}]"
            if ra is None:
                site_diffs.append({"site": label, "diffs": {"presence": ["absent", "present"]},
                                   "vuln": None, "fixed": rb.tuple_view()})
                continue
            if rb is None:
                site_diffs.append({"site": label, "diffs": {"presence": ["present", "absent"]},
                                   "vuln": ra.tuple_view(), "fixed": None})
                continue
            ta, tb = ra.tuple_view(), rb.tuple_view()
            d = {k: [ta[k], tb[k]] for k in TUPLE_COORDS if ta[k] != tb[k]}
            if d:
                site_diffs.append({"site": label, "diffs": d, "vuln": ta, "fixed": tb})
        if not site_diffs:
            res.unchanged_paths += 1
            continue
        res.changed_paths.append({"path": path, "n_sites": len(site_diffs)})
        res.changed_sites.extend(site_diffs)
        gap_a = any(v.startswith("GAP") for r in sa.values() for v in r.verdicts)
        gap_b = any(v.startswith("GAP") for r in sb.values() for v in r.verdicts)
        if gap_b:
            res.still_gap.append(path)
        elif gap_a:
            res.verdict_clearing.append(path)
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
        print(f"  変化した経路 {len(r.changed_paths)} / 不変 {r.unchanged_paths} "
              f"/ 脆弱側のみ {len(r.only_vuln)} / 修正側のみ {len(r.only_fixed)}")
        for c in r.changed_sites[:14]:
            for k, (x, y) in sorted(c["diffs"].items()):
                print(f"    {c['site']:44s} {k:20s} {str(x):16s} -> {y}")
        print(
            f"  verdict-clearing: 対単位 = {r.pair_cleared}"
            f"（経路単位 {len(r.verdict_clearing)} 解消 / {len(r.still_gap)} 残存）"
        )
        for pth in r.still_gap[:6]:
            print(f"      修正側にも GAP が残る経路: {pth}")

    n_pass = sum(1 for r in results if r.two_sided)
    n_cleared = sum(1 for r in results if r.pair_cleared)
    print(f"\n両側通過 {n_pass}/{len(results)} 対")
    print(f"verdict-clearing 数（対単位・必須併記）: {n_cleared}/{n_pass}")
    print("**タプル変化のみで通過した対と区別せずに報告すると「修正を検出した」と誤読される**")

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
                    "n_verdict_clearing_pairs": n_cleared,
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
