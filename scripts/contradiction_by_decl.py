#!/usr/bin/env python3
"""CONTRADICTION を宣言ごとに数え、判定原理を 1 つずつ反対側にした感度分析を出す（D56）。

**判定の規則はここに無い**（`authgap/dparse.py: contradiction_findings`）。この script は
manifest の行の注記（`contradiction:<宣言>` / `contradiction_unknown:<宣言>:<理由>`）を読むだけ。

    .venv/bin/python scripts/contradiction_by_decl.py evidence/scan_v2_run13 --md docs/contradiction_by_decl.md

数え方（CLAUDE.md 規則 3）:

* 単位は `compare_scans.py` と同じ **(木, ユニットの relpath, ユニットの行, qualname, site, kind)**（D64 / U50。
  以前は位置が無く、別モジュールの同名ツールの矛が 1 件に潰れていた）。manifest の集合は `summary.json` の
  ok の木で決める（`scripts/runlib.py`）。宣言ごとに、その組の
  どれかの行に `contradiction:<宣言>` があれば「矛」、無くて `contradiction_unknown:<宣言>:…`
  があれば「不」（理由は組の中の理由の集合）。
* D1〜D4 は 4 つとも主指標で、宣言ごとに報告する（D62。以前は D3 / D4 を探索的としていた — D56 / §6）。
  **合算しない。**
* 感度分析: 理由のコードは §7 の判定表のどの分岐を通ったかを表すので、原理を反対側にしたときの
  結果は注記から正確に決まる（再走査は要らない）:
  - 1-i-a（永続する設定を含めない）: 理由 `db_persistent` を宣言内に
  - 1-ii-a（リモートの状態を含めない）: D1 / D2 の理由 `net_*` を宣言内に
  - 2-b（不明を矛盾に倒す）/ 2-c（宣言内に倒す）: 「不」をすべて矛 / 内に
  - 3-b（モデル由来の値を能力として読まない）: 理由に `model` を含む「矛」を「不」に
  - 4-b（破壊性の 2 つだけ）: D3 / D4 を数えない

モデルの値が制御位置に届く矛の層（D90。**層の判定はこの script の `load_model_control` の 1 か所だけ**。
`scan_v2.py`・`final_sample.py`・`final_aggregate.py` はここを呼ぶ）:

* S1（モデルの値が制御位置に流れ込む矛）= 宣言 d の矛の組のうち、主 slot（`authgap/catalog/sinks.py: PRIMARY_SLOTS`。
  ここでは import するだけで写さない）の値の主体が MODEL のもの（案 B）。GAP_INJECT の有無は列で、層の出入りに使わない。
* S2（モデルが制御位置を選べる矛）= S1 のうち、その主 slot の値が MODEL かつ確度 resolved（D57）。
  S1−S2（MODEL で opaque）は「不明」として別に数え、S2 にも層の外にも寄せない（CLAUDE.md 規則 4）。
* 組の行（`locations`）は、その組（site, kind）の行のうち `contradiction_reason:<d>:` の注記を持つ行
  （`final_sample.pair_locations` と同じ範囲）。行の効果は、同じ (relpath, 行, site, kind) の効果の全部。
* 軸: 行は「どれかの行が満たす」が主、1 つの行の効果は「全効果が満たす（保守的）」が主。ほかの 3 つの組み合わせも出す。
* D1〜D3 だけ（D4 には原理 3 を当てない）。宣言ごとに出し、合算しない（D62）。
"""

from __future__ import annotations

import argparse
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from runlib import load_manifest, print_warnings, run_manifests, unit_key  # noqa: E402

from authgap.catalog.sinks import PRIMARY_SLOTS  # noqa: E402  読むだけ（集合を写さない。D90）

DECLS = ("D1", "D2", "D3", "D4")


