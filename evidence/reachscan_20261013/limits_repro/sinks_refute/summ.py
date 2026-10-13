import json,sys
d=json.load(open(sys.argv[1]))
for u in d['units']:
    print('==', u['unit'].get('tool_name') if isinstance(u['unit'],dict) else u['unit'], 'D', u['D_kind'].get('explicit'), 'opaque', u.get('opaque_reasons'))
    for e in u['effects']:
        print('  eff', e['kind'], e['site'], e['lineno'], e['resolution'], {k:(v.get('prin'),v.get('prov')) for k,v in e['slots'].items()})
    for r in u.get('rows', []):
        print('  row', r.get('kind'), r.get('site'), r.get('slot'), r.get('verdicts'), r.get('notes'))
