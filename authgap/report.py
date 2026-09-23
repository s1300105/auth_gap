"""出力層: `probe.json` / `manifest.json` / `results.sarif` / `fingerprint.json`。

**決定論**（§5.2）: manifest から volatile ブロック（実行時刻、経過時間、
絶対パス）を除き、キーをソートして再直列化したうえでのバイト一致。
volatile はトップレベルの `run_meta` に閉じ込める。

**`UNKNOWN` を決して clean にしない。** `resolution=opaque(reason)|remote` の行と
`parse_failure` / `TRUNCATED` 行は必ず出す。
"""

from __future__ import annotations

import hashlib
import json
import os
from typing import Any, Optional

from .analyze import gate_verdict_counts
from .catalog import validators as V
from .catalog.entries import ENTRY_RULES, LLM_CALLS
from .catalog.sinks import DIRECT_SINKS, PIPE_SINKS, PROXY_SINKS, SLOTS, SUB_KINDS
from .enforcement import ENFORCEMENT_TABLE
from .ir import (
    AST_NODE_CAP,
    CFG_NODE_CAP,
    EFFECT_ROW_CAP,
    GATE_NODOM_REASONS,
    GATE_OPAQUE_REASONS,
    MAX_DEPTH,
    SUMMARY_CAP,
    VAL_OPAQUE_REASONS,
    WALL_CLOCK_CAP,
    K,
)
from .runner import RunResult

SCHEMA_VERSION = "authgap/v1"


def canonical_json(obj: Any) -> str:
    """決定論的な直列化。**キーをソートし、区切りを固定する。**"""
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


# --------------------------------------------------------------------------
# 解析指紋（月 10 で凍結）
# --------------------------------------------------------------------------


def fingerprint() -> dict:
    """`docs/fingerprint.json` の中身。

    sink 表、R1/R2 カタログ、ゲート述語カタログ、weak 理由語彙、cap と深さ、
    D パーサ規則と執行表の sha256 を入れる（§6 の凍結）。
    **凍結後の実行は指紋を evidence に書き、不一致は held-out 結果を無効にする。**
    """
    sink_blob = canonical_json(
        {
            "slots": {k: list(v) for k, v in sorted(SLOTS.items())},
            "sub_kinds": {k: list(v) for k, v in sorted(SUB_KINDS.items())},
            "direct": {
                k: [
                    {"kind": r.kind, "slots": sorted(r.slots), "exec_mode_kw": r.exec_mode_kw}
                    for r in rows
                ]
                for k, rows in sorted(DIRECT_SINKS.items())
            },
            "proxy": [
                {
                    "recv": sorted(r.recv_types),
                    "method": r.method,
                    "kind": r.kind,
                    "slots": sorted(r.slots),
                    "from_ctor": dict(sorted(r.from_ctor.items())),
                }
                for r in PROXY_SINKS
            ],
            "pipe": [{"method": r.method, "slots": sorted(r.slots)} for r in PIPE_SINKS],
        }
    )
    entry_blob = canonical_json(
        {
            "llm_calls": list(LLM_CALLS),
            "entry_rules": [
                {"kind": r.kind, "framework": r.framework, "names": list(r.names), "bases": list(r.bases)}
                for r in ENTRY_RULES
            ],
        }
    )
    gate_blob = canonical_json(
        {
            "validator_shapes": list(V.SHAPE_NAMES),
            "weak_reasons": list(V.WEAK_REASONS),
            "downgrades": list(V.DOWNGRADES),
            "config_atom_sources": list(V.CONFIG_ATOM_SOURCES),
            "gate_opaque": sorted(GATE_OPAQUE_REASONS),
            "gate_nodom": sorted(GATE_NODOM_REASONS),
            "val_opaque": sorted(VAL_OPAQUE_REASONS),
            "witness_templates": dict(sorted(V.WITNESS_TEMPLATES.items())),
        }
    )
    enf_blob = canonical_json(
        [{"path": r.path, "verdict": r.verdict, "evidence": r.evidence} for r in ENFORCEMENT_TABLE]
    )
    return {
        "schema": SCHEMA_VERSION,
        "caps": {
            "K": K,
            "SUMMARY_CAP": SUMMARY_CAP,
            "AST_NODE_CAP": AST_NODE_CAP,
            "EFFECT_ROW_CAP": EFFECT_ROW_CAP,
            "CFG_NODE_CAP": CFG_NODE_CAP,
            "WALL_CLOCK_CAP": WALL_CLOCK_CAP,
            "MAX_DEPTH": MAX_DEPTH,
        },
        "sha256": {
            "sink_table": _sha(sink_blob),
            "entry_catalog": _sha(entry_blob),
            "gate_vocabulary": _sha(gate_blob),
            "enforcement_table": _sha(enf_blob),
        },
        "counts": {
            "direct_sink_names": len(DIRECT_SINKS),
            "proxy_rows": len(PROXY_SINKS),
            "pipe_rows": len(PIPE_SINKS),
            "validator_shapes": len(V.SHAPE_NAMES),
            "weak_reasons": len(V.WEAK_REASONS),
        },
        "frozen_at": None,
        "git_commit": None,
    }


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------
# probe.json（F0a）
# --------------------------------------------------------------------------


