#!/usr/bin/env python3
"""実装変異試験（§2.5.6）。**生存 ≤ 2** が受け入れ条件。

支配判定の実装に 15 個の変異を入れ、`fixtures/gates/` と
`fixtures/dominance_mutants/` のテストで殺せるかを見る。1 件も落ちなければ
その変異は**生存**であり、テストがその性質を守っていないことを意味する。

比較対象として記録する前身の数字は「**56 テスト時代の実装変異 15 件中 9〜10 件が
生存**（監査 §1.5 stage2-guard-5）」。監査応答でテストは 99 件に増えたが監査自身が
変異試験を再実施していないため **HEAD での生存数は未知**である。

    python scripts/mutation_test.py
    python scripts/mutation_test.py --json evidence/w0/mutation_survival.json
"""

from __future__ import annotations

import argparse
import ast
import contextlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from authgap import cfgbuild, dominance, gate, srcindex  # noqa: E402
from authgap.gateharness import analyze_case  # noqa: E402

# --------------------------------------------------------------------------
# 変異
# --------------------------------------------------------------------------


@contextlib.contextmanager
def patched(obj, name, value):
    old = getattr(obj, name)
    setattr(obj, name, value)
    try:
        yield
    finally:
        setattr(obj, name, old)


def m_dominates_always_true():
    return patched(dominance.DomTree, "dominates", lambda self, a, b: True)


def m_dominates_always_false():
    return patched(dominance.DomTree, "dominates", lambda self, a, b: False)


def m_drop_g_ii():
    """(G-ii) を落とす: 支配していればゲートするとみなす。"""

    def gates(cfg, dom, g, d, raises_form=False):
        if g != d and dom.is_reachable(d) and dom.dominates(g, d):
            return dominance.GateCheck(True)
        return dominance.GateCheck(False, "no_gate")

    return _patch_gates(gates)


def m_no_cfg_removal():
    """`CFG∖{g}` の除去をやめる。"""
    orig = cfgbuild.CFG.reachable_from
    return patched(
        cfgbuild.CFG, "reachable_from", lambda self, start, blocked=frozenset(): orig(self, start, frozenset())
    )


def m_deny_all_successors():
    return patched(
        dominance, "deny_successors", lambda cfg, g, raises_form=False: set(cfg.successors(g))
    )


def m_deny_ignores_exc():
    def deny(cfg, g, raises_form=False):
        node = cfg.nodes[g]
        if node.kind != "test":
            return set()
        sense = dominance.test_sense(node.test_expr)
        return set(cfg.successors(g, ("false" if sense == "positive" else "true",)))

    return patched(dominance, "deny_successors", deny)


def m_sense_always_positive():
    return patched(dominance, "test_sense", lambda expr: "positive")


def m_no_subject_match():
    return patched(gate, "subject_ok", lambda cand, subjects: True)


def m_opaque_squashed_to_nodom():
    return patched(gate, "opaque_beats_no_gate", lambda: False)


def m_assume_approval():
    """**推定で A にする**（A-b のゲート要約を省き raise すると仮定する）。"""
    orig = gate.SummaryCache.get

    def get(self, fd, depth=0):
        s = orig(self, fd, depth)
        s.raises_on_deny = True
        return s

    return patched(gate.SummaryCache, "get", get)


def m_no_finally_copies():
    """`finally` を脱出種別ごとに複製せず、**1 ノードで表す**。

    仕様書が「唯一の例外」として複製を要求している当の性質を外す変異。
    """
    orig = cfgbuild.CFGBuilder._copy_finally

    def copy_finally(self, body, exit_kind, ctx):
        cache = getattr(self, "_shared_finally", None)
        if cache is None:
            cache = self._shared_finally = {}
        key = id(body)
        if key in cache:
            return cache[key]
        frag = orig(self, body, "normal", ctx)
        for nid in self.cfg.nodes:
            if self.cfg.nodes[nid].copy_kind is not None:
                self.cfg.nodes[nid].copy_kind = None
        cache[key] = frag
        return frag

    return patched(cfgbuild.CFGBuilder, "_copy_finally", copy_finally)


def m_no_exception_edges():
    return patched(cfgbuild.CFGBuilder, "_link_exc", lambda self, nid, ctx, node: None)


def m_no_cap_record():
    orig = cfgbuild.CFGBuilder._new

    def _new(self, *a, **kw):
        nid = orig(self, *a, **kw)
        self.cfg.opaque[:] = [r for r in self.cfg.opaque if r != "cfg_cap"]
        return nid

    return patched(cfgbuild.CFGBuilder, "_new", _new)


def m_no_parse_failure_record():
    orig = srcindex.SourceIndex.parse

    def parse(self, path):
        tree = orig(self, path)
        self.parse_failures.clear()
        return tree

    return patched(srcindex.SourceIndex, "parse", parse)


def m_not_desugaring_removed():
    """`not` の脱糖をやめ、`not X` を 1 つの葉として扱う。"""
    orig = cfgbuild._TestBuilder._emit

    def emit(self, e, t, f, pt, pf):
        if isinstance(e, ast.UnaryOp) and isinstance(e.op, ast.Not):
            return self._leaf(e, t, f, pt, pf)
        return orig(self, e, t, f, pt, pf)

    return patched(cfgbuild._TestBuilder, "_emit", emit)


