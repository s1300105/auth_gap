import json, sys
m = json.load(open(sys.argv[1]))
print("mcp_version:", m.get("mcp_version", {}).get("class"))
for u in m["units"]:
    un = u["unit"]
    print(f"UNIT {un['tool_name']} L{un['lineno']} form={un.get('annotation_form')} ann={un.get('annotations')} "
          f"und={un.get('undetermined_fields')} disp={un.get('dispatch_annotations')}")
    print("   D_kind:", json.dumps(u["D_kind"], ensure_ascii=False, sort_keys=True))
    if "D_kind_by_tool" in u:
        print("   D_kind_by_tool:", json.dumps(u["D_kind_by_tool"], ensure_ascii=False, sort_keys=True))
    for r in u["rows"]:
        print(f"   ROW L{r['lineno']} {r['site']} {r['kind']} verdicts={r['verdicts']} notes={[n for n in r.get('notes', []) if 'contra' in n]}")
