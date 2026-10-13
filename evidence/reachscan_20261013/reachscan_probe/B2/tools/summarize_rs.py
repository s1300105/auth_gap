"""reachscan JSON の要約（entry point と注釈 / finding / mismatch）。"""
import json, os, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
root = d.get("target", "")
def rel(p):
    try:
        return os.path.relpath(p, root) if p and root else p
    except ValueError:
        return p
def hints(a):
    if not a:
        return "-"
    return " ".join(f"{k}={v['value']}({v['source'][0]})" for k, v in a.items() if isinstance(v, dict))
print("version:", d.get("reachscan_version"), "files:", d.get("num_files_scanned"), "eps:", d.get("entry_points_detected"))
for ep in d.get("py_entry_points", []):
    print("EP", ep["name"], rel(ep["file"]) + ":" + str(ep["lineno"]), ep.get("framework"), ep.get("pattern_type"),
          "ann:", hints(ep.get("annotations")), "declared_tools:", [t["name"] for t in ep.get("declared_tools", [])])
for it in d.get("findings", []):
    f = it["finding"]
    print("FINDING", it["detector"], f["capability"], repr(f["evidence"]), rel(f["file"]) + ":" + str(f["lineno"]),
          f.get("risk_level"), "reach=" + str(f.get("reachability")), "ep=" + str(f.get("entry_point_name")),
          "path=" + str(f.get("reachability_path")), ("SUPPRESSED " + json.dumps(f["suppression"])) if f.get("suppression") else "")
for m in d.get("annotation_mismatches", []):
    o = m["observed"]
    print("MISMATCH", m["tool"], m["rule"], m["risk_level"], m["declared"], o["capability"], repr(o["evidence"]),
          rel(o["file"]) + ":" + str(o["lineno"]), "send_kind=" + str(o.get("send_kind")), "dispatch=" + m["entry_point"]["dispatch"],
          "path=" + str(m["reachability_path"]), "extra=" + str([(a["evidence"], a["lineno"]) for a in m.get("additional_observations", [])]),
          ("SUPPRESSED " + json.dumps(m["suppression"])) if m.get("suppression") else "")
print("suppression_warnings:", d.get("suppression_warnings"))
print("risks:", [r.get("id") for r in d.get("risks", [])])
