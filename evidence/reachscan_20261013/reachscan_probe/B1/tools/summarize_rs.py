"""reachscan JSON + --explain の要約（入口 / 注釈 / declared_tools / findings / mismatches / Not checked）。"""
import json, os, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
explain = sys.argv[2] if len(sys.argv) > 2 else None
root = d.get("target", "")
def rel(p):
    return os.path.relpath(p, root) if p and root and p.startswith(root) else p
def hints(a):
    if not a:
        return None
    return {k: (a[k]["value"], a[k]["source"]) for k in ("readOnlyHint", "destructiveHint", "idempotentHint", "openWorldHint")} | {
        "declared": a.get("declared"), "unresolved_reference": a.get("unresolved_reference")}
print("num_files_scanned:", d.get("num_files_scanned"), "entry_points_detected:", d.get("entry_points_detected"))
for ep in d.get("py_entry_points", []):
    print("EP", ep["name"], rel(ep["file"]) + ":" + str(ep["lineno"]), ep["framework"], ep["pattern_type"], ep["confidence"],
          "reachable_findings=", len(ep.get("reachable_findings", [])))
    if "annotations" in ep:
        print("   annotations:", json.dumps(hints(ep["annotations"])))
    for t in ep.get("declared_tools", []):
        print("   declared_tool:", t["name"], "line", t["lineno"], json.dumps(hints(t["annotations"])))
for e in d.get("findings", []):
    f = e["finding"]
    print("FINDING", f["capability"], repr(f["evidence"]), rel(f["file"]) + ":" + str(f["lineno"]), f["reachability"],
          "ep=", f.get("entry_point_name"), "path=", f.get("reachability_path"))
for m in d.get("annotation_mismatches", []):
    o = m["observed"]
    print("MISMATCH", m["tool"], m["rule"], m["risk_level"], m["declared"], "dispatch=", m["entry_point"]["dispatch"],
          "ep_line=", m["entry_point"]["lineno"], "observed=", o["capability"], repr(o["evidence"]), "line", o["lineno"],
          "path=", m["reachability_path"], "extra_obs=", [(x["capability"], x["lineno"]) for x in m.get("additional_observations", [])])
if explain:
    txt = open(explain, encoding="utf-8").read()
    i = txt.find("Not checked")
    if i >= 0:
        block = txt[i:].split("\n\n")[0]
        print("EXPLAIN:", block.replace(root + "/", ""))
    else:
        print("EXPLAIN: (no 'Not checked' block)")
