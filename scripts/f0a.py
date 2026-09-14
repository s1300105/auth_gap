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


@dataclass
class PopStats:
    """1 母集団ぶんの集計。"""

    population: str
    n_trees: int = 0
    n_trees_failed: int = 0
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
    #: rubric 1c。
    rubric1c_units: int = 0
    rubric1c_no_validator: int = 0
    #: trig（別 run で埋める）。
    trig_modes: Counter = field(default_factory=Counter)
    parse_failures: int = 0
    truncations: int = 0
    elapsed_s: float = 0.0

    # -- 率 ---------------------------------------------------------------

    def ratio(self, n: int, denom: int) -> float | None:
        return (n / denom) if denom else None

    @property
    def in_tree_resolution_ratio(self) -> float | None:
        """`resolved / (resolved + opaque + remote)`（**効果サイト**の解決率）。"""
        total = sum(self.resolution.values())
        return self.ratio(self.resolution["resolved"], total)

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
            "n_trees_failed": self.n_trees_failed,
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
            "in_tree_resolution_ratio": self.in_tree_resolution_ratio,
            "remote_ratio": self.remote_ratio,
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
            "elapsed_s": round(self.elapsed_s, 1),
        }


def accumulate(stats: PopStats, res: RunResult, rubric: frozenset[str], with_trig: bool) -> None:
    stats.n_trees += 1
    stats.elapsed_s += res.elapsed_s
    stats.parse_failures += len(res.tree.parse_failures)
    stats.truncations += len(res.tree.cap_hits) + len(res.wall_clock_truncations)
    d_op = res.tree.d_op
    for u in res.tree.units:
        _accumulate_unit(stats, u, d_op, rubric, with_trig)


def _accumulate_unit(stats: PopStats, u: UnitReport, d_op, rubric, with_trig: bool) -> None:
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
        for r in e.resolution.reasons:
            stats.resolution_by_cause[r] += 1
        for slot, v in e.control_slots().items():
            stats.slots_all[v.prov.kind] += 1
            if slot in PRIMARY_SLOTS:
                stats.slots_primary[v.prov.kind] += 1
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
    ap.add_argument("--evidence", default=os.path.join(ROOT, "evidence", "f0a"))
    ap.add_argument("--limit", type=int, default=0, help="母集団ごとの上限（動作確認用）")
    args = ap.parse_args()

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

    rubric = load_rubric_1c()
    by_pop: dict[str, PopStats] = {}
    seen: dict[str, int] = {}
    for path, pop in jobs:
        st = by_pop.setdefault(pop, PopStats(pop))
        if args.limit and seen.get(pop, 0) >= args.limit:
            continue
        if not os.path.isdir(path):
            st.n_trees_failed += 1
            continue
        seen[pop] = seen.get(pop, 0) + 1
        t0 = time.monotonic()
        try:
            res = run(RunConfig(src_root=path, population=pop, full=args.with_traced))
        except Exception as exc:  # 1 本の失敗で全体を落とさない。**件数として残す。**
            st.n_trees_failed += 1
            print(f"FAIL {path}: {type(exc).__name__}: {exc}", file=sys.stderr)
            continue
        accumulate(st, res, rubric, args.with_traced)
        print(f"  {os.path.basename(path):48s} units={len(res.tree.units):4d} "
              f"{time.monotonic() - t0:5.1f}s")

    out = {
        "schema": "authgap/f0a/v1",
        "run_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "traced_ratio": None if not args.with_traced else "別 run で計測（母集団別）",
        "populations": {p: s.to_json() for p, s in sorted(by_pop.items())},
    }
    os.makedirs(args.evidence, exist_ok=True)
    dest = os.path.join(args.evidence, "f0a.json")
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(canonical_json(out))
    _write_md(by_pop, args.with_traced)
    print(f"\nwrote {dest} / {F0A_MD} / {F0C_MD}")
    _print_gates(by_pop)
    return 0


def _fmt(x: float | None) -> str:
    return "—" if x is None else f"{x:.1%}"


def _print_gates(by_pop: dict[str, PopStats]) -> None:
    print("\n=== §10 の関門 ===")
    for p, s in sorted(by_pop.items()):
        itr = s.in_tree_resolution_ratio
        vh = s.validator_holding
        op = s.opaque_ratio(True)
        print(f"[{p}] 木 {s.n_trees}（失敗 {s.n_trees_failed}） ユニット {s.n_units}")
        print(f"  in_tree_resolution_ratio {_fmt(itr)}  (>= 50%): "
              f"{'○' if itr is not None and itr >= GATE_IN_TREE_RESOLUTION else '×'}")
        print(f"  validator 保有            {_fmt(vh)}  (>= 5%):  "
              f"{'○' if vh is not None and vh >= GATE_VALIDATOR_HOLDING else '×'}")
        print(f"  opaque 率（主 slot）      {_fmt(op)}  (<= 40%): "
              f"{'○' if op is not None and op <= GATE_OPAQUE else '×'}")
        print(f"  r_D {_fmt(s.r_d)}（粗い分母 {_fmt(s.r_d_crude)}） → {s.branch}")


def _write_md(by_pop: dict[str, PopStats], with_trig: bool) -> None:
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
            f"木 {s.n_trees} 本（取得 / 解析に失敗 {s.n_trees_failed} 本）、"
            f"ユニット {s.n_units}、危険効果を持つユニット {s.n_dangerous}"
            f"（偽陽性クラス除外後 {s.n_dangerous_clean}）",
            "",
            "| 指標 | 値 | 関門 | 判定 |",
            "|---|---|---|---|",
            f"| `in_tree_resolution_ratio` | {_fmt(s.in_tree_resolution_ratio)} | ≥ 50% | "
            f"{'○' if (s.in_tree_resolution_ratio or 0) >= GATE_IN_TREE_RESOLUTION else '×'} |",
            f"| validator 保有ツール | {_fmt(s.validator_holding)} | ≥ 5% | "
            f"{'○' if (s.validator_holding or 0) >= GATE_VALIDATOR_HOLDING else '×'} |",
            f"| opaque 率（主 slot 7 種） | {_fmt(s.opaque_ratio(True))} | ≤ 40% | "
            f"{'○' if (s.opaque_ratio(True) or 1) <= GATE_OPAQUE else '×'} |",
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
            f"parse 失敗 {s.parse_failures} 件、cap 到達 {s.truncations} 件"
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
    with open(F0A_MD, "w", encoding="utf-8") as fh:
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
    with open(F0C_MD, "w", encoding="utf-8") as fh:
        fh.write("\n".join(f0c) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
