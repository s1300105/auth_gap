import json, sys
for p in sys.argv[1:]:
    d = json.load(open(p))
    print("=====", p.split("/")[-1], "units", len(d.get("units", [])), "pf", d.get("parse_failures"))
    for u in d["units"]:
        un = u["unit"]
        print("  U", un.get("unit_id"), "names", un.get("dispatch_names"), "unjoined", un.get("dispatch_unjoined"), "opaque", u.get("opaque_reasons"))
        dj = u.get("dispatch_join")
        if dj: print("    attr", dj.get("attribution"), "all", dj.get("effects_all_tools"))
        for r in u.get("rows", []):
            print("    R", r.get("lineno"), r.get("site"), r.get("verdicts"))
