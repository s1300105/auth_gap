import ast,os,sys,json
sys.path.insert(0,os.path.dirname(__file__))
from scan import dotted, danger_kind, schema_props, ann_field_list, FileInfo
from collections import defaultdict, Counter

def str_consts(test):
    """names compared against in `name == "x"` / `name in ("a","b")`"""
    out=set()
    for n in ast.walk(test):
        if isinstance(n, ast.Compare):
            for c in [n.left]+list(n.comparators):
                if isinstance(c, ast.Constant) and isinstance(c.value,str): out.add(c.value)
                elif isinstance(c,(ast.Tuple,ast.List,ast.Set)):
                    for e in c.elts:
                        if isinstance(e,ast.Constant) and isinstance(e.value,str): out.add(e.value)
    return out

def arg_keys(node):
    """keys read out of the arguments dict inside this node"""
    ks=set()
    for n in ast.walk(node):
        if isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Constant) and isinstance(n.slice.value,str):
            ks.add(n.slice.value)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr=="get" and n.args:
            a=n.args[0]
            if isinstance(a, ast.Constant) and isinstance(a.value,str): ks.add(a.value)
        if isinstance(n, ast.Call) and dotted(n.func).split(".")[-1] in ("model_validate","parse_obj") :
            pass
    return ks

def branch_effects(node):
    kinds=set(); ctrl=set()
    for n in ast.walk(node):
        if isinstance(n, ast.Call):
            k=danger_kind(n.func)
            if k:
                kinds.add(k)
                for a in list(n.args)+[kw.value for kw in n.keywords]:
                    ctrl |= arg_keys(a)
    return kinds, ctrl

def scan_repo(root, label):
    schemas={}   # name -> (params, ann_fields, file)
    branches=defaultdict(lambda: [set(), set()])  # name -> (effects, ctrl keys)
    for dp,dns,fns in os.walk(root):
        dns[:]=[d for d in dns if d not in ('.git','__pycache__','node_modules','tests','test','docs')]
        for f in fns:
            if not f.endswith('.py') or f.startswith('test_'): continue
            p=os.path.join(dp,f)
            try: src=open(p,encoding='utf-8',errors='replace').read()
            except Exception: continue
            if 'inputSchema' not in src and 'call_tool' not in src: continue
            try: tree=ast.parse(src)
            except Exception: continue
            rel=os.path.relpath(p,root)
            for n in ast.walk(tree):
                if isinstance(n, ast.Call) and dotted(n.func).split('.')[-1] in ('Tool','ToolDef'):
                    kws={kw.arg:kw.value for kw in n.keywords if kw.arg}
                    sch=kws.get('inputSchema') or kws.get('input_schema')
                    nm=kws.get('name')
                    if sch is None or not isinstance(nm, ast.Constant): continue
                    schemas[str(nm.value)]=(schema_props(sch), ann_field_list(kws['annotations']) if 'annotations' in kws else [], rel)
            # call_tool handlers
            for n in ast.walk(tree):
                if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)):
                    decos=[dotted(d.func if isinstance(d,ast.Call) else d) for d in n.decorator_list]
                    if not (any(d.split('.')[-1]=='call_tool' for d in decos) or n.name in ('call_tool','handle_call_tool','_call_tool')):
                        continue
                    for st in ast.walk(n):
                        if isinstance(st, ast.If):
                            names=str_consts(st.test)
                            if not names: continue
                            k,c=branch_effects(ast.Module(body=st.body,type_ignores=[]))
                            for nm in names:
                                branches[nm][0]|=k; branches[nm][1]|=c
                        if isinstance(st, ast.Match):
                            for case in st.cases:
                                nms=set()
                                for pn in ast.walk(case.pattern):
                                    if isinstance(pn, ast.MatchValue) and isinstance(pn.value, ast.Constant) and isinstance(pn.value.value,str):
                                        nms.add(pn.value.value)
                                if not nms: continue
                                k,c=branch_effects(ast.Module(body=case.body,type_ignores=[]))
                                for nm in nms:
                                    branches[nm][0]|=k; branches[nm][1]|=c
    return schemas, branches

DOM={'enum','pattern','format'}
ALL=DOM|{'numeric','length'}
tot=Counter()
detail=[]
base=sys.argv[1]
for d in sorted(os.listdir(base)):
    full=os.path.join(base,d)
    if not os.path.isdir(full): continue
    schemas,branches=scan_repo(full,d)
    joined=set(schemas)&set(branches)
    tot['schemas']+=len(schemas); tot['branches']+=len(branches); tot['joined']+=len(joined)
    for nm in sorted(joined):
        params,ann,rel=schemas[nm]
        eff,ctrl=branches[nm]
        if not eff: continue
        tot['dangerous']+=1
        pk={p['name']:set(p['kinds']) for p in params}
        ctrl_named = ctrl & set(pk)
        if ctrl_named: tot['dang_with_named_ctrl']+=1
        dom=any(pk.get(c,set())&DOM for c in ctrl_named)
        anyc=any(pk.get(c,set())&ALL for c in ctrl_named)
        annf=set(ann)&{'readOnlyHint','destructiveHint','idempotentHint','openWorldHint'}
        if dom: tot['ctrl_dom']+=1
        if anyc: tot['ctrl_any']+=1
        if annf: tot['ann']+=1
        if dom or annf: tot['D_either']+=1
        detail.append((d,nm,sorted(eff),sorted(ctrl_named),{c:sorted(pk.get(c,[])) for c in ctrl_named},sorted(annf)))
print(dict(tot))
n=tot['dangerous'] or 1
print(f"joined dangerous low-level tools: {tot['dangerous']}")
print(f"  domain constraint on ctrl key: {tot['ctrl_dom']} ({tot['ctrl_dom']/n:.1%})")
print(f"  any constraint on ctrl key:    {tot['ctrl_any']} ({tot['ctrl_any']/n:.1%})")
print(f"  explicit annotation:           {tot['ann']} ({tot['ann']/n:.1%})")
print(f"  D either:                      {tot['D_either']} ({tot['D_either']/n:.1%})")
for x in detail[:25]: print("   ",x)