def probe_json(res: RunResult, corpus_id: str, traced_ratio_null: bool = True) -> dict:
    """§5.1 が列挙する全キーを持つ probe.json。

    **`traced_ratio` は A5（F0a）の run では `null` とし、その run には二度と
    書き込まない。** traced 率は B1 完了後に**新しい `run_id` で probe を再実行**
    して得る。
    """
    tree = res.tree
    units = tree.units
    dangerous = [u for u in units if u.has_dangerous_effect]

    n_effects_by_kind: dict[str, int] = {}
    resolution = {"resolved": 0, "opaque": 0, "remote": 0}
    by_cause = {r: 0 for r in sorted(VAL_OPAQUE_REASONS)}
    shapes: dict[str, int] = {}
    db_only = 0
    db_only_non_db = 0

    for u in units:
        for e in u.effects:
            n_effects_by_kind[e.kind] = n_effects_by_kind.get(e.kind, 0) + 1
            resolution[e.resolution.kind] += 1
            for r in e.resolution.reasons:
                by_cause[r] = by_cause.get(r, 0) + 1
            if e.db_rule == "db":
                db_only += 1
        # **分子は `u.db_unresolved` から取る。** 以前は `e.db_rule == "db_unresolved"` の
        # 効果を数えていたが、**その効果は作られないので到達不能だった**（O28 / D49）。
        # DB の proxy 行の受け手型はすべて `DB_RECEIVER_TYPES` の部分集合なので、
        # `_from_proxy_row` に入る時点で受け手は DB 型に解決できている。
        db_only_non_db += len(u.db_unresolved)
        for s in u.validator_shapes:
            shapes[s] = shapes.get(s, 0) + 1
        if u.val is not None:
            for r in u.val.opaque_reasons:
                by_cause[r] = by_cause.get(r, 0) + 1

    rubric_units = [u for u in units if _is_rubric_1c(u)]
    enf_counts: dict[str, int] = {}
    for v in res.enforcement.values():
        key = f"{v.path}:{v.verdict}"
        enf_counts[key] = enf_counts.get(key, 0) + 1

    pin_counts = {"exact": 0, "lockfile": 0, "lower_bound_only": 0, "upper_bounded": 0, "unreadable": 0}
    for p in res.dep_pins.values():
        pin_counts[p.status] = pin_counts.get(p.status, 0) + 1

    return {
        "schema": SCHEMA_VERSION,
        "corpus_id": corpus_id,
        "population": tree.population,
        "n_units": len(units),
        "n_units_with_dangerous_effect": len(dangerous),
        "n_effects_by_kind": dict(sorted(n_effects_by_kind.items())),
        "resolution": resolution,
        "resolution_by_cause": dict(sorted(by_cause.items())),
        "rubric1c": {
            "n_units": len(rubric_units),
            "n_units_without_validator": sum(1 for u in rubric_units if not u.validator_shapes),
        },
        "registry_resolution_ratio": tree.trig_index.registry_resolution_ratio() if tree.trig_index else None,
        "n_units_with_validator": sum(1 for u in units if u.validator_shapes),
        "validator_shapes": dict(sorted(shapes.items())),
        "n_units_with_D_kind": sum(1 for u in units if not u.d_kind.is_bottom),
        "n_units_with_annotations_present": sum(
            1 for u in units if u.unit.annotations is not None
        ),
        "n_units_with_D_dom_covering": 0,
        "n_units_with_D_op": sum(
            1 for u in units if tree.d_op is not None and tree.d_op.covers(u.unit.tool_name)
        ),
        # **`r_prev` の分子**（D22）。0 の決め打ちだったので §10 の
        # 「方向そのものを疑うべき条件」の 3 つ目が原理的に測れなかった。
        "n_units_with_D_prev_join": sum(1 for u in units if u.d_prev_joined),
        "n_units_with_D_prev_join_dangerous": sum(1 for u in dangerous if u.d_prev_joined),
        "d_layer_unknown": {
            "enforcement": sum(1 for v in res.enforcement.values() if v.verdict == "D_unknown"),
            "pattern": 0,
            "annotation_form": sum(
                1 for u in units if u.unit.annotation_form in ("unreadable", "unpack")
            ),
        },
        "enforcement_path_counts": dict(sorted(enf_counts.items())),
        "dep_pin_resolvable": pin_counts,
        "effect_fp_audit": {"db_only": db_only, "db_only_non_db_execute": db_only_non_db},
        "traced_ratio": None if traced_ratio_null else (
            tree.trig_index.traced_ratio(
                [u.unit for u in units]
            ) if tree.trig_index else None
        ),
        "parse_failures": list(tree.parse_failures),
        "truncations": [
            {"relpath": r, "cap": c, "count": n} for r, c, n in tree.cap_hits
        ] + [{"unit_id": u, "cap": "wall_clock"} for u in res.wall_clock_truncations],
        "in_tree_resolution_ratio": tree.in_tree_resolution_ratio(),
        "opaque_ratio_primary_slots": tree.opaque_ratio(primary_only=True),
        "opaque_ratio_all_slots": tree.opaque_ratio(primary_only=False),
        "exposure_declarations": res.exposure_declarations,
        "annotations_join": {
            "tool_literals": tree.n_tool_literals,
            "joined": tree.n_annotation_joined,
            "unjoined": tree.n_annotation_unjoined,
        },
    }


