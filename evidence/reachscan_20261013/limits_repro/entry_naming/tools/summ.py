import json, sys
for p in sys.argv[1:]:
    m = json.load(open(p))
    print("==", p.split("/")[-1], "| d_op:", {k: m["d_op"][k] for k in ("allow", "deny", "source")}, "| mcp_version:", m.get("mcp_version", {}).get("class"))
    for u in m["units"]:
        un = u["unit"]
        dk = u.get("D_kind", {})
        print(f"  UNIT {un['unit_id']} fw={un['framework']} kind={un['entry_kind']} tool_name={un['tool_name']!r} form={un.get('annotation_form')} D_explicit={dk.get('explicit')} bottom={dk.get('bottom')} enf={u['enforcement'].get('path')}/{u['enforcement'].get('verdict')} reg={un.get('registration')}")
        for r in u["rows"]:
            print(f"     ROW {r.get('kind')} L{r.get('lineno')} {sorted(r.get('verdicts', []))} covered_by={r.get('covered_by')} notes={[n for n in r.get('notes', []) if 'contradiction' in n]}")
