import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
print("dispatch_sites:", [(s["form"], s["lineno"], s["resolution"], s["candidates"]) for s in d.get("dispatch_sites", [])])
for u in d["units"]:
    un = u["unit"]
    contra = sorted({n for r in u.get("rows", []) for n in r.get("notes", []) if n.startswith("contradiction")})
    print(f"UNIT {un.get('tool_name')} opaque={u.get('opaque_reasons')} cap_hits={u.get('cap_hits')} uitc={u.get('unresolved_in_tree_calls')}")
    for e in u.get("effects", []):
        print(f"   EFFECT {e.get('site')} {e.get('kind')} {e.get('relpath', '')}:{e.get('lineno')} res={e.get('resolution')} chain={e.get('witness_chain')}")
    for r in u.get("rows", []):
        print(f"   ROW {r.get('site')} {r.get('slot')} L{r.get('lineno')} {r.get('verdicts')}")
    if contra: print("   NOTES", contra)
