import json, sys
scan, probe = sys.argv[1], sys.argv[2]
d = json.load(open(scan))
try:
    p = json.load(open(probe))
    print("probe.annotations_join", p.get("annotations_join"))
except Exception as e:
    print("probe: unreadable", e)
for u in d["units"]:
    un = u["unit"]
    print("UNIT", un.get("framework"), un.get("qualname"), "@", un.get("relpath"), "tool_name=", un.get("tool_name"),
          "dispatch_names=", un.get("dispatch_names"))
    print("    D_kind", json.dumps(u["D_kind"], ensure_ascii=False))
    if "dispatch_join" in u:
        print("    dispatch_join", json.dumps(u["dispatch_join"], ensure_ascii=False))
        print("    D_kind_by_tool", json.dumps({k: v.get("explicit") for k, v in u["D_kind_by_tool"].items()}))
    effs = u.get("effects", [])
    for r in u["rows"]:
        print("    ROW", r["site"], r["kind"], "%s:%s" % (r["relpath"], r["lineno"]), "slot", r.get("slot"),
              "verdicts=", r["verdicts"], "notes=", r.get("notes"))
