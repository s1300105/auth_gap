"""木 1 本を端から端まで走らせる。

逐次ランナー。**再試行・再開の機構は持たない**（§7.3。venv も型環境も作らない
ので不要）。壁時計 cap に当たったファイルは `TRUNCATED` 行として記録する。
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from typing import Optional

from .analyze import TreeReport, UnitReport, analyze_unit_f0a, analyze_unit_full
from .dparse import DOp, DPrev, exposure_as_d_op, in_tree_exposure, parse_d_op
from .enforcement import DepPin, EnforcementVerdict, classify_unit, read_dep_pins
from .entries import find_tool_literals, find_units, join_annotations
from .ir import WALL_CLOCK_CAP
from .srcindex import SourceIndex
from .trig import TrigIndex, build_trig_index
from .val import Options
from .verdict import load_rubric_1c

#: 母集団の種別。D_op の帰属規則がこれで決まる（Def 6）。
POPULATIONS = ("app", "mcp_server", "tool_package")


@dataclass
class RunConfig:
    src_root: str
    population: str = "mcp_server"
    exposure_file: Optional[str] = None
    prev_manifest: Optional[str] = None
    rubric_1c_path: Optional[str] = None
    options: Options = field(default_factory=Options)
    #: 完全解析（支配判定 + 判定）を行うか。偽なら F0a だけ。
    full: bool = True
    #: §3 の 3 腕（``A`` / ``B`` / ``C``）。**同一バイナリのフラグ違い。**
    arm: str = "C"


@dataclass
class RunResult:
    tree: TreeReport
    enforcement: dict[str, EnforcementVerdict] = field(default_factory=dict)
    dep_pins: dict[str, DepPin] = field(default_factory=dict)
    exposure_declarations: list[dict] = field(default_factory=list)
    wall_clock_truncations: list[str] = field(default_factory=list)
    elapsed_s: float = 0.0


def run(cfg: RunConfig) -> RunResult:
    started = time.monotonic()
    index = SourceIndex(cfg.src_root)
    index.build()

    units = find_units(index)
    literals = find_tool_literals(index)
    joined, unjoined = join_annotations(units, literals)

    trig_index: TrigIndex = build_trig_index(index, units)
    d_op: DOp = parse_d_op(index, cfg.population, cfg.exposure_file)
    exposure_decls = in_tree_exposure(index)
    in_tree_d_op = exposure_as_d_op(exposure_decls)
    if not in_tree_d_op.is_bottom:
        # §8-7 の凍結: in-tree の露出宣言を D_op に**含める**。
        d_op = DOp(
            allow=d_op.allow,
            ask=d_op.ask,
            deny=d_op.deny | in_tree_d_op.deny,
            source=d_op.source or in_tree_d_op.source,
            excluded_files=d_op.excluded_files,
        )
    rubric = load_rubric_1c(cfg.rubric_1c_path)
    prev = DPrev.load(cfg.prev_manifest) if cfg.prev_manifest else None
    pins = read_dep_pins(cfg.src_root)

    tree = TreeReport(
        src_root=os.path.abspath(cfg.src_root),
        population=cfg.population,
        trig_index=trig_index,
        d_op=d_op,
        n_tool_literals=len(literals),
        n_annotation_joined=joined,
        n_annotation_unjoined=unjoined,
    )
    res = RunResult(tree=tree, dep_pins=pins)

    for unit in units:
        t0 = time.monotonic()
        if cfg.full:
            report: UnitReport = analyze_unit_full(
                index,
                unit,
                trig_index,
                d_op,
                rubric_1c=rubric,
                exposure_supplied=bool(cfg.exposure_file),
                prev_unit=prev.join(unit.unit_id) if prev else None,
                options=cfg.options,
                arm=cfg.arm,
            )
        else:
            report = analyze_unit_f0a(index, unit, cfg.options)
        if time.monotonic() - t0 > WALL_CLOCK_CAP:
            res.wall_clock_truncations.append(unit.unit_id)
            report.notes.append("TRUNCATED(wall_clock)")
        tree.units.append(report)
        res.enforcement[unit.unit_id] = classify_unit(unit.framework, unit.entry_kind, pins)

    tree.parse_failures = sorted(index.parse_failures)
    tree.cap_hits = sorted(index.cap_hits)
    res.exposure_declarations = exposure_decls
    res.elapsed_s = time.monotonic() - started
    return res