def load_reasons(run_dir: str) -> dict:
    """`{(木, relpath, 行, qualname, site, kind): {宣言: {(status, reason)}}}` を行の注記から作る。"""
    out: dict = collections.defaultdict(lambda: collections.defaultdict(set))
    manifests, warnings = run_manifests(run_dir)
    print_warnings(warnings, os.path.basename(run_dir.rstrip("/")))
    for t, path in manifests:
        for u in load_manifest(path)["units"]:
            uk = unit_key(t, u["unit"])
            for r in u.get("rows", []):
                key = (*uk, r["site"], r["kind"])
                for n in r.get("notes", []):
                    if n.startswith("contradiction_reason:"):
                        _, d, reason = n.split(":", 2)
                        out[key][d].add(("contradiction", reason))
                    elif n.startswith("contradiction_unknown:"):
                        _, d, reason = n.split(":", 2)
                        out[key][d].add(("unknown", reason))
    return out


# ---------------------------------------------------------------- モデルの値が制御位置に届く矛の層（D90）

#: 層を出す宣言（D90 の 3。D4 には出さない）。書く順も D1 が先。
LAYER_DECLS = ("D1", "D2", "D3")

#: 論文・集計での層の書き方（D90 の 10）。「確認なしで」は D1 だけ（D84 の ①。D2・D3 は確認を省くことを確かめていない）。
#: 攻撃に使えることを示した数とは書かない（D67 の 1、D84）。
LAYER_WORDING = {
    "D1": "確認なしで起きうる変更のうち、モデルの値が制御位置に届くもの",
    "D2": "宣言に反する変更のうち、モデルの値が制御位置に届くもの",
    "D3": "宣言に反する通信のうち、モデルの値が制御位置に届くもの",
}

#: 選択理由（D90 の 4）。矛の理由のうち、それ自体が slot の「選べる」（MODEL かつ resolved）を条件にしているもの。
#: **名前で固定する**（glob `*_model_*` は spawn_model・exec_model に当たらず、部分文字列 `model` は
#: net_method_model を拾う）。感度分析 3-b の集合 = この 7 つ ＋ `net_method_model`。
CHOICE_REASONS = frozenset({
    "spawn_model", "fs_writeout_model_path", "fs_unknown_model_path", "net_put_model_url", "exec_model",
    "net_model_host", "db_model_sql",
})

#: 組の層の値。優先は左から（S2 ⊂ S1。S1_opaque = S1−S2 =「不明」）。
#: G1_nonprimary = S1 に入らないが、組の行のどれかの slot に GAP_INJECT がある（参考の段。D90 の 5）。名前に反して
#: **主 slot の GAP_INJECT も入りうる**（効果の軸を保守的にしたので、同じ行の別の効果の主 slot が MODEL でなければ
#: S1 から外れる）。その数は `model_control_counts` の `outside_S1_gap_inject_primary` で別に出す。
MC_STATUSES = ("S2", "S1_opaque", "G1_nonprimary", "none")

#: 層の値 → 群（**群の対応はここ 1 か所**。final_aggregate.py はここを import する）。S1 = S2 ∪ S1−S2。
S1_STATUSES = ("S2", "S1_opaque")
OUTSIDE_STATUSES = ("G1_nonprimary", "none")
MC_GROUPS = {"S1": S1_STATUSES, "S2": ("S2",), "S1_minus_S2": ("S1_opaque",), "outside": OUTSIDE_STATUSES}

#: 判定との対応表の列（層の値を 1 つの列に写す）。「（層の記録なし）」は抜き取りの targets に記録が無い組。
MC_COLS = ("S2", "S1_opaque", "outside", "（層の記録なし）")


def mc_col(status: str | None) -> str:
    """層の値 → 対応表の列。None は「（層の記録なし）」。**語彙に無い値は例外**（黙ってどこかの列に入れない。規則 4）。"""
    if status is None:
        return "（層の記録なし）"
    if status not in MC_STATUSES:
        raise ValueError(f"層の値が語彙に無い: {status!r}（MC_STATUSES = {MC_STATUSES}。D90）")
    return status if status in S1_STATUSES else "outside"

