import json, sys, glob, os
for f in sorted(glob.glob(os.path.join(sys.argv[1], "*.json"))):
    n = os.path.basename(f)[:-5]
    try:
        r = json.load(open(f))
    except Exception as e:
        print(f"== {n}: load failed {e}"); continue
    print(f"== {n} parse_failures={r.get('parse_failures')} units={len(r.get('units', []))}")
    for u in r.get("units", []):
        un = u["unit"]
        print(f"   U {un.get('tool_name')} ann={un.get('annotations')} D_kind={ {k: v for k, v in u['D_kind'].items() if k in ('explicit','upper','unknown','malformed','closed_world','idempotent','bottom')} } opaque={u.get('opaque_reasons')}")
        seen = set()
        for row in u.get("rows", []):
            cn = tuple(x for x in row.get("notes", []) if x.startswith("contradiction"))
            key = (row.get("site"), row.get("lineno"), cn)
            if key in seen: continue
            seen.add(key)
            print(f"     R {row.get('kind')} {row.get('site')} L{row.get('lineno')} {list(cn)} verdicts={row.get('verdicts')}")
