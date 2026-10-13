import json, sys
d = json.load(open(sys.argv[1]))
print("parse_failures", d.get("parse_failures"), "truncations", d.get("truncations"))
for u in sorted(d["units"], key=lambda u: u["unit"]["lineno"]):
    un = u["unit"]
    print(f"== {un['tool_name']} ann={un['annotations']} D={u["D_kind"]}")
    print("   effects:", [(e["kind"], e["site"], e["form"], e["lineno"], e["resolution"] if isinstance(e["resolution"], str) else e["resolution"]) for e in u["effects"]])
    print("   opaque_reasons:", u["opaque_reasons"], " unresolved_in_tree:", u["unresolved_in_tree_calls"], " notes:", u["notes"])
    for r in u["rows"]:
        print("   row:", r["kind"], r["site"], r["slot"], r["verdicts"], r["notes"])
