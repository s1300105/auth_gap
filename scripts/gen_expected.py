#!/usr/bin/env python3
"""付録 G と支配 mutant の期待値ファイルを生成する。

**期待値の出所は 2 つだけである。**

1. `(verdict, reason クラス, grade)` — 本スクリプト内の手書き表。出所は
   仕様書 §2.5 付録 G の表と §2.5.6 の受け入れ条件であり、**解析器の出力ではない。**
2. `witness 行` / `effect 行` — fixture 中の `# WITNESS` / `# EFFECT` マーカー。
   人が置いた位置であり、**解析器の出力ではない。**

したがって生成された `expected.json` は「実装を見て書いた期待値」ではない。
§2.5.6 が要求する「実装着手前にコミットして凍結する」を満たすために、
採点器 `authgap/gate.py` を書く前に生成してコミットすること。

再生成: `python scripts/gen_expected.py`
"""

from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --------------------------------------------------------------------------
# 手書きの期待表（出所: 仕様書 §2.5 付録 G）
#
# `verdict` / `reason` / `grade` は仕様書の表から写す。`predecessor` は
# 「前身の実測」列、`direction` は「誤りの向き」列。
# --------------------------------------------------------------------------

GATES = {
    "g01_exit_prefix": {
        "hole": "exit 前に 1 文（`_is_exit_body` の全 exit 要求）",
        "verdict": "DOM",
        "reason": None,
        "grade": "OP",
        "predecessor": 'NODOM（"non-exit body"）',
        "direction": "誤 FN",
    },
    "g02_or_failure_conjunction": {
        "hole": "`or` の失敗連言",
        "verdict": "DOM",
        "reason": None,
        "grade": "USER",
        "predecessor": 'NODOM（"`or` disjunct"）[f7aced6 では DOM]',
        "direction": "誤 FN（v2 で退行）",
    },
    "g03_await_bare_approval": {
        "hole": "`await` した承認割り込みの裸文",
        "verdict": "DOM",
        "reason": None,
        "grade": "USER",
        "predecessor": "NODOM（seen にすら出ない）",
        "direction": "誤 FN",
    },
    "g04_walrus_test": {
        "hole": "walrus を含む test",
        "verdict": "DOM",
        "reason": None,
        "grade": "USER",
        "predecessor": "NODOM [f7aced6 では DOM]",
        "direction": "誤 FN（v2 で退行）",
    },
    "g05_try_revalidate_reraise": {
        "hole": "try/except でパス検証が再送出",
        "verdict": "DOM",
        "reason": None,
        "grade": "OP",
        "value_grade": "strong-path",
        "predecessor": "NODOM",
        "direction": "誤 FN",
    },
    "g06_except_swallows_approval": {
        "hole": "承認の例外が except で握り潰される",
        "verdict": "NODOM",
        "reason": "deny_reaches_effect",
        "grade": None,
        "predecessor": "NODOM",
        "direction": "一致（回帰固定）",
    },
    "g07_comprehension_filter": {
        "hole": "内包表記の `if` フィルタ",
        "verdict": "DOM",
        "reason": None,
        "grade": "OP",
        "predecessor": "NODOM",
        "direction": "誤 FN",
    },
    "g08_context_manager_approval": {
        "hole": "CM 形の承認ゲート（`Gateway.require_approval`、木内解決可）",
        "verdict": "DOM",
        "reason": None,
        "grade": "USER",
        "predecessor": "NODOM",
        "direction": "誤 FN",
    },
    "g09_suppress_absorbs_approval": {
        "hole": "`contextlib.suppress` が承認を吸収",
        "verdict": "NODOM",
        "reason": "deny_reaches_effect",
        "grade": None,
        "predecessor": "NODOM",
        "direction": "一致（回帰固定）",
    },
    "g10_loop_continue_allowlist": {
        "hole": "ループ内 `continue` の allowlist",
        "verdict": "DOM",
        "reason": None,
        "grade": "OP",
        "atom": {"name": "ALLOWED_TOOLS", "source": "module_const", "default_closed": True},
        "predecessor": "DOM",
        "direction": "一致（回帰固定）",
    },
    "g11_non_binding_subject": {
        "hole": "主語不一致（`Gateway.is_allowed(self.default_tool)`）",
        "verdict": "NODOM",
        "reason": "non_binding_gate",
        "grade": None,
        "predecessor": "DOM",
        "direction": "誤 clear（不健全）",
    },
    "g12_effect_in_finally": {
        "hole": "効果が `finally` 側にある",
        "verdict": "NODOM",
        "reason": "deny_reaches_effect",
        "grade": None,
        "predecessor": "NODOM",
        "direction": "一致（回帰固定）",
        "reason_note": (
            "**仕様書の付録 G は G12 の reason を書いていない。** "
            "`deny_reaches_effect` は本 fixture の構造からの導出である: "
            "承認の拒否辺は finally(exc) 複製へ入り、その複製が効果そのものなので "
            "`d ∈ Reach(s)` が成り立つ。§2.5.6 が 3 つ組一致を要求する以上 reason を "
            "空のままには置けないのでここで固定した。**学生が追認すること。**"
        ),
    },
    "g13_dynamic_registry": {
        "hole": "木内で解決できないレジストリ（`Gateway.plugins.get(name)`）",
        "verdict": "OPAQUE",
        "reason": "dynamic_registry",
        "grade": None,
        "resolution": "opaque",
        "row": "UNKNOWN",
        "predecessor": "未実測（コード読解からの推定）。§9-13 で実測に置き換える",
        "direction": "誤 clean（不健全）と推定",
    },
    "g14_alt_entry": {
        "hole": "第 2 のユニット入口（無ガード）",
        "verdict": "NODOM",
        "reason": "alt_entry",
        "grade": None,
        "row": "GAP_SELECT",
        "entries": ["dispatch", "llm_loop"],
        "not_entries": ["run_shell"],
        "predecessor": "guarded=True（clear）",
        "direction": "誤 clear（不健全）",
    },
    "g15_req_occ_vs_req_val": {
        "hole": "最弱等級 / `req_occ` と `req_val` の分離",
        "verdict": "DOM",
        "reason": None,
        "grade": "OP",
        "req_occ": "OP",
        "req_val": {"slot": "argv[*]", "grade": "weak", "weak_reason": "no_dashdash"},
        "row": "GAP_INJECT",
        "rule": "規則 W（weak validator は宣言に優先）",
        "predecessor": "guarded=True（clear）",
        "direction": "誤 clear（不健全）",
    },
}

