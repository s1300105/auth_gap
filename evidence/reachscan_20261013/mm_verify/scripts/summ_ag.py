import json, sys, os, glob
for f in sorted(glob.glob(os.path.join(sys.argv[1], "*.json"))):
    n = os.path.basename(f)[:-5]
    r = json.load(open(f))
    print(f"== {n} parse_failures={r.get('parse_failures')} units={len(r.get('units', []))} mcp={r.get('mcp_version',{}).get('class')}")
    for u in r.get("units", []):
        un = u["unit"]
        print(f"   U {un.get('tool_name') or un.get('qualname')} L{un.get('lineno')} ann={un.get('annotations')} form={un.get('annotation_form')} malformed={un.get('malformed_fields')} undet={un.get('undetermined_fields')} D_kind={u['D_kind']} opaque={u.get('opaque_reasons')} notes={u.get('notes')}")
        if u.get('dispatch_join'): print('     join', u['dispatch_join'])
        for e in u.get('effects', []):
            print(f"     E {e.get('kind')} {e.get('site')} L{e.get('lineno')} res={e.get('resolution')} chain={e.get('witness_chain')} http={e.get('http_method')} mode={e.get('fs_mode')} destr={e.get('destructive')}")
        for row in u.get("rows", []):
            cn = [x for x in (row.get("notes") or []) if x.startswith("contradiction")]
            print(f"     R {row.get('kind')} {row.get('site')} L{row.get('lineno')} {cn} verdicts={row.get('verdicts')}")
