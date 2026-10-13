import json, sys
for path in sys.argv[1:]:
    r = json.load(open(path))
    print("=====", path.rsplit("/",1)[-1], "py_files", r.get("num_files_scanned"))
    for e in r["findings"]:
        f = e["finding"]
        print("  F", e["detector"], f["capability"], repr(f["evidence"]), f["lineno"], f.get("reachability"), f.get("entry_point_name"))
    for m in r.get("annotation_mismatches", []):
        obs = [m["observed"]] + m.get("additional_observations", [])
        print("  M", m["tool"], m["rule"], m["risk_level"], [(o["capability"], o["evidence"], o["lineno"], o.get("send_kind")) for o in obs])
    print("  EP", [e.get("name") for e in r.get("py_entry_points", [])])
