import json, sys, glob, os
for f in sorted(glob.glob(os.path.join(sys.argv[1], "*.json"))):
    n = os.path.basename(f)[:-5]
    try:
        r = json.load(open(f))
    except Exception as e:
        print(f"== {n}: JSON load failed {e}"); continue
    print(f"== {n}  files={r.get('num_files_scanned')} ts_files={r.get('num_ts_files_scanned')} eps={r.get('entry_points_detected')}")
    for ep in r.get("py_entry_points", []):
        ann = ep.get("annotations")
        dt = ep.get("declared_tools")
        print(f"   EP {ep.get('name')} L{ep.get('lineno')} fw={ep.get('framework')} ann={'-' if ann is None else {k:(v['value'],v['source'][0]) for k,v in ann.items() if isinstance(v,dict)}} decl={[ (t['name'], {k:(v['value'],v['source'][0]) for k,v in t['annotations'].items() if isinstance(v,dict)}) for t in (dt or [])]}")
    for it in r.get("findings", []):
        fd = it["finding"]
        print(f"   F {fd.get('capability'):8} {fd.get('reachability')!s:15} {fd.get('evidence')} @L{fd.get('lineno')} risk={fd.get('risk_level')} supp={bool(fd.get('suppression'))}")
    for m in r.get("annotation_mismatches", []):
        o = m["observed"]
        print(f"   M [{m['risk_level']}] {m['tool']} {m['rule']} {m['declared']} <- {o['capability']} {o['evidence']} L{o['lineno']} send_kind={o.get('send_kind')} path={m['reachability_path']} dispatch={m['entry_point']['dispatch']} extra={[ (x['capability'],x['evidence'],x['lineno']) for x in m['additional_observations']]} supp={m.get('suppression')} id={m['mismatch_id']}")
    if r.get("suppression_warnings"):
        print("   SW", r["suppression_warnings"])