MUTANTS = {
    "m1_binding_only": {
        "hole": "`ok = confirm(name)` の束縛のみで無条件 dispatch",
        "not_verdict": "DOM",
        "note": "A-a / A-b / A-c のいずれも取れない。confirm は木内で解決でき拒否側が raise しない",
    },
    "m2_or_polarity": {
        "hole": "`if trusted or confirm(name):`（`or` の極性）",
        "not_verdict": "DOM",
        "note": "G2 と対。両方を正しく分けられることが前身 v2 との差",
    },
    "m3_reversed_polarity": {
        "hole": "`if not is_allowed(name): tool.run()`（極性逆）",
        "not_verdict": "DOM",
    },
    "m4_file_level_gate": {
        "hole": "無関係な関数の `human_in_the_loop=False`（file-level gate の誤検出）",
        "not_verdict": "DOM",
    },
    "m5_same_name_other_module": {
        "hole": "別モジュールの同名クラスにゲートがあり、当該ユニットの連結経路上には無い形",
        "not_verdict": "DOM",
        "note": "下向き走査が同名クラスに引きずられないことを試す",
    },
    "m6_parse_failure": {
        "hole": "parse 失敗ファイルの黙殺",
        "not_verdict": "DOM",
        "requires_rows": ["parse_failure"],
        "source": "m6_parse_failure.py.broken",
        "note": "期待値は「非支配」に加えて該当行が出力されること。行が出なければ不合格",
    },
    "m7_cfg_cap": {
        "hole": "node/深さ cap 到達での黙示 clear",
        "not_verdict": "DOM",
        "requires_rows": ["TRUNCATED", "OPAQUE(cfg_cap)"],
        "note": "期待値は「非支配」に加えて該当行が出力されること。行が出なければ不合格",
    },
    "m8_effect_on_false_branch": {
        "hole": "ガード偽側の分岐に dispatch がある形",
        "not_verdict": "DOM",
    },
}

MARKER = re.compile(r"#\s*(EFFECT|WITNESS)(\s|$)")


def markers(path: str) -> dict[str, list[int]]:
    """`# EFFECT` / `# WITNESS` マーカーの行番号を拾う。"""
    out: dict[str, list[int]] = {"EFFECT": [], "WITNESS": []}
    with open(path, encoding="utf-8") as fh:
        for i, line in enumerate(fh, 1):
            for m in re.finditer(r"#\s*(EFFECT|WITNESS)", line):
                out[m.group(1)].append(i)
    return out


def build(directory: str, table: dict, kind: str) -> dict:
    out: dict = {
        "_schema": "authgap/fixtures/expected/v1",
        "_kind": kind,
        "_provenance": (
            "verdict / reason / grade は仕様書 §2.5 付録 G と §2.5.6 から手で写した。"
            "effect_line / witness_line は fixture 中の # EFFECT / # WITNESS マーカー。"
            "**いずれも解析器の出力ではない。** 生成: scripts/gen_expected.py"
        ),
        "cases": {},
    }
    for name, spec in sorted(table.items()):
        src = spec.get("source", name + ".py")
        path = os.path.join(directory, src)
        if not os.path.exists(path):
            print(f"missing fixture: {path}", file=sys.stderr)
            sys.exit(1)
        mk = markers(path)
        case = dict(spec)
        case["file"] = src
        case["effect_line"] = mk["EFFECT"][0] if mk["EFFECT"] else None
        case["witness_line"] = mk["WITNESS"][0] if mk["WITNESS"] else None
        out["cases"][name] = case
    return out


def main() -> None:
    for sub, table, kind in (
        ("fixtures/gates", GATES, "appendix_g"),
        ("fixtures/dominance_mutants", MUTANTS, "dominance_mutants"),
    ):
        d = os.path.join(ROOT, sub)
        data = build(d, table, kind)
        dest = os.path.join(d, "expected.json")
        with open(dest, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2, sort_keys=True)
            fh.write("\n")
        print(f"wrote {dest} ({len(data['cases'])} cases)")


if __name__ == "__main__":
    main()