def _is_rubric_1c(u) -> bool:
    from .verdict import load_rubric_1c

    return u.unit.tool_name in load_rubric_1c()


# --------------------------------------------------------------------------
# manifest.json
# --------------------------------------------------------------------------


def manifest_json(res: RunResult, run_id: str, volatile: bool = True) -> dict:
    """§5.2 の manifest。**volatile はトップレベルの `run_meta` に閉じ込める。**"""
    tree = res.tree
    out: dict[str, Any] = {
        "schema": SCHEMA_VERSION,
        "population": tree.population,
        "fingerprint": fingerprint(),
        "units": [_unit_manifest(u, res) for u in tree.units],
        "parse_failures": list(tree.parse_failures),
        "truncations": [{"relpath": r, "cap": c, "count": n} for r, c, n in tree.cap_hits],
        "gate_verdict_counts": gate_verdict_counts(tree),
        "d_op": tree.d_op.to_json() if tree.d_op else None,
        "dispatch_sites": [s.to_json() for s in (tree.trig_index.sites if tree.trig_index else [])],
    }
    if volatile:
        out["run_meta"] = {
            "run_id": run_id,
            "src_root": tree.src_root,
            "elapsed_s": round(res.elapsed_s, 3),
        }
    return out


def _unit_manifest(u, res: RunResult) -> dict:
    d = u.to_json()
    v = res.enforcement.get(u.unit.unit_id)
    if v is not None:
        d["enforcement"] = v.to_json()
    return d


def strip_volatile(manifest: dict) -> dict:
    """3 回一致の比較に使う形（volatile を落とす）。"""
    out = dict(manifest)
    out.pop("run_meta", None)
    return out


def determinism_signature(manifest: dict) -> str:
    return canonical_json(strip_volatile(manifest))


# --------------------------------------------------------------------------
# SARIF
# --------------------------------------------------------------------------


