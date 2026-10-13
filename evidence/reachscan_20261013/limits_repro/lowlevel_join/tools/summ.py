import json, sys
d = json.load(open(sys.argv[1]))
print("mcp_version", d.get("mcp_version", {}).get("class"), "unresolved_handler", d.get("unresolved_handler"))
for u in d["units"]:
    un = u["unit"]
    print("UNIT", un.get("unit_id"), "tool_name=", un.get("tool_name"), "dispatch_names=", un.get("dispatch_names"))
    for k in ("dispatch_annotations", "dispatch_unjoined", "annotation_form", "annotations", "malformed_fields"):
        if k in un:
            print("   ", k, "=", json.dumps(un[k], ensure_ascii=False))
    print("    D_kind", json.dumps(u["D_kind"], ensure_ascii=False))
    for k in ("D_kind_by_tool",):
        if k in u: print("   ", k, json.dumps(u[k]))
    print("    notes", u.get("notes"), "opaque", u.get("opaque_reasons"))
    enf = u.get("enforcement", {})
    if isinstance(enf, dict):
        for k, v in enf.items():
            if k in ("unjoined_literals", "dispatch_attribution", "d_kind_by_tool", "attribution"):
                print("    enf.", k, json.dumps(v, ensure_ascii=False))
    for r in u["rows"]:
        print("    ROW", r["site"], r["kind"], "line", r["lineno"], "slot", r.get("slot"), "verdicts=", r["verdicts"], "notes=", r.get("notes"), "attrib=", r.get("dispatch_attribution", r.get("tools")))