def _patch_gates(fn):
    """`gates` は複数の module が `from ... import` で束縛しているので全部差す。"""

    @contextlib.contextmanager
    def cm():
        olds = []
        for mod in (dominance, gate, gateharness_gates_holder()):
            if hasattr(mod, "gates"):
                olds.append((mod, mod.gates))
                mod.gates = fn
        try:
            yield
        finally:
            for mod, old in olds:
                mod.gates = old

    return cm()


def gateharness_gates_holder():
    from authgap import gateharness

    return gateharness


MUTATIONS = [
    ("dominates_always_true", "支配規則の反転（常に支配とみなす）", m_dominates_always_true),
    ("dominates_always_false", "支配規則の反転（常に非支配とみなす）", m_dominates_always_false),
    ("drop_G_ii", "(G-ii) を落とし支配だけでゲートとみなす", m_drop_g_ii),
    ("no_cfg_removal", "`CFG∖{g}` の除去をやめる", m_no_cfg_removal),
    ("deny_all_successors", "拒否後継を全後継にする", m_deny_all_successors),
    ("deny_ignores_exc", "拒否後継から例外辺を落とす", m_deny_ignores_exc),
    ("sense_always_positive", "述語のセンスを常に肯定にする", m_sense_always_positive),
    ("no_subject_match", "主語一致を削除する", m_no_subject_match),
    ("opaque_squashed_to_nodom", "OPAQUE を NODOM に潰す", m_opaque_squashed_to_nodom),
    ("assume_approval", "推定で A にする（ゲート要約を省く）", m_assume_approval),
    ("no_finally_copies", "`finally` 複製を抑止する", m_no_finally_copies),
    ("no_exception_edges", "例外辺を削除する", m_no_exception_edges),
    ("no_cap_record", "cap の記録を削除する", m_no_cap_record),
    ("no_parse_failure_record", "parse 失敗の記録を削除する", m_no_parse_failure_record),
    ("not_desugaring_removed", "`not` の脱糖を削除する", m_not_desugaring_removed),
]


# --------------------------------------------------------------------------
# 実行
# --------------------------------------------------------------------------


def load(sub: str) -> dict:
    with open(os.path.join(ROOT, sub, "expected.json"), encoding="utf-8") as fh:
        return json.load(fh)["cases"]


def failing_cases() -> list[str]:
    """期待値と食い違うケースの一覧。空なら「全部通った」。"""
    bad: list[str] = []
    for sub in ("fixtures/gates", "fixtures/dominance_mutants"):
        directory = os.path.join(ROOT, sub)
        for case, spec in sorted(load(sub).items()):
            try:
                res = analyze_case(
                    directory,
                    case,
                    spec["file"],
                    spec.get("effect_line"),
                    spec.get("coordinate", "occ"),
                    frozenset(spec.get("not_entries", ())),
                )
            except Exception as exc:  # 変異で落ちるのも「殺した」に数える
                bad.append(f"{case}:raised {type(exc).__name__}")
                continue
            if spec.get("not_verdict"):
                if res.verdict == spec["not_verdict"]:
                    bad.append(f"{case}:verdict")
                for need in spec.get("requires_rows", []):
                    if need not in res.rows:
                        bad.append(f"{case}:row {need}")
                continue
            if res.verdict != spec["verdict"]:
                bad.append(f"{case}:verdict")
            elif res.reason != spec["reason"]:
                bad.append(f"{case}:reason")
            elif spec["witness_line"] is not None and res.witness_line != spec["witness_line"]:
                bad.append(f"{case}:witness")
            elif spec.get("grade") is not None and res.grade != spec["grade"]:
                bad.append(f"{case}:grade")
    return bad


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    args = ap.parse_args()

    base = failing_cases()
    if base:
        print("変異を入れる前から期待値と食い違っている。先にそれを直すこと:")
        for b in base:
            print("  ", b)
        return 2

    rows = []
    survived = []
    for name, desc, factory in MUTATIONS:
        with factory():
            killed_by = failing_cases()
        alive = not killed_by
        rows.append(
            {
                "mutation": name,
                "description": desc,
                "survived": alive,
                "killed_by": killed_by[:6],
                "n_killed_by": len(killed_by),
            }
        )
        if alive:
            survived.append(name)
        mark = "SURVIVED" if alive else f"killed ({len(killed_by)})"
        print(f"{name:26s} {mark:16s} {desc}")

    print(f"\n生存 {len(survived)}/{len(MUTATIONS)}（受け入れ条件: ≤ 2）")
    if survived:
        print("生存した変異:", ", ".join(survived))
    if args.json:
        os.makedirs(os.path.dirname(args.json), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(
                {
                    "acceptance": "生存 <= 2 (§2.5.6)",
                    "predecessor_reference": "56 テスト時代の実装変異 15 件中 9〜10 件が生存。HEAD での生存数は未知",
                    "n_mutations": len(MUTATIONS),
                    "n_survived": len(survived),
                    "survived": survived,
                    "rows": rows,
                },
                fh,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            fh.write("\n")
        print(f"wrote {args.json}")
    return 0 if len(survived) <= 2 else 1


if __name__ == "__main__":
    raise SystemExit(main())
