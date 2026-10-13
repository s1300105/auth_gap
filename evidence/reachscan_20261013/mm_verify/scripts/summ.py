import json, sys, os
d = sys.argv[1]
for fn in sorted(os.listdir(d)):
    if not fn.endswith('.json'): continue
    r = json.load(open(os.path.join(d, fn)))
    print('=====', fn, 'files', r.get('num_files_scanned'), 'ts', r.get('num_ts_files_scanned'), 'eps', r.get('entry_points_detected'))
    for ep in r.get('py_entry_points', []):
        ann = ep.get('annotations')
        a = {k: (v['value'], v['source']) for k, v in ann.items() if isinstance(v, dict)} if ann else None
        print('  EP', ep['name'], ep['lineno'], ep['pattern_type'], a)
        for t in ep.get('declared_tools', []):
            print('    TOOL', t['name'], t['lineno'], {k: (v['value'], v['source']) for k, v in t['annotations'].items() if isinstance(v, dict)})
    for ep in r.get('ts_entry_points', []):
        print('  TSEP', ep.get('name'), ep.get('lineno'))
    for it in r['findings']:
        f = it['finding']
        print('  F', it['detector'], f['capability'], repr(f['evidence']), f['lineno'], f['reachability'], f.get('reachability_path'), f.get('risk_level'), 'SUPP' if f.get('suppression') else '')
    for m in r['annotation_mismatches']:
        print('  M', m['tool'], m['rule'], m['risk_level'], m['observed']['capability'], repr(m['observed']['evidence']), m['observed']['lineno'], m['reachability_path'], 'addl=', [(o['capability'], o['evidence'], o['lineno'], o['reachability_path']) for o in m['additional_observations']], 'supp=', m.get('suppression'), 'id=', m['mismatch_id'], 'ep=', m['entry_point'])
    print('  keys', sorted(r.keys()))
