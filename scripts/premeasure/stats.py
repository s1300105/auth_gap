import json,sys
from collections import Counter, defaultdict
import statistics as st

CK = ["enum","pattern","format","path_type","numeric","length","contype"]
def load(p): return json.load(open(p))

def tool_kinds(t):
    k=set()
    for p in t["params"]: k|=set(p["kinds"])
    return k

def anno(t):
    # only real MCP annotation fields count
    f=set(t.get("ann_fields") or [])
    real = f & {"readOnlyHint","destructiveHint","idempotentHint","openWorldHint","title"}
    return t["annotations"] and bool(real | (set() if f else set()))

def report(path,label):
    d=load(path)
    print(f"\n===== {label}: n_entries={len(d)}  repos={len(set(t['repo'] for t in d))}")
    withp=[t for t in d if t["params"]]
    print(f"entries with >=1 param: {len(withp)} ({len(withp)/len(d):.1%})")
    tot_params=sum(len(t["params"]) for t in d)
    print(f"total params: {tot_params}")
    # tool level
    rows=[]
    def pct(n,dn): return f"{n} / {dn} = {n/dn:.1%}" if dn else "-"
    n=len(withp)
    for k in CK:
        c=sum(1 for t in withp if k in tool_kinds(t))
        rows.append((k,c))
    anyc=sum(1 for t in withp if tool_kinds(t) & set(CK))
    anyc_noscalar=sum(1 for t in withp if tool_kinds(t) & {"enum","pattern","format","path_type"})
    annotated=sum(1 for t in withp if any(p["type"] not in ("none","?") for p in t["params"]))
    desconly=sum(1 for t in withp if any(p["desc"] for p in t["params"]) and not (tool_kinds(t)&set(CK)))
    mcpann=sum(1 for t in d if t["annotations"])
    retd=sum(1 for t in d if t["return_direct"])
    appr=sum(1 for t in d if t["approval"])
    print("-- tool-level presence (denominator = entries with >=1 param) --")
    for k,c in rows: print(f"  {k:10s} {pct(c,n)}")
    print(f"  ANY-constraint          {pct(anyc,n)}")
    print(f"  ANY domain(enum/pattern/format/path) {pct(anyc_noscalar,n)}")
    print(f"  any-typed-param         {pct(annotated,n)}")
    print(f"  desc-only (no constraint) {pct(desconly,n)}")
    print(f"  MCP annotations=        {pct(mcpann,len(d))}")
    print(f"  return_direct=          {pct(retd,len(d))}")
    print(f"  approval kw=            {pct(appr,len(d))}")
    # param level
    pc=Counter(); ptypes=Counter()
    for t in d:
        for p in t["params"]:
            ptypes[p["type"]]+=1
            for k in p["kinds"]: pc[k]+=1
            if not p["kinds"]: pc["NONE"]+=1
    print("-- param-level --")
    for k,c in pc.most_common(): print(f"  {k:10s} {c} ({c/tot_params:.1%})")
    print("  top types:", ptypes.most_common(12))
    # dangerous subset
    dang=[t for t in d if t["effects"]]
    print(f"-- entries with detected dangerous effect: {len(dang)} ({len(dang)/len(d):.1%})")
    ek=Counter()
    for t in dang:
        for e in t["effects"]: ek[e]+=1
    print("   effect kinds:", ek.most_common())
    dctl=[t for t in dang if t["ctrl_params"]]
    print(f"   with >=1 model-controlled ctrl param (syntactic): {len(dctl)} ({len(dctl)/max(1,len(dang)):.1%})")
    for k in CK+["ANY","DOMAIN"]:
        if k=="ANY": c=sum(1 for t in dctl if any(set(p["kinds"])&set(CK) for p in t["params"] if p["name"] in t["ctrl_params"]))
        elif k=="DOMAIN": c=sum(1 for t in dctl if any(set(p["kinds"])&{"enum","pattern","format","path_type"} for p in t["params"] if p["name"] in t["ctrl_params"]))
        else: c=sum(1 for t in dctl if any(k in p["kinds"] for p in t["params"] if p["name"] in t["ctrl_params"]))
        print(f"   ctrl-param {k:10s} {pct(c,len(dctl))}")
    # per repo
    byrepo=defaultdict(list)
    for t in d: byrepo[t["repo"]].append(t)
    per=[]
    for r,ts in sorted(byrepo.items()):
        tw=[t for t in ts if t["params"]]
        if not tw: continue
        a=sum(1 for t in tw if tool_kinds(t)&set(CK))/len(tw)
        dm=sum(1 for t in tw if tool_kinds(t)&{"enum","pattern","format","path_type"})/len(tw)
        an=sum(1 for t in ts if t["annotations"])/len(ts)
        per.append((r,len(ts),a,dm,an))
    print("-- per repo (n, any-constraint, domain-constraint, mcp-annotations) --")
    for r,nn,a,dm,an in per: print(f"   {r:45s} {nn:5d} {a:6.1%} {dm:6.1%} {an:6.1%}")
    if per:
        print(f"   MEDIAN across repos: any={st.median([x[2] for x in per]):.1%} domain={st.median([x[3] for x in per]):.1%} mcpann={st.median([x[4] for x in per]):.1%}")
        print(f"   repos with >=1 annotated tool: {sum(1 for x in per if x[4]>0)}/{len(per)}")

report(sys.argv[1], sys.argv[2])
