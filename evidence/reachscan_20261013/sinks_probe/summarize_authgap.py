import json, sys
for path in sys.argv[1:]:
    d = json.load(open(path))
    print("=====", path.rsplit("/", 1)[-1], "parse_failures:", d.get("parse_failures"))
    for u in d["units"]:
        name = u["unit"].get("qualname")
        effs = [(e["kind"], e["site"], e["lineno"], e.get("destructive"), e.get("fs_mode"), e.get("http_method"), e.get("resolution")) for e in u["effects"]]
        notes = sorted({n for r in u["rows"] for n in r.get("notes", []) if n.startswith("contradiction")})
        verdicts = sorted({v for r in u["rows"] for v in r.get("verdicts", [])})
        print(f"  {name}: effects={effs}")
        print(f"      contra={notes} verdicts={verdicts}")
