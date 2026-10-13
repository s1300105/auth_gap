import json, sys
for path in sys.argv[1:]:
    r = json.load(open(path))
    print("=====", path.rsplit("/",1)[-1], "py_files", r.get("num_files_scanned"))
    print("-- findings (cap, evidence, line, reachability, entry)")
    for e in r["findings"]:
        f = e["finding"]
        print("  ", e["detector"], f["capability"], repr(f["evidence"]), f["lineno"], f.get("reachability"), f.get("entry_point_name"))
    print("-- mismatches (tool, rule, observed + additional)")
    for m in r.get("annotation_mismatches", []):
        obs = [m["observed"]] + m.get("additional_observations", [])
        print("  ", m["tool"], m["rule"], [(o["capability"], o["evidence"], o["lineno"]) for o in obs])
    eps = r.get("py_entry_points", [])
    print("-- entry points", [(ep.get("name"), (ep.get("annotations") or {}).get("readOnlyHint")) for ep in eps][:20])
