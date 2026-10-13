"""AuthGap manifest の 1 ツール 1 行の要約（unit / ann_form / ann / D_kind / 行の verdict）。"""
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
print("mcp_version:", json.dumps(d.get("mcp_version"), ensure_ascii=False))
for k in ("unresolved_handler", "dispatch_sites"):
    if d.get(k):
        print(k + ":", json.dumps(d.get(k), ensure_ascii=False))
for k in d:
    if k not in ("units",) and ("unjoin" in k or "literal" in k or "join" in k):
        print(k + ":", json.dumps(d[k], ensure_ascii=False))
for u in d["units"]:
    un = u["unit"]
    dk = u.get("D_kind") or {}
    dks = {k: dk[k] for k in ("bottom", "explicit", "unknown", "malformed") if k in dk}
    rows = [(r.get("kind"), r.get("lineno"), [v for v in r.get("verdicts", []) if v == "CONTRADICTION"],
             [n for n in (r.get("notes") or []) if n.startswith("contradiction")]) for r in u.get("rows", [])]
    print(f"UNIT tool={un.get('tool_name')} qual={un.get('qualname')} rel={un.get('relpath')} kind={un.get('entry_kind')} "
          f"fw={un.get('framework')} line={un.get('lineno')} form={un.get('annotation_form')} ann={un.get('annotations')} "
          f"D={json.dumps(dks)} reg={json.dumps(un.get('registration'))}")
    if un.get("dispatch_names") is not None:
        print("   dispatch_names=", un.get("dispatch_names"), "dispatch_join=", json.dumps(u.get("dispatch_join")))
    print("   effects=", [(e.get("site"), e.get("kind"), e.get("lineno"), e.get("witness_chain")) for e in u.get("effects", [])])
    print("   rows=", rows)