#: 軸 (行, 効果)。最初が主（D90 の 3: 行は「どれか」、効果は保守的＝「全部」）。
AXES = (("any", "all"), ("any", "any"), ("all", "all"), ("all", "any"))
PRIMARY_AXIS = AXES[0]

#: ゲートの状態（D90 の 5。列として出すだけで層の出入りには使わない）。値は manifest の
#: `grades` / `req_val`（効果の番号:slot）と、行の `covered_by` / `rubric_1c` から読む（下の `gate_state`）。
GATE_STATES = ("なし", "weak", "strong・allowlist", "承認", "D_op", "rubric 1c", "不明")

#: final_sample.py が targets に残し、**final_sheet.py が判定表に写してはいけない**欄（D90 の 8）。
MODEL_CONTROL_FIELDS = frozenset({"model_control", "model_control_rows"})


def axis_name(axis: tuple[str, str]) -> str:
    return f"row_{axis[0]}/effect_{axis[1]}"


def effect_choice(effect: dict) -> str | None:
    """効果 1 つの主 slot の主体と確度: `chosen`（MODEL かつ resolved）/ `influenced`（MODEL で opaque）/ None。

    `authgap/dparse.py: _choice` と同じ分け方（複数の slot は chosen を優先）を、主 slot 全部に当てる。
    """
    out = None
    for name, v in sorted((effect.get("slots") or {}).items()):
        if name not in PRIMARY_SLOTS or not isinstance(v, dict) or v.get("prin") != "MODEL":
            continue
        if v.get("prov") == "resolved":
            return "chosen"
        out = "influenced"
    return out


def gate_state(unit: dict, i: int, slot: str, rows: list[dict]) -> str:
    """効果 i の slot のゲートの状態（`authgap/verdict.py: _inject_coordinate` の分岐の順に読む）。

    1. `req_val` が MODEL でなく、等級が weak でない → 引き上げられている（USER は承認の割り込み、OP は値の検証・allowlist）。
    2. 行に `rubric_1c` が `inventory(...)` → rubric 1c。3. 行が INVENTORY で `covered_by == "op"` → D_op。
    4. 等級 weak → weak（規則 W で GAP_INJECT は残る）。5. それ以外 → なし。
    manifest に `req_val` の記録が無ければ「不明」（黙って「なし」に倒さない。規則 4）。
    行には効果の番号が無いので、2・3 は同じ (relpath, 行, site, kind, slot) の行の和で読む。
    """
    k = f"{i}:{slot}"
    req_val = unit.get("req_val")
    if not isinstance(req_val, dict) or k not in req_val:
        return "不明"
    req = req_val[k]
    grade = ((unit.get("grades") or {}).get(k) or {}).get("grade")
    if req != "MODEL" and grade != "weak":
        return "承認" if req == "USER" else "strong・allowlist"
    if any(str(r.get("rubric_1c") or "").startswith("inventory") for r in rows):
        return "rubric 1c"
    if any(r.get("covered_by") == "op" and "INVENTORY" in (r.get("verdicts") or []) for r in rows):
        return "D_op"
    if grade == "weak":
        return "weak"
    return "なし"


def _resolution(effects: list[dict]) -> str | None:
    rs = {e.get("resolution") for e in effects}
    if not effects:
        return None
    if rs == {"resolved"}:
        return "resolved"
    if rs == {"opaque"}:
        return "opaque"
    return "mixed" if rs <= {"resolved", "opaque"} else "不明"


