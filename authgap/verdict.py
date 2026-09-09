"""Def 7: 判定。

**層ごとに独立に評価する。** D_dom は SELECT を被覆せず、D_kind は INJECT を
被覆しない（Def 6 の「層ごとに独立」）。

**`UNKNOWN` を決して clean にしない。** remote / opaque / 動的レジストリ /
`D_unknown` は manifest に `resolution=opaque(reason)|remote` の行として残す。

**全 GAP 行と全 INVENTORY 行に `covered_by` と `D_layer_present` の 2 列を必須にする。**
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any, Optional

from .catalog.sinks import PRIMARY_SLOTS
from .dparse import DKind, DOp
from .effects import Effect
from .ir import Prin, Req

#: verdict の語彙（Def 7）。
VERDICTS = (
    "GAP_SELECT",
    "GAP_INJECT",
    "GAP_DRIFT",
    "CONTRADICTION",
    "INVENTORY",
    "UNKNOWN",
)

#: 明示ベースライン P0（Def 6）。
#: 「MODEL は EXEC / SPAWN / 正規化なしの FS_READ・FS_WRITE / private-range NET に
#: 届いてはならない」。
P0_KINDS = frozenset({"EXEC", "SPAWN", "FS_READ", "FS_WRITE"})


@dataclass
class Row:
    """manifest の 1 行 = `(unit id, effect, position)`。"""

    unit_id: str
    effect: Effect
    slot: Optional[str] = None
    verdicts: set[str] = field(default_factory=set)
    covered_by: Optional[str] = None
    d_layer_present: tuple[str, ...] = ()
    #: 規則 W によって GAP になった行か（比率を指標に出す）。
    rule_w: bool = False
    #: rubric 1c の判定に使った経路。
    rubric_1c: Optional[str] = None
    notes: tuple[str, ...] = ()

    def to_json(self) -> dict:
        d: dict[str, Any] = {
            "unit_id": self.unit_id,
            "kind": self.effect.kind,
            "site": self.effect.site,
            "form": self.effect.form,
            "lineno": self.effect.lineno,
            "relpath": self.effect.relpath,
            "verdicts": sorted(self.verdicts),
            "covered_by": self.covered_by,
            "D_layer_present": list(self.d_layer_present),
        }
        if self.slot:
            d["slot"] = self.slot
        if self.rule_w:
            d["rule_w"] = True
        if self.rubric_1c:
            d["rubric_1c"] = self.rubric_1c
        if self.notes:
            d["notes"] = list(self.notes)
        return d


# --------------------------------------------------------------------------
# 凍結済み rubric 1c
# --------------------------------------------------------------------------


def load_rubric_1c(path: Optional[str] = None) -> frozenset[str]:
    """仕様として任意実行するツールの名前（`docs/rubric_1c.json` に凍結）。"""
    if path is None:
        path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "rubric_1c.json"
        )
    if not os.path.exists(path):
        return frozenset()
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    return frozenset(data.get("tool_names", []))


# --------------------------------------------------------------------------
# 判定
# --------------------------------------------------------------------------


@dataclass
class UnitVerdictInput:
    """1 ユニットぶんの入力。"""

    unit_id: str
    tool_name: Optional[str]
    effects: list[Effect]
    trig_label: Prin
    trig_mode: str  # traced | assumed
    req_occ: Req
    #: `(effect index, slot) -> req_val`
    req_val: dict[tuple[int, str], Req]
    #: `(effect index, slot) -> (等級, weak 理由)`
    grades: dict[tuple[int, str], tuple[Optional[str], Optional[str]]]
    d_kind: DKind
    d_op: DOp
    #: D_prev との差分規則の結果。
    drift_reasons: tuple[str, ...] = ()
    #: 解析経路で立った opaque 理由。
    opaque_reasons: tuple[str, ...] = ()
    #: 運用者が exposure ファイルを供給したか（rubric 1c が要求する）。
    exposure_supplied: bool = False
    rubric_1c_names: frozenset[str] = frozenset()
    #: `effect index -> req_occ`（**`req_occ(e)` は効果ごと**。Def 5）。
    #: **既定値つきなので必ず末尾に置く**（位置引数の並びを崩さないため）。
    req_occ_by_effect: dict[int, Req] = field(default_factory=dict)


def decide(inp: UnitVerdictInput) -> list[Row]:
    """Def 7 の判定を行い、行の列を返す。

    行は `(unit id, effect, position)` 単位。**行の verdict は集合である**（§3）。
    """
    rows: list[Row] = []
    effect_kinds = {e.kind for e in inp.effects}
    d_layers = _layers_present(inp)

    contradiction_flag = _contradiction(inp, effect_kinds)

    for i, eff in enumerate(inp.effects):
        # -- UNKNOWN: 解決できていない行は clean にしない -------------------
        unresolved = eff.resolution.kind != "resolved" or bool(inp.opaque_reasons)

        # -- SELECT 座標（効果ごとに 1 行）-------------------------------
        sel = Row(inp.unit_id, eff, None, set(), None, d_layers)
        if contradiction_flag and eff.kind in ("EXEC", "SPAWN", "FS_WRITE"):
            sel.verdicts.add("CONTRADICTION")
        occ = inp.req_occ_by_effect.get(i, inp.req_occ)
        if inp.trig_label is Prin.MODEL and inp.trig_mode == "traced" and occ is Req.MODEL:
            if inp.d_op.covers(inp.tool_name):
                sel.verdicts.add("INVENTORY")
                sel.covered_by = "op"
            elif inp.d_kind.covers(eff.kind):
                sel.verdicts.add("INVENTORY")
                sel.covered_by = "kind"
            else:
                sel.verdicts.add("GAP_SELECT")
        elif inp.trig_mode == "assumed":
            # **`assumed` の trig では SELECT 行は GAP ではなくマニフェスト行。**
            sel.notes = sel.notes + ("select_manifest_only(assumed_trig)",)
        if inp.drift_reasons and inp.d_kind.is_bottom and inp.d_op.is_bottom:
            sel.verdicts.add("GAP_DRIFT")
            sel.covered_by = sel.covered_by or "prev"
            sel.notes = sel.notes + tuple(inp.drift_reasons)
        if unresolved:
            sel.verdicts.add("UNKNOWN")
        if sel.verdicts or sel.notes:
            rows.append(sel)

        # -- INJECT 座標（制御位置ごとに 1 行）---------------------------
        for slot, value in sorted(eff.control_slots().items()):
            grade, weak_reason = inp.grades.get((i, slot), (None, None))
            req = inp.req_val.get((i, slot), Req.MODEL)
            row = Row(inp.unit_id, eff, slot, set(), None, d_layers)

            if value.prov.kind != "resolved":
                row.verdicts.add("UNKNOWN")

            if value.prin is not Prin.MODEL:
                if row.verdicts:
                    rows.append(row)
                continue

            # 規則 W: weak validator は宣言に優先する（D_op には優先しない）。
            weak = grade == "weak"
            if req is not Req.MODEL and not weak:
                # ゲートが引き上げているので GAP ではない。
                continue

            if inp.d_op.covers(inp.tool_name):
                row.verdicts.add("INVENTORY")
                row.covered_by = "op"
                rows.append(row)
                continue

            # rubric 1c（凍結済み）
            if inp.tool_name in inp.rubric_1c_names and slot in PRIMARY_SLOTS:
                any_validator = any(
                    inp.grades.get((i, s), (None, None))[0] is not None
                    for s in eff.control_slots()
                )
                if not any_validator and inp.exposure_supplied:
                    row.verdicts.add("INVENTORY")
                    row.covered_by = "op"
                    row.rubric_1c = "inventory(no_validator+exposure)"
                    rows.append(row)
                    continue
                row.rubric_1c = (
                    "gap(rule_w:weak_validator)" if weak else "gap(P0:no_exposure)"
                )

            # D_dom は実装条件を満たすまで常に ⊥（反証条件 F1）。
            # D_kind は kind の上界しか宣言せず**制御位置を宣言しないので
            # INJECT を被覆しない**。宣言があることは行に記録するだけ。
            if inp.d_kind.covers(eff.kind):
                row.notes = row.notes + (f"D_layer_present:kind:{eff.kind}",)

            if eff.kind in P0_KINDS or eff.kind in ("DB", "NET"):
                row.verdicts.add("GAP_INJECT")
                row.rule_w = weak
            if row.verdicts:
                rows.append(row)

    return rows


def _contradiction(inp: UnitVerdictInput, effect_kinds: set[str]) -> bool:
    from .dparse import contradiction as _c

    return _c(inp.d_kind, effect_kinds)


def _layers_present(inp: UnitVerdictInput) -> tuple[str, ...]:
    out: list[str] = []
    if not inp.d_kind.is_bottom:
        out.append("kind")
    if inp.d_kind.present_no_bound:
        out.append("kind_no_bound")
    if not inp.d_op.is_bottom:
        out.append("op")
    if inp.drift_reasons:
        out.append("prev")
    if inp.d_kind.unknown:
        out.append("unknown")
    return tuple(out)
