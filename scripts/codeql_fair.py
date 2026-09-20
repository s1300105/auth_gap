#!/usr/bin/env python3
"""公平な CodeQL 比較（`docs/preregistration.md` §5 #4）: source を AuthGap の入口集合に揃える。

既定の `py/path-injection` は remote flow source（Flask / FastAPI 等）しか source に
しないので、MCP ツール引数もツール関数の引数も追わない（§5 #4 の第 4 類型）。
ここでは **AuthGap が入口と認識したユニットの仮引数**を source にしたクエリを生成し、
同じ木に当てる。**sink・sanitizer・伝播規則は CodeQL のまま**（変えると比較にならない）。

    # 1. 入口集合を書き出す（AuthGap の entries カタログの結果そのもの）
    .venv/bin/python scripts/codeql_fair.py dump corpus/A1__vuln:mcp_server corpus/A9__vuln:tool_package ... --out entries.json
    # 2. クエリを生成する（python-queries pack の中に置くと依存が解決する）
    .venv/bin/python scripts/codeql_fair.py gen entries.json --out <codeql>/qlpacks/codeql/python-queries/<ver>/Security/CWE-022/AuthGapPathInjection.ql
    # 3. codeql database create / analyze は手で回す（bundle の場所に依存する）
    # 4. SARIF を要約する
    .venv/bin/python scripts/codeql_fair.py summarize fair_A9__vuln.sarif ... --out evidence/codeql_fair/summary.json

生成したクエリと要約は `scripts/codeql/AuthGapPathInjection.ql` と
`evidence/codeql_fair/` に置く（2026-09-20 の実行分）。
"""

from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

QL_HEAD = '''/**
 * @name Path injection with AuthGap entry arguments as sources (fair comparison, prereg §5 #4)
 * @description Same as py/path-injection but the source set is the parameters of the tool
 *              entry functions that AuthGap recognises in this tree (docs/preregistration.md §5 #4).
 * @kind path-problem
 * @problem.severity error
 * @security-severity 7.5
 * @precision high
 * @id py/authgap-path-injection
 * @tags security
 */

import python
import semmle.python.dataflow.new.DataFlow
import semmle.python.security.dataflow.PathInjectionCustomizations
import semmle.python.security.dataflow.PathInjectionQuery
import PathInjectionFlow::PathGraph

'''

QL_TAIL = '''
/** A parameter of a function AuthGap treats as a tool entry. */
class AuthGapEntrySource extends PathInjection::Source {
  AuthGapEntrySource() {
    exists(Function f, Parameter p |
      authgapEntry(f.getLocation().getFile().getRelativePath(), f.getName()) and
      p = f.getAnArg() and
      this.(DataFlow::ParameterNode).getParameter() = p
    )
  }
}

from PathInjectionFlow::PathNode source, PathInjectionFlow::PathNode sink
where PathInjectionFlow::flowPath(source, sink)
select sink.getNode(), source, sink, "This path depends on a $@.", source.getNode(),
  "AuthGap entry argument"
'''


def cmd_dump(args) -> int:
    from authgap.runner import RunConfig, run

    out = {}
    for spec in args.trees:
        path, _, pop = spec.partition(":")
        res = run(RunConfig(src_root=path, population=pop or "mcp_server", full=False))
        rows = []
        for u in res.tree.units:
            rows.append({
                "relpath": u.unit.relpath,
                "qualname": u.unit.qualname,
                "entry_kind": u.unit.entry_kind,
                "params": [p.name for p in u.unit.params],
                "dangerous": u.has_dangerous_effect,
            })
        out[os.path.basename(path.rstrip("/"))] = rows
        print(f"{path}: {len(rows)} units ({sum(1 for r in rows if r['dangerous'])} dangerous)")
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    return 0


def cmd_gen(args) -> int:
    d = json.load(open(args.entries, encoding="utf-8"))
    pairs = sorted({(r["relpath"], (r["qualname"] or "").split(".")[-1]) for rows in d.values() for r in rows if r.get("relpath")})
    body = "private predicate authgapEntry(string relpath, string name) {\n" + "\n  or\n".join(
        f'  relpath = "{rel}" and name = "{name}"' for rel, name in pairs
    ) + "\n}\n"
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(QL_HEAD + body + QL_TAIL)
    print(f"{len(pairs)} entry functions -> {args.out}")
    return 0


def summarize_sarif(path: str) -> list[dict]:
    d = json.load(open(path, encoding="utf-8"))
    out = []
    for r in d["runs"][0].get("results", []):
        loc = r["locations"][0]["physicalLocation"]
        src = None
        try:
            cf = r["codeFlows"][0]["threadFlows"][0]["locations"][0]["location"]["physicalLocation"]
            src = f"{cf['artifactLocation']['uri']}:{cf['region']['startLine']}"
        except (KeyError, IndexError):
            pass
        out.append({"sink": f"{loc['artifactLocation']['uri']}:{loc['region']['startLine']}", "source": src,
                    "rule": r.get("ruleId")})
    return out


def cmd_summarize(args) -> int:
    out = {}
    for p in args.sarifs:
        name = os.path.splitext(os.path.basename(p))[0]
        rows = summarize_sarif(p)
        out[name] = {"n": len(rows), "findings": rows}
        print(f"{name}: {len(rows)}")
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("dump")
    p.add_argument("trees", nargs="+", help="<path>:<population>")
    p.add_argument("--out", required=True)
    p = sub.add_parser("gen")
    p.add_argument("entries")
    p.add_argument("--out", required=True)
    p = sub.add_parser("summarize")
    p.add_argument("sarifs", nargs="+")
    p.add_argument("--out", required=True)
    args = ap.parse_args()
    return {"dump": cmd_dump, "gen": cmd_gen, "summarize": cmd_summarize}[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())