def location_facts(unit: dict, relpath, lineno, site: str, kind: str, rows: list[dict],
                   effects: list[tuple[int, dict]], reasons: set[str]) -> dict:
    """組の 1 行（relpath, 行）の事実。`rows` はその (relpath, 行, site, kind) の manifest の行（slot ごと）、
    `effects` は同じ鍵の (効果の番号, 効果)、`reasons` はその行に付いた宣言 d の理由。"""
    choices = [effect_choice(e) for _, e in effects]
    n = len(effects)
    inject = sorted({r.get("slot") for r in rows if "GAP_INJECT" in (r.get("verdicts") or [])} - {None})
    gates = set()
    model_slots, resolved_slots = set(), set()
    for i, e in effects:
        for name, v in (e.get("slots") or {}).items():
            if name in PRIMARY_SLOTS and isinstance(v, dict) and v.get("prin") == "MODEL":
                model_slots.add(name)
                if v.get("prov") == "resolved":
                    resolved_slots.add(name)
                gates.add(gate_state(unit, i, name, [r for r in rows if r.get("slot") == name]))
    s1 = [c in ("chosen", "influenced") for c in choices]
    s2 = [c == "chosen" for c in choices]
    return {
        "relpath": relpath, "lineno": lineno, "site": site, "kind": kind, "n_effects": n,
        "s1_all": bool(n) and all(s1), "s1_any": any(s1), "s2_all": bool(n) and all(s2), "s2_any": any(s2),
        "model_choice": "chosen" if (n and all(s2)) else ("influenced" if (n and all(s1)) else "none"),
        "model_choice_by_effect": [c or "none" for c in choices],
        "model_primary_slots": sorted(model_slots), "resolved_model_primary_slots": sorted(resolved_slots),
        "inject_slots": inject, "inject_primary_slots": sorted(set(inject) & PRIMARY_SLOTS),
        "gate_states": sorted(gates, key=GATE_STATES.index),
        "effect_resolution": _resolution([e for _, e in effects]),
        "reasons": sorted(reasons), "choice_reason": bool(set(reasons) & CHOICE_REASONS),
    }


def pair_status(locs: list[dict], axis: tuple[str, str]) -> tuple[str, list[dict], list[dict]]:
    """組の層の値と、その軸で S1 / S2 を満たす行。行の軸 `any`（どれか）/ `all`（全部）、効果の軸 `all` / `any`。"""
    row_mode, eff_mode = axis
    l1 = [x for x in locs if x[f"s1_{eff_mode}"]]
    l2 = [x for x in locs if x[f"s2_{eff_mode}"]]
    if row_mode == "any":
        in1, in2 = bool(l1), bool(l2)
    else:
        in1, in2 = bool(locs) and len(l1) == len(locs), bool(locs) and len(l2) == len(locs)
    if in2:
        return "S2", l1, l2
    if in1:
        return "S1_opaque", l1, []
    if any(x["inject_slots"] for x in locs):
        return "G1_nonprimary", [], []
    return "none", [], []


def _loc_str(x: dict) -> str:
    return f"{x['relpath']}:{x['lineno']}"


def pair_model_control(locs: list[dict]) -> dict:
    """組 1 つの層の記録（主の軸の値・ほかの軸の値・満たす行・列）。"""
    status, l1, l2 = pair_status(locs, PRIMARY_AXIS)
    basis = l2 or l1 or locs  # 列（ゲート・GAP_INJECT・効果の確度・選択理由）を読む行
    res = {x["effect_resolution"] for x in basis} - {None}
    return {
        "status": status,
        "axes": {axis_name(a): pair_status(locs, a)[0] for a in AXES},
        "rows_S1": [_loc_str(x) for x in l1], "rows_S2": [_loc_str(x) for x in l2],
        "gap_inject_primary": any(x["inject_primary_slots"] for x in basis),
        "gap_inject_any": any(x["inject_slots"] for x in locs),
        "gate_states": sorted({g for x in basis for g in x["gate_states"]}, key=GATE_STATES.index),
        "effect_resolution": (res.pop() if len(res) == 1 else ("mixed" if res else None)),
        "choice_reason": any(x["choice_reason"] for x in basis),
        "reasons": sorted({r for x in locs for r in x["reasons"]}),
        "n_rows": len(locs), "n_rows_without_effects": sum(1 for x in locs if not x["n_effects"]),
        "locations": locs,
    }


