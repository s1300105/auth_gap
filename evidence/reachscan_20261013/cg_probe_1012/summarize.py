import json, sys, pathlib
for p in sorted(pathlib.Path(sys.argv[1]).glob("*.json")):
    d = json.loads(p.read_text())
    print("==", p.stem, "eps:", [e.get("name") for e in d.get("py_entry_points", [])])
    for f in d.get("findings", []):
        f = f.get("finding", f)
        print("   ", f.get("capability"), f.get("evidence"), "L%s" % f.get("lineno"), f.get("reachability"), f.get("reachability_path"))
    for m in d.get("annotation_mismatches", []):
        print("   MISMATCH", m.get("rule"), m.get("tool"), m.get("risk_level"), [o.get("evidence") for o in [m.get("observation", {})]], m.get("observations") and len(m.get("observations")))
    err = (p.parent / (p.stem + ".stderr")).read_text().strip()
    if err:
        print("   STDERR:", err.replace("\n", " | ")[:400])
