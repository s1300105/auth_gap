#!/usr/bin/env python3
"""両側条件の採点（§6 T1）。head-to-head の**主指標**を出す道具。

両側成功に数えるのは、**脆弱版と修正版の両方に同一の効果サイトが存在し**、
変化が次のいずれかで起きた対に限る（§6 T1.1）:

    effect kind | val 主体 | gate grade・reason | req_occ | req_val |
    exec mode | DISPATCH 候補集合の resolution

**分子は 3 列で出す**（`docs/preregistration.md` §5 #2 (a)。片方だけ出さない）:

* `pass_preregistered`（**主指標**）: `docs/expected_tuples.json` に事前登録した
  変化が、**その向きで**（脆弱側 `from` → 修正側 `to`）、期待した位置に
  `min_sites` 件以上起きていること。逆向きの対（修正版 → 脆弱版）は定義上通らない。
* `pass_coord_match`: 期待した座標が期待した位置で動いた（向きと値は問わない）。
* `pass_any_change`: 8 座標のどれかが値として違う（旧来の分子）。
  **`open` を `Path.read_text` に書き換えただけの対や逆向きの対も通す**ので、
  「修正を検出した」とは読めない。併記のためだけに残す。

厳密 ⊆ 座標 ⊆ any-change。期待表に無い対は `None`（未測定）で、False にして
安全側に倒さない。

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

#: 事前登録した期待タプル（`docs/cve_triage.csv` の `expected_tuple_change` の機械可読版）。
EXPECTED_TUPLES = os.path.join(ROOT, "docs", "expected_tuples.json")


def load_expected(path: str = EXPECTED_TUPLES) -> dict[str, dict]:
    """`{pair_id: {"vuln", "fixed", "population", "changes", "unchanged"?}}`。無ければ空。"""
    if not os.path.isfile(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)["pairs"]

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


def collect(src_root: str, population: str, arm: str = "C") -> dict[tuple, SideRow]:
    """片側を解析して効果サイトごとの行にする。

    `arm` は `authgap.analyze.ARMS` の腕。既定は完全版 ``C``。判別実験 (b)
    （`docs/preregistration.md` §5 #2）では ``C0``（等級潰し腕）で同じ対を回し、
    `C − C0` を出す。**腕は解析器に渡すだけで、ここでの集計は腕に依存しない。**
    """
    res = run(RunConfig(src_root=src_root, population=population, full=True, arm=arm))
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
                    # **経路が空のときはユニット名で埋める。**
                    # sink をユニット本体で直に呼ぶ形（AutoGPT の
                    # `execute_shell` / `execute_shell_popen`）は
                    # `witness_chain` が空なので、埋めないと別のツールが
                    # 同じ経路 `-` に潰れて変化が読めなくなる。
                    chain=tuple(e.get("witness_chain", ())) or (u["unit"]["qualname"],),
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
    #: 変化した経路のうち、修正側にまだ GAP が残っているもの（全 GAP 種）。
    still_gap: list[str] = field(default_factory=list)
    #: 同じく、修正側にまだ `GAP_INJECT` が残っているもの。
    still_gap_inject: list[str] = field(default_factory=list)
    #: 事前登録した期待（`docs/expected_tuples.json` の 1 対分）。無ければ None。
    expected: Optional[dict] = None
    #: 期待との照合結果（`match_expected` の出力）。expected が無ければ None。
    preregistered: Optional[dict] = None

    @property
    def two_sided(self) -> bool:
        """旧来の分子（any-change）。`pass_any_change` と同じ。"""
        return bool(self.changed_paths)

    @property
    def pass_any_change(self) -> bool:
        return self.two_sided

    @property
    def pass_preregistered(self) -> Optional[bool]:
        """**主指標**。期待表に無い対は None（未測定）。"""
        if self.preregistered is None:
            return None
        return bool(self.preregistered["strict"])

    @property
    def pass_coord_match(self) -> Optional[bool]:
        if self.preregistered is None:
            return None
        return bool(self.preregistered["coord"])

    @property
    def preregistered_misses(self) -> list[str]:
        if self.preregistered is None:
            return []
        return list(self.preregistered["misses"])

    @property
    def pair_cleared(self) -> bool:
        """**対単位の verdict-clearing（厳密）**。

        変化した経路のどれにも修正側で GAP が**一切**残っていないこと。
        1 本でも残っていれば AuthGap はそのツールを依然 GAP として報告するので、
        「修正を検出した」とは書けない。

        **MCP サーバではこれはほぼ常に偽になる。** `GAP_SELECT` は
        「モデルがそのツールを呼ぶかを決めており、承認割り込みも宣言も無い」
        ことを言うので、**値検証を足しても消えない**。消えるのは承認割り込みを
        足した対（A9 のような `approval-add`）だけである。
        """
        return self.two_sided and not self.still_gap

    @property
    def pair_cleared_inject(self) -> bool:
        """**対単位の verdict-clearing（INJECT 座標に限る）**。

        CVE が問うているのは多くの場合「引数位置の注入」なので、
        `GAP_INJECT` が消えたかを別に数える。**厳密版と必ず並べて報告する。**
        片方だけを書くと、SELECT 座標が常に残ることを隠すか、
        値検証の効果を見落とすかのどちらかになる。
        """
        return self.two_sided and not self.still_gap_inject

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
            "still_gap_inject_paths": sorted(self.still_gap_inject),
            "pair_cleared_strict": self.pair_cleared,
            "pair_cleared_inject": self.pair_cleared_inject,
            # 3 列（prereg §5 #2 (a)）。
            "pass_preregistered": self.pass_preregistered,
            "pass_coord_match": self.pass_coord_match,
            "pass_any_change": self.pass_any_change,
            "preregistered": self.preregistered,
        }

    # 旧名（テストと既存の呼び出し向け）。
    @property
    def changed(self) -> list[dict]:
        return self.changed_sites


def _chain_label(chain: tuple) -> str:
    return "->".join(chain) if chain else "-"


@dataclass
class SiteRecord:
    """両版に存在する経路の下の 1 サイト（片側に無ければ `None`）。照合の単位。"""

    kind: str
    site: str
    slot: Optional[str]
    path: str
    vuln: Optional[dict]
    fixed: Optional[dict]

    @property
    def label(self) -> str:
        return f"{self.kind}@{self.site}#{self.slot}"

    def value(self, side: str, coord: str):
        t = self.vuln if side == "vuln" else self.fixed
        if coord == "presence":
            return "present" if t is not None else "absent"
        return None if t is None else t.get(coord)


def _site_matches(rec: SiteRecord, cond: dict) -> bool:
    """期待の絞り込み（`docs/expected_tuples.json` の `_semantics`）。"""
    if "site" in cond and not rec.label.startswith(cond["site"]):
        return False
    if "slot" in cond and rec.slot != cond["slot"]:
        return False
    if "path" in cond and cond["path"] not in rec.path:
        return False
    return True


def match_expected(records: list[SiteRecord], expected: dict) -> dict:
    """期待表 1 対分を `records` に当てる。

    戻り値: ``{"strict": bool, "coord": bool, "changes": [...], "unchanged": [...], "misses": [...]}``

    * `strict`（= `pass_preregistered`）: すべての `changes` について、条件に合う
      サイトのうち **`from` → `to` がこの向きで起きた**ものが `min_sites` 件以上。
      `unchanged` は両側で `value` に等しいものが `min_sites` 件以上。
    * `coord`（= `pass_coord_match`）: 同じ位置で当該座標の値が**何かしら違う**
      ものが `min_sites` 件以上（向きも値も問わない）。`unchanged` は両側で
      等しい（値は問わない）ものが `min_sites` 件以上。
    """
    misses: list[str] = []
    strict = True
    coord_ok = True
    out_changes = []
    for c in expected.get("changes", []):
        cands = [r for r in records if _site_matches(r, c)]
        n_strict = sum(
            1 for r in cands if r.value("vuln", c["coord"]) == c["from"] and r.value("fixed", c["coord"]) == c["to"]
        )
        n_coord = sum(1 for r in cands if r.value("vuln", c["coord"]) != r.value("fixed", c["coord"]))
        ok_s, ok_c = n_strict >= c["min_sites"], n_coord >= c["min_sites"]
        strict &= ok_s
        coord_ok &= ok_c
        desc = {k: c[k] for k in ("site", "slot", "path") if k in c}
        out_changes.append(
            {"cond": desc, "coord": c["coord"], "from": c["from"], "to": c["to"], "min_sites": c["min_sites"],
             "n_candidates": len(cands), "n_strict": n_strict, "n_coord": n_coord, "ok_strict": ok_s, "ok_coord": ok_c}
        )
        if not ok_s:
            got = sorted({f"{r.value('vuln', c['coord'])}->{r.value('fixed', c['coord'])}" for r in cands})
            misses.append(f"{desc} {c['coord']} {c['from']}->{c['to']} x{c['min_sites']}: strict {n_strict} (観測 {got})")
    out_unchanged = []
    for u in expected.get("unchanged", []):
        cands = [r for r in records if _site_matches(r, u)]
        n_strict = sum(
            1 for r in cands if r.value("vuln", u["coord"]) == u["value"] and r.value("fixed", u["coord"]) == u["value"]
        )
        n_coord = sum(1 for r in cands if r.value("vuln", u["coord"]) == r.value("fixed", u["coord"]))
        ok_s, ok_c = n_strict >= u["min_sites"], n_coord >= u["min_sites"]
        strict &= ok_s
        coord_ok &= ok_c
        desc = {k: u[k] for k in ("site", "slot", "path") if k in u}
        out_unchanged.append(
            {"cond": desc, "coord": u["coord"], "value": u["value"], "min_sites": u["min_sites"],
             "n_candidates": len(cands), "n_strict": n_strict, "n_coord": n_coord, "ok_strict": ok_s, "ok_coord": ok_c}
        )
        if not ok_s:
            misses.append(f"{desc} {u['coord']} == {u['value']!r} x{u['min_sites']} (不変): {n_strict}")
    return {"strict": strict, "coord": coord_ok, "changes": out_changes, "unchanged": out_unchanged, "misses": misses}


def compare(
    pair_id: str,
    vuln: str,
    fixed: str,
    population: str,
    arm: str = "C",
    expected: Optional[dict] = None,
    expected_path: str = EXPECTED_TUPLES,
) -> PairResult:
    """1 対を採点する。

    `expected` を省くと `expected_path` の表から `pair_id` で引く。表に無い対は
    `pass_preregistered` / `pass_coord_match` が None（未測定）になる。
    逆向きの対を試すときは `expected=` を明示して渡す（`pair_id` では引かない）。
    """
    a = collect(vuln, population, arm)
    b = collect(fixed, population, arm)
    res = PairResult(pair_id, vuln, fixed)
    if expected is None:
        expected = load_expected(expected_path).get(pair_id)
    res.expected = expected
    records: list[SiteRecord] = []

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
            records.append(
                SiteRecord(
                    kind=key[0], site=key[1], slot=key[2], path=path,
                    vuln=None if ra is None else ra.tuple_view(),
                    fixed=None if rb is None else rb.tuple_view(),
                )
            )
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
        inj_b = any("GAP_INJECT" in r.verdicts for r in sb.values())
        if gap_b:
            res.still_gap.append(path)
        elif gap_a:
            res.verdict_clearing.append(path)
        if inj_b:
            res.still_gap_inject.append(path)
    if expected is not None:
        res.preregistered = match_expected(records, expected)
    return res


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pair", default="pair")
    ap.add_argument("--vuln")
    ap.add_argument("--fixed")
    ap.add_argument("--population", default="mcp_server")
    ap.add_argument("--spec", help="docs/corpus_spec.json 形式。`<id>@vuln` / `<id>@fixed` を対にする")
    ap.add_argument("--json")
    ap.add_argument("--arm", default="C", help="解析の腕（C / C0 / A / B）。判別実験 (b) は C0")
    ap.add_argument("--expected", default=EXPECTED_TUPLES, help="事前登録した期待タプルの表")
    args = ap.parse_args()
    expected_all = load_expected(args.expected)

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
        # 期待表にあって spec に無い CVE（A10 = A9 と修正コミットを共有）は、
        # その corpus が揃っていれば CVE 単位の行として足す。**A9 と A10 は同じ
        # 2 木を読む**ので、木の対としては 7、CVE としては 8 になる。
        have = {pid for pid, _, _, _ in pairs}
        for pid, e in sorted(expected_all.items()):
            if pid in have:
                continue
            v = os.path.join(ROOT, "corpus", e["vuln"])
            f = os.path.join(ROOT, "corpus", e["fixed"])
            if os.path.isdir(v) and os.path.isdir(f):
                pairs.append((pid, v, f, e.get("population", "mcp_server")))
    # `--population` は spec に population が無い対の既定値としてだけ使う。
    if args.vuln and args.fixed:
        pairs.append((args.pair, args.vuln, args.fixed, args.population))
    if not pairs:
        ap.error("--spec か --vuln/--fixed が要る")

    results = []
    for pid, v, f, pop in pairs:
        if not (os.path.isdir(v) and os.path.isdir(f)):
            print(f"SKIP {pid}: コーパスが無い（{v} / {f}）", file=sys.stderr)
            continue
        r = compare(pid, v, f, pop, arm=args.arm, expected=expected_all.get(pid), expected_path=args.expected)
        results.append(r)
        print(
            f"\n=== {pid} [腕 {args.arm}] : 事前登録照合 = {r.pass_preregistered} / "
            f"座標一致 = {r.pass_coord_match} / any-change = {r.pass_any_change} ==="
        )
        for m in r.preregistered_misses:
            print(f"    未達: {m}")
        print(f"  変化した経路 {len(r.changed_paths)} / 不変 {r.unchanged_paths} "
              f"/ 脆弱側のみ {len(r.only_vuln)} / 修正側のみ {len(r.only_fixed)}")
        for c in r.changed_sites[:14]:
            for k, (x, y) in sorted(c["diffs"].items()):
                print(f"    {c['site']:44s} {k:20s} {str(x):16s} -> {y}")
        print(
            f"  verdict-clearing: 厳密（全 GAP）= {r.pair_cleared} / "
            f"INJECT 座標のみ = {r.pair_cleared_inject}"
        )
        print(
            f"      経路単位: 全 GAP 解消 {len(r.verdict_clearing)} / 残存 {len(r.still_gap)}"
            f" ｜ INJECT 残存 {len(r.still_gap_inject)}"
        )
        for pth in r.still_gap_inject[:4]:
            print(f"      修正側にも GAP_INJECT が残る経路: {pth}")

    n_pass = sum(1 for r in results if r.two_sided)
    n_cleared = sum(1 for r in results if r.pair_cleared)
    n_cleared_inj = sum(1 for r in results if r.pair_cleared_inject)
    measured = [r for r in results if r.pass_preregistered is not None]
    n_strict = sum(1 for r in measured if r.pass_preregistered)
    n_coord = sum(1 for r in measured if r.pass_coord_match)
    n_trees = len({(r.vuln_root, r.fixed_root) for r in results})
    print(f"\n[腕 {args.arm}] 対 = {len(results)}（CVE 単位。木の対は {n_trees}）")
    print(f"両側通過（3 列、prereg §5 #2 (a)）: 事前登録照合 {n_strict}/{len(measured)} ｜ "
          f"座標一致 {n_coord}/{len(measured)} ｜ any-change {n_pass}/{len(results)}")
    if len(measured) < len(results):
        print(f"  期待表に無い対 {len(results) - len(measured)}（未測定。False にしない）")
    print("**主指標は事前登録照合。any-change は逆向きの対や sink 名の置換だけの対も通すので併記にとどめる**")
    print(f"verdict-clearing（必須併記）: 厳密 {n_cleared}/{n_pass} / "
          f"INJECT 座標のみ {n_cleared_inj}/{n_pass}")
    print("**タプル変化のみで通過した対と区別せずに報告すると「修正を検出した」と誤読される**")
    if n_cleared == 0 and n_pass:
        print("→ 厳密版が 0 なのは `GAP_SELECT` が値検証では消えないため。"
              "消えるのは承認割り込みを足した対だけである。**この理由を本文に書く**")

    if args.json:
        os.makedirs(os.path.dirname(args.json) or ".", exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(
                {
                    "accepted_reasons": sorted(ACCEPTED_REASONS),
                    "na_reasons": sorted(NA_REASONS),
                    "coords": list(TUPLE_COORDS),
                    "arm": args.arm,
                    "n_pairs": len(results),
                    "n_tree_pairs": n_trees,
                    "n_two_sided_pass": n_pass,
                    "n_pass_preregistered": n_strict,
                    "n_pass_coord_match": n_coord,
                    "n_measured": len(measured),
                    "n_verdict_clearing_pairs_strict": n_cleared,
                    "n_verdict_clearing_pairs_inject": n_cleared_inj,
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
