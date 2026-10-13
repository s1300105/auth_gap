"""destructive_sinks: expected.json と両道具の結果をツールごとに並べる。"""
import json, sys
exp = json.load(open(sys.argv[1], encoding="utf-8"))["tools"]
rs = json.load(open(sys.argv[2], encoding="utf-8"))
ag = json.load(open(sys.argv[3], encoding="utf-8"))
rs_mm = {}
for m in rs["annotation_mismatches"]:
    rs_mm.setdefault(m["tool"], []).append([m["rule"], m["risk_level"], m["observed"]["evidence"], m["observed"]["lineno"]])
rs_find = {}
for f in rs["findings"]:
    x = f["finding"]
    rs_find.setdefault(x.get("entry_point_name"), []).append([x["capability"], x["evidence"], x["lineno"]])
out = {}
for u in ag["units"]:
    t = u["unit"]["tool_name"]
    if t not in exp:
        continue
    site = exp[t]["site"]
    rows = [r for r in u["rows"] if r["site"] == site and r["kind"] == "FS_WRITE"]
    out[t] = {
        "expected_contradiction": exp[t]["contradiction"],
        "authgap_contradiction": any("CONTRADICTION" in r["verdicts"] for r in rows),
        "authgap_notes": sorted({n for r in rows for n in (r.get("notes") or []) if n.startswith("contradiction")}),
        "reachscan_mismatch": bool(rs_mm.get(t)),
        "reachscan_mismatches": rs_mm.get(t, []),
        "reachscan_findings_for_tool": rs_find.get(t, []),
    }
json.dump(out, sys.stdout, ensure_ascii=False, indent=1, sort_keys=True)
print()
