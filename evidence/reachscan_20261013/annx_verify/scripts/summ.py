import json, sys
d = json.load(open(sys.argv[1]))
for ep in d.get("py_entry_points", []):
    a = ep.get("annotations")
    short = None
    if a:
        short = {"declared": a["declared"], "unres_ref": a["unresolved_reference"],
                 **{k: (a[k]["value"], a[k]["source"]) for k in ("readOnlyHint","destructiveHint","idempotentHint","openWorldHint")}}
    dt = [{"name": t["name"], **{k: (t["annotations"][k]["value"], t["annotations"][k]["source"]) for k in ("readOnlyHint","destructiveHint")}} for t in ep.get("declared_tools", [])]
    print("EP", ep["name"], ep["lineno"], ep["framework"], ep["confidence"], "ann=", short, "decl=", dt)
for m in d.get("annotation_mismatches", []):
    print("MM", m["rule"], m["tool"], m["entry_point"]["dispatch"], m["observed"]["evidence"])
print("n_ep", len(d.get("py_entry_points", [])), "n_mm", len(d.get("annotation_mismatches", [])))
