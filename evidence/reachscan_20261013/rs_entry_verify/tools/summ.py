import json, sys
for p in sys.argv[1:]:
    try:
        d = json.load(open(p))
    except Exception as e:
        print(p, "ERR", e); continue
    print("=====", p.split("/")[-1], "files", d.get("num_files_scanned"), "eps", d.get("entry_points_detected"))
    for ep in d.get("py_entry_points", []):
        ann = ep.get("annotations")
        ro = ann and ann.get("readOnlyHint")
        print("  EP", ep["name"], ep["file"].split("/")[-1]+":"+str(ep["lineno"]), ep["framework"], ep["confidence"], ep["pattern_type"], "ann.ro=", ro, "unres=", ann and ann.get("unresolved_reference"))
        for t in ep.get("declared_tools", []):
            print("     DECL", t["name"], t["lineno"], t["annotations"]["readOnlyHint"])
    for f in d.get("findings", []):
        ff = f["finding"]
        print("  F", ff.get("capability"), ff.get("evidence"), ff.get("file","").split("/")[-1]+":"+str(ff.get("lineno")), ff.get("reachability"), ff.get("reachability_path"))
    for m in d.get("annotation_mismatches", []):
        print("  MM", m["tool"], m["rule"], m["observed"]["evidence"], m["observed"]["lineno"], m["reachability_path"], "extra", [(o["evidence"], o["lineno"]) for o in m.get("additional_observations", [])])
    print("  keys:", sorted(d.keys()))
