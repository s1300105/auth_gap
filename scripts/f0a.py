#!/usr/bin/env python3
"""F0a（真の床）の実行と集計（§6 F0a / §10 の D 規則）。

**支配判定に依存しない。** ユニットごとの危険効果 kind の真偽値、構文的
validator 形状、config atom と既定値、annotation の有無、ゲート述語の存在
（支配判定なし）だけを測る。

§10 の D 規則がここで決まる。**分母は 2 通り出す**:

* 粗い分母 = 危険効果を持つユニット
* 偽陽性クラスを除いた分母 = そこから非 DB の `.execute()` 等を除いたもの

**`r_D` は和ではなく和集合**（`D_kind ≠ ⊥` または `D_op ≠ ⊥` を満たすユニット。
両層を持つユニットは 1 回だけ数える。`r_kind + r_op` という書き方は誤り）。

**`traced_ratio` は A5 の run では `null`。** traced 率は別 run で測り、
**母集団別（低レベル MCP / 高レベル MCP / ツールパッケージ / アプリ）に出す**
（`docs/decisions.md` D9 — 1 つに平均すると構造差が消える）。

使い方::

    python scripts/f0a.py --sample docs/corpus_sample.json
    python scripts/f0a.py --trees corpus/w-a__b corpus/w-c__d --with-traced
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
import time
from collections import Counter
from dataclasses import dataclass, field

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from authgap.analyze import UnitReport  # noqa: E402
from authgap.catalog.sinks import DANGEROUS_KINDS, PRIMARY_SLOTS  # noqa: E402
from authgap.report import canonical_json  # noqa: E402
from authgap.runner import RunConfig, RunResult, run  # noqa: E402
from authgap.verdict import load_rubric_1c  # noqa: E402

F0A_MD = os.path.join(ROOT, "docs", "f0a.md")
F0C_MD = os.path.join(ROOT, "docs", "f0c.md")

#: §10 の関門。
GATE_IN_TREE_RESOLUTION = 0.50
GATE_VALIDATOR_HOLDING = 0.05
GATE_OPAQUE = 0.40
#: D 規則の分岐境界。
BRANCH_HIGH = 0.20
BRANCH_LOW = 0.05

#: 確度の合流順（`authgap.ir.prov_merge` と同じ。**resolved を優先しない**）。
_PROV_RANK = {"resolved": 0, "remote": 1, "opaque": 2}


def _merge_prov_kind(old: str | None, new: str) -> str:
    return new if old is None or _PROV_RANK[new] > _PROV_RANK[old] else old


@dataclass
class PopStats:
    """1 母集団ぶんの集計。"""

    population: str
    n_trees: int = 0
    #: 取得できていない木（`corpus/` に無い）。**抽出順で次を繰り上げる**ので
    #: 上限の枠を消費しない。件数は残す。
    n_trees_missing: int = 0
    #: 解析中に例外で落ちた木。**繰り上げない**（道具の失敗を置き換えで隠さない）。
    n_trees_failed: int = 0
    #: 解析できたがユニットが 1 件も無かった木。
    #: **フレームの雑音を測る量である**（code search で集めた母集団には
    #: クライアント / 例 / fork / 無関係な repo が混ざる）。
    n_trees_no_units: int = 0
    n_units: int = 0
    #: 危険効果を持つユニット（粗い分母）。
    n_dangerous: int = 0
    #: 偽陽性クラス（`db_unresolved` だけのユニット）を除いた分母。
    n_dangerous_clean: int = 0
    n_effects: Counter = field(default_factory=Counter)
    resolution: Counter = field(default_factory=Counter)
    resolution_by_cause: Counter = field(default_factory=Counter)
    shapes: Counter = field(default_factory=Counter)
    n_with_validator: int = 0
    n_with_gate_predicate: int = 0
    #: D 層。
    n_d_kind: int = 0
    n_d_kind_clean: int = 0
    n_d_op: int = 0
    n_d_union: int = 0
    n_d_union_clean: int = 0
    n_annotations_present: int = 0
    n_d_unknown: int = 0
    #: 発生ゲートの 4 形態別。
    occurrence_gates: Counter = field(default_factory=Counter)
    #: 制御位置の確度（主 slot 限定 / 全 slot）。
    slots_primary: Counter = field(default_factory=Counter)
    slots_all: Counter = field(default_factory=Counter)
    #: **サイト単位**（(木, relpath, lineno, kind) → 合流した確度）。効果行は呼び出し
    #: 経路ごとに複製されるので、行で数えると少数のサイトに重みが集中する。
    #: 合流は `prov_merge` と同じ優先順 `opaque > remote > resolved`。
    site_resolution: dict = field(default_factory=dict)
    #: (木, relpath, lineno, kind, slot) → 合流した確度。
    site_slots: dict = field(default_factory=dict)
    #: rubric 1c。
    rubric1c_units: int = 0
    rubric1c_no_validator: int = 0
    #: trig（別 run で埋める）。
    trig_modes: Counter = field(default_factory=Counter)
    parse_failures: int = 0
    truncations: int = 0
    #: 木ごとの時間上限で解析しなかったユニット数。
    budget_skipped: int = 0
    elapsed_s: float = 0.0

    # -- 率 ---------------------------------------------------------------

    def ratio(self, n: int, denom: int) -> float | None:
        return (n / denom) if denom else None

    @property
    def in_tree_resolution_ratio(self) -> float | None:
        """`resolved / (resolved + opaque + remote)`（**効果行**単位。併記用）。"""
        total = sum(self.resolution.values())
        return self.ratio(self.resolution["resolved"], total)

    @property
    def in_tree_resolution_ratio_sites(self) -> float | None:
        """同じ比を**効果サイト**単位で（§1 の文言どおり。§10 の関門はこれで判定する）。"""
        c = Counter(self.site_resolution.values())
        return self.ratio(c["resolved"], sum(c.values()))

    def opaque_ratio_sites(self, primary: bool = True) -> float | None:
        """`opaque / (resolved + opaque)` をサイト × slot 単位で。`remote` は分母に入れない。"""
        c = Counter(
            kind for key, kind in self.site_slots.items() if not primary or key[4] in PRIMARY_SLOTS
        )
        return self.ratio(c["opaque"], c["resolved"] + c["opaque"])

    @property
    def remote_ratio(self) -> float | None:
        """**関門ではなく報告値**（§1）。"""
        total = sum(self.resolution.values())
        return self.ratio(self.resolution["remote"], total)

    def opaque_ratio(self, primary: bool = True) -> float | None:
        """`opaque / (resolved + opaque)`。**`remote` は分母に入れない。**"""
        c = self.slots_primary if primary else self.slots_all
        denom = c["resolved"] + c["opaque"]
        return self.ratio(c["opaque"], denom)

    @property
    def r_kind(self) -> float | None:
        return self.ratio(self.n_d_kind_clean, self.n_dangerous_clean)

    @property
    def r_kind_crude(self) -> float | None:
        return self.ratio(self.n_d_kind, self.n_dangerous)

    @property
    def r_op(self) -> float | None:
        return self.ratio(self.n_d_op, self.n_dangerous_clean)

    @property
    def r_d(self) -> float | None:
        """**和集合**。`r_kind + r_op` ではない。"""
        return self.ratio(self.n_d_union_clean, self.n_dangerous_clean)

    @property
    def r_d_crude(self) -> float | None:
        return self.ratio(self.n_d_union, self.n_dangerous)

    @property
    def validator_holding(self) -> float | None:
        return self.ratio(self.n_with_validator, self.n_units)

    @property
    def branch(self) -> str:
        """§10 の D 規則の分岐。**偽陽性クラスを除いた分母で判断する**（反証条件 F2）。"""
        r = self.r_d
        if r is None:
            return "判定不能（危険効果を持つユニットが 0）"
        if r >= BRANCH_HIGH:
            return "分岐 1（thesis sentence を維持。ただし covered_by の層別内訳を必須にする）"
        if r >= BRANCH_LOW:
            return "分岐 2（宣言がある箇所は D との差、無い箇所は P0 との差を報告）"
        return "分岐 3（宣言との差を主張から外し、P0 と D_prev に主張順序を移す）"

    def to_json(self) -> dict:
        return {
            "population": self.population,
            "n_trees": self.n_trees,
            "n_trees_missing_promoted": self.n_trees_missing,
            "n_trees_failed": self.n_trees_failed,
            "n_trees_no_units": self.n_trees_no_units,
            "n_units": self.n_units,
            "n_units_with_dangerous_effect": self.n_dangerous,
            "n_units_with_dangerous_effect_fp_excluded": self.n_dangerous_clean,
            "n_effects_by_kind": dict(sorted(self.n_effects.items())),
            "resolution": dict(sorted(self.resolution.items())),
            "resolution_by_cause": dict(sorted(self.resolution_by_cause.items())),
            "validator_shapes": dict(sorted(self.shapes.items())),
            "n_units_with_validator": self.n_with_validator,
            "n_units_with_gate_predicate": self.n_with_gate_predicate,
            "occurrence_gate_forms": dict(sorted(self.occurrence_gates.items())),
            "D": {
                "n_d_kind": self.n_d_kind,
                "n_d_kind_fp_excluded": self.n_d_kind_clean,
                "n_d_op": self.n_d_op,
                "n_d_union": self.n_d_union,
                "n_d_union_fp_excluded": self.n_d_union_clean,
                "n_annotations_present": self.n_annotations_present,
                "n_d_unknown": self.n_d_unknown,
                "r_kind_fp_excluded": self.r_kind,
                "r_kind_crude": self.r_kind_crude,
                "r_dom": 0.0,
                "r_op": self.r_op,
                "r_D_fp_excluded": self.r_d,
                "r_D_crude": self.r_d_crude,
                "branch": self.branch,
            },
            "n_effect_rows": sum(self.resolution.values()),
            "n_effect_sites": len(self.site_resolution),
            "resolution_sites": dict(sorted(Counter(self.site_resolution.values()).items())),
            "in_tree_resolution_ratio_sites": self.in_tree_resolution_ratio_sites,
            "in_tree_resolution_ratio": self.in_tree_resolution_ratio,
            "remote_ratio": self.remote_ratio,
            "opaque_ratio_primary_slots_sites": self.opaque_ratio_sites(True),
            "opaque_ratio_all_slots_sites": self.opaque_ratio_sites(False),
            "opaque_ratio_primary_slots": self.opaque_ratio(True),
            "opaque_ratio_all_slots": self.opaque_ratio(False),
            "validator_holding_ratio": self.validator_holding,
            "rubric1c": {
                "n_units": self.rubric1c_units,
                "n_units_without_validator": self.rubric1c_no_validator,
            },
            "trig_modes": dict(sorted(self.trig_modes.items())),
            "parse_failures": self.parse_failures,
            "truncations": self.truncations,
            "units_skipped_by_tree_budget": self.budget_skipped,
            "elapsed_s": round(self.elapsed_s, 1),
        }


def accumulate(stats: PopStats, res: RunResult, rubric: frozenset[str], with_trig: bool) -> None:
    stats.n_trees += 1
    if not res.tree.units:
        stats.n_trees_no_units += 1
    stats.elapsed_s += res.elapsed_s
    stats.parse_failures += len(res.tree.parse_failures)
    stats.truncations += len(res.tree.cap_hits) + len(res.wall_clock_truncations)
    stats.budget_skipped += res.tree_budget_skipped
    d_op = res.tree.d_op
    tree = os.path.basename(res.tree.src_root)
    for u in res.tree.units:
        _accumulate_unit(stats, u, d_op, rubric, with_trig, tree)


def _accumulate_unit(
    stats: PopStats, u: UnitReport, d_op, rubric, with_trig: bool, tree: str = ""
) -> None:
    stats.n_units += 1
    for s in u.validator_shapes:
        stats.shapes[s] += 1
    if u.validator_shapes:
        stats.n_with_validator += 1
    if u.gate_predicate_present:
        stats.n_with_gate_predicate += 1
    for name, closed in u.config_atoms.items():
        stats.occurrence_gates[f"atom:{name}:{'closed' if closed else 'open/unknown'}"] += 1
    if u.unit.annotations is not None:
        stats.n_annotations_present += 1
    if u.d_kind.unknown:
        stats.n_d_unknown += 1
    if with_trig and u.trig is not None:
        stats.trig_modes[f"{u.unit.framework}:{u.trig.mode}"] += 1

    dangerous = [e for e in u.effects if e.kind in DANGEROUS_KINDS]
    for e in u.effects:
        stats.n_effects[e.kind] += 1
        stats.resolution[e.resolution.kind] += 1
        site = (tree, e.relpath, e.lineno, e.kind)
        stats.site_resolution[site] = _merge_prov_kind(
            stats.site_resolution.get(site), e.resolution.kind
        )
        for r in e.resolution.reasons:
            stats.resolution_by_cause[r] += 1
        for slot, v in e.control_slots().items():
            stats.slots_all[v.prov.kind] += 1
            if slot in PRIMARY_SLOTS:
                stats.slots_primary[v.prov.kind] += 1
            sk = site + (slot,)
            stats.site_slots[sk] = _merge_prov_kind(stats.site_slots.get(sk), v.prov.kind)
    if u.val is not None:
        for r in u.val.opaque_reasons:
            stats.resolution_by_cause[r] += 1

    if not dangerous:
        return
    stats.n_dangerous += 1
    # **偽陽性クラスを除いた分母**: 危険効果が `db_unresolved` だけのユニットは除く。
    real = [e for e in dangerous if e.db_rule != "db_unresolved"]
    clean = bool(real)
    if clean:
        stats.n_dangerous_clean += 1

    has_kind = not u.d_kind.is_bottom
    has_op = bool(d_op is not None and d_op.covers(u.unit.tool_name))
    if has_kind:
        stats.n_d_kind += 1
        if clean:
            stats.n_d_kind_clean += 1
    if has_op:
        stats.n_d_op += 1
    if has_kind or has_op:  # **和集合。両層を持つユニットは 1 回だけ。**
        stats.n_d_union += 1
        if clean:
            stats.n_d_union_clean += 1

    if u.unit.tool_name in rubric:
        stats.rubric1c_units += 1
        if not u.validator_shapes:
            stats.rubric1c_no_validator += 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", default=os.path.join(ROOT, "docs", "corpus_sample.json"))
    ap.add_argument("--trees", nargs="*", help="木を直接指定（population は --population）")
    ap.add_argument("--population", default="mcp_server")
    ap.add_argument("--with-traced", action="store_true",
                    help="trig を計算する。**A5 の run では使わない**（§5.1）")
    ap.add_argument("--evidence", default=None,
                    help="既定は evidence/f0a（--label があれば evidence/f0a_<label>）")
    ap.add_argument("--label", default="",
                    help="run の名前（例: run2）。**前の run の出力を上書きしない**ため、"
                         "docs/f0a_<label>.md と evidence/f0a_<label>/ に書く（D14）")
    ap.add_argument("--limit", type=int, default=0,
                    help="全母集団に同じ上限を掛ける（煙試験用）。指定すると --limits を無視する")
    ap.add_argument("--limits", default="mcp_server=60,tool_package=30,app=8",
                    help="母集団ごとの上限（§6 の標本設計 60 / 30 / 8）。"
                         "**取得できた木を抽出順に先頭から数える**（失敗は繰り上げ）")
    ap.add_argument("--tree-budget", type=float, default=180.0,
                    help="1 本の木の壁時計上限（秒）。超えた分は TRUNCATED として記録する")
    args = ap.parse_args()
    suffix = f"_{args.label}" if args.label else ""
    if args.evidence is None:
        args.evidence = os.path.join(ROOT, "evidence", f"f0a{suffix}")
    md_a = os.path.join(ROOT, "docs", f"f0a{suffix}.md")
    md_c = os.path.join(ROOT, "docs", f"f0c{suffix}.md")

    jobs: list[tuple[str, str]] = []
    if args.trees:
        jobs = [(t, args.population) for t in args.trees]
    else:
        if not os.path.exists(args.sample):
            print(f"{args.sample} が無い。先に scripts/sample_corpus.py", file=sys.stderr)
            return 2
        with open(args.sample, encoding="utf-8") as fh:
            for t in json.load(fh)["targets"]:
                path = os.path.join(ROOT, "corpus", t["name"])
                jobs.append((path, t.get("population", "mcp_server")))

    limits = _parse_limits(args.limits) if not args.limit else {}
    rubric = load_rubric_1c()
    by_pop: dict[str, PopStats] = {}
    seen: dict[str, int] = {}
    tree_rows: list[dict] = []
    unit_rows: list[dict] = []
    for path, pop in jobs:
        st = by_pop.setdefault(pop, PopStats(pop))
        cap = args.limit or limits.get(pop, 0)
        if cap and seen.get(pop, 0) >= cap:
            continue
        if not _tree_ready(path):
            # **取得できていない木は枠を消費しない**（抽出順で次を繰り上げる）。
            st.n_trees_missing += 1
            tree_rows.append({"tree": os.path.basename(path), "population": pop, "status": "missing"})
            continue
        seen[pop] = seen.get(pop, 0) + 1
        t0 = time.monotonic()
        try:
            res = run(
                RunConfig(
                    src_root=path,
                    population=pop,
                    full=args.with_traced,
                    max_tree_seconds=args.tree_budget,
                )
            )
        except Exception as exc:  # 1 本の失敗で全体を落とさない。**件数として残す。**
            st.n_trees_failed += 1
            tree_rows.append({
                "tree": os.path.basename(path), "population": pop, "status": "analysis_failed",
                "error": f"{type(exc).__name__}: {exc}",
            })
            print(f"FAIL {path}: {type(exc).__name__}: {exc}", file=sys.stderr)
            continue
        accumulate(st, res, rubric, args.with_traced)
        tree_rows.append(_tree_row(path, pop, res))
        unit_rows.extend(_unit_rows(path, pop, res, rubric))
        print(f"  {os.path.basename(path):48s} units={len(res.tree.units):4d} "
              f"{time.monotonic() - t0:5.1f}s")

    for pop in sorted(by_pop):
        cap = args.limit or limits.get(pop, 0)
        if cap and seen.get(pop, 0) < cap:
            print(f"**[{pop}] 目標 {cap} 本に届かない（解析 {seen.get(pop, 0)} 本）。**"
                  "取得を待つか、割り増し分が尽きたかを確認すること", file=sys.stderr)

    out = {
        "schema": "authgap/f0a/v1",
        "run_meta": {
            "run_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
            # **どの解析器で測ったか。** 野外データを見た後で解析器を直したら、
            # 直す前の run と後の run を commit で区別して両方報告する。
            "analyzer_commit": _git_head(ROOT),
            "analyzer_dirty": _git_dirty(ROOT),
            "label": args.label or None,
            "sample": os.path.relpath(args.sample, ROOT) if not args.trees else None,
            "limits": {p: (args.limit or limits.get(p, 0)) for p in sorted(by_pop)},
            "tree_budget_s": args.tree_budget,
        },
        "traced_ratio": None if not args.with_traced else "別 run で計測（母集団別）",
        "populations": {p: s.to_json() for p, s in sorted(by_pop.items())},
    }
    os.makedirs(args.evidence, exist_ok=True)
    dest = os.path.join(args.evidence, "f0a.json")
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(canonical_json(out))
    # **手検証用の行データ。** 集計値だけでは学生が 1 件ずつ辿れない。
    with open(os.path.join(args.evidence, "trees.jsonl"), "w", encoding="utf-8") as fh:
        for r in tree_rows:
            fh.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    with open(os.path.join(args.evidence, "units.jsonl"), "w", encoding="utf-8") as fh:
        for r in unit_rows:
            fh.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    _write_md(by_pop, args.with_traced, md_a, md_c)
    print(f"\nwrote {dest} (+ trees.jsonl / units.jsonl) / {md_a} / {md_c}")
    _print_gates(by_pop)
    return 0


def _parse_limits(spec: str) -> dict[str, int]:
    out: dict[str, int] = {}
    for part in spec.split(","):
        if not part.strip():
            continue
        k, v = part.split("=")
        out[k.strip()] = int(v)
    return out


def _tree_ready(path: str) -> bool:
    """木が取得済みで checkout が完了しているか（`fetch_corpus._checkout_complete`）。

    **ディレクトリの有無だけで判断しない。** 中断した worktree は空のまま残り、
    解析すると「ユニット 0 件」になって雑音率を押し上げる。
    """
    if not os.path.isdir(path):
        return False
    if not os.path.exists(os.path.join(path, ".git")):
        return True  # git 管理外の木（`--trees` で直接渡したもの）
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    from fetch_corpus import _checkout_complete

    return _checkout_complete(path)


def _git_head(path: str) -> str | None:
    import subprocess

    p = subprocess.run(["git", "rev-parse", "HEAD"], cwd=path, capture_output=True, text=True)
    return p.stdout.strip() if p.returncode == 0 else None


def _git_dirty(path: str) -> bool | None:
    """解析器（`authgap/`）に未コミットの変更があるか。"""
    import subprocess

    p = subprocess.run(
        ["git", "status", "--porcelain", "--", "authgap"], cwd=path, capture_output=True, text=True
    )
    return bool(p.stdout.strip()) if p.returncode == 0 else None


def _tree_row(path: str, pop: str, res: RunResult) -> dict:
    return {
        "tree": os.path.basename(path),
        "population": pop,
        "status": "analyzed",
        "commit_sha": _git_head(path),
        "n_units": len(res.tree.units),
        "n_tool_literals": res.tree.n_tool_literals,
        "parse_failures": len(res.tree.parse_failures),
        "cap_hits": len(res.tree.cap_hits),
        "units_skipped_by_tree_budget": res.tree_budget_skipped,
        "d_op_source": res.tree.d_op.source if res.tree.d_op is not None else None,
    }


def _unit_rows(path: str, pop: str, res: RunResult, rubric: frozenset[str]) -> list[dict]:
    """1 ユニット 1 行。**集計に入った判断を全部そのまま出す**（手で辿れるように）。"""
    rows = []
    d_op = res.tree.d_op
    for u in res.tree.units:
        dangerous = [e for e in u.effects if e.kind in DANGEROUS_KINDS]
        rows.append({
            "tree": os.path.basename(path),
            "population": pop,
            "unit_id": u.unit.unit_id,
            "tool_name": u.unit.tool_name,
            "framework": u.unit.framework,
            "entry_kind": u.unit.entry_kind,
            "relpath": u.unit.relpath,
            "lineno": getattr(u.unit.node, "lineno", None),
            "effects": [
                {
                    "kind": e.kind,
                    "form": e.form,
                    "relpath": e.relpath,
                    "lineno": e.lineno,
                    "resolution": e.resolution.kind,
                    "resolution_reasons": list(e.resolution.reasons),
                    "db_rule": e.db_rule,
                    "slots": {s: v.prov.kind for s, v in sorted(e.control_slots().items())},
                }
                for e in u.effects
            ],
            "dangerous": bool(dangerous),
            "dangerous_fp_excluded": any(e.db_rule != "db_unresolved" for e in dangerous),
            "validator_shapes": list(u.validator_shapes),
            "gate_predicate_present": u.gate_predicate_present,
            "config_atoms": {k: v for k, v in sorted(u.config_atoms.items())},
            "annotations_present": u.unit.annotations is not None,
            "D_kind": u.d_kind.to_json(),
            "D_op_covers": bool(d_op is not None and d_op.covers(u.unit.tool_name)),
            "rubric1c": u.unit.tool_name in rubric,
            "notes": list(u.notes),
        })
    return rows


def _fmt(x: float | None) -> str:
    return "—" if x is None else f"{x:.1%}"


def _ge(x: float | None, thr: float) -> str:
    """関門 `x >= thr`。**分母 0 は × ではなく「不明」**（黙って不合格に倒さない）。"""
    return "不明" if x is None else ("○" if x >= thr else "×")


def _le(x: float | None, thr: float) -> str:
    """関門 `x <= thr`。`0.0` を偽値として扱わない（`x or 1` は 0% を不合格にする）。"""
    return "不明" if x is None else ("○" if x <= thr else "×")


def _print_gates(by_pop: dict[str, PopStats]) -> None:
    print("\n=== §10 の関門 ===")
    for p, s in sorted(by_pop.items()):
        # **関門はサイト単位で判定する**（D15）。行単位は下に併記する。
        itr = s.in_tree_resolution_ratio_sites
        vh = s.validator_holding
        op = s.opaque_ratio_sites(True)
        print(f"[{p}] 木 {s.n_trees}（未取得 {s.n_trees_missing} / 解析失敗 {s.n_trees_failed} / "
              f"ユニット 0 件 {s.n_trees_no_units}） ユニット {s.n_units}")
        print(f"  in_tree_resolution_ratio {_fmt(itr)}  (>= 50%): {_ge(itr, GATE_IN_TREE_RESOLUTION)}")
        print(f"  validator 保有            {_fmt(vh)}  (>= 5%):  {_ge(vh, GATE_VALIDATOR_HOLDING)}")
        print(f"  opaque 率（主 slot）      {_fmt(op)}  (<= 40%): {_le(op, GATE_OPAQUE)}")
        print(f"  （行単位: resolution {_fmt(s.in_tree_resolution_ratio)} / "
              f"opaque {_fmt(s.opaque_ratio(True))}。サイト {len(s.site_resolution)} / "
              f"行 {sum(s.resolution.values())}）")
        print(f"  r_D {_fmt(s.r_d)}（粗い分母 {_fmt(s.r_d_crude)}） → {s.branch}")


def _write_md(
    by_pop: dict[str, PopStats], with_trig: bool, f0a_md: str = F0A_MD, f0c_md: str = F0C_MD
) -> None:
    lines = [
        "# F0a（真の床）",
        "",
        "**支配判定に依存しない測定**（§6 F0a）。ユニットごとの危険効果 kind の",
        "真偽値、構文的 validator 形状、config atom と既定値、annotation の有無、",
        "ゲート述語の存在（支配判定なし）。",
        "",
        "再現: `python scripts/f0a.py --sample docs/corpus_sample.json`",
        "",
        "**分母は 2 通り出す**（§10）。粗い分母 = 危険効果を持つユニット。",
        "偽陽性クラスを除いた分母 = そこから非 DB の `.execute()` 等だけのユニットを除いたもの。",
        "**§10 の分岐判定は偽陽性クラスを除いた分母で行う**（反証条件 F2）。",
        "",
    ]
    for p, s in sorted(by_pop.items()):
        lines += [
            f"## 母集団: {p}",
            "",
            f"解析した木 {s.n_trees} 本（未取得で繰り上げ {s.n_trees_missing} 本、"
            f"解析中の例外 {s.n_trees_failed} 本、"
            f"ユニット 0 件 {s.n_trees_no_units} 本 = **フレームの雑音**）、"
            f"ユニット {s.n_units}、危険効果を持つユニット {s.n_dangerous}"
            f"（偽陽性クラス除外後 {s.n_dangerous_clean}）",
            "",
            "| 指標 | 値 | 関門 | 判定 |",
            "|---|---|---|---|",
            f"| `in_tree_resolution_ratio`（**サイト単位**、{len(s.site_resolution)} サイト） | "
            f"{_fmt(s.in_tree_resolution_ratio_sites)} | ≥ 50% | "
            f"{_ge(s.in_tree_resolution_ratio_sites, GATE_IN_TREE_RESOLUTION)} |",
            f"| 同（行単位、{sum(s.resolution.values())} 行、併記） | "
            f"{_fmt(s.in_tree_resolution_ratio)} | — | — |",
            f"| validator 保有ツール | {_fmt(s.validator_holding)} | ≥ 5% | "
            f"{_ge(s.validator_holding, GATE_VALIDATOR_HOLDING)} |",
            f"| opaque 率（主 slot 7 種、**サイト単位**） | {_fmt(s.opaque_ratio_sites(True))} | ≤ 40% | "
            f"{_le(s.opaque_ratio_sites(True), GATE_OPAQUE)} |",
            f"| opaque 率（主 slot 7 種、行単位、併記） | {_fmt(s.opaque_ratio(True))} | — | — |",
            f"| opaque 率（全 slot、併記） | {_fmt(s.opaque_ratio(False))} | — | — |",
            f"| `remote` 率（**関門ではない**） | {_fmt(s.remote_ratio)} | — | — |",
            "",
            "### D 層別存在率（§10 の D 規則）",
            "",
            "| 率 | 偽陽性クラス除外 | 粗い分母 |",
            "|---|---|---|",
            f"| `r_kind` | {_fmt(s.r_kind)} | {_fmt(s.r_kind_crude)} |",
            "| `r_dom` | 0.0%（**パーサを書かない**。Def 6 の実装条件） | 0.0% |",
            f"| `r_op` | {_fmt(s.r_op)} | — |",
            f"| **`r_D`（和集合）** | **{_fmt(s.r_d)}** | {_fmt(s.r_d_crude)} |",
            "",
            f"**分岐: {s.branch}**",
            "",
            "**`r_D` は和ではなく和集合である。** `r_kind + r_op` という書き方はしない。",
            f"annotation 保有ユニット {s.n_annotations_present} 件のうち、上界を動かす",
            f"フィールドを明示しているのは {s.n_d_kind} 件。読めない形（`D_unknown`）は "
            f"{s.n_d_unknown} 件。",
            "",
            "### 効果と確度",
            "",
            "| kind | 件数 |",
            "|---|---|",
        ]
        for k, v in sorted(s.n_effects.items()):
            lines.append(f"| {k} | {v} |")
        lines += [
            "",
            f"確度: {dict(sorted(s.resolution.items()))}",
            "",
            f"opaque の内訳: {dict(sorted(s.resolution_by_cause.items()))}",
            "",
            "### validator 形状（§6 F0a の語彙）",
            "",
            f"{dict(sorted(s.shapes.items())) or '（0 件）'}",
            "",
            f"ゲート述語を持つユニット {s.n_with_gate_predicate} / {s.n_units}",
            "",
            f"parse 失敗 {s.parse_failures} 件、cap 到達 {s.truncations} 件、"
            f"時間上限で未解析のユニット {s.budget_skipped} 件"
            "（**黙って落としていない**）",
            "",
        ]
        if with_trig and s.trig_modes:
            lines += [
                "### trig（母集団別・登録形別）",
                "",
                "**1 つに平均しない**（`docs/decisions.md` D9）。",
                "",
                f"{dict(sorted(s.trig_modes.items()))}",
                "",
            ]
    with open(f0a_md, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    # -- F0c-1 -----------------------------------------------------------
    f0c = [
        "# F0c（前身の 4 条件を新規に測る）",
        "",
        "**F0c-1（A5 の run で測る）**",
        "",
        "| 条件 | 測定量 | 値 |",
        "|---|---|---|",
    ]
    for p, s in sorted(by_pop.items()):
        f0c.append(
            f"| (iii) ツール本体が別プロセス / HTTP の向こうにある率 | `resolution.remote` "
            f"[{p}] | {_fmt(s.remote_ratio)} |"
        )
    for p, s in sorted(by_pop.items()):
        denom = s.rubric1c_units
        val = (s.rubric1c_no_validator / denom) if denom else None
        f0c.append(
            f"| (iv) 無ガードのシェル実行が仕様である率 | `rubric1c` [{p}] | "
            f"{s.rubric1c_no_validator}/{denom} = {_fmt(val)} |"
        )
    f0c += [
        "",
        "**(ii) framework 境界で型が消える率は AuthGap では測定不能**"
        "（型環境を構築しないため）。**別の量を (ii) の名前で報告してはならない。**",
        "",
        "**(i) dispatch キーが in-tree で解決する率**（`traced_ratio` と",
        "`registry_resolution_ratio`）は **B1 完了後の別 run**で測る。",
        "F0c の完成は B1 完了時点である。",
        "",
        "§1 が F0c に負わせている callee 側反転の正当化は (i)+(iii) と §1.5 で行う。",
        "",
    ]
    with open(f0c_md, "w", encoding="utf-8") as fh:
        fh.write("\n".join(f0c) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
