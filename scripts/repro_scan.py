"""小さな再現用の木を解析して、判定に効くものだけを 1 画面に出す（添削用。`docs/review_plan.md`）。

    .venv/bin/python scripts/repro_scan.py <木のディレクトリ> [--population mcp_server] [--json]

出すもの: ユニットごとに、宣言 D、効果行（kind / site / form / 行 / 解決 / 主体と出自と根）、
verdict 行と notes（`contradiction:D1` など）、解決できなかった木内呼び出しの数。
木全体の parse 失敗と上限到達も出す。**`--json` は manifest をそのまま出す。**

テストの `_units` ヘルパ（`tests/test_fix_d61.py`）と同じ経路（`runner.run` → `report.manifest_json`）を通るので、
ここで出た結果は full scan の結果と同じ規則で作られている。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from authgap.report import manifest_json  # noqa: E402
from authgap.runner import RunConfig, run  # noqa: E402


def _slot(v: dict) -> str:
    s = f"{v.get('prin')}/{v.get('prov')}"
    if v.get("prov_reasons"):
        s += "(" + ",".join(v["prov_reasons"]) + ")"
    sh = v.get("shape", {})
    s += f" {sh.get('k')}"
    if "const" in sh:
        s += f"={sh['const']!r}"
    if v.get("roots"):
        s += " roots=" + ",".join(v["roots"])
    return s


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("tree")
    ap.add_argument("--population", default="mcp_server", choices=["app", "mcp_server", "tool_package"])
    ap.add_argument("--json", action="store_true", help="manifest をそのまま出す")
    a = ap.parse_args()

    res = run(RunConfig(src_root=str(Path(a.tree).resolve()), population=a.population, full=True))
    m = manifest_json(res, "repro")
    if a.json:
        json.dump(m, sys.stdout, ensure_ascii=False, indent=1, sort_keys=True)
        return 0

    if m.get("parse_failures"):
        print("parse_failures:", m["parse_failures"])
    if m.get("truncations"):
        print("truncations:", m["truncations"])
    for u in m["units"]:
        unit = u["unit"]
        print(f"== {unit.get('qualname')}  ({unit.get('relpath')}:{unit.get('lineno')})  "
              f"entry={unit.get('entry_kind')}/{unit.get('framework')}  form={unit.get('annotation_form')}")
        print("   annotations:", json.dumps(unit.get("annotations"), ensure_ascii=False, sort_keys=True),
              " D_kind:", json.dumps(u.get("D_kind"), ensure_ascii=False, sort_keys=True))
        if u.get("unresolved_in_tree_calls"):
            print("   unresolved_in_tree_calls:", len(u["unresolved_in_tree_calls"]))
        for e in u.get("effects", []):
            extra = []
            for k in ("destructive", "fs_mode", "http_method", "sql_head", "sub_kind", "db_rule"):
                if k in e:
                    extra.append(f"{k}={e[k]}")
            if e.get("resolution_reasons"):
                extra.append("reasons=" + ",".join(e["resolution_reasons"]))
            if e.get("witness_chain"):
                extra.append("chain=" + ">".join(e["witness_chain"]))
            print(f"   E {e['kind']:<8} {e['site']:<28} {e['form']:<6} L{e['lineno']:<4} {e['relpath']:<20} "
                  f"{e['resolution']:<9} {' '.join(extra)}")
            for name, v in sorted(e.get("slots", {}).items()):
                print(f"       .{name:<8} {_slot(v)}")
        for r in u.get("rows", []):
            keep = {k: r[k] for k in r if k in ("verdict", "kind", "site", "notes", "grade", "rule", "reason", "decl")}
            print("   R", json.dumps(keep, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