def load_model_control(run_dir: str, include_unknown: bool = False) -> dict:
    """`{(木, relpath, 行, qualname, site, kind, 宣言): 組の層の記録}`（D90。**層の判定はここだけ**）。

    組は `load_reasons` + `apply_flip(…, None)` で矛（`include_unknown` なら不も）の組。宣言は `LAYER_DECLS`。
    記録の `status` は主の軸（行 = どれか、効果 = 全部）の `S2` / `S1_opaque` / `G1_nonprimary` / `none`。
    `contradiction` は「矛」か「不」。不の組の行は `contradiction_unknown:<d>:` の注記を持つ行。
    """
    reasons = load_reasons(run_dir)
    want: dict[str, dict[tuple, dict[tuple, str]]] = collections.defaultdict(lambda: collections.defaultdict(dict))
    for key, per in reasons.items():
        for d in LAYER_DECLS:
            s = apply_flip(per.get(d, set()), d, None)
            if s == "矛" or (include_unknown and s == "不"):
                want[key[0]][key[:4]][(key[4], key[5], d)] = s
    out: dict[tuple, dict] = {}
    manifests, _warnings = run_manifests(run_dir)  # 警告は load_reasons が出した
    for tree, path in manifests:
        if tree not in want:
            continue
        for u in load_manifest(path)["units"]:
            uk = unit_key(tree, u["unit"])
            if uk not in want[tree]:
                continue
            eff_by: dict[tuple, list] = collections.defaultdict(list)
            for i, e in enumerate(u.get("effects") or []):
                eff_by[(e.get("relpath"), e.get("lineno"), e.get("site"), e.get("kind"))].append((i, e))
            rows_by: dict[tuple, list] = collections.defaultdict(list)
            for r in u.get("rows", []):
                rows_by[(r.get("relpath"), r.get("lineno"), r.get("site"), r.get("kind"))].append(r)
            for (site, kind, d), s in want[tree][uk].items():
                prefix = f"contradiction_reason:{d}:" if s == "矛" else f"contradiction_unknown:{d}:"
                locs = []
                for (rp, ln, st, kd), rows in rows_by.items():
                    if st != site or kd != kind:
                        continue
                    rs = {str(n)[len(prefix):] for r in rows for n in r.get("notes", []) if str(n).startswith(prefix)}
                    if rs:
                        locs.append(location_facts(u, rp, ln, site, kind, rows, eff_by.get((rp, ln, st, kd), []), rs))
                locs.sort(key=lambda x: (str(x["relpath"] or ""), x["lineno"] if isinstance(x["lineno"], int) else -1))
                out[(*uk, site, kind, d)] = {"contradiction": s, **pair_model_control(locs)}
    return out


def _count(items: list[tuple[tuple, list[str]]]) -> dict:
    """[(組の鍵, 行の一覧)] → 組・物理的な位置 (木, relpath, 行, site)・木の数。"""
    locs = set()
    for p, rows in items:
        for x in rows:
            rp, _, ln = x.rpartition(":")
            locs.add((p[0], rp, ln, p[4]))
    return {"pairs": len(items), "locations": len(locs), "trees": len({p[0] for p, _ in items})}


