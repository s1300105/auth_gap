import json, sys, pathlib
for p in sorted(pathlib.Path(sys.argv[1]).glob("*.manifest.json")):
    d = json.loads(p.read_text())
    print("==", p.name.split(".")[0], "truncations:", d.get("truncations"))
    for u in d["units"]:
        print("  unit", u["unit"]["tool_name"], "opaque_reasons", u.get("opaque_reasons"), "cap_hits", u.get("cap_hits"), "unresolved_in_tree", u.get("unresolved_in_tree_calls"), "notes", u.get("notes"))
        for e in u["effects"]:
            print("    eff", e["kind"], e["site"], "L%s" % e["lineno"], e["resolution"], e.get("witness_chain"))
        for r in u.get("rows", []):
            print("    row", r["site"], "L%s" % r["lineno"], r["verdicts"], [n for n in r["notes"] if n.startswith("contradiction")])
