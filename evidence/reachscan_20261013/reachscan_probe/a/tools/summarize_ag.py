"""AuthGap manifest の要約（tool / 宣言 / 効果 / 行の verdict と notes）。"""
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
print("dispatch_sites:", json.dumps(d.get("dispatch_sites"), ensure_ascii=False))
print("unresolved_handler:", json.dumps(d.get("unresolved_handler"), ensure_ascii=False))
print("parse_failures:", d.get("parse_failures"), "truncations:", d.get("truncations"))
for u in d["units"]:
    un = u["unit"]
    print("=" * 70)
    print("UNIT", un.get("tool_name"), "qual=", un.get("qualname"), "entry_kind=", un.get("entry_kind"),
          "line=", un.get("lineno"), "ann_form=", un.get("annotation_form"), "ann=", un.get("annotations"))
    for k in ("dispatch_names", "dispatch_join", "d_kind_by_tool", "joined_tools", "unjoined_literals"):
        if k in un:
            print("  unit.%s =" % k, json.dumps(un[k], ensure_ascii=False))
    for k in u:
        if k.startswith("dispatch") or k.startswith("d_kind"):
            print("  %s =" % k, json.dumps(u[k], ensure_ascii=False))
    print("  D_kind:", json.dumps(u.get("D_kind"), ensure_ascii=False))
    print("  trig:", u.get("trig"), "opaque_reasons:", u.get("opaque_reasons"), "notes:", u.get("notes"))
    print("  unresolved_in_tree_calls:", u.get("unresolved_in_tree_calls"))
    for e in u.get("effects", []):
        print("  EFFECT", e.get("site"), e.get("kind"), e.get("sub_kind"), "line", e.get("lineno"),
              "destructive=", e.get("destructive", "-"), "fs_mode=", e.get("fs_mode", "-"),
              "res=", e.get("resolution"), "form=", e.get("form"), "chain=", e.get("witness_chain"),
              "attributed=", e.get("attributed", "-"), "opaque=", e.get("opaque", "-"))
    for r in u.get("rows", []):
        print("  ROW", r.get("site"), r.get("kind"), r.get("slot"), "line", r.get("lineno"),
              "verdicts=", r.get("verdicts"), "covered_by=", r.get("covered_by"),
              "D_layer=", r.get("D_layer_present"), "notes=", r.get("notes"),
              "attributed=", r.get("attributed", "-"))
