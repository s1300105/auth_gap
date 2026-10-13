import json,sys
txt=open(sys.argv[1]).read()
d=json.loads(txt.split('\n決定論')[0])
print('d_op', json.dumps(d['d_op'],ensure_ascii=False))
for u in d['units']:
    un=u['unit']
    print('UNIT',un['unit_id'],'fw=',un['framework'],'kind=',un['entry_kind'],'tool_name=',repr(un['tool_name']),'ann=',un.get('annotations'),'form=',un.get('annotation_form'),'Dkind_bottom=',u['D_kind']['bottom'],'expl=',u['D_kind']['explicit'],'enf=',u['enforcement']['path'],u['enforcement']['verdict'], 'Dop_cov=',u.get('D_op_covers'))
    for r in u['rows']:
        print('   ROW',r['kind'],r['relpath'],'L',r['lineno'],r['verdicts'],'covered_by=',r['covered_by'],[n for n in r['notes'] if n.startswith('contra')])
print(txt.split('\n決定論')[1][:60] if '\n決定論' in txt else '')
