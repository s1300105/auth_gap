"""ケースごと・ツールごとに reachscan と AuthGap の結果を並べる（rs JSON と ag manifest を読むだけ）。"""
import json, os, sys
rs = json.load(open(sys.argv[1], encoding="utf-8"))
ag = json.load(open(sys.argv[2], encoding="utf-8"))
root = rs.get("target", "")
fid2f = {it["finding"]["finding_id"]: it["finding"] for it in rs["findings"]}
tools = {}
for ep in rs.get("py_entry_points", []):
    t = tools.setdefault(ep["name"], {"rs_mismatch": [], "rs_reach_findings": [], "ag": None})
    for fid in ep.get("reachable_findings", []):
        f = fid2f.get(fid)
        if f:
            t["rs_reach_findings"].append(f"{f['capability']}:{f['evidence']}@{f['lineno']}")
for m in rs.get("annotation_mismatches", []):
    t = tools.setdefault(m["tool"], {"rs_mismatch": [], "rs_reach_findings": [], "ag": None})
    t["rs_mismatch"].append(f"{m['rule']}({m['risk_level']}):{m['observed']['evidence']}@{m['observed']['lineno']}" + (" [suppressed]" if m.get("suppression") else ""))
for u in ag["units"]:
    name = u["unit"]["tool_name"]
    t = tools.setdefault(name, {"rs_mismatch": [], "rs_reach_findings": [], "ag": None})
    contra, unk = set(), set()
    for r in u.get("rows", []):
        for n in r.get("notes", []):
            if n.startswith("contradiction_reason:"):
                contra.add(f"{n.split(':',1)[1]}@{r['lineno']}")
            elif n.startswith("contradiction_unknown:"):
                unk.add(f"{n.split(':',1)[1]}@{r['lineno']}")
    t["ag"] = {"effects": [f"{e['site']}:{e['kind']}@{e['lineno']}({e['resolution']})" for e in u.get("effects", [])],
               "CONTRA": sorted(contra), "CONTRA_UNKNOWN": sorted(unk), "opaque_reasons": u.get("opaque_reasons")}
other = [f"{f['capability']}:{f['evidence']}@{os.path.relpath(f['file'], root)}:{f['lineno']}={f['reachability']}"
         for f in fid2f.values() if f.get("reachability") != "reachable"]
print(json.dumps({"tools": tools, "rs_not_reachable_findings": other}, ensure_ascii=False, indent=1))