def model_control_counts(mc: dict, decl: str, axis: tuple[str, str] = PRIMARY_AXIS) -> dict:
    """宣言 1 つの層の全数（矛の組だけ）。S1・S2・S1−S2 の組・物理的な位置・木、S2 の選択理由の別、列の内訳。"""
    s1, s2, s1o, g1, none = [], [], [], [], []
    choice, other = [], []
    gates: collections.Counter = collections.Counter()
    resol: collections.Counter = collections.Counter()
    inj, inj_out = [], []
    for p, v in sorted(mc.items(), key=lambda kv: tuple(str(x) for x in kv[0])):
        if p[6] != decl or v["contradiction"] != "矛":
            continue
        st, l1, l2 = pair_status(v["locations"], axis)
        r1, r2 = [_loc_str(x) for x in l1], [_loc_str(x) for x in l2]
        if st not in S1_STATUSES and any(x["inject_primary_slots"] for x in v["locations"]):
            inj_out.append((p, [_loc_str(x) for x in v["locations"] if x["inject_primary_slots"]]))
        if st in S1_STATUSES:
            s1.append((p, r1))
            basis = l2 or l1
            for g in {g for x in basis for g in x["gate_states"]} or {"（記録なし）"}:
                gates[g] += 1
            rs = {x["effect_resolution"] for x in basis} - {None}
            resol[rs.pop() if len(rs) == 1 else ("mixed" if rs else "（効果なし）")] += 1
            if any(x["inject_primary_slots"] for x in basis):
                inj.append((p, r1))
        if st == "S2":
            s2.append((p, r2))
            (choice if any(x["choice_reason"] for x in l2) else other).append((p, r2))
        elif st == "S1_opaque":
            s1o.append((p, r1))
        elif st == "G1_nonprimary":
            g1.append((p, [_loc_str(x) for x in v["locations"]]))
        else:
            none.append((p, [_loc_str(x) for x in v["locations"]]))
    return {"axis": axis_name(axis), "S1": _count(s1), "S2": _count(s2), "S1_minus_S2": _count(s1o),
            "S2_choice_reason": _count(choice), "S2_other_reason": _count(other),
            "S1_gap_inject_primary": _count(inj), "outside_S1_gap_inject_primary": _count(inj_out),
            "G1_nonprimary": _count(g1), "outside": _count(none),
            "S1_by_gate_state": dict(sorted(gates.items(), key=lambda kv: (GATE_STATES + ("（記録なし）",)).index(kv[0]))),
            "S1_by_effect_resolution": dict(sorted(resol.items())),
            "trees_S1": sorted({p[0] for p, _ in s1}), "trees_S2": sorted({p[0] for p, _ in s2})}


def unknown_model_reasons(mc: dict, decl: str) -> dict:
    """不の組で主 slot に MODEL があるもの（主の軸の S1）を理由ごとに（D90 の 7。分子に入れない併記）。

    理由は**主の軸で S1 を満たす行**の理由だけを数える（矛の側の列が S1 を満たす行から読むのと揃える）。
    組の全部の行の理由を数えると、主体が MODEL でない行の理由が混ざる。1 組に複数の理由がありうる。
    """
    c: collections.Counter = collections.Counter()
    n = 0
    for p, v in mc.items():
        if p[6] != decl or v["contradiction"] != "不":
            continue
        st, l1, _ = pair_status(v["locations"], PRIMARY_AXIS)
        if st not in S1_STATUSES:
            continue
        n += 1
        for r in sorted({r for x in l1 for r in x["reasons"]}):
            c[r] += 1
    return {"pairs": n, "by_reason": dict(sorted(c.items()))}


def fixed_wording(cnt: dict) -> str:
    """S2 が少ないときも多いときも同じ文（D90 の 10。結果を見て書き方を選ばない）。

    文は D90 で固定した字面のまま（「件」は組の数）。木の数は文に足さず、層の表の「木」の欄で出す。
    """
    return f"解析器で選べると言えたものが {cnt['S2']['pairs']} 件、不明が {cnt['S1_minus_S2']['pairs']} 件"


def apply_flip(findings: set, decl: str, flip: str | None) -> str:
    """原理を 1 つ反対側にしたときの、宣言 1 つ分の結果（矛 / 不 / 内）。"""
    res = set()
    for status, reason in findings:
        s = "矛" if status == "contradiction" else "不"
        if flip == "1-i-a" and reason == "db_persistent":
            continue
        if flip == "1-ii-a" and decl in ("D1", "D2") and reason.startswith("net_"):
            continue
        if flip == "3-b" and s == "矛" and "model" in reason:
            s = "不"
        if flip == "2-b" and s == "不":
            s = "矛"
        if flip == "2-c" and s == "不":
            continue
        res.add(s)
    if flip == "4-b" and decl in ("D3", "D4"):
        return "内"
    return "矛" if "矛" in res else ("不" if "不" in res else "内")


