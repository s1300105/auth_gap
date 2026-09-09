#!/usr/bin/env python3
"""Semgrep OSS baseline との対ごと突き合わせ（§6 T1.5 の合格条件 (ii)）。

**同じ source 設定**の Semgrep CE ルール（`baselines/semgrep_authgap_source.yaml`）を
AuthGap と同じ対集合に当て、両側通過率を並べて出す。

§6 が要求する報告様式:

* **(a) source と sink が同一関数内にある行に限定した部分表**と
  **(b) 全行表**の 2 つに分ける。Semgrep CE は手続き内 taint のみなので、
  (b) で拾えない行は「機能境界による取りこぼし」であって実装の不備ではない。
* **同じ source 設定の Semgrep が同じ両側対を通過したら、貢献は「ルールファイル」
  であり静的解析の新規性は主張しない**（§1.5.4 の事前登録。v2 から変更なし）。

Semgrep が表せる「タプル」は `(ファイル, 規則, 囲み関数)` だけである。
等級・要求主体・実行モード・DISPATCH の解決状態は持たない。したがって
**Semgrep の「両側通過」は「所見の集合が変わったか」でしか定義できない。**
これは Semgrep の欠点ではなく、比較したい軸そのものである（§1.5.6 の軸 1）。

使い方::

    python scripts/baseline_semgrep.py --spec docs/corpus_spec.json \\
        --json evidence/w0/baseline_semgrep.json
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Optional

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

RULES = os.path.join(ROOT, "baselines", "semgrep_authgap_source.yaml")
SEMGREP = os.path.join(ROOT, ".venv", "bin", "semgrep")


@dataclass(frozen=True)
class Finding:
    relpath: str
    rule: str
    #: 所見を含む関数の qualname（行番号は修正でずれるので使わない）。
    func: str
    #: source と sink が同一関数内か（(a) の部分表に入るか）。
    intra: bool

    def key(self) -> tuple:
        return (self.relpath, self.rule, self.func)


def run_semgrep(root: str) -> tuple[list[Finding], list[str]]:
    """Semgrep を 1 本の木に当てる。**失敗は握り潰さず理由を返す。**"""
    if not os.path.exists(SEMGREP):
        return [], ["semgrep が入っていない（uv pip install semgrep）"]
    proc = subprocess.run(
        [SEMGREP, "--config", RULES, "--json", "--quiet", "--metrics=off", "."],
        cwd=root,
        capture_output=True,
        text=True,
    )
    if not proc.stdout.strip():
        return [], [f"semgrep が出力を返さなかった: {proc.stderr[:300]}"]
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return [], [f"semgrep の JSON を読めない: {proc.stdout[:200]}"]
    errors = [e.get("message", str(e))[:200] for e in data.get("errors", [])]
    out: list[Finding] = []
    for r in data.get("results", []):
        rel = r["path"]
        line = r["start"]["line"]
        func = _enclosing_function(os.path.join(root, rel), line)
        out.append(
            Finding(
                relpath=rel,
                rule=r["check_id"].split(".")[-1],
                func=func or f"<module>:{line}",
                # **Semgrep CE は手続き内 taint のみ**なので、報告された行は
                # 定義上すべて (a) の部分表に入る。(b) との差は「(b) で
                # 出るべきだったのに出なかった行」であり、AuthGap 側にしか無い。
                intra=True,
            )
        )
    return out, errors


def _enclosing_function(path: str, line: int) -> Optional[str]:
    try:
        with open(path, encoding="utf-8") as fh:
            tree = ast.parse(fh.read(), filename=path)
    except (OSError, SyntaxError, ValueError):
        return None
    best: Optional[str] = None
    best_line = -1
    stack: list[tuple[ast.AST, str]] = [(tree, "")]
    while stack:
        node, prefix = stack.pop()
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                qual = f"{prefix}{child.name}"
                start = child.lineno
                end = getattr(child, "end_lineno", start) or start
                if start <= line <= end and start > best_line and not isinstance(child, ast.ClassDef):
                    best, best_line = qual, start
                stack.append((child, f"{qual}."))
            else:
                stack.append((child, prefix))
    return best


@dataclass
class PairResult:
    pair_id: str
    vuln_only: list[str] = field(default_factory=list)
    fixed_only: list[str] = field(default_factory=list)
    both: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def two_sided(self) -> bool:
        """**所見の集合が変わったか。** Semgrep はこれ以上の座標を持たない。

        baseline に最も有利な読み方（増減どちらでも「変化」とみなす）。
        """
        return bool(self.vuln_only or self.fixed_only)

    @property
    def two_sided_by_disappearance(self) -> bool:
        """**脆弱側の所見が消えたか。** こちらが「修正を検出した」の意味である。

        修正でコードが増えて所見が**増えた**だけの対を「両側通過」に数えると、
        baseline が修正を検出したように見える。§6 T1.1 が verdict-clearing の
        併記を要求しているのと同じ理由で、増減を分けて報告する。
        """
        return bool(self.vuln_only)

    @property
    def cleared(self) -> bool:
        """脆弱側に出ていた所見が修正側で消え、新しい所見も出ていないか。"""
        return bool(self.vuln_only) and not self.fixed_only

    def to_json(self) -> dict:
        return {
            "pair_id": self.pair_id,
            "two_sided_pass_any_change": self.two_sided,
            "two_sided_pass_by_disappearance": self.two_sided_by_disappearance,
            "cleared": self.cleared,
            "n_vuln_only": len(self.vuln_only),
            "n_fixed_only": len(self.fixed_only),
            "n_both": len(self.both),
            "vuln_only": sorted(self.vuln_only),
            "fixed_only": sorted(self.fixed_only),
            "errors": self.errors,
        }


def compare(pair_id: str, vuln: str, fixed: str) -> PairResult:
    a, ea = run_semgrep(vuln)
    b, eb = run_semgrep(fixed)
    ka = {f.key() for f in a}
    kb = {f.key() for f in b}
    res = PairResult(pair_id, errors=ea + eb)
    fmt = lambda k: f"{k[0]}::{k[2]}::{k[1]}"  # noqa: E731
    res.vuln_only = [fmt(k) for k in ka - kb]
    res.fixed_only = [fmt(k) for k in kb - ka]
    res.both = [fmt(k) for k in ka & kb]
    return res


def load_pairs(spec_path: str) -> list[tuple[str, str, str]]:
    with open(spec_path, encoding="utf-8") as fh:
        targets = json.load(fh)["targets"]
    by_id: dict[str, dict[str, dict]] = {}
    for t in targets:
        if "@" not in t["name"]:
            continue
        pid, side = t["name"].split("@", 1)
        by_id.setdefault(pid, {})[side] = t
    out = []
    for pid in sorted(by_id):
        if {"vuln", "fixed"} <= set(by_id[pid]):
            out.append(
                (
                    pid,
                    os.path.join(ROOT, "corpus", f"{pid}__vuln"),
                    os.path.join(ROOT, "corpus", f"{pid}__fixed"),
                )
            )
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", default=os.path.join(ROOT, "docs", "corpus_spec.json"))
    ap.add_argument("--json")
    ap.add_argument("--authgap-json", default=os.path.join(ROOT, "evidence", "w0", "two_sided.json"))
    args = ap.parse_args()

    results: list[PairResult] = []
    for pid, v, f in load_pairs(args.spec):
        if not (os.path.isdir(v) and os.path.isdir(f)):
            print(f"SKIP {pid}: コーパスが無い", file=sys.stderr)
            continue
        r = compare(pid, v, f)
        results.append(r)
        print(
            f"{pid:6s} 変化あり={str(r.two_sided):5s} 消滅あり={str(r.two_sided_by_disappearance):5s} "
            f"解消={str(r.cleared):5s} "
            f"脆弱側のみ {len(r.vuln_only)} / 修正側のみ {len(r.fixed_only)} / 両側 {len(r.both)}"
        )
        for e in r.errors[:2]:
            print(f"       semgrep error: {e}")

    n_pass = sum(1 for r in results if r.two_sided)
    n_disappear = sum(1 for r in results if r.two_sided_by_disappearance)
    print(f"\nSemgrep OSS の両側通過: 変化あり {n_pass}/{len(results)} 対 / "
          f"**消滅あり {n_disappear}/{len(results)} 対**")
    if n_pass and not n_disappear:
        print("→ 変化はすべて「修正でコードが増えて所見が**増えた**」ものであり、")
        print("  修正を検出したのではない。**この区別を本文に書く。**")

    authgap = _load_authgap(args.authgap_json)
    if authgap:
        print("\n=== 対ごとの並べ表（§6 の報告様式）===")
        print(f"{'対':6s} {'AuthGap':>8s} {'Semgrep':>8s}  備考")
        for r in results:
            a = authgap.get(r.pair_id)
            sem = r.two_sided_by_disappearance
            note = ""
            if a and not sem:
                note = "AuthGap のみ通過"
                if r.two_sided:
                    note += "（Semgrep は所見が**増えた**だけ）"
            elif not a and sem:
                note = "**Semgrep のみ通過**（AuthGap の取りこぼし）"
            elif a and sem:
                note = "引き分け（**そう書く**。§1.5 の報告様式）"
            print(f"{r.pair_id:6s} {str(a):>8s} {str(sem):>8s}  {note}")
        both_pass = sum(
            1 for r in results if r.two_sided_by_disappearance and authgap.get(r.pair_id)
        )
        print(
            f"\n**同じ source 設定の Semgrep が通過した対: {n_pass} / うち AuthGap も通過: {both_pass}**"
        )
        print("§1.5.4 の事前登録: 同じ両側対を Semgrep が通過したら、貢献は")
        print("「ルールファイル」であり静的解析の新規性は主張しない。")

    if args.json:
        os.makedirs(os.path.dirname(args.json) or ".", exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(
                {
                    "rules": os.path.relpath(RULES, ROOT),
                    "note": "Semgrep CE は手続き内 taint のみ。(a) 部分表と (b) 全行表の差は"
                    "機能境界であって実装の不備ではない（§6 / §1.5.4）",
                    "n_pairs": len(results),
                    "n_two_sided_pass_any_change": n_pass,
                    "n_two_sided_pass_by_disappearance": n_disappear,
                    "pairs": [r.to_json() for r in results],
                },
                fh,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            fh.write("\n")
        print(f"\nwrote {args.json}")
    return 0


def _load_authgap(path: str) -> dict[str, bool]:
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    return {p["pair_id"]: p["two_sided_pass"] for p in data.get("pairs", [])}


if __name__ == "__main__":
    raise SystemExit(main())