def sarif(res: RunResult) -> dict:
    """witness 付きの SARIF。**weak 理由ごとに witness テンプレートを出す。**"""
    results = []
    rules: dict[str, dict] = {}
    for u in res.tree.units:
        for row in u.rows:
            for verdict in sorted(row.verdicts):
                rule_id = verdict if not row.slot else f"{verdict}:{row.slot}"
                grade, weak_reason = (None, None)
                if row.slot is not None:
                    idx = _effect_index(u, row)
                    grade, weak_reason = u.grades.get((idx, row.slot), (None, None))
                witness = V.WITNESS_TEMPLATES.get(weak_reason or "", "")
                rules.setdefault(
                    rule_id,
                    {
                        "id": rule_id,
                        "shortDescription": {"text": verdict},
                        "fullDescription": {"text": f"{verdict} on slot {row.slot}"},
                    },
                )
                results.append(
                    {
                        "ruleId": rule_id,
                        "level": "warning" if verdict.startswith("GAP") else "note",
                        "message": {
                            "text": _message(u, row, verdict, grade, weak_reason, witness)
                        },
                        "locations": [
                            {
                                "physicalLocation": {
                                    "artifactLocation": {"uri": row.effect.relpath},
                                    "region": {"startLine": row.effect.lineno},
                                }
                            }
                        ],
                        "properties": {
                            "unit_id": row.unit_id,
                            "kind": row.effect.kind,
                            "form": row.effect.form,
                            "slot": row.slot,
                            "grade": grade,
                            "weak_reason": weak_reason,
                            "witness": witness,
                            "covered_by": row.covered_by,
                            "D_layer_present": list(row.d_layer_present),
                            "rule_w": row.rule_w,
                            "resolution": row.effect.resolution.kind,
                            "witness_chain": list(row.effect.witness_chain),
                        },
                    }
                )
    return {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "AuthGap",
                        "informationUri": "https://github.com/s1300105/auth_gap",
                        "rules": [rules[k] for k in sorted(rules)],
                    }
                },
                "results": results,
            }
        ],
    }


def _effect_index(u, row) -> int:
    for i, e in enumerate(u.effects):
        if e is row.effect:
            return i
    return -1


def _message(u, row, verdict: str, grade, weak_reason, witness: str) -> str:
    bits = [f"{verdict} {row.effect.kind}@{row.slot or '-'} via {row.effect.site} ({row.effect.form})"]
    if grade:
        bits.append(f"grade={grade}" + (f"({weak_reason})" if weak_reason else ""))
    if witness:
        bits.append(f"witness={witness}")
    if row.effect.witness_chain:
        bits.append("chain=" + " -> ".join(row.effect.witness_chain))
    return "; ".join(bits)


# --------------------------------------------------------------------------
# 書き出し
# --------------------------------------------------------------------------


def write_evidence(res: RunResult, out_dir: str, run_id: str, corpus_id: str) -> dict[str, str]:
    """`evidence/<run_id>/` に成果物を書く。**これ以外は evidence に数えない。**"""
    os.makedirs(out_dir, exist_ok=True)
    paths: dict[str, str] = {}
    for name, obj in (
        ("probe.json", probe_json(res, corpus_id)),
        ("manifest.json", manifest_json(res, run_id)),
        ("results.sarif", sarif(res)),
        ("fingerprint.json", fingerprint()),
    ):
        p = os.path.join(out_dir, name)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(canonical_json(obj))
        paths[name] = p
    return paths


def annotation_patch(res: RunResult) -> list[dict]:
    """CONTRADICTION 行の直列化のみ。**ポリシー emitter は作らない**（§5.2）。"""
    out: list[dict] = []
    for u in res.tree.units:
        for row in u.rows:
            if "CONTRADICTION" not in row.verdicts:
                continue
            out.append(
                {
                    "unit_id": row.unit_id,
                    "tool_name": u.unit.tool_name,
                    "relpath": row.effect.relpath,
                    "lineno": row.effect.lineno,
                    "declared": u.d_kind.to_json(),
                    "observed_kind": row.effect.kind,
                }
            )
    return out


def _optional(x: Optional[Any]) -> Any:
    return x