FLIPS = [(None, "採った原理（1-i b / 1-ii b / 2 a / 3 a / 4 a）"),
         ("1-i-a", "1-i を a に（永続する設定を含めない）"),
         ("1-ii-a", "1-ii を a に（リモートの状態を含めない）"),
         ("2-b", "2 を b に（不明を矛盾に倒す）"),
         ("2-c", "2 を c に（不明を宣言内に倒す）"),
         ("3-b", "3 を b に（モデル由来の値を能力として読まない）"),
         ("4-b", "4 を b に（破壊性の 2 つだけ）")]


def to_md(run_dir: str) -> str:
    rs = load_reasons(run_dir)
    o = ["# CONTRADICTION の宣言ごとの件数と、判定原理の感度分析（D56）", "",
         f"再現: `python scripts/contradiction_by_decl.py {os.path.relpath(run_dir)}`", "",
         "単位は (木, ユニットの relpath:行, qualname, site, kind)（D64 / U50）。**D1〜D4 は 4 つとも主指標（D62）。"
         "宣言ごとに読み、合算しない。**「D1+D2 矛」の列は過去の run と比べるためだけに残す（主指標ではない）。", ""]
    o += ["## 採った原理での件数", "", "| 宣言 | 矛 | 不 | 矛の木 |", "|---|---|---|---|"]
    for d in DECLS:
        c = collections.Counter()
        trees = set()
        for key, per in rs.items():
            s = apply_flip(per.get(d, set()), d, None)
            c[s] += 1
            if s == "矛":
                trees.add(key[0])
        o.append(f"| {d} | {c['矛']} | {c['不']} | {len(trees)} |")
    o += ["", "## 理由ごとの内訳（採った原理）", "", "| 宣言 | 結果 | 理由 | 組 |", "|---|---|---|---|"]
    rc = collections.Counter()
    for per in rs.values():
        for d, fs in per.items():
            for status, reason in fs:
                rc[(d, "矛" if status == "contradiction" else "不", reason)] += 1
    for (d, s, r), n in sorted(rc.items()):
        o.append(f"| {d} | {s} | `{r}` | {n} |")
    o += ["", "## 感度分析（原理を 1 つずつ反対側にする）", "",
          "| 変えた原理 | D1 矛 | D1 不 | D2 矛 | D2 不 | D1+D2 矛（比較用） | D3 矛 | D3 不 | D4 矛 | D4 不 |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for flip, label in FLIPS:
        cnt = {d: collections.Counter() for d in DECLS}
        main = set()
        for key, per in rs.items():
            for d in DECLS:
                s = apply_flip(per.get(d, set()), d, flip)
                cnt[d][s] += 1
                if s == "矛" and d in ("D1", "D2"):
                    main.add(key)
        o.append(f"| {label} | {cnt['D1']['矛']} | {cnt['D1']['不']} | {cnt['D2']['矛']} | {cnt['D2']['不']} | "
                 f"{len(main)} | {cnt['D3']['矛']} | {cnt['D3']['不']} | {cnt['D4']['矛']} | {cnt['D4']['不']} |")
    o.append("")
    o += model_control_md(load_model_control(run_dir, include_unknown=True))
    return "\n".join(o)


def model_control_md(mc: dict) -> list[str]:
    """層（D90）の表。宣言ごと（D1 が先）、合算しない。"""
    o = ["## モデルの値が制御位置に届く矛の層（D90。解析器の出力。主指標ではない）", "",
         "S1 = 矛の組のうち主 slot（PRIMARY_SLOTS）の値の主体が MODEL（案 B）、S2 = そのうち MODEL かつ resolved（D57）、"
         "S1−S2 = MODEL で opaque（**不明**。S2 にも層の外にも寄せない）。主の軸は 行 = どれかの行、効果 = 全効果（保守的）。"
         "位置は (木, relpath, 行, site)。GAP_INJECT は列で、層の出入りに使わない。D4 は出さない。精度で補正しない全数。", "",
         "| 宣言 | 層 | 組 | 物理的な位置 | 木 |", "|---|---|---|---|---|"]
    counts = {d: model_control_counts(mc, d) for d in LAYER_DECLS}
    labels = [("S1", "S1 流れ込む"), ("S2", "S2 選べる"), ("S1_minus_S2", "S1−S2 不明"),
              ("S2_choice_reason", "S2 のうち理由が選択理由"), ("S2_other_reason", "S2 のうち理由が選択理由でない"),
              ("S1_gap_inject_primary", "参考: S1 ∩ 案 A（S1 を満たす行の主 slot に GAP_INJECT）"),
              ("outside_S1_gap_inject_primary", "参考: S1 の外で主 slot に GAP_INJECT（案 A のうち S1 に入らない。効果の軸で外れたものなど）"),
              ("G1_nonprimary", "層の外: S1 に入らないが、どれかの slot に GAP_INJECT（主 slot のものを含みうる）"),
              ("outside", "層の外: それ以外")]
    for d in LAYER_DECLS:
        for k, lab in labels:
            c = counts[d][k]
            o.append(f"| {d} | {lab} | {c['pairs']} | {c['locations']} | {c['trees']} |")
    o += ["", "決めておいた書き方（D90 の 10。「件」は組の数。木の数は上の表）:", ""]
    o += [f"- {d}: {fixed_wording(counts[d])}" for d in LAYER_DECLS]
    o += ["", "### 軸ごと（主でない組み合わせも出す）", "",
          "| 宣言 | 軸 (行 / 効果) | S1 組 | S1 木 | S2 組 | S2 木 | S1−S2 組 | S1−S2 木 |", "|---|---|---|---|---|---|---|---|"]
    for d in LAYER_DECLS:
        for a in AXES:
            c = model_control_counts(mc, d, a)
            o.append(f"| {d} | {a[0]} / {a[1]}{'（主）' if a == PRIMARY_AXIS else ''} | {c['S1']['pairs']} | {c['S1']['trees']} | "
                     f"{c['S2']['pairs']} | {c['S2']['trees']} | {c['S1_minus_S2']['pairs']} | {c['S1_minus_S2']['trees']} |")
    o += ["", "### S1 の列（主の軸。ゲートの状態は 1 組に複数ありうる）", "",
          "| 宣言 | ゲートの状態 | 効果の確度（resolution） |", "|---|---|---|"]
    for d in LAYER_DECLS:
        c = counts[d]
        o.append(f"| {d} | " + (", ".join(f"{k} {v}" for k, v in c["S1_by_gate_state"].items()) or "—") + " | "
                 + (", ".join(f"{k} {v}" for k, v in c["S1_by_effect_resolution"].items()) or "—") + " |")
    o += ["", "### 併記: 不の組で主 slot に MODEL があるもの（分子に入れない。主の軸で S1 を満たす行の理由ごと、"
          "1 組に複数の理由がありうる）", "",
          "| 宣言 | 組 | 理由 |", "|---|---|---|"]
    for d in LAYER_DECLS:
        u = unknown_model_reasons(mc, d)
        o.append(f"| {d} | {u['pairs']} | " + (", ".join(f"`{k}` {v}" for k, v in u["by_reason"].items()) or "—") + " |")
    o.append("")
    return o


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run")
    ap.add_argument("--md")
    args = ap.parse_args(argv)
    md = to_md(args.run)
    if args.md:
        with open(args.md, "w", encoding="utf-8") as fh:
            fh.write(md + "\n")
    print(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
